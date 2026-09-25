// Função da Vercel: lê e grava o documento do dashboard no Upstash Redis
// (Vercel → Storage → Upstash for Redis). Sem dependências: usa a API REST.
//
//   GET  /api/data  → { version, updatedAt, data } ou { version: 0, data: null }
//   POST /api/data  ← { data, baseVersion }  → { version, updatedAt }
//                     409 se alguém salvou depois da versão que você carregou
const KEY = "controle-demandas:dados";
const MAX_BYTES = 900 * 1024;

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  const url = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
  const token = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;
  if (!url || !token) {
    return res.status(503).json({ erro: "Banco de dados não configurado na Vercel (faltam KV_REST_API_URL e KV_REST_API_TOKEN)." });
  }

  const redis = async (cmd, body) => {
    const r = await fetch(`${url.replace(/\/$/, "")}/${cmd}`, {
      method: body === undefined ? "GET" : "POST",
      headers: { Authorization: `Bearer ${token}` },
      body,
    });
    const j = await r.json().catch(() => ({}));
    if (!r.ok || j.error) throw new Error(j.error || `Upstash respondeu ${r.status}`);
    return j.result;
  };
  const ler = async () => {
    const raw = await redis(`get/${encodeURIComponent(KEY)}`);
    return raw ? JSON.parse(raw) : { version: 0, updatedAt: null, data: null };
  };

  try {
    if (req.method === "GET") return res.status(200).json(await ler());

    if (req.method === "POST") {
      let body = req.body;
      if (typeof body === "string") body = JSON.parse(body || "{}");
      const data = body && body.data;
      if (!data || typeof data !== "object" || !Array.isArray(data.projetos) || !Array.isArray(data.secoes)) {
        return res.status(400).json({ erro: "Formato inválido: esperado { data: { projetos: [], secoes: [] } }." });
      }
      const atual = await ler();
      if ((Number(body.baseVersion) || 0) !== (atual.version || 0)) {
        return res.status(409).json({ erro: "Os dados foram alterados por outra pessoa. Recarregue a página.", version: atual.version });
      }
      const doc = { version: (atual.version || 0) + 1, updatedAt: new Date().toISOString(), data };
      const texto = JSON.stringify(doc);
      if (Buffer.byteLength(texto) > MAX_BYTES) return res.status(413).json({ erro: "Dados grandes demais para salvar." });
      await redis(`set/${encodeURIComponent(KEY)}`, texto);
      return res.status(200).json({ version: doc.version, updatedAt: doc.updatedAt });
    }

    res.setHeader("Allow", "GET, POST");
    return res.status(405).json({ erro: "Método não permitido." });
  } catch (e) {
    return res.status(500).json({ erro: `Falha ao acessar o banco: ${e.message}` });
  }
};
