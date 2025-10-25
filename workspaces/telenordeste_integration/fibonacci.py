import time


def fibonacci_iterativa(n):
    """
    Calcula o n-ésimo número de Fibonacci usando abordagem iterativa.
    
    Args:
        n (int): Posição na sequência de Fibonacci (0-indexed)
    
    Returns:
        int: O n-ésimo número de Fibonacci
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b


def fibonacci_recursiva(n):
    """
    Calcula o n-ésimo número de Fibonacci usando abordagem recursiva.
    
    Args:
        n (int): Posição na sequência de Fibonacci (0-indexed)
    
    Returns:
        int: O n-ésimo número de Fibonacci
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    
    return fibonacci_recursiva(n - 1) + fibonacci_recursiva(n - 2)


if __name__ == '__main__':
    # Definir o valor de n para teste
    n = 30
    
    print("=" * 60)
    print(f"TESTE DE PERFORMANCE - FIBONACCI({n})")
    print("=" * 60)
    
    # Testar fibonacci_iterativa
    print("\n🔄 Executando fibonacci_iterativa...")
    inicio_iterativa = time.perf_counter()
    resultado_iterativa = fibonacci_iterativa(n)
    fim_iterativa = time.perf_counter()
    tempo_iterativa = fim_iterativa - inicio_iterativa
    
    print(f"   Resultado: {resultado_iterativa}")
    print(f"   Tempo: {tempo_iterativa:.6f} segundos")
    
    # Testar fibonacci_recursiva
    print("\n🔄 Executando fibonacci_recursiva...")
    inicio_recursiva = time.perf_counter()
    resultado_recursiva = fibonacci_recursiva(n)
    fim_recursiva = time.perf_counter()
    tempo_recursiva = fim_recursiva - inicio_recursiva
    
    print(f"   Resultado: {resultado_recursiva}")
    print(f"   Tempo: {tempo_recursiva:.6f} segundos")
    
    # Validação e comparação
    print("\n" + "=" * 60)
    print("RESULTADOS E ANÁLISE")
    print("=" * 60)
    
    if resultado_iterativa == resultado_recursiva:
        print(f"✅ VALIDAÇÃO: Ambas funções retornaram o mesmo valor: {resultado_iterativa}")
    else:
        print(f"❌ ERRO: Resultados diferentes!")
        print(f"   Iterativa: {resultado_iterativa}")
        print(f"   Recursiva: {resultado_recursiva}")
    
    # Comparação de performance
    print(f"\n📊 COMPARAÇÃO DE PERFORMANCE:")
    print(f"   Iterativa:  {tempo_iterativa:.6f}s")
    print(f"   Recursiva:  {tempo_recursiva:.6f}s")
    
    if tempo_iterativa < tempo_recursiva:
        diferenca = tempo_recursiva / tempo_iterativa
        print(f"   🏆 Iterativa é {diferenca:.2f}x mais rápida!")
    else:
        diferenca = tempo_iterativa / tempo_recursiva
        print(f"   🏆 Recursiva é {diferenca:.2f}x mais rápida!")
    
    print("=" * 60)
