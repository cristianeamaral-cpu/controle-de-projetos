import json,re
TL=json.load(open('timeline.json')); S={s['id']:s for s in TL['scenes']}
h=open('video.tpl.html').read()
def W(m):
    sc,w,extra=m.group(1),m.group(2),m.group(3) or ''
    s=S[sc]; vo=s['vo']; i=vo.find(w); assert i>=0,(sc,w)
    v=0.15+i/len(vo)*s['voDur']
    return str(round(v+(float(extra) if extra else 0),3))
h=re.sub(r"\{W:(\w+):([^}+]+)\}(?:\+([\d.]+))?",W,h)
h=h.replace('%%TL%%',json.dumps(TL))
open('build/video.html','w').write(h)
print('ok',TL['total'])
