# FAQ — Ecossistema de Palestrantes PSA (pacote para o time de tech)

Conteúdo do FAQ convertido do documento original (Google Docs → PDF) para
formatos prontos para integrar na plataforma do Ecossistema de Palestrantes.

| Arquivo | Uso |
|---------|-----|
| `faq.json` | **Fonte da verdade.** Dados estruturados para alimentar o front/CMS/API. |
| `faq.md` | Versão legível (revisão de conteúdo, base de conhecimento, help center). |
| `faq.html` | Trecho HTML pronto para embutir (acordeão com `<details>`, sem dependências). |
| `faq-schema.jsonld` | Dados estruturados `FAQPage` (schema.org) para SEO. |
| `gerar.py` | Regera `faq.md`, `faq.html` e `faq-schema.jsonld` a partir do `faq.json`. |

## Estrutura do `faq.json`

```
secoes[]            id, ordem, titulo
  subsecoes[]       id, titulo (null quando a seção não tem abas)
    perguntas[]     id, pergunta, resposta
```

- `id`: slug estável e único — usar como âncora (`/faq#creditos-ia`) e chave
  de rastreamento/analytics. Não alterar depois de publicado.
- `resposta`: Markdown simples (`**negrito**`, `*itálico*`, `[link](url)`,
  listas `- ` e `1. `). Renderizar com qualquer parser Markdown, ou usar o
  HTML já gerado.

## Fluxo de atualização

1. Editar `faq.json` (incrementar `versao` e `atualizado_em`).
2. Rodar `python3 docs/faq-ecossistema-palestrantes/gerar.py`.
3. Publicar na plataforma.

## Publicação na plataforma

- **Página de FAQ:** embutir `faq.html` (ou renderizar a partir do `faq.json`)
  e incluir o JSON-LD no `<head>`:
  `<script type="application/ld+json">…conteúdo de faq-schema.jsonld…</script>`
- **Ajuda contextual:** cada subseção corresponde a uma aba do produto
  (ex.: `aba-cache-formatos`, `aba-eventos`), permitindo exibir as perguntas
  relevantes dentro da própria tela.

## Pontos para validar com o time de conteúdo

- Seção 05 diz "quatro **consultoras**", mas Santiago é nome masculino —
  confirmar se o texto deve ser "consultores(as)" ou "assistentes".
- Aba Depoimentos: a pergunta é "Posso ocultar um depoimento?", mas a resposta
  fala em aprovação manual para exibir. Confirmar se é possível ocultar um
  depoimento **já aprovado**.
- No PDF original, a última pergunta ("Para que serve a integração da agenda?")
  estava fora da lista; aqui foi padronizada como as demais.
