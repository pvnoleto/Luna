#!/usr/bin/env python3
"""
Programa para calcular fatorial de um número
Implementações: recursiva, iterativa e usando módulo math
"""

import math


def fatorial_recursivo(n):
    """
    Calcula fatorial usando recursão
    
    Args:
        n (int): Número inteiro não-negativo
        
    Returns:
        int: Fatorial de n
    """
    if n < 0:
        raise ValueError("Fatorial não definido para números negativos")
    if n == 0 or n == 1:
        return 1
    return n * fatorial_recursivo(n - 1)


def fatorial_iterativo(n):
    """
    Calcula fatorial usando loop iterativo
    
    Args:
        n (int): Número inteiro não-negativo
        
    Returns:
        int: Fatorial de n
    """
    if n < 0:
        raise ValueError("Fatorial não definido para números negativos")
    
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado


def fatorial_math(n):
    """
    Calcula fatorial usando a biblioteca math
    
    Args:
        n (int): Número inteiro não-negativo
        
    Returns:
        int: Fatorial de n
    """
    if n < 0:
        raise ValueError("Fatorial não definido para números negativos")
    return math.factorial(n)


def main():
    """Função principal com interface interativa"""
    print("=" * 50)
    print("CALCULADORA DE FATORIAL")
    print("=" * 50)
    print()
    
    while True:
        try:
            entrada = input("Digite um número (ou 'sair' para encerrar): ")
            
            if entrada.lower() in ['sair', 'exit', 'q']:
                print("Encerrando programa...")
                break
            
            numero = int(entrada)
            
            # Calcula usando os três métodos
            resultado_recursivo = fatorial_recursivo(numero)
            resultado_iterativo = fatorial_iterativo(numero)
            resultado_math = fatorial_math(numero)
            
            print(f"\n📊 Resultados para {numero}!")
            print(f"   Recursivo:  {resultado_recursivo}")
            print(f"   Iterativo:  {resultado_iterativo}")
            print(f"   Math:       {resultado_math}")
            print(f"   Notação:    {numero}! = {resultado_recursivo}")
            print()
            
            # Verifica consistência
            if resultado_recursivo == resultado_iterativo == resultado_math:
                print("✅ Todos os métodos retornaram o mesmo resultado!\n")
            
        except ValueError as e:
            print(f"❌ Erro: {e}")
            print("Por favor, digite um número inteiro não-negativo.\n")
        except RecursionError:
            print(f"❌ Erro: Número muito grande para cálculo recursivo.")
            print("Tente um número menor ou use o método iterativo.\n")
        except KeyboardInterrupt:
            print("\n\nPrograma interrompido pelo usuário.")
            break


if __name__ == "__main__":
    main()
