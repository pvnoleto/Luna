# 🚀 Guia de Configuração - TeleNordeste Integration

## Pré-requisitos

- Python 3.8 ou superior
- Conta Notion com acesso à API
- Conta Google com acesso ao Calendar
- Projeto Google Cloud (gratuito)

## Passo 1: Configurar Notion

### 1.1 Obter API Key do Notion

1. Acesse: https://www.notion.so/my-integrations
2. Clique em **"+ New integration"**
3. Dê um nome (ex: "TeleNordeste Sync")
4. Selecione o workspace
5. Copie o **Internal Integration Token** (começa com `secret_`)

### 1.2 Compartilhar Database com a Integração

1. Abra seu database de tarefas no Notion
2. Clique nos **três pontos** (•••) no canto superior direito
3. Selecione **"Add connections"**
4. Escolha sua integração
5. Copie o **Database ID** da URL:
   - URL: `https://notion.so/workspace/DATABASE_ID?v=...`

### 1.3 Estrutura Recomendada do Database

Crie um database com as seguintes propriedades:

| Propriedade | Tipo | Descrição |
|------------|------|-----------|
| Name/Título | Title | Nome da tarefa |
| Status | Select | A Fazer, Em Progresso, Concluído |
| Data | Date | Data/prazo da tarefa |
| Prioridade | Select | Alta, Média, Baixa |
| Responsável | Person | Quem vai executar |
| Descrição | Text | Detalhes da tarefa |

## Passo 2: Configurar Google Calendar

### 2.1 Criar Projeto no Google Cloud

1. Acesse: https://console.cloud.google.com/
2. Clique em **"Select a project"** → **"New Project"**
3. Nome: "TeleNordeste Sync"
4. Clique em **"Create"**

### 2.2 Ativar Google Calendar API

1. No menu lateral, vá em **"APIs & Services"** → **"Library"**
2. Busque por "Google Calendar API"
3. Clique em **"Enable"**

### 2.3 Criar Credenciais OAuth 2.0

1. Vá em **"APIs & Services"** → **"Credentials"**
2. Clique em **"+ Create Credentials"** → **"OAuth client ID"**
3. Se solicitado, configure a **OAuth consent screen**:
   - User Type: External
   - App name: TeleNordeste Sync
   - User support email: seu email
   - Developer contact: seu email
4. Application type: **Desktop app**
5. Name: "TeleNordeste Desktop"
6. Clique em **"Create"**
7. **BAIXE** o arquivo JSON (📥 Download JSON)
8. Renomeie para `credentials.json` e coloque em `config/credentials.json`

## Passo 3: Instalar o Sistema

### 3.1 Instalar Dependências

```bash
# Navegue até o diretório do projeto
cd workspaces/telenordeste_integration

# Instale as dependências
pip install -r requirements.txt
```

### 3.2 Configurar Variáveis de Ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env e configure:
# - NOTION_API_KEY (do passo 1.1)
# - NOTION_DATABASE_ID (do passo 1.2)
# - GOOGLE_CALENDAR_ID (geralmente "primary")
# - TIMEZONE (ex: America/Fortaleza)
```

### 3.3 Primeira Autenticação com Google

```bash
# Execute o teste de conexão
cd src
python calendar_client.py
```

Isso abrirá seu navegador para autorizar o acesso ao Google Calendar.
Após autorizar, um arquivo `token.pickle` será criado automaticamente.

## Passo 4: Testar a Integração

### 4.1 Listar Tarefas do Notion

```bash
cd src
python main.py list-tasks
```

### 4.2 Listar Eventos do Calendar

```bash
python main.py list-events
```

### 4.3 Sincronizar Tarefas

```bash
# Sincronização manual
python main.py sync

# Sincronizar apenas "A Fazer"
python main.py sync --status "A Fazer"
```

## Passo 5: Usar Sincronização Automática

### 5.1 Modo Contínuo

```bash
# Sincroniza automaticamente a cada 15 minutos
python main.py auto

# Ou especifique o intervalo
python main.py auto --interval 30
```

### 5.2 Como Serviço (Opcional)

#### Windows (Task Scheduler)

1. Abra **Task Scheduler**
2. Crie nova tarefa:
   - Trigger: At startup + Repeat every 15 minutes
   - Action: Start program
   - Program: `python`
   - Arguments: `"C:\path\to\Luna\workspaces\telenordeste_integration\src\main.py" auto`

#### Linux/Mac (Cron)

```bash
# Edite crontab
crontab -e

# Adicione (executa a cada 15 minutos)
*/15 * * * * cd /path/to/telenordeste_integration/src && python main.py sync
```

## 📋 Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `python main.py sync` | Sincroniza todas as tarefas |
| `python main.py sync --status "A Fazer"` | Sincroniza por status |
| `python main.py auto` | Sincronização automática contínua |
| `python main.py list-tasks` | Lista tarefas do Notion |
| `python main.py list-events` | Lista eventos do Calendar |
| `python main.py cleanup` | Remove eventos de tarefas concluídas |
| `python main.py info` | Mostra informações de sincronização |

## 🔧 Solução de Problemas

### Erro: "notion-client not found"

```bash
pip install --upgrade notion-client
```

### Erro: "credentials.json not found"

Certifique-se de que o arquivo está em `config/credentials.json`

### Erro: "Invalid database_id"

Verifique se:
1. O Database ID está correto
2. A integração foi compartilhada com o database

### Eventos duplicados

```bash
# Limpe o estado e ressincronize
rm config/sync_state.json
python main.py sync
```

## 🎯 Dicas de Uso

1. **Primeira sincronização**: Execute `python main.py sync` para criar todos os eventos
2. **Manutenção**: Use `python main.py cleanup` semanalmente
3. **Status**: Verifique com `python main.py info`
4. **Filtros**: Use `--status` para sincronizar apenas tarefas específicas

## 📞 Suporte

Para problemas ou dúvidas, abra uma issue no repositório ou entre em contato.

---

✅ Configuração completa! Agora suas tarefas do Notion serão sincronizadas automaticamente com o Google Calendar.
