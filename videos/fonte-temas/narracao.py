# Narração sintética fluida (padrão da série): pf_dora, velocidade 0,98, caudas com fade.
import soundfile as sf, json, numpy as np
from kokoro_onnx import Kokoro
k=Kokoro('voices/kokoro-v1.0.onnx','voices/voices-v1.0.bin')
segs=[
 "A seleção correta dos seus temas é o que define a quais oportunidades de palestras você poderá se candidatar!",
 "Na aba Temas, você pode selecionar múltiplos Macro Temas, para mapear todas as suas áreas de atuação.",
 "Porém, atenção a esta regra: você deve escolher exatamente um Tema Principal.",
 "Ele será a sua maior bandeira na plataforma.",
 "Escolha com cuidado, pois o algoritmo cruza esses temas com os brífins enviados pelos clientes!",
]
out=[]
for i,t in enumerate(segs):
    s,sr=k.create(t,voice='pf_dora',speed=0.98,lang='pt-br')
    idx=np.where(np.abs(s)>0.006)[0]; a=max(idx[0]-int(.05*sr),0); b=min(idx[-1]+int(.3*sr),len(s))
    s=s[a:b].copy(); n=int(.03*sr); s[:n]*=np.linspace(0,1,n); m=int(.2*sr); s[-m:]*=np.linspace(1,0,m)
    sf.write(f'vo/s{i}.wav',s,sr); out.append(round(len(s)/sr,2))
print(json.dumps(out))
