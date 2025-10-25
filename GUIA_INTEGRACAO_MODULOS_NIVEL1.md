# GUIA DE INTEGRAÇÃO - MÓDULOS NÍVEL 1

**Data**: 24 de Outubro de 2025
**Versão**: Luna V3 - Módulos Nível 1
**Status**: 📘 GUIA COMPLETO DE INTEGRAÇÃO

---

## 📋 SUMÁRIO

Este guia explica como integrar os 4 módulos auxiliares de Nível 1 ao Luna V3:

1. **Dashboard de Métricas** (`dashboard_metricas.py`) - Visualização em tempo real
2. **Parameter Tuner** (`parameter_tuner.py`) - Auto-tuning de parâmetros
3. **Massive Context Analyzer** (`massive_context_analyzer.py`) - Análise paralela de repositórios
4. **Rollback Manager** (`rollback_manager.py`) - Rollback inteligente

---

## 🎯 VISÃO GERAL

### Arquitetura de Integração

```
┌─────────────────────────────────────────────────┐
│       Luna V3 (luna_v3_FINAL_OTIMIZADA.py)      │
│                                                   │
│  ┌────────────────────────────────────────┐     │
│  │     AgenteCompletoV3 (Core)            │     │
│  └────────────────────────────────────────┘     │
│           │                                       │
│           ├─► 🔧 Detector Melhorias (já integrado)│
│           ├─► 🧠 Sistema Auto-Evolução (já integrado)│
│           │                                       │
│           └─► NOVOS MÓDULOS (Nível 1):           │
│                                                   │
│               ┌──────────────────────┐            │
│               │ 📊 Dashboard Métricas│            │
│               │ (dashboard_metricas) │            │
│               └──────────────────────┘            │
│                       ↑                           │
│                       │ Coleta métricas           │
│               ┌──────────────────────┐            │
│               │ ⚙️ Parameter Tuner    │            │
│               │ (parameter_tuner)    │            │
│               └──────────────────────┘            │
│                       ↑                           │
│                       │ Ajusta thresholds         │
│               ┌──────────────────────┐            │
│               │ 🔍 Context Analyzer  │            │
│               │ (massive_context)    │            │
│               └──────────────────────┘            │
│                       ↑                           │
│                       │ Análise paralela          │
│               ┌──────────────────────┐            │
│               │ 🔄 Rollback Manager  │            │
│               │ (rollback_manager)   │            │
│               └──────────────────────┘            │
│                       ↑                           │
│                       │ Protege auto-evolução     │
└─────────────────────────────────────────────────┘
```

### Modo de Integração

Todos os módulos seguem o padrão de **integração opcional**:
- ✅ **Graceful degradation**: Sistema funciona sem os módulos
- ✅ **Import dinâmico**: Carregados apenas se disponíveis
- ✅ **Standalone**: Podem ser usados independentemente
- ✅ **Zero breaking changes**: Não quebram funcionalidade existente

---

## 1️⃣ DASHBOARD DE MÉTRICAS

### 📘 Descrição

Visualiza métricas em tempo real durante a execução de tarefas:
- Cache hit rate e economia de tokens
- Quality scores com tendência
- Batch processing stats
- Auto-melhorias aplicadas
- Token usage e custo estimado

### 📦 Instalação

**Dependências opcionais** (para dashboard Rich):
```bash
pip install rich
```

**Sem Rich**: Dashboard funciona em modo simples (plain text)

### 🔌 Integração no Luna V3

**Opção A: Integração Automática** (recomendado)

Adicionar no `__init__` de `AgenteCompletoV3` (`luna_v3_FINAL_OTIMIZADA.py`):

```python
# Após inicialização dos sistemas existentes (linha ~1830)

# 📊 Dashboard de Métricas (opcional)
try:
    from dashboard_metricas import MetricsDashboard
    self.dashboard = MetricsDashboard(agente=self, modo="auto")
    print("📊 Dashboard de Métricas: ATIVADO")
except ImportError:
    self.dashboard = None
    print("📊 Dashboard de Métricas: NÃO DISPONÍVEL")
```

**Opção B: Uso Manual** (para testes)

```python
from dashboard_metricas import MetricsDashboard

# Inicializar
dashboard = MetricsDashboard(agente=None, modo="simple")

# Atualizar métricas manualmente
dashboard.metricas['cache']['total_requests'] = 10
dashboard.metricas['cache']['cache_hits'] = 8
dashboard.metricas['cache']['tokens_economizados'] = 5000

# Exibir
dashboard.exibir()
```

