/* Controle de Demandas — dados, armazenamento e cálculos compartilhados
   entre o dashboard (index.html) e o painel de edição (admin/). */
(function (g) {
  "use strict";
  const DAY = 864e5;
  const LS_KEY = "controle-demandas-dados";
  const API = "/api/data";

  const CAMPOS = {
    responsavel: "Responsável", especialidade: "Especialidade", tipo: "Tipo de Demanda",
    etapa: "Etapa", status: "Status", incidente: "Incidente Operacional", motivo: "Motivo do Bloqueio",
  };
  // campo do projeto → lista de opções que o alimenta
  const LISTA_DO_CAMPO = {
    responsavel: "pessoas", especialidade: "especialidades", tipo: "tipos", etapa: "etapas",
    status: "status", incidente: "incidentes", motivo: "motivos",
  };
  const CATEGORIAS = { afazer: "A fazer", andamento: "Em andamento", bloqueado: "Bloqueado", concluido: "Concluído" };
  const ESCOPOS = { todos: "Todos os projetos", ativos: "Somente ativos (não concluídos)", concluidos: "Somente concluídos" };
  const OPS = { igual: "é igual a", diferente: "é diferente de", preenchido: "está preenchido", vazio: "está vazio" };

  const uid = () => Math.random().toString(36).slice(2, 10);
  const pad = n => String(n).padStart(2, "0");
  const iso = d => d ? `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}` : "";
  const parseData = s => {
    if (!s) return null;
    const m = String(s).match(/^(\d{4})-(\d{2})-(\d{2})/);
    return m ? new Date(+m[1], +m[2] - 1, +m[3], 12) : null;
  };
  const hoje = () => { const d = new Date(); d.setHours(12, 0, 0, 0); return d; };
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const clone = o => JSON.parse(JSON.stringify(o));

  /* ---------- tipos de widget ---------- */
  // campos: esquema do formulário de configuração no admin
  const FILTRO = { k: "filtro", label: "Filtro", tipo: "filtro" };
  const ESCOPO = { k: "escopo", label: "Quais projetos", tipo: "select", opcoes: ESCOPOS };
  const TIPOS_WIDGET = {
    kpi_pontualidade: { nome: "Cartão · Índice de Pontualidade", largura: "pequeno", campos: [FILTRO] },
    kpi_tempo: { nome: "Cartão · Tempo médio (criação → entrega)", largura: "pequeno", campos: [FILTRO] },
    kpi_contagem: { nome: "Cartão · Contagem de projetos", largura: "pequeno", campos: [ESCOPO, FILTRO] },
    kpi_manual: {
      nome: "Cartão · Número digitado", largura: "pequeno", campos: [
        { k: "valor", label: "Valor", tipo: "text" },
        { k: "unidade", label: "Unidade (ex.: %, dias, R$)", tipo: "text" },
        { k: "legenda", label: "Texto abaixo do número", tipo: "text" },
      ],
    },
    grafico: {
      nome: "Gráfico · Contagem agrupada", largura: "medio", campos: [
        { k: "agrupar", label: "Agrupar por", tipo: "select", opcoes: CAMPOS },
        { k: "forma", label: "Formato", tipo: "select", opcoes: { barras: "Barras horizontais", colunas: "Colunas verticais", rosca: "Rosca" } },
        ESCOPO, FILTRO,
      ],
    },
    vazao: {
      nome: "Gráfico · Vazão (concluídos por período)", largura: "medio", campos: [
        { k: "agrupamento", label: "Agrupar por", tipo: "select", opcoes: { 7: "Semana", 14: "Quinzena", 30: "Mês (30 dias)" } },
        { k: "periodos", label: "Quantidade de períodos", tipo: "number" },
        FILTRO,
      ],
    },
    alocacao: {
      nome: "Gráfico · Alocação por responsável", largura: "medio", campos: [
        { k: "empilhar", label: "Empilhar por", tipo: "select", opcoes: { etapa: "Etapa", especialidade: "Especialidade", status: "Status", tipo: "Tipo de Demanda" } },
        FILTRO,
      ],
    },
    tabela: { nome: "Tabela · Lista de projetos", largura: "grande", campos: [ESCOPO, FILTRO] },
  };

  function novoWidget(tipo) {
    const t = TIPOS_WIDGET[tipo];
    const base = { id: uid(), tipo, titulo: t.nome.split("· ")[1] || t.nome, descricao: "", visivel: true, largura: t.largura, config: {} };
    const c = base.config;
    if (tipo === "kpi_contagem" || tipo === "tabela") c.escopo = "todos";
    if (tipo === "kpi_manual") Object.assign(c, { valor: "0", unidade: "", legenda: "" });
    if (tipo === "grafico") Object.assign(c, { agrupar: "etapa", forma: "colunas", escopo: "ativos" });
    if (tipo === "vazao") Object.assign(c, { agrupamento: 7, periodos: 12 });
    if (tipo === "alocacao") c.empilhar = "etapa";
    return base;
  }

  /* ---------- documento padrão ---------- */
  function secoesPadrao() {
    const w = (tipo, titulo, descricao, config = {}, extra = {}) => Object.assign(novoWidget(tipo), { titulo, descricao }, extra, { config: Object.assign(novoWidget(tipo).config, config) });
    return [
      { id: uid(), titulo: "KPIs de Saúde e Ritmo", widgets: [
        w("kpi_pontualidade", "Índice de Pontualidade", "Concluídos até a Data de Fechamento Esperada"),
        w("kpi_tempo", "Tempo Médio · Novos Produtos", "Criação → entrega, concluídos", { filtro: { campo: "tipo", op: "igual", valor: "Novo Produto" } }),
        w("kpi_tempo", "Tempo Médio · Ajustes", "Abertura do ajuste → entrega", { filtro: { campo: "tipo", op: "igual", valor: "Ajuste/Customização" } }),
        w("kpi_contagem", "Incidentes na Operação", "Projetos com Incidente Operacional marcado", { escopo: "todos", filtro: { campo: "incidente", op: "preenchido", valor: "" } }),
        w("kpi_manual", "Meta de Pontualidade", "Número digitado no admin (exemplo)", { valor: "90", unidade: "%", legenda: "Meta definida pela liderança" }, { visivel: false }),
        w("grafico", "Incidentes por tipo", "Contagem de projetos por Incidente Operacional", { agrupar: "incidente", forma: "barras", escopo: "todos", filtro: { campo: "incidente", op: "preenchido", valor: "" } }, { largura: "grande" }),
      ] },
      { id: uid(), titulo: "O Fluxo das Demandas", widgets: [
        w("grafico", "Volume na Esteira por Etapa", "Projetos ativos por etapa", { agrupar: "etapa", forma: "colunas", escopo: "ativos" }),
        w("vazao", "Vazão da Equipe", "Projetos concluídos por data de entrega"),
      ] },
      { id: uid(), titulo: "Capacidade e Sobrecarga", widgets: [
        w("alocacao", "Alocação por Colaborador", "Projetos ativos (não concluídos) por responsável"),
        w("grafico", "Demandas por Status Geral", "Status interno da tarefa", { agrupar: "status", forma: "rosca", escopo: "todos" }),
        w("tabela", "Projetos Bloqueados · Gargalos Críticos", "Status = Bloqueado, ordenado pelo tempo no status atual", { escopo: "todos", filtro: { campo: "status", op: "igual", valor: "Bloqueado" } }),
      ] },
    ];
  }

  function opcoesPadrao() {
    return {
      pessoas: [
        { nome: "Ana Ribeiro", especialidade: "Designer" }, { nome: "Bruno Lima", especialidade: "Designer" },
        { nome: "Carla Mendes", especialidade: "Copywriter" }, { nome: "Diego Souza", especialidade: "Copywriter" },
        { nome: "Elisa Prado", especialidade: "Dev" }, { nome: "Felipe Rocha", especialidade: "Dev" },
      ],
      especialidades: ["Designer", "Copywriter", "Dev"],
      tipos: ["Novo Produto", "Ajuste/Customização"],
      etapas: [
        { nome: "Ideação" }, { nome: "Em Desenvolvimento" }, { nome: "Homologação" },
        { nome: "Pronto para Entrega / Concluído", final: true },
      ],
      status: [
        { nome: "A fazer", categoria: "afazer" }, { nome: "Em andamento", categoria: "andamento" },
        { nome: "Bloqueado", categoria: "bloqueado" }, { nome: "Concluído", categoria: "concluido" },
      ],
      incidentes: ["Atraso técnico", "Retrabalho de conteúdo", "Falha de briefing", "Indisponibilidade de fornecedor", "Erro de aprovação"],
      motivos: ["Aguardando aprovação da liderança", "Aguardando conteúdo do palestrante", "Dependência de outro time", "Falta de capacidade", "Pendência jurídica/contratual"],
    };
  }

  // projetos de exemplo, determinísticos (pontualidade ≈ 5%)
  function projetosExemplo() {
    let seed = 42;
    const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    const pick = a => a[Math.floor(rnd() * a.length)];
    const op = opcoesPadrao();
    const team = op.pessoas.map(p => [p.nome, p.especialidade]);
    const etapas = op.etapas.map(e => e.nome);
    const temas = ["Liderança Ágil", "IA no Varejo", "Cultura de Dados", "Vendas Consultivas", "ESG na Prática",
      "Gestão de Crises", "Futuro do Trabalho", "Customer Success", "Inovação Aberta", "Saúde Mental",
      "Negociação Estratégica", "Marketing de Conteúdo", "Transformação Digital", "Comunicação Não Violenta"];
    const incid = ["Atraso técnico", "Atraso técnico", ...op.incidentes.slice(1)];
    const today = hoje();
    const out = [];
    for (let i = 1; i <= 96; i++) {
      const [dono0, cargo0] = pick(team);
      const [dono, cargo] = (i > 64 && rnd() < 0.35) ? team[0] : [dono0, cargo0];
      const tipo = rnd() < 0.55 ? "Novo Produto" : "Ajuste/Customização";
      const dur = tipo === "Novo Produto" ? 14 + rnd() * 26 : 3 + rnd() * 10;
      const criado = new Date(today - (i <= 64 ? 20 + rnd() * 90 : rnd() * 30) * DAY);
      let esperado = new Date(+criado + dur * (0.8 + rnd() * 0.5) * DAY);
      let etapa, status, entregue = null, desde;
      if (i <= 64) {
        etapa = etapas[3]; status = "Concluído";
        entregue = new Date(Math.min(+criado + dur * DAY, +today - rnd() * 2 * DAY));
        desde = entregue;
        esperado = i % 20 === 0 ? new Date(+entregue + 3 * DAY) : new Date(+criado + (entregue - criado) * 0.6);
      } else {
        const r = rnd();
        etapa = r < 0.25 ? etapas[0] : r < 0.75 ? etapas[1] : etapas[2];
        const s = rnd();
        status = s < 0.22 ? "Bloqueado" : (etapa === etapas[0] && s < 0.6) ? "A fazer" : "Em andamento";
        desde = new Date(today - Math.min((today - criado) / DAY, 1 + rnd() * 18) * DAY);
      }
      const incidente = rnd() < 0.3 ? pick(incid) : "";
      out.push({
        id: uid(),
        nome: `${tipo === "Novo Produto" ? "Projeto" : "Ajuste"} · ${pick(temas)}`,
        responsavel: dono, especialidade: cargo, tipo, etapa, status,
        criado: iso(criado), esperado: iso(esperado), entregue: iso(entregue),
        incidente, motivo: status === "Bloqueado" ? pick(op.motivos) : "",
        statusDesde: iso(desde),
      });
    }
    return out;
  }

  function documentoPadrao({ comExemplos = true } = {}) {
    return {
      titulo: "Controle de Demandas",
      subtitulo: "Saúde, fluxo e capacidade da produção",
      opcoes: opcoesPadrao(),
      projetos: comExemplos ? projetosExemplo() : [],
      secoes: secoesPadrao(),
    };
  }

  // completa campos ausentes (documentos salvos por versões anteriores)
  function normalizar(doc) {
    const base = documentoPadrao({ comExemplos: false });
    doc = Object.assign({}, base, doc || {});
    doc.opcoes = Object.assign({}, base.opcoes, doc.opcoes || {});
    doc.projetos = Array.isArray(doc.projetos) ? doc.projetos : [];
    doc.secoes = Array.isArray(doc.secoes) ? doc.secoes : base.secoes;
    doc.projetos.forEach(p => { p.id ||= uid(); });
    doc.secoes.forEach(s => { s.id ||= uid(); s.widgets ||= []; s.widgets.forEach(w => { w.id ||= uid(); w.config ||= {}; }); });
    return doc;
  }

  /* ---------- armazenamento ---------- */
  // modo "nuvem": /api/data com banco configurado (todos veem o mesmo)
  // modo "local": sem banco — os dados ficam só neste navegador
  const lsGet = () => { try { return JSON.parse(localStorage.getItem(LS_KEY)); } catch (_) { return null; } };
  const lsSet = v => { try { localStorage.setItem(LS_KEY, JSON.stringify(v)); return true; } catch (_) { return false; } };

  async function carregar() {
    try {
      const r = await fetch(API, { cache: "no-store" });
      if (r.ok && (r.headers.get("content-type") || "").includes("json")) {
        const j = await r.json();
        if (j.data) return { data: normalizar(j.data), versao: j.version || 0, modo: "nuvem", atualizado: j.updatedAt };
        return { data: documentoPadrao(), versao: 0, modo: "nuvem", novo: true };
      }
    } catch (_) { /* sem API: segue para o modo local */ }
    const local = lsGet();
    if (local && local.data) return { data: normalizar(local.data), versao: 0, modo: "local", atualizado: local.updatedAt };
    return { data: documentoPadrao(), versao: 0, modo: "local", novo: true };
  }

  async function salvar(estado) {
    if (estado.modo === "nuvem") {
      const r = await fetch(API, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ data: estado.data, baseVersion: estado.versao }),
      });
      const j = await r.json().catch(() => ({}));
      if (r.status === 409) { const e = new Error("conflito"); e.conflito = true; throw e; }
      if (!r.ok) throw new Error(j.erro || `Erro ${r.status} ao salvar`);
      estado.versao = j.version; estado.atualizado = j.updatedAt;
      return;
    }
    estado.atualizado = new Date().toISOString();
    if (!lsSet({ data: estado.data, updatedAt: estado.atualizado })) throw new Error("O navegador bloqueou o armazenamento local");
  }

  /* ---------- cálculos ---------- */
  function contexto(doc) {
    const finais = new Set(doc.opcoes.etapas.filter(e => e.final).map(e => e.nome));
    const cat = Object.fromEntries(doc.opcoes.status.map(s => [s.nome, s.categoria]));
    const concluido = p => finais.has(p.etapa) || cat[p.status] === "concluido" || !!p.entregue;
    return { finais, cat, concluido };
  }
  function passaFiltro(p, f) {
    if (!f || !f.campo || !f.op) return true;
    const v = String(p[f.campo] || "").trim();
    switch (f.op) {
      case "igual": return v === f.valor;
      case "diferente": return v !== f.valor;
      case "preenchido": return !!v;
      case "vazio": return !v;
    }
    return true;
  }
  function selecionar(doc, { escopo = "todos", filtro } = {}) {
    const { concluido } = contexto(doc);
    return doc.projetos.filter(p =>
      (escopo === "ativos" ? !concluido(p) : escopo === "concluidos" ? concluido(p) : true) && passaFiltro(p, filtro));
  }
  // nomes de uma lista de opções (objetos ou strings)
  const nomesLista = (doc, campo) => (doc.opcoes[LISTA_DO_CAMPO[campo]] || []).map(o => typeof o === "string" ? o : o.nome);

  // renomeia um valor em todos os projetos e filtros de widgets
  function renomearValor(doc, campo, antigo, novo) {
    if (!antigo || antigo === novo) return 0;
    let n = 0;
    doc.projetos.forEach(p => { if (p[campo] === antigo) { p[campo] = novo; n++; } });
    doc.secoes.forEach(s => s.widgets.forEach(w => {
      const f = w.config && w.config.filtro;
      if (f && f.campo === campo && f.valor === antigo) f.valor = novo;
    }));
    return n;
  }
  const usoValor = (doc, campo, valor) => doc.projetos.filter(p => p[campo] === valor).length;

  g.CD = {
    DAY, CAMPOS, LISTA_DO_CAMPO, CATEGORIAS, ESCOPOS, OPS, TIPOS_WIDGET,
    uid, iso, parseData, hoje, esc, clone,
    novoWidget, documentoPadrao, secoesPadrao, projetosExemplo, normalizar,
    carregar, salvar, contexto, passaFiltro, selecionar, nomesLista, renomearValor, usoValor,
  };
})(window);
