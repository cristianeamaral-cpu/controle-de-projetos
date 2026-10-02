# Mesma lógica do tts.py (encaixe nos cortes, acelera se não couber), com voz offline Kokoro pm_alex.
# Provisório enquanto speech.platform.bing.com (AntonioNeural) está bloqueado neste ambiente.
import json, os, sys, numpy as np, soundfile as sf, subprocess
S='/tmp/claude-0/-home-user-controle-de-projetos/a7e4ab82-d7ae-55cd-9826-274306ef78e0/scratchpad/'
sys.path.insert(0,S); import psa_fix
from kokoro_onnx import Kokoro
k=Kokoro(S+'voices/kokoro-v1.0.onnx',S+'voices/voices-v1.0.bin')
FALA={'PSA':'pê, ésse, á','login':'lóguin','Google':'gúgou','LinkedIn':'Linquedín','WhatsApp':'uótsapi','YouTube':'iutúbi','Facebook':'Feicebúqui',
      'CPF':'cê pê éfe','RG':'érre gê'}
TOTAL=json.load(open('cortes.json'))['total']; os.makedirs('audio',exist_ok=True)
cenas=json.load(open('roteiro.json',encoding='utf-8'))
def gera(c,sp):
    t=c['vo']
    for a,b in FALA.items(): t=t.replace(a,b)
    s,sr=psa_fix.create(k,t,voice='pm_alex',speed=sp)
    idx=np.where(np.abs(s)>0.006)[0]; s=s[idx[0]:idx[-1]+int(.05*sr)]
    sf.write(f"audio/{c['id']}.wav",s,sr); return len(s)/sr
fim=0.0
for i,c in enumerate(cenas):
    prox=cenas[i+1]['start'] if i+1<len(cenas) else TOTAL-2.5
    sp=1.10
    while True:
        a=gera(c,sp); ini=max(c['start']+0.25,fim+0.1)
        if ini+a<=prox+0.7 or sp>=1.22: break
        sp+=0.03
    c['voStart'],c['audio'],c['rate']=round(ini,2),round(a,2),round((sp-1)*100)
    fim=ini+a; c['dur']=round((prox if i+1<len(cenas) else TOTAL)-c['start'],2)
    print(f"{c['id']:9} cena {c['start']:6.2f}  voz {ini:6.2f}-{ini+a:6.2f}  vel +{c['rate']}%  (próxima {prox:.2f})")
json.dump(cenas,open('timeline.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
