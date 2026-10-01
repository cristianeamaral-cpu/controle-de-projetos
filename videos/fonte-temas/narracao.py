# Narração sintética ágil: pf_dora, velocidade 1,04, pausas internas encurtadas (máx. 0,18 s).
import soundfile as sf, json, numpy as np
from kokoro_onnx import Kokoro
import sys; sys.path.insert(0,'.'); import psa_fix
k=Kokoro('voices/kokoro-v1.0.onnx','voices/voices-v1.0.bin')
segs=[
 "A seleção correta dos seus temas é fundamental para direcionar a sua carreira na plataforma!",
 "Na aba Temas, você pode escolher múltiplos Macro Temas.",
 "Quanto mais macrotemas alinhados à sua ekspertíze você selecionar, mais você amplia as suas possibilidades de candidatura a oportunidades e abre um leque ainda maior para gerar pesquisas e insáits no pê ésse á Tréndis.",
 "Porém, atenção a esta regra importante: você deve escolher exatamente um Tema Principal.",
 "Ele será a sua maior bandeira e o seu principal posicionamento no mercado.",
 "Escolha com atenção, pois nosso algoritmo utiliza essa seleção para cruzar seus dados com os brífins dos clientes e potencializar seus resultados!",
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
    sf.write(f'vo/s{i}.wav',s,sr); out.append(round(len(s)/sr,2))
print(json.dumps(out))
