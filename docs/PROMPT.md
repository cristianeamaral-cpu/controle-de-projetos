# Prompt — Dashboard "Esteira de Produção de Projetos"

> Prompt original usado para gerar o dashboard deste repositório.
> Guia prático de configuração: [`configuracao-hubspot.md`](./configuracao-hubspot.md).
> Dashboard gerado: [`../index.html`](../index.html).

## Pré-requisitos

Para que os relatórios funcionem, configure um **Pipeline de Tíquetes** chamado
`Esteira de Produção de Projetos` com as seguintes etapas:

1. Ideação (Briefing/Pesquisa)
2. Em Desenvolvimento (Roteiro/Design/Dev)
3. Homologação (Validação/Trial)
4. Pronto para Entrega / Concluído

Crie as seguintes **Propriedades Customizadas** nos tíquetes:

* `Tipo de Demanda` (Novo Produto ou Ajuste/Customização)
* `Incidente Operacional` (Atraso técnico, etc.)
* `Motivo do Bloqueio` (gargalo)

## Estrutura do Dashboard

### SEÇÃO 1: KPIs de Saúde e Ritmo (Visualização em Cartões de Resumo)

Estes cartões ficam no topo do painel para que o PM e a liderança batam o olho no desempenho geral.

* **Índice de Pontualidade na Entrega**
  * Tipo de relatório: Relatório de tíquetes personalizados.
  * Métrica: Percentual de tíquetes concluídos antes ou na `Data de Fechamento Esperada`.
* **Tempo Médio de Produção (Novos Produtos)**
  * Filtro: `Tipo de Demanda` = Novo Produto + Etapa = Concluído.
  * Métrica: Média de dias decorridos entre a data de criação e a data de fechamento.
* **Tempo Médio de Ajustes**
  * Filtro: `Tipo de Demanda` = Ajuste/Customização + Etapa = Concluído.
  * Métrica: Média de dias decorridos entre a abertura do ajuste e a entrega.
* **Incidentes na Operação**
  * Tipo de relatório: Gráfico de pizza ou barras horizontais.
  * Métrica: Contagem de tíquetes agrupados por tipo de erro marcado na propriedade `Incidente Operacional`.

### SEÇÃO 2: O Fluxo das Demandas

Mostra o volume físico de trabalho passando pelas fases acordadas.

* **Volume na Esteira por Etapa (Ideação, Desenvolvimento e Homologação)**
  * Tipo de relatório: Gráfico de barras verticais ou funil.
  * Configuração: Eixo X = `Etapa do tíquete`; Eixo Y = `Contagem de tíquetes`.
  * Objetivo: Monitorar o acúmulo de projetos em Em Desenvolvimento (onde Designers, Copywriters e Devs atuam simultaneamente).
* **Vazão da Equipe**
  * Tipo de relatório: Gráfico de linhas ou colunas diárias/semanais.
  * Configuração: Eixo X = `Data de Fechamento` (agrupado por semana ou quinzena); Eixo Y = `Contagem de tíquetes concluídos`.

### SEÇÃO 3: Gestão de Capacidade e Sobrecarga (Pessoas & Gargalos)

Mede o fator humano e os impedimentos da equipe.

* **Alocação por Colaborador e Especialidade**
  * Tipo de relatório: Gráfico de barras empilhadas (Vertical ou Horizontal).
  * Configuração: Eixo X = `Proprietário do tíquete` (Membro do time); Eixo Y = `Contagem de tíquetes ativos` (não concluídos); Empilhado por = `Etapa do Tíquete` ou cargo (Designer, Copywriter, Dev).
  * Assonância com a dor: Permite ver imediatamente se um Designer está com 10 tíquetes em andamento enquanto o Copywriter tem apenas 2.
* **Demandas por Status Geral**
  * Tipo de relatório: Gráfico de rosca.
  * Configuração: Divisão visual por status interno da tarefa no ecossistema (A fazer, Em andamento, Bloqueado, Concluído).
* **Lista de Projetos Bloqueados (Gargalos Críticos)**
  * Tipo de relatório: Relatório em formato de tabela detalhada.
  * Colunas: `Nome do Projeto`, `Proprietário`, `Tempo que permanece no status atual`, `Motivo do Bloqueio`.
  * Filtro: `Status` = Bloqueado (ou etapa correspondente que depende da liderança).
