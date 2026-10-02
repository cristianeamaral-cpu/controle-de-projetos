# Mixagem no padrão do kit (render.mjs): narração no voStart de cada cena, highpass 90 Hz, compressor,
# volume 2.2, trilha a 0.55 com ducking (sidechain) e loudnorm -14 LUFS.  Gera mix.wav.
import json, os, subprocess
TL = json.load(open('timeline.json')); sc = TL['scenes']
aud = lambda i: f"kit/audio/{i}.mp3" if TL.get('voz') == 'kit' else f"audio/{i}.wav"
ins, f = [], []
for i, c in enumerate(sc):
    ins += ['-i', aud(c['id'])]; ms = round(c['voStart'] * 1000)
    f.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[a{i}]")
ins += ['-i', 'trilha.wav']; m = len(sc)
mix = ';'.join(f) + ';' + ''.join(f'[a{i}]' for i in range(m)) + f"amix=inputs={m}:normalize=0,apad=whole_dur={TL['total']+0.6}" \
    ",highpass=f=90,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,volume=2.2,asplit=2[vo][sc];" \
    f"[{m}:a]volume=0.55[mu];[mu][sc]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=350[mud];" \
    "[vo][mud]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.2,aresample=48000[a]"
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', *ins, '-filter_complex', mix, '-map', '[a]', '-t', str(TL['total']+0.6), 'mix.wav'], check=True)
print('mix.wav ok')
