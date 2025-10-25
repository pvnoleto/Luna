# 🔐 GUIA INTERATIVO - CONFIGURAÇÃO DE CREDENCIAIS

**Workspace:** telenordeste_integration
**Onda:** 2 - Configuração de Credenciais
**Status:** AGUARDANDO AÇÃO DO USUÁRIO

---

## ⚠️ IMPORTANTE - LEIA COM ATENÇÃO

Este guia irá ajudá-lo a configurar as credenciais necessárias para o funcionamento do sistema TeleNordeste Integration.

**Tempo Estimado:** 15-20 minutos

---

## 📋 CHECKLIST DE CONFIGURAÇÃO

### Fase 1: Notion API (5-10 minutos)
- [ ] Acessar https://www.notion.so/my-integrations
- [ ] Criar nova integração "TeleNordeste Calendar Sync"
- [ ] Copiar Integration Token
- [ ] Conectar integração ao seu database
- [ ] Copiar Database ID
- [ ] Atualizar config.json

### Fase 2: Google Calendar API (10-15 minutos)
- [ ] Acessar https://console.cloud.google.com/
- [ ] Criar projeto "TeleNordeste Integration"
- [ ] Ativar Google Calendar API
- [ ] Criar credenciais OAuth 2.0 (Desktop App)
- [ ] Baixar credentials.json
- [ ] Salvar na pasta do workspace

### Fase 3: Validação (2 minutos)
- [ ] Executar script de verificação
- [ ] Confirmar todas as credenciais

---

## 🎯 PASSO A PASSO DETALHADO

### PARTE 1: CONFIGURAR NOTION API

#### Passo 1: Acessar o Portal de Integrações
1. Abra seu navegador
2. Acesse: **https://www.notion.so/my-integrations**
3. Faça login com sua conta Notion (se necessário)

#### Passo 2: Criar Nova Integração
1. Clique no botão **"+ New integration"**
2. Preencha os campos:
   - **Name:** TeleNordeste Calendar Sync
   - **Associated workspace:** Selecione seu workspace
   - **Logo:** (Opcional)
3. Clique em **"Submit"**

#### Passo 3: Copiar o Integration Token
1. Na página da integração criada, você verá:
   - **Internal Integration Token**
2. Clique em **"Show"** e depois em **"Copy"**
3. ⚠️ **IMPORTANTE:** Guarde este token em segurança!
   - Formato: `secret_XXXXXXXXXXXXXXXXXXXXXXXXXXXXX`

#### Passo 4: Conectar Integração ao Database
1. Abra seu database no Notion (onde estão as tarefas)
2. Clique nos **3 pontos** (⋯) no canto superior direito
3. Selecione **"Add connections"**
4. Busque e selecione **"TeleNordeste Calendar Sync"**
5. Clique em **"Confirm"**

#### Passo 5: Copiar Database ID
1. Com o database aberto, olhe a URL do navegador:
   ```
   https://www.notion.so/workspace/DATABASE_ID?v=...
   ```
2. O **DATABASE_ID** é a sequência entre o nome do workspace e o `?v=`
3. Exemplo:
   ```
   URL: https://www.notion.so/myworkspace/a1b2c3d4e5f6...?v=xyz
   DATABASE_ID: a1b2c3d4e5f6...
   ```
4. Copie este ID

#### Passo 6: Atualizar config.json
1. Abra o arquivo **config.json** no workspace
2. Adicione a seção "notion" (ou edite se já existir):
   ```json
   {
     "notion": {
       "token": "secret_SEU_TOKEN_AQUI",
       "database_id": "SEU_DATABASE_ID_AQUI"
     },
     ... (resto do arquivo)
   }
   ```
3. Substitua os valores pelos que você copiou
4. Salve o arquivo

✅ **NOTION CONFIGURADO!**

---

### PARTE 2: CONFIGURAR GOOGLE CALENDAR API

#### Passo 1: Acessar Google Cloud Console
1. Abra seu navegador
2. Acesse: **https://console.cloud.google.com/**
3. Faça login com sua conta Google

#### Passo 2: Criar Novo Projeto
1. No topo da página, clique no **seletor de projetos**
2. Clique em **"NEW PROJECT"**
3. Preencha:
   - **Project name:** TeleNordeste Integration
   - **Location:** (deixe padrão ou escolha organização)