### 📊 Pontos de Coleta de Métricas

**1. Cache (após cada chamada API)**

No método `_executar_chamada_api()` (linha ~2700):

```python
# Após processar response
if self.dashboard:
    # Atualizar métricas de cache
    self.dashboard.metricas['cache']['total_requests'] += 1

    if hasattr(response, 'usage'):
        # Cache hit
        if getattr(response.usage, 'cache_read_input_tokens', 0) > 0:
            self.dashboard.metricas['cache']['cache_hits'] += 1
            self.dashboard.metricas['cache']['tokens_economizados'] += (
                response.usage.cache_read_input_tokens
            )
        else:
            self.dashboard.metricas['cache']['cache_misses'] += 1

    # Exibir atualização (opcional)
    if self.metricas['cache']['total_requests'] % 5 == 0:  # A cada 5 requests
        self.dashboard.exibir()
```

**2. Quality Scores (após cada iteração)**

No método `executar_tarefa()` após calcular `quality_score`:

```python
if self.dashboard and quality_score > 0:
    self.dashboard.metricas['quality']['scores'].append(quality_score)
    self.dashboard.metricas['quality']['current_score'] = quality_score
    self.dashboard.metricas['quality']['best_score'] = max(
        self.dashboard.metricas['quality']['best_score'],
        quality_score
    )
    # Recalcular média
    scores = self.dashboard.metricas['quality']['scores']
    self.dashboard.metricas['quality']['avg_score'] = sum(scores) / len(scores)
```

**3. Tokens (global)**

Adicionar contador global no `__init__`:

```python
self.total_tokens_usados = 0
self.total_custo_usd = 0.0
```

Atualizar após cada request:

```python
if hasattr(response, 'usage'):
    tokens_input = response.usage.input_tokens
    tokens_output = response.usage.output_tokens

    self.total_tokens_usados += (tokens_input + tokens_output)

    # Custo estimado (Claude Sonnet 4.5)
    # $3.00 / 1M input tokens, $15.00 / 1M output tokens
    custo = (tokens_input / 1_000_000 * 3.0) + (tokens_output / 1_000_000 * 15.0)
    self.total_custo_usd += custo

    if self.dashboard:
        self.dashboard.metricas['tokens']['total_usados'] = self.total_tokens_usados
        self.dashboard.metricas['tokens']['custo_total_usd'] = self.total_custo_usd
```

### 🎨 Modos de Exibição

**Modo Rich** (se `rich` instalado):
- Dashboard interativo atualizado em tempo real
- Cores e formatação profissional
- Tabelas e barras de progresso

**Modo Simple** (fallback):
- Output em texto simples
- Sem cores ou formatação especial
- Compatível com todos os terminais

**Modo Silent**:
- Apenas coleta dados sem exibir
- Útil para execuções em background

### 📈 Exemplo de Output

**Modo Simple**:
```
====================================
📊 DASHBOARD DE MÉTRICAS
====================================

🔵 CACHE:
   Total Requests: 15
   Cache Hits: 12 (80.0%)
   Cache Misses: 3 (20.0%)
   Tokens Economizados: 45,230
   Custo Economizado: $0.14

🟢 QUALITY:
   Current Score: 92.5
   Best Score: 95.0
   Average Score: 91.2

🟡 TOKENS:
   Total Usado: 8,540
   Custo Total: $0.09
```

---

## 2️⃣ PARAMETER TUNER

### 📘 Descrição

Auto-tuning de parâmetros do Luna V3 baseado em histórico de performance:
- Ajusta `quality_threshold`, `batch_threshold`, `stagnation_limit`, `timeout_iteracao_segundos`
- Analisa últimas N execuções
- Sugere valores ótimos por modo (conservador, moderado, agressivo)
- Salva histórico em `tuner_history.json`

### 🔌 Integração no Luna V3

**Opção A: Auto-tuning Periódico**

Adicionar no final do método `executar_tarefa()` (após sucesso):

