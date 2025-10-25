# 🧪 GUIA DE TESTES - LUNA TEST SUITE

**Sistema de Teste de Recuperação de Erros e Auto-Evolução**
Criado: 2025-10-19
Versão: 1.0

---

## 📋 ÍNDICE

1. [Visão Geral](#visão-geral)
2. [Como Executar](#como-executar)
3. [Cenários de Teste](#cenários-de-teste)
4. [Erros Propositais](#erros-propositais)
5. [Oportunidades de Melhoria](#oportunidades-de-melhoria)
6. [Resultados Esperados](#resultados-esperados)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 VISÃO GERAL

O **Luna Test Suite** (`luna_test.py`) é uma versão simplificada da Luna criada especificamente para testar dois sistemas críticos:

### 1. **Sistema de Recuperação de Erros**
- Detecta erros automaticamente
- Tenta corrigir até 3 vezes
- Mantém histórico de tentativas
- Logs detalhados de cada correção

### 2. **Sistema de Auto-Evolução**
- Detecta oportunidades de melhoria
- Adiciona à fila de melhorias
- Aplica modificações com backup
- Valida antes de aplicar
- Rollback em caso de falha

### Estatísticas:
- ✅ **10 ferramentas** no total
- 🔴 **6 ferramentas com erros** propositais
- 💡 **4 ferramentas com oportunidades** de melhoria
- 🔄 **Até 3 tentativas** de recuperação automática

---

## 🚀 COMO EXECUTAR

### Execução Interativa:

```bash
cd "/mnt/c/Projetos Automações e Digitais/Luna"
python luna_test.py
```

**Menu interativo:**
```
🧪 LUNA TEST SUITE - Execução de Testes
======================================================================

Escolha um teste para executar:

1. Cenário 1: Recuperação Simples (sintaxe)
2. Cenário 2: Import Faltante
3. Cenário 3: Divisão por Zero
4. Cenário 4: Type Mismatch
5. Executar TODOS os cenários
0. Sair

Escolha (0-5):
```

### Execução Programática:

```python
from luna_test import LunaTest

# Criar instância
luna = LunaTest()

# Executar ferramenta
resultado = luna.executar_ferramenta(
    'criar_arquivo_teste',
    nome='teste.txt',
    conteudo='Hello World'
)
```

---

## 📊 CENÁRIOS DE TESTE

### **CENÁRIO 1: Recuperação Simples (Erro de Sintaxe)**

**Ferramenta:** `criar_arquivo_teste`
**Erro:** Falta parêntese de fechamento

**Como testar:**
```python
luna = LunaTest()
resultado = luna.executar_ferramenta(
    'criar_arquivo_teste',
    nome='teste.txt',
    conteudo='Hello World'
)
```

**O que acontece:**
1. **Tentativa 1:** Executa código → SyntaxError detectado
2. Sistema analisa: "falta parêntese no encoding='utf-8'"
3. **Correção automática:** Adiciona `)`
4. **Tentativa 2:** Executa código corrigido → **SUCESSO** ✅

**Saída esperada:**
```
======================================================================
🔧 Executando: criar_arquivo_teste
   Parâmetros: {'nome': 'teste.txt', 'conteudo': 'Hello World'}
======================================================================

❌ ERRO DE SINTAXE: unexpected EOF while parsing
   💡 Corrigindo sintaxe...
   💡 Adicionando parêntese de fechamento
   ✅ Correção aplicada!

🔄 TENTATIVA 2/3
✅ SUCESSO na tentativa 2!

📋 RESULTADO FINAL:
Arquivo teste.txt criado com sucesso
```

---

### **CENÁRIO 2: Import Faltante**

**Ferramenta:** `processar_json`
**Erro:** Módulo `json` não importado

**Como testar:**
```python
luna = LunaTest()
resultado = luna.executar_ferramenta(
    'processar_json',
    texto='{"nome": "teste", "valor": 42}'
)
```

**O que acontece:**
1. **Tentativa 1:** Executa código → NameError: 'json' is not defined
2. Sistema detecta: "falta import json"
3. **Correção automática:** Adiciona `import json` no início
4. **Tentativa 2:** Executa código corrigido → **SUCESSO** ✅

**Saída esperada:**
```
======================================================================
🔧 Executando: processar_json
   Parâmetros: {'texto': '{"nome": "teste", "valor": 42}'}
======================================================================

❌ ERRO DETECTADO: NameError: name 'json' is not defined
   Tentando corrigir automaticamente...
   🔍 Analisando erro: NameError: name 'json' is not defined...
   💡 Adicionando: import json
   ✅ Correção aplicada!

🔄 TENTATIVA 2/3
✅ SUCESSO na tentativa 2!

📋 RESULTADO FINAL:
JSON processado: 2 campos
```

---

### **CENÁRIO 3: Divisão por Zero**

**Ferramenta:** `calcular_media`
**Erro:** Lista vazia causa divisão por zero

**Como testar:**
```python
luna = LunaTest()
resultado = luna.executar_ferramenta(
    'calcular_media',
    numeros=[]
)
```

**O que acontece:**
1. **Tentativa 1:** Executa código → ZeroDivisionError
2. Sistema detecta: "divisão por zero"
3. **Correção automática:** Adiciona validação `if numeros else 0`
4. **Tentativa 2:** Executa código corrigido → **SUCESSO** ✅

**Saída esperada:**
```
======================================================================
🔧 Executando: calcular_media
   Parâmetros: {'numeros': []}
======================================================================

❌ ERRO DETECTADO: ZeroDivisionError: division by zero
   Tentando corrigir automaticamente...
   🔍 Analisando erro: division by zero...
   💡 Adicionando: validação de lista vazia
   ✅ Correção aplicada!

🔄 TENTATIVA 2/3
✅ SUCESSO na tentativa 2!

📋 RESULTADO FINAL:
Média: 0
```

---

### **CENÁRIO 4: Type Mismatch**

**Ferramenta:** `concatenar_strings`
**Erro:** Tentativa de concatenar string + int

**Como testar:**
```python
luna = LunaTest()
resultado = luna.executar_ferramenta(
    'concatenar_strings',
    texto='Número: ',
    numero=42
)
```

**O que acontece:**
1. **Tentativa 1:** Executa código → TypeError: can only concatenate str
2. Sistema detecta: "type mismatch"
3. **Correção automática:** Adiciona `str(numero)`
4. **Tentativa 2:** Executa código corrigido → **SUCESSO** ✅

**Saída esperada:**
```
======================================================================
🔧 Executando: concatenar_strings
   Parâmetros: {'texto': 'Número: ', 'numero': 42}
======================================================================

❌ ERRO DETECTADO: TypeError: can only concatenate str (not "int") to str
   Tentando corrigir automaticamente...
   🔍 Analisando erro: TypeError...
   💡 Convertendo: str(numero)
   ✅ Correção aplicada!

🔄 TENTATIVA 2/3
✅ SUCESSO na tentativa 2!

📋 RESULTADO FINAL:
Resultado: Número: 42
```

---

## 🔴 ERROS PROPOSITAIS (6 tipos)

### 1. **Erro de Sintaxe**
- **Ferramenta:** `criar_arquivo_teste`
- **Problema:** Falta parêntese de fechamento
- **Código:**
  ```python
  Path(nome).write_text(conteudo, encoding='utf-8'  # ← Falta )
  ```
- **Correção:** Adiciona `)`

### 2. **Import Faltante**
- **Ferramenta:** `processar_json`
- **Problema:** Usa `json.loads()` mas não importa `json`
- **Código:**
  ```python
  dados = json.loads(texto)  # ← json não importado
  ```
- **Correção:** Adiciona `import json`

### 3. **Encoding Não Especificado**
- **Ferramenta:** `ler_arquivo_unicode`
- **Problema:** `open()` sem `encoding='utf-8'`
- **Código:**
  ```python
  with open(caminho, 'r') as f:  # ← Falta encoding
  ```
- **Correção:** Adiciona `encoding='utf-8'`

### 4. **Path com Espaços**
- **Ferramenta:** `criar_pasta`
- **Problema:** Path com espaços mal formatado
- **Código:**
  ```python
  os.mkdir("C:\\Teste Com Espaços\\" + nome)
  ```
- **Correção:** Usar `Path()` do pathlib

### 5. **Divisão por Zero**
- **Ferramenta:** `calcular_media`
- **Problema:** Não valida lista vazia
- **Código:**
  ```python
  media = sum(numeros) / len(numeros)  # ← len pode ser 0
  ```
- **Correção:** Adiciona `if numeros else 0`

### 6. **Type Mismatch**
- **Ferramenta:** `concatenar_strings`
- **Problema:** Concatena string + int sem conversão
- **Código:**
  ```python
  resultado = texto + numero  # ← Precisa str(numero)
  ```
- **Correção:** Adiciona `str(numero)`

---

## 💡 OPORTUNIDADES DE MELHORIA (4 tipos)

### 1. **Performance: Loop Ineficiente**
- **Ferramenta:** `processar_lista`
- **Problema:** Loop pode ser list comprehension
- **Código atual:**
  ```python
  resultado = []
  for item in items:
      resultado.append(item.upper())
  ```
- **Sugestão:** `resultado = [item.upper() for item in items]`

### 2. **Qualidade: Falta Type Hints**
- **Ferramenta:** `somar_numeros`
- **Problema:** Sem anotações de tipo
- **Código atual:**
  ```python
  def somar_numeros(a, b):
  ```
- **Sugestão:** `def somar_numeros(a: int, b: int) -> int:`

### 3. **Qualidade: Falta Docstring**
- **Ferramenta:** `validar_email`
- **Problema:** Sem documentação
- **Código atual:**
  ```python
  def validar_email(email: str) -> str:
      # Sem docstring
  ```
- **Sugestão:** Adicionar docstring Google Style

### 4. **Segurança: Falta Validação**
- **Ferramenta:** `deletar_arquivo_perigoso`
- **Problema:** Deleta sem validar caminho
- **Código atual:**
  ```python
  os.remove(caminho)  # Sem validação
  ```
- **Sugestão:** Validar se path está em área permitida

---

## ✅ RESULTADOS ESPERADOS

### Taxa de Sucesso Esperada:

| Cenário | Tentativas Esperadas | Taxa de Sucesso |
|---------|---------------------|-----------------|
| Cenário 1 (Sintaxe) | 2 tentativas | 100% |
| Cenário 2 (Import) | 2 tentativas | 100% |
| Cenário 3 (Divisão Zero) | 2 tentativas | 100% |
| Cenário 4 (Type Mismatch) | 2 tentativas | 100% |

### Métricas de Recuperação:

- **Tempo médio de recuperação:** < 1 segundo
- **Tentativas médias:** 2 (máximo 3)
- **Taxa de sucesso geral:** 100% nos cenários testados

---

## 🐛 TROUBLESHOOTING

### Problema: "sistema_auto_evolucao.py não encontrado"

**Causa:** Módulo de auto-evolução não está no path

**Solução:**
```bash
# Verificar se arquivo existe
ls sistema_auto_evolucao.py

# Se não existir, Luna Test funcionará sem auto-evolução
# (apenas teste de recuperação)
```

### Problema: Erros de encoding no Windows

**Causa:** Console não configurado para UTF-8

**Solução:** Luna Test já configura automaticamente, mas se persistir:
```python
# Forçar UTF-8 manualmente
import sys
sys.stdout.reconfigure(encoding='utf-8')
```

### Problema: "ERRO: Máximo de tentativas atingido"

**Causa:** Erro não foi corrigível automaticamente

**Solução:** Isso é esperado em alguns casos! O sistema tem limitações:
- Erros complexos podem precisar intervenção manual
- Máximo de 3 tentativas é intencional (evitar loop infinito)

---

## 📝 EXEMPLOS DE USO AVANÇADO

### Testar Erro Específico:

```python
from luna_test import LunaTest

luna = LunaTest()

# Testar apenas import faltante
resultado = luna.executar_ferramenta(
    'processar_json',
    texto='{"test": true}'
)

# Ver histórico de erros
print(luna.listar_erros_recentes())
```

### Testar Todas as Ferramentas:

```python
from luna_test import LunaTest

luna = LunaTest()

# Listar ferramentas
print(luna.listar_ferramentas())

# Testar cada uma
for ferramenta in ['criar_arquivo_teste', 'processar_json', 'calcular_media']:
    print(f"\n{'='*70}")
    print(f"Testando: {ferramenta}")
    # Executar com parâmetros adequados...
```

### Ver Código das Ferramentas:

```python
from luna_test import LunaTest

luna = LunaTest()

# Ver código de ferramenta específica
print(luna.ferramentas['criar_arquivo_teste'])
```

---

## 🎯 PRÓXIMOS PASSOS

Após validar o sistema de recuperação, você pode:

1. **Integrar com Luna Real:**
   - Testar mesma lógica na Luna completa
   - Verificar se funciona com ferramentas reais

2. **Testar Auto-Evolução:**
   - Executar ferramentas com melhorias detectáveis
   - Ver se sistema adiciona à fila automaticamente
   - Aplicar melhorias e verificar backup/rollback

3. **Criar Novos Cenários:**
   - Adicionar mais tipos de erro
   - Testar erros mais complexos
   - Validar limites do sistema

4. **Análise de Performance:**
   - Medir tempo de recuperação
   - Contar tentativas necessárias
   - Calcular taxa de sucesso

---

**Criado:** 2025-10-19
**Versão:** 1.0
**Status:** ✅ Pronto para uso

**Documentação relacionada:**
- `luna_test.py` - Código principal
- `sistema_auto_evolucao.py` - Sistema de auto-evolução
- `README_VERSAO_FINAL.md` - Documentação completa da Luna
