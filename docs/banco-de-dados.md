# Banco de dados: como ligar na Vercel

O `/admin` salva tudo (projetos, listas e seções) num banco **Upstash Redis**
conectado ao projeto da Vercel. O plano gratuito é suficiente.

Enquanto o banco não estiver conectado, o dashboard funciona em **modo local**:
o que for salvo no `/admin` fica só no navegador de quem salvou, e aparece um
aviso amarelo no topo das páginas.

## Passo a passo (uma vez só)

1. Abra o projeto na Vercel → aba **Storage** → **Create Database**.
2. Escolha **Upstash** → **Redis** (Upstash for Redis) → aceite o plano gratuito
   → escolha a região mais próxima (ex.: São Paulo, `gru1`) → **Create**.
3. Na tela seguinte, clique em **Connect Project** e selecione este projeto
   (marque os ambientes *Production* e *Preview*).
   A Vercel cria sozinha as variáveis `KV_REST_API_URL` e `KV_REST_API_TOKEN`.
4. Vá em **Deployments** → no deploy mais recente → **⋯ → Redeploy**.
   As variáveis só valem para deploys feitos depois de conectar o banco.
5. Abra `/admin`. O indicador no topo deve mostrar **“Conectado ao banco”**.
   Na primeira vez, o banco vem com os projetos de exemplo. Para zerar:
   **Geral → Apagar todos os projetos**.

> Também funciona com um banco criado direto no site da Upstash: basta cadastrar
> `UPSTASH_REDIS_REST_URL` e `UPSTASH_REDIS_REST_TOKEN` em
> **Settings → Environment Variables** e fazer o redeploy.

## Branch de produção

O endereço principal (`…vercel.app`) só publica o branch configurado em
**Settings → Git → Production Branch**. Se ele apontar para `main` e esse branch
não existir no repositório, o site mostra 404 ou uma versão antiga.

## Como funciona

- `api/data.js` é uma função da Vercel: `GET /api/data` lê e `POST /api/data`
  grava o documento inteiro (um único registro no Redis).
- Cada gravação tem um número de versão. Se duas pessoas editarem ao mesmo tempo,
  a segunda recebe o aviso *“Outra pessoa salvou alterações”* e precisa
  recarregar. Assim ninguém apaga o trabalho do outro sem perceber.
- **Sem senha:** qualquer pessoa com o link do `/admin` consegue editar e excluir.
  Faça cópias de segurança em **Geral → Baixar cópia de segurança (JSON)**.
