# Relatório: Diagnóstico Completo - Bug Crítico Fase 3 do Planejamento

**Data**: 2025-10-23
**Execuções Analisadas**: 9a70f9 (validação bug fix), 82b7e2 (suite 12 tarefas)
**Status**: 🔴 **BUG CRÍTICO CONFIRMADO**
**Gravidade**: CRÍTICA - Sistema de planejamento inutilizável

---

## 📊 SUMÁRIO EXECUTIVO

O sistema de planejamento avançado da Luna V3 está **completamente quebrado** devido a um bug na **Fase 3** (Decomposição em Subtarefas) que impede a geração de planos executáveis.

**Impacto**:
- ✅ Fases 1-2 funcionam perfeitamente (Análise + Estratégia)
- ❌ Fase 3 falha 100% das vezes (JSON malformado)
- ❌ Nenhuma tarefa é executada de fato (0 ondas geradas)
- ❌ Sistema retorna sucesso falso (exit code 0, mas 0% tarefas realizadas)

---

## 🔍 ANÁLISE DO PLANO FALHO

### Arquivo: `plano_20251023_181913.json` (9.6KB)

**Estrutura do Plano**:
```json
{
  "tarefa_original": "TAREFA 1: Criar calculadora de Fibonacci...",  // ✅ OK
  "analise": {                                                          // ✅ FASE 1 - PERFEITA
    "requisitos_explicitos": [7 itens],
    "requisitos_implicitos": [8 itens],
    "dependencias": {...},
    "riscos": [3 riscos identificados],
    "estimativa_complexidade": "simples",
    "tempo_estimado": "3-5 minutos",
    "conhecimento_previo_relevante": [5 itens]
  },
  "estrategia": {                                                       // ✅ FASE 2 - EXCELENTE
    "abordagem": "Desenvolvimento incremental...",
    "justificativa": "Esta abordagem garante...",
    "sequencia_otima": [8 ações detalhadas],                           // ✅ 8 passos lógicos
    "oportunidades_paralelizacao": [1 item],
    "pontos_validacao": [5 pontos bem definidos],
    "planos_contingencia": [4 contingências]
  },
  "decomposicao": {                                                    // ❌ FASE 3 - VAZIA!
    "ondas": [],                                                       // ❌ 0 ondas
    "total_subtarefas": 0,                                            // ❌ 0 subtarefas
    "tempo_estimado_sequencial": "desconhecido",
    "tempo_estimado_paralelo": "desconhecido"
  },
  "ondas": []                                                          // ❌ VAZIO
}
```

**Veredicto**: Plano tem **excelente qualidade** nas Fases 1-2, mas é **completamente inútil** devido ao vazio na Fase 3.

---

## 🐛 DIAGNÓSTICO TÉCNICO DO BUG

### Localização

**Arquivo**: `luna_v3_FINAL_OTIMIZADA.py`
**Função**: `PlanificadorAvancado._decompor_em_subtarefas()` (linhas 460-508)
**Fase**: 3/4 do sistema de planejamento

### Erro Observado

```
⚠️  Tentativa 1: Erro ao parsear JSON (Expecting ',' delimiter: line 1 column 13279 (char 13278))
⚠️  Erro ao parsear JSON da decomposição após 2 tentativas: Expecting ':' delimiter: line 1 column 6700 (char 6699)
✓ Total de ondas: 0
✓ Total de subtarefas: 0
```

### Causa Raiz

A API Claude está **gerando JSON sintaticamente inválido** mesmo após:
1. ✅ Sanitização de caracteres de controle (linha 493) - **JÁ IMPLEMENTADA**
2. ✅ Remoção de markdown (linhas 483-488)
3. ✅ Tentativa de completar JSON truncado (linhas 490-491)
4. ✅ Retry com menos tokens (2048 vs 4096) na 2ª tentativa

**O problema não é caractere de controle** (já corrigido anteriormente).
**O problema é JSON estruturalmente malformado**: vírgulas ou dois-pontos faltando.

### Diferença dos Bugs

| Aspecto | Bug Anterior (CORRIGIDO ✅) | Bug Atual (ATIVO ❌) |
|---------|---------------------------|---------------------|
| **Erro** | Invalid control character | Expecting ',' ou ':' delimiter |
| **Causa** | Caracteres 0x00-0x1F não-escapados | JSON malformado (sintaxe) |
| **Local** | Dentro de strings JSON | Estrutura do JSON |
| **Correção Aplicada** | `re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)` | Nenhuma (pendente) |
| **Status** | ✅ Funcionava antes | ❌ Quebrou agora |

