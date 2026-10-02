# Narração offline (Kokoro, voz masculina pm_alex) + timeline.json com início/duração das cenas
import sys, json, numpy as np, soundfile as sf
sys.path.insert(0,'.'); import psa_fix
from kokoro_onnx import Kokoro
k=Kokoro('voices/kokoro-v1.0.onnx','voices/voices-v1.0.bin')
R=json.load(open('v10/roteiro.json')); t=0.0; out=[]
for sc in R:
    s,sr=psa_fix.create(k,sc['vo'],voice='pm_alex',speed=1.12)
    idx=np.where(np.abs(s)>0.006)[0]; s=s[max(idx[0]-int(.02*sr),0):idx[-1]+int(.12*sr)].copy()
    m=int(.06*sr); s[-m:]*=np.linspace(1,0,m)
    sf.write(f"v10/audio/{sc['id']}.wav",s,sr); a=len(s)/sr
    d=max(sc['min'],a+0.55+0.15)
    out.append({'id':sc['id'],'start':round(t,3),'dur':round(d,3),'voStart':round(t+0.15,3),'voDur':round(a,3),'vo':sc['vo']}); t+=d
json.dump({'total':round(t,3),'scenes':out},open('v10/timeline.json','w'),ensure_ascii=False,indent=1)
for o in out: print(o['id'],o['start'],o['dur'],o['voDur'])
print('total',round(t,2))
