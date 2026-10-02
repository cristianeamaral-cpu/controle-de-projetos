import json,re,unicodedata
TL=json.load(open('timeline.json')); S={s['id']:s for s in TL['scenes']}
h=open('video.tpl.html').read()
ALIAS={'gúgou':'Google','Linquedín':'LinkedIn'}   # grafias fonéticas (Kokoro) → texto do kit
def norm(x): return ''.join(c for c in unicodedata.normalize('NFD',x.lower()) if c.isalnum())
def W(m):
    sc,w,extra=m.group(1),m.group(2),m.group(3) or ''
    s=S[sc]; vo=s['vo']; v=None
    if s.get('words'):                      # tempos reais da voz do kit (WordBoundary)
        cand=[w,ALIAS.get(w,w)]
        for t,tok in s['words']:
            if any(norm(tok).startswith(norm(c)) or norm(c).startswith(norm(tok)) and len(norm(tok))>=4 for c in cand):
                v=0.15+t; break
    if v is None:                           # estimativa proporcional ao texto
        i=-1
        for c in (w,ALIAS.get(w,w)):
            i=vo.find(c)
            if i>=0: break
        assert i>=0,(sc,w)
        v=0.15+i/len(vo)*s['voDur']
    return str(round(v+(float(extra) if extra else 0),3))
h=re.sub(r"\{W:(\w+):([^}+]+)\}(?:\+([\d.]+))?",W,h)
h=h.replace('%%TL%%',json.dumps({'total':TL['total'],'scenes':[{k:v for k,v in s.items() if k!='words'} for s in TL['scenes']]}))
open('build/video.html','w').write(h)
print('ok',TL['total'])
