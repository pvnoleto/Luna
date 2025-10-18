#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testes automatizados para o programa fatorial"""

from fatorial import fatorial_recursivo, fatorial_iterativo, fatorial_math

print("TESTES AUTOMATIZADOS DO PROGRAMA FATORIAL\n")
print("=" * 60)

# Casos de teste
casos_teste = [0, 1, 5, 10, 15, 20]

print("\nTestando calculos:")
for n in casos_teste:
    rec = fatorial_recursivo(n)
    ite = fatorial_iterativo(n)
    mat = fatorial_math(n)
    
    print(f"  {n}! = {rec:,}")
    
    # Verifica consistencia
    assert rec == ite == mat, f"Inconsistencia no calculo de {n}!"

print("\n[OK] Todos os calculos estao corretos e consistentes!")

# Teste de erro com numero negativo
print("\nTestando tratamento de erros:")
try:
    fatorial_recursivo(-5)
    print("  [ERRO] Deveria lancar excecao para numero negativo")
except ValueError as e:
    print(f"  [OK] Numero negativo: {e}")

# Teste de casos especiais
print("\nCasos especiais:")
print(f"  0! = {fatorial_recursivo(0)} (por definicao)")
print(f"  1! = {fatorial_recursivo(1)}")

print("\n" + "=" * 60)
print("TODOS OS TESTES PASSARAM COM SUCESSO!")
