"""Gera a locução (Piper, local) frase a frase e grava cues.js com o tempo de cada frase.

uso: python narrar.py <piper-bin> <modelo.onnx>
"""
import json, re, subprocess, sys, wave
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "narracao"
GAP = 0.35  # pausa entre frases (s)

piper, model = sys.argv[1], sys.argv[2]
cues = {}
for line in (OUT / "roteiro.tsv").read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    sid, text = line.split("\t", 1)
    sentences = [s for s in re.split(r"(?<=[.?!])\s+", text.strip()) if s]
    frames, rate, params, starts, durs, t = [], None, None, [], [], 0.0
    for i, sent in enumerate(sentences):
        part = OUT / f"{sid}_{i}.wav"
        subprocess.run([piper, "-m", model, "--length-scale", "0.95", "-f", str(part)],
                       input=sent.encode(), check=True, stderr=subprocess.DEVNULL)
        with wave.open(str(part)) as w:
            params, rate = w.getparams(), w.getframerate()
            data = w.readframes(w.getnframes())
        if i:
            frames.append(b"\0" * int(GAP * rate) * params.sampwidth)
            t += GAP
        starts.append(round(t, 3))
        d = len(data) / (rate * params.sampwidth)
        durs.append(round(d, 3))
        frames.append(data)
        t += d
        part.unlink()
    with wave.open(str(OUT / f"{sid}.wav"), "wb") as w:
        w.setparams(params)
        w.writeframes(b"".join(frames))
    cues[sid] = {"dur": round(t, 3), "starts": starts, "durs": durs}
    print(sid, round(t, 2), len(sentences))

(HERE / "cues.js").write_text("window.NARR = " + json.dumps(cues) + ";\n", encoding="utf-8")
