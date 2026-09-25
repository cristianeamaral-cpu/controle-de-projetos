/* Controle de Demandas — desenho dos cartões e gráficos (SVG, sem dependências). */
(function (g) {
  "use strict";
  const { DAY, esc, parseData, contexto, selecionar, nomesLista, CAMPOS } = g.CD;

  const fmt1 = n => n.toLocaleString("pt-BR", { maximumFractionDigits: 1 });
  const fmtDia = d => d.toLocaleDateString("pt-BR", { day: "2-digit", month: "short" }).replace(".", "");
  const media = xs => xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : NaN;
  const dias = (a, b) => (b - a) / DAY;

  /* ---------- cores ---------- */
  const escuro = () => {
    const t = document.documentElement.dataset.theme;
    return t ? t === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  };
  // rampa ordinal (azul) para etapas; o passo mais claro ainda contrasta com a superfície
  const RAMPA = {
    claro: ["#86b6ef", "#6da7ec", "#5598e7", "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281"],
    escuro: ["#6da7ec", "#5598e7", "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95"],
  };
  const CATEGORICA = {
    claro: ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"],
    escuro: ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300"],
  };
  function rampa(n) {
    const r = RAMPA[escuro() ? "escuro" : "claro"];
    if (n <= 1) return [r[Math.floor(r.length / 2)]];
    return Array.from({ length: n }, (_, i) => r[Math.round(i * (r.length - 1) / (n - 1))]);
  }
  // etapas abertas recebem a rampa azul; a etapa final (entrega) usa o verde de "concluído"
  function coresEtapas(doc) {
    const abertas = doc.opcoes.etapas.filter(e => !e.final).map(e => e.nome), cs = rampa(abertas.length);
    const m = Object.fromEntries(abertas.map((n, i) => [n, cs[i]]));
    doc.opcoes.etapas.filter(e => e.final).forEach(e => { m[e.nome] = "var(--good)"; });
    return m;
  }
  const categorica = () => CATEGORICA[escuro() ? "escuro" : "claro"];
  const COR_CATEGORIA = { afazer: "var(--neutral)", andamento: "var(--series-1)", bloqueado: "var(--critical)", concluido: "var(--good)" };
  const ICONE_CATEGORIA = { afazer: "circle", andamento: "half", bloqueado: "block", concluido: "check" };

  /* ---------- tooltip ---------- */
  let tip;
  function mostrarTip(e, titulo, linhas) {
    tip ||= Object.assign(document.body.appendChild(document.createElement("div")), { id: "tip", role: "tooltip" });
    tip.innerHTML = `<b>${esc(titulo)}</b>` + linhas.map(([a, b]) => `<div class="row"><span>${esc(a)}</span><span>${esc(b)}</span></div>`).join("");
    tip.style.display = "block";
    const w = tip.offsetWidth, h = tip.offsetHeight;
    let x = e.clientX + 14, y = e.clientY + 14;
    if (x + w > innerWidth - 8) x = e.clientX - w - 14;
    if (y + h > innerHeight - 8) y = e.clientY - h - 14;
    tip.style.left = x + "px"; tip.style.top = y + "px";
  }
  const esconderTip = () => { if (tip) tip.style.display = "none"; };
  function ligarTips(root) {
    root.querySelectorAll("[data-tip]").forEach(el => {
      const d = JSON.parse(el.dataset.tip);
      el.addEventListener("mousemove", e => mostrarTip(e, d.t, d.r));
      el.addEventListener("mouseleave", esconderTip);
    });
  }
  const tipAttr = (t, r) => `data-tip="${esc(JSON.stringify({ t, r }))}"`;

  /* ---------- primitivas SVG ---------- */
  // barra com cantos arredondados (4px) só na ponta de dados
  function barra(x, y, w, h, dir, r = 4) {
    if (w <= 0 || h <= 0) return "";
    if (dir === "up") {
      r = Math.min(r, w / 2, h);
      return `M${x},${y + h}V${y + r}Q${x},${y} ${x + r},${y}H${x + w - r}Q${x + w},${y} ${x + w},${y + r}V${y + h}Z`;
    }
    r = Math.min(r, h / 2, w);
    return `M${x},${y}H${x + w - r}Q${x + w},${y} ${x + w},${y + r}V${y + h - r}Q${x + w},${y + h} ${x + w - r},${y + h}H${x}Z`;
  }
  function maxBonito(v) {
    if (v <= 5) return 5;
    const p = Math.pow(10, Math.floor(Math.log10(v)));
    for (const m of [1, 2, 2.5, 5, 10]) if (m * p >= v) return m * p;
    return 10 * p;
  }
  const marcas = (max, n = 4) => Array.from({ length: n + 1 }, (_, i) => max / n * i);
  const cortar = (s, max) => s.length > max ? s.slice(0, max - 1) + "…" : s;
  const vazio = (el, msg = "Nenhum projeto neste recorte.") => { el.innerHTML = `<p class="empty">${esc(msg)}</p>`; };

  function barrasH(el, itens) {
    if (!itens.length) return vazio(el);
    const W = Math.max(280, el.clientWidth || 720), rowH = 30, bh = 16, H = itens.length * rowH + 22;
    const labelW = Math.min(200, W * 0.42), plotW = W - labelW - 40;
    const max = maxBonito(Math.max(...itens.map(d => d.v)));
    const x = v => labelW + v / max * plotW;
    const maxCh = Math.floor((labelW - 12) / 6.6);
    let s = `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="Gráfico de barras horizontais">`;
    for (const t of marcas(max)) s += `<line class="gridline" x1="${x(t)}" x2="${x(t)}" y1="0" y2="${H - 20}"/><text x="${x(t)}" y="${H - 6}" text-anchor="middle">${fmt1(t)}</text>`;
    itens.forEach((d, i) => {
      const y = i * rowH + (rowH - bh) / 2;
      s += `<text class="lbl" x="${labelW - 10}" y="${y + bh / 2 + 4}" text-anchor="end">${esc(cortar(d.k, maxCh))}</text>`;
      s += `<path d="${barra(labelW, y, d.v / max * plotW, bh, "right")}" fill="${d.cor || "var(--series-1)"}"/>`;
      s += `<text class="val" x="${x(d.v) + 6}" y="${y + bh / 2 + 4}">${d.v}</text>`;
      s += `<rect class="hit" x="0" y="${i * rowH}" width="${W}" height="${rowH}" ${tipAttr(d.k, [["Projetos", d.v], ...(d.extra || [])])}/>`;
    });
    s += `<line class="baseline" x1="${labelW}" x2="${labelW}" y1="0" y2="${H - 20}"/></svg>`;
    el.innerHTML = s; ligarTips(el);
  }

  function colunas(el, itens, { rotulo = d => d.k, valores = "todos" } = {}) {
    if (!itens.length) return vazio(el);
    const W = Math.max(280, el.clientWidth || 560), H = 280, L = 36, B = 44, T = 18, plotH = H - B - T, plotW = W - L - 8;
    const max = maxBonito(Math.max(1, ...itens.map(d => d.v)));
    const step = plotW / itens.length, bw = Math.min(64, step * 0.56);
    const y = v => T + plotH - v / max * plotH;
    const cada = Math.ceil(itens.length / Math.max(2, Math.floor(plotW / 80)));
    const maxCh = Math.max(6, Math.floor(step / 6.6));
    let s = `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="Gráfico de colunas">`;
    for (const t of marcas(max)) s += `<line class="gridline" x1="${L}" x2="${W - 8}" y1="${y(t)}" y2="${y(t)}"/><text x="${L - 6}" y="${y(t) + 4}" text-anchor="end">${fmt1(t)}</text>`;
    itens.forEach((d, i) => {
      const cx = L + step * i + step / 2, h = d.v / max * plotH;
      s += `<path d="${barra(cx - bw / 2, y(d.v), bw, h, "up")}" fill="${d.cor || "var(--series-1)"}"/>`;
      if (valores === "todos" || (valores === "ultimo" && i === itens.length - 1)) s += `<text class="val" x="${cx}" y="${y(d.v) - 6}" text-anchor="middle">${d.v}</text>`;
      if (i % cada === 0) s += `<text class="lbl" x="${cx}" y="${H - B + 18}" text-anchor="middle">${esc(cortar(rotulo(d), cada > 1 ? 12 : maxCh))}</text>`;
      s += `<rect class="hit" x="${cx - step / 2}" y="${T}" width="${step}" height="${plotH}" ${tipAttr(d.titulo || d.k, [["Projetos", d.v], ...(d.extra || [])])}/>`;
    });
    s += `<line class="baseline" x1="${L}" x2="${W - 8}" y1="${T + plotH}" y2="${T + plotH}"/></svg>`;
    el.innerHTML = s; ligarTips(el);
  }

  function empilhadas(el, legendaEl, linhas, chaves, cores) {
    legendaEl.innerHTML = chaves.map((k, i) => `<span><i style="background:${cores[i]}"></i>${esc(k)}</span>`).join("");
    if (!linhas.length) return vazio(el, "Nenhum projeto ativo.");
    const W = Math.max(280, el.clientWidth || 560), rowH = 34, bh = 18, labelW = Math.min(150, W * 0.35), H = linhas.length * rowH + 22;
    const plotW = W - labelW - 36, max = maxBonito(Math.max(...linhas.map(p => p.total)));
    const x = v => labelW + v / max * plotW;
    const maxCh = Math.floor((labelW - 12) / 6.6);
    let s = `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="Barras empilhadas">`;
    for (const t of marcas(max)) s += `<line class="gridline" x1="${x(t)}" x2="${x(t)}" y1="0" y2="${H - 20}"/><text x="${x(t)}" y="${H - 6}" text-anchor="middle">${fmt1(t)}</text>`;
    linhas.forEach((p, i) => {
      const y = i * rowH + (rowH - bh) / 2;
      s += `<text class="lbl" x="${labelW - 10}" y="${y + bh / 2 - 1}" text-anchor="end">${esc(cortar(p.nome, maxCh))}</text>`;
      s += `<text x="${labelW - 10}" y="${y + bh / 2 + 12}" text-anchor="end">${esc(p.sub || "")}</text>`;
      let acc = 0;
      const segs = chaves.map((k, j) => ({ k, j, v: p.por[k] || 0 })).filter(d => d.v > 0);
      segs.forEach((d, n) => {
        const x0 = x(acc) + (n ? 1 : 0), x1 = x(acc + d.v) - (n < segs.length - 1 ? 1 : 0);
        s += n === segs.length - 1
          ? `<path d="${barra(x0, y, x1 - x0, bh, "right")}" fill="${cores[d.j]}"/>`
          : `<rect x="${x0}" y="${y}" width="${Math.max(0, x1 - x0)}" height="${bh}" fill="${cores[d.j]}"/>`;
        acc += d.v;
      });
      s += `<text class="val" x="${x(p.total) + 6}" y="${y + bh / 2 + 4}">${p.total}</text>`;
      s += `<rect class="hit" x="0" y="${i * rowH}" width="${W}" height="${rowH}" ${tipAttr(`${p.nome}${p.sub ? " · " + p.sub : ""}`, [...chaves.map(k => [k, p.por[k] || 0]), ["Total", p.total]])}/>`;
    });
    s += `<line class="baseline" x1="${labelW}" x2="${labelW}" y1="0" y2="${H - 20}"/></svg>`;
    el.innerHTML = s; ligarTips(el);
  }

  const ICONES = {
    circle: `<circle cx="7" cy="7" r="5" fill="none" stroke="currentColor" stroke-width="2"/>`,
    half: `<circle cx="7" cy="7" r="5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M7 2a5 5 0 0 1 0 10z" fill="currentColor"/>`,
    block: `<circle cx="7" cy="7" r="6" fill="currentColor"/><rect x="3.5" y="6" width="7" height="2" fill="var(--surface)"/>`,
    check: `<circle cx="7" cy="7" r="6" fill="currentColor"/><path d="M4.2 7.2l2 2 3.8-4" fill="none" stroke="var(--surface)" stroke-width="1.8"/>`,
    dot: `<circle cx="7" cy="7" r="5" fill="currentColor"/>`,
  };
  function rosca(el, itens) {
    const total = itens.reduce((a, d) => a + d.v, 0);
    const R = 80, r = 54, C = 90;
    let s = `<div class="donut-wrap"><svg width="180" height="180" viewBox="0 0 180 180" role="img" aria-label="Gráfico de rosca">`;
    if (!total) s += `<circle cx="${C}" cy="${C}" r="${(R + r) / 2}" fill="none" stroke="var(--grid)" stroke-width="${R - r}"/>`;
    let a0 = -Math.PI / 2;
    const gap = itens.filter(d => d.v).length > 1 ? 0.025 : 0;
    const p = (rad, a) => `${C + rad * Math.cos(a)},${C + rad * Math.sin(a)}`;
    itens.forEach(d => {
      if (!d.v) return;
      const a1 = a0 + d.v / total * Math.PI * 2, s0 = a0 + gap / 2, s1 = a1 - gap / 2, large = s1 - s0 > Math.PI ? 1 : 0;
      const path = (s1 - s0) >= Math.PI * 2 - 0.001
        ? `M${C - R},${C}a${R},${R} 0 1,0 ${2 * R},0a${R},${R} 0 1,0 ${-2 * R},0M${C - r},${C}a${r},${r} 0 1,1 ${2 * r},0a${r},${r} 0 1,1 ${-2 * r},0Z`
        : `M${p(R, s0)}A${R},${R} 0 ${large} 1 ${p(R, s1)}L${p(r, s1)}A${r},${r} 0 ${large} 0 ${p(r, s0)}Z`;
      s += `<path d="${path}" fill="${d.cor}" fill-rule="evenodd" ${tipAttr(d.k, [["Projetos", d.v], ["Participação", fmt1(d.v / total * 100) + "%"]])}/>`;
      a0 = a1;
    });
    s += `<text x="${C}" y="${C + 2}" text-anchor="middle" style="fill:var(--ink);font-size:26px;font-weight:650">${total}</text>`;
    s += `<text x="${C}" y="${C + 20}" text-anchor="middle">projetos</text></svg>`;
    s += `<ul class="donut-list">` + itens.map(d => `<li><svg class="ico" viewBox="0 0 14 14" style="color:${d.cor}" aria-hidden="true">${ICONES[d.icone || "dot"]}</svg>${esc(d.k)}<span class="n">${d.v}</span><span class="p">${total ? Math.round(d.v / total * 100) : 0}%</span></li>`).join("") + `</ul></div>`;
    el.innerHTML = s; ligarTips(el);
  }

  /* ---------- agrupamento ---------- */
  function agrupar(doc, projetos, campo, { mostrarZerados } = {}) {
    const cont = new Map();
    projetos.forEach(p => { const k = p[campo] || ""; if (k) cont.set(k, (cont.get(k) || 0) + 1); });
    const ordem = nomesLista(doc, campo);
    let itens;
    if (campo === "etapa" || campo === "status") {
      itens = ordem.map(k => ({ k, v: cont.get(k) || 0 })).filter(d => d.v || mostrarZerados(d.k));
      cont.forEach((v, k) => { if (!ordem.includes(k)) itens.push({ k, v }); });
    } else {
      itens = [...cont].map(([k, v]) => ({ k, v })).sort((a, b) => b.v - a.v);
    }
    return itens;
  }

  function coresPara(doc, campo, itens, forma) {
    if (campo === "etapa") {
      const m = coresEtapas(doc);
      itens.forEach(d => { d.cor = m[d.k] || "var(--neutral)"; });
    } else if (campo === "status") {
      const cat = contexto(doc).cat;
      itens.forEach(d => { const c = cat[d.k] || "andamento"; d.cor = COR_CATEGORIA[c]; d.icone = ICONE_CATEGORIA[c]; });
    } else if (forma === "rosca") {
      const cs = categorica();
      if (itens.length > cs.length) {
        const resto = itens.splice(cs.length - 1);
        itens.push({ k: "Outros", v: resto.reduce((a, d) => a + d.v, 0) });
      }
      itens.forEach((d, i) => { d.cor = d.k === "Outros" ? "var(--neutral)" : cs[i]; });
    }
    return itens;
  }

  /* ---------- widgets ---------- */
  const RENDER = {
    kpi_pontualidade(corpo, w, doc) {
      const base = selecionar(doc, { escopo: "concluidos", filtro: w.config.filtro }).filter(p => p.entregue && p.esperado);
      const noPrazo = base.filter(p => parseData(p.entregue) <= parseData(p.esperado)).length;
      const pct = base.length ? noPrazo / base.length * 100 : NaN;
      corpo.innerHTML = `<div class="value">${isNaN(pct) ? "–" : `${Math.round(pct)}<small>%</small>`}</div>
        <div class="foot">${base.length ? `${noPrazo} de ${base.length} entregues no prazo` : "Sem projetos concluídos com prazo"}</div>
        <div class="meter"><span style="width:${isNaN(pct) ? 0 : pct}%"></span></div>`;
    },
    kpi_tempo(corpo, w, doc) {
      const lt = selecionar(doc, { escopo: "concluidos", filtro: w.config.filtro })
        .filter(p => p.criado && p.entregue).map(p => dias(parseData(p.criado), parseData(p.entregue)));
      const m = media(lt);
      corpo.innerHTML = `<div class="value">${isNaN(m) ? "–" : `${fmt1(m)}<small>dias</small>`}</div>
        <div class="foot">${lt.length ? `média de ${lt.length} concluídos · máx. ${fmt1(Math.max(...lt))} dias` : "Nenhum concluído"}</div>`;
    },
    kpi_contagem(corpo, w, doc) {
      const sel = selecionar(doc, w.config);
      const f = w.config.filtro;
      let foot = "";
      if (f && f.campo && doc.projetos.length) {
        foot = `${fmt1(sel.length / doc.projetos.length * 100)}% dos projetos`;
        const top = agrupar(doc, sel, f.campo, { mostrarZerados: () => false })[0];
        if (f.op === "preenchido" && top) foot += ` · principal: ${top.k}`;
      }
      corpo.innerHTML = `<div class="value">${sel.length}</div><div class="foot">${esc(foot)}</div>`;
    },
    kpi_manual(corpo, w) {
      const c = w.config;
      corpo.innerHTML = `<div class="value">${esc(c.valor || "–")}${c.unidade ? `<small>${esc(c.unidade)}</small>` : ""}</div><div class="foot">${esc(c.legenda || "")}</div>`;
    },
    grafico(corpo, w, doc) {
      const c = w.config, sel = selecionar(doc, c);
      const { finais } = contexto(doc);
      const zerado = c.agrupar === "etapa" ? k => !(c.escopo === "ativos" && finais.has(k)) : c.agrupar === "status" ? () => true : () => false;
      const itens = coresPara(doc, c.agrupar, agrupar(doc, sel, c.agrupar, { mostrarZerados: zerado }), c.forma);
      const total = sel.length || 1;
      itens.forEach(d => { d.extra = [["Participação", fmt1(d.v / total * 100) + "%"]]; });
      if (c.forma === "rosca") return rosca(corpo, itens);
      if (c.forma === "barras") return barrasH(corpo, itens);
      colunas(corpo, itens);
    },
    vazao(corpo, w, doc, estado) {
      const B = +(estado.agrupamento || w.config.agrupamento || 7), n = Math.max(2, Math.min(52, +w.config.periodos || 12));
      const fim = CD.hoje(); fim.setHours(23, 59, 59, 999);
      const baldes = Array.from({ length: n }, (_, i) => {
        const ate = new Date(+fim - (n - 1 - i) * B * DAY), de = new Date(+ate - B * DAY + 1);
        return { de, ate, v: 0 };
      });
      selecionar(doc, { escopo: "concluidos", filtro: w.config.filtro }).forEach(p => {
        const d = parseData(p.entregue); if (!d) return;
        const b = baldes.find(b => d >= b.de && d <= b.ate); if (b) b.v++;
      });
      const m = media(baldes.map(b => b.v));
      colunas(corpo, baldes.map(b => ({ ...b, k: fmtDia(b.de), titulo: `${fmtDia(b.de)} – ${fmtDia(b.ate)}`, extra: [["Média do período", fmt1(m)]] })), { valores: "ultimo" });
    },
    alocacao(corpo, w, doc, estado) {
      const campo = estado.empilhar || w.config.empilhar || "etapa";
      const ativos = selecionar(doc, { escopo: "ativos", filtro: w.config.filtro });
      const pessoas = Object.fromEntries(doc.opcoes.pessoas.map(p => [p.nome, p.especialidade]));
      const por = {};
      ativos.forEach(p => {
        const nome = p.responsavel || "Sem responsável";
        const l = por[nome] ||= { nome, sub: pessoas[nome] || p.especialidade || "", por: {}, total: 0 };
        const k = p[campo] || "Não informado";
        l.por[k] = (l.por[k] || 0) + 1; l.total++;
      });
      const linhas = Object.values(por).sort((a, b) => b.total - a.total);
      const presentes = new Set(ativos.map(p => p[campo] || "Não informado"));
      const chaves = [...nomesLista(doc, campo), "Não informado"].filter(k => presentes.has(k));
      presentes.forEach(k => { if (!chaves.includes(k)) chaves.push(k); });
      let cores;
      if (campo === "etapa") {
        const m = coresEtapas(doc);
        cores = chaves.map(k => m[k] || "var(--neutral)");
      } else if (campo === "status") {
        const cat = contexto(doc).cat;
        cores = chaves.map(k => COR_CATEGORIA[cat[k]] || "var(--neutral)");
      } else {
        const cs = rampa(Math.max(1, chaves.filter(k => k !== "Não informado").length));
        let i = 0; cores = chaves.map(k => k === "Não informado" ? "var(--neutral)" : cs[i++]);
      }
      corpo.innerHTML = `<div class="legend"></div><div class="plot"></div>`;
      empilhadas(corpo.querySelector(".plot"), corpo.querySelector(".legend"), linhas, chaves, cores);
    },
    tabela(corpo, w, doc) {
      const hojeD = CD.hoje();
      const linhas = selecionar(doc, w.config)
        .map(p => ({ ...p, d: p.statusDesde ? Math.max(0, Math.floor(dias(parseData(p.statusDesde), hojeD))) : null }))
        .sort((a, b) => (b.d ?? -1) - (a.d ?? -1));
      corpo.innerHTML = `<div class="table-scroll"><table>
        <thead><tr><th>Nome do Projeto</th><th>Responsável</th><th>Etapa</th><th class="num">Dias no status atual</th><th>Motivo do Bloqueio</th></tr></thead>
        <tbody>${linhas.length ? linhas.map(r => `<tr>
          <td>${esc(r.nome)}</td><td>${esc(r.responsavel)}</td><td><span class="pill">${esc(r.etapa)}</span></td>
          <td class="num ${r.d >= 7 ? "age-hi" : ""}">${r.d ?? "—"}${r.d >= 7 ? " ⚠" : ""}</td>
          <td>${esc(r.motivo || "Não informado")}</td></tr>`).join("") : `<tr><td colspan="5" class="empty">Nenhum projeto neste recorte.</td></tr>`}</tbody>
      </table></div>`;
    },
  };

  // controles locais (não salvos): alternar agrupamento / empilhamento na visualização
  const CONTROLES = {
    vazao: w => ({ chave: "agrupamento", atual: String(w.config.agrupamento || 7), opcoes: { 7: "Semana", 14: "Quinzena", 30: "Mês" } }),
    alocacao: w => ({ chave: "empilhar", atual: w.config.empilhar || "etapa", opcoes: { etapa: "Etapa", especialidade: "Especialidade" } }),
  };

  function desenharDashboard(raiz, doc) {
    esconderTip();
    const secoes = doc.secoes.map(s => ({ ...s, widgets: s.widgets.filter(w => w.visivel !== false && RENDER[w.tipo]) })).filter(s => s.widgets.length);
    if (!secoes.length) { raiz.innerHTML = `<p class="vazio-dash">Nenhuma seção visível. Adicione seções e gráficos no <a href="admin/">admin</a>.</p>`; return; }
    raiz.innerHTML = secoes.map((s, i) => `<h2>${i + 1} · ${esc(s.titulo)}</h2><div class="grid secao">${s.widgets.map(w => {
      const ctl = CONTROLES[w.tipo] && CONTROLES[w.tipo](w);
      const atual = ctl && (estadoLocal[w.id]?.[ctl.chave] || ctl.atual);
      return `<div class="card w-${esc(w.largura || "medio")}${w.tipo.startsWith("kpi") ? " tile" : ""}" data-w="${esc(w.id)}">
        <div class="card-head"><div><h3>${esc(w.titulo)}</h3>${w.descricao ? `<p class="hint">${esc(w.descricao)}</p>` : ""}</div>
        ${ctl ? `<div class="seg" role="group">${Object.entries(ctl.opcoes).map(([k, v]) => `<button data-ctl="${esc(ctl.chave)}" data-v="${esc(k)}" aria-pressed="${String(atual) === k}">${esc(v)}</button>`).join("")}</div>` : ""}</div>
        <div class="corpo"></div></div>`;
    }).join("")}</div>`).join("");
    const porId = Object.fromEntries(secoes.flatMap(s => s.widgets).map(w => [w.id, w]));
    raiz.querySelectorAll("[data-w]").forEach(card => {
      const w = porId[card.dataset.w];
      try { RENDER[w.tipo](card.querySelector(".corpo"), w, doc, estadoLocal[w.id] || {}); }
      catch (e) { console.error(e); card.querySelector(".corpo").innerHTML = `<p class="empty">Não foi possível desenhar este item. Revise a configuração no admin.</p>`; }
      card.querySelectorAll("[data-ctl]").forEach(b => b.onclick = () => {
        (estadoLocal[w.id] ||= {})[b.dataset.ctl] = b.dataset.v;
        desenharDashboard(raiz, doc);
      });
    });
  }
  const estadoLocal = {};

  g.CDCharts = { desenharDashboard, CAMPOS };
})(window);
