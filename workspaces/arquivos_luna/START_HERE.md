# 🚀 AGENTES CLAUDE - START HERE

## ⚡ 30 SEGUNDOS

```bash
# 1. Instalar
pip install anthropic python-dotenv

# 2. Configurar
echo "ANTHROPIC_API_KEY=sk-ant-api03-SUA_CHAVE" > .env

# 3. Escolher agente
python agente_evolutivo.py        # 90% dos casos
python agente_ultra_avancado.py   # Se precisa navegar web

# 4. Usar
"Crie um site de portfólio para mim"
```

**API Key:** https://console.anthropic.com/settings/keys ($10 = ~300 tarefas)

---

## 🎯 2 AGENTES, QUAL USAR?

### **Agente Auto-Evolutivo** (agente_evolutivo.py)
```
✅ Cria ferramentas dinamicamente
✅ Instala bibliotecas
✅ Adapta-se a qualquer tarefa
❌ Não vê sites visualmente

Use para:
- Criar aplicações
- APIs REST
- Processamento de dados
- Bots (Telegram, Discord)
- 80-90% das tarefas

Custo: $0.02-0.10/tarefa
```

### **Agente Ultra-Avançado** 🆕 (agente_ultra_avancado.py)
```
✅ Tudo do anterior +
✅ NAVEGA WEB visualmente
✅ INTERAGE com sites
✅ TIRA SCREENSHOTS
✅ BASH avançado

Use para:
- Automação web
- Testar formulários
- Web scraping visual
- Monitorar sites
- Preencher forms

Custo: $0.05-0.20/tarefa
Requer: pip install playwright
```

---

## 📚 DOCUMENTAÇÃO

