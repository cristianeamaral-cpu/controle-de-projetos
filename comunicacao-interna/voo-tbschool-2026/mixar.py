"""Junta o vídeo (sem áudio) com a locução de cada cena nos tempos de timeline.json.

uso: python mixar.py video_sem_audio.mp4 saida.mp4
"""
import json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).parent
src, out = sys.argv[1], sys.argv[2]
tl = json.loads((HERE / "timeline.json").read_text())

args, chains = ["ffmpeg", "-v", "error", "-y", "-i", src], []
for n, sc in enumerate(tl["scenes"], start=1):
    args += ["-i", str(HERE / "narracao" / f"{sc['id']}.wav")]
    ms = int(sc["start"] * 1000)
    chains.append(f"[{n}:a]aresample=48000,adelay={ms}|{ms}[a{n}]")
mix = "".join(f"[a{n}]" for n in range(1, len(tl["scenes"]) + 1))
chains.append(f"{mix}amix=inputs={len(tl['scenes'])}:normalize=0,"
              f"apad,atrim=0:{tl['duration']:.3f},loudnorm=I=-16:TP=-1.5:LRA=11[out]")
args += ["-filter_complex", ";".join(chains), "-map", "0:v", "-map", "[out]",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", out]
subprocess.run(args, check=True)
