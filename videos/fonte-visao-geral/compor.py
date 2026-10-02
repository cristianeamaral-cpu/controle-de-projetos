import json,subprocess
U='/root/.claude/uploads/a7e4ab82-d7ae-55cd-9826-274306ef78e0/'; R='/home/user/controle-de-projetos/videos/'
F={'v01':U+'918b48d4-01_Como_Acessar_Plataforma_FazerLogin.mp4','v02':U+'d6710fac-02_Preenchimento_Dados_Cadastrais.mp4',
   'tem':R+'temas-e-macro-temas.mp4','cac':R+'cache-formatos-e-complexidade.mp4','opo':R+'oportunidades-e-crm.mp4','ast':R+'assistentes-virtuais.mp4','tre':R+'psa-trends-e-psa-play.mp4'}
TL=json.load(open('timeline.json')); S={s['id']:s for s in TL['scenes']}
plan={'p1':[('v01',15.5),('v01',19.5)],'p2':[('v02',89.4)],'p3':[('tem',10.5),('cac',11.5)],'p4':[('opo',10.0),('opo',51.0)],'p5':[('ast',7.5),('tre',13.0)]}
ins=['-framerate','30','-i','build/frames/f%05d.jpg','-i','mix.wav']; fc=[]; last='0:v'; k=2
for sid,parts in plan.items():
    s=S[sid]; n=len(parts); seg=(s['dur']-0.15)/n
    for j,(src,ss) in enumerate(parts):
        t0=s['start']+0.12+j*seg; ln=seg+(0.03 if j<n-1 else 0)
        ins+=['-ss',str(ss),'-t',f'{ln:.3f}','-i',F[src]]
        fl=f"[{k}:v]scale=960:540,format=yuva420p,setpts=PTS-STARTPTS+{t0:.3f}/TB"
        if j==0: fl+=f",fade=t=in:st={t0:.3f}:d=0.25:alpha=1"
        if j==n-1: fl+=f",fade=t=out:st={t0+ln-0.2:.3f}:d=0.2:alpha=1"
        fc.append(fl+f"[c{k}]"); fc.append(f"[{last}][c{k}]overlay=840:270:eof_action=pass[o{k}]"); last=f"o{k}"; k+=1
subprocess.run(['ffmpeg','-loglevel','error','-y']+ins+['-filter_complex',";".join(fc),'-map',f'[{last}]','-map','1:a','-c:v','libx264','-preset','slow','-b:v','2800k','-maxrate','3400k','-bufsize','7M','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',R+'visao-geral-ecossistema-psa.mp4'],check=True)
print('ok')
