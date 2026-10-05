# Controle de Projetos — Controle de Demandas

Dashboard de acompanhamento da produção de projetos: pontualidade, tempos de
produção, fluxo por etapa, vazão da equipe, alocação e gargalos. Os dados são
cadastrados manualmente no painel **/admin**.

| Caminho | Conteúdo |
|---------|----------|
| `index.html` | Dashboard (visualização) |
| `licenciamento/` | **Painel de entregas do Licenciamento TB School**: o que será entregue, em qual ordem e o status de cada etapa |
| `vercel.json` | Abre o painel do Licenciamento na raiz dos domínios que começam com `licenciamento` |
| `licenciamento/onboarding/` | MVP do onboarding de quem comprou o Licenciamento |
| `api/licenciamento.js` | Função da Vercel que guarda o painel do Licenciamento no mesmo banco (chave própria) |
| `admin/` | Painel de edição: projetos, listas de opções, seções e cartões do dashboard |
| `api/data.js` | Função da Vercel que lê e grava os dados no banco (Upstash Redis) |
| `assets/` | Estilos, cálculos e gráficos compartilhados |
| [`docs/banco-de-dados.md`](docs/banco-de-dados.md) | **Como ligar o banco de dados na Vercel** |
| [`docs/PROMPT.md`](docs/PROMPT.md) | Prompt/especificação original do dashboard |
| [`docs/configuracao-hubspot.md`](docs/configuracao-hubspot.md) | Referência de pipeline, propriedades e relatórios no HubSpot |

## Painel do Licenciamento (/licenciamento)

Gestor de entregas do produto Licenciamento TB School, montado a partir do
“06 · Manual Final”, “07 · Decisões Finais” e “Arquitetura do Produto”.

- **Quadro em 6 colunas, uma por fase**, com as 24 entregas na ordem em que
  destravam o produto (clique numa entrega para editar), cada uma com
  entregável, responsável, prazo, status, dependências e a fonte no documento.
- **Próxima entrega:** a primeira da ordem ainda não concluída cujas dependências
  já estão prontas. Entregas com prazo vencido aparecem como “Em atraso”.
- **Link direto por entrega:** `/licenciamento/#e07` abre a entrega 07 (botão
  “Copiar link” dentro de cada uma). `/licenciamento/#f3` abre a fase 3.
- Edição na própria página; com o banco ligado, a equipe inteira vê o mesmo estado.

### Onboarding do Licenciado (/licenciamento/onboarding/)

MVP do que o cliente vê depois de comprar o Licenciamento, em 8 passos
baseados no Manual Final: boas-vindas, cadastro (com o compromisso de seguir a
metodologia), escolha da turma (que calcula as datas dos 14 dias), Espelho dos
12 pilares com radar, Plateia online (Dias 0–6), testes por eixo com nota
mínima de 70% (pré-requisito do presencial), imersão presencial com as duas
certificações e os primeiros passos como Licenciado (Kit, Comunidade, Vendas e
primeira turma). As turmas são em Porto Alegre (time interno PSA em 24/10/2026; time externo em 26 e
27/10/2026) e o progresso fica salvo só no
navegador.

### Endereço próprio (landing page)

O `vercel.json` faz qualquer domínio do projeto que comece com `licenciamento`
abrir o painel direto na raiz. Para ativar, na Vercel: **Settings → Domains →
Add** e cadastre, por exemplo, `licenciamento-tbschool.vercel.app` (ou um
subdomínio seu, como `licenciamento.seudominio.com.br`). O painel continua
também em `/licenciamento/` no domínio principal, e os links de entrega
funcionam nos dois (`…/#e07`).

## O que dá para fazer no /admin

- **Projetos:** cadastrar, editar e excluir (nome, responsável, especialidade,
  tipo de demanda, etapa, status, datas de criação/prazo/entrega, incidente e
  motivo do bloqueio).
- **Listas de opções:** pessoas da equipe, especialidades, tipos de demanda,
  etapas, status, incidentes e motivos de bloqueio. Renomear um item atualiza
  todos os projetos que o usam.
- **Seções do dashboard:** criar, renomear, reordenar e excluir seções; mostrar ou
  esconder, reordenar, mover e configurar cada cartão ou gráfico; criar gráficos
  novos (agrupar por qualquer campo, em barras, colunas ou rosca, com filtro) e
  cartões com **números digitados**.
- **Geral:** título e subtítulo do dashboard, cópia de segurança (JSON) e restauração.

As alterações são salvas automaticamente.

## Testar no computador

```
python3 -m http.server 8000
```

Abra `http://localhost:8000`. Sem a função da Vercel, o site roda em modo
local e salva os dados só no navegador.
