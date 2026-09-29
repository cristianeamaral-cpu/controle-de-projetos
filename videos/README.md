# Vídeos tutoriais — Ecossistema PSA

| Vídeo | Duração | Conteúdo |
|-------|---------|----------|
| [`como-acessar-o-ecossistema-psa.mp4`](como-acessar-o-ecossistema-psa.mp4) | 52 s | Login no site (botão **Login** no canto superior direito), entrada por e-mail, Google ou LinkedIn, dica de LGPD (perfil único, sem logins secundários para assessores, assistentes etc.) e recomendação do Google Chrome. |

Formato: 1920×1080, 30 fps, H.264 + AAC. Mesma trilha de fundo do vídeo
"Minha conta e sincronização de agenda" (música separada da narração original).

## Como o vídeo foi gerado (`fonte/`)

1. **Telas:** `video.html` contém todas as cenas animadas (as legendas estão ocultas pela regra `.cap{display:none}`; remova-a para exibi-las); a função
   `seek(t)` posiciona a animação no segundo `t`.
2. **Quadros:** `node render.js full 52.5` (Playwright) grava `frames/f00000.jpg…` a 30 fps.
   `node render.js test 3,15,27` salva quadros avulsos para conferência.
3. **Narração:** `narracao.py` gera cada frase com o TTS offline Kokoro (voz `pf_dora`).
   As frases usam grafia fonética (ex.: "gúgou Crôume", "éle gê pê dê") para a pronúncia sair correta.
4. **Trilha:** música de fundo extraída do vídeo de referência com `audio-separator`
   (modelo UVR-MDX-NET-Inst_HQ_3), mixada com a narração no ffmpeg.

Para os próximos vídeos da série, basta trocar as cenas em `video.html`, as frases em
`narracao.py` e os tempos de início de cada frase.
