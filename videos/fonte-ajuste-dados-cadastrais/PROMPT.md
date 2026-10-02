# Ajuste de vídeo PSA: tirar travadas, narração nova em PT-BR, trilha e mixagem

Abra esta pasta (`psa-video-ajuste-kit`) como diretório de trabalho no Claude Code e cole o texto abaixo, trocando o caminho do vídeo.

---

Quero ajustar o vídeo `C:/CAMINHO/DO/MEU/video.mp4` do mesmo jeito que foi feito no vídeo "Visão geral do Ecossistema PSA". Nesta pasta estão os scripts usados nele. Leia todos antes de começar e use-os, sem reescrever do zero.

## O que fazer

1. **Instalar o que falta:** `pip install edge-tts imageio-ffmpeg numpy faster-whisper`.
2. **Tirar as travadas:** `python analisa.py "<vídeo>"`. O script remove os quadros congelados no meio de movimento, grava o `video_mudo.mp4` e o `cortes.json` (duração e cortes candidatos) e gera a `folha.jpg`, com um quadro a cada 2 segundos.
3. **Ler o vídeo:** abra a `folha.jpg` e confira os cortes. A detecção não pega transições com fade, então acerte os tempos olhando os quadros. Rode `python transcreve.py "<vídeo>"` para ler a narração original.
4. **Roteiro:** monte o `roteiro.json` no formato do `roteiro_exemplo.json`, com uma entrada por cena: `id`, `start` (início da cena no `video_mudo.mp4`) e `vo` (a fala). Marque `"drop": true` na cena em que a música deve "explodir", que costuma ser a cena da revelação. **Me mostre o roteiro e espere eu aprovar.**
5. **Narração:** `python tts.py`. A voz é `pt-BR-AntonioNeural` a +10%, e o script acelera sozinho se a fala não couber na cena. Se alguma cena passar de +15%, encurte a frase em vez de acelerar.
6. **Conferir a pronúncia:** `python transcreve.py audio/*.wav`. Se o transcritor entender uma palavra errada, ela provavelmente está soando estranha. Troque a palavra ou escreva do jeito que se fala, e gere a narração de novo.
7. **Trilha:** `python trilha.py` gera uma música original sintetizada, sem direitos de terceiros.
8. **Mixagem:** `python mix.py "<saída>.mp4"`. A música abaixa quando a voz entra, e o áudio sai normalizado em -14 LUFS.

## Regras da narração (aprendidas no vídeo do Ecossistema)

- 100% português do Brasil, com frases curtas e faladas.
- Evite palavras que a voz lê como inglês: **"complete"** (use "preencha"), **"Candidate-se"** (use "Inscreva-se"), **"login"** (use "entre com").
- Palavras que saíram erradas e foram corrigidas: "bio" (use "biografia") e "liberado" logo no começo da frase (use "O seu acesso foi liberado").
- "PSA Trends" só sai certo escrito "PSA Trêndis". "IA" é lida como "inteligência artificial", o que está ok.
- Números por extenso na fala ("cem por cento").
- Não use travessão (—) nos textos.

## Entrega

Diga onde ficou o MP4, quanto ele dura, quantos quadros congelados foram removidos e se alguma tela do vídeo tem problema que não dá para corrigir sem regravar (por exemplo, uma tela que aparece sem carregar).
