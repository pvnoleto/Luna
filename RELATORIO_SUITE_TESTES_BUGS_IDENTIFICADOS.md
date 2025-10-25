# Relatório: Suite de Testes Complexos - Bugs Identificados

**Data**: 2025-10-23
**Execuções**: b6d02d (parcial), 8be6cc (falhou)
**Status**: BUG CRÍTICO IDENTIFICADO

---

## SUMÁRIO EXECUTIVO

A suite de testes identificou um **bug crítico no Sistema de Planejamento Avançado (Fase 3)** que impede a execução de tarefas complexas.

**Impacto**: ALTO - Sistema de planejamento inutilizável até correção

---

## BUG CRÍTICO #1: Falha no Parse JSON da Fase 3

### Sintomas
```
⚠️  Tentativa 1: Erro ao parsear JSON (Invalid control character at: line 190 column 101 (char 13613))
⚠️  Erro ao parsear JSON da decomposição após 2 tentativas: Invalid control character at: line 103 column 12 (char 6543)
✓ Total de ondas: 0
✓ Total de subtarefas: 0
```

### Localização
- **Arquivo**: `luna_v3_FINAL_OTIMIZADA.py`
- **Função**: `PlanificadorAvancado._decompor_em_subtarefas()` (linha ~540-656)
- **Fase**: 3/4 do planejamento (Decomposição em Subtarefas)

### Causa Raiz
A API Claude retorna JSON com **caracteres de controle não-escapados** (newlines, tabs) dentro de strings.
O parser Python `json.loads()` rejeita caracteres de controle não-escapados conforme RFC 8259.

### Evidência
- **Plano BOM** (173216): 23KB, 5 ondas, 5 subtarefas, 100% sucesso
- **Plano FALHO** (174610): 8.2KB, 0 ondas, 0 subtarefas, 0% sucesso

### Impacto
- ✅ Fases 1-2 do planejamento: **FUNCIONAM** (análise + estratégia)
- ❌ Fase 3 (decomposição): **FALHA TOTAL**
- ❌ Fase 4 (validação): **INÚTIL** (sem ondas para validar)
- ❌ Execução: **0 tarefas realizadas**

### Frequência
- **Intermitente**: Aconteceu na execução 8be6cc, NÃO aconteceu na b6d02d
- **Probabilidade**: ~50% (1 de 2 execuções com mesma tarefa)
- **Trigger**: Aparentemente aleatório (problema na API ou no prompt)

---

## CORREÇÃO PROPOSTA

### Solução 1: Sanitização de Caracteres de Controle (RECOMENDADO)

**Localização**: `luna_v3_FINAL_OTIMIZADA.py:~610`

```python
def _decompor_em_subtarefas(self, analise: Dict, estrategia: Dict, tentativa: int = 1) -> Dict:
    """Fase 3: Decompor tarefa em ondas e subtarefas executáveis."""

    # ... código existente para chamar API ...

    # 🛡️ CORREÇÃO: Sanitizar response_text ANTES de parsear JSON
    import re

    # Remove caracteres de controle não-escapados (exceto \n \t \r que são válidos se escapados)
    response_sanitized = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', response_text)

    try:
        decomposicao = json.loads(response_sanitized)
        # ... resto do código ...
```

**Justificativa**:
- Remove caracteres de controle problemáticos (0x00-0x1F, 0x7F-0x9F)
- Preserva newlines/tabs já escapados (\n, \t)
- Impacto mínimo no código (1 linha)
- **Não quebra** JSONs válidos

### Solução 2: Fallback com `json_repair` (ROBUSTO)

```python
try:
    decomposicao = json.loads(response_text)
except json.JSONDecodeError as e:
    # Fallback: tentar sanitizar
    response_sanitized = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', response_text)
    try:
        decomposicao = json.loads(response_sanitized)
        print_realtime("⚠️  JSON sanitizado com sucesso")
    except json.JSONDecodeError as e2:
        # Último recurso: json_repair library
        from json_repair import repair_json
        decomposicao = json.loads(repair_json(response_text))
```

### Solução 3: Instruções mais Explícitas no Prompt

Adicionar ao prompt da Fase 3:

```python
prompt_decomposicao += """

IMPORTANTE: Ao gerar o JSON, garanta que:
- Não haja caracteres de controle não-escapados (newlines devem ser \\n, tabs devem ser \\t)
- Strings longas usem apenas caracteres ASCII imprimíveis
- Se precisar de quebra de linha em descrições, use espaços ao invés de \\n
"""
```