---

## 📈 HISTÓRICO DE EXECUÇÕES

### Execução b6d02d (2025-10-23 17:32) - ✅ SUCESSO
- **Plano**: `plano_20251023_173216.json` (23KB)
- **Fase 3**: ✅ 5 ondas, 5 subtarefas
- **Tarefa executada**: 100% (TAREFA 1 completa)
- **Exit code**: 0

### Execução 8be6cc (2025-10-23 17:46) - ❌ FALHA
- **Plano**: `plano_20251023_174610.json` (8.2KB)
- **Fase 3**: ❌ 0 ondas, 0 subtarefas
- **Tarefa executada**: 0%
- **Exit code**: 0 (sucesso falso!)

### Execução 9a70f9 (2025-10-23 18:02) - ✅ SUCESSO
- **Plano**: `plano_20251023_180253.json` (26KB)
- **Fase 3**: ✅ 5 ondas, 7 subtarefas
- **Tarefa executada**: 100% (TAREFA 1 completa)
- **Exit code**: 0

### Execução 82b7e2 (2025-10-23 18:19) - ❌ FALHA
- **Plano**: `plano_20251023_181913.json` (9.6KB)
- **Fase 3**: ❌ 0 ondas, 0 subtarefas
- **Tarefa executada**: 0%
- **Exit code**: 0 (sucesso falso!)

### Padrão Identificado

**Taxa de falha: 50%** (2 sucessos, 2 falhas em 4 execuções)
**Características**:
- Planos BEM-SUCEDIDOS: 23-26KB
- Planos FALHOS: 8-10KB (65% menores)
- Bug é **intermitente** e **aleatório**
- Provavelmente relacionado ao comportamento não-determinístico da API

---

## 🔬 ANÁLISE DO CÓDIGO

### Mecanismos de Proteção Existentes

**1. Sanitização de Caracteres de Controle** (linha 493):
```python
import re
resultado_sanitizado = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', resultado_limpo)
decomposicao = json.loads(resultado_sanitizado)
```
✅ **JÁ IMPLEMENTADO** - Remove caracteres 0x00-0x1F e 0x7F-0x9F

**2. Limpeza de Markdown** (linhas 483-488):
```python
if resultado_limpo.startswith('```json'):
    resultado_limpo = resultado_limpo[7:]
if resultado_limpo.startswith('```'):
    resultado_limpo = resultado_limpo[3:]
if resultado_limpo.endswith('```'):
    resultado_limpo = resultado_limpo[:-3]
```
✅ Remove blocos de código markdown

**3. Correção de JSON Truncado** (linhas 490-491):
```python
if not resultado_limpo.endswith('}'):
    resultado_limpo = resultado_limpo.rstrip(',') + '\n    ]\n  }\n],\n"total_subtarefas": 0,...'
```
✅ Tenta completar JSON incompleto

**4. Retry com Menos Tokens** (linhas 477-481):
```python
max_tentativas = 2
for tentativa in range(max_tentativas):
    max_tokens_atual = 4096 if tentativa == 0 else 2048
