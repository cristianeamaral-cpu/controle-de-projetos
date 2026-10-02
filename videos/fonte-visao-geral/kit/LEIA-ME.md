# Narração do kit (voz pt-BR-AntonioNeural) — vídeo "Visão geral do Ecossistema PSA"

O `tts.py` é o do kit, sem alterações: voz **pt-BR-AntonioNeural**, rate **+14%**, pitch **+2Hz** e tempos por palavra (WordBoundary).
O `roteiro.json` traz o texto do vídeo de visão geral no mesmo formato do kit (`id`, `min`, `vo`).

## No seu PC (dentro de `C:\Users\Usuario\psa-video-kit` ou de uma cópia desta pasta)
1. `pip install edge-tts imageio-ffmpeg`
2. Copie este `roteiro.json` para a pasta e rode `python tts.py`.
3. O script gera a pasta `audio\` (gancho.mp3 … fecha.mp3) e o arquivo `timeline.json`.
4. Envie a pasta `audio\` e o `timeline.json` aqui na conversa.

## Depois (feito aqui)
1. Coloque `audio/` e `timeline.json` nesta pasta `kit/`.
2. `python kit/importar.py` converte para `../timeline.json` com os tempos reais das palavras.
3. `python trilha.py` gera a trilha com o drop em "revela".
4. `python build.py` sincroniza as animações pelas palavras.
5. `node render.js video <total>` renderiza os quadros.
6. `python mixar.py` faz a mixagem no padrão do `render.mjs`: highpass 90, compressor, volume 2.2, trilha 0.55 com ducking e -14 LUFS.
7. `python compor.py` aplica os trechos dos tutoriais e gera o MP4 final.
