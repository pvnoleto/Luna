"""
dados_execucao.py

Dados estruturados capturados da execução do fibonacci_calc.py

Este módulo armazena os resultados da execução do cálculo de Fibonacci
para uso em relatórios e análises posteriores.
"""

# Dados extraídos da execução
TEMPO_ITERATIVO = 0.000004  # segundos
TEMPO_RECURSIVO = 0.196282  # segundos
VALOR_CALCULADO = 832040    # F(30)
N = 30                       # posição calculada
DIFERENCA_PERFORMANCE = 44609.41  # vezes mais lento

# Dicionário estruturado para fácil acesso
resultados = {
    'tempo_iterativo': TEMPO_ITERATIVO,
    'tempo_recursivo': TEMPO_RECURSIVO,
    'valor_calculado': VALOR_CALCULADO,
    'n': N,
    'diferenca_performance': DIFERENCA_PERFORMANCE,
    'unidade_tempo': 'segundos',
    'validacao': {
        'resultado_iterativo': VALOR_CALCULADO,
        'resultado_recursivo': VALOR_CALCULADO,
        'valores_identicos': True
    }
}


def get_resultados():
    """
    Retorna o dicionário com todos os resultados da execução.
    
    Returns:
        dict: Dicionário contendo todos os dados da execução
    """
    return resultados


def get_tempo_iterativo():
    """Retorna o tempo de execução da implementação iterativa em segundos."""
    return TEMPO_ITERATIVO


def get_tempo_recursivo():
    """Retorna o tempo de execução da implementação recursiva em segundos."""
    return TEMPO_RECURSIVO


def get_valor_calculado():
    """Retorna o valor calculado de F(n)."""
    return VALOR_CALCULADO


if __name__ == "__main__":
    # Exibe os dados quando executado diretamente
    print("=== RESULTADOS DA EXECUÇÃO FIBONACCI ===\n")
    print(f"Posição calculada (n): {N}")
    print(f"Valor de F({N}): {VALOR_CALCULADO}")
    print(f"\nTempo Iterativo: {TEMPO_ITERATIVO:.6f} segundos")
    print(f"Tempo Recursivo: {TEMPO_RECURSIVO:.6f} segundos")
    print(f"\nDiferença de Performance: {DIFERENCA_PERFORMANCE:.2f}x mais lento")
    print(f"\n✅ Validação: Ambos os métodos retornaram {VALOR_CALCULADO}")
