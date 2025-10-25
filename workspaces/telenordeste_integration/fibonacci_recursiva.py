"""
Implementação de Fibonacci usando recursão simples.

COMPLEXIDADE: O(2^n) tempo - MUITO INEFICIENTE!
Esta implementação é puramente educacional para demonstrar a ineficiência
da recursão simples sem memoization.

Autor: Luna AI
Data: 2024
"""


def fibonacci_recursiva(n: int) -> int:
    """
    Calcula o n-ésimo número de Fibonacci usando recursão simples.
    
    Esta é uma implementação INEFICIENTE com complexidade O(2^n).
    Cada chamada gera duas novas chamadas recursivas, criando uma
    árvore exponencial de chamadas. Para n=30, serão realizadas
    aproximadamente 2^30 = 1.073.741.824 operações!
    
    CASOS BASE:
    - F(0) = 0
    - F(1) = 1
    
    FÓRMULA RECURSIVA:
    - F(n) = F(n-1) + F(n-2) para n >= 2
    
    Args:
        n (int): Posição na sequência de Fibonacci (deve ser >= 0)
        
    Returns:
        int: O n-ésimo número de Fibonacci
        
    Raises:
        ValueError: Se n for negativo
        TypeError: Se n não for um inteiro
        
    Examples:
        >>> fibonacci_recursiva(0)
        0
        >>> fibonacci_recursiva(1)
        1
        >>> fibonacci_recursiva(5)
        5
        >>> fibonacci_recursiva(10)
        55
        >>> fibonacci_recursiva(30)
        832040
        
    Warnings:
        NÃO USE esta função para valores grandes de n (n > 35).
        O tempo de execução cresce exponencialmente!
        
        Tempos aproximados:
        - n=20: ~0.002s
        - n=30: ~20s
        - n=35: ~200s
        - n=40: ~30 minutos!
    """
    # Validação de entrada
    if not isinstance(n, int):
        raise TypeError(f"n deve ser um inteiro, recebido: {type(n).__name__}")
    
    if n < 0:
        raise ValueError(f"n deve ser >= 0, recebido: {n}")
    
    # CASOS BASE
    # F(0) = 0
    if n == 0:
        return 0
    
    # F(1) = 1
    if n == 1:
        return 1
    
    # CHAMADAS RECURSIVAS - INEFICIENTE!
    # Cada chamada gera duas novas chamadas, criando crescimento exponencial
    # F(n) = F(n-1) + F(n-2)
    #
    # Exemplo para n=5:
    #                    fib(5)
    #                   /      \
    #               fib(4)      fib(3)
    #              /     \      /     \
    #          fib(3)  fib(2) fib(2) fib(1)
    #         /    \   /   \   /   \
    #     fib(2) fib(1) ... ...  ... ...
    #
    # Note que fib(3), fib(2), fib(1) são calculados MÚLTIPLAS VEZES!
    # Isso é extremamente ineficiente e causa a complexidade O(2^n)
    
    return fibonacci_recursiva(n - 1) + fibonacci_recursiva(n - 2)


if __name__ == "__main__":
    import time
    
    print("=" * 70)
    print("DEMONSTRAÇÃO: Fibonacci Recursiva - INEFICIENTE O(2^n)")
    print("=" * 70)
    print()
    
    # Testes básicos
    print("Testes básicos:")
    print("-" * 70)
    test_cases = [0, 1, 2, 5, 10, 15]
    
    for n in test_cases:
        inicio = time.perf_counter()
        resultado = fibonacci_recursiva(n)
        fim = time.perf_counter()
        tempo = (fim - inicio) * 1000  # Converter para milissegundos
        
        print(f"F({n:2d}) = {resultado:6d}  |  Tempo: {tempo:8.3f} ms")
    
    print()
    print("=" * 70)
    print("TESTE PRINCIPAL: Calculando F(30) - AGUARDE...")
    print("=" * 70)
    print("⚠️  AVISO: Isso pode levar de 10 a 180 segundos!")
    print()
    
    # Teste principal: n=30
    n = 30
    print(f"Iniciando cálculo de F({n})...")
    inicio = time.perf_counter()
    
    resultado = fibonacci_recursiva(n)
    
    fim = time.perf_counter()
    tempo_segundos = fim - inicio
    
    print()
    print("=" * 70)
    print("RESULTADO:")
    print("=" * 70)
    print(f"F({n}) = {resultado}")
    print(f"Tempo de execução: {tempo_segundos:.2f} segundos")
    print()
    
    # Verificar se está correto
    valor_esperado = 832040
    if resultado == valor_esperado:
        print("✅ SUCESSO! Valor correto!")
    else:
        print(f"❌ ERRO! Esperado: {valor_esperado}, Obtido: {resultado}")
    
    print()
    print("=" * 70)
    print("ANÁLISE DE INEFICIÊNCIA:")
    print("=" * 70)
    print(f"Complexidade: O(2^n) = O(2^{n}) ≈ {2**n:,} operações")
    print()
    print("Por que é tão lento?")
    print("- Cada chamada gera 2 novas chamadas recursivas")
    print("- Valores são recalculados múltiplas vezes")
    print(f"- Para n={n}, F(10) é calculado ~17.000 vezes!")
    print(f"- Para n={n}, F(20) é calculado ~10.000 vezes!")
    print()
    print("Solução: Use memoization ou iteração!")
    print("=" * 70)
