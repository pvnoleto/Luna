# TeleNordeste - Integração Notion + Google Calendar

Sistema de integração automática que sincroniza tarefas do Notion com o Google Calendar.

## Funcionalidades

- 📋 Busca tarefas do Notion Database
- 📅 Cria eventos no Google Calendar automaticamente
- 🔄 Sincronização bidirecional
- ⚡ Atualização em tempo real
- 🔐 Autenticação segura via OAuth2

## Estrutura do Projeto

```
telenordeste_integration/
├── config/
│   ├── credentials.json          # Credenciais Google Calendar
│   └── notion_config.json        # Configuração Notion
├── src/
│   ├── notion_client.py          # Cliente Notion API
│   ├── calendar_client.py        # Cliente Google Calendar API
│   ├── sync_manager.py           # Gerenciador de sincronização
│   └── main.py                   # Aplicação principal
├── requirements.txt
└── README.md
```

## Configuração

1. Configure as credenciais do Notion
2. Configure as credenciais do Google Calendar
3. Execute: `python src/main.py`

## Requisitos

- Python 3.8+
- Conta Notion com API habilitada
- Projeto Google Cloud com Calendar API habilitada
