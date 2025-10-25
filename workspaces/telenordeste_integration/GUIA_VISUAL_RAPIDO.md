# 🎯 GUIA VISUAL RÁPIDO - Em 3 Passos

**Tempo total: 15-20 minutos** ⏱️

---

## 📊 STATUS ATUAL

```
🟢🟢🟢🟢🟢🟢🟢🟢⚪⚪  83% Completo
└─────────────────────┘
      JÁ PRONTO        FALTA
```

---

## 🚀 PASSO 1: INSTALAR DEPENDÊNCIAS (2 min)

```bash
cd workspaces\telenordeste_integration
pip install -r requirements.txt
```

### ✅ Resultado Esperado:
```
Successfully installed:
  - requests
  - google-auth ⭐ (IMPORTANTE!)
  - google-auth-oauthlib
  - google-api-python-client
  - python-dateutil
  - pytz
```

---

## 🔵 PASSO 2: CONFIGURAR NOTION (5 min)

### 2.1. Criar Integração
```
🌐 Abrir: https://www.notion.so/my-integrations

┌─────────────────────────────────────┐
│  Notion Integrations                │
├─────────────────────────────────────┤
│  [+ New integration]  ← CLICAR      │
└─────────────────────────────────────┘

Nome: TeleNordeste Calendar Sync
Workspace: [seu workspace]

⬇️

📋 COPIAR: Integration Token
   (começa com "secret_...")
```

### 2.2. Conectar ao Database
```
📄 Abrir seu database no Notion

┌────────────────────────────────┐
│  Meu Database     ⋮  ← CLICAR │
├────────────────────────────────┤
│  → Add connections             │
│  → TeleNordeste Calendar Sync  │
└────────────────────────────────┘

⬇️

📋 COPIAR: Database ID da URL
   notion.so/workspace/[ISSO_AQUI]?v=...
                       ↑↑↑↑↑↑↑↑↑↑
```

### 2.3. Atualizar config.json
```json
{
  "notion": {
    "token": "secret_cole_aqui",
    "database_id": "cole_aqui"
  },
  "site": { ... },
  "credenciais": { ... },
  ...
}
```

---

## 🔴 PASSO 3: CONFIGURAR GOOGLE (10 min)

### 3.1. Criar Projeto
```
🌐 Abrir: https://console.cloud.google.com/

┌────────────────────────────────────┐
│  Select a project ▼                │
├────────────────────────────────────┤
│  → NEW PROJECT                     │
│     Nome: TeleNordeste Integration │
│     [CREATE]                       │
└────────────────────────────────────┘
```

### 3.2. Ativar API
```
📚 Menu → APIs & Services → Library

┌────────────────────────────────────┐
│  🔍 Search: Google Calendar API    │
├────────────────────────────────────┤
│  Google Calendar API               │
│  [ENABLE]  ← CLICAR                │
└────────────────────────────────────┘
```

### 3.3. Criar Credenciais
```
🔐 APIs & Services → Credentials

┌────────────────────────────────────┐
│  [+ CREATE CREDENTIALS ▼]          │
├────────────────────────────────────┤
│  → OAuth client ID                 │
└────────────────────────────────────┘

⬇️

Se aparecer "Configure consent screen":
┌────────────────────────────────────┐
│  User Type: ⚪ Internal            │
│             ⚫ External            │
│  App name: TeleNordeste Integration│
│  User support email: seu@email.com │
│  [SAVE AND CONTINUE]               │
└────────────────────────────────────┘

⬇️

Application type: Desktop app
Name: TeleNordeste Desktop
[CREATE]

⬇️

┌────────────────────────────────────┐
│  OAuth client created              │
│  [DOWNLOAD JSON]  ← CLICAR         │
└────────────────────────────────────┘

⬇️

1. Renomear para: credentials.json
2. Mover para: workspaces\telenordeste_integration\
```

---

## ✅ VERIFICAR TUDO (1 min)

```bash
python verificar_status.py
```

### ✅ Esperado:
```
════════════════════════════════════════════════
         TELENORDESTE INTEGRATION
           STATUS CHECK COMPLETO
════════════════════════════════════════════════

✅ Python 3.8+........................... OK
✅ Dependências......................... OK
✅ Arquivos Essenciais.................. OK
✅ Configurações........................ OK
✅ Credenciais.......................... OK
✅ Documentação......................... OK

🎉 Projeto 100% pronto!
```

---

## 🎮 USAR O SISTEMA

```bash
python main.py
```

### Menu:
```
╔════════════════════════════════════════╗
║           MENU PRINCIPAL               ║
╠════════════════════════════════════════╣
║  1. 🧪 Testar Conexões                ║
║  2. 🔍 Dry Run (Simulação)            ║
║  3. 🚀 Sincronizar (Real)             ║
║  4. 📊 Estatísticas                   ║
║  5. 📜 Histórico                      ║
╚════════════════════════════════════════╝
```

### Fluxo Recomendado:
```
1️⃣  Opção 1 → Testar Conexões
    ✅ Notion: OK
    ✅ Google Calendar: OK

         ↓

2️⃣  Opção 2 → Dry Run
    🔍 Buscando tarefas...
    📋 5 tarefas encontradas
    🧪 Simulando criação...
    ✅ 5 eventos seriam criados

         ↓

3️⃣  Opção 3 → Sincronizar (Real)
    ⚠️  Isso criará eventos REAIS!
    ❓ Confirma? (s/n): s
    🚀 Sincronizando...
    ✅ 5 eventos criados!
    📊 Histórico atualizado
```

---

