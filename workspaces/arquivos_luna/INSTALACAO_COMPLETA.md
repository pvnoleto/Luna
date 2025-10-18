# 🚀 GUIA COMPLETO DE INSTALAÇÃO - DO ZERO AO USO

## 🎯 O QUE VOCÊ VAI TER

Um agente AI com **TODAS AS CAPACIDADES**:

```
✅ Auto-evolução (cria ferramentas)
✅ Computer Use (navega web visualmente)
✅ Credenciais seguras (AES-256)
✅ Memória permanente (aprende sempre)
✅ Login automático em sites
✅ Autonomia TOTAL
```

**Tempo total de instalação: 10-15 minutos**

---

## 📋 PRÉ-REQUISITOS

### **Sistema:**
- Windows, macOS ou Linux
- Python 3.9 ou superior
- 4GB RAM mínimo
- Conexão internet

### **Conta Anthropic:**
- Criar conta (grátis)
- Adicionar $10 de créditos
- Obter API Key

---

## 🎬 PASSO A PASSO COMPLETO

### **ETAPA 1: INSTALAR PYTHON (se não tiver)**

#### **Windows:**
```powershell
# Baixar de python.org/downloads
# Executar instalador
# ✅ Marcar "Add Python to PATH"
```

#### **macOS:**
```bash
# Instalar Homebrew (se não tiver)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python
brew install python@3.11
```

#### **Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**Verificar instalação:**
```bash
python --version
# Deve mostrar: Python 3.9+ ou superior
```

---

### **ETAPA 2: CRIAR CONTA ANTHROPIC**

1. **Acesse:** https://console.anthropic.com

2. **Criar conta:**
   - Click em "Sign Up"
   - Use email + senha OU Google/GitHub
   - Verificar email

3. **Adicionar créditos:**
   - Menu: "Settings" → "Billing"
   - "Add credits"
   - Adicionar $10 (recomendado inicial)
   - Cartão de crédito/débito

4. **Obter API Key:**
   - Menu: "Settings" → "API Keys"
   - "Create Key"
   - **COPIAR E GUARDAR** (aparece só uma vez!)
   - Formato: `sk-ant-api03-...`

**💡 Importante:** Guarde a API Key em local seguro!

---

### **ETAPA 3: CRIAR PASTA DO PROJETO**

```bash
# Windows (PowerShell/CMD)
mkdir C:\agente-claude
cd C:\agente-claude

# macOS/Linux
mkdir ~/agente-claude
cd ~/agente-claude
```

---

### **ETAPA 4: INSTALAR DEPENDÊNCIAS**

#### **Bibliotecas Python:**

```bash
# Bibliotecas essenciais
pip install anthropic python-dotenv

# Para Computer Use (navegação web)
pip install playwright

# Para credenciais seguras
pip install cryptography

# Instalar navegador Chromium
playwright install chromium
```

**Se der erro de permissão no Linux/macOS:**
```bash
pip install --user anthropic python-dotenv playwright cryptography
```

**Tempo estimado:** 2-5 minutos

---

### **ETAPA 5: BAIXAR ARQUIVOS DO AGENTE**

Você precisa de 4 arquivos principais:

#### **Opção A: Download manual**

Baixe estes arquivos e salve na pasta do projeto:

