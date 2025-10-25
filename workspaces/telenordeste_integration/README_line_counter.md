# 📊 Line Counter - Contador de Linhas e Comentários Python

## 🎯 Objetivo

Módulo para análise de arquivos Python, contando diferentes tipos de linhas:
- **Total de linhas**: Todas as linhas do arquivo
- **Linhas em branco**: Linhas vazias ou apenas com espaços
- **Linhas de comentário**: Linhas que começam com `#`
- **Linhas de código**: Linhas que contêm código executável

## 🚀 Funcionalidades

### Função Principal: `count_lines_and_comments(content)`

```python
from line_counter import count_lines_and_comments

# Exemplo de uso básico
code = """# Comentário
def hello():
    print("Hello!")
"""

result = count_lines_and_comments(code)
print(result)
# Output: {'total_lines': 3, 'blank_lines': 0, 'comment_lines': 1, 'code_lines': 2}
```

### Características

✅ **Precisão**: Usa regex para identificar padrões corretamente  
✅ **Robustez**: Lida com indentação e caracteres especiais  
✅ **Validação**: Garante que a soma dos tipos = total de linhas  
✅ **Documentação**: Docstrings completas e exemplos  
✅ **Testes**: Suite de testes automáticos incluída  

## 📖 Uso Completo

### Análise de Arquivo Individual

```python
from line_counter import count_lines_and_comments
from file_reader import read_file_with_fallback

# Lê arquivo
content, encoding, success = read_file_with_fallback('meu_arquivo.py')

# Analisa linhas
stats = count_lines_and_comments(content)

print(f"Total: {stats['total_lines']}")
print(f"Código: {stats['code_lines']}")
print(f"Comentários: {stats['comment_lines']}")
print(f"Em branco: {stats['blank_lines']}")
```

### Análise de Projeto Completo

```python
from line_counter import count_lines_and_comments
from find_python_files import find_python_files
from file_reader import read_file_with_fallback

# Encontra todos arquivos Python
arquivos = find_python_files('/caminho/projeto')

# Analisa cada arquivo
for arquivo in arquivos:
    content, _, _ = read_file_with_fallback(arquivo)
    stats = count_lines_and_comments(content)
    print(f"{arquivo}: {stats['code_lines']} linhas de código")
```

### Script Pronto: `exemplo_uso_line_counter.py`

Incluímos um script completo que analisa um projeto inteiro:

```bash
# Analisa o diretório atual
python exemplo_uso_line_counter.py

# Analisa um diretório específico
python exemplo_uso_line_counter.py /caminho/do/projeto
```

**Output do script:**
- Estatísticas totais do projeto
- Percentuais de cada tipo de linha
- Top 5 maiores arquivos
- Informações detalhadas por arquivo

## 🧪 Testes

Execute os testes incluídos:

```bash
python line_counter.py
```

**Testes incluídos:**
1. ✅ Código simples com comentários e linhas em branco
2. ✅ Múltiplos comentários consecutivos
3. ✅ Arquivo complexo com docstrings e classes
4. ✅ Arquivo vazio
5. ✅ Apenas comentários
6. ✅ Comentários indentados

**Validações:**
- Todos os valores são não negativos
- Soma dos tipos = total de linhas
- Dicionário com chaves corretas
- Valores são inteiros

## 📋 Especificação Técnica

### Input
- **Tipo**: `str` (conteúdo completo do arquivo)
- **Formato**: String com conteúdo Python válido ou inválido

### Output
- **Tipo**: `Dict[str, int]`
- **Chaves**:
  - `total_lines`: Total de linhas (≥ 0)
  - `blank_lines`: Linhas em branco (≥ 0)
  - `comment_lines`: Linhas de comentário (≥ 0)
  - `code_lines`: Linhas de código (≥ 0)

### Critérios de Sucesso

✅ `blank_lines + comment_lines + code_lines == total_lines`  
✅ Todos os valores são inteiros não negativos  
✅ Função lida com todos os casos extremos  

### Regex Utilizados

```python
# Linha em branco (apenas whitespace)
r'^\s*$'

# Linha de comentário (começa com # após whitespace opcional)
r'^\s*#'
```

## 🔗 Integração com Outros Módulos

Este módulo faz parte de um sistema maior de análise de código:

```
find_python_files.py  →  Descobre arquivos .py
         ↓
file_reader.py        →  Lê arquivos com encoding correto
         ↓
line_counter.py       →  Conta linhas e comentários
         ↓
[Próximo módulo]      →  Análise AST e complexidade
```

## 📊 Exemplo de Saída

```
======================================================================
RELATÓRIO DE ANÁLISE
======================================================================

📊 ESTATÍSTICAS TOTAIS:
  Total de linhas:      5,180
  Linhas em branco:     1,021 (19.7%)
  Linhas de comentário: 299 (5.8%)
  Linhas de código:     3,860 (74.5%)

📈 TOP 5 MAIORES ARQUIVOS (por linhas de código):

  1. main.py
     Total: 312 linhas
     Código: 235 linhas
     Comentários: 15 linhas
     Brancos: 62 linhas
```

## ⚠️ Limitações Conhecidas

1. **Comentários inline**: Linhas como `x = 1  # comentário` são contadas como código, não como comentário
2. **Docstrings**: Docstrings (`"""..."""`) são contados como código, não como comentário
3. **Strings multilinha**: Strings com `\n` são uma linha só

Estas limitações são intencionais e seguem a especificação da tarefa.

## 🎯 Casos de Uso

- **Métricas de projeto**: Quantificar tamanho do codebase
- **Análise de qualidade**: Verificar proporção de comentários
- **Relatórios**: Gerar estatísticas para stakeholders
- **CI/CD**: Monitorar crescimento do código
- **Refatoração**: Identificar arquivos grandes que precisam de atenção

## ✅ Status

**SUBTAREFA 2.2**: ✅ COMPLETA

- [x] Função `count_lines_and_comments` implementada
- [x] Regex para blank_lines e comment_lines
- [x] Cálculo de code_lines
- [x] Retorna dicionário com 4 chaves
- [x] Validação: soma = total
- [x] Valores não negativos garantidos
- [x] Testes automatizados (6 casos)
- [x] Documentação completa
- [x] Exemplo de uso integrado
- [x] Validado em projeto real (27 arquivos, 5,180 linhas)

## 🔄 Próximos Passos

Este módulo está pronto para ser integrado com:
- Análise AST para complexidade ciclomática
- Detecção de code smells
- Geração de relatórios HTML/PDF
- Integração com sistemas de CI/CD

---

**Desenvolvido por**: Luna AI Agent  
**Data**: 2025-01-23  
**Status**: ✅ Produção  