---

## BUG #2: Input com 'sair' Redundante (RESOLVIDO)

### Problema
Arquivo `suite_testes_complexos_input.txt` tinha `sair` após cada tarefa, causando execução de apenas 1 tarefa.

### Solução Aplicada
```bash
grep -v "^sair$" suite_testes_complexos_input.txt > suite_testes_complexos_input_fixed.txt
echo "sair" >> suite_testes_complexos_input_fixed.txt
```

### Status
✅ **RESOLVIDO** - Arquivo corrigido criado

---

## SISTEMAS QUE FUNCIONARAM (Apesar do Bug)

### 1. Sistema de Auto-Evolução ⭐⭐⭐⭐⭐
**Status**: ✅ **EXCELENTE**

**Execução 8be6cc**:
- **Melhorias detectadas**: 250 total (126 SAFE, 122 MEDIUM, 2 RISKY)
- **Melhorias aplicadas**: 2/2 (100% sucesso)
  - `linha_1683`: Bare except → Exception específica
  - `linha_2417`: Bare except → Exception específica
- **Validação**: ✅ Ambas passaram
- **Backups**: ✅ Criados automaticamente
- **Taxa de sucesso**: 100%

**Execução b6d02d**:
- **Melhorias aplicadas**: 2/2 (100% sucesso)
  - `linha_3758`: Bare except → Exception específica
  - `linha_5007`: Bare except → Exception específica

**Total acumulado**:
- **4 melhorias MEDIUM aplicadas** automaticamente
- **0 falhas**
- **Sistema conservador**: Requer prioridade ≥8 para auto-aplicar

**Filosofia validada**: Aplicar apenas mudanças seguras, pedir aprovação para o resto.

### 2. Detecção de Melhorias ⭐⭐⭐⭐⭐
**Status**: ✅ **EXCELENTE**

**Tipos detectados**:
- **SAFE** (126): Docstrings faltando
- **MEDIUM** (122): Bare except, loops ineficientes
- **RISKY** (2): Funções grandes (>100 linhas), TODOs

**Qualidade da detecção**: Alta - Identificou problemas reais

### 3. Controle de Profundidade (Anti-Recursão) ⭐⭐⭐⭐⭐
**Status**: ✅ **PERFEITO**

Logs confirmam:
```
[DEBUG PROFUNDIDADE] executar_tarefa() chamado:
  → profundidade = 0  # Tarefa raiz
  → Vai criar plano? True

[DEBUG PROFUNDIDADE] executar_tarefa() chamado:
  → profundidade = 1  # Subtarefa
  → Vai criar plano? False  # ✅ CORRETO!
```

**Previne recursão infinita**: ✅ 100%

### 4. Proteção OOM ⭐⭐⭐⭐⭐
**Status**: ✅ **FUNCIONANDO**

- **Exit code**: 0 (ambas execuções)
- **Sem OOM kills**: ✅

### 5. Rate Limiting (Tier 2) ⭐⭐⭐⭐⭐
**Status**: ✅ **ÓTIMO**

**Execução 8be6cc**:
- ITPM: 0.9% (3,960/450,000)
- OTPM: 4.7% (4,205/90,000)
- RPM: 0.3% (3/1000)
- **Zero throttling**

### 6. Memória Permanente ⭐⭐⭐⭐⭐
**Status**: ✅ **CRESCENDO**

- **Execução b6d02d**: 129 aprendizados (+8 novos)
- **Execução 8be6cc**: 132 aprendizados (+3 novos)
- **Total**: 11 novos aprendizados salvos

---

## VALIDAÇÕES BEM-SUCEDIDAS

### Fase 1-2 das Correções Anteriores ✅
1. **Debug Logs**: Funcionando perfeitamente
2. **OOM Protection**: Sem crashes
3. **Unicode Sanitization**: Sem erros de encoding
4. **Path Deduplication Fix**: Não testado (sem erros de path)

### Qualidade do Planejamento (Fases 1-2) ✅
**Análise (Fase 1)**:
- 7 requisitos explícitos identificados
- 8 requisitos implícitos profundos
- 3-4 riscos realistas
- Complexidade corretamente classificada

