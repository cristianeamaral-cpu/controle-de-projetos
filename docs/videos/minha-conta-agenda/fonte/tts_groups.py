# Narração: voz da versão 1 (Kokoro pf_dora, pt-BR, velocidade 0.98)
import json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
k=Kokoro("kokoro.onnx","voices.bin"); VOICE="pf_dora"; SPEED=0.98; sr=24000
segs=json.load(open("v11/segs.json")); text={s[0]:s[1] for s in segs}; gap={s[0]:s[2] for s in segs}
groups=[["c0","c1","c2","c3"],["c5"],["s1","s1b","s2"],["p1","p1b"],["p2","p2b"],["p3","p3b"],["d0","d1","d1h","d3"],["d3b","f2"],["f1","out"]]
fix=[("Google Calendar","Gúgol Calêndar"),("conta do Google","conta do Gúgol"),("da PSA","da pê ésse á")]
def say(t):
    for a,b in fix: t=t.replace(a,b)
    s,_=k.create(t,voice=VOICE,speed=SPEED,lang="pt-br")
    idx=np.where(np.abs(s)>0.01)[0]; return s[max(0,idx[0]-300):idx[-1]+2400]
d={x:len(say(text[x])) for g in groups for x in g}
T={};D={};clips=[];c=3.6
extra={"c3":3.0,"c5":0.8,"p1b":0.7,"f2":0.6}   # c3: pausa para mostrar o PSA Score
for g in groups:
    s=say(" ".join(text[x] for x in g)); L=len(s)/sr
    fr=np.array([d[x] for x in g],float); cum=np.cumsum(fr)/fr.sum()*L
    env=np.convolve(np.abs(s),np.ones(480)/480,'same'); starts=[0.0]
    for b in cum[:-1]:
        lo,hi=int(max(0,b-0.45)*sr),int(min(L,b+0.45)*sr); starts.append((lo+int(np.argmin(env[lo:hi])))/sr)
    for j,x in enumerate(g):
        T[x]=round(c+starts[j],3); D[x]=round((starts[j+1] if j+1<len(g) else L)-starts[j],3)
    fi=int(.01*sr); s[:fi]*=np.linspace(0,1,fi); s[-fi*3:]*=np.linspace(1,0,fi*3)
    clips.append((c,s)); last=g[-1]
    if last=="c3":  # janelas silenciosas do PSA Score (animação)
        e=c+L; T["c4"]=round(e+.35,3); D["c4"]=1.3; T["c4b"]=round(e+1.65,3); D["c4b"]=1.2
    c+=L+gap[last]+extra.get(last,0)
END=round(c+3.4,2); N=int(END*sr); v=np.zeros(N)
for t0,s in clips: i=int(t0*sr); v[i:i+len(s)]+=s
v=v/np.max(np.abs(v))*0.89
sf.write("v11/voz_crua.wav",v,sr); json.dump({"T":T,"D":D,"END":END},open("v11/tl.json","w"),indent=1)
print(END,{x:(T[x],D[x]) for x in T})
