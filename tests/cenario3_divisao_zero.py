#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 CENÁRIO 3: Divisão por Zero
================================

Testa: calcular_media (lista vazia causa ZeroDivisionError)
Resultado esperado: Adiciona validação automaticamente na 2ª tentativa
"""

import sys
import os

# Adicionar diretório pai ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from luna_test import LunaTest


def main():
    print("\n" + "🧪"*35)
    print("CENÁRIO 3: Divisão por Zero")
    print("🧪"*35)
    print("\nTeste: calcular_media")
    print("Erro: Lista vazia causa ZeroDivisionError")
    print("Esperado: Adiciona validação 'if numeros else 0' na 2ª tentativa\n")

    # Criar instância
    luna = LunaTest()

    # Executar teste com lista VAZIA (causa erro)
    print("\n🚀 TESTE 1: Lista vazia (deve causar erro e corrigir)\n")
    resultado1 = luna.executar_ferramenta(
        'calcular_media',
        numeros=[]
    )

    print("\n" + "="*70)
    print("📋 RESULTADO TESTE 1 (lista vazia)")
    print("="*70)
    print(resultado1)

    # Executar teste com lista VÁLIDA (deve funcionar após correção)
    print("\n\n🚀 TESTE 2: Lista com valores (deve funcionar)\n")
    resultado2 = luna.executar_ferramenta(
        'calcular_media',
        numeros=[10, 20, 30, 40, 50]
    )

    print("\n" + "="*70)
    print("📋 RESULTADO TESTE 2 (lista válida)")
    print("="*70)
    print(resultado2)

    # Estatísticas
    print("\n📊 ESTATÍSTICAS:")
    print(f"   - Total de erros detectados: {len(luna.erros_recentes)}")
    print(f"   - Teste 1 (vazio): {'Corrigido' if 'Média: 0' in resultado1 else 'Falhou'}")
    print(f"   - Teste 2 (válido): {'Sucesso' if 'Média: 30' in resultado2 else 'Falhou'}")

    print("\n✅ Testes concluídos!\n")

    return luna


if __name__ == "__main__":
    main()
