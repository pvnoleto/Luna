# 🚀 Quick Start - TeleNordeste Integration

**Comece em 5 minutos!**

---

## ⚡ Instalação Rápida

### Windows

```batch
# 1. Instalar dependências
install.bat

# 2. Executar programa
run.bat
```

### Linux/Mac

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar programa
python main.py
```

---

## 🔑 Obter Credenciais

### Notion (2 minutos)

1. **Integration Token**
   - Acesse: https://www.notion.so/my-integrations
   - Clique **"+ New integration"**
   - Copie o token (começa com `secret_`)

2. **Database ID**
   - Abra seu database no Notion
   - Clique **"⋮" → "Add connections"** → Escolha sua integration
   - Copie o ID da URL: `notion.so/[SEU_ID]?v=...`

### Google Calendar (3 minutos)

1. **Criar Projeto**
   - Acesse: https://console.cloud.google.com/
   - Crie novo projeto

2. **Ativar API**
   - Menu → APIs & Services → Library
   - Busque "Google Calendar API"
   - Clique "Enable"

3. **Credenciais**
   - APIs & Services → Credentials
   - "+ CREATE CREDENTIALS" → OAuth client ID
   - Application type: **Desktop app**
   - Download JSON → Salve como `credentials.json`

---

## 🎯 Primeiro Uso

```bash
python main.py
```

1. **Seguir assistente** de configuração
2. **Testar conexões** (opção 1)
3. **Dry Run** (opção 2) - teste seguro
4. **Sincronizar** (opção 3) - criar eventos reais

---

## 📋 Estrutura do Notion

Seu database precisa ter:

| Campo | Tipo | Exemplo |
|-------|------|---------|
| **Name** | Title | "Reunião com cliente" |
| **Data** | Date | 24/10/2025 14:00 |
| **Status** | Select | "A Fazer" |
| Descrição | Text | "Discutir proposta" |
| Duração | Number | 60 |

---

## 🔍 Comandos Rápidos

### Testar tudo

```bash
python main.py
# Opção 1: Testar Conexões
```

### Simulação (seguro)

```bash
python main.py
# Opção 2: Dry Run
```

### Sincronizar

```bash
python main.py
# Opção 3: Sincronizar (Real)
```

---

## 🐛 Problemas Comuns

### "Token não configurado"
→ Execute `python main.py` e siga o assistente

### "Credentials não encontrado"
→ Baixe `credentials.json` do Google e coloque na pasta

### "Database not found"
→ Compartilhe o database com sua integration no Notion

### "Access blocked"
→ Na tela de auth, clique "Advanced" → "Go to [App] (unsafe)"

---

## 📚 Próximos Passos

- ✅ [README Completo](README_COMPLETO.md) - Documentação detalhada
- ✅ [Exemplos de Uso](example_usage.py) - Uso programático
- ✅ [Configuração Avançada](#configuração-avançada)

---

## ⚙ Configuração Avançada

### Alterar timezone

```json
// config.json
{
  "sync": {
    "timezone": "America/Sao_Paulo"
  }
}
```

### Alterar campos mapeados

```json
// config.json
{
  "mapping": {
    "title_field": "Título",
    "date_field": "Quando",
    "description_field": "Notas"
  }
}
```

### Usar calendário secundário

```json
// config.json
{
  "google_calendar": {
    "calendar_id": "seu_calendar_id@group.calendar.google.com"
  }
}
```

Para obter o ID:
1. Google Calendar → Settings
2. Escolha o calendário
3. Copie "Calendar ID"

---

## 🎉 Pronto!

Agora você pode sincronizar suas tarefas automaticamente!

**Dica**: Execute primeiro em modo **Dry Run** para testar.

---

## 📞 Ajuda

- **Erros**: Veja `integration.log`
- **Dúvidas**: Consulte [README_COMPLETO.md](README_COMPLETO.md)
- **Exemplos**: Execute `python example_usage.py`

---

**Última atualização**: 23/10/2025
