# Narração mais fluida: velocidade natural, pontuação para respiração, caudas preservadas com fade.
import soundfile as sf, json, numpy as np
from kokoro_onnx import Kokoro
k=Kokoro('voices/kokoro-v1.0.onnx','voices/voices-v1.0.bin')
segs=[
 "Com o primeiro lóguin concluído, o próximo passo é estruturar e preencher sua página na plataforma pê ésse á.",
 "Ao acessar a aba Meu Perfil, você visualizará o indicador de Força da sua Página, na parte superior.",
 "O objetivo é atingir cem por cento de preenchimento.",
 "Atente-se à escolha da sua foto de perfil, pois a imagem enviada neste campo será exatamente a mesma exibida publicamente no site da pê ésse á, para os contratantes.",
 "Ela representa a sua imagem profissional no mercado.",
 "Em seguida, preencha a Sua Biografia Profissional. Este espaço serve para descrever sua trajetória, conquistas, e experiência de palco.",
 "Para otimizar o tempo de preenchimento, você pode utilizar o recurso Gerar com i á, para obter uma sugestão estruturada.",
 "Abaixo, insira sua Frase de Destaque: um resumo objetivo do seu posicionamento, entre trinta e sessenta caracteres.",
 "Prossiga com o preenchimento dos Dados Pessoais: Nome, Nome Artístico, cê pê éfe, érre gê, e Formação.",
 "E das informações de Contato, incluindo o uatsáp, e um contato de emergência.",
 "Na seção Redes Sociais, inclua os línks do instagrã, feicibúqui, Linquedín, e o vídeo em destaque do iutúbi.",
 "Por fim, informe sua Localização, essencial para o cálculo logístico dos eventos, e selecione as opções referentes ao Seu momento atual.",
 "Ao concluir e salvar as alterações, seu perfil estará completo, atualizado, e pronto para visualização pelos contratantes.",
]
out=[]
for i,t in enumerate(segs):
    s,sr=k.create(t,voice='pf_dora',speed=0.98,lang='pt-br')
    idx=np.where(np.abs(s)>0.006)[0]; a=max(idx[0]-int(.05*sr),0); b=min(idx[-1]+int(.3*sr),len(s))
    s=s[a:b].copy(); n=int(.03*sr); s[:n]*=np.linspace(0,1,n); m=int(.2*sr); s[-m:]*=np.linspace(1,0,m)
    sf.write(f'vo/s{i}.wav',s,sr); out.append(round(len(s)/sr,2))
print(json.dumps(out))
