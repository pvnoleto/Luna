# 🚀 GUIA RÁPIDO - LUNA V3

## ⚡ Início em 5 Minutos

---

## 1️⃣ INSTALAÇÃO (2 minutos)

### Pré-requisitos
```bash
# Python 3.8+
python --version

# Instalar dependências obrigatórias
pip install anthropic python-dotenv

# Opcional (para computer use)
pip install playwright
playwright install chromium
```

### Configurar API Key
```bash
# Criar arquivo .env na pasta Luna
ANTHROPIC_API_KEY=sk-ant-api-XXXXXXXX
```

---

## 2️⃣ EXECUTAR (1 minuto)

```bash
cd "C:\Projetos Automações e Digitais\Luna"
python luna_v3_FINAL_OTIMIZADA.py
```

---

## 3️⃣ CONFIGURAÇÃO INICIAL (1 minuto)

### Perguntas ao Iniciar

**1. Tier da API**
```
Escolha: 2 (Tier 2 - 1000 RPM)
```

**2. Modo de Rate Limiting**
```
Escolha: 2 (Balanceado - RECOMENDADO)
```

**3. Cofre de Credenciais** *(Opcional)*
```
Usar? s ou n
Se sim: Digite master password
```

---

## 4️⃣ PRIMEIRO USO (1 minuto)

### Exemplo 1: Tarefa Simples
```
💬 O que você quer? Crie um script Python que calcula o fatorial de um número

✅ Luna vai:
1. Buscar aprendizados relevantes
2. Criar o arquivo fatorial.py
3. Mostrar o código
4. Salvar o aprendizado
```

### Exemplo 2: Com Workspace
```
💬 O que você quer? Crie um workspace para meu projeto web

✅ Luna vai:
1. Criar pasta Luna/workspaces/projeto_web/
2. Selecionar como workspace atual
3. Próximos arquivos vão para lá automaticamente
```

### Exemplo 3: Computer Use
```
💬 O que você quer? Tire um screenshot do Google

✅ Luna vai:
1. Verificar Playwright
2. Iniciar navegador
3. Navegar para google.com
4. Tirar screenshot
5. Salvar no workspace
```

---

## 🎯 COMANDOS ÚTEIS

### Durante a Execução

| Comando | Ação |
|---------|------|
| `sair`, `exit`, `quit` | Sair da Luna |
| `multi` | Modo multiline (textos grandes) |
| `Enter` | Confirmar texto colado |
| `Ctrl+C` | Interrupção graciosa |
| `Ctrl+C` (2x) | Forçar saída |

### Para Textos Grandes
```
Opção 1: Cole normalmente (Ctrl+V)
         Luna mostra preview e pede confirmação

Opção 2: Digite 'multi'
         Cole o texto
         Digite 'FIM' para terminar
```

---

## 📁 ESTRUTURA DE ARQUIVOS

```
Luna/
├── luna_v3_FINAL_OTIMIZADA.py  ← Executar este
├── .env                         ← API key aqui
├── cofre.enc                    ← Credenciais (se usar)
├── memoria_agente.json          ← Memória permanente
└── workspaces/                  ← Seus projetos
    ├── projeto1/
    └── projeto2/
```

---

## ⚙️ CONFIGURAÇÕES RECOMENDADAS

### Para Uso Diário
```
Tier: 2 (Tier 2)
Modo: Balanceado
Cofre: Opcional
Memória: Sim (automático)
```

### Para Desenvolvimento Intenso
```
Tier: 2 ou 3
Modo: Agressivo
Cofre: Sim (para automações)
Memória: Sim
```

### Para Projetos Grandes
```
Tier: 3 ou 4
Modo: Balanceado ou Agressivo
Cofre: Sim
Memória: Sim
Workspaces: Criar um por projeto
```

---

## 🔧 TROUBLESHOOTING RÁPIDO

### Erro: "ANTHROPIC_API_KEY não encontrada"
```bash
# Solução:
1. Crie arquivo .env na pasta Luna
2. Adicione: ANTHROPIC_API_KEY=sk-ant-...
```

### Erro: "Module 'anthropic' not found"
```bash
# Solução:
pip install anthropic python-dotenv
```

### Erro: "Playwright not found"
```bash
# Solução (só se usar computer use):
pip install playwright
playwright install chromium
```

### Erro: Rate Limit 429
```bash
# Solução:
A Luna já trata isso automaticamente!
Aguarda 60s e continua
```

### Luna não responde
```bash
# Possíveis causas:
1. Sem internet
2. API key inválida
3. Sem créditos na Anthropic

# Verificar:
1. Teste conexão
2. Confira API key no .env
3. Veja saldo em console.anthropic.com
```

---

## 💡 DICAS PRO

### 1. Use Workspaces
```
✅ Organize projetos separadamente
✅ Arquivos vão para lugar certo automaticamente
✅ Fácil de encontrar depois

Comando:
💬 Crie um workspace chamado meu_projeto
```

### 2. Aproveite a Memória
```
✅ Luna lembra entre sessões
✅ Busca aprendizados automaticamente
✅ Melhora com o tempo

Ela faz isso sozinha!
```