## 🎯 DIAGRAMA DE FLUXO

```
┌─────────────────────────────────────────────────┐
│                   USUÁRIO                       │
└──────────────────┬──────────────────────────────┘
                   │ python main.py
                   ↓
┌─────────────────────────────────────────────────┐
│              main.py (CLI)                      │
│  • Menu interativo                              │
│  • Validações                                   │
│  • Confirmações                                 │
└──────────────────┬──────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────┐
│           integrator.py                         │
│  • Orquestra sincronização                      │
│  • Detecta duplicatas                           │
│  • Gera histórico                               │
└─────┬────────────────────────┬──────────────────┘
      │                        │
      ↓                        ↓
┌──────────────┐      ┌────────────────────┐
│notion_client │      │google_calendar_    │
│              │      │client              │
│• Busca       │      │• Cria eventos      │
│  tarefas     │      │• Verifica          │
│• Filtra      │      │  duplicatas        │
│  por status  │      │• Lista eventos     │
└──────┬───────┘      └────────┬───────────┘
       │                       │
       ↓                       ↓
┌──────────────┐      ┌────────────────────┐
│  Notion API  │      │ Google Calendar    │
│              │      │ API                │
└──────────────┘      └────────────────────┘
```

---

## 📱 ESTRUTURA DO DATABASE NOTION

### Propriedades Obrigatórias:

| Coluna | Tipo | Exemplo |
|--------|------|---------|
| 📝 **Name** | Title | "Consulta Dr. Silva" |
| 📅 **Data** | Date | 25/10/2025 14:00 |
| 🏷️ **Status** | Select | "A Fazer" |

### Propriedades Opcionais:

| Coluna | Tipo | Exemplo |
|--------|------|---------|
| 📄 Descrição | Text | "Teleconsulta cardiologia" |
| ⏱️ Duração | Number | 60 (minutos) |
| 🏥 Especialidade | Select | "Cardiologia" |
| 👤 Paciente | Text | "João Silva" |

### Exemplo Visual:
```
┌─────────────────────┬────────────┬──────────┬───────────────┐
│ Name                │ Data       │ Status   │ Especialidade │
├─────────────────────┼────────────┼──────────┼───────────────┤
│ Consulta Dr. Silva  │ 25/10 14:00│ A Fazer  │ Cardiologia   │
│ Retorno Dra. Maria  │ 26/10 10:00│ A Fazer  │ Dermatologia  │
│ Exame João          │ 27/10 15:30│ A Fazer  │ Neurologia    │
└─────────────────────┴────────────┴──────────┴───────────────┘
                            ↓
                     Sincronização
                            ↓
┌─────────────────────────────────────────────────────────┐
│              📅 GOOGLE CALENDAR                         │
├─────────────────────────────────────────────────────────┤
│ 25 OUT  14:00-15:00  Consulta Dr. Silva                │
│ 26 OUT  10:00-11:00  Retorno Dra. Maria                │
│ 27 OUT  15:30-16:30  Exame João                        │
└─────────────────────────────────────────────────────────┘
```

---

## 🔍 TROUBLESHOOTING RÁPIDO

### ❌ Erro: "No module named 'google.auth'"
```bash
pip install google-auth
```

### ❌ Erro: "Invalid Notion Token"
- ✅ Verificar se começa com "secret_"
- ✅ Confirmar integração conectada ao database

### ❌ Erro: "Google Calendar API not enabled"
- ✅ Ir em Google Cloud Console
- ✅ APIs & Services → Library
- ✅ Buscar "Google Calendar API" → Enable

### ❌ Erro: "No tasks found"
- ✅ Verificar tarefas com status "A Fazer"
- ✅ Verificar campo Data preenchido
- ✅ Verificar data futura ou hoje

---

## 📞 LINKS RÁPIDOS

### Configuração
- 🔵 **Notion:** notion.so/my-integrations
- 🔴 **Google:** console.cloud.google.com

### Documentação
- 📖 **Completa:** README_COMPLETO.md
- ⚡ **Rápida:** QUICK_START.md
- 📋 **Ações:** ACOES_IMEDIATAS.md
- 📊 **Status:** STATUS_PROJETO.md

### Suporte
- 💬 **WhatsApp:** 11 96856-6334
- 🌐 **Site:** telenordeste.com.br

---

## ⏱️ CHECKLIST RÁPIDO

```
□ pip install -r requirements.txt
□ Criar integração Notion
□ Copiar token Notion
□ Conectar ao database
□ Copiar Database ID
□ Adicionar ao config.json (seção notion)
□ Criar projeto Google Cloud
□ Ativar Calendar API
□ Criar credenciais OAuth
□ Baixar credentials.json
□ Colocar na pasta do projeto
□ python verificar_status.py (verificar tudo)
□ python main.py (executar)
□ Opção 1: Testar conexões
□ Opção 2: Dry Run
□ Opção 3: Sincronizar! 🚀
```

---

## 🎉 PRONTO!

Após seguir esses 3 passos simples, seu sistema estará **100% operacional**!

```
     ANTES                    DEPOIS
       
    📋 Notion            📋 Notion
       │                    │
       │                    │ Sincronização
       ✗                    │ Automática
                            ↓
    📅 Calendar          📅 Calendar
    (vazio)              (atualizado)
```

---

**Tempo estimado:** 15-20 minutos  
**Dificuldade:** 😊 Fácil  
**Resultado:** 🚀 Sistema profissional completo!

---

**Criado por:** Luna AI Assistant  
**Data:** 23/10/2025  
**Versão:** 1.0
