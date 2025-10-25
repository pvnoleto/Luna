# 🏥 Agendador TeleNordeste - Versão Refatorada

Sistema automatizado de agendamento médico com integração completa entre Notion, Google Calendar e automação web.

## 🚀 Melhorias desta Versão

### ✨ Principais Mudanças

1. **Segurança Aprimorada**
   - ✅ Credenciais movidas para `.env` (não commitadas no git)
   - ✅ Proteção contra vazamento de tokens
   - ✅ Arquivo `.env.example` para referência

2. **Arquitetura Modular**
   - ✅ Código organizado em classes especializadas
   - ✅ Separação de responsabilidades (SRP)
   - ✅ Fácil manutenção e extensão
   - ✅ Type hints completos

3. **Configuração Flexível**
   - ✅ `config.json` para dados da UBS
   - ✅ Timeouts configuráveis
   - ✅ Especialidades mapeadas
   - ✅ Horários válidos centralizados

4. **Logging Profissional**
   - ✅ Logs salvos em arquivo (`agendador.log`)
   - ✅ Níveis de log (INFO, WARNING, ERROR)
   - ✅ Timestamps completos
   - ✅ Auditoria completa

5. **Performance Otimizada**
   - ✅ Uso de `wait_for_selector` quando possível
   - ✅ Timeouts configuráveis
   - ✅ Código mais eficiente

## 📋 Pré-requisitos

### Dependências Python

```bash
pip install python-dotenv playwright notion-client
pip install google-auth google-auth-oauthlib google-api-python-client
playwright install chromium
```

### Arquivos Necessários

1. **`.env`** - Credenciais (criar a partir de `.env.example`)
2. **`config.json`** - Configurações (já incluído)
3. **`../../integracao_google.py`** - Módulo Google Calendar da Luna
4. **`../../credentials.json`** - Credenciais OAuth2 do Google (opcional)

## 🔧 Configuração Inicial

### 1. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env com suas credenciais
nano .env
```

Preencha:
- `NOTION_TOKEN` - Token da integração Notion
- `NOTION_DATABASE_ID` - ID do banco de dados
- `DRY_RUN` - `true` para teste, `false` para produção
- `USAR_GOOGLE_CALENDAR` - `true` para integrar com Calendar

### 2. Configurar config.json (Opcional)

Edite `config.json` para ajustar:
- Dados da UBS (email, telefone, CNES)
- URLs das agendas
- Horários válidos
- Timeouts
- Especialidades

### 3. Configurar Google Calendar (Opcional)

Se `USAR_GOOGLE_CALENDAR=true`:

1. Criar projeto no Google Cloud Console
2. Ativar Google Calendar API
3. Criar credenciais OAuth 2.0 (Desktop app)
4. Baixar `credentials.json` para pasta raiz da Luna
5. Na primeira execução, autorizar acesso (abre navegador)

## 🎯 Como Usar

### Modo Teste (DRY RUN)

```bash
# Configurar em .env
DRY_RUN=true

# Executar
python agendador_refatorado.py
```

**Comportamento:**
- ✅ Busca tarefas reais do Notion
- ✅ Navega e testa seletores
- ✅ Simula agendamento
- ❌ NÃO efetiva reserva
- ✅ Cria eventos no Calendar (se ativado)
- ❌ NÃO atualiza status no Notion

### Modo Produção

```bash
# Configurar em .env
DRY_RUN=false

