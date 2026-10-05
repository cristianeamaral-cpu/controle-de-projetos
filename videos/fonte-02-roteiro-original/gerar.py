# Narração com o TEXTO ORIGINAL do vídeo 02, cada frase no mesmo momento do original.
# Mesma voz da versão anterior: Piper pt_BR-faber + 5% mais lenta + tom mais grave (voz_grave).
# Segue a lógica do tts.py do kit: se a fala não couber, acelera aos poucos (até +22%).
import json, os, subprocess, sys, numpy as np, soundfile as sf, librosa
ns={}; exec(open('tts_piper.py').read().split('TOTAL=')[0], ns); tts=ns['tts']
FALA=dict(ns['FALA']); FALA.update({'login':'lóguin','WhatsApp':'Uatsápi','Prossiga com':'Pro ssiga com'})
TOTAL=json.load(open('cortes.json'))['total']; os.makedirs('audio',exist_ok=True); os.makedirs('bruto',exist_ok=True)
cenas=json.load(open('roteiro.json',encoding='utf-8')); so=sys.argv[1:]
def fala(t):
    for a,b in FALA.items(): t=t.replace(a,b)
    return t
def syn(t,sp):
    g=tts.generate(fala(t),sid=0,speed=sp); y=librosa.resample(np.array(g.samples),orig_sr=g.sample_rate,target_sr=48000)
    i=np.where(np.abs(y)>0.006)[0]; return y[i[0]:i[-1]+int(.03*48000)]
def bruto(c,sp):
    if c['id']=='redes':      # LinkedIn com tônica na 1ª sílaba: emenda na pausa da vírgula
        a=syn('Na seção Redes Sociais, inclua os links do Instagram, Facebook,',sp)
        b=syn('i LinkedIn, e o vídeo em destaque do YouTube.',sp)
        a[-960:]*=np.linspace(1,0,960); return np.concatenate([a,np.zeros(int(.12*48000)),b])
    return syn(c['vo'],sp)
def grave(id):
    af="asetrate=44160,aresample=48000,atempo=1.0326,bass=g=2.5:f=140:w=0.8,equalizer=f=3200:t=q:w=1.2:g=1.2"
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',f'bruto/{id}.wav','-af',af,'-ar','48000',f'audio/{id}.wav'],check=True)
    return sf.info(f'audio/{id}.wav').duration
fim=0.0
for i,c in enumerate(cenas):
    prox=cenas[i+1]['start'] if i+1<len(cenas) else TOTAL-2.5
    ini=max(c['start']+0.25,fim+0.1)
    if so and c['id'] not in so and os.path.exists(f"audio/{c['id']}.wav"):
        a=sf.info(f"audio/{c['id']}.wav").duration; sp=1+c.get('rate',0)/100
    else:
        sp=1.0
        while True:
            sf.write(f"bruto/{c['id']}.wav",bruto(c,sp),48000); a=grave(c['id'])
            if ini+a<=prox+0.7 or sp>=1.22: break
            sp+=0.03
    c['voStart'],c['audio'],c['rate']=round(ini,2),round(a,2),round((sp-1)*100)
    fim=ini+a; c['dur']=round((prox if i+1<len(cenas) else TOTAL)-c['start'],2)
    print(f"{c['id']:10} voz {ini:6.2f}-{ini+a:6.2f}  vel {c['rate']:+d}%  (próxima {prox:.2f})")
json.dump(cenas,open('timeline.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
