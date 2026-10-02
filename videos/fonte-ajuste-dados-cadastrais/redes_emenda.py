# Cena "redes": gera em duas partes para o LinkedIn sair com a tônica na 1ª sílaba (LÍN-que-din),
# como se fala no Brasil, e emenda na pausa natural da vírgula. Grava em audio_aprovado/redes.wav.
import numpy as np, soundfile as sf, librosa
ns={}; exec(open('tts_piper.py').read().split('TOTAL=')[0], ns); tts=ns['tts']
def syn(t):
    g=tts.generate(t,sid=0,speed=1.0); y=librosa.resample(np.array(g.samples),orig_sr=g.sample_rate,target_sr=48000)
    i=np.where(np.abs(y)>0.006)[0]; return y[i[0]:i[-1]+int(.03*48000)]
a=syn('Em redes sociais, inclua Instagrã, Facebook,')
b=syn('Línquedim e o seu vídeo do Iutúbi.')
fa=np.linspace(1,0,int(.02*48000)); a[-len(fa):]*=fa
s=np.concatenate([a,np.zeros(int(.16*48000)),b])
sf.write('audio_aprovado/redes.wav',s,48000); print('redes', round(len(s)/48000,2),'s')
