#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 CENÁRIO 2: Import Faltante
==============================

Testa: processar_json (módulo json não importado)
Resultado esperado: Adiciona import automaticamente na 2ª tentativa
"""

import sys
import os

# Adicionar diretório pai ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from luna_test import LunaTest


def main():
    print("\n" + "🧪"*35)
    print("CENÁRIO 2: Import Faltante")
    print("🧪"*35)
    print("\nTeste: processar_json")
    print("Erro: Módulo 'json' não importado")
    print("Esperado: Adiciona 'import json' automaticamente na 2ª tentativa\n")

    # Criar instância
    luna = LunaTest()

    # Executar teste
    print("\n🚀 EXECUTANDO TESTE...\n")
    resultado = luna.executar_ferramenta(
        'processar_json',
        texto='{"nome": "teste", "idade": 25, "ativo": true}'
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
        print(f"   - Tipo de erro: {luna.erros_recentes[-1]['erro'][:50]}")
        print(f"   - JSON processado: {'Sim' if 'campos' in resultado else 'Não'}")

    print("\n✅ Teste concluído!\n")

    return luna


if __name__ == "__main__":
    main()
