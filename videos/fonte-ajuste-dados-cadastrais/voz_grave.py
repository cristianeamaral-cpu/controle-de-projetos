# Ajuste fino da voz aprovada: 5% mais lenta, tom ~1,4 semitom mais grave e mais corpo nos graves.
# Lê audio_aprovado/*.wav e grava audio/*.wav; mantém o voStart de cada cena e atualiza a duração.
import json, subprocess, soundfile as sf
TOM, LENTO = 0.92, 0.95          # asetrate abaixa tom e timbre; atempo compensa para ficar só 5% mais lento
TL = json.load(open('timeline.json', encoding='utf-8'))
for i, c in enumerate(TL):
    af = (f"asetrate={int(48000*TOM)},aresample=48000,atempo={LENTO/TOM:.4f},"
          "bass=g=2.5:f=140:w=0.8,equalizer=f=3200:t=q:w=1.2:g=1.2")
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f"audio_aprovado/{c['id']}.wav", '-af', af, '-ar', '48000', f"audio/{c['id']}.wav"], check=True)
    a = sf.info(f"audio/{c['id']}.wav").duration; c['audio'] = round(a, 2)
    prox = TL[i + 1]['start'] if i + 1 < len(TL) else json.load(open('cortes.json'))['total'] - 2.5
    print(f"{c['id']:9} voz {c['voStart']:6.2f}-{c['voStart'] + a:6.2f}  (próxima {prox:.2f})", '' if c['voStart'] + a <= prox + 0.7 else '  << NÃO CABE')
json.dump(TL, open('timeline.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
