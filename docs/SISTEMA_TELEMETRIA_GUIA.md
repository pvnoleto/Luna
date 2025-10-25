# 📊 SISTEMA DE TELEMETRIA E ANÁLISE - GUIA COMPLETO

## 🎯 Visão Geral

O **Sistema de Telemetria** é uma solução completa de monitoramento, análise e otimização automática da Luna V3. Ele registra todas as operações, analisa padrões de uso, detecta gargalos e sugere otimizações baseadas em dados reais.

**Criado:** 2025-10-20
**Versão:** 1.0
**Parte do sistema de melhorias Luna V3**

---

## 🆚 Diferença dos Logs Existentes

| Aspecto | Logs Antigos | Sistema de Telemetria |
|---------|--------------|----------------------|
| **Escopo** | Logs fragmentados (auto_modificacoes.log, workspace.log) | Centralizado e estruturado |
| **Formato** | Texto livre | JSON Lines (JSONL) |
| **Análise** | ❌ Manual | ✅ Automática |
| **Métricas** | ❌ Só em memória (perdidas ao fechar) | ✅ Persistidas em arquivo |
| **Sugestões** | ❌ Não | ✅ Otimizações automáticas |
| **Regressões** | ❌ Não detecta | ✅ Detecta automaticamente |

---

## 🚀 Funcionalidades

### 1. Registro Automático de Eventos

**Uso de Ferramentas:**
- Nome da ferramenta
- Parâmetros (sanitizados - senhas removidas)
- Tempo de execução
- Resultado (sucesso/erro)
- Mensagem de erro se houver

**Requisições API:**
- Tokens de input e output
- Tokens de cache (read/creation)
- Latência da API
- Modelo usado
- Cache hit (sim/não)

**Sessões:**
- Início e fim
- Duração total
- Total de requisições
- Total de tokens
- Taxa de cache hit
- Ferramentas usadas por tipo
- Economia de tokens
- Número de erros

### 2. Análise Inteligente de Dados

**Detecção de Gargalos:**
- Ferramentas lentas (> 5s médio)
- API lenta (> 10s latência)
- Erros frequentes (> 20% taxa de erro)
- Cache hit rate baixo (< 30%)

**Identificação de Padrões:**
- Top 10 ferramentas mais usadas
- Top 5 ferramentas mais lentas
- Distribuição de uso por hora
- Tendências ao longo do tempo

**Detecção de Regressões:**
- Compara períodos de uso
- Identifica ferramentas que ficaram mais lentas
- Alerta sobre aumentos > 50% no tempo

### 3. Sugestões de Otimização

**Baseadas em dados reais:**
- Priorizadas por impacto + facilidade
- Com exemplos de código
- Específicas para cada gargalo
- Acionáveis imediatamente

### 4. Dashboards e Relatórios

**Métricas em Tempo Real:**
- Sessão atual
- Requisições API
- Tokens consumidos
- Cache hit rate
- Economia de tokens

**Relatório Completo:**
- Gargalos identificados
- Padrões de uso
- Sugestões de otimização
- Regressões detectadas

---

## 📝 Como Usar

### Opção 1: Via Luna (Ferramentas Integradas)

#### 1. Ver Métricas da Sessão Atual

```
Luna, mostre as métricas da sessão atual
```

Luna executará a ferramenta `ver_metricas_sessao` e mostrará:
- Duração da sessão
- Total de requisições
- Total de tokens
- Taxa de cache hit
- Economia de tokens
- Ferramentas usadas
- Erros

#### 2. Analisar Telemetria Completa

```
Luna, analise a telemetria
```

Luna executará `analisar_telemetria` e gerará relatório com:
- Gargalos identificados (com severidade)
- Padrões de uso (top ferramentas)
- Sugestões de otimização
- Regressões detectadas

#### 3. Listar Apenas Gargalos

```
Luna, liste os gargalos de performance
```

Luna executará `listar_gargalos` e mostrará:
- Ferramentas lentas
- API lenta
- Erros frequentes
- Cache hit baixo

#### 4. Obter Sugestões de Otimização

```
Luna, sugira otimizações baseadas nos dados
```

Luna executará `sugerir_otimizacoes` e retornará:
- Top 5 sugestões priorizadas
- Impacto estimado
- Facilidade de implementação
- Exemplos de código

---

### Opção 2: Diretamente via Python