1. **[agente_completo_final.py](computer:///mnt/user-data/outputs/agente_completo_final.py)** (Agente principal)
2. **[cofre_credenciais.py](computer:///mnt/user-data/outputs/cofre_credenciais.py)** (Sistema de credenciais)
3. **[memoria_permanente.py](computer:///mnt/user-data/outputs/memoria_permanente.py)** (Sistema de memória)
4. **[setup_credenciais.py](computer:///mnt/user-data/outputs/setup_credenciais.py)** (Helper de setup)

#### **Opção B: Criar manualmente**

Se preferir, posso fornecer o conteúdo de cada arquivo.

---

### **ETAPA 6: CONFIGURAR API KEY**

Criar arquivo `.env` na pasta do projeto:

#### **Windows:**
```powershell
# No Bloco de Notas ou editor de texto
# Criar arquivo: .env
# Conteúdo:
ANTHROPIC_API_KEY=sk-ant-api03-SUA_CHAVE_AQUI
```

#### **macOS/Linux:**
```bash
# Criar arquivo .env
echo "ANTHROPIC_API_KEY=sk-ant-api03-SUA_CHAVE_AQUI" > .env

# OU usando nano/vim
nano .env
# Adicionar: ANTHROPIC_API_KEY=sk-ant-api03-SUA_CHAVE_AQUI
# Salvar: Ctrl+O, Enter, Ctrl+X
```

**⚠️ IMPORTANTE:**
- Substituir `SUA_CHAVE_AQUI` pela sua API key real
- Não compartilhar este arquivo
- Não commitar no git

---

### **ETAPA 7: TESTAR INSTALAÇÃO BÁSICA**

Criar arquivo de teste `teste_basico.py`:

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('ANTHROPIC_API_KEY')
client = anthropic.Anthropic(api_key=api_key)

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=100,
    messages=[{"role": "user", "content": "Diga 'Olá, estou funcionando!'"}]
)

print(response.content[0].text)
```

**Executar:**
```bash
python teste_basico.py
```

**Resultado esperado:**
```
Olá, estou funcionando!
```

✅ **Se funcionou, API configurada corretamente!**

---

### **ETAPA 8: CONFIGURAR CREDENCIAIS (OPCIONAL)**

Se você quer usar login automático em sites:

```bash
python setup_credenciais.py rapido
```

**Processo interativo:**
```
🔐 COFRE DE CREDENCIAIS

🆕 Criando novo cofre...
🔑 Crie uma Master Password: ********
🔑 Confirme a Master Password: ********
✅ Cofre criado!

Configurar Notion? (s/n): s
👤 Usuário/Email: seu.email@gmail.com
🔑 Senha: ********
✅ Notion configurado!

Configurar Gmail? (s/n): n
Configurar GitHub? (s/n): n

✅ Setup concluído!
```

**💡 Dicas:**
- Use master password FORTE
- Anote em local seguro
- Não há recuperação se esquecer!

---

### **ETAPA 9: PRIMEIRO USO DO AGENTE**

Agora vem a parte emocionante! 🎉

```bash
python agente_completo_final.py
```

**Perguntas iniciais:**
```
🔐 Sistema de credenciais disponível
   Usar cofre de credenciais? (s/n): s
   🔑 Master Password: ********

🧠 Sistema de memória disponível
   Usar memória permanente? (s/n): s

✅ Cofre aberto! 2 credenciais carregadas
🧠 Memória carregada: 0 aprendizados

👤 O que você quer?
```

---

### **ETAPA 10: TESTAR FUNCIONALIDADES**

#### **Teste 1: Criação simples**
```
👤 Crie um programa Python que calcula fatorial
```

**Resultado:**
```
✅ Arquivo 'fatorial.py' criado!
```

#### **Teste 2: Computer Use**
```
👤 Acesse google.com e tire um screenshot
```

**Resultado:**
```
🌐 Iniciando navegador...
🔗 Navegando: https://google.com
📸 Screenshot: screenshot.png
✅ Screenshot salvo!
```

#### **Teste 3: Login automático (se configurou)**
```
👤 Entre no Notion
```

**Resultado:**
```
🔐 Login automático: notion
✅ Login realizado!
```

#### **Teste 4: Aprendizado**
```
👤 Salve um aprendizado: categoria=tecnica, 
conteudo=Python é case-sensitive, tags=python,basico
```

**Resultado:**
```
🧠 Aprendizado salvo!
```

---

## ✅ CHECKLIST COMPLETO

### **Instalação Base:**
```
[ ] Python 3.9+ instalado
[ ] pip funcionando
[ ] Conta Anthropic criada
[ ] $10 de créditos adicionados
[ ] API Key obtida e guardada
[ ] Pasta do projeto criada
```

### **Dependências:**
```
[ ] pip install anthropic python-dotenv
[ ] pip install playwright
[ ] pip install cryptography
[ ] playwright install chromium
```

### **Arquivos:**
```
[ ] agente_completo_final.py
[ ] cofre_credenciais.py
[ ] memoria_permanente.py
[ ] setup_credenciais.py
[ ] .env criado com API key
```

### **Configuração:**
```
[ ] Teste básico funcionou
[ ] Cofre de credenciais criado (opcional)
[ ] 1-2 serviços configurados (opcional)
[ ] Master password anotada
```

### **Teste Final:**
```
[ ] python agente_completo_final.py executa
[ ] Criou arquivo simples
[ ] Navegou para site (se Playwright OK)
[ ] Login funcionou (se cofre configurado)
[ ] 🎉 TUDO FUNCIONANDO!
```

---

## 🎓 ESTRUTURA FINAL DO PROJETO

```
agente-claude/
├── .env                          # API key (NÃO commitar!)
├── agente_completo_final.py      # Agente principal ⭐
├── cofre_credenciais.py          # Sistema de credenciais
├── memoria_permanente.py         # Sistema de memória
├── setup_credenciais.py          # Helper de setup
├── cofre.enc                     # Cofre criptografado (criado automaticamente)
├── memoria_agente.json           # Memória (criada automaticamente)
├── teste_basico.py               # Teste opcional
└── screenshots/                  # Screenshots (criados automaticamente)
```

---

## 💡 PRIMEIROS COMANDOS PARA TESTAR

### **1. Comandos simples:**
```
"Crie um programa Python que soma dois números"
"Liste os arquivos na pasta atual"
"Crie um arquivo de texto com minhas notas"
```

### **2. Web básico:**
```
"Acesse wikipedia.org e tire screenshot"
"Entre no hackernews.com e me diga a primeira notícia"
```

### **3. Com credenciais:**
```
"Entre no Notion" (se configurou)
"Liste minhas credenciais"
```

### **4. Aprendizado:**
```
"Busque aprendizados sobre Python"
"Salve um aprendizado: categoria=preferencia, conteudo=Eu prefiro Python"
```

### **5. Avançado:**
```
"Entre no GitHub, vá no meu repositório X e crie uma issue"
"Crie um bot do Telegram que responde com piadas"
"Faça scraping do site X e salve em CSV"
```

---

## 🆘 TROUBLESHOOTING

### **Erro: "Module not found"**
```bash
# Instalar dependência faltando
pip install nome-do-modulo
```

### **Erro: "API key inválida"**
```bash
# Verificar .env
cat .env  # Linux/macOS
type .env # Windows

# Verificar no console Anthropic
# console.anthropic.com/settings/keys
```

### **Erro: "Playwright not installed"**
```bash
pip install playwright
playwright install chromium
```

### **Erro: "Master password incorreta"**
```
→ Não há recuperação!
→ Criar novo cofre:
  rm cofre.enc  # ou delete manualmente
  python setup_credenciais.py rapido
```

### **Erro: "Permission denied"**
```bash
# Linux/macOS
chmod +x agente_completo_final.py

# Windows
# Executar PowerShell como Administrador
```

### **Navegador não abre:**
```bash
# Reinstalar Chromium
playwright install --force chromium
```

### **Muito lento:**
```
→ Fechar outros programas
→ Verificar internet
→ Reduzir max_iteracoes no código
```

---

## 📊 CUSTOS E LIMITES

### **Custos típicos:**
```
Tarefa simples: $0.01-0.03
Tarefa média: $0.05-0.10
Tarefa complexa: $0.10-0.30
Com Computer Use: +20-50%

$10 iniciais = 50-500 tarefas (dependendo)
```

### **Monitorar uso:**
```
Console Anthropic → Settings → Billing
Ver uso em tempo real
Definir alertas de limite
```

### **Otimizar custos:**
```
✅ Usar agente_evolutivo.py quando não precisa de web
✅ Desabilitar memória se não precisa
✅ Limitar max_iteracoes
✅ Tarefas específicas e claras
```

---

## 🎯 PRÓXIMOS PASSOS

### **Agora:**
```
1. ✅ Instalação completa
2. ✅ Testes básicos funcionando
3. → Explorar capacidades
4. → Criar primeiro projeto real
```

### **Esta semana:**
```
1. Adicionar mais credenciais
2. Deixar agente criar ferramentas
3. Ver memória crescer
4. Automatizar tarefas repetitivas
```

### **Este mês:**
```
1. Dominar todos os recursos
2. Criar workflows complexos
3. Integrar com seus sistemas
4. Compartilhar aprendizados
```

---

## 📚 DOCUMENTAÇÃO ADICIONAL

| Preciso de... | Leia... |
|---------------|---------|
| **Visão geral** | [START_HERE.md](computer:///mnt/user-data/outputs/START_HERE.md) |
| **Computer Use** | [GUIA_COMPUTER_USE.md](computer:///mnt/user-data/outputs/GUIA_COMPUTER_USE.md) |
| **Credenciais** | [GUIA_CREDENCIAIS.md](computer:///mnt/user-data/outputs/GUIA_CREDENCIAIS.md) |
| **Comparação** | [COMPARACAO_AGENTES.md](computer:///mnt/user-data/outputs/COMPARACAO_AGENTES.md) |
| **Índice geral** | [INDICE_COMPLETO.md](computer:///mnt/user-data/outputs/INDICE_COMPLETO.md) |

---

## 🎊 PARABÉNS!

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  🎉 INSTALAÇÃO COMPLETA!                                    ║
║                                                              ║
║  Você agora tem o agente AI mais avançado possível:        ║
║                                                              ║
║  ✅ Auto-evolução (cria ferramentas)                        ║
║  ✅ Computer Use (navega web)                               ║
║  ✅ Credenciais seguras (AES-256)                           ║
║  ✅ Memória permanente (aprende)                            ║
║  ✅ Login automático                                        ║
║  ✅ Autonomia TOTAL                                         ║
║                                                              ║
║  Pronto para criar coisas incríveis! 🚀                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🚀 COMANDO FINAL PARA COMEÇAR

```bash
python agente_completo_final.py
```

**Diga o que você quer e deixe a mágica acontecer!** ✨

---

## 💬 AJUDA E SUPORTE

**Dúvidas de instalação?**
→ Revise este guia passo a passo

**Erros específicos?**
→ Consulte Troubleshooting acima

**Quer entender melhor?**
→ Leia a documentação adicional

**Funcionou?**
→ Compartilhe o que você criou! 🎉

---

**Criado com ❤️ para democratizar o acesso a IA avançada**

**Versão: 1.0 Final | Data: 2025**
