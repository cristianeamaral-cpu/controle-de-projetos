/* Controle de Demandas — painel de edição (/admin). */
(async () => {
  "use strict";
  const { esc, uid, iso, hoje, CAMPOS, CATEGORIAS, OPS, TIPOS_WIDGET, LISTA_DO_CAMPO } = CD;
  const $ = id => document.getElementById(id);
  let estado;

  /* ---------- salvar (automático) ---------- */
  let timer, salvando = Promise.resolve(), bloqueado = false;
  function marcar(texto, classe = "") { const s = $("salvo"); s.textContent = texto; s.className = "salvo " + classe; }
  function alterado() {
    if (bloqueado) return;
    marcar("Alterações pendentes…");
    clearTimeout(timer);
    timer = setTimeout(() => { salvando = salvando.then(gravar); }, 500);
  }
  async function gravar() {
    marcar("Salvando…");
    try {
      await CD.salvar(estado);
      marcar(estado.modo === "nuvem" ? "Salvo ✓" : "Salvo neste navegador ✓", "ok");
    } catch (e) {
      if (e.conflito) {
        bloqueado = true;
        marcar("Não salvo: conflito", "erro");
        $("aviso").innerHTML = `<p class="aviso"><b>Outra pessoa salvou alterações enquanto você editava.</b> Sua última alteração não foi gravada. <button id="recarregar" class="mini">Recarregar dados</button></p>`;
        $("recarregar").onclick = () => location.reload();
      } else {
        marcar("Erro ao salvar", "erro");
        alert("Não foi possível salvar: " + e.message);
      }
    }
  }
  addEventListener("beforeunload", e => { if ($("salvo").textContent.startsWith("Alterações pendentes") || $("salvo").textContent === "Salvando…") { e.preventDefault(); e.returnValue = ""; } });

  const doc = () => estado.data;
  const nomes = campo => CD.nomesLista(doc(), campo);
  const opcoesHTML = (lista, atual, vazio) => {
    const itens = [...lista];
    if (atual && !itens.includes(atual)) itens.push(atual);
    return (vazio !== undefined ? `<option value="">${esc(vazio)}</option>` : "") +
      itens.map(v => `<option value="${esc(v)}"${v === atual ? " selected" : ""}>${esc(v)}</option>`).join("");
  };
  const fmtData = s => { const d = CD.parseData(s); return d ? d.toLocaleDateString("pt-BR") : "—"; };

  /* ---------- abas ---------- */
  document.querySelectorAll("[data-tab]").forEach(b => b.onclick = () => {
    document.querySelectorAll("[data-tab]").forEach(x => x.setAttribute("aria-selected", x === b));
    document.querySelectorAll(".painel").forEach(p => p.hidden = p.id !== "p-" + b.dataset.tab);
    try { sessionStorage.setItem("admin-aba", b.dataset.tab); } catch (_) {}
  });

  /* ================= PROJETOS ================= */
  function renderProjetos() {
    $("fEtapa").innerHTML = opcoesHTML(nomes("etapa"), $("fEtapa").value, "Todas as etapas");
    $("fStatus").innerHTML = opcoesHTML(nomes("status"), $("fStatus").value, "Todos os status");
    const q = $("busca").value.trim().toLowerCase(), fe = $("fEtapa").value, fs = $("fStatus").value;
    const lista = doc().projetos
      .filter(p => (!q || `${p.nome} ${p.responsavel}`.toLowerCase().includes(q)) && (!fe || p.etapa === fe) && (!fs || p.status === fs))
      .sort((a, b) => String(b.criado || "").localeCompare(String(a.criado || "")));
    $("tProjetos").innerHTML = lista.length ? lista.map(p => `<tr>
      <td>${esc(p.nome)}</td><td>${esc(p.responsavel || "—")}</td><td><span class="pill">${esc(p.etapa || "—")}</span></td>
      <td>${esc(p.status || "—")}</td><td>${fmtData(p.esperado)}</td><td>${fmtData(p.entregue)}</td>
      <td><div class="acoes"><button class="mini" data-editar="${esc(p.id)}">Editar</button><button class="mini perigo" data-excluir="${esc(p.id)}">Excluir</button></div></td>
    </tr>`).join("") : `<tr><td colspan="7" class="empty">${doc().projetos.length ? "Nenhum projeto encontrado com esses filtros." : "Nenhum projeto cadastrado. Clique em “+ Novo projeto”."}</td></tr>`;
    $("contProjetos").textContent = `${lista.length} de ${doc().projetos.length} projetos`;
    $("tProjetos").querySelectorAll("[data-editar]").forEach(b => b.onclick = () => abrirProjeto(doc().projetos.find(p => p.id === b.dataset.editar)));
    $("tProjetos").querySelectorAll("[data-excluir]").forEach(b => b.onclick = () => {
      const p = doc().projetos.find(p => p.id === b.dataset.excluir);
      if (!confirm(`Excluir o projeto “${p.nome}”? Esta ação não pode ser desfeita.`)) return;
      doc().projetos = doc().projetos.filter(x => x !== p);
      renderProjetos(); alterado();
    });
  }
  ["busca", "fEtapa", "fStatus"].forEach(id => $(id).addEventListener("input", renderProjetos));

  let projetoAtual = null;
  function abrirProjeto(p) {
    projetoAtual = p || null;
    const f = $("fProjeto"), d = doc(), v = p || {
      etapa: nomes("etapa")[0], status: nomes("status")[0], tipo: nomes("tipo")[0],
      criado: iso(hoje()), statusDesde: iso(hoje()),
    };
    $("dProjetoTitulo").textContent = p ? "Editar projeto" : "Novo projeto";
    f.nome.value = v.nome || "";
    f.responsavel.innerHTML = opcoesHTML(nomes("responsavel"), v.responsavel, "— Sem responsável —");
    f.especialidade.innerHTML = opcoesHTML(nomes("especialidade"), v.especialidade, "—");
    f.tipo.innerHTML = opcoesHTML(nomes("tipo"), v.tipo, "—");
    f.etapa.innerHTML = opcoesHTML(nomes("etapa"), v.etapa);
    f.status.innerHTML = opcoesHTML(nomes("status"), v.status);
    f.incidente.innerHTML = opcoesHTML(nomes("incidente"), v.incidente, "Nenhum");
    f.motivo.innerHTML = opcoesHTML(nomes("motivo"), v.motivo, "Nenhum");
    for (const k of ["criado", "esperado", "entregue", "statusDesde"]) f[k].value = v[k] || "";
    f.dataset.statusOriginal = v.status || "";
    $("dProjeto").showModal();
    f.nome.focus();
  }
  $("novoProjeto").onclick = () => abrirProjeto(null);
  (() => {
    const f = $("fProjeto");
    f.responsavel.onchange = () => {
      const pessoa = doc().opcoes.pessoas.find(p => p.nome === f.responsavel.value);
      if (pessoa && pessoa.especialidade) f.especialidade.value = pessoa.especialidade;
    };
    const aoConcluir = () => {
      const { finais, cat } = CD.contexto(doc());
      if ((finais.has(f.etapa.value) || cat[f.status.value] === "concluido") && !f.entregue.value) f.entregue.value = iso(hoje());
    };
    f.status.onchange = () => { if (f.status.value !== f.dataset.statusOriginal) f.statusDesde.value = iso(hoje()); aoConcluir(); };
    f.etapa.onchange = aoConcluir;
    f.querySelector('[value="cancelar"]').type = "button";
    f.querySelector('[value="cancelar"]').onclick = () => $("dProjeto").close();
    f.addEventListener("submit", () => {
      const p = projetoAtual || { id: uid() };
      for (const k of ["nome", "responsavel", "especialidade", "tipo", "etapa", "status", "incidente", "motivo", "criado", "esperado", "entregue", "statusDesde"]) p[k] = f[k].value.trim();
      if (!projetoAtual) doc().projetos.push(p);
      renderProjetos(); alterado();
    });
  })();

  /* ================= LISTAS ================= */
  const LISTAS = [
    { k: "pessoas", titulo: "Pessoas da equipe", campo: "responsavel", extra: "especialidade" },
    { k: "especialidades", titulo: "Especialidades", campo: "especialidade" },
    { k: "tipos", titulo: "Tipos de Demanda", campo: "tipo" },
    { k: "etapas", titulo: "Etapas do pipeline", campo: "etapa", extra: "final", dica: "Marque “final” na etapa que representa a entrega/conclusão." },
    { k: "status", titulo: "Status da tarefa", campo: "status", extra: "categoria", dica: "A categoria define a cor e as regras (ex.: Bloqueado entra na lista de gargalos)." },
    { k: "incidentes", titulo: "Incidentes Operacionais", campo: "incidente" },
    { k: "motivos", titulo: "Motivos de Bloqueio", campo: "motivo" },
  ];
  const nomeDe = o => typeof o === "string" ? o : o.nome;

  function renderListas() {
    $("listas").innerHTML = LISTAS.map(L => {
      const itens = doc().opcoes[L.k] || [];
      return `<div class="card" data-lista="${L.k}"><h3>${esc(L.titulo)}</h3>${L.dica ? `<p class="hint">${esc(L.dica)}</p>` : `<p class="hint">${itens.length} itens</p>`}
        ${itens.map((o, i) => `<div class="item" data-i="${i}">
          <input type="text" value="${esc(nomeDe(o))}" aria-label="Nome">
          ${L.extra === "especialidade" ? `<select data-extra aria-label="Especialidade">${opcoesHTML(doc().opcoes.especialidades, o.especialidade, "—")}</select>` : ""}
          ${L.extra === "final" ? `<label><input type="checkbox" data-extra ${o.final ? "checked" : ""}> final</label>` : ""}
          ${L.extra === "categoria" ? `<select data-extra aria-label="Categoria">${Object.entries(CATEGORIAS).map(([k, v]) => `<option value="${k}"${o.categoria === k ? " selected" : ""}>${esc(v)}</option>`).join("")}</select>` : ""}
          <button class="icone" data-mover="-1" aria-label="Subir"${i === 0 ? " disabled" : ""}>↑</button>
          <button class="icone" data-mover="1" aria-label="Descer"${i === itens.length - 1 ? " disabled" : ""}>↓</button>
          <button class="icone perigo" data-remover aria-label="Excluir">✕</button>
        </div>`).join("")}
        <form class="novo"><input type="text" placeholder="${L.extra === "categoria" ? "Novo status" : "Novo item"}" aria-label="Novo item" required>
          ${L.extra === "categoria" ? `<select data-nova-categoria aria-label="Categoria do novo status">${Object.entries(CATEGORIAS).map(([k, v]) => `<option value="${k}"${k === "andamento" ? " selected" : ""}>${esc(v)}</option>`).join("")}</select>` : ""}
          <button class="mini">Adicionar</button></form>
      </div>`;
    }).join("");

    $("listas").querySelectorAll("[data-lista]").forEach(card => {
      const L = LISTAS.find(x => x.k === card.dataset.lista), arr = doc().opcoes[L.k];
      const existe = (nome, exceto) => arr.some((o, i) => i !== exceto && nomeDe(o).toLowerCase() === nome.toLowerCase());
      card.querySelectorAll(".item").forEach(row => {
        const i = +row.dataset.i, input = row.querySelector("input[type=text]");
        input.onchange = () => {
          const novo = input.value.trim(), antigo = nomeDe(arr[i]);
          if (!novo || existe(novo, i)) { alert(novo ? "Já existe um item com esse nome." : "O nome não pode ficar vazio."); input.value = antigo; return; }
          if (typeof arr[i] === "string") arr[i] = novo; else arr[i].nome = novo;
          const n = CD.renomearValor(doc(), L.campo, antigo, novo);
          if (L.k === "especialidades") doc().opcoes.pessoas.forEach(p => { if (p.especialidade === antigo) p.especialidade = novo; });
          if (n) marcar(`${n} projeto(s) atualizados`);
          tudo(); alterado();
        };
        const extra = row.querySelector("[data-extra]");
        if (extra) extra.onchange = () => {
          if (L.extra === "final") arr[i].final = extra.checked;
          else arr[i][L.extra] = extra.value;
          alterado();
        };
        row.querySelectorAll("[data-mover]").forEach(b => b.onclick = () => {
          const j = i + +b.dataset.mover; [arr[i], arr[j]] = [arr[j], arr[i]]; renderListas(); alterado();
        });
        row.querySelector("[data-remover]").onclick = () => {
          const nome = nomeDe(arr[i]);
          if ((L.k === "etapas" || L.k === "status") && arr.length === 1) return alert("É preciso ter pelo menos um item nesta lista.");
          const uso = CD.usoValor(doc(), L.campo, nome);
          if (!confirm(uso ? `“${nome}” é usado em ${uso} projeto(s). Excluir mesmo assim? O campo ficará vazio nesses projetos.` : `Excluir “${nome}”?`)) return;
          arr.splice(i, 1);
          doc().projetos.forEach(p => { if (p[L.campo] === nome) p[L.campo] = ""; });
          if (L.k === "especialidades") doc().opcoes.pessoas.forEach(p => { if (p.especialidade === nome) p.especialidade = ""; });
          tudo(); alterado();
        };
      });
      card.querySelector("form.novo").onsubmit = e => {
        e.preventDefault();
        const input = e.target.querySelector("input"), nome = input.value.trim();
        if (!nome) return;
        if (existe(nome)) return alert("Já existe um item com esse nome.");
        arr.push(L.extra === "especialidade" ? { nome, especialidade: "" } : L.extra === "final" ? { nome } : L.extra === "categoria" ? { nome, categoria: e.target.querySelector("[data-nova-categoria]").value } : nome);
        tudo(); alterado();
        $("listas").querySelector(`[data-lista="${L.k}"] form.novo input`).focus();
      };
    });
  }

  /* ================= SEÇÕES ================= */
  const LARGURAS = { pequeno: "Pequeno (1/4)", medio: "Médio (1/2)", grande: "Inteiro" };
  function renderSecoes() {
    const secoes = doc().secoes;
    $("secoes").innerHTML = secoes.length ? secoes.map((s, si) => `<div class="card secao-admin" data-s="${si}">
      <div class="cab">
        <input type="text" value="${esc(s.titulo)}" aria-label="Título da seção" data-titulo-secao>
        <button class="icone" data-mover-secao="-1" aria-label="Subir seção"${si === 0 ? " disabled" : ""}>↑</button>
        <button class="icone" data-mover-secao="1" aria-label="Descer seção"${si === secoes.length - 1 ? " disabled" : ""}>↓</button>
        <button class="mini perigo" data-excluir-secao>Excluir seção</button>
      </div>
      ${s.widgets.map((w, wi) => `<div class="widget${w.visivel === false ? " oculto" : ""}" data-w="${wi}">
        <input type="checkbox" data-visivel ${w.visivel !== false ? "checked" : ""} aria-label="Mostrar no dashboard" title="Mostrar no dashboard">
        <div class="info"><div>${esc(w.titulo)}</div><div class="tipo">${esc((TIPOS_WIDGET[w.tipo] || {}).nome || w.tipo)} · ${esc(LARGURAS[w.largura] || "")}</div></div>
        <div class="ctrl">
          <button class="icone" data-mover-w="-1" aria-label="Subir"${wi === 0 ? " disabled" : ""}>↑</button>
          <button class="icone" data-mover-w="1" aria-label="Descer"${wi === s.widgets.length - 1 ? " disabled" : ""}>↓</button>
          ${secoes.length > 1 ? `<select class="mini" data-mover-para aria-label="Mover para seção"><option value="">Mover para…</option>${secoes.map((x, xi) => xi === si ? "" : `<option value="${xi}">${esc(x.titulo)}</option>`).join("")}</select>` : ""}
          <button class="mini" data-config>Editar</button>
          <button class="mini perigo" data-excluir-w>Excluir</button>
        </div>
      </div>`).join("") || `<p class="hint">Seção vazia. Ela não aparece no dashboard até receber um item.</p>`}
      <div class="novo">
        <select data-novo-tipo aria-label="Tipo do novo item">${Object.entries(TIPOS_WIDGET).map(([k, t]) => `<option value="${k}">${esc(t.nome)}</option>`).join("")}</select>
        <button class="mini" data-novo-w>+ Adicionar item</button>
      </div>
    </div>`).join("") : `<p class="vazio-dash">Nenhuma seção. Clique em “+ Nova seção”.</p>`;

    $("secoes").querySelectorAll("[data-s]").forEach(card => {
      const si = +card.dataset.s, s = secoes[si];
      card.querySelector("[data-titulo-secao]").onchange = e => { s.titulo = e.target.value.trim() || "Sem título"; alterado(); };
      card.querySelectorAll("[data-mover-secao]").forEach(b => b.onclick = () => {
        const j = si + +b.dataset.moverSecao; [secoes[si], secoes[j]] = [secoes[j], secoes[si]]; renderSecoes(); alterado();
      });
      card.querySelector("[data-excluir-secao]").onclick = () => {
        if (!confirm(`Excluir a seção “${s.titulo}” e seus ${s.widgets.length} item(ns)?`)) return;
        secoes.splice(si, 1); renderSecoes(); alterado();
      };
      card.querySelector("[data-novo-w]").onclick = () => {
        const w = CD.novoWidget(card.querySelector("[data-novo-tipo]").value);
        s.widgets.push(w); renderSecoes(); alterado(); abrirWidget(w);
      };
      card.querySelectorAll("[data-w]").forEach(row => {
        const wi = +row.dataset.w, w = s.widgets[wi];
        row.querySelector("[data-visivel]").onchange = e => { w.visivel = e.target.checked; renderSecoes(); alterado(); };
        row.querySelectorAll("[data-mover-w]").forEach(b => b.onclick = () => {
          const j = wi + +b.dataset.moverW; [s.widgets[wi], s.widgets[j]] = [s.widgets[j], s.widgets[wi]]; renderSecoes(); alterado();
        });
        const para = row.querySelector("[data-mover-para]");
        if (para) para.onchange = () => { if (para.value === "") return; s.widgets.splice(wi, 1); secoes[+para.value].widgets.push(w); renderSecoes(); alterado(); };
        row.querySelector("[data-config]").onclick = () => abrirWidget(w);
        row.querySelector("[data-excluir-w]").onclick = () => {
          if (!confirm(`Excluir “${w.titulo}”?`)) return;
          s.widgets.splice(wi, 1); renderSecoes(); alterado();
        };
      });
    });
  }
  $("novaSecao").onclick = () => {
    doc().secoes.push({ id: uid(), titulo: "Nova seção", widgets: [] });
    renderSecoes(); alterado();
    const inputs = $("secoes").querySelectorAll("[data-titulo-secao]");
    inputs[inputs.length - 1].select();
  };

  /* ---------- diálogo de configuração do item ---------- */
  let widgetAtual = null;
  function campoFiltroHTML(f = {}) {
    const campo = f.campo || "", op = f.op || "igual";
    const valores = campo ? nomes(campo) : [];
    return `<div class="filtro" data-filtro>
      <select data-f="campo" aria-label="Campo do filtro"><option value="">Sem filtro</option>${Object.entries(CAMPOS).map(([k, v]) => `<option value="${k}"${k === campo ? " selected" : ""}>${esc(v)}</option>`).join("")}</select>
      <select data-f="op" aria-label="Condição"${campo ? "" : " disabled"}>${Object.entries(OPS).map(([k, v]) => `<option value="${k}"${k === op ? " selected" : ""}>${esc(v)}</option>`).join("")}</select>
      <select data-f="valor" aria-label="Valor"${campo && (op === "igual" || op === "diferente") ? "" : " disabled"}>${opcoesHTML(valores, f.valor, "—")}</select>
    </div>`;
  }
  function lerFiltro(box) {
    const g = k => box.querySelector(`[data-f="${k}"]`).value;
    return g("campo") ? { campo: g("campo"), op: g("op"), valor: g("valor") } : null;
  }
  // o filtro se redesenha quando muda o campo/condição (valores e campos habilitados dependem disso)
  function ligarFiltro() {
    const box = $("camposWidget").querySelector("[data-filtro]");
    if (!box) return;
    box.addEventListener("change", e => {
      const f = lerFiltro(box) || {};
      if (e.target.dataset.f === "campo") f.valor = "";
      box.outerHTML = campoFiltroHTML(f);
      ligarFiltro();
    });
  }
  function abrirWidget(w) {
    widgetAtual = w;
    const t = TIPOS_WIDGET[w.tipo];
    $("dWidgetTitulo").textContent = t.nome;
    const c = w.config;
    let html = `<label class="inteiro">Título<input type="text" name="titulo" value="${esc(w.titulo)}" required></label>
      <label class="inteiro">Descrição (opcional)<input type="text" name="descricao" value="${esc(w.descricao || "")}"></label>
      <label>Largura<select name="largura">${Object.entries(LARGURAS).map(([k, v]) => `<option value="${k}"${w.largura === k ? " selected" : ""}>${esc(v)}</option>`).join("")}</select></label>
      <label>Mostrar no dashboard<select name="visivel"><option value="1"${w.visivel !== false ? " selected" : ""}>Sim</option><option value="0"${w.visivel === false ? " selected" : ""}>Não</option></select></label>`;
    for (const f of t.campos) {
      if (f.tipo === "filtro") html += `<label class="inteiro">Filtrar projetos<small>Opcional. Ex.: Tipo de Demanda é igual a Novo Produto.</small>${campoFiltroHTML(c.filtro)}</label>`;
      else if (f.tipo === "select") html += `<label>${esc(f.label)}<select name="c_${f.k}">${Object.entries(f.opcoes).map(([k, v]) => `<option value="${esc(k)}"${String(c[f.k]) === String(k) ? " selected" : ""}>${esc(v)}</option>`).join("")}</select></label>`;
      else html += `<label${f.k === "legenda" ? ' class="inteiro"' : ""}>${esc(f.label)}<input type="${f.tipo === "number" ? "number" : "text"}" name="c_${f.k}" value="${esc(c[f.k] ?? "")}"${f.tipo === "number" ? ' min="2" max="52"' : ""}></label>`;
    }
    $("camposWidget").innerHTML = html;
    ligarFiltro();
    if (!$("dWidget").open) $("dWidget").showModal();
  }
  (() => {
    const f = $("fWidget");
    f.querySelector('[value="cancelar"]').type = "button";
    f.querySelector('[value="cancelar"]').onclick = () => $("dWidget").close();
    f.addEventListener("submit", () => {
      const w = widgetAtual, t = TIPOS_WIDGET[w.tipo];
      w.titulo = f.titulo.value.trim() || t.nome;
      w.descricao = f.descricao.value.trim();
      w.largura = f.largura.value;
      w.visivel = f.visivel.value === "1";
      for (const c of t.campos) {
        if (c.tipo === "filtro") { const box = $("camposWidget").querySelector("[data-filtro]"); w.config.filtro = lerFiltro(box); }
        else if (c.tipo === "number") w.config[c.k] = Math.max(2, Math.min(52, +f["c_" + c.k].value || 12));
        else w.config[c.k] = f["c_" + c.k].value;
      }
      renderSecoes(); alterado();
    });
  })();

  /* ================= GERAL ================= */
  function renderGeral() {
    $("gTitulo").value = doc().titulo || "";
    $("gSubtitulo").value = doc().subtitulo || "";
    $("nomeDash").textContent = doc().titulo || "Controle de Demandas";
    $("infoModo").textContent = estado.modo === "nuvem"
      ? "Os dados ficam no banco de dados da Vercel: todos que abrem o dashboard veem as mesmas informações."
      : "Banco de dados não configurado: os dados ficam salvos apenas neste navegador.";
  }
  $("gTitulo").onchange = () => { doc().titulo = $("gTitulo").value.trim() || "Controle de Demandas"; renderGeral(); alterado(); };
  $("gSubtitulo").onchange = () => { doc().subtitulo = $("gSubtitulo").value.trim(); alterado(); };
  $("backup").onclick = () => {
    const blob = new Blob([JSON.stringify(doc(), null, 2)], { type: "application/json" });
    const a = Object.assign(document.createElement("a"), { href: URL.createObjectURL(blob), download: `controle-de-demandas-${iso(hoje())}.json` });
    a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  };
  $("restaurar").onchange = async e => {
    const f = e.target.files[0]; e.target.value = "";
    if (!f) return;
    try {
      const d = JSON.parse(await f.text());
      if (!Array.isArray(d.projetos) || !Array.isArray(d.secoes)) throw new Error("arquivo não é uma cópia de segurança deste dashboard");
      if (!confirm(`Substituir todos os dados atuais pelo arquivo (${d.projetos.length} projetos)?`)) return;
      estado.data = CD.normalizar(d); tudo(); alterado();
    } catch (err) { alert("Não foi possível restaurar: " + err.message); }
  };
  $("secoesPadrao").onclick = () => {
    if (!confirm("Substituir todas as seções pelas seções padrão? Os projetos e listas não mudam.")) return;
    doc().secoes = CD.secoesPadrao(); tudo(); alterado();
  };
  $("exemplos").onclick = () => {
    if (!confirm("Substituir todos os projetos pelos 96 projetos de exemplo?")) return;
    doc().projetos = CD.projetosExemplo(); tudo(); alterado();
  };
  $("apagarTudo").onclick = () => {
    if (!confirm(`Apagar os ${doc().projetos.length} projetos? As listas e seções continuam. Esta ação não pode ser desfeita.`)) return;
    doc().projetos = []; tudo(); alterado();
  };

  function tudo() { renderProjetos(); renderListas(); renderSecoes(); renderGeral(); }

  $("theme").onclick = () => {
    const root = document.documentElement;
    const dark = root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
    root.dataset.theme = dark ? "light" : "dark";
    try { localStorage.setItem("esteira-theme", root.dataset.theme); } catch (_) {}
  };

  /* ---------- início ---------- */
  estado = await CD.carregar();
  if (estado.modo === "local") {
    $("aviso").innerHTML = `<p class="aviso"><b>Banco de dados não configurado.</b> O que você salvar aqui fica só neste navegador. Para a equipe toda ver, conecte o banco na Vercel (passo a passo em <code>docs/banco-de-dados.md</code>).</p>`;
  } else if (estado.novo) {
    $("aviso").innerHTML = `<p class="aviso"><b>Banco conectado e vazio.</b> Carregamos projetos de exemplo para você começar. Para zerar, use Geral → “Apagar todos os projetos”.</p>`;
  }
  marcar(estado.modo === "nuvem" ? "Conectado ao banco" : "Modo local");
  tudo();
  try { const aba = sessionStorage.getItem("admin-aba"); if (aba) document.querySelector(`[data-tab="${aba}"]`)?.click(); } catch (_) {}
})();
