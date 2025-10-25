# PLANO DE IMPLEMENTAÇÃO - TIMEOUTS E PROGRESS LOGGING

## Objetivo
Implementar sistema de timeouts e logging de progresso para prevenir stalls durante execução de tarefas.

## Modificações a Implementar

### 1. Imports Adicionais (Início do Arquivo)
```python
import threading
from typing import Optional, List, Dict, Any, Tuple  # garantir que está importado
```

### 2. Classe de Exceção Customizada (Após imports)
```python
class IterationTimeoutError(Exception):
    """Exceção lançada quando uma iteração excede o tempo limite."""
    pass
```

### 3. Variável de Configuração na Classe AgenteCompletoV3
```python
# Adicionar no __init__ da classe (aproximadamente linha 1100-1200)
self.timeout_iteracao_segundos = 120  # 2 minutos por iteração (padrão)
self.timeout_subtarefa_segundos = 300  # 5 minutos por subtarefa completa
```

### 4. Função de Timeout Helper (Método da Classe)
```python
def _executar_com_timeout(self, func, timeout_segundos=120, descricao="operação"):
    """
    Executa uma função com timeout.

    Args:
        func: Função a executar (sem argumentos, use lambda se necessário)
        timeout_segundos: Timeout em segundos
        descricao: Descrição da operação para logging

    Returns:
        Resultado da função

    Raises:
        IterationTimeoutError: Se timeout for excedido
    """
    resultado = [None]  # Lista para armazenar resultado (mutável)
    excecao = [None]    # Lista para armazenar exceção

    def executar_wrapper():
        try:
            resultado[0] = func()
        except Exception as e:
            excecao[0] = e

    thread = threading.Thread(target=executar_wrapper, daemon=True)
    thread.start()
    thread.join(timeout=timeout_segundos)

    if thread.is_alive():
        print_realtime(f'\n⏱️ TIMEOUT: {descricao} excedeu {timeout_segundos}s')
        raise IterationTimeoutError(f"{descricao} excedeu {timeout_segundos} segundos")

    if excecao[0]:
        raise excecao[0]

    return resultado[0]
```

### 5. Modificação no Loop Principal (Linhas 2698-2774)

**ANTES (linha 2705):**
```python
response = self._executar_chamada_API()
```

**DEPOIS:**
```python
# Logging de início de iteração
inicio_iteracao = time.time()
print_realtime(f'   ⏰ Início: {datetime.now().strftime("%H:%M:%S")}')

try:
    # Executar com timeout
    response = self._executar_com_timeout(
        func=lambda: self._executar_chamada_api(),
        timeout_segundos=self.timeout_iteracao_segundos,
        descricao=f"Iteração {iteracao}/{limite_atual}"
    )

    # Logging de conclusão
    tempo_decorrido = time.time() - inicio_iteracao
    print_realtime(f'   ✅ Concluída em {tempo_decorrido:.1f}s')

except IterationTimeoutError as e:
    print_realtime(f'\n❌ TIMEOUT NA ITERAÇÃO {iteracao}')
    print_realtime(f'   A iteração estava executando há mais de {self.timeout_iteracao_segundos}s')
    print_realtime(f'   Possível causa: operação de ferramenta muito lenta')
    print_realtime('\n❓ Deseja continuar mesmo assim?')
    print_realtime('   [s] Sim, pular esta iteração e continuar')
    print_realtime('   [n] Não, parar execução')

    try:
        escolha = input('\n💬 Escolha: ').strip().lower()
        if escolha == 's':
            print_realtime('⚠️ Pulando iteração com timeout e continuando...')
            continue  # Pula para próxima iteração
        else:
            print_realtime('⏹️ Parando execução devido a timeout')
            self._exibir_estatisticas()
            return None
    except (KeyboardInterrupt, EOFError):
        print_realtime('\n⏹️ Interrompido pelo usuário')
        self._exibir_estatisticas()
        return None
```

### 6. Adicionar Timeout de Subtarefa (Início da Função executar_tarefa)

**ADICIONAR após linha 2605 (após calcular max_iteracoes):**
```python
# Timeout de subtarefa (caso profundidade > 0, é uma subtarefa)
inicio_subtarefa = time.time()
timeout_subtarefa_ativo = (profundidade > 0)

if timeout_subtarefa_ativo:
    print_realtime(f'⏱️ Timeout de subtarefa ativo: {self.timeout_subtarefa_segundos}s máximo')
```

**ADICIONAR no final do loop (antes de linha 2775):**
```python
# Verificar timeout de subtarefa
if timeout_subtarefa_ativo:
    tempo_decorrido_subtarefa = time.time() - inicio_subtarefa
    if tempo_decorrido_subtarefa > self.timeout_subtarefa_segundos:
        print_realtime(f'\n⏱️ TIMEOUT DE SUBTAREFA')
        print_realtime(f'   Tempo decorrido: {tempo_decorrido_subtarefa:.1f}s')
        print_realtime(f'   Limite: {self.timeout_subtarefa_segundos}s')
        print_realtime('   Encerrando subtarefa...')
        self._exibir_estatisticas()
        return None
```

## Localizações Exatas das Modificações

1. **Imports**: Topo do arquivo (linhas 1-50)
2. **Classe IterationTimeoutError**: Após imports, antes de definições de classe (linha ~400)
3. **Variáveis de timeout**: No `__init__` da classe AgenteCompletoV3 (linha ~1150)
4. **Método _executar_com_timeout**: Como método da classe, antes de executar_tarefa (linha ~2550)
5. **Modificação do loop**: Dentro de executar_tarefa, substituir linha 2705
6. **Timeout de subtarefa**: Início e fim de executar_tarefa (linhas 2606 e 2774)

## Validação das Modificações

Após implementar, testar com:
```python
# Teste 1: Tarefa simples (não deve timeout)
python luna_v3_FINAL_OTIMIZADA.py
> "Diga olá mundo"

# Teste 2: Tarefa com operação potencialmente lenta
> "Criar arquivo com 1000 linhas de teste e executar validações complexas"

# Teste 3: Reexecutar TAREFA 3 da suite de 12 tarefas
```

## Rollback
Se houver problemas, restaurar backup criado em:
`.backups/luna_v3_FINAL_OTIMIZADA.py.backup_[timestamp]`
