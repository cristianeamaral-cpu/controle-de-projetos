# uso: python mix.py saida.mp4
# junta vídeo sem travadas + narração + trilha (sidechain) → MP4 final
import sys, json, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
TL = json.load(open('timeline.json', encoding='utf-8'))
OUT = sys.argv[1] if len(sys.argv) > 1 else 'video_final.mp4'
TOTAL = json.load(open('cortes.json'))['total']

ins = ['-i', 'video_mudo.mp4', '-i', 'trilha.wav']
filt = []
for i, c in enumerate(TL):
    ins += ['-i', f"audio/{c['id']}.wav"]
    ms = int(c['voStart'] * 1000)
    filt.append(f"[{i + 2}:a]aresample=48000,pan=stereo|c0=c0|c1=c0,adelay={ms}|{ms}[a{i}]")
n = len(TL)
mix = (';'.join(filt) + ';' + ''.join(f'[a{i}]' for i in range(n)) +
       f'amix=inputs={n}:normalize=0,highpass=f=70,acompressor=threshold=0.15:ratio=2.5:attack=5:release=120,apad,asplit[vo][sc];'
       '[1:a]volume=0.42[mu];[mu][sc]sidechaincompress=threshold=0.03:ratio=8:attack=15:release=400[mud];'
       '[vo][mud]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.2,aresample=48000[a]')
subprocess.run([FF, '-y', '-hide_banner', '-loglevel', 'error', *ins, '-filter_complex', mix,
                '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                '-t', str(TOTAL), '-movflags', '+faststart', OUT], check=True)
print(OUT)