# Executar
python agendador_refatorado.py
```

**Comportamento:**
- ✅ Busca tarefas reais
- ✅ Agenda automaticamente
- ✅ Clica em "Reservar"
- ✅ Cria eventos no Calendar
- ✅ Atualiza status para "Concluída"

## 📊 Estrutura do Código

```
agendador_refatorado.py
├── ConfigManager          # Gerencia .env e config.json
├── AgendadorLogger        # Sistema de logs (arquivo + console)
├── NotionManager          # Operações com Notion API
├── CalendarManager        # Operações com Google Calendar
├── AgendadorWeb           # Automação web (Playwright)
└── AgendadorTeleNE        # Orquestrador principal
```

### Classes Principais

#### ConfigManager
- Carrega `.env` e `config.json`
- Fornece configurações para outros módulos
- Valida especialidades infantis

#### AgendadorLogger
- Logs em arquivo (`agendador.log`)
- Logs coloridos no console
- Níveis: info, sucesso, erro, aviso

#### NotionManager
- Conecta à API do Notion
- Busca tarefas "Não iniciado"
- Parseia dados das tarefas
- Atualiza status

#### CalendarManager
- Conecta ao Google Calendar
- Verifica disponibilidade de horários
- Cria eventos com lembretes

#### AgendadorWeb
- Navega para agendas (Infantil/Adulto)
- Seleciona especialidades (detecção inteligente)
- Busca horários disponíveis
- Preenche formulário
- Confirma agendamento

#### AgendadorTeleNE
- Orquestra todo o processo
- Gerencia ciclo de vida
- Gera relatórios

## 🔍 Funcionalidades

### Detecção Inteligente de Especialidades

O sistema busca especialidades com múltiplas estratégias:

1. **Mapeamento de variações** (config.json)
   - "neurologia" → ["neurologia", "neuro", "neurologista"]
   - "psiquiatria infantil" → ["psiquiatria infantil", "psiquiatria pediátrica"]

2. **Busca em 3 níveis**
   - Texto exato (case-insensitive)
   - Contém texto
   - Botões/links/divs

### Verificação Google Calendar

Antes de agendar, verifica se horário está livre:
- ✅ Busca eventos no período
- ✅ Mostra conflitos
- ✅ Pula horários ocupados
- ✅ Garante sem sobreposição

### Sistema de Logs

```
2025-10-23 14:30:15 [INFO] 🔍 Buscando tarefas 'Não Iniciadas' no Notion...
2025-10-23 14:30:16 [INFO] SUCESSO: Encontradas 3 tarefas para processar
2025-10-23 14:30:17 [INFO] 🧭 Navegando para Agenda Adulto...
2025-10-23 14:30:25 [INFO] SUCESSO: Navegação bem-sucedida!
...
```

**Logs salvos em:** `agendador.log`

## 📈 Relatório de Execução

Ao final, exibe:

```
📊 RELATÓRIO FINAL
============================================================
✅ Sucessos: 2
❌ Erros: 1
📋 Total: 3
📈 Taxa de sucesso: 66.7%

🎉 2 agendamento(s) realizado(s)!

============================================================
🔧 CONFIGURAÇÕES:
   • Modo: DRY RUN (Teste)
   • Calendar: Ativado
   • Timezone: America/Fortaleza
============================================================
```

## 🐛 Troubleshooting

### Erro: "NOTION_TOKEN not found"
**Solução:** Verifique se `.env` existe e está preenchido

### Erro: "Arquivo de configuração não encontrado"
**Solução:** Certifique-se de que `config.json` está no mesmo diretório

### Erro: "Especialidade não encontrada"
**Solução:** 
1. Verifique o nome exato no site
2. Adicione variação em `config.json` → `especialidades`

### Erro: "Google Calendar: Invalid credentials"
**Solução:**
1. Verifique `credentials.json` na raiz da Luna
2. Delete `token_calendar.json` para re-autenticar
3. Execute novamente

### Navegador não abre
**Solução:** Sistema detecta sandbox automaticamente
- **Sandbox:** Executa headless
- **Local:** Executa com GUI

## 🔒 Segurança

### Arquivos Sensíveis

**NUNCA commitar:**
- `.env` (credenciais)
- `token_calendar.json` (token OAuth)
- `agendador.log` (pode conter dados sensíveis)

**Adicionar ao `.gitignore`:**
```
.env
token_*.json
agendador.log
```

**Pode commitar:**
- `.env.example` (sem credenciais reais)
- `config.json` (sem dados sensíveis)
- `agendador_refatorado.py` (código)

## 📝 Comparação: Original vs Refatorado

| Aspecto | Original | Refatorado |
|---------|----------|------------|
| **Linhas de código** | 1131 | ~1100 (modular) |
| **Credenciais** | Hardcoded | .env |
| **Configurações** | Hardcoded | config.json |
| **Logging** | Console | Arquivo + Console |
| **Type hints** | Parcial | Completo |
| **Classes** | 0 | 6 especializadas |
| **Timeouts** | Fixos | Configuráveis |
| **Imports duplicados** | Sim | Não |
| **Maior função** | 192 linhas | <100 linhas |
| **Manutenibilidade** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🎯 Próximos Passos

Após validar o script refatorado:

1. **Testar em modo DRY_RUN**
   ```bash
   python agendador_refatorado.py
   ```

2. **Verificar logs**
   ```bash
   tail -f agendador.log
   ```

3. **Validar com tarefa real (DRY_RUN)**
   - Cria tarefa no Notion
   - Executa script
   - Verifica que NÃO agendou

4. **Ativar produção**
   ```bash
   # Em .env
   DRY_RUN=false
   ```

5. **Usar como baseline para Luna**
   - Pedir à Luna para criar agendador similar
   - Comparar qualidade do código gerado

## 📞 Suporte

Para dúvidas ou problemas:
1. Verificar logs em `agendador.log`
2. Consultar este README
3. Revisar configurações em `.env` e `config.json`

---

**Desenvolvido com ❤️ para automação médica**  
**Versão Refatorada:** Production-ready com best practices