```python
# Auto-tuning periódico (a cada 10 tarefas)
if hasattr(self, 'contador_tarefas'):
    self.contador_tarefas += 1
else:
    self.contador_tarefas = 1

if self.contador_tarefas % 10 == 0:  # A cada 10 tarefas
    try:
        from parameter_tuner import ParameterTuner
        tuner = ParameterTuner()

        # Salvar execução atual
        tuner.salvar_execucao(
            parametros={
                'quality_threshold': self.quality_threshold,
                'batch_threshold': self.batch_threshold,
                'stagnation_limit': self.stagnation_limit,
                'timeout_iteracao_segundos': self.timeout_iteracao_segundos
            },
            metricas={
                'quality_score': resultado.get('quality_score', 0),
                'tokens_usados': self.total_tokens_usados,
                'tempo_total': resultado.get('tempo_execucao', 0),
                'num_iteracoes': resultado.get('iteracoes_usadas', 0)
            }
        )

        # Sugerir ajustes (modo moderado)
        sugestoes = tuner.sugerir_ajustes(modo="moderado")
        if sugestoes and not sugestoes.get('erro'):
            print("\n⚙️ Parameter Tuner: Ajustes sugeridos disponíveis")
            tuner.exibir_recomendacoes()

            # Aplicar automaticamente? (opcional)
            # tuner.aplicar_ajustes(self, modo="automatico", auto_confirmar=True)
    except ImportError:
        pass  # Parameter Tuner não disponível
```

**Opção B: Uso Manual via Comando**

Adicionar ferramenta ao sistema:

```python
# No método _criar_ferramentas_codigo()
{
    "name": "auto_tuning",
    "description": "Analisa histórico e sugere ajustes de parâmetros para otimizar performance",
    "input_schema": {
        "type": "object",
        "properties": {
            "modo": {
                "type": "string",
                "description": "Modo: conservador, moderado ou agressivo",
                "enum": ["conservador", "moderado", "agressivo"]
            }
        },
        "required": []
    }
}

# No método executar()
elif nome == "auto_tuning":
    try:
        from parameter_tuner import ParameterTuner
        tuner = ParameterTuner()
        modo = parametros.get('modo', 'moderado')

        # Analisar histórico
        analise = tuner.analisar_historico()

        # Sugerir ajustes
        sugestoes = tuner.sugerir_ajustes(modo=modo)

        # Exibir
        tuner.exibir_recomendacoes()

        return json.dumps({
            'analise': analise,
            'sugestoes': sugestoes
        }, indent=2, ensure_ascii=False)
    except ImportError:
        return "❌ Parameter Tuner não disponível (verifique parameter_tuner.py)"
```

### 📊 Exemplo de Uso

```python
from parameter_tuner import ParameterTuner

# Inicializar
tuner = ParameterTuner(history_file="tuner_history.json")

# Salvar execução
tuner.salvar_execucao(
    parametros={
        'quality_threshold': 90,
        'batch_threshold': 50
    },
    metricas={
        'quality_score': 88,
        'tokens_usados': 5000,
        'tempo_total': 45,
        'num_iteracoes': 8
    }
)

# Analisar histórico (últimas 10 execuções)
analise = tuner.analisar_historico(ultimas_n=10)

# Sugerir ajustes
sugestoes = tuner.sugerir_ajustes(modo="moderado")

# Exibir recomendações
tuner.exibir_recomendacoes()

# Aplicar ajustes (com confirmação)
aplicados = tuner.aplicar_ajustes(agente, modo="manual", auto_confirmar=False)
```

### 📈 Output Exemplo

```
======================================================================
📊 AUTO-TUNING RECOMENDAÇÕES
======================================================================

quality_threshold:
   Atual: 90
   Sugerido: 87
   Motivo: Qualidade média alta (88.5). Podemos reduzir threshold.
   Ganho esperado: 10-15% menos iterações

batch_threshold:
   Atual: 50
   Sugerido: 40
   Motivo: Tarefas pequenas (média 7.2 iterações). Batch pode processar menos.
   Ganho esperado: 20-30% mais tarefas usando batch

======================================================================
```

---

## 3️⃣ MASSIVE CONTEXT ANALYZER

### 📘 Descrição

Análise paralela de repositórios grandes (300-400 arquivos):
- Usa `ThreadPoolExecutor` para processamento paralelo
- Suporta múltiplos tipos de arquivo (*.py, *.js, *.md, etc)
- Agrega estatísticas (linhas, tamanho, etc)
- Speedup estimado: 10-15x vs sequencial

### 🔌 Integração no Luna V3

**Adicionar Ferramenta**:

