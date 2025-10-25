# 🚀 TeleNordeste Integration

**Integração automática entre Notion e Google Calendar**

Sincronize tarefas do Notion diretamente para o Google Calendar de forma automática e inteligente.

---

## 📋 Índice

1. [Características](#-características)
2. [Requisitos](#-requisitos)
3. [Instalação](#-instalação)
4. [Configuração](#-configuração)
5. [Uso](#-uso)
6. [Estrutura do Projeto](#-estrutura-do-projeto)
7. [Troubleshooting](#-troubleshooting)
8. [FAQ](#-faq)

---

## ✨ Características

- ✅ **Sincronização bidirecional** (Notion → Google Calendar)
- 🔄 **Detecção de duplicatas** (evita criar eventos repetidos)
- 🎯 **Filtros personalizáveis** (por status, data, etc)
- 🔍 **Modo Dry Run** (teste antes de criar eventos reais)
- 📊 **Histórico de sincronizações**
- 🔐 **Autenticação OAuth segura**
- 📝 **Logs detalhados**
- 🎨 **Interface amigável**

---

## 🛠 Requisitos

### Software

- Python 3.8 ou superior
- Conta Google (para Google Calendar)
- Conta Notion (com workspace)

### APIs Necessárias

1. **Notion API** - Integration Token
2. **Google Calendar API** - OAuth 2.0 Credentials

---

## 📦 Instalação

### 1. Clone ou baixe o projeto

```bash
cd workspaces/telenordeste_integration
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Verificar instalação

```bash
python -c "import requests, google.auth; print('✅ Dependências instaladas!')"
```

---

## ⚙ Configuração

### Passo 1: Configurar Notion

#### 1.1. Criar Integration

1. Acesse: https://www.notion.so/my-integrations
2. Clique em **"+ New integration"**
3. Dê um nome (ex: "TeleNordeste Calendar Sync")
4. Selecione o workspace
5. Copie o **Internal Integration Token** (começa com `secret_`)

#### 1.2. Compartilhar Database

1. Abra seu database no Notion
2. Clique nos **três pontos** (⋮) no canto superior direito
3. Selecione **"Add connections"**
4. Escolha sua integração criada
5. Copie o **Database ID** da URL:
   ```
   https://notion.so/workspace/[DATABASE_ID]?v=...
                              ^^^^^^^^^^^^^^^^
   ```

#### 1.3. Estrutura Recomendada do Database

Seu database deve ter estas propriedades:

| Propriedade | Tipo | Obrigatório | Descrição |
|------------|------|-------------|-----------|
| Name | Title | ✅ | Título da tarefa |
| Data | Date | ✅ | Data/hora do evento |
| Status | Select | ✅ | Status da tarefa (ex: "A Fazer") |
| Descrição | Rich Text | ❌ | Descrição detalhada |
| Duração | Number | ❌ | Duração em minutos (padrão: 60) |

### Passo 2: Configurar Google Calendar

#### 2.1. Criar Projeto no Google Cloud

1. Acesse: https://console.cloud.google.com/
2. Crie um novo projeto (ou use existente)
3. Dê um nome (ex: "TeleNordeste Integration")

#### 2.2. Ativar Google Calendar API

1. No menu lateral, vá em **"APIs & Services" > "Library"**
2. Busque por **"Google Calendar API"**
3. Clique em **"Enable"**

#### 2.3. Criar Credenciais OAuth 2.0

1. Vá em **"APIs & Services" > "Credentials"**
2. Clique em **"+ CREATE CREDENTIALS"**
3. Selecione **"OAuth client ID"**
4. Se solicitado, configure a **"OAuth consent screen"**:
   - User Type: **External** (ou Internal se G Workspace)
   - App name: TeleNordeste Integration
   - User support email: seu email
   - Developer contact: seu email
5. Application type: **"Desktop app"**
6. Dê um nome (ex: "TeleNordeste Desktop")
7. Clique em **"CREATE"**
8. **IMPORTANTE**: Clique em **"DOWNLOAD JSON"**
9. Salve o arquivo como **`credentials.json`** na pasta do projeto

### Passo 3: Executar Assistente de Configuração

```bash
python main.py
```

O assistente irá guiá-lo através da configuração inicial.

---

## 🎮 Uso

### Executar o programa

```bash
python main.py
```

### Menu Principal

```
┌──────────────────────────────────────────────────────────────┐
│                        MENU PRINCIPAL                         │
├──────────────────────────────────────────────────────────────┤
│  1. 🧪 Testar Conexões                                       │
│  2. 🔍 Sincronizar (Dry Run - Simulação)                     │
│  3. 🚀 Sincronizar (Real - Criar Eventos)                    │
│  4. 📊 Ver Estatísticas                                      │
│  5. 📜 Ver Histórico de Sincronização                        │
│  6. 🔧 Reconfigurar Credenciais                              │
│  7. 📖 Ajuda                                                 │
│  8. 🚪 Sair                                                  │
└──────────────────────────────────────────────────────────────┘
```

### Fluxo Recomendado

1. **Testar Conexões** (opção 1)
   - Verifica se Notion e Google Calendar estão acessíveis

2. **Dry Run** (opção 2)
   - Simula a sincronização sem criar eventos
   - Mostra quantos eventos seriam criados

3. **Sincronização Real** (opção 3)
   - Cria eventos reais no Google Calendar
   - Requer confirmação explícita

### Uso Programático

```python
from config import ConfigManager
from integrator import NotionCalendarIntegrator

# Inicializar
config = ConfigManager()
integrator = NotionCalendarIntegrator(config)

# Testar conexões
integrator.test_connections()

# Sincronizar (dry run)
stats = integrator.sync_tasks_to_calendar(
    status_filter="A Fazer",
    dry_run=True
)

# Sincronizar (real)
stats = integrator.sync_tasks_to_calendar(
    status_filter="A Fazer",
    dry_run=False
)

print(f"Eventos criados: {stats['created']}")
```

---

## 📁 Estrutura do Projeto

```
telenordeste_integration/
├── config.py                   # Gerenciador de configurações
├── notion_client.py            # Cliente Notion API
├── google_calendar_client.py   # Cliente Google Calendar API
├── integrator.py               # Orquestrador principal
├── main.py                     # Interface de usuário
├── requirements.txt            # Dependências Python
├── README_COMPLETO.md          # Esta documentação
├── config.json                 # Configurações (criado automaticamente)
├── credentials.json            # Credenciais Google (você fornece)
├── token.json                  # Token OAuth (criado automaticamente)
└── integration.log             # Logs de execução
```

### Arquivos Importantes

- **config.json**: Configurações gerais (tokens, IDs, mapeamentos)
- **credentials.json**: Credenciais OAuth do Google (não commitar!)
- **token.json**: Token de autenticação (não commitar!)
- **integration.log**: Histórico de operações

---

## 🔧 Troubleshooting

### Erro: "Notion API Token não configurado"

**Solução**: Execute o assistente de configuração:
```bash
python main.py
```

### Erro: "Arquivo de credenciais não encontrado"

**Solução**: 
1. Baixe credentials.json do Google Cloud Console
2. Coloque na pasta do projeto
3. Verifique o nome: deve ser exatamente `credentials.json`

### Erro: "Access blocked: This app isn't verified"

**Solução**:
1. Na tela de autenticação, clique em "Advanced"
2. Clique em "Go to [App Name] (unsafe)"
3. Isso é normal para apps em desenvolvimento

### Erro: "Database not found"

**Solução**:
1. Verifique se o Database ID está correto
2. Certifique-se de ter compartilhado o database com a integração

### Eventos duplicados

**Solução**:
- O sistema verifica automaticamente duplicatas por título
- Se encontrar duplicatas, verifique o filtro de datas

### Tarefas não aparecem

**Solução**:
1. Verifique o filtro de status em config.json
2. Certifique-se de que as tarefas têm data definida
3. Use modo Dry Run para debug

---

## ❓ FAQ

### Posso sincronizar múltiplos databases?

Atualmente não, mas você pode criar múltiplas instâncias da integração, cada uma com seu próprio config.json.

### Como alterar o calendário de destino?

Edite `config.json`:
```json
{
  "google_calendar": {
    "calendar_id": "SEU_CALENDAR_ID"
  }
}
```

Para usar calendário secundário, substitua `"primary"` pelo ID do calendário.

### Como personalizar os campos mapeados?

Edite a seção `mapping` em `config.json`:
```json
{
  "mapping": {
    "title_field": "Nome",
    "date_field": "Quando",
    "description_field": "Notas",
    "duration_field": "Tempo"
  }
}
```

### Posso automatizar a sincronização?

Sim! Use agendador de tarefas:

**Windows (Task Scheduler)**:
```bash
schtasks /create /tn "Notion Sync" /tr "python C:\caminho\main.py" /sc daily /st 09:00
```

**Linux/Mac (Cron)**:
```bash
0 9 * * * cd /caminho && python main.py
```

### Como atualizar eventos já criados?

Atualmente o sistema não atualiza eventos existentes. Para isso, você precisaria:
1. Deletar o evento no Calendar
2. Executar a sincronização novamente

### É seguro?

Sim!
- Usa OAuth 2.0 (padrão da indústria)
- Tokens armazenados localmente
- Sem compartilhamento de credenciais
- Código aberto para auditoria

### Onde ficam os logs?

No arquivo `integration.log` na pasta do projeto.

Para ver em tempo real (Linux/Mac):
```bash
tail -f integration.log
```

---

## 🎯 Próximos Passos

Após configurar:

1. ✅ Teste as conexões
2. ✅ Execute Dry Run
3. ✅ Sincronize algumas tarefas de teste
4. ✅ Configure automação (opcional)
5. ✅ Personalize mapeamentos (opcional)

---

## 📞 Suporte

Para problemas ou dúvidas:

1. Verifique a seção [Troubleshooting](#-troubleshooting)
2. Consulte o [FAQ](#-faq)
3. Revise os logs em `integration.log`

---

## 📝 Licença

Este projeto é de uso interno da TeleNordeste.

---

## 🙏 Créditos

Desenvolvido para automatizar o fluxo de trabalho entre Notion e Google Calendar.

**Versão**: 1.0.0  
**Data**: Outubro 2025

---

## 🔄 Changelog

### v1.0.0 (2025-10-23)
- ✨ Lançamento inicial
- ✅ Integração Notion → Google Calendar
- ✅ Modo Dry Run
- ✅ Detecção de duplicatas
- ✅ Interface de usuário
- ✅ Sistema de logs
