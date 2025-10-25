"""
Módulo de cálculo de Fibonacci usando método iterativo.
Complexidade: O(n) tempo, O(1) espaço.
"""

def fibonacci_iterativa(n):
    """
    Calcula o n-ésimo número da sequência de Fibonacci usando método iterativo.
    
    A sequência de Fibonacci é definida como:
    F(0) = 0
    F(1) = 1
    F(n) = F(n-1) + F(n-2) para n >= 2
    
    Args:
        n (int): Posição na sequência de Fibonacci (deve ser >= 0)
    
    Returns:
        int: O n-ésimo número de Fibonacci
    
    Raises:
        ValueError: Se n não for um inteiro não-negativo
        
    Complexidade:
        Tempo: O(n) - percorre n iterações
        Espaço: O(1) - usa apenas variáveis auxiliares
    
    Examples:
        >>> fibonacci_iterativa(0)
        0
        >>> fibonacci_iterativa(1)
        1
        >>> fibonacci_iterativa(5)
        5
        >>> fibonacci_iterativa(10)
        55
        >>> fibonacci_iterativa(30)
        832040
    """
    
    # Validação de entrada: verificar se n é inteiro
    if not isinstance(n, int):
        raise ValueError(f"n deve ser um número inteiro, mas recebeu {type(n).__name__}")
    
    # Validação de entrada: verificar se n é não-negativo
    if n < 0:
        raise ValueError(f"n deve ser >= 0, mas recebeu {n}")
    
    # Casos base: F(0) = 0
    if n == 0:
        return 0
    
    # Casos base: F(1) = 1
    if n == 1:
        return 1
    
    # Inicializar variáveis para os dois primeiros números
    # fib_prev representa F(i-2)
    # fib_curr representa F(i-1)
    fib_prev = 0  # F(0)
    fib_curr = 1  # F(1)
    
    # Iterar de 2 até n para calcular F(n)
    # Em cada iteração, calculamos F(i) = F(i-1) + F(i-2)
    for i in range(2, n + 1):
        # Calcular próximo número de Fibonacci
        fib_next = fib_prev + fib_curr
        
        # Atualizar variáveis para próxima iteração
        fib_prev = fib_curr  # F(i-2) agora é o antigo F(i-1)
        fib_curr = fib_next  # F(i-1) agora é o recém-calculado F(i)
    
    # Retornar o n-ésimo número de Fibonacci
    return fib_curr


# Teste e validação da função
if __name__ == "__main__":
    import time
    
    print("=" * 60)
    print("TESTE DA FUNÇÃO fibonacci_iterativa")
    print("=" * 60)
    
    # Casos de teste básicos
    test_cases = [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (6, 8),
        (7, 13),
        (8, 21),
        (9, 34),
        (10, 55),
        (15, 610),
        (20, 6765),
        (30, 832040),
    ]
    
    print("\n1. TESTES DE CORREÇÃO:")
    print("-" * 60)
    all_passed = True
    for n, expected in test_cases:
        result = fibonacci_iterativa(n)
        status = "✓" if result == expected else "✗"
        print(f"{status} F({n:2d}) = {result:>10d} (esperado: {expected:>10d})")
        if result != expected:
            all_passed = False
    
    print("\n2. TESTE DE PERFORMANCE (n=30):")
    print("-" * 60)
    n_test = 30
    start_time = time.time()
    result = fibonacci_iterativa(n_test)
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"Resultado: F({n_test}) = {result}")
    print(f"Tempo de execução: {elapsed_time:.6f} segundos")
    print(f"Critério (< 0.001s): {'✓ PASSOU' if elapsed_time < 0.001 else '✗ FALHOU'}")
    
    print("\n3. TESTES DE VALIDAÇÃO:")
    print("-" * 60)
    
    # Teste de entrada negativa
    try:
        fibonacci_iterativa(-1)
        print("✗ Falhou ao rejeitar n negativo")
    except ValueError as e:
        print(f"✓ Rejeitou n negativo: {e}")
    
    # Teste de entrada não-inteira
    try:
        fibonacci_iterativa(3.5)
        print("✗ Falhou ao rejeitar n não-inteiro")
    except ValueError as e:
        print(f"✓ Rejeitou n não-inteiro: {e}")
    
    # Teste de entrada string
    try:
        fibonacci_iterativa("10")
        print("✗ Falhou ao rejeitar string")
    except ValueError as e:
        print(f"✓ Rejeitou string: {e}")
    
    print("\n" + "=" * 60)
    print("RESUMO:")
    print("=" * 60)
    print(f"Todos os testes passaram: {'✓ SIM' if all_passed else '✗ NÃO'}")
    print(f"Performance adequada: {'✓ SIM' if elapsed_time < 0.001 else '✗ NÃO'}")
    print(f"Validações implementadas: ✓ SIM")
    print("=" * 60)
