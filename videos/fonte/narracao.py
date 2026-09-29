import soundfile as sf, json, numpy as np
from kokoro_onnx import Kokoro
k=Kokoro('voices/kokoro-v1.0.onnx','voices/voices-v1.0.bin')
segs=[
 "Olá, palestrante! Seja bem-vindo ao Ecossistema pê ésse á.",
 "Neste vídeo, vou te mostrar como é simples e rápido acessar a nossa plataforma.",
 "Acesse o site profissionais ésse á, ponto com, ponto bê érre, e clique em lóguin, no canto superior direito.",
 "Você pode entrar digitando seu imêiu cadastrado, ou clicando diretamente no botão do gúgou, ou do Linquedín.",
 "Dica importante: Por conformidade com a éle gê pê dê, cada palestrante deve possuir apenas um perfil único.",
 "Não sendo permitido criar lóguins secundários para assessores ou assistentes.",
 "Além disso, recomendamos usar o navegador gúgou Crôume, para ter a melhor experiência possível.",
 "Faça seu lóguin, e nos vemos no próximo vídeo!",
]
out=[]
for i,t in enumerate(segs):
    s,sr=k.create(t,voice='pf_dora',speed=1.05,lang='pt-br')
    # trim silence
    idx=np.where(np.abs(s)>0.01)[0]; s=s[max(idx[0]-800,0):idx[-1]+1600]
    sf.write(f'vo/s{i}.wav',s,sr); out.append(len(s)/sr)
print(json.dumps([round(d,2) for d in out]), sr)
