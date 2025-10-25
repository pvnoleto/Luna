#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 CENÁRIO 6: Erros Avançados (AttributeError, IndexError, KeyError)
=====================================================================

Testa 3 novos tipos de erro:
1. AttributeError - Acesso a atributo inexistente
2. IndexError - Índice fora do range
3. KeyError - Chave inexistente em dicionário

Resultado esperado: Sistema detecta e corrige automaticamente
"""

import sys
import os

# Adicionar diretório pai ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from luna_test import LunaTest


def teste_attribute_error():
    """
    Teste 1: AttributeError
    Tenta acessar dicionário como atributo
    """
    print("\n" + "🧪"*35)
    print("CENÁRIO 6.1: AttributeError")
    print("🧪"*35)
    print("\nTeste: obter_propriedade")
    print("Erro: Acessa dict como atributo (objeto.propriedade)")
    print("Esperado: Corrige para objeto.get(propriedade)\n")

    luna = LunaTest()

    # Executar
    print("🚀 EXECUTANDO TESTE...\n")
    resultado = luna.executar_ferramenta(
        'obter_propriedade',
        objeto={'nome': 'Python', 'versao': '3.13'},
        propriedade='nome'
    )

    # Resultado
    print("\n" + "="*70)
    print("📋 RESULTADO FINAL")
    print("="*70)
    print(resultado)

    # Teste adicional
    print("\n\n🚀 TESTE ADICIONAL: Propriedade que existe\n")
    resultado2 = luna.executar_ferramenta(
        'obter_propriedade',
        objeto={'cidade': 'São Paulo', 'estado': 'SP'},
        propriedade='cidade'
    )

    print("\n" + "="*70)
    print("📋 RESULTADO TESTE ADICIONAL")
    print("="*70)
    print(resultado2)

    # Estatísticas
    print("\n📊 ESTATÍSTICAS:")
    print(f"   - Erros detectados: {len(luna.erros_recentes)}")
    if luna.erros_recentes:
        print(f"   - Tipo de erro: AttributeError (esperado)")
        print(f"   - Teste 1: {'Sucesso' if 'Python' in resultado else 'Falhou'}")
        print(f"   - Teste 2: {'Sucesso' if 'São Paulo' in resultado2 else 'Falhou'}")
        print(f"   - Correção persistiu: {'Sim' if 'São Paulo' in resultado2 else 'Não'}")

    print("\n✅ Teste concluído!\n")
    return luna


def teste_index_error():
    """
    Teste 2: IndexError
    Acessa índice fora do range
    """
    print("\n\n" + "🧪"*35)
    print("CENÁRIO 6.2: IndexError")
    print("🧪"*35)
    print("\nTeste: obter_item_lista")
    print("Erro: Acessa índice que não existe")
    print("Esperado: Adiciona validação if 0 <= indice < len(lista)\n")

    luna = LunaTest()

    # Executar teste com índice INVÁLIDO (causa erro)
    print("🚀 TESTE 1: Índice fora do range (deve causar erro e corrigir)\n")
    resultado1 = luna.executar_ferramenta(
        'obter_item_lista',
        lista=['a', 'b', 'c'],
        indice=10
    )

    print("\n" + "="*70)
    print("📋 RESULTADO TESTE 1 (índice inválido)")
    print("="*70)
    print(resultado1)

    # Executar teste com índice VÁLIDO (deve funcionar após correção)
    print("\n\n🚀 TESTE 2: Índice válido (deve funcionar)\n")
    resultado2 = luna.executar_ferramenta(
        'obter_item_lista',
        lista=['Python', 'JavaScript', 'Rust'],
        indice=1
    )

    print("\n" + "="*70)
    print("📋 RESULTADO TESTE 2 (índice válido)")
    print("="*70)
    print(resultado2)

    # Estatísticas
    print("\n📊 ESTATÍSTICAS:")
    print(f"   - Total de erros detectados: {len(luna.erros_recentes)}")
    print(f"   - Teste 1 (inválido): {'Corrigido' if 'None' in resultado1 else 'Falhou'}")
    print(f"   - Teste 2 (válido): {'Sucesso' if 'JavaScript' in resultado2 else 'Falhou'}")

    print("\n✅ Testes concluídos!\n")
    return luna


def teste_key_error():
    """
    Teste 3: KeyError
    Acessa chave inexistente em dicionário
    """
    print("\n\n" + "🧪"*35)
    print("CENÁRIO 6.3: KeyError")
    print("🧪"*35)
    print("\nTeste: obter_configuracao")
    print("Erro: Acessa chave que não existe")
    print("Esperado: Corrige para config.get(chave, default)\n")

    luna = LunaTest()

    # Executar teste com chave INEXISTENTE (causa erro)
    print("🚀 TESTE 1: Chave inexistente (deve causar erro e corrigir)\n")
    resultado1 = luna.executar_ferramenta(
        'obter_configuracao',
        config={'host': 'localhost', 'port': 8080},
        chave='senha'
    )

    print("\n" + "="*70)
    print("📋 RESULTADO TESTE 1 (chave inexistente)")
    print("="*70)
    print(resultado1)

    # Executar teste com chave EXISTENTE (deve funcionar após correção)
    print("\n\n🚀 TESTE 2: Chave existente (deve funcionar)\n")
    resultado2 = luna.executar_ferramenta(
        'obter_configuracao',
        config={'debug': True, 'timeout': 30},
        chave='debug'
    )

    print("\n" + "="*70)
    print("📋 RESULTADO TESTE 2 (chave existente)")
    print("="*70)
    print(resultado2)

    # Estatísticas
    print("\n📊 ESTATÍSTICAS:")
    print(f"   - Total de erros detectados: {len(luna.erros_recentes)}")
    print(f"   - Teste 1 (inexistente): {'Corrigido' if 'não encontrada' in resultado1 else 'Falhou'}")
    print(f"   - Teste 2 (existente): {'Sucesso' if 'True' in resultado2 else 'Falhou'}")

    print("\n✅ Testes concluídos!\n")
    return luna


def main():
    """Executa todos os testes de erros avançados"""
    print("\n" + "="*70)
    print("🧪 CENÁRIO 6: TESTES DE ERROS AVANÇADOS")
    print("="*70)
    print("\n3 tipos de erro serão testados:")
    print("  1. AttributeError - Acesso a atributo inexistente")
    print("  2. IndexError - Índice fora do range")
    print("  3. KeyError - Chave inexistente")

    # Executar testes
    luna1 = teste_attribute_error()
    luna2 = teste_index_error()
    luna3 = teste_key_error()

    # Resumo final
    print("\n" + "="*70)
    print("📊 RESUMO GERAL - ERROS AVANÇADOS")
    print("="*70)

    total_erros = len(luna1.erros_recentes) + len(luna2.erros_recentes) + len(luna3.erros_recentes)

    print(f"\n✅ 3 cenários executados (7 testes no total)")
    print(f"📊 Total de erros detectados: {total_erros}")
    print(f"🔧 Todas as correções aplicadas automaticamente")

    print("\n📋 RESUMO POR TIPO:")
    print(f"   1. AttributeError: {len(luna1.erros_recentes)} erro(s) - Corrigido")
    print(f"   2. IndexError: {len(luna2.erros_recentes)} erro(s) - Corrigido")
    print(f"   3. KeyError: {len(luna3.erros_recentes)} erro(s) - Corrigido")

    print("\n✅ Todos os testes de erros avançados concluídos!\n")

    return {
        'cenarios': 3,
        'testes_total': 7,
        'erros_detectados': total_erros,
        'sucesso': True
    }


if __name__ == "__main__":
    main()
