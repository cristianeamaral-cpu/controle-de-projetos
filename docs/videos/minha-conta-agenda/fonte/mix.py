import numpy as np, soundfile as sf, librosa, json
from scipy.signal import butter, sosfilt, fftconvolve
sr=48000
v,_=librosa.load("v9/voz_crua.wav",sr=sr); m,_=sf.read("v9/trilha.wav")
N=min(len(v),len(m)); v=v[:N]; m=m[:N]
m=m-0.5*sosfilt(butter(2,170,'low',fs=sr,output='sos'),m)+0.8*sosfilt(butter(2,3000,'high',fs=sr,output='sos'),m)
def sos(t,f,**k): return butter(2,f,t,fs=sr,output='sos')
# voz: passa-altas, presença, compressão suave, ambiência leve
v=sosfilt(sos('high',85),v)
pres=sosfilt(butter(2,[2500,5000],'band',fs=sr,output='sos'),v); v=v+0.35*pres
air=sosfilt(butter(2,6000,'high',fs=sr,output='sos'),v); v=v+0.6*air
warm=sosfilt(butter(2,[160,320],'band',fs=sr,output='sos'),v); v=v+0.15*warm
env=np.sqrt(np.convolve(v**2,np.ones(480)/480,'same'))+1e-6
thr=0.08; g=np.where(env>thr,(thr/env)**0.5,1.0); g=np.convolve(g,np.ones(240)/240,'same'); v=v*g
rng=np.random.default_rng(3); L=int(.5*sr); ir=rng.standard_normal(L)*np.exp(-np.arange(L)/sr*11); ir/=np.sqrt((ir**2).sum())
v=v+0.07*fftconvolve(v,ir)[:N]
v=v/np.max(np.abs(v))*0.8
# ducking: trilha abaixa sob a voz
ve=np.convolve(np.abs(v),np.ones(2400)/2400,'same'); speak=(ve>0.01).astype(float)
duck=np.convolve(speak,np.ones(int(.35*sr))/int(.35*sr),'same')
gain=0.30-0.17*np.clip(duck,0,1)   # ~-10 dB sem voz, ~-18 dB sob a voz
mix=v+m*gain
rms=np.sqrt((mix**2).mean()); mix=mix*(10**(-16.5/20)/rms); mix=np.tanh(mix*1.1)/1.1; mix=mix/max(1,np.max(np.abs(mix))/0.97)
sf.write("v9/mix.wav",mix.astype(np.float32),sr)
sf.write("v9/trilha_sem_voz.wav",(m*0.30/np.max(np.abs(m*0.30))*0.6).astype(np.float32),sr)
def bands(y):
    S=np.abs(librosa.stft(y)); fq=librosa.fft_frequencies(sr=sr); s=S.mean(1)
    return [round(20*np.log10(s[(fq>=a)&(fq<b)].mean()),1) for a,b in [(20,80),(80,200),(200,500),(500,2000),(2000,6000),(6000,12000)]]
r,_=librosa.load("ref/ref.wav",sr=sr)
for n,y in [("ref",r),("nosso",mix),("trilha",m)]:
    b=bands(y); print(n,[x-b[2] for x in b], 'rms dB',round(20*np.log10(np.sqrt((y**2).mean())),1))
