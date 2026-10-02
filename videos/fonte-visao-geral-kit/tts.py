# narração PT-BR (edge-tts) encaixada nos cortes do vídeo → timeline.json
import asyncio, os, json, subprocess, re
import edge_tts, imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
VOZ, RATE, PITCH = 'pt-BR-FranciscaNeural', '+10%', '+0Hz'
TOTAL = json.load(open('cortes.json'))['total']
os.makedirs('audio', exist_ok=True)
cenas = json.load(open('roteiro.json', encoding='utf-8'))

def duracao(p):
    out = subprocess.run([FF, '-i', p], capture_output=True, text=True).stderr
    h, m, s = re.search(r'Duration: (\d+):(\d+):([\d.]+)', out).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)

async def gera(c, rate):
    p = f"audio/{c['id']}.mp3"; w = f"audio/{c['id']}.wav"
    await edge_tts.Communicate(c['vo'], VOZ, rate=rate, pitch=PITCH).save(p)
    # corta o silêncio que o edge-tts deixa no começo e no fim
    tr = 'silenceremove=start_periods=1:start_threshold=-45dB'
    subprocess.run([FF, '-y', '-loglevel', 'error', '-i', p, '-af',
                    f'{tr},areverse,{tr},areverse,apad=pad_dur=0.05', '-ar', '48000', w], check=True)
    return duracao(w)

async def main():
    fim_anterior = 0.0
    for i, c in enumerate(cenas):
        prox = cenas[i + 1]['start'] if i + 1 < len(cenas) else TOTAL - 2.5
        rate = int(RATE[:-1])
        while True:
            a = await gera(c, f'{rate:+d}%')
            ini = max(c['start'] + 0.25, fim_anterior + 0.1)
            # pode invadir até 0,7 s da cena seguinte; senão acelera um pouco
            if ini + a <= prox + 0.7 or rate >= 22: break
            rate += 3
        c['voStart'], c['audio'], c['rate'] = round(ini, 2), round(a, 2), rate
        fim_anterior = ini + a
        c['dur'] = round(prox - c['start'], 2) if i + 1 < len(cenas) else round(TOTAL - c['start'], 2)
        print(f"{c['id']:7} cena {c['start']:6.2f}  voz {ini:6.2f}-{ini + a:6.2f}  rate {rate:+d}%  (próxima {prox:.2f})")
    json.dump(cenas, open('timeline.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

asyncio.run(main())
