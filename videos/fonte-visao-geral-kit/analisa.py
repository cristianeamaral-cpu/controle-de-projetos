# uso: python analisa.py "C:/caminho/video.mp4"
# 1) remove quadros congelados no meio de movimento (as "travadinhas")
# 2) grava video_mudo.mp4 (sem áudio)
# 3) acha os cortes de cena e grava cortes.json + folha.jpg (um quadro a cada 2 s, para conferir)
import sys, json, subprocess, numpy as np, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
SRC = sys.argv[1]

raw = subprocess.run([FF, '-loglevel', 'error', '-i', SRC, '-vf', 'scale=320:180,format=gray',
                      '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
v = np.frombuffer(raw, np.uint8).reshape(-1, 180, 320).astype(np.int16)
d = np.abs(np.diff(v, axis=0)).mean(axis=(1, 2))      # d[i] = diferença entre quadro i e i+1

drop = [i + 1 for i in range(1, len(d) - 1)
        if d[i] < 0.2 * min(d[i - 1], d[i + 1]) and min(d[i - 1], d[i + 1]) > 0.4 and max(d[i - 1], d[i + 1]) < 6]
print(f'quadros: {len(v)} · congelados removidos: {len(drop)}', drop)

vf = 'setpts=N/30/TB'
if drop:
    vf = "select='not(" + '+'.join(f'eq(n,{f})' for f in drop) + ")'," + vf
subprocess.run([FF, '-y', '-loglevel', 'error', '-i', SRC, '-an', '-vf', vf, '-r', '30', '-c:v', 'libx264',
                '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', 'video_mudo.mp4'], check=True)

# corte = salto grande de imagem; junta saltos próximos (flash/transição) num corte só
saltos = [i + 1 for i, x in enumerate(d) if x > 15]
cortes = [0]
for f in saltos:
    if f - cortes[-1] > 45: cortes.append(f)
novo = lambda f: f - sum(1 for x in drop if x < f)
total = round((len(v) - len(drop)) / 30, 2)
starts = [round(novo(f) / 30, 2) for f in cortes]
json.dump({'total': total, 'cortes': starts}, open('cortes.json', 'w'), indent=1)
print('duração final', total, 's · cortes candidatos (s), confira na folha.jpg:', starts)

subprocess.run([FF, '-y', '-loglevel', 'error', '-i', 'video_mudo.mp4', '-vf', 'fps=1/2,scale=480:-1,tile=6x5',
                '-frames:v', '1', 'folha.jpg'], check=True)
print('folha.jpg gerada')
