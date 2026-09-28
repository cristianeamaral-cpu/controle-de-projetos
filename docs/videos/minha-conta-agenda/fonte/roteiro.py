import json,html,re
segs=json.load(open("segs.json")); tl=json.load(open("tl.json")); T,D=tl["T"],tl["D"]
text={s[0]:s[1] for s in segs}; dirn={s[0]:s[3] for s in segs}
groups=[["intro"],["c0","c1","c2","c3","c4","c4b"],["c5"],["s1","s1b"],["s2","p1","p1b"],["p2","p2b"],["p3","p3b"],["d0"],["d1","d2","d3","d3b"],["f1"],["f2"],["out"]]
tela=["Abertura com o título","Minha Conta: dados, plano, créditos e PSA Score em destaque","Cursor clica em “Sincronizar calendário”","Tela Sincronizar calendário; destaque “menos de um minuto”","“Como funciona” + passo 1 com janela de autorização (clique em Permitir)","Passo 2 + semana sendo mapeada","Passo 3 + agenda unificada (PSA + Google)","Cartão “O que acessamos”","Datas, horários, títulos e local em destaque + mapa","Clique em “Conectar Google Calendar”","Destaque em “Desconectar”","Encerramento"]
def fmt(x): return f"{int(x//60)}:{x%60:04.1f}"
def ts(x): return f"{int(x//3600):02}:{int(x%3600//60):02}:{int(x%60):02},{int(round((x%1)*1000))%1000:03}"
rows="";srt=""
for i,g in enumerate(groups,1):
    t=" ".join(text[x] for x in g); a=T[g[0]]; e=T[g[-1]]+D[g[-1]]
    d=" ".join(x for x in [dirn[k] for k in g] if x and "Emende" not in x and "Sem pausa" not in x and "Fluido" not in x) or "Fluido."
    rows+=f"<tr><td class=n>{i:02}</td><td class=t>{fmt(a)}<small>≈ {e-a:.1f}s</small></td><td class=s>{html.escape(tela[i-1])}</td><td class=f>{html.escape(t)}</td><td class=d>{html.escape(d)}</td></tr>"
    srt+=f"{i}\n{ts(a)} --> {ts(e+.1)}\n{t}\n\n"
open("legendas.srt","w").write(srt)
words=len(" ".join(s[1] for s in segs).split())
page=open("../v3/roteiro.html").read()
page=re.sub(r"<table>.*</table>",f"<table><tr><th>#</th><th>Início</th><th>Na tela</th><th>Fala</th><th>Direção</th></tr>{rows}</table>",page,flags=re.S)
page=re.sub(r"duração total ≈ \d+s · \d+ falas · \d+ palavras",f"duração total ≈ {tl['END']:.0f}s · {len(groups)} falas · {words} palavras",page)
page=re.sub(r"<div class=box><b>Ritmo</b>.*?</div>","<div class=box><b>Ritmo</b>Fluido e natural, como numa conversa: cerca de 170 palavras por minuto. Leia cada fala de uma vez só, emendando as vírgulas.</div>",page,flags=re.S)
page=re.sub(r"<div class=box><b>Pausas</b>.*?</div>","<div class=box><b>Pausas</b>Só entre uma fala e outra (meio segundo). Dentro da fala, respire apenas nas vírgulas e nos dois-pontos, sem parar.</div>",page,flags=re.S)
page=page.replace("Os tempos batem com o vídeo “sem narração”.","Os tempos batem com o vídeo “sem narração”.")
open("roteiro.html","w").write(page)
