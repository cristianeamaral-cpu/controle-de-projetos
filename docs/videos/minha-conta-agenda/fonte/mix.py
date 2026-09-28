import json,numpy as np,soundfile as sf,re
tl=json.load(open("v2/tl.json"));T,D,END=tl["T"],tl["D"],tl["END"]
sr=24000;N=int(END*sr)+sr
voice=np.zeros(N)
for k,t in T.items():
    s,_=sf.read(f"v2/audio/{k}.wav"); i=int(t*sr); voice[i:i+len(s)]+=s
voice=voice/np.max(np.abs(voice))*0.89
# soft ambient pad (Cmaj7 -> Am7 -> Fmaj7 -> G), very quiet
t=np.arange(N)/sr
chords=[[261.63,329.63,392.0,493.88],[220.0,261.63,329.63,392.0],[174.61,220.0,261.63,329.63],[196.0,246.94,293.66,392.0]]
pad=np.zeros(N);L=8.0
for ci in range(int(END/L)+2):
    a=int(ci*L*sr);b=min(N,int((ci*L+L+2)*sr))
    if a>=N:break
    tt=t[a:b]-ci*L; env=np.clip(tt/2.5,0,1)*np.clip((L+2-tt)/2.5,0,1)
    for f in chords[ci%4]:
        pad[a:b]+=env*(np.sin(2*np.pi*f*tt)+.3*np.sin(2*np.pi*f*2*tt+.5))*(0.9+0.1*np.sin(2*np.pi*.2*tt))
pad=pad/np.max(np.abs(pad))
# duck under voice
envv=np.convolve(np.abs(voice),np.ones(4800)/4800,'same'); duck=np.where(envv>0.01,0.045,0.08)
duck=np.convolve(duck,np.ones(12000)/12000,'same')
fade=np.clip(t/1.5,0,1)*np.clip((END-t)/2.5,0,1)
mix=voice+pad*duck*fade
sf.write("v2/mix.wav",mix[:int(END*sr)],sr)
sf.write("v2/trilha.wav",(pad*0.08*fade)[:int(END*sr)],sr)
def ts(x): h=int(x//3600);m=int(x%3600//60);s=x%60; return f"{h:02}:{m:02}:{int(s):02},{int(round((s%1)*1000)):03}"
caps=re.findall(r'^ (\w+):"(.*)",?$',open("v2/video.html").read().split('const CAPS')[1],re.M)
with open("v2/legendas.srt","w") as f:
    for n,(k,c) in enumerate(caps,1):
        c=re.sub('<br>','\n',re.sub('</?b>','',c))
        f.write(f"{n}\n{ts(T[k])} --> {ts(T[k]+D[k]+.1)}\n{c}\n\n")
print(len(caps))