```python
from telemetria_manager import TelemetriaManager, AnalisadorTelemetria

# 1. Iniciar sessão
telemetria = TelemetriaManager()
telemetria.iniciar_sessao()

# 2. Usar normalmente a Luna
# (registros são feitos automaticamente)

# 3. Ver métricas da sessão
metricas = telemetria.obter_metricas_sessao()
print(f"Duração: {metricas['duracao_sessao']:.1f}s")
print(f"Requisições: {metricas['total_requisicoes']}")

# 4. Analisar telemetria
analisador = AnalisadorTelemetria()

# Detectar gargalos
gargalos = analisador.detectar_gargalos()
for g in gargalos:
    print(f"{g.descricao} - Severidade: {g.severidade}")
    print(f"  Sugestão: {g.sugestao_otimizacao}")

# Identificar padrões
padroes = analisador.identificar_padroes_uso()
print(f"\nTop 5 ferramentas mais usadas:")
for f in padroes['ferramentas_mais_usadas'][:5]:
    print(f"  {f['ferramenta']}: {f['usos']} usos")

# Sugestões de otimização
sugestoes = analisador.sugerir_otimizacoes()
for s in sugestoes[:3]:
    print(f"\n{s.titulo}")
    print(f"  {s.descricao}")
    print(f"  Impacto: {s.impacto_estimado} | Facilidade: {s.facilidade_implementacao}")

# Detectar regressões
regressoes = analisador.detectar_regressoes()
if regressoes:
    print("\nRegressões detectadas:")
    for r in regressoes:
        print(f"  {r['ferramenta']}: {r['tempo_antigo']:.2f}s -> {r['tempo_novo']:.2f}s (+{r['aumento_percentual']:.1f}%)")

# 5. Finalizar sessão
telemetria.finalizar_sessao()
```

---

## 📊 Exemplo de Output

### Métricas da Sessão:

```
============================================================
MÉTRICAS DA SESSÃO ATUAL
============================================================
Duração: 125.3s
Requisições API: 8
Total de tokens: 15,420
Taxa de cache hit: 62.5%
Economia (tokens): 3,200
Ferramentas usadas: 24
Erros: 1
============================================================
```

### Análise Completa:

```
==============================================================================
📊 RELATÓRIO DE ANÁLISE DE TELEMETRIA - LUNA V3
==============================================================================
Gerado em: 2025-10-20 14:30:45

🚨 GARGALOS IDENTIFICADOS
------------------------------------------------------------------------------

🟠 Ferramenta 'bash' está lenta (Severidade: media)
   Tipo: ferramenta_lenta
   Métricas: {'tempo_medio': 6.8, 'tempo_max': 15.2, 'execucoes': 12}
   💡 Sugestão: Considere otimizar 'bash' ou executar em paralelo. Tempo médio: 6.8s

🟡 Taxa de cache hit está baixa (Severidade: media)
   Tipo: cache_baixo
   Métricas: {'taxa_cache_hit': 28.5, 'cache_hits': 2, 'total_requisicoes': 7}
   💡 Sugestão: Taxa de cache: 28.5%. Considere usar prompt caching em contextos repetidos.

📈 PADRÕES DE USO
------------------------------------------------------------------------------

🔧 Top 5 Ferramentas Mais Usadas:
   1. bash: 12 usos
   2. ler_arquivo: 8 usos
   3. criar_arquivo: 5 usos
   4. listar_arquivos: 3 usos
   5. navegador_ir: 2 usos

⏱️  Top 5 Ferramentas Mais Lentas:
   1. bash: 6.80s médio
   2. navegador_screenshot: 3.20s médio
   3. navegador_ir: 2.50s médio
   4. criar_arquivo: 0.15s médio
   5. ler_arquivo: 0.08s médio

📊 Total de eventos analisados: 30

💡 SUGESTÕES DE OTIMIZAÇÃO (Priorizadas)
------------------------------------------------------------------------------

1. 🔥 Aumentar uso de Prompt Caching
   Taxa de cache hit atual: 28.5%. Usar prompt caching pode economizar tokens e reduzir latência.
   Impacto: alto | Facilidade: facil

   Exemplo de código:
   # Marcar blocos de sistema para cache
   system=[
       {
           "type": "text",
           "text": "Contexto grande...",
           "cache_control": {"type": "ephemeral"}
       }
   ]

2. 🟡 Otimizar 'bash' (mais usada)
   Ferramenta mais usada (12 vezes). Qualquer otimização terá grande impacto.
   Impacto: alto | Facilidade: moderada

3. 🟡 Otimizar ferramenta 'bash'
   A ferramenta 'bash' tem tempo médio de 6.8s. Isso pode impactar a experiência do usuário.
   Impacto: medio | Facilidade: moderada

   Exemplo de código:
   # Considere implementar cache para 'bash'
   # ou executar operações pesadas em paralelo
   import asyncio

   async def bash_otimizado():
       # Implementação otimizada
       pass

✅ Nenhuma regressão de performance detectada

==============================================================================
```

