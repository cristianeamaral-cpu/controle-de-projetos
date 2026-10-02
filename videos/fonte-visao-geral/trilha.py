# Trilha original sintetizada (numpy): 120 BPM, Lá menor (Am F C G). Tensão até o drop; groove depois.
import numpy as np, json, soundfile as sf
SR=48000; TL=json.load(open('v11/timeline.json')); T=TL['total']+0.6
DROP=[s for s in TL['scenes'] if s['id']=='revela'][0]['start']
CUTS=[s['start'] for s in TL['scenes']][1:]
N=int(T*SR); L=np.zeros(N); Rr=np.zeros(N); t=np.arange(N)/SR
BEAT=0.5; rng=np.random.default_rng(7)
def note(f): return 440*2**((f-69)/12)
def add(sig,start,pan=0.0,g=1.0):
    i=int(start*SR); j=min(N,i+len(sig)); 
    if i>=N or j<=0: return
    s=sig[:j-i]*g; L[i:j]+=s*(1-pan)/1.0*0.7; Rr[i:j]+=s*(1+pan)*0.7/1.0
def env(n,a=0.005,r=0.2):
    e=np.ones(n); na=max(1,int(a*SR)); e[:na]=np.linspace(0,1,na); x=np.arange(n)/SR; return e*np.exp(-x/r)
CH=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]  # Am F C G
BASS=[45,41,36,43]
# --- pad escuro (todo o vídeo, mais forte antes do drop)
for b in range(int(T/2)+1):
    c=CH[b%4]; st=b*2.0; n=int(2.1*SR); x=np.arange(n)/SR
    sig=sum(np.sin(2*np.pi*note(m-12)*x+0.3*np.sin(2*np.pi*0.3*x)) for m in c)/3
    sig*=np.minimum(1,x/0.4)*np.minimum(1,(2.1-x)/0.4)
    add(sig,st,0,0.20 if st<DROP else 0.10)
# --- antes do drop: tique-taque + batida de coração + riser
for k in range(int(DROP/BEAT)):
    st=k*BEAT; n=int(0.03*SR); x=np.arange(n)/SR
    add(np.sin(2*np.pi*(2400 if k%2 else 1800)*x)*env(n,0.001,0.008),st,(-.3 if k%2 else .3),0.12)
for k in range(int(DROP/1.0)):
    for d,g in [(0,1),(0.22,0.7)]:
        n=int(0.25*SR); x=np.arange(n)/SR; f=55*np.exp(-x*6)+38
        add(np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,0.002,0.09),k*1.0+d,0,0.55*g)
n=int(3.0*SR); x=np.arange(n)/SR; rs=rng.standard_normal(n)
rs=np.convolve(rs,np.ones(8)/8,'same')*(x/3.0)**2.2*0.35+np.sin(2*np.pi*(200+900*(x/3)**2)*x)*(x/3)**2*0.15
add(rs,DROP-3.0,0,1.0)
# --- impacto no drop
n=int(2.5*SR); x=np.arange(n)/SR
imp=np.sin(2*np.pi*np.cumsum(60*np.exp(-x*3)+35)/SR)*np.exp(-x*1.6)+rng.standard_normal(n)*np.exp(-x*7)*0.5
add(imp,DROP,0,0.9)
# --- groove depois do drop
FIM=TL['scenes'][-1]['start']+TL['scenes'][-1]['dur']-1.6
k=0; st=DROP
while st<FIM:
    bar=int((st-DROP)//2); c=CH[bar%4]; pos=k%4
    # kick
    n=int(0.3*SR); x=np.arange(n)/SR; add(np.sin(2*np.pi*np.cumsum(150*np.exp(-x*30)+45)/SR)*env(n,0.001,0.12),st,0,0.75)
    # clap nos tempos 2 e 4
    if pos in (1,3):
        n=int(0.2*SR); add(rng.standard_normal(n)*env(n,0.001,0.06),st,0,0.28)
    # hats em semicolcheias
    for q in range(4):
        n=int(0.04*SR); hh=rng.standard_normal(n); hh=hh-np.convolve(hh,np.ones(4)/4,'same')
        add(hh*env(n,0.0005,0.012),st+q*BEAT/4,(0.35 if q%2 else -0.35),0.10 if q%2 else 0.06)
    # baixo no contratempo
    n=int(0.22*SR); x=np.arange(n)/SR; bf=note(BASS[bar%4]); b=np.sign(np.sin(2*np.pi*bf*x))*0.5+np.sin(2*np.pi*bf*x)*0.5
    add(np.convolve(b,np.ones(20)/20,'same')*env(n,0.004,0.12),st+BEAT/2,0,0.30)
    # arpejo com eco
    for q in range(2):
        m=c[(k*2+q)%3]+12; n=int(0.18*SR); x=np.arange(n)/SR
        ar=(np.sin(2*np.pi*note(m)*x)+0.3*np.sin(2*np.pi*note(m)*2*x))*env(n,0.002,0.08)
        tt=st+q*BEAT/2
        for e,ge in [(0,0.12),(0.375,0.06),(0.75,0.03)]: add(ar,tt+e,(-.4 if e else .2),ge)
    st+=BEAT; k+=1
# --- whooshes nos cortes depois do drop
for c in CUTS:
    if c<=DROP+0.1: continue
    n=int(0.45*SR); x=np.arange(n)/SR; w=np.convolve(rng.standard_normal(n),np.ones(30)/30,'same')*np.sin(np.pi*x/0.45)**2
    add(w,c-0.3,0,0.5)
# --- acorde final grande
n=int(3.5*SR); x=np.arange(n)/SR
fin=sum(np.sin(2*np.pi*note(m)*x)+0.4*np.sin(2*np.pi*note(m-12)*x) for m in [57,60,64,69])/4*np.minimum(1,x/0.02)*np.exp(-x*0.9)
add(fin,FIM,0,0.55)
add(np.sin(2*np.pi*np.cumsum(60*np.exp(-x*3)+35)/SR)*np.exp(-x*1.8),FIM,0,0.6)
y=np.stack([L,Rr],1); y/=np.max(np.abs(y))+1e-9; y*=0.9
fo=int(0.8*SR); y[-fo:]*=np.linspace(1,0,fo)[:,None]
sf.write('v11/trilha.wav',y,SR); print('trilha',T,'drop',DROP)
