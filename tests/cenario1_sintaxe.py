#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 CENÁRIO 1: Recuperação de Erro de Sintaxe
==============================================

Testa: criar_arquivo_teste (falta parêntese de fechamento)
Resultado esperado: Corrige na 2ª tentativa
"""

import sys
import os

# Adicionar diretório pai ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from luna_test import LunaTest


def main():
    print("\n" + "🧪"*35)
    print("CENÁRIO 1: Recuperação de Erro de Sintaxe")
    print("🧪"*35)
    print("\nTeste: criar_arquivo_teste")
    print("Erro: Falta parêntese de fechamento")
    print("Esperado: Corrige automaticamente na 2ª tentativa\n")

    # Criar instância
    luna = LunaTest()

    # Executar teste
    print("\n🚀 EXECUTANDO TESTE...\n")
    resultado = luna.executar_ferramenta(
        'criar_arquivo_teste',
        nome='teste_cenario1.txt',
        conteudo='Hello from Scenario 1!'
    )

    # Resultado
    print("\n" + "="*70)
    print("📋 RESULTADO FINAL")
    print("="*70)
    print(resultado)

    # Estatísticas
    print("\n📊 ESTATÍSTICAS:")
    print(f"   - Erros detectados: {len(luna.erros_recentes)}")
    if luna.erros_recentes:
        print(f"   - Última tentativa: {luna.erros_recentes[-1]['tentativa']}")
        print(f"   - Erro corrigido: {'Sim' if 'sucesso' in resultado.lower() else 'Não'}")

    print("\n✅ Teste concluído!\n")

    return luna


if __name__ == "__main__":
    main()