---

## 📂 Estrutura de Arquivos

### Arquivos Gerados

```
Luna/
├── luna_telemetria_ferramentas.jsonl  # Uso de ferramentas (JSONL)
├── luna_telemetria_api.jsonl          # Requisições API (JSONL)
└── luna_performance.json               # Sessões (JSON)
```

### Formato JSONL (JSON Lines)

**Ferramenta:**
```json
{"timestamp": "2025-10-20T14:30:45", "ferramenta": "bash", "parametros": {"comando": "ls -la"}, "resultado_tipo": "sucesso", "tempo_execucao": 0.123, "tokens_estimados": 0, "erro_msg": null}
```

**API:**
```json
{"timestamp": "2025-10-20T14:30:46", "tokens_input": 1500, "tokens_output": 800, "tokens_cache_read": 500, "tokens_cache_creation": 0, "cache_hit": true, "tempo_latencia": 2.5, "modelo": "claude-sonnet-4"}
```

### Formato JSON (Sessões)

```json
{
  "sessoes": [
    {
      "timestamp_inicio": "2025-10-20T14:25:00",
      "timestamp_fim": "2025-10-20T14:32:15",
      "duracao_total": 435.2,
      "total_requisicoes": 8,
      "total_tokens_input": 12000,
      "total_tokens_output": 5420,
      "total_ferramentas_usadas": 24,
      "ferramentas_por_tipo": {
        "bash": 12,
        "ler_arquivo": 8,
        "criar_arquivo": 4
      },
      "taxa_cache_hit": 62.5,
      "economia_tokens": 3200,
      "erros_count": 1
    }
  ]
}
```

---

## 🔧 Configuração e Customização

### Limites de Detecção

Edite `telemetria_manager.py` para ajustar thresholds:

```python
# Ferramenta lenta
if tempo_medio > 5.0:  # Ajuste aqui (segundos)
    # Gargalo detectado

# API lenta
if latencia_media > 10.0:  # Ajuste aqui (segundos)
    # Gargalo detectado

# Taxa de erro alta
if taxa_erro > 20:  # Ajuste aqui (percentual)
    # Gargalo detectado

# Cache hit baixo
if cache_rate < 30:  # Ajuste aqui (percentual)
    # Gargalo detectado
```

### Histórico de Eventos

```python
# Limitar eventos analisados
analisador.detectar_gargalos(limite_eventos=1000)  # Padrão: 1000

# Analisar período específico
eventos_recentes = analisador.carregar_eventos_ferramentas(limite=500)
```

### Histórico de Sessões

```python
# Manter últimas N sessões
data['sessoes'] = data['sessoes'][-50:]  # Padrão: 50
```

---

## 🛡️ Privacidade e Segurança

### Sanitização Automática

O sistema **remove automaticamente** dados sensíveis dos logs:

```python
campos_sensiveis = {'senha', 'password', 'token', 'api_key', 'secret', 'credential'}

# Exemplo:
parametros = {'senha': 'abc123'}
# Salvo como: {'senha': '***REDACTED***'}
```

### Truncamento de Dados

- Parâmetros > 200 chars: Truncados
- Resultados: Primeiros 200 chars apenas
- Outputs de erro: Primeiros 500 chars

### Dados NÃO Registrados

❌ Senhas
❌ Tokens de API
❌ Secrets
❌ Credenciais
❌ Conteúdo completo de arquivos grandes

### Dados Registrados

✅ Nome da ferramenta
✅ Tempo de execução
✅ Tipo de resultado (sucesso/erro)
✅ Tokens consumidos
✅ Cache hit rate
✅ Métricas agregadas

---

## 📈 Casos de Uso

