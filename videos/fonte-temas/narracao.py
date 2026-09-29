# Narração sintética fluida (padrão da série): pf_dora, velocidade 0,98, caudas com fade.
import soundfile as sf, json, numpy as np
from kokoro_onnx import Kokoro
k=Kokoro('voices/kokoro-v1.0.onnx','voices/voices-v1.0.bin')
segs=[
 "A seleção correta dos seus temas é fundamental para direcionar a sua carreira na plataforma!",
 "Na aba Temas, você pode escolher múltiplos Macro Temas.",
 "Quanto mais macrotemas alinhados à sua ekspertíze você selecionar, mais você amplia as suas possibilidades de candidatura a oportunidades,",
 "e abre um leque ainda maior para gerar pesquisas e insáits no pê ésse á Tréndis.",
 "Porém, atenção a esta regra importante: você deve escolher exatamente um Tema Principal.",
 "Ele será a sua maior bandeira, e o seu principal posicionamento no mercado.",
 "Escolha com carinho, pois nosso algoritmo utiliza essa seleção para cruzar seus dados com os brífins dos clientes, e potencializar seus resultados!",
]
out=[]
for i,t in enumerate(segs):
    s,sr=k.create(t,voice='pf_dora',speed=0.98,lang='pt-br')
    idx=np.where(np.abs(s)>0.006)[0]; a=max(idx[0]-int(.05*sr),0); b=min(idx[-1]+int(.3*sr),len(s))
    s=s[a:b].copy(); n=int(.03*sr); s[:n]*=np.linspace(0,1,n); m=int(.2*sr); s[-m:]*=np.linspace(1,0,m)
    sf.write(f'vo/s{i}.wav',s,sr); out.append(round(len(s)/sr,2))
print(json.dumps(out))
