# Narração sintética ágil: pf_dora, velocidade 1,04, pausas internas encurtadas (máx. 0,18 s).
import soundfile as sf, json, numpy as np
from kokoro_onnx import Kokoro
import sys; sys.path.insert(0,'.'); import psa_fix
k=Kokoro('voices/kokoro-v1.0.onnx','voices/voices-v1.0.bin')
segs=[
 "Quer saber como melhorar sua perfórmance de palco?",
 "Use a Análise de Palestra por IA para vídeos de até uma hora e meia!",
 "Ela oferece duas modalidades: a Essencial, gratuita para análise inicial,",
 "e a Completa, que avalia mais de quarenta e cinco pontos de perfórmance em cinco eixos detalhados.",
 "Os seus créditos de i á são renovados mensalmente no seu plano.",
 "Se precisar de mais créditos antes da virada do mês, você pode adquirir pacotes adicionais a qualquer momento!",
]
def squeeze(s,sr,maxp=.18,thr=.008):
    fr=int(.01*sr); e=np.array([np.abs(s[i:i+fr]).max() for i in range(0,len(s),fr)]); q=e<thr
    out=[];i=0;n=len(q)
    while i<n:
        j=i
        while j<n and q[j]==q[i]: j+=1
        seg=s[i*fr:j*fr]
        if q[i] and (j-i)*.01>maxp and i>0 and j<n:
            keep=int(maxp*sr); h=keep//2; seg=np.concatenate([seg[:h],seg[-(keep-h):]])
        out.append(seg); i=j
    return np.concatenate(out)
out=[]
for i,t in enumerate(segs):
    s,sr=psa_fix.create(k,t,voice='pf_dora',speed=1.04)
    idx=np.where(np.abs(s)>0.006)[0]; a=max(idx[0]-int(.02*sr),0); b=min(idx[-1]+int(.12*sr),len(s))
    s=squeeze(s[a:b].copy(),sr); n=int(.02*sr); s[:n]*=np.linspace(0,1,n); m=int(.08*sr); s[-m:]*=np.linspace(1,0,m)
    sf.write(f'vo/s{i}.wav' if __name__!='__main__' else f'vo/s{i}.wav',s,sr); out.append(round(len(s)/sr,2))
print(json.dumps(out))
