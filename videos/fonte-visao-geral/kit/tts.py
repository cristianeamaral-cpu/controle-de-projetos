# narração + tempos de cada palavra → timeline.json (start/dur de cada cena saem da fala)
import asyncio, json, subprocess, re, os
import edge_tts, imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
VOZ, RATE, PITCH = 'pt-BR-AntonioNeural', '+14%', '+2Hz'
os.makedirs('audio', exist_ok=True)
cenas = json.load(open('roteiro.json', encoding='utf-8-sig'))

def duracao(p):
    out = subprocess.run([FF, '-i', p], capture_output=True, text=True).stderr
    h, m, s = re.search(r'Duration: (\d+):(\d+):([\d.]+)', out).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)

async def main():
    t = 0.0
    for c in cenas:
        p = f"audio/{c['id']}.mp3"
        com = edge_tts.Communicate(c['vo'], VOZ, rate=RATE, pitch=PITCH, boundary='WordBoundary')
        ws = []
        with open(p, 'wb') as f:
            async for ch in com.stream():
                if ch['type'] == 'audio': f.write(ch['data'])
                elif ch['type'] == 'WordBoundary': ws.append((round(ch['offset'] / 1e7, 2), ch['text']))
        c['audio'] = round(duracao(p), 2)
        c['start'] = round(t, 2)
        c['dur'] = round(max(c['min'], c['audio'] + 0.55), 2)
        c['voStart'] = round(t + 0.15, 2)
        c['words'] = ws
        t += c['dur']
        print(f"{c['id']:9} start {c['start']:6.2f} dur {c['dur']:5.2f} audio {c['audio']:5.2f}  ", ' '.join(f'{a}:{w}' for a, w in ws))
    json.dump(cenas, open('timeline.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('total', round(t, 2))

asyncio.run(main())
