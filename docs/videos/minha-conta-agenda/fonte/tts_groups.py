# Narração: voz masculina pt-BR nativa (Piper "cadu", via sherpa-onnx)
import json, numpy as np, soundfile as sf, sherpa_onnx
V='piper/vits-piper-pt_BR-cadu-medium'
cfg=sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(vits=sherpa_onnx.OfflineTtsVitsModelConfig(
    model=f'{V}/pt_BR-cadu-medium.onnx',tokens=f'{V}/tokens.txt',data_dir=f'{V}/espeak-ng-data',
    noise_scale=0.667,noise_scale_w=0.8,length_scale=1.0),num_threads=4))
tts=sherpa_onnx.OfflineTts(cfg); SPEED=0.86
segs=json.load(open("v8/segs.json")); text={s[0]:s[1] for s in segs}; gap={s[0]:s[2] for s in segs}
groups=[["c0","c1","c2","c3","c4","c4b"],["c5"],["s1","s1b","s2"],["p1","p1b"],["p2","p2b"],["p3","p3b"],["d0","d1","d1h","d3","d2"],["d3b","f2"],["f1","out"]]
fix=[("PSA Score","pê ésse á Scór"),("da PSA","da pê ésse á"),("Google Calendar","Gúgol Calêndar"),("conta do Google","conta do Gúgol")]
def say(t):
    for a,b in fix: t=t.replace(a,b)
    a=tts.generate(t,sid=0,speed=SPEED); s=np.array(a.samples,dtype=np.float32)
    idx=np.where(np.abs(s)>0.01)[0]; return s[max(0,idx[0]-300):idx[-1]+2000], a.sample_rate
d={k:len(say(text[k])[0]) for g in groups for k in g}
T={};D={};clips=[];c=3.6
extra={"c5":0.8,"p1b":0.7,"f2":0.6}
for g in groups:
    s,sr=say(" ".join(text[x] for x in g)); L=len(s)/sr
    fr=np.array([d[x] for x in g],float); cum=np.cumsum(fr)/fr.sum()*L
    env=np.convolve(np.abs(s),np.ones(441)/441,'same'); starts=[0.0]
    for b in cum[:-1]:
        lo,hi=int(max(0,b-0.45)*sr),int(min(L,b+0.45)*sr); starts.append((lo+int(np.argmin(env[lo:hi])))/sr)
    for j,x in enumerate(g):
        T[x]=round(c+starts[j],3); D[x]=round((starts[j+1] if j+1<len(g) else L)-starts[j],3)
    clips.append((c,s)); last=g[-1]; c+=L+gap[last]+extra.get(last,0)
END=round(c+3.4,2); N=int(END*sr); v=np.zeros(N)
for t0,s in clips: i=int(t0*sr); v[i:i+len(s)]+=s
v=v/np.max(np.abs(v))*0.89
sf.write("v8/voz_crua.wav",v,sr); json.dump({"T":T,"D":D,"END":END},open("v8/tl.json","w"),indent=1)
words=sum(len(text[k].split()) for k in text); talk=sum(len(s) for _,s in clips)/sr
print(END,'ppm',round(words/talk*60)); print({x:(T[x],D[x]) for x in T})