```
✅ 2 tentativas: 4096 tokens → 2048 tokens

### O Que Está Faltando

❌ **Parsing JSON Robusto**: Não há fallback para JSONs sintaticamente inválidos
❌ **Validação Estrutural**: Não valida se JSON tem estrutura mínima esperada
❌ **Logging Detalhado**: Não salva JSON bruto para debug
❌ **JSON Repair**: Não usa bibliotecas especializadas em consertar JSON quebrado

---

## 💡 PROPOSTAS DE CORREÇÃO

### Solução 1: JSON Repair com Fallback (RECOMENDADO)

**Implementação**:
```python
def _decompor_em_subtarefas(self, estrategia: Dict) -> Dict:
    # ... código existente até linha 493 ...

    import re
    resultado_sanitizado = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', resultado_limpo)

    try:
        decomposicao = json.loads(resultado_sanitizado)
    except json.JSONDecodeError as e_principal:
        # 🛡️ FALLBACK 1: Tentar json_repair
        try:
            from json_repair import repair_json
            json_reparado = repair_json(resultado_sanitizado)
            decomposicao = json.loads(json_reparado)
            print_realtime("   ⚠️  JSON reparado automaticamente")
        except Exception as e_repair:
            # 🛡️ FALLBACK 2: Parsear linha por linha para recuperar o máximo possível
            try:
                import ast
                # Tentar extrair ondas manualmente usando regex
                ondas_match = re.search(r'"ondas"\s*:\s*\[(.*?)\]', resultado_sanitizado, re.DOTALL)
                if ondas_match:
                    # Processar ondas encontradas...
                    print_realtime("   ⚠️  Ondas parcialmente recuperadas")
                else:
                    raise e_principal
            except:
                # 🛡️ FALLBACK 3: Retornar erro
                if tentativa < max_tentativas - 1:
                    print_realtime(f'   ⚠️  Tentativa {tentativa + 1}: Erro ao parsear JSON ({e_principal})')
                    # Salvar JSON bruto para debug
                    with open(f'Luna/.debug/json_falho_{tentativa}.json', 'w') as f:
                        f.write(resultado_sanitizado)
                else:
                    print_realtime(f'   ⚠️  Erro ao parsear JSON após {max_tentativas} tentativas: {e_principal}')
                    return {'ondas': [], 'total_subtarefas': 0, ...}
