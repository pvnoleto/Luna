#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 CENÁRIO 5: Teste de Auto-Evolução
=====================================

Testa as 4 ferramentas com OPORTUNIDADES DE MELHORIA:
1. processar_lista - Loop ineficiente (pode ser list comprehension)
2. somar_numeros - Falta type hints
3. validar_email - Falta docstring
4. deletar_arquivo_perigoso - Falta validação de segurança

Objetivo: Verificar se o sistema de auto-evolução detecta e sugere melhorias
"""

import sys
import os
from datetime import datetime

# Adicionar diretório pai ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from luna_test import LunaTest


def testar_loop_ineficiente():
    """
    MELHORIA 1: Loop ineficiente
    Pode ser convertido para list comprehension
    """
    print("\n" + "💡"*35)
    print("MELHORIA 1: Loop Ineficiente → List Comprehension")
    print("💡"*35)
    print("\nTeste: processar_lista")
    print("Oportunidade: Loop pode ser list comprehension")
    print("Sugestão: resultado = [item.upper() for item in items]\n")

    luna = LunaTest()

    # Ver código original
    print("📄 CÓDIGO ORIGINAL:")
    print("-" * 70)
    print(luna.ferramentas['processar_lista'])
    print("-" * 70)

    # Executar
    print("\n🚀 EXECUTANDO...")
    resultado = luna.executar_ferramenta(
        'processar_lista',
        items=['python', 'javascript', 'rust', 'go']
    )

    print("\n" + "="*70)
    print("📋 RESULTADO")
    print("="*70)
    print(resultado)

    # Verificar se auto-evolução detectou
    if luna.auto_evolucao_disponivel and luna.fila_melhorias:
        print("\n✅ Sistema de auto-evolução ATIVO")
        print(f"   Melhorias na fila: {len(luna.fila_melhorias.melhorias_pendentes)}")
    else:
        print("\n⚠️  Auto-evolução não detectou ou não está disponível")

    return luna


def testar_falta_type_hints():
    """
    MELHORIA 2: Falta type hints
    Função sem anotações de tipo
    """
    print("\n\n" + "💡"*35)
    print("MELHORIA 2: Falta Type Hints")
    print("💡"*35)
    print("\nTeste: somar_numeros")
    print("Oportunidade: Função sem type hints")
    print("Sugestão: def somar_numeros(a: int, b: int) -> str:\n")

    luna = LunaTest()

    # Ver código original
    print("📄 CÓDIGO ORIGINAL:")
    print("-" * 70)
    print(luna.ferramentas['somar_numeros'])
    print("-" * 70)

    # Executar
    print("\n🚀 EXECUTANDO...")
    resultado = luna.executar_ferramenta(
        'somar_numeros',
        a=42,
        b=58
    )

    print("\n" + "="*70)
    print("📋 RESULTADO")
    print("="*70)
    print(resultado)

    return luna


def testar_falta_docstring():
    """
    MELHORIA 3: Falta docstring
    Função sem documentação
    """
    print("\n\n" + "💡"*35)
    print("MELHORIA 3: Falta Docstring")
    print("💡"*35)
    print("\nTeste: validar_email")
    print("Oportunidade: Função sem docstring")
    print("Sugestão: Adicionar docstring Google Style\n")

    luna = LunaTest()

    # Ver código original
    print("📄 CÓDIGO ORIGINAL:")
    print("-" * 70)
    print(luna.ferramentas['validar_email'])
    print("-" * 70)

    # Executar
    print("\n🚀 EXECUTANDO...")
    resultado = luna.executar_ferramenta(
        'validar_email',
        email='teste@exemplo.com'
    )

    print("\n" + "="*70)
    print("📋 RESULTADO")
    print("="*70)
    print(resultado)

    return luna


def testar_falta_validacao():
    """
    MELHORIA 4: Falta validação de segurança
    Deleta arquivo sem verificar caminho
    """
    print("\n\n" + "💡"*35)
    print("MELHORIA 4: Falta Validação de Segurança")
    print("💡"*35)
    print("\nTeste: deletar_arquivo_perigoso")
    print("Oportunidade: Deleta sem validar caminho")
    print("Sugestão: Validar se path está em área permitida\n")

    luna = LunaTest()

    # Ver código original
    print("📄 CÓDIGO ORIGINAL:")
    print("-" * 70)
    print(luna.ferramentas['deletar_arquivo_perigoso'])
    print("-" * 70)

    # Criar arquivo temporário para teste
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write('teste')
        temp_file = f.name

    print(f"\n📝 Arquivo temporário criado: {temp_file}")

    # Executar
    print("\n🚀 EXECUTANDO...")
    resultado = luna.executar_ferramenta(
        'deletar_arquivo_perigoso',
        caminho=temp_file
    )

    print("\n" + "="*70)
    print("📋 RESULTADO")
    print("="*70)
    print(resultado)

    # Verificar se arquivo foi deletado
    import os
    if not os.path.exists(temp_file):
        print("⚠️  Arquivo foi deletado sem validação de segurança!")
    else:
        print("✅ Arquivo não foi deletado (proteção funcionou)")

    # Limpar se ainda existir
    try:
        os.remove(temp_file)
    except:
        pass

    return luna


def main():
    """Executa todos os testes de auto-evolução"""
    print("\n" + "="*70)
    print("🧪 TESTE DE AUTO-EVOLUÇÃO - LUNA TEST SUITE")
    print("="*70)
    print("\nObjetivo: Verificar detecção de oportunidades de melhoria")
    print("\n4 testes serão executados:")
    print("  1. Loop ineficiente")
    print("  2. Falta type hints")
    print("  3. Falta docstring")
    print("  4. Falta validação de segurança")

    inicio = datetime.now()

    # Executar testes
    luna1 = testar_loop_ineficiente()
    luna2 = testar_falta_type_hints()
    luna3 = testar_falta_docstring()
    luna4 = testar_falta_validacao()

    fim = datetime.now()
    duracao = (fim - inicio).total_seconds()

    # Resumo final
    print("\n\n" + "="*70)
    print("📊 RESUMO - TESTE DE AUTO-EVOLUÇÃO")
    print("="*70)

    print(f"\n⏱️  Tempo total: {duracao:.2f}s")
    print(f"✅ 4 testes executados com sucesso")

    # Verificar auto-evolução
    if luna1.auto_evolucao_disponivel:
        print(f"\n💡 Sistema de auto-evolução: ATIVO")
        total_melhorias = 0
        if luna1.fila_melhorias:
            total_melhorias += len(luna1.fila_melhorias.melhorias_pendentes)
        print(f"   Oportunidades detectadas: {total_melhorias}")

        if total_melhorias > 0:
            print("\n   Melhorias sugeridas:")
            for i, melhoria in enumerate(luna1.fila_melhorias.melhorias_pendentes[:5], 1):
                print(f"   {i}. {melhoria.get('tipo', 'desconhecido')}: {melhoria.get('motivo', '')[:60]}")
    else:
        print(f"\n⚠️  Sistema de auto-evolução: INATIVO")
        print("   (sistema_auto_evolucao.py não encontrado)")

    print("\n✅ Todos os testes de auto-evolução concluídos!\n")

    return {
        'duracao': duracao,
        'testes': 4,
        'auto_evolucao_ativo': luna1.auto_evolucao_disponivel
    }


if __name__ == "__main__":
    main()
