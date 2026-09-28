import json
from kokoro_onnx import Kokoro
import soundfile as sf, numpy as np
k=Kokoro("kokoro.onnx","voices.bin")
segs=json.load(open("v3/segs.json"))
fix=[("PSA Score","PSA Scór"),("na PSA","na pê ésse á"),("Google Calendar","Gúgol Calêndar")]
out={}
for key,t,_,_ in segs:
    for a,b in fix: t=t.replace(a,b)
    s,sr=k.create(t,voice="pf_dora",speed=1.06,lang="pt-br")
    idx=np.where(np.abs(s)>0.01)[0]; s=s[max(0,idx[0]-500):idx[-1]+2400]
    sf.write(f"v3/audio/{key}.wav",s,sr); out[key]=len(s)/sr
json.dump(out,open("v3/durs.json","w"),indent=1); print(out, sum(out.values()))