```python
# No método _criar_ferramentas_codigo()
{
    "name": "analyze_repository",
    "description": "Analisa repositório completo em paralelo (300-400 arquivos). Retorna estatísticas agregadas.",
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Caminho do diretório a analisar"
            },
            "file_types": {
                "type": "array",
                "description": "Tipos de arquivo (ex: ['*.py', '*.js'])",
                "items": {"type": "string"}
            },
            "max_files": {
                "type": "number",
                "description": "Máximo de arquivos (padrão: 400)"
            }
        },
        "required": ["path"]
    }
}

# No método executar()
elif nome == "analyze_repository":
    try:
        from massive_context_analyzer import MassiveContextAnalyzer

        path = parametros.get('path', '.')
        file_types = parametros.get('file_types', ['*.py'])
        max_files = parametros.get('max_files', 400)

        analyzer = MassiveContextAnalyzer(agente=self, max_workers=10)

        results = analyzer.analyze_repository(
            path=path,
            file_types=file_types,
            max_files=max_files,
            operation="summary"
        )

        return json.dumps(results, indent=2, ensure_ascii=False)
    except ImportError:
        return "❌ MassiveContextAnalyzer não disponível"
```

### 📊 Exemplo de Uso

```python
from massive_context_analyzer import MassiveContextAnalyzer

# Inicializar (10 workers paralelos)
analyzer = MassiveContextAnalyzer(max_workers=10)

# Analisar repositório Python
results = analyzer.analyze_repository(
    path="/mnt/c/Projetos/Luna",
    file_types=["*.py"],
    max_files=400,
    operation="summary"
)

# Resultados
print(f"Total: {results['total']} arquivos")
print(f"Sucesso: {results['success']}")
print(f"Linhas: {results['total_lines']:,}")
print(f"Tamanho: {results['total_size_kb']:.1f} KB")
print(f"Tempo: {results['elapsed_seconds']:.1f}s")
print(f"Speedup: {results['speedup']}")
```

### 📈 Output Exemplo

```
🔍 Analisando repositório: /mnt/c/Projetos/Luna
   Tipos: ['*.py'], Max: 400
   ✅ 87 arquivos encontrados

✅ Análise completa em 3.2s
   Speedup: 27.2 arquivos/s

📊 RESULTADOS:
   Total: 87
   Sucesso: 87
   Linhas: 45,230
   Tamanho: 892.5 KB
   Tempo: 3.2s
   Speedup: 27.2 arquivos/s
```

---

## 4️⃣ ROLLBACK MANAGER

### 📘 Descrição

Sistema de rollback inteligente para auto-evolução:
- Cria snapshots antes de modificações
- Valida sintaxe antes de aplicar
- Rollback automático se testes falharem
- Mantém histórico de snapshots

### 🔌 Integração com Sistema Auto-Evolução

**Modificar `sistema_auto_evolucao.py`**:

```python
# No método aplicar_melhoria()

# Importar RollbackManager
from rollback_manager import RollbackManager

# Inicializar (uma vez no __init__)
self.rollback_manager = RollbackManager(backup_dir=".rollback_backups")

# Antes de aplicar melhoria
def aplicar_melhoria(self, caminho_arquivo: str, melhoria: Dict) -> bool:
    # Ler código original
    codigo_original = Path(caminho_arquivo).read_text(encoding='utf-8')

    # Aplicar modificação (gerar código novo)
    codigo_novo = self._aplicar_modificacao(codigo_original, melhoria)

    # Aplicar com rollback inteligente
    sucesso, codigo_final, mensagem = self.rollback_manager.apply_with_rollback(
        codigo_original=codigo_original,
        codigo_novo=codigo_novo,
        run_tests=lambda c: self._validar_codigo(c)  # Sua função de validação
    )

    if sucesso:
        # Salvar código final
        Path(caminho_arquivo).write_text(codigo_final, encoding='utf-8')
        print(f"✅ Melhoria aplicada: {melhoria['tipo']}")
        return True
    else:
        print(f"❌ Rollback executado: {mensagem}")
        return False
```

### 📊 Exemplo de Uso Standalone

```python
from rollback_manager import RollbackManager

# Inicializar
manager = RollbackManager(backup_dir=".rollback_backups")

# Código original
codigo_original = '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
'''

# Código novo (otimizado)
codigo_novo = '''
def fibonacci(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci(n-1, memo) + fibonacci(n-2, memo)
    return memo[n]
'''

# Função de teste (opcional)
def run_tests(codigo):
    # Executar testes
    exec(codigo)
    # Se chegar aqui, código é válido
    return fibonacci(10) == 55  # Teste simples

# Aplicar com rollback automático
sucesso, codigo_final, msg = manager.apply_with_rollback(
    codigo_original=codigo_original,
    codigo_novo=codigo_novo,
    run_tests=run_tests
)

if sucesso:
    print("✅ Código aplicado com sucesso!")
else:
    print(f"❌ Rollback: {msg}")
```