### 1. Identificar Ferramentas Lentas

```python
analisador = AnalisadorTelemetria()
gargalos = analisador.detectar_gargalos()

for g in gargalos:
    if g.tipo == 'ferramenta_lenta':
        print(f"Ferramenta lenta: {g.descricao}")
        print(f"Tempo médio: {g.metricas['tempo_medio']}s")
```

### 2. Otimizar Cache Hit Rate

```python
padroes = analisador.identificar_padroes_uso()
gargalos = analisador.detectar_gargalos()

cache_baixo = [g for g in gargalos if g.tipo == 'cache_baixo']
if cache_baixo:
    print(f"Taxa atual: {cache_baixo[0].metricas['taxa_cache_hit']:.1f}%")
    print("Sugestão: Adicionar cache_control aos blocos de sistema")
```

### 3. Monitorar Regressões

```python
# Executar após cada atualização
regressoes = analisador.detectar_regressoes(janela_antiga=100, janela_nova=100)

if regressoes:
    print("ALERTA: Regressões detectadas!")
    for r in regressoes:
        print(f"  {r['ferramenta']}: +{r['aumento_percentual']:.1f}% mais lento")
```

### 4. Gerar Relatório Periódico

```python
# Executar diariamente/semanalmente
relatorio = analisador.gerar_relatorio_completo()

# Salvar ou enviar por email
with open('relatorio_semanal.txt', 'w') as f:
    f.write(relatorio)
```

---

## 🐛 Troubleshooting

### "Nenhum evento para analisar"

✅ **Solução**: Use a Luna primeiro para gerar eventos de telemetria.

### "Arquivo de log não encontrado"

✅ **Solução**: Telemetria cria arquivos automaticamente na primeira execução. Se não existirem, execute `telemetria.iniciar_sessao()`.

### Métricas não batem com expectativa

✅ **Solução**: Verifique se `telemetria.iniciar_sessao()` foi chamado no início e `telemetria.finalizar_sessao()` no fim.

### Análise muito lenta

✅ **Solução**: Limite eventos analisados: `detectar_gargalos(limite_eventos=500)`.

### UnicodeEncodeError no Windows

✅ **Solução**: Já tratado no código com configuração UTF-8. Se persistir, verifique variável de ambiente `PYTHONUTF8=1`.

---

## 💡 Boas Práticas

1. **Execute análises regularmente**: Semanal ou após grandes mudanças
2. **Monitore regressões**: Compare períodos antes/depois de otimizações
3. **Priorize sugestões de alto impacto**: Foque nas que economizam mais tokens/tempo
4. **Valide mudanças**: Execute análise antes e depois de implementar sugestões
5. **Mantenha histórico**: Não delete os arquivos .jsonl (são leves)
6. **Use cache agressivamente**: Taxa ideal > 50%

---

## 🔄 Integração com Outros Sistemas

### Auto-Evolução

O detector de melhorias pode usar telemetria para sugestões:

```python
# Futura integração
if self.detector_melhorias:
    sugestoes_telemetria = self.analisador_telemetria.sugerir_otimizacoes()
    self.detector_melhorias.adicionar_sugestoes(sugestoes_telemetria)
```

### Dashboard de Métricas

```python
# Futura integração com dashboard_metricas.py
if self.dashboard:
    metricas = self.telemetria.obter_metricas_sessao()
    self.dashboard.atualizar_metricas(metricas)
```

---

## 📚 Documentação Adicional

- **Código fonte**: `telemetria_manager.py`
- **Integração com Luna**: `luna_v3_FINAL_OTIMIZADA.py` (linhas 265-271, 2235-2238, 2830-2950, 3417-3447, 4030-4070, 5210-5212, 5244-5247)
- **Análise do sistema atual**: `docs/ANALISE_SISTEMA_LOGS.md`

---

## ✅ Conclusão

O Sistema de Telemetria da Luna V3:
- ✅ Registra automaticamente todas as operações
- ✅ Analisa padrões e detecta gargalos
- ✅ Sugere otimizações baseadas em dados
- ✅ Detecta regressões de performance
- ✅ Protege privacidade (sanitização automática)
- ✅ 100% integrado e testado

**Use regularmente** para manter a Luna sempre otimizada!

---

**Criado por:** Luna V3 (Claude + Anthropic)
**Data:** 2025-10-20
**Versão:** 1.0
