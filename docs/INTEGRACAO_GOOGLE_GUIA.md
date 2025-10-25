# 📧 GUIA DE INTEGRAÇÃO GOOGLE (GMAIL + CALENDAR) - LUNA V3

> **Integração oficial via API do Google**
> Acesso direto, rápido e eficiente ao Gmail e Google Calendar sem precisar de navegador Playwright.

---

## 📑 ÍNDICE

1. [Visão Geral](#visão-geral)
2. [Configuração Inicial](#configuração-inicial)
3. [Instalação de Dependências](#instalação-de-dependências)
4. [Primeiros Passos](#primeiros-passos)
5. [Gmail - Funcionalidades](#gmail---funcionalidades)
6. [Google Calendar - Funcionalidades](#google-calendar---funcionalidades)
7. [Exemplos Práticos](#exemplos-práticos)
8. [Troubleshooting](#troubleshooting)
9. [Referência Completa](#referência-completa)

---

## 🎯 VISÃO GERAL

### O que é?
Integração SDK direta com Gmail e Google Calendar usando as APIs oficiais do Google. Permite ao Luna gerenciar emails e eventos de forma programática.

### Vantagens vs Playwright
| Critério | Integração SDK | Playwright |
|----------|----------------|------------|
| **Velocidade** | <1s por operação | 10-30s por operação |
| **Confiabilidade** | ⭐⭐⭐⭐⭐ (API estável) | ⭐⭐⭐ (UI pode mudar) |
| **Uso de memória** | <10MB | 500MB+ (navegador) |
| **Headless** | ✅ Nativo | ✅ Possível |
| **Rate limits** | API limits claros | Pode ser detectado |
| **Autenticação** | OAuth2 oficial | Login manual |

### Funcionalidades Implementadas

**Gmail (8 métodos):**
- ✅ Conectar via OAuth2
- ✅ Listar emails com filtros avançados
- ✅ Ler conteúdo completo (texto + HTML)
- ✅ Enviar emails (texto e HTML)
- ✅ Marcar como lido/não lido
- ✅ Deletar emails (lixeira ou permanente)
- ✅ Arquivar emails
- ✅ Buscar com query do Gmail

**Google Calendar (6 métodos):**
- ✅ Conectar via OAuth2
- ✅ Listar eventos com filtros
- ✅ Criar eventos (simples e recorrentes)
- ✅ Atualizar eventos existentes
- ✅ Deletar eventos
- ✅ Buscar eventos por texto

---

## ⚙️ CONFIGURAÇÃO INICIAL

### 1. Criar Projeto no Google Cloud Console

1. Acesse: https://console.cloud.google.com/
2. Crie um novo projeto ou selecione um existente
3. Navegue para **APIs & Services** > **Enable APIs and Services**
4. Ative as seguintes APIs:
   - **Gmail API**
   - **Google Calendar API**

### 2. Criar Credenciais OAuth 2.0

1. Vá para **APIs & Services** > **Credentials**
2. Clique em **Create Credentials** > **OAuth client ID**
3. Configure a tela de consentimento (OAuth consent screen):
   - User Type: **External** (para uso pessoal)
   - App name: `Luna V3`
   - User support email: seu email
   - Developer contact: seu email
   - Scopes: Adicionar os escopos necessários
     - Gmail: `https://www.googleapis.com/auth/gmail.modify`
     - Calendar: `https://www.googleapis.com/auth/calendar`
4. Tipo de aplicativo: **Desktop app**
5. Nome: `Luna Desktop Client`
6. Baixe o arquivo JSON de credenciais

### 3. Configurar Credenciais no Luna

**Opção 1: Arquivo direto**
```bash
# Salvar credentials.json na pasta do Luna
mv ~/Downloads/client_secret_*.json /caminho/para/Luna/credentials.json
```

**Opção 2: Armazenar no cofre do Luna (RECOMENDADO)**
```python
# Usar o cofre de credenciais do Luna
from cofre_credenciais import CofreCredenciais

cofre = CofreCredenciais()
cofre.adicionar(
    servico="google_oauth",
    usuario="meu_email@gmail.com",
    senha=json.dumps(credentials_dict)  # Conteúdo do JSON
)
```

---

## 📦 INSTALAÇÃO DE DEPENDÊNCIAS

### Instalar bibliotecas do Google

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Verificar instalação

```bash
python -c "from integracao_google import GOOGLE_DISPONIVEL; print('✅ OK' if GOOGLE_DISPONIVEL else '❌ ERRO')"
```

---

## 🚀 PRIMEIROS PASSOS

### Primeira Execução (Autenticação)

```python
from integracao_google import IntegracaoGmail, IntegracaoGoogleCalendar

# ===== GMAIL =====
# Primeira vez: abrirá navegador para autorização
gmail = IntegracaoGmail(credentials_path="credentials.json")
# Após autorização, salva token em "token_gmail.json"

# ===== GOOGLE CALENDAR =====
# Primeira vez: abrirá navegador para autorização
calendar = IntegracaoGoogleCalendar(credentials_path="credentials.json")
# Após autorização, salva token em "token_calendar.json"
```

**O que acontece:**
1. Navegador abre automaticamente
2. Você faz login na sua conta Google
3. Autoriza o aplicativo Luna
4. Token é salvo localmente
5. Próximas execuções usam o token automaticamente

### Execuções Seguintes (Automático)

```python
# Usa token salvo, não pede autorização novamente
gmail = IntegracaoGmail(token_path="token_gmail.json")
calendar = IntegracaoGoogleCalendar(token_path="token_calendar.json")
```

---

## 📧 GMAIL - FUNCIONALIDADES

### 1. Listar Emails

```python
gmail = IntegracaoGmail(token_path="token_gmail.json")

# Listar 10 emails mais recentes
emails = gmail.listar_emails(max_results=10)

# Apenas emails não lidos
emails_nao_lidos = gmail.listar_emails(
    max_results=20,
    apenas_nao_lidos=True
)

# Filtrar por remetente
emails_do_joao = gmail.listar_emails(
    remetente="joao@example.com",
    max_results=50
)

# Filtrar por assunto
emails_reuniao = gmail.listar_emails(
    assunto="reunião",
    max_results=10
)

# Filtrar por data
emails_recentes = gmail.listar_emails(
    depois_de="2025/10/01",
    antes_de="2025/10/31",
    max_results=100
)

# Query avançada (sintaxe Gmail)
emails_importantes = gmail.listar_emails(
    query="is:important from:chefe@example.com subject:urgente",
    max_results=5
)

# Estrutura do retorno
for email in emails:
    print(f"ID: {email['id']}")
    print(f"Remetente: {email['remetente']}")
    print(f"Assunto: {email['assunto']}")
    print(f"Data: {email['data']}")
    print(f"Preview: {email['snippet']}")
    print(f"Lido: {email['lido']}")
```

### 2. Ler Email Completo

```python
# Ler email específico pelo ID
email = gmail.ler_email(email_id="abc123xyz")

# Dados completos disponíveis
print(f"Remetente: {email['remetente']}")
print(f"Destinatário: {email['destinatario']}")
print(f"Assunto: {email['assunto']}")
print(f"Data: {email['data']}")
print(f"Corpo texto: {email['corpo_texto']}")
print(f"Corpo HTML: {email['corpo_html']}")
print(f"Labels: {email['labels']}")
print(f"Thread ID: {email['thread_id']}")
```

### 3. Enviar Email

```python
# Email simples (texto)
gmail.enviar_email(
    destinatario="exemplo@gmail.com",
    assunto="Relatório Semanal",
    corpo="Segue anexo o relatório da semana."
)

# Email HTML
gmail.enviar_email(
    destinatario="cliente@example.com",
    assunto="Proposta Comercial",
    corpo="""
    <html>
        <body>
            <h1>Proposta Comercial</h1>
            <p>Prezado cliente,</p>
            <p>Segue nossa proposta:</p>
            <ul>
                <li>Item 1: R$ 100</li>
                <li>Item 2: R$ 200</li>
            </ul>
            <p><strong>Total: R$ 300</strong></p>
        </body>
    </html>
    """,
    html=True
)

# Email com cópia
gmail.enviar_email(
    destinatario="principal@example.com",
    assunto="Reunião de Alinhamento",
    corpo="Confirma presença?",
    cc=["pessoa1@example.com", "pessoa2@example.com"],
    bcc=["observador@example.com"]
)
```

### 4. Gerenciar Status de Emails

```python
# Marcar como lido
gmail.marcar_como_lido(email_id="abc123")

# Marcar como não lido
gmail.marcar_como_nao_lido(email_id="xyz789")

# Arquivar (remover da inbox)
gmail.arquivar_email(email_id="def456")

# Deletar (mover para lixeira)
gmail.deletar_email(email_id="ghi789", permanente=False)

# Deletar permanentemente
gmail.deletar_email(email_id="jkl012", permanente=True)
```

---

## 📅 GOOGLE CALENDAR - FUNCIONALIDADES

### 1. Listar Eventos

```python
calendar = IntegracaoGoogleCalendar(token_path="token_calendar.json")

# Próximos 10 eventos
eventos = calendar.listar_eventos(max_results=10)

# Eventos de um período específico
eventos_mes = calendar.listar_eventos(
    time_min="2025-10-01T00:00:00Z",
    time_max="2025-10-31T23:59:59Z",
    max_results=100
)

# Buscar por texto
eventos_reuniao = calendar.listar_eventos(
    query="reunião",
    max_results=20
)

# Incluir eventos passados
eventos_todos = calendar.listar_eventos(
    max_results=50,
    apenas_futuros=False
)

# Estrutura do retorno
for evento in eventos:
    print(f"ID: {evento['id']}")
    print(f"Título: {evento['titulo']}")
    print(f"Início: {evento['inicio']}")
    print(f"Fim: {evento['fim']}")
    print(f"Descrição: {evento['descricao']}")
    print(f"Local: {evento['localizacao']}")
    print(f"Participantes: {evento['participantes']}")
    print(f"Link Meet: {evento['link_meet']}")
    print(f"Dia inteiro: {evento['dia_inteiro']}")
```

### 2. Criar Evento

```python
# Evento simples
evento_id = calendar.criar_evento(
    titulo="Reunião com Cliente",
    inicio="2025-10-20T14:00:00",
    fim="2025-10-20T15:00:00",
    descricao="Discussão sobre o projeto X",
    localizacao="Sala de Reuniões 3"
)

# Evento com participantes
calendar.criar_evento(
    titulo="Planning Semanal",
    inicio="2025-10-21T10:00:00",
    fim="2025-10-21T11:00:00",
    descricao="Planejamento da sprint",
    participantes=[
        "dev1@example.com",
        "dev2@example.com",
        "manager@example.com"
    ],
    lembrete_minutos=[10, 30]  # Lembrete 10min e 30min antes
)

# Evento de dia inteiro
calendar.criar_evento(
    titulo="Férias",
    inicio="2025-12-20",
    fim="2025-12-31",
    dia_inteiro=True
)

# Evento recorrente (toda segunda-feira às 10h por 10 semanas)
calendar.criar_evento(
    titulo="Reunião Semanal",
    inicio="2025-10-20T10:00:00",
    fim="2025-10-20T11:00:00",
    descricao="Alinhamento semanal da equipe",
    recorrencia=["RRULE:FREQ=WEEKLY;BYDAY=MO;COUNT=10"]
)

# Evento recorrente (todo dia útil por 1 mês)
calendar.criar_evento(
    titulo="Daily Standup",
    inicio="2025-10-20T09:00:00",
    fim="2025-10-20T09:15:00",
    recorrencia=["RRULE:FREQ=DAILY;BYDAY=MO,TU,WE,TH,FR;UNTIL=20251120T090000Z"]
)
```

### 3. Atualizar Evento

```python
# Atualizar título e horário
calendar.atualizar_evento(
    evento_id="abc123xyz",
    titulo="Reunião Remarcada",
    inicio="2025-10-20T15:00:00",
    fim="2025-10-20T16:00:00"
)

# Atualizar apenas descrição
calendar.atualizar_evento(
    evento_id="def456",
    descricao="Atualização: Trazer laptop"
)

# Atualizar local
calendar.atualizar_evento(
    evento_id="ghi789",
    localizacao="Online - Google Meet"
)
```

### 4. Deletar Evento

```python
# Deletar evento
calendar.deletar_evento(evento_id="abc123xyz")

# Deletar de calendário específico
calendar.deletar_evento(
    evento_id="def456",
    calendar_id="outro_calendario@group.calendar.google.com"
)
```

### 5. Buscar Eventos

```python
# Buscar por palavra-chave
eventos_projeto_x = calendar.buscar_eventos(
    texto="Projeto X",
    max_results=20
)

# Buscar em todos os eventos (passados e futuros)
todos_eventos_reuniao = calendar.buscar_eventos(
    texto="reunião",
    max_results=100
)
```

---

## 💡 EXEMPLOS PRÁTICOS

### Exemplo 1: Monitor de Emails Importantes

```python
from integracao_google import IntegracaoGmail
import time

gmail = IntegracaoGmail(token_path="token_gmail.json")

def monitorar_emails_importantes():
    """Monitora emails importantes e envia notificação"""
    emails = gmail.listar_emails(
        query="is:important is:unread",
        max_results=5
    )

    if emails:
        print(f"⚠️  {len(emails)} emails importantes não lidos:")
        for email in emails:
            print(f"\n📧 De: {email['remetente']}")
            print(f"   Assunto: {email['assunto']}")
            print(f"   Preview: {email['snippet']}")

        return emails
    else:
        print("✅ Nenhum email importante pendente")
        return []

# Executar a cada 5 minutos
while True:
    monitorar_emails_importantes()
    time.sleep(300)  # 5 minutos
```

### Exemplo 2: Responder Email Automaticamente

```python
from integracao_google import IntegracaoGmail

gmail = IntegracaoGmail(token_path="token_gmail.json")

def responder_email_automatico():
    """Responde emails de confirmação automaticamente"""
    # Buscar emails com assunto "Confirma presença"
    emails = gmail.listar_emails(
        assunto="Confirma presença",
        apenas_nao_lidos=True,
        max_results=10
    )

    for email in emails:
        # Extrair remetente
        remetente = email['remetente']

        # Enviar confirmação
        gmail.enviar_email(
            destinatario=remetente,
            assunto=f"Re: {email['assunto']}",
            corpo="Confirmo minha presença. Até lá!\n\n--\nEnviado automaticamente pelo Luna"
        )

        # Marcar original como lido e arquivar
        gmail.marcar_como_lido(email['id'])
        gmail.arquivar_email(email['id'])

        print(f"✅ Respondido: {email['assunto']}")

responder_email_automatico()
```

### Exemplo 3: Criar Reuniões Automáticas

```python
from integracao_google import IntegracaoGoogleCalendar
from datetime import datetime, timedelta

calendar = IntegracaoGoogleCalendar(token_path="token_calendar.json")

def criar_reunioes_semanais(equipe):
    """Cria reuniões semanais automáticas para os próximos 3 meses"""
    # Data inicial: próxima segunda-feira às 10h
    hoje = datetime.now()
    dias_ate_segunda = (7 - hoje.weekday()) % 7
    proxima_segunda = hoje + timedelta(days=dias_ate_segunda)
    proxima_segunda = proxima_segunda.replace(hour=10, minute=0, second=0)

    # Data final: 3 meses depois
    data_final = proxima_segunda + timedelta(weeks=12)

    evento_id = calendar.criar_evento(
        titulo="Reunião Semanal de Equipe",
        inicio=proxima_segunda.isoformat(),
        fim=(proxima_segunda + timedelta(hours=1)).isoformat(),
        descricao="Alinhamento semanal da equipe",
        participantes=equipe,
        recorrencia=[
            f"RRULE:FREQ=WEEKLY;BYDAY=MO;UNTIL={data_final.strftime('%Y%m%dT%H%M%SZ')}"
        ],
        lembrete_minutos=[10, 60]
    )

    print(f"✅ Reuniões semanais criadas até {data_final.strftime('%Y-%m-%d')}")
    return evento_id

# Criar para equipe
equipe = [
    "dev1@example.com",
    "dev2@example.com",
    "manager@example.com"
]
criar_reunioes_semanais(equipe)
```

### Exemplo 4: Sincronizar Agenda com Notion

```python
from integracao_google import IntegracaoGoogleCalendar
from integracao_notion import IntegracaoNotion

calendar = IntegracaoGoogleCalendar(token_path="token_calendar.json")
notion = IntegracaoNotion(token="seu_token_notion")

def sincronizar_eventos_notion(database_id):
    """Sincroniza eventos do Google Calendar com database do Notion"""
    # Listar eventos dos próximos 7 dias
    hoje = datetime.now()
    fim_semana = hoje + timedelta(days=7)

    eventos = calendar.listar_eventos(
        time_min=hoje.isoformat() + 'Z',
        time_max=fim_semana.isoformat() + 'Z',
        max_results=50
    )

    for evento in eventos:
        # Criar página no Notion para cada evento
        notion.criar_pagina(
            database_id=database_id,
            propriedades={
                "Título": criar_prop_titulo(evento['titulo']),
                "Data": criar_prop_data(evento['inicio'], evento['fim']),
                "Descrição": criar_prop_texto(evento['descricao']),
                "Local": criar_prop_texto(evento['localizacao']),
                "Link": criar_prop_url(evento['html_link'])
            }
        )

        print(f"✅ Sincronizado: {evento['titulo']}")

sincronizar_eventos_notion("seu_database_id_aqui")
```

---

## 🔧 TROUBLESHOOTING

### Erro: "Bibliotecas do Google não instaladas"

**Solução:**
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Erro: "Token expirado" ou "Invalid credentials"

**Causa:** Token OAuth2 expirou ou foi revogado.

**Solução:**
```bash
# Deletar tokens antigos
rm token_gmail.json
rm token_calendar.json

# Reconectar (vai abrir navegador novamente)
python -c "from integracao_google import IntegracaoGmail; IntegracaoGmail(credentials_path='credentials.json')"
```

### Erro: "API not enabled"

**Causa:** APIs do Gmail ou Calendar não foram habilitadas no Google Cloud Console.

**Solução:**
1. Acesse https://console.cloud.google.com/
2. Selecione seu projeto
3. Vá em **APIs & Services** > **Library**
4. Busque e ative:
   - Gmail API
   - Google Calendar API

### Erro: "Access denied" ou "insufficient permissions"

**Causa:** Escopos OAuth insuficientes.

**Solução:**
1. Deletar tokens: `rm token_*.json`
2. Verificar escopos no código:
   - Gmail: `https://www.googleapis.com/auth/gmail.modify`
   - Calendar: `https://www.googleapis.com/auth/calendar`
3. Reconectar para gerar novo token com escopos corretos

### Navegador não abre para autenticação

**Causa:** Ambiente headless ou sem interface gráfica.

**Solução:** Usar autenticação por código (copiar/colar URL):
```python
# Modificar temporariamente em integracao_google.py
flow.run_local_server(port=0)  # Padrão
# Trocar por:
flow.run_console()  # Mostra URL no terminal
```

### Rate limit exceeded

**Causa:** Muitas requisições em pouco tempo.

**Solução:**
- Gmail: Limite de 250 emails enviados por dia (contas gratuitas)
- Calendar: 1.000.000 requisições por dia
- Adicionar delays entre operações:
```python
import time
for email in emails:
    # processar email
    time.sleep(0.1)  # 100ms entre requisições
```

---

## 📚 REFERÊNCIA COMPLETA

### IntegracaoGmail

**Métodos disponíveis:**

| Método | Descrição | Retorno |
|--------|-----------|---------|
| `listar_emails(...)` | Lista emails com filtros | `List[Dict]` |
| `ler_email(email_id)` | Lê email completo | `Dict` |
| `enviar_email(...)` | Envia email | `str` (ID do email) |
| `marcar_como_lido(email_id)` | Marca email como lido | `bool` |
| `marcar_como_nao_lido(email_id)` | Marca email como não lido | `bool` |
| `deletar_email(email_id, permanente)` | Deleta email | `bool` |
| `arquivar_email(email_id)` | Arquiva email | `bool` |

**Estrutura de email retornado:**
```python
{
    'id': str,
    'thread_id': str,
    'remetente': str,
    'destinatario': str,
    'assunto': str,
    'data': str,
    'corpo_texto': str,
    'corpo_html': str,
    'snippet': str,  # Preview de 100 caracteres
    'labels': List[str],
    'lido': bool,
    'importante': bool,
    'interno_data': str  # Timestamp em milliseconds
}
```

### IntegracaoGoogleCalendar

**Métodos disponíveis:**

| Método | Descrição | Retorno |
|--------|-----------|---------|
| `listar_eventos(...)` | Lista eventos com filtros | `List[Dict]` |
| `criar_evento(...)` | Cria novo evento | `str` (ID do evento) |
| `atualizar_evento(...)` | Atualiza evento existente | `bool` |
| `deletar_evento(evento_id)` | Deleta evento | `bool` |
| `buscar_eventos(texto)` | Busca eventos por texto | `List[Dict]` |

**Estrutura de evento retornado:**
```python
{
    'id': str,
    'titulo': str,
    'descricao': str,
    'localizacao': str,
    'inicio': str,  # ISO 8601
    'fim': str,  # ISO 8601
    'dia_inteiro': bool,
    'criador': str,
    'organizador': str,
    'participantes': List[Dict],
    'link_meet': str,
    'status': str,
    'html_link': str,
    'recorrente': bool,
    'recorrencia': List[str],
    'criado_em': str,
    'atualizado_em': str
}
```

### Formatos de Data/Hora

**ISO 8601 (eventos com hora específica):**
```python
"2025-10-20T14:30:00"  # 20 out 2025 às 14h30
```

**Data simples (eventos de dia inteiro):**
```python
"2025-10-20"  # 20 out 2025
```

**Com timezone:**
```python
"2025-10-20T14:30:00-03:00"  # Brasília
"2025-10-20T14:30:00Z"        # UTC
```

### Regras de Recorrência (RRULE)

**Exemplos comuns:**

```python
# Todo dia por 10 dias
["RRULE:FREQ=DAILY;COUNT=10"]

# Toda semana às segundas por 3 meses
["RRULE:FREQ=WEEKLY;BYDAY=MO;UNTIL=20251220T000000Z"]

# Todo mês no dia 15 por 12 meses
["RRULE:FREQ=MONTHLY;BYMONTHDAY=15;COUNT=12"]

# Dias úteis (seg-sex) por tempo indeterminado
["RRULE:FREQ=DAILY;BYDAY=MO,TU,WE,TH,FR"]

# Primeira segunda-feira de cada mês
["RRULE:FREQ=MONTHLY;BYDAY=1MO"]
```

---

## 🎯 COMPARAÇÃO COM NOTION

| Aspecto | Google (Gmail + Calendar) | Notion |
|---------|--------------------------|--------|
| **Autenticação** | OAuth2 (navegador 1x) | Token API direto |
| **Setup inicial** | Mais complexo | Simples |
| **Renovação de token** | Automática | Não expira |
| **Escopos** | Granulares (Gmail, Calendar separados) | Único (workspace) |
| **Rate limits** | Generosos (1M+ req/dia) | Moderados |
| **Dados estruturados** | JSON complexo | JSON simples |
| **Webhooks** | Disponível (Push notifications) | Não oficial |

---

## ✅ CHECKLIST DE SETUP

- [ ] Criar projeto no Google Cloud Console
- [ ] Ativar Gmail API
- [ ] Ativar Google Calendar API
- [ ] Criar credenciais OAuth 2.0
- [ ] Baixar arquivo credentials.json
- [ ] Instalar dependências Python
- [ ] Testar conexão Gmail
- [ ] Testar conexão Calendar
- [ ] Salvar tokens de acesso
- [ ] (Opcional) Armazenar credentials no cofre do Luna

---

## 📞 SUPORTE

- **Documentação oficial Gmail API:** https://developers.google.com/gmail/api
- **Documentação oficial Calendar API:** https://developers.google.com/calendar/api
- **Python Google Client:** https://github.com/googleapis/google-api-python-client
- **OAuth 2.0 para aplicações desktop:** https://developers.google.com/identity/protocols/oauth2/native-app

---

**Versão:** 1.0
**Autor:** Sistema Luna
**Data:** 2025-10-19
