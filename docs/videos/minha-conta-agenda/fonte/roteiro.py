import json,html
segs=json.load(open("segs.json")); tl=json.load(open("tl.json")); T,D=tl["T"],tl["D"]
tela={"intro":"Abertura: título “Minha Conta e Sincronização de Agenda”","c0":"Tela Minha Conta (visão geral)","c1":"Destaque: Dados cadastrais","c2":"Destaque: Seu plano","c3":"Destaque: Créditos (barra enche)","c4":"Destaque: PSA Score (indicador sobe até 87)","c4b":"Etiqueta “Qualidade da sua jornada profissional”","c5":"Cursor clica em “Sincronizar calendário”","s1":"Tela Sincronizar calendário (visão geral)","s1b":"Destaque: “Leva menos de um minuto”","s2":"Destaque: cartão “Como funciona”","p1":"Passo 1 + etiqueta “Autorizar acesso”","p1b":"Janela de autorização; clique em “Permitir”","p2":"Passo 2 + etiqueta “Mapear disponibilidade”","p2b":"Semana sendo lida; datas e locais","p3":"Passo 3 + etiqueta “Visualização unificada”","p3b":"Agenda unificada: eventos PSA + Google","d0":"Destaque: cartão “O que acessamos”","d1":"Destaque: Datas e Horários","d2":"Destaque: Títulos dos eventos","d3":"Destaque: Local dos eventos","d3b":"Mapa com oportunidades na região","f1":"Clique em “Conectar Google Calendar”","f2":"Destaque: “Desconectar”","out":"Encerramento: “Agenda organizada, mais oportunidades.”"}
def fmt(x): return f"{int(x//60)}:{x%60:04.1f}"
rows=""
for i,(k,txt,gap,dirn) in enumerate(segs,1):
    txt=html.escape(txt).replace(", ",", <span class=p>/</span> ").replace(": ",": <span class=p>/</span> ")
    mark='<span class=p>//</span>' if gap>=0.9 else '<span class=p>/</span>'
    rows+=f"<tr><td class=n>{i:02}</td><td class=t>{fmt(T[k])}<small>≈ {D[k]:.1f}s</small></td><td class=s>{html.escape(tela[k])}</td><td class=f>{txt} {mark}</td><td class=d>{html.escape(dirn)}</td></tr>"
total=len(" ".join(s[1] for s in segs).split())
page=f"""<!doctype html><html lang=pt-BR><head><meta charset=utf-8><link href="fonts/fonts.css" rel="stylesheet"><style>
@page{{size:A4 landscape;margin:14mm}}
body{{font-family:Manrope,sans-serif;color:#141414;font-size:10.5pt;margin:0}}
h1,h2,.stamp{{font-family:Anton,sans-serif;font-weight:400;text-transform:uppercase;letter-spacing:.5px}}
.cover{{background:#050505;color:#fff;padding:26px 30px;border-radius:10px;position:relative;overflow:hidden}}
.cover:after{{content:"";position:absolute;right:-120px;top:-160px;width:520px;height:520px;border-radius:50%;background:radial-gradient(circle,rgba(9,60,167,.9),rgba(9,60,167,0) 65%)}}
.logo{{font-family:Anton;font-size:30pt;position:relative;z-index:1}} .logo i{{font-style:normal;color:#FF650F}}
h1{{font-size:30pt;margin:6px 0 4px;line-height:1.05;position:relative;z-index:1}} h1 em{{font-style:normal;color:#FF650F}}
.cover p{{position:relative;z-index:1;margin:4px 0;font-size:11pt;opacity:.9}}
.stamp{{display:inline-block;color:#FF650F;border:2.5px solid #FF650F;padding:2px 10px;transform:rotate(-3deg);font-size:13pt;margin-top:8px;position:relative;z-index:1}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:14px 0}}
.box{{border:1.5px solid #E6E6EA;border-radius:10px;padding:10px 12px}}
.box b{{display:block;font-family:Anton;font-weight:400;text-transform:uppercase;color:#093CA7;font-size:12pt;letter-spacing:.4px;margin-bottom:3px}}
h2{{color:#093CA7;font-size:16pt;margin:14px 0 6px}}
table{{width:100%;border-collapse:collapse}} th{{background:#093CA7;color:#fff;text-align:left;font-weight:800;padding:7px 8px;font-size:9.5pt}}
td{{border-bottom:1px solid #E6E6EA;padding:8px;vertical-align:top}} tr{{page-break-inside:avoid}}
td.n{{font-family:Anton;color:#FF650F;font-size:13pt;width:28px}} td.t{{width:62px;font-weight:800}} td.t small{{display:block;font-weight:600;color:#888;font-size:8.5pt}}
td.s{{width:190px;color:#555;font-size:9.5pt}} td.f{{font-size:12pt;font-weight:600;line-height:1.45}} td.d{{width:200px;color:#555;font-size:9.5pt;font-style:italic}}
.p{{color:#FF650F;font-weight:800}}
</style></head><body>
<div class=cover><div class=logo>PSA<i>.</i></div><h1>Roteiro de gravação<br><em>Minha Conta e Sincronização de Agenda</em></h1>
<p>Vídeo explicativo para palestrantes · locução feminina · duração total ≈ {tl['END']:.0f}s · {len(segs)} falas · {total} palavras</p><div class=stamp>Sugestão de locução</div></div>
<div class=grid>
<div class=box><b>Tom</b>Acolhedor e didático, como quem apresenta a plataforma a um colega. Sorria ao falar, principalmente na abertura e no fechamento.</div>
<div class=box><b>Ritmo</b>Calmo: cerca de 130–140 palavras por minuto. É o primeiro contato do palestrante com a funcionalidade, então dê tempo para ele olhar a tela.</div>
<div class=box><b>Pausas</b><span class=p>/</span> pausa curta (≈0,4s) &nbsp;·&nbsp; <span class=p>//</span> pausa longa (≈1s). Nas falas “Primeiro, segundo, terceiro passo”, respire antes de explicar.</div>
<div class=box><b>Gravação</b>Grave cada fala em arquivo separado (01, 02…) ou numa faixa única, respeitando as pausas. Os tempos batem com o vídeo “sem narração”.</div>
</div>
<h2>Falas e marcações</h2>
<table><tr><th>#</th><th>Início</th><th>Na tela</th><th>Fala</th><th>Direção</th></tr>{rows}</table>
<p style="margin-top:10px;color:#666;font-size:9pt">Pronúncia: “Google Calendar” como <b>gúgol calêndar</b> · “PSA” letra por letra (<b>pê-ésse-á</b>) · “Score” como <b>scór</b>.</p>
</body></html>"""
open("roteiro.html","w").write(page)