### 3. Cole Textos Grandes
```
✅ Cole com Ctrl+V normalmente
✅ Luna mostra preview
✅ Confirma se está correto

Ou:
💬 multi
   (cole o texto)
   FIM
```

### 4. Use Recuperação Automática
```
✅ Se algo der erro, Luna tenta corrigir
✅ Até 3 tentativas automáticas
✅ Volta à tarefa após sucesso

Você não precisa fazer nada!
```

### 5. Ctrl+C Seguro
```
✅ Luna fecha navegador
✅ Salva estatísticas
✅ Cleanup automático

Sempre seguro interromper!
```

---

## 📊 ESTATÍSTICAS

### Ao Final de Cada Tarefa
```
📊 ESTATÍSTICAS DA SESSÃO:
   Requisições: 15
   Tokens usados: 25,430
   Média tokens/req: 1,695
   Esperas: 2 (45s total)
```

### Ao Sair
```
📊 ESTATÍSTICAS FINAIS:
   Total de requisições: 42
   Total de tokens: 89,234

💾 RESUMO DA MEMÓRIA:
   Aprendizados: 18
   Tarefas: 12
   Ferramentas: 24
```

---

## 🎯 EXEMPLOS DE USO

### Desenvolvimento
```
💬 Crie um API REST em Python com FastAPI
💬 Adicione autenticação JWT
💬 Crie testes unitários
```

### Automação Web
```
💬 Acesse o site X e extraia os preços
💬 Preencha o formulário com meus dados
💬 Tire screenshots das 3 primeiras páginas
```

### Análise de Dados
```
💬 Leia o CSV e faça análise estatística
💬 Crie gráficos com matplotlib
💬 Gere relatório em PDF
```

### Criação de Conteúdo
```
💬 Escreva um artigo sobre IA
💬 Crie apresentação em Markdown
💬 Gere README para meu projeto
```

---

## ⚡ ATALHOS E TRUQUES

### Rápido e Direto
```
💬 ls
💬 pwd  
💬 cat arquivo.txt
```

### Instalar Bibliotecas
```
💬 Instale pandas e matplotlib
```

### Criar Múltiplos Arquivos
```
💬 Crie estrutura de projeto Django
```

### Ver Workspaces
```
💬 Liste todos os workspaces
```

### Ver Aprendizados
```
💬 Busque aprendizados sobre Python
```

---

## 🎓 PRÓXIMOS PASSOS

### Após Primeiro Uso
1. ✅ Crie um workspace para seu projeto
2. ✅ Use Luna para tarefas reais
3. ✅ Veja a memória crescer

### Para Usuários Avançados
1. 📖 Leia o `README_VERSAO_FINAL.md`
2. 🔧 Configure o cofre de credenciais
3. 🌐 Use computer use para automações
4. 🚀 Crie ferramentas customizadas

### Para Desenvolvedores
1. 📝 Leia o código fonte
2. 🧪 Adicione testes unitários
3. 🔧 Contribua com melhorias
4. 📚 Estude a arquitetura

---

## 📚 DOCUMENTAÇÃO COMPLETA

- `README_VERSAO_FINAL.md` - Documentação detalhada
- `CHANGELOG.md` - Histórico de versões
- `RESUMO_EXECUTIVO.md` - Análise completa
- `GUIA_RAPIDO.md` - Este arquivo

---

## 🆘 SUPORTE

### Problemas?
1. Consulte o Troubleshooting acima
2. Leia o README completo
3. Verifique o CHANGELOG

### Dúvidas?
1. Toda documentação está em português
2. Código tem comentários explicativos
3. Docstrings detalham cada função

---

## ✅ CHECKLIST DE INÍCIO

- [ ] Python 3.8+ instalado
- [ ] Dependencies instaladas (`pip install anthropic python-dotenv`)
- [ ] Arquivo `.env` criado com API key
- [ ] Luna executada pela primeira vez
- [ ] Tier configurado
- [ ] Modo configurado
- [ ] Primeira tarefa executada com sucesso

**Tudo OK? Você está pronto! 🎉**

---

## 🎯 LEMBRE-SE

### 3 Regras de Ouro
1. 🔑 **API Key**: Sempre no `.env`
2. 🎯 **Workspaces**: Use para organizar
3. 🧠 **Memória**: Luna aprende sozinha

### O Que Luna FAZ Automaticamente
- ✅ Busca aprendizados relevantes
- ✅ Detecta e corrige erros (até 3x)
- ✅ Respeita rate limits
- ✅ Salva aprendizados
- ✅ Organiza no workspace
- ✅ Fecha recursos (Ctrl+C)

### O Que VOCÊ Precisa Fazer
- ✅ Descrever o que quer
- ✅ Confirmar textos grandes (se houver)
- ✅ Aproveitar! 🚀

---

**Pronto para começar? Execute a Luna e divirta-se! 🌙✨**

```bash
python luna_v3_FINAL_OTIMIZADA.py
```

---

**Versão do Guia**: 1.0  
**Data**: 2025-10-17  
**Status**: ✅ Testado e Validado