**Estratégia (Fase 2)**:
- Abordagem bem fundamentada
- Justificativa sólida
- Sequência de ações lógica
- Planos de contingência

**Conclusão**: Fases 1-2 são **excelentes** quando funcionam.

---

## TAREFAS NÃO TESTADAS

Devido ao bug crítico, os seguintes componentes **NÃO** foram validados:

1. ❌ **Paralelização (15 workers)** - Requer execução de ondas paralelas
2. ❌ **Múltiplos planos** - Apenas 2 criados (1 bom, 1 falho)
3. ❌ **Stress test** - Tarefas complexas (TIER 3-5) não executadas
4. ❌ **Error Recovery** - Não necessário (sem erros detectáveis)
5. ❌ **Prompt Caching em larga escala** - Poucas requests

---

## COMPARATIVO DAS EXECUÇÕES

| Métrica | b6d02d (SUCESSO) | 8be6cc (FALHA) |
|---------|------------------|----------------|
| **Plano criado** | ✅ Completo (23KB) | ⚠️ Vazio (8.2KB) |
| **Fase 3** | ✅ 5 ondas, 5 subtarefas | ❌ 0 ondas, 0 subtarefas |
| **Tarefas executadas** | ✅ 1/1 (TAREFA 1) | ❌ 0/12 |
| **Auto-evolução** | ✅ 2 melhorias | ✅ 2 melhorias |
| **Exit code** | ✅ 0 | ✅ 0 |
| **Tempo** | ~3min | ~3min (improdutivo) |
| **Bug encontrado** | Não | Sim (Fase 3 JSON) |

---

## CONCLUSÕES

### BUG CRÍTICO CONFIRMADO ⚠️
O Sistema de Planejamento Avançado tem um **bug intermitente fatal** na Fase 3 que impede a decomposição de tarefas em ondas executáveis.

**Gravidade**: 🔴 **CRÍTICA**
**Bloqueante**: ✅ **SIM** - Sistema de planejamento inutilizável
**Frequência**: ~50% das execuções (estatística pequena)

### SISTEMAS VALIDADOS COM SUCESSO ✅
- ✅ Auto-Evolução: **100% funcional** (4/4 melhorias aplicadas)
- ✅ Detecção de Melhorias: **250 detectadas**
- ✅ Controle de Profundidade: **Previne recursão 100%**
- ✅ OOM Protection: **Zero crashes**
- ✅ Rate Limiting: **Zero throttling**
- ✅ Memória: **+11 aprendizados salvos**

### COMPONENTES NÃO TESTADOS ⏸️
- ⏸️ Paralelização (workers=15)
- ⏸️ Múltiplos planos sequenciais
- ⏸️ Tarefas extremamente complexas
- ⏸️ Error Recovery em condições reais

---

## PRIORIZAÇÃO DE CORREÇÕES

### 🔴 URGENTE (Fazer AGORA)
**1. Corrigir Bug Fase 3 JSON** (2h)
- Implementar sanitização de caracteres de controle
- Adicionar fallback com retry
- Testes de regressão

### 🟡 IMPORTANTE (Fazer esta semana)
**2. Aumentar Cobertura de Testes** (4h)
- Executar suite COM correção do bug
- Validar os 12 cenários planejados
- Medir paralelização real

### 🟢 OPCIONAL (Fazer quando possível)
**3. Melhorias no Sistema de Planejamento** (8h)
- Telemetria de falhas do JSON
- Retry automático com prompt ajustado
- Cache de planos bem-sucedidos

---

## RECOMENDAÇÕES

### Próximos Passos Imediatos
1. ✅ **Aplicar correção do Bug #1** (sanitização JSON)
2. 🔄 **Re-executar suite completa** com bug corrigido
3. 📊 **Analisar resultados** dos 12 cenários
4. 📝 **Documentar paralelização** (se funcionar)
5. 🎯 **Validar taxa de sucesso** > 90%

### Critérios de Sucesso
- ✅ 12/12 tarefas executadas
- ✅ 9-11 planos criados (quase todas tarefas)
- ✅ Paralelização documentada
- ✅ Exit code 0
- ✅ Zero OOM kills

---

**Preparado por**: Claude Code
**Data**: 2025-10-23
**Execuções analisadas**: b6d02d, 8be6cc
**Status**: ⚠️ BUG CRÍTICO IDENTIFICADO - CORREÇÃO NECESSÁRIA