4. Clique em **"CREATE"**
5. Aguarde a criação (alguns segundos)
6. Selecione o projeto criado

#### Passo 3: Ativar Google Calendar API
1. No menu lateral, vá em: **APIs & Services** → **Library**
2. Na busca, digite: **"Google Calendar API"**
3. Clique no resultado **"Google Calendar API"**
4. Clique no botão **"ENABLE"**
5. Aguarde a ativação

#### Passo 4: Configurar OAuth Consent Screen (se necessário)
1. Vá em: **APIs & Services** → **OAuth consent screen**
2. Se aparecer a tela de configuração:
   - **User Type:** External
   - Clique em **"CREATE"**
3. Preencha o formulário:
   - **App name:** TeleNordeste Integration
   - **User support email:** seu_email@gmail.com
   - **Developer contact:** seu_email@gmail.com
4. Clique em **"SAVE AND CONTINUE"**
5. Em **"Scopes"**, clique em **"SAVE AND CONTINUE"** (sem adicionar)
6. Em **"Test users"**, adicione seu email e clique em **"SAVE AND CONTINUE"**
7. Clique em **"BACK TO DASHBOARD"**

#### Passo 5: Criar Credenciais OAuth 2.0
1. Vá em: **APIs & Services** → **Credentials**
2. Clique em **"+ CREATE CREDENTIALS"**
3. Selecione: **"OAuth client ID"**
4. Se pedir para configurar OAuth consent screen, siga o Passo 4
5. Preencha:
   - **Application type:** Desktop app
   - **Name:** TeleNordeste Desktop
6. Clique em **"CREATE"**
7. Na janela de confirmação, clique em **"DOWNLOAD JSON"**

#### Passo 6: Salvar credentials.json
1. O arquivo JSON será baixado (geralmente chamado `client_secret_XXXXX.json`)
2. Renomeie o arquivo para: **credentials.json**
3. Mova o arquivo para a pasta do workspace:
   ```
   workspaces/telenordeste_integration/credentials.json
   ```

✅ **GOOGLE CALENDAR CONFIGURADO!**

---

### PARTE 3: VALIDAR CONFIGURAÇÕES

#### Executar Script de Verificação
1. Abra o terminal na pasta do workspace
2. Execute:
   ```bash
   python verificar_status.py
   ```
3. Verifique os resultados:
   - ✅ Notion Token configurado
   - ✅ Notion Database ID configurado
   - ✅ credentials.json encontrado

#### Se houver erros:
- **Notion Token inválido:** Verifique se copiou corretamente e se começa com "secret_"
- **Database ID inválido:** Verifique a URL do database
- **credentials.json não encontrado:** Confirme que está na pasta correta

---

## 🎉 CONFIGURAÇÃO COMPLETA!

Após completar todos os passos acima, você terá:
- ✅ Integração Notion configurada e conectada
- ✅ Projeto Google Cloud criado
- ✅ Google Calendar API ativada
- ✅ Credenciais OAuth 2.0 configuradas
- ✅ config.json atualizado
- ✅ credentials.json salvo

---

## 🚀 PRÓXIMOS PASSOS

Após concluir a configuração:

1. **Testar Conexões:**
   ```bash
   python main.py
   ```
   Selecione: **Opção 1 - Testar Conexões**

2. **Fazer Dry Run:**
   Selecione: **Opção 2 - Sincronizar (Dry Run)**

3. **Sincronização Real:**
   Selecione: **Opção 3 - Sincronizar (Real)**

---

## 📞 PRECISA DE AJUDA?

Se encontrar problemas:

1. Consulte: **ACOES_IMEDIATAS.md**
2. Execute: `python verificar_status.py`
3. Verifique logs em: logs/ (se existir)

---

## 🔒 SEGURANÇA

⚠️ **IMPORTANTE:**
- NUNCA compartilhe seus tokens ou credentials.json
- Estes arquivos estão no .gitignore e não serão versionados
- Mantenha backups seguros das credenciais

---

**Data de Criação:** 23/10/2025
**Última Atualização:** 23/10/2025 19:45
