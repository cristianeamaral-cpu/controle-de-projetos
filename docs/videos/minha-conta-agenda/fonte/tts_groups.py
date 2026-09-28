import json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
k=Kokoro("kokoro.onnx","voices.bin")
VOICE="pm_alex"
segs=json.load(open("v7/segs.json")); d=json.load(open("v7/durs.json"))
groups=[["intro"],["c0","c1","c2","c3","c4","c4b"],["c5"],["s1","s1b"],["s2","p1","p1b"],["p2","p2b"],["p3","p3b"],["d0"],["d1","d2","d3","d3b"],["f1"],["f2"],["out"]]
text={s[0]:s[1] for s in segs}; gap={s[0]:s[2] for s in segs}
fix=[("PSA Score","PSA Scór"),("na PSA","na pê ésse á"),("Google Calendar","Gúgol Calêndar"),("conta do Google","conta do Gúgol"),("eventos do Google","eventos do Gúgol")]
sr=24000; T={}; D={}; clips=[]; c=0.7
extra={"intro":0.3,"c5":0.8,"p1b":0.7,"f1":0.8,"f2":0.2}
for g in groups:
    t=" ".join(text[x] for x in g)
    for a,b in fix: t=t.replace(a,b)
    s,_=k.create(t,voice=VOICE,speed=1.0,lang="pt-br")
    idx=np.where(np.abs(s)>0.01)[0]; s=s[max(0,idx[0]-400):idx[-1]+2400]
    L=len(s)/sr
    # estimate boundaries from separate-fragment durations, snap to nearest silence
    fr=np.array([d[x] for x in g]); cum=np.cumsum(fr)/fr.sum()*L
    env=np.convolve(np.abs(s),np.ones(480)/480,'same')
    starts=[0.0]
    for b in cum[:-1]:
        lo,hi=int(max(0,b-0.6)*sr),int(min(L,b+0.6)*sr)
        w=env[lo:hi]; i=lo+int(np.argmin(w)); starts.append(i/sr)
    for j,x in enumerate(g):
        T[x]=round(c+starts[j],3); end=starts[j+1] if j+1<len(g) else L; D[x]=round(end-starts[j],3)
    clips.append((c,s)); last=g[-1]
    c+=L+gap[last]+extra.get(last,0)
END=round(c+2.8,2)
N=int(END*sr); v=np.zeros(N)
for t0,s in clips: i=int(t0*sr); v[i:i+len(s)]+=s
v=v/np.max(np.abs(v))*0.89
fade=np.clip((END-np.arange(N)/sr)/0.5,0,1)
sf.write("v7/voz_crua.wav",v*fade,sr)
json.dump({"T":T,"D":D,"END":END},open("v7/tl.json","w"),indent=1)
print(END, {x:(T[x],D[x]) for x in T})
