# Trilha sintetizada: eletrônica/cinematográfica escura, 117 BPM, Sol menor
import json, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve
sr=48000; tl=json.load(open("v8/tl.json")); T=tl["T"]; END=tl["END"]
N=int(END*sr); t=np.arange(N)/sr
BPM=117; beat=60/BPM; bar=4*beat
rng=np.random.default_rng(7)
def lp(x,f,o=2): return sosfilt(butter(o,f,'low',fs=sr,output='sos'),x)
def hp(x,f,o=2): return sosfilt(butter(o,f,'high',fs=sr,output='sos'),x)
def bp(x,a,b,o=2): return sosfilt(butter(o,[a,b],'band',fs=sr,output='sos'),x)
def midi(m): return 440*2**((m-69)/12)
def saw(f,tt,det=0.0): 
    ph=(f*(1+det))*tt; return 2*(ph-np.floor(ph+.5))
# progressão Gm - Eb - Bb - F (1 compasso cada)
prog=[[55,58,62],[51,55,58],[46,50,53],[53,57,60]]  # tríades (MIDI)
roots=[43,39,46,41]
# intensidade ao longo do vídeo (0..1): intro calma, corpo, respiros, final
def env_at(x):
    pts=[(0,.35),(T["c0"]-1,.55),(T["c0"],.8),(T["s1"]-1,.8),(T["s1"],.95),(T["d0"]-.5,.95),(T["d0"],.75),(T["f1"],.9),(T["out"]+.6,1.0),(END-2.2,.9),(END,0)]
    xs,ys=zip(*pts); return np.interp(x,xs,ys)
I=env_at(t)
out=np.zeros(N); drums=np.zeros(N)
nb=int(END/bar)+1
# pad (serras desafinadas, filtradas)
pad=np.zeros(N)
for b in range(nb):
    a=int(b*bar*sr); z=min(N,int((b*bar+bar+1.2)*sr))
    if a>=N: break
    tt=t[a:z]-b*bar; e=np.clip(tt/0.9,0,1)*np.clip((bar+1.2-tt)/1.2,0,1)
    for m in prog[b%4]:
        f=midi(m); pad[a:z]+=e*(saw(f,tt,-.004)+saw(f,tt,.004)+.5*np.sin(2*np.pi*f/2*tt))
pad=lp(pad,1400,2)*0.05
# baixo pulsante em colcheias
bass=np.zeros(N); step=beat/2
for i in range(int(END/step)+1):
    a=int(i*step*sr); z=min(N,a+int(step*sr))
    if a>=N: break
    tt=t[a:z]-i*step; f=midi(roots[int(i*step/bar)%4])
    e=np.exp(-tt*9)*(1-np.exp(-tt*400))
    bass[a:z]+=e*(np.sin(2*np.pi*f*tt)+.35*saw(f,tt))
bass=lp(bass,420,2)*0.22
# arpejo (pluck) em semicolcheias, com eco
arp=np.zeros(N); st=beat/4; pat=[0,1,2,1,2,0,2,1]
for i in range(int(END/st)+1):
    a=int(i*st*sr); z=min(N,a+int(.35*sr))
    if a>=N: break
    tt=t[a:z]-i*st; ch=prog[int(i*st/bar)%4]; m=ch[pat[i%8]]+12
    f=midi(m); arp[a:z]+=np.exp(-tt*14)*(np.sin(2*np.pi*f*tt)+.25*np.sin(2*np.pi*2*f*tt))*(0.7 if i%2 else 1)
d=int(beat*.75*sr); echo=arp.copy()
for k in range(1,4): echo[d*k:]+=arp[:-d*k]*(.38**k)
arp=hp(lp(echo,3200),300)*0.045
# bateria: kick, clap suave, hi-hat
kick=np.zeros(N); kl=int(.45*sr); kt=np.arange(kl)/sr
ks=np.sin(2*np.pi*np.cumsum(45+95*np.exp(-kt*28))/sr)*np.exp(-kt*7)
hat=np.zeros(N); hl=int(.06*sr); hs=hp(rng.standard_normal(hl),7000)*np.exp(-np.arange(hl)/sr*70)
clap=np.zeros(N); cl=int(.25*sr); cs=bp(rng.standard_normal(cl),900,2500)*np.exp(-np.arange(cl)/sr*18)
side=np.ones(N)
for i in range(int(END/beat)+1):
    a=int(i*beat*sr)
    if a>=N: break
    z=min(N,a+kl); kick[a:z]+=ks[:z-a]
    sl=min(N,a+int(beat*sr)); tt=np.arange(sl-a)/sr; side[a:sl]=np.minimum(side[a:sl],1-.55*np.exp(-tt*9))
    if i%4 in (1,3):
        z=min(N,a+cl); clap[a:z]+=cs[:z-a]
    for off in (.5,):
        h=int((i+off)*beat*sr)
        if h<N: z=min(N,h+hl); hat[h:z]+=hs[:z-h]
# bateria entra depois da abertura e sai no encerramento
dm=np.clip((t-(T["c0"]-1.2))/1.5,0,1)*np.clip((END-2.4-t)/0.8,0,1)
drums=(kick*0.30+clap*0.05+hat*0.035)*dm
# whooshes nas trocas de cena
wh=np.zeros(N)
for tc in [T["c0"]-1.0,T["s1"]-.6,T["out"]+.6]:
    L=1.4; a=int((tc-L+.3)*sr); z=a+int(L*sr); n=rng.standard_normal(z-a); x=np.linspace(0,1,z-a)
    e=x**2*np.exp(-(1-x)*0)*(1-np.clip((x-.85)/.15,0,1))
    wh[a:z]+=bp(n,300,6000)*e*0.06
# impacto final (sub + ruído)
a=int((T["out"]+.6)*sr); L=int(2.5*sr); tt=np.arange(L)/sr
imp=np.sin(2*np.pi*np.cumsum(38+60*np.exp(-tt*10))/sr)*np.exp(-tt*2.2)*0.35
wh[a:a+L]+=imp[:max(0,min(L,N-a))]
mus=(pad+bass*side+arp*(.6+.4*side))*I+drums+wh
# reverb curto (ruído decaindo) para dar espaço
ir=rng.standard_normal(int(1.2*sr))*np.exp(-np.arange(int(1.2*sr))/sr*4); ir/=np.abs(ir).sum()/6
mus=mus+0.25*fftconvolve(mus,ir)[:N]
mus*=np.clip(t/1.0,0,1)*np.clip((END-t)/1.8,0,1)
mus=np.tanh(mus*1.6)/1.6
mus=mus/np.max(np.abs(mus))*0.9
sf.write("v8/trilha.wav",mus.astype(np.float32),sr)
print("ok",END)
