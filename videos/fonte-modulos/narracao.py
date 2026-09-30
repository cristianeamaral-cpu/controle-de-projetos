# Narração sintética ágil: pf_dora, velocidade 1,04, pausas internas encurtadas (máx. 0,18 s).
import soundfile as sf, json, numpy as np
from kokoro_onnx import Kokoro
k=Kokoro('voices/kokoro-v1.0.onnx','voices/voices-v1.0.bin')
segs=[
 "A seguir, apresentamos os módulos complementares desenvolvidos para fortalecer o seu perfil profissional.",
 "Na aba Eventos, é gerado um kiuár côudi exclusivo para as suas apresentações.",
 "Ao final do evento, os participantes podem escanear o código para avaliar a palestra e emitir o certificado de participação imediatamente.",
 "Além disso, o arquivo do certificado fica disponível para dáunlôudi e divulgação em suas redes profissionais.",
 "Na aba Depoimentos, você gerencia sua prova social com total controle: as avaliações recebidas são publicadas somente após a sua aprovação manual.",
 "Na aba Biblioteca, é possível cadastrar suas publicações, artigos e materiais autorais, inserindo línks diretos para canais de venda como a Ámazon ou sua loja própria.",
 "Por fim, na aba Informações para Curso, preencha os dados de logística interna, que serão utilizados exclusivamente pela equipe pê ésse á no planejamento e na organização de eventos presenciais.",
 "Mantenha essas informações sempre atualizadas para potencializar a sua visibilidade e autoridade na plataforma!",
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
    s,sr=k.create(t,voice='pf_dora',speed=1.04,lang='pt-br')
    idx=np.where(np.abs(s)>0.006)[0]; a=max(idx[0]-int(.02*sr),0); b=min(idx[-1]+int(.12*sr),len(s))
    s=squeeze(s[a:b].copy(),sr); n=int(.02*sr); s[:n]*=np.linspace(0,1,n); m=int(.08*sr); s[-m:]*=np.linspace(1,0,m)
    sf.write(f'vo/s{i}.wav',s,sr); out.append(round(len(s)/sr,2))
print(json.dumps(out))
