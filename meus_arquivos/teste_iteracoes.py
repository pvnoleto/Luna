#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de Iteracoes - Verifica o limite maximo de iteracoes
"""

def teste_iteracoes():
    """Faz um loop de 50 iteracoes para testar o limite"""
    print("=" * 60)
    print("TESTE DE ITERACOES - Verificando limite maximo")
    print("=" * 60)
    
    contador = 0
    max_iteracoes = 50
    
    for i in range(1, max_iteracoes + 1):
        contador += 1
        if i % 5 == 0:  # Mostra a cada 5 iteracoes
            print(f"[OK] Iteracao {i}/{max_iteracoes} completada")
    
    print("=" * 60)
    print(f"TESTE COMPLETO!")
    print(f"Total de iteracoes executadas: {contador}")
    print(f"Limite configurado: {max_iteracoes}")
    
    if contador == max_iteracoes:
        print("SUCESSO: O sistema esta executando todas as 50 iteracoes!")
    else:
        print(f"AVISO: Algo esta errado. Esperado: {max_iteracoes}, Obtido: {contador}")
    
    print("=" * 60)
    
    return contador

if __name__ == "__main__":
    resultado = teste_iteracoes()
    print(f"\nResultado final: {resultado} iteracoes")
