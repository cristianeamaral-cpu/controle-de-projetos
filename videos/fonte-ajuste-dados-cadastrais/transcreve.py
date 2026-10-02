# uso: python transcreve.py arquivo1 [arquivo2 ...]   (vídeo ou áudio)
# serve para ler a narração do vídeo original e para conferir a pronúncia da narração nova
import sys, subprocess, numpy as np, imageio_ffmpeg
from faster_whisper import WhisperModel
FF = imageio_ffmpeg.get_ffmpeg_exe()
m = WhisperModel('medium', device='cpu', compute_type='int8')
for f in sys.argv[1:]:
    raw = subprocess.run([FF, '-loglevel', 'error', '-i', f, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                         capture_output=True).stdout
    a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    segs, _ = m.transcribe(a, language='pt', vad_filter=True)
    print(f'== {f}')
    for s in segs: print(f'{s.start:6.2f}-{s.end:6.2f} {s.text}')
