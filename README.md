# Controle de Projetos — Controle de Demandas

Dashboard de acompanhamento da produção de projetos: pontualidade, tempos de
produção, fluxo por etapa, vazão da equipe, alocação e gargalos. Os dados são
cadastrados manualmente no painel **/admin**.

| Caminho | Conteúdo |
|---------|----------|
| `index.html` | Dashboard (visualização) |
| `licenciamento/` | **Painel de entregas do Licenciamento TB School**: o que será entregue, em qual ordem e o status de cada etapa |
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

- **23 entregas em 6 fases**, na ordem em que destravam o produto, cada uma com
  entregável, responsável, prazo, status, dependências e a fonte no documento.
- **Próxima entrega:** a primeira da ordem ainda não concluída cujas dependências
  já estão prontas. Entregas com prazo vencido aparecem como “Em atraso”.
- **Link direto por entrega:** `/licenciamento/#e07` abre a entrega 07 (botão
  “Copiar link” dentro de cada uma). `/licenciamento/#f3` abre a fase 3.
- Edição na própria página; com o banco ligado, a equipe inteira vê o mesmo estado.

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
