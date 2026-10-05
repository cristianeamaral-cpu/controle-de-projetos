# Mesma lógica do tts.py do kit (encaixe nos cortes, acelera se não couber), com voz brasileira
# Piper pt_BR-faber-medium (offline, falante nativo). Provisório enquanto a AntonioNeural está bloqueada.
import json, os, numpy as np, soundfile as sf, sherpa_onnx, librosa
d='/tmp/claude-0/-home-user-controle-de-projetos/a7e4ab82-d7ae-55cd-9826-274306ef78e0/scratchpad/voices/vits-piper-pt_BR-faber-medium/'
tts=sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
    vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=d+'pt_BR-faber-medium.onnx',tokens=d+'tokens.txt',data_dir=d+'espeak-ng-data'),num_threads=4)))
# grafias só de pronúncia (o texto falado é o do roteiro)
FALA={'LinkedIn':'Línquedim','Instagram':'Instagrã','YouTube':'Iutúbi','cachês':'kachês','biografia,':'bio grafia,','Ecossistema PSA.':'Ecossistema PSA!','Calma.':'Calma!','Gerar com IA':'Gerár com IA','É essa imagem':'É exatamente essa imagem'}
TOTAL=json.load(open('cortes.json'))['total']; os.makedirs('audio',exist_ok=True)
cenas=json.load(open('roteiro.json',encoding='utf-8'))
def gera(c,sp):
    t=c['vo']
    for a,b in FALA.items(): t=t.replace(a,b)
    g=tts.generate(t,sid=0,speed=sp); s=librosa.resample(np.array(g.samples),orig_sr=g.sample_rate,target_sr=48000); sr=48000
    idx=np.where(np.abs(s)>0.006)[0]; s=s[idx[0]:idx[-1]+int(.05*sr)]
    sf.write(f"audio/{c['id']}.wav",s,sr); return len(s)/sr
fim=0.0
for i,c in enumerate(cenas):
    prox=cenas[i+1]['start'] if i+1<len(cenas) else TOTAL-2.5
    sp=1.00   # fala mais pausada, melhor dicção
    while True:
        a=gera(c,sp); ini=max(c['start']+0.25,fim+0.1)
        if ini+a<=prox+0.7 or sp>=1.22: break
        sp+=0.03
    c['voStart'],c['audio'],c['rate']=round(ini,2),round(a,2),round((sp-1)*100)
    fim=ini+a; c['dur']=round((prox if i+1<len(cenas) else TOTAL)-c['start'],2)
    print(f"{c['id']:9} cena {c['start']:6.2f}  voz {ini:6.2f}-{ini+a:6.2f}  vel +{c['rate']}%  (próxima {prox:.2f})")
json.dump(cenas,open('timeline.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
