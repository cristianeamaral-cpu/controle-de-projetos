# Configuração no HubSpot — Esteira de Produção de Palestras

Passo a passo para montar, dentro do HubSpot (Service Hub), o pipeline, as
propriedades e os relatórios descritos em [`PROMPT.md`](./PROMPT.md).

> O arquivo [`../index.html`](../index.html) é uma versão
> offline do mesmo painel: abra no navegador e importe a exportação CSV dos
> tíquetes para visualizar os mesmos indicadores fora do HubSpot.

---

## 1. Pipeline de Tíquetes

**Configurações → Objetos → Tíquetes → Pipelines → Criar pipeline**

Nome: `Esteira de Produção de Palestras`

| # | Etapa | Status do tíquete (HubSpot) |
|---|-------|-----------------------------|
| 1 | Ideação (Briefing/Pesquisa) | Aberto |
| 2 | Em Desenvolvimento (Roteiro/Design/Dev) | Aberto |
| 3 | Homologação (Validação/Trial) | Aberto |
| 4 | Pronto para Entrega / Concluído | **Fechado** |

Marcar a etapa 4 como *Fechado* faz o HubSpot preencher automaticamente a
`Data de fechamento`, que é a base dos KPIs de tempo e de vazão.

## 2. Propriedades Customizadas

**Configurações → Propriedades → Propriedades de tíquete → Criar propriedade**
(grupo sugerido: *Esteira de Palestras*)

| Rótulo | Nome interno | Tipo de campo | Opções |
|--------|--------------|---------------|--------|
| Tipo de Demanda | `tipo_de_demanda` | Seleção suspensa | Novo Produto · Ajuste/Customização |
| Incidente Operacional | `incidente_operacional` | Seleção suspensa | Nenhum · Atraso técnico · Retrabalho de conteúdo · Falha de briefing · Indisponibilidade de fornecedor · Erro de aprovação |
| Motivo do Bloqueio | `motivo_do_bloqueio` | Seleção suspensa | Aguardando aprovação da liderança · Aguardando conteúdo do palestrante · Dependência de outro time · Falta de capacidade · Pendência jurídica/contratual |
| Data de Fechamento Esperada | `data_fechamento_esperada` | Seletor de data | — |
| Status da Tarefa | `status_da_tarefa` | Seleção suspensa | A fazer · Em andamento · Bloqueado · Concluído |
| Especialidade | `especialidade` | Seleção suspensa | Designer · Copywriter · Dev |

As três últimas propriedades não estavam na lista original, mas os relatórios
precisam delas:

* **Data de Fechamento Esperada**: para o Índice de Pontualidade. Se o portal já
  usar outra propriedade de prazo, use essa.
* **Status da Tarefa**: para o gráfico de rosca e a lista de bloqueados.
* **Especialidade**: para empilhar a alocação por cargo. Também pode ficar no
  cadastro do usuário/equipe, em vez do tíquete.

**Recomendado:** crie um fluxo de trabalho que limpe `Motivo do Bloqueio` quando
`Status da Tarefa` deixar de ser *Bloqueado*.

## 3. Relatórios

**Relatórios → Dashboards → Criar dashboard** → nome: `Esteira de Produção de Palestras`.
Em todos os relatórios, filtre por **Pipeline = Esteira de Produção de Palestras**.

### Seção 1 — KPIs de Saúde e Ritmo (cartões de resumo)

| Relatório | Construtor | Configuração |
|-----------|-----------|--------------|
| Índice de Pontualidade na Entrega | Relatório personalizado (Tíquetes) → *Resumo/KPI* | Crie a propriedade calculada `entregue_no_prazo` = `if(closed_date <= data_fechamento_esperada, 1, 0)`. Métrica = média de `entregue_no_prazo` (formatada em %). Filtro: Etapa = Pronto para Entrega / Concluído. |
| Tempo Médio de Produção (Novos Produtos) | Relatório personalizado → *KPI* | Métrica: média de **Tempo até o fechamento** (em dias). Filtros: Tipo de Demanda = Novo Produto; Etapa = Concluído. |
| Tempo Médio de Ajustes | Relatório personalizado → *KPI* | Igual ao anterior, com Tipo de Demanda = Ajuste/Customização. |
| Incidentes na Operação | Relatório personalizado → *Barras horizontais* | Eixo = Incidente Operacional; Métrica = contagem de tíquetes; filtro: Incidente Operacional ≠ Nenhum/vazio. |

### Seção 2 — Fluxo das Demandas

| Relatório | Configuração |
|-----------|--------------|
| Volume na Esteira por Etapa | Barras verticais (ou funil). Eixo X = Etapa do tíquete; Eixo Y = contagem. Filtro: Etapa é Ideação, Em Desenvolvimento ou Homologação. |
| Vazão da Equipe | Colunas. Eixo X = Data de fechamento (agrupar por **semana**; troque para mês/quinzena se preferir); Eixo Y = contagem. Filtro: Etapa = Concluído; período = últimos 90 dias. |

### Seção 3 — Capacidade e Sobrecarga

| Relatório | Configuração |
|-----------|--------------|
| Alocação por Colaborador e Especialidade | Barras horizontais empilhadas. Eixo = Proprietário do tíquete; Métrica = contagem; Dividir por = Etapa do tíquete (ou Especialidade). Filtro: Etapa ≠ Concluído. |
| Demandas por Status Geral | Rosca. Dividir por = Status da Tarefa. |
| Lista de Projetos Bloqueados | Tabela. Colunas: Nome do tíquete, Proprietário, **Tempo na etapa atual** (ou dias desde a última alteração de `status_da_tarefa`), Motivo do Bloqueio. Filtro: Status da Tarefa = Bloqueado. Ordenar pelo tempo, decrescente. |

## 4. Exportar dados para o dashboard offline

**Tíquetes → Exportar** (formato CSV) com estas colunas, nesta nomenclatura:

```
ID do tíquete, Nome do tíquete, Proprietário do tíquete, Especialidade,
Tipo de Demanda, Etapa do tíquete, Status da Tarefa, Data de criação,
Data de Fechamento Esperada, Data de fechamento, Incidente Operacional,
Motivo do Bloqueio, Data de entrada na etapa atual
```

Datas em `AAAA-MM-DD` ou `DD/MM/AAAA`. O botão **Baixar CSV modelo** do
dashboard gera um arquivo de exemplo no formato esperado.
