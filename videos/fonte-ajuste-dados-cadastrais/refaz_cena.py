# refaz só uma cena (mesmo voStart), mantendo as outras falas: python refaz_cena.py <id>
import sys, json, numpy as np, soundfile as sf, librosa
ns={}; exec(open('tts_piper.py').read().split('TOTAL=')[0], ns)
TL=json.load(open('timeline.json',encoding='utf-8')); c=[x for x in TL if x['id']==sys.argv[1]][0]
t=c['vo']
for a,b in ns['FALA'].items(): t=t.replace(a,b)
g=ns['tts'].generate(t,sid=0,speed=1.0); s=librosa.resample(np.array(g.samples),orig_sr=g.sample_rate,target_sr=48000)
idx=np.where(np.abs(s)>0.006)[0]; s=s[idx[0]:idx[-1]+int(.05*48000)]
sf.write(f"audio/{c['id']}.wav",s,48000); c['audio']=round(len(s)/48000,2)
json.dump(TL,open('timeline.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
