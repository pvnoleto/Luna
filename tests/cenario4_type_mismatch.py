#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 CENÁRIO 4: Type Mismatch
============================

Testa: concatenar_strings (string + int sem conversão)
Resultado esperado: Adiciona str(numero) automaticamente na 2ª tentativa
"""

import sys
import os

# Adicionar diretório pai ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from luna_test import LunaTest


def main():
    print("\n" + "🧪"*35)
    print("CENÁRIO 4: Type Mismatch (TypeError)")
    print("🧪"*35)
    print("\nTeste: concatenar_strings")
    print("Erro: Tentativa de concatenar string + int sem conversão")
    print("Esperado: Adiciona str(numero) automaticamente na 2ª tentativa\n")

    # Criar instância
    luna = LunaTest()

    # Executar teste
    print("\n🚀 EXECUTANDO TESTE...\n")
    resultado = luna.executar_ferramenta(
        'concatenar_strings',
        texto='O número é: ',
        numero=42
    )

    # Resultado
    print("\n" + "="*70)
    print("📋 RESULTADO FINAL")
    print("="*70)
    print(resultado)

    # Teste com diferentes valores
    print("\n\n🚀 TESTE ADICIONAL: Concatenar com número negativo\n")
    resultado2 = luna.executar_ferramenta(
        'concatenar_strings',
        texto='Temperatura: ',
        numero=-15
    )

    print("\n" + "="*70)
    print("📋 RESULTADO TESTE ADICIONAL")
    print("="*70)
    print(resultado2)

    # Estatísticas
    print("\n📊 ESTATÍSTICAS:")
    print(f"   - Erros detectados: {len(luna.erros_recentes)}")
    if luna.erros_recentes:
        print(f"   - Tipo de erro: TypeError (esperado)")
        print(f"   - Teste 1: {'Sucesso' if 'O número é: 42' in resultado else 'Falhou'}")
        print(f"   - Teste 2: {'Sucesso' if 'Temperatura: -15' in resultado2 else 'Falhou'}")
        print(f"   - Correção persistiu: {'Sim' if 'Sucesso' in resultado2 else 'Não'}")

    print("\n✅ Testes concluídos!\n")

    return luna


if __name__ == "__main__":
    main()
