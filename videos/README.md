# Vídeos tutoriais — Ecossistema PSA

| Vídeo | Duração | Conteúdo |
|-------|---------|----------|
| [`oportunidades-e-crm.mp4`](oportunidades-e-crm.mp4) | 1 min 4 s | **Oportunidades de Palestras** (mural, Candidatar com justificativa, curadoria PSA e negociação direta; abas Abertas, Encerradas e Participando) e **CRM PSA** (Nova Demanda visível só para você; etiqueta "Demanda PSA" nas negociações da plataforma). Telas baseadas nos prints. Fontes em [`fonte-oportunidades-crm/`](fonte-oportunidades-crm/). |
| [`modulos-complementares.mp4`](modulos-complementares.mp4) | 1 min 7 s | Módulos complementares: **Eventos** (QR Code exclusivo, avaliação da palestra, certificado na hora e download para divulgação), **Depoimentos** (publicados só após aprovação manual), **Biblioteca** (publicações com links para Amazon ou loja própria) e **Informações para Curso** (logística interna de uso exclusivo da equipe PSA). Fontes em [`fonte-modulos/`](fonte-modulos/). |
| [`cache-formatos-e-complexidade.mp4`](cache-formatos-e-complexidade.mp4) | 40 s | Aba **Cachês e Formatos** (Caches): seleção do **Formato** (Palestra, Palestra online, Treinamento, Mentoria, Treinamento online, Mentoria online, Mestre de Cerimônias); três níveis de complexidade (**Baixa, Média e Alta**) conforme o deslocamento exigido; campo **Valor** com o valor líquido exato a receber; a plataforma apresenta a informação ao contratante na negociação; encerramento "Defina sua precificação com estratégia e garanta que seu perfil esteja pronto para as melhores oportunidades". Tela baseada no print da plataforma. Fontes em [`fonte-cache/`](fonte-cache/). |
| [`temas-e-macro-temas.mp4`](temas-e-macro-temas.mp4) | 48 s | Aba **Temas**: múltiplos Macro Temas (até 6) ampliam as oportunidades de candidatura e os insights no **PSA Trends**; regra de **exatamente 1 Tema Principal** (maior bandeira e principal posicionamento); Salvar; algoritmo cruza os dados com os briefings dos clientes. Narração em ritmo moderado (velocidade 1,04, pausas internas de no máximo 0,18 s, sem ambiência). Fontes em [`fonte-temas/`](fonte-temas/). |
| [`meu-perfil-completo.mp4`](meu-perfil-completo.mp4) | 1 min 43 s | Aba **Meu Perfil**: Força da Página (meta 100%), foto de perfil (a mesma exibida no site para contratantes), Biografia Profissional com **Gerar com IA**, Frase de Destaque (30 a 60 caracteres), Dados Pessoais, Contato, Redes Sociais, Localização, Seu momento atual e Salvar alterações. Fontes em [`fonte-meu-perfil/`](fonte-meu-perfil/). |
| [`como-acessar-o-ecossistema-psa.mp4`](como-acessar-o-ecossistema-psa.mp4) | 52 s | Login no site (botão **Login** no canto superior direito), entrada por e-mail, Google ou LinkedIn, dica de LGPD (perfil único, sem logins secundários para assessores ou assistentes) e recomendação do Google Chrome. |

Formato: 1920×1080, 30 fps, H.264 + AAC. Mesma trilha de fundo do vídeo
"Minha conta e sincronização de agenda" (música separada da narração original).
Identidade visual igual à do vídeo "Minha Conta + Google Calendar": fundo azul-marinho
(`#05102B`) com constelação, títulos em Archivo Black condensada (branco e laranja `#F74E00`),
sobretítulo laranja espaçado, marcador de passos e textos da interface em Manrope (laranja `#FD6E06`).

## Padrão visual da série

Todos os vídeos seguem o vídeo de referência **"Minha Conta + Google Calendar"**:
fundo azul-marinho com constelação, títulos em Archivo Black condensada (branco + laranja `#F74E00`),
sobretítulo laranja espaçado, painel branco com faixa laranja, logo "PSA." no canto e textos da
interface em Manrope. Sem legendas. Trilha: a mesma música de fundo (repetida com transição suave
quando o vídeo passa de 68 s). Voz: Kokoro `pf_dora`, velocidade 0,98, pausas de respiração (0,55 s entre frases da mesma cena,
1,2 s entre cenas) e tratamento leve (EQ de presença, compressão suave e ambiência curta).

## Como o vídeo foi gerado (`fonte/`)

1. **Telas:** `video.src.html` é a fonte (o fundo de constelação fica em `stars.svg.html` e é inserido no lugar de `%%STARS%%` para gerar `video.html`);
   `video.html` contém todas as cenas animadas (as legendas estão ocultas pela regra `.cap{display:none}`; remova-a para exibi-las); a função
   `seek(t)` posiciona a animação no segundo `t`.
2. **Quadros:** `node render.js full 51.9` (Playwright) grava `frames/f00000.jpg…` a 30 fps.
   `node render.js test 3,15,27` salva quadros avulsos para conferência.
3. **Narração:** `narracao.py` gera cada frase com o TTS offline Kokoro (voz `pf_dora`).
   As frases usam grafia fonética (ex.: "gúgou Crôume", "éle gê pê dê") para a pronúncia sair correta.
4. **Trilha:** música de fundo extraída do vídeo de referência com `audio-separator`
   (modelo UVR-MDX-NET-Inst_HQ_3), mixada com a narração no ffmpeg.

Para os próximos vídeos da série, basta trocar as cenas em `video.html`, as frases em
`narracao.py` e os tempos de início de cada frase.
