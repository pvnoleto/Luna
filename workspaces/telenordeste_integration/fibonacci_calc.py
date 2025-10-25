#!/usr/bin/env python3
"""
fibonacci_calc.py

Módulo de cálculo de números de Fibonacci com comparação de performance.

Este arquivo implementa duas abordagens para calcular o n-ésimo número
da sequência de Fibonacci:
1. Iterativa: Utiliza loop para calcular de forma eficiente (O(n))
2. Recursiva: Utiliza chamadas recursivas simples (O(2^n))

O módulo também mede e compara o desempenho de ambas as implementações
para demonstrar a diferença de eficiência entre as abordagens.

Autor: Sistema Luna
Data: 2024
"""

import time
import sys


def fibonacci_iterativo(n):
    """
    Calcula o n-ésimo número de Fibonacci usando iteração.
    
    Esta implementação utiliza um loop for para calcular iterativamente
    os números da sequência de Fibonacci, mantendo apenas os dois últimos
    valores em memória. É extremamente eficiente com complexidade O(n).
    
    Args:
        n (int): A posição do número de Fibonacci desejado (n >= 0)
    
    Returns:
        int: O n-ésimo número da sequência de Fibonacci
        
    Examples:
        >>> fibonacci_iterativo(0)
        0
        >>> fibonacci_iterativo(1)
        1
        >>> fibonacci_iterativo(10)
        55
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def fibonacci_recursivo(n):
    """
    Calcula o n-ésimo número de Fibonacci usando recursão.
    
    Esta implementação usa a definição matemática clássica da sequência
    de Fibonacci de forma recursiva: F(n) = F(n-1) + F(n-2).
    Embora elegante, é muito ineficiente para valores grandes de n,
    pois recalcula os mesmos valores múltiplas vezes (complexidade O(2^n)).
    
    Args:
        n (int): A posição do número de Fibonacci desejado (n >= 0)
    
    Returns:
        int: O n-ésimo número da sequência de Fibonacci
        
    Examples:
        >>> fibonacci_recursivo(0)
        0
        >>> fibonacci_recursivo(1)
        1
        >>> fibonacci_recursivo(10)
        55
        
    Note:
        Para valores de n > 35, esta função pode demorar muito tempo
        para executar devido à complexidade exponencial.
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci_recursivo(n - 1) + fibonacci_recursivo(n - 2)


def main():
    """
    Função principal que mede o tempo de execução das duas implementações.
    
    Esta função executa um teste de performance comparando as implementações
    iterativa e recursiva do cálculo de Fibonacci. Por padrão, calcula o
    30º número de Fibonacci (n=30), que é suficiente para demonstrar a
    diferença significativa de desempenho entre as duas abordagens.
    
    O teste mede o tempo de execução usando time.perf_counter() para
    obter precisão de alta resolução, e exibe os resultados formatados
    incluindo o fator de diferença entre os tempos.
    """
    # Valor de n para teste - escolhido para demonstrar diferença de performance
    # sem tornar o teste muito demorado (n=30 é ideal para fins didáticos)
    n = 30
    
    print(f"Calculando Fibonacci para n={n}\n")
    
    # Medição da implementação iterativa
    inicio_iterativo = time.perf_counter()
    resultado_iterativo = fibonacci_iterativo(n)
    fim_iterativo = time.perf_counter()
    tempo_iterativo = fim_iterativo - inicio_iterativo
    
    print(f"Implementação Iterativa:")
    print(f"  Resultado: {resultado_iterativo}")
    print(f"  Tempo de execução: {tempo_iterativo:.6f} segundos")
    print()
    
    # Medição da implementação recursiva
    inicio_recursivo = time.perf_counter()
    resultado_recursivo = fibonacci_recursivo(n)
    fim_recursivo = time.perf_counter()
    tempo_recursivo = fim_recursivo - inicio_recursivo
    
    print(f"Implementação Recursiva:")
    print(f"  Resultado: {resultado_recursivo}")
    print(f"  Tempo de execução: {tempo_recursivo:.6f} segundos")
    print()
    
    # Comparação de performance entre as implementações
    diferenca = tempo_recursivo / tempo_iterativo if tempo_iterativo > 0 else 0
    print(f"A implementação recursiva foi {diferenca:.2f}x mais lenta que a iterativa")


if __name__ == "__main__":
    main()