| Preciso de... | Leia... |
|---------------|---------|
| **Decidir qual usar** | [COMPARACAO_AGENTES.md](computer:///mnt/user-data/outputs/COMPARACAO_AGENTES.md) ⭐ |
| **Computer Use (web)** | [GUIA_COMPUTER_USE.md](computer:///mnt/user-data/outputs/GUIA_COMPUTER_USE.md) |
| **Auto-evolução geral** | [README_AGENTE_EVOLUTIVO.md](computer:///mnt/user-data/outputs/README_AGENTE_EVOLUTIVO.md) |
| **Ver exemplos reais** | [EXEMPLO_SESSAO_REAL.md](computer:///mnt/user-data/outputs/EXEMPLO_SESSAO_REAL.md) |
| **Tudo em um lugar** | [INDICE_COMPLETO.md](computer:///mnt/user-data/outputs/INDICE_COMPLETO.md) |

---

## 🧪 EXEMPLOS RÁPIDOS

### **Auto-Evolutivo:**
```
"Crie uma API REST com Flask para gerenciar tarefas"
"Faça um bot do Telegram que responde com piadas"
"Processe este CSV e gere relatório em PDF"
"Crie sistema de login completo com banco de dados"
```

### **Ultra-Avançado (Computer Use):**
```
"Acesse hackernews.com e me diga as 5 notícias principais"
"Teste o formulário de contato do meu site localhost:3000"
"Monitore o preço do produto X no site Y"
"Preencha automaticamente o formulário em site.com"
```

---

## 💡 DECISÃO EM 1 PERGUNTA

> **"Preciso que o agente ABRA sites no navegador?"**

```
SIM → agente_ultra_avancado.py
NÃO → agente_evolutivo.py
```

---

## 🎯 INSTALAÇÃO COMPLETA

### **Auto-Evolutivo (recomendado começar aqui):**
```bash
# 1. Bibliotecas
pip install anthropic python-dotenv

# 2. Configurar
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

# 3. Baixar
# agente_evolutivo.py

# 4. Executar
python agente_evolutivo.py
```

### **Ultra-Avançado (se precisar web):**
```bash
# 1-2. Mesmo do anterior

# 3. Adicional para navegador
pip install playwright
playwright install chromium

# 4. Baixar
# agente_ultra_avancado.py

# 5. Executar
python agente_ultra_avancado.py
```

---

## 📊 COMPARAÇÃO RÁPIDA

| Feature | Auto-Evolutivo | Ultra-Avançado |
|---------|----------------|----------------|
| Cria ferramentas | ✅ | ✅ |
| Instala libs | ✅ | ✅ |
| Navega web | ❌ | ✅ |
| Screenshots | ❌ | ✅ |
| Interage com sites | ❌ | ✅ |
| Custo | Menor | Maior |
| Velocidade | Rápido | Médio |
| Casos de uso | 90% | 100% |

---

## 🔥 CAPACIDADES

### **Ambos podem:**
- Criar qualquer tipo de arquivo
- Executar comandos
- Instalar bibliotecas Python
- Criar novas ferramentas conforme precisa
- Adaptar-se a qualquer tarefa
- Aprender permanentemente

### **Só Ultra-Avançado:**
- Abrir navegador (Chromium)
- Navegar sites visualmente
- Clicar em botões/links
- Preencher formulários
- Tirar screenshots
- Aguardar elementos carregarem
- Interagir como humano faria

---

## ⚠️ IMPORTANTE

### **Segurança:**
```
⚠️ Ambos agentes têm CONTROLE TOTAL do sistema
✅ Use em ambiente isolado para teste
✅ Revise comandos destrutivos
✅ Faça backups
```

### **Custos:**
```
$10 iniciais = ~200-500 tarefas
Monitor em: console.anthropic.com/settings/billing
```

### **Requisitos:**
```
- Python 3.9+
- Conta Anthropic (grátis)
- $10 de créditos
- 5-10 minutos de setup
```

---

## 🎓 PROGRESSÃO SUGERIDA

```
DIA 1:
└─ agente_evolutivo.py
   └─ Testar comandos simples
   └─ Criar pequenos projetos

SEMANA 1:
└─ Explorar capacidades
   └─ Criar APIs, bots, automações
   └─ Ver agente criando ferramentas

SEMANA 2 (se precisar):
└─ agente_ultra_avancado.py
   └─ Automação web
   └─ Testes de UI
```

---

## 🆘 TROUBLESHOOTING

**Erro: API key inválida**
→ Verificar .env, console.anthropic.com

**Erro: Module not found**
→ pip install anthropic python-dotenv

**Playwright não funciona**
→ playwright install chromium

**Muito caro**
→ Usar agente_evolutivo (mais barato)

**Muito lento**
→ Usar agente_evolutivo (mais rápido)

**Não vê site**
→ Precisa do agente_ultra_avancado

---

## ✅ CHECKLIST

```
[ ] Conta Anthropic criada
[ ] API Key obtida
[ ] $10 créditos adicionados
[ ] pip install anthropic python-dotenv
[ ] Arquivo .env criado com chave
[ ] Agente escolhido e baixado
[ ] python agente_X.py executado
[ ] Testei comando simples
[ ] FUNCIONOU! 🎉
```

---

## 🎊 COMEÇAR AGORA

### **Recomendação para 90%:**
```bash
python agente_evolutivo.py
```
Digite: `"Crie um programa Python que calcula fatorial"`

### **Se precisar de web:**
```bash
python agente_ultra_avancado.py
```
Digite: `"Acesse google.com e tire screenshot"`

---

## 📞 LINKS ÚTEIS

- **Console Anthropic:** https://console.anthropic.com
- **Obter API Key:** https://console.anthropic.com/settings/keys
- **Documentação:** https://docs.anthropic.com
- **Billing:** https://console.anthropic.com/settings/billing

---

## 🌟 LEMBRE-SE

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║  Você só precisa DIZER o que quer.                  ║
║  O agente faz TUDO sozinho.                         ║
║                                                      ║
║  Cria ferramentas.                                  ║
║  Instala bibliotecas.                               ║
║  Escreve código.                                    ║
║  Testa.                                             ║
║  Entrega pronto.                                    ║
║                                                      ║
║  É REALMENTE autonomia total! 🚀                    ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```

---

**Boa sorte e divirta-se!** 🎉

**Dúvidas?** Consulte os guias detalhados ou me pergunte! 🤝
