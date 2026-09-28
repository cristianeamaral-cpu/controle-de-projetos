import json,sys
from kokoro_onnx import Kokoro
import soundfile as sf, numpy as np
k=Kokoro("kokoro.onnx","voices.bin")
segs=json.load(open("segs.json"))
# pronunciation fixes
fix=[("PSA Score","PSA Scór"),("na PSA","na pê ésse á"),("Google Calendar","Gúgol Calêndar")]
out={}
for key,t in segs:
    for a,b in fix: t=t.replace(a,b)
    print(key, k.tokenizer.phonemize(t,'pt-br'))
    s,sr=k.create(t,voice=sys.argv[1] if len(sys.argv)>1 else "pf_dora",speed=0.98,lang="pt-br")
    # trim silence
    idx=np.where(np.abs(s)>0.01)[0]; s=s[max(0,idx[0]-500):idx[-1]+2400]
    sf.write(f"audio/{key}.wav",s,sr); out[key]=len(s)/sr
json.dump(out,open("durs.json","w"),indent=1); print(out)