### 📈 Output Exemplo

```
📸 Snapshot criado: snapshot_pre_apply_20251024_013045.py
✅ Validação OK - mudança aplicada
✅ Código aplicado com sucesso!
```

**Com erro**:
```
📸 Snapshot criado: snapshot_pre_apply_20251024_013102.py
❌ Código novo tem erro de sintaxe
🔄 Rollback executado: snapshot_pre_apply_20251024_013102.py
❌ Rollback: Erro de sintaxe - rollback executado
```

---

## 🔗 FLUXO DE INTEGRAÇÃO COMPLETO

### Cenário: Execução com Todos os Módulos

```python
# 1. Inicializar Luna V3 com módulos
agente = AgenteCompletoV3(
    api_key=os.getenv('ANTHROPIC_API_KEY'),
    tier=2,
    modo_rate_limit='balanceado'
)

# Módulos carregados automaticamente via graceful degradation:
# ✅ Dashboard (se disponível)
# ✅ Parameter Tuner (se disponível)

# 2. Executar tarefa
resultado = agente.executar_tarefa("Analisar repositório completo")

# Durante execução:
# - Dashboard coleta métricas em tempo real
# - Parameter Tuner salva performance da tarefa
# - Massive Context Analyzer processa 400 arquivos em paralelo
# - Rollback Manager protege auto-melhorias

# 3. Após 10 tarefas, auto-tuning automático:
# - Parameter Tuner analisa histórico
# - Sugere ajustes (quality_threshold: 90 → 87)
# - Usuário confirma aplicação

# 4. Exibir métricas finais:
if agente.dashboard:
    agente.dashboard.exibir()
```

---

## ⚙️ CONFIGURAÇÃO RECOMENDADA

### Mínima (Sem Módulos)

```
Luna V3 standalone
- Funcionalidade completa
- Sem visualização avançada
- Sem auto-tuning
- Sem análise paralela massiva
```

### Padrão (Com Módulos Básicos)

```bash
# Instalar Luna V3
# Módulos incluídos: dashboard, parameter_tuner, massive_context, rollback

# Sem dependências extras
pip install anthropic python-dotenv
```

### Avançada (Com Rich Dashboard)

```bash
# Instalar com Rich para dashboard interativo
pip install anthropic python-dotenv rich
```

---

## 📊 TESTES DE VALIDAÇÃO

### Testar Dashboard

```bash
python -c "from dashboard_metricas import MetricsDashboard; d = MetricsDashboard(); d.exibir(); print('✅ OK')"
```

### Testar Parameter Tuner

```bash
python parameter_tuner.py
# Deve exibir: ✅ Testes concluídos!
```

### Testar Massive Context Analyzer

```bash
python massive_context_analyzer.py
# Deve exibir: ✅ Melhoria 1.3: FUNCIONAL
```

### Testar Rollback Manager

```bash
python rollback_manager.py
# Deve exibir: ✅ Melhoria 1.4: FUNCIONAL
```

---

## 🚀 PRÓXIMOS PASSOS

### Fase 1: Integração Básica (ATUAL)
- ✅ Módulos criados e testados standalone
- ✅ Guia de integração completo
- ⏳ Integração funcional no luna_v3_FINAL_OTIMIZADA.py

### Fase 2: Integração Avançada
- Dashboard em tempo real durante execução
- Auto-tuning periódico automático
- Rollback integrado ao sistema auto-evolução

### Fase 3: Otimizações
- Dashboard com gráficos (usando plotext)
- Parameter Tuner com ML (sklearn)
- Análise semântica de código (AST avançado)

---

## 📚 REFERÊNCIAS

### Arquivos do Projeto

- `luna_v3_FINAL_OTIMIZADA.py` - Sistema principal
- `dashboard_metricas.py` - Dashboard de métricas (449 linhas)
- `parameter_tuner.py` - Auto-tuning (377 linhas)
- `massive_context_analyzer.py` - Análise paralela (157 linhas)
- `rollback_manager.py` - Sistema de rollback (182 linhas)

### Documentação Relacionada

- `CLAUDE.md` - Guia principal do projeto
- `RELATORIO_VALIDACAO_PLANNING_BUGFIX.md` - Validação do bug fix
- `RELATORIO_IMPLEMENTACAO_TIMEOUTS.md` - Sistema de timeouts

---

**Criado por**: Claude Code (Anthropic)
**Data**: 24 de Outubro de 2025
**Versão**: 1.0 - Guia Completo de Integração