```

**Vantagens**:
- ✅ Tenta 3 níveis de recuperação antes de desistir
- ✅ Usa library especializada (json_repair)
- ✅ Salva JSONs falhos para debug
- ✅ Mantém compatibilidade com código existente

**Desvantagens**:
- ❌ Requer nova dependência (`json_repair`)
- ❌ Mais complexo (50+ linhas)

---

### Solução 2: Prompt Mais Restritivo (SIMPLES)

**Modificação no prompt** (linha 476):
```python
prompt = f'''DECOMPOSIÇÃO EM SUBTAREFAS EXECUTÁVEIS

Estratégia definida (Fase 2):
{json.dumps(estrategia, indent=2, ensure_ascii=False)}

IMPORTANTE - REGRAS DE FORMATAÇÃO JSON:
1. Gere JSON ESTRITAMENTE VÁLIDO (RFC 8259)
2. Use APENAS aspas duplas (")
3. Escape todos os caracteres especiais (\\n, \\t, \\")
4. NÃO use vírgulas após último item de arrays/objetos
5. SEMPRE inclua dois-pontos (:) após chaves
6. SEMPRE termine objetos com }}
7. NÃO use comentários ou texto extra

Decomponha em subtarefas CONCRETAS, EXECUTÁVEIS e ATÔMICAS. Retorne APENAS JSON:

{{
    "ondas": [
        {{
            "numero": 1,
            "descricao": "descrição clara",
            "subtarefas": [
                {{
                    "id": "1.1",
                    "titulo": "título curto",
                    "descricao": "descrição específica",
                    "ferramentas": ["ferramenta1"],
                    "input": "input esperado",
                    "output_esperado": "output produzido",
                    "criterio_sucesso": "validação",
                    "tokens_estimados": 5000,
                    "tempo_estimado": "30s",
                    "prioridade": "critica",
                    "dependencias": []
                }}
            ],
            "pode_executar_paralelo": false
        }}
    ],
    "total_subtarefas": 1,
    "tempo_estimado_sequencial": "tempo seq",
    "tempo_estimado_paralelo": "tempo par"
}}

RESPONDA APENAS COM JSON VÁLIDO. SEM TEXTO ADICIONAL ANTES OU DEPOIS.'''
```

**Vantagens**:
- ✅ Sem novas dependências
- ✅ Simples (apenas modificação de prompt)
- ✅ Pode reduzir taxa de erro

**Desvantagens**:
- ❌ Não garante 100% de sucesso (API pode ignorar)
- ❌ Não resolve JSONs já malformados

---

### Solução 3: Reduzir Tamanho da Resposta (PALIATIVO)

**Simplificar schema JSON esperado**:
```python
# Schema simplificado (menos campos = menos chance de erro)
prompt = f'''...retorne JSON SIMPLIFICADO:

{{
    "ondas": [
        {{
            "numero": 1,
            "titulo": "título da onda",
            "tarefas": [
                {{
                    "id": "1.1",
                    "descricao": "o que fazer",
                    "resultado_esperado": "o que produzir"
                }}
            ],
            "paralelo": false
        }}
    ],
    "total": 0
}}'''
```

**Vantagens**:
- ✅ JSON menor = menos chance de erro
- ✅ Mais rápido (menos tokens)
- ✅ Simples de implementar

**Desvantagens**:
- ❌ Perda de informação valiosa (ferramentas, estimativas, etc.)
- ❌ Não resolve problema raiz

---

## 🎯 RECOMENDAÇÃO FINAL

**Implementar Solução 1 + Solução 2 COMBINADAS**:

1. **Curto prazo** (5 min): Aplicar **Solução 2** (prompt mais restritivo)
   - Adicionar instruções explícitas de formatação JSON
   - Pode reduzir taxa de falha de 50% para ~20-30%

2. **Médio prazo** (30 min): Implementar **Solução 1** (JSON repair)
   - Instalar `json_repair`: `pip install json-repair`
   - Adicionar fallbacks de recuperação
   - Salvar JSONs falhos para análise

3. **Longo prazo** (2h): Refatorar sistema de planejamento
   - Considerar usar formato mais simples (YAML, TOML)
   - Validação estrutural antes de retornar
   - Telemetria de falhas por fase

---

## 📊 IMPACTO E PRIORIZAÇÃO

| Aspecto | Avaliação |
|---------|-----------|
| **Gravidade** | 🔴 CRÍTICA |
| **Frequência** | 🟡 ALTA (50% das execuções) |
| **Impacto** | 🔴 BLOQUEANTE (0 tarefas executadas) |
| **Usuários Afetados** | 🔴 100% (qualquer tarefa complexa) |
| **Prioridade** | 🔴 P0 - URGENTE |

**Estimativa de Esforço**:
- Solução 2 (prompt): ~5-10 minutos
- Solução 1 (repair): ~30-45 minutos
- Solução 3 (simplificação): ~15-20 minutos
- Refatoração completa: ~2-4 horas

**ROI**:
- **Alto** - Desbloqueia funcionalidade crítica (planejamento)
- **Essencial** - Sem isso, 12 tarefas planejadas = 0 executadas

---

## 🔬 EVIDÊNCIAS ADICIONAIS

### Comparação Plano BOM vs FALHO

| Métrica | Plano BOM (173216) | Plano FALHO (181913) | Diferença |
|---------|-------------------|---------------------|-----------|
| **Tamanho** | 23KB | 9.6KB | -58% |
| **Ondas** | 5 | 0 | -100% |
| **Subtarefas** | 5 | 0 | -100% |
| **Fase 1 OK?** | ✅ | ✅ | Igual |
| **Fase 2 OK?** | ✅ | ✅ | Igual |
| **Fase 3 OK?** | ✅ | ❌ | **DIFERENÇA** |

### Logs de Erro Detalhados

**Execução 82b7e2** (mais recente):
```
📋 FASE 3/3: Decomposição em Subtarefas Executáveis...
   ⚠️  Tentativa 1: Erro ao parsear JSON (Expecting ',' delimiter: line 1 column 13279 (char 13278))
   ⚠️  Erro ao parsear JSON da decomposição após 2 tentativas: Expecting ':' delimiter: line 1 column 6700 (char 6699)
   ✓ Total de ondas: 0
   ✓ Total de subtarefas: 0
```

**Análise**:
- Tentativa 1 falhou em ~13KB de JSON (provavelmente truncado)
- Tentativa 2 falhou em ~6.7KB (metade do tamanho)
- Ambos com erros de sintaxe (`:` ou `,` faltando)

---

## ✅ PRÓXIMOS PASSOS IMEDIATOS

1. **AGORA** (5 min): Aplicar Solução 2 (prompt mais restritivo)
2. **HOJE** (30 min): Instalar `json_repair` e implementar Solução 1
3. **VALIDAR** (15 min): Re-executar suite 12 tarefas
4. **DOCUMENTAR** (10 min): Atualizar relatórios com resultados

---

**Preparado por**: Claude Code
**Data**: 2025-10-23 21:35 UTC
**Execuções analisadas**: b6d02d, 8be6cc, 9a70f9, 82b7e2
**Status**: 🔴 **BUG CRÍTICO CONFIRMADO - CORREÇÃO URGENTE NECESSÁRIA**
