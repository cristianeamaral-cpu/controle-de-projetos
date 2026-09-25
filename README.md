# Controle de Projetos — Esteira de Produção de Palestras

Dashboard de acompanhamento da produção de palestras: pontualidade, tempos de
produção, fluxo por etapa, vazão da equipe, alocação e gargalos.

| Arquivo | Conteúdo |
|---------|----------|
| [`docs/PROMPT.md`](docs/PROMPT.md) | Prompt/especificação original do dashboard |
| [`docs/configuracao-hubspot.md`](docs/configuracao-hubspot.md) | Passo a passo: pipeline, propriedades customizadas e relatórios no HubSpot |
| [`dashboard/index.html`](dashboard/index.html) | Dashboard pronto (HTML único, sem dependências) |

## Como usar o dashboard

1. Abra `dashboard/index.html` no navegador. Ele já carrega dados de exemplo.
2. No HubSpot, exporte os tíquetes do pipeline **Esteira de Produção de Palestras**
   em CSV, com as colunas listadas em `docs/configuracao-hubspot.md` (seção 4).
3. Clique em **Importar CSV do HubSpot**. Todos os indicadores são recalculados
   no próprio navegador. Nenhum dado sai da sua máquina.

Use **Baixar CSV modelo** para ver o formato esperado.

## Seções

1. **KPIs de Saúde e Ritmo**: Índice de Pontualidade, Tempo Médio (Novos Produtos),
   Tempo Médio (Ajustes), Incidentes na Operação e incidentes por tipo.
2. **Fluxo das Demandas**: volume ativo por etapa e vazão semanal/quinzenal.
3. **Capacidade e Sobrecarga**: alocação por colaborador (empilhada por etapa ou
   especialidade), status geral em rosca e tabela de projetos bloqueados.
