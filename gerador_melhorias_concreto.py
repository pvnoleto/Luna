#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de Melhorias Concretas - Fase 1
=========================================

Integra o POC validado ao detector de melhorias.
Gera código Python concreto para as 6 melhorias P3 da fila.
"""

import ast
import json
from typing import Dict, List
from pathlib import Path

# Importar funções do POC
import sys
sys.path.insert(0, '/workspace')
from poc_gerador_docstrings import (
    inferir_descricao_funcao,
    gerar_docstring_concreta
)


def processar_fila_melhorias_p3(
    arquivo_fonte: str = 'luna_v3_FINAL_OTIMIZADA.py',
    arquivo_fila: str = 'Luna/.melhorias/fila_melhorias.json'
) -> Dict:
    """
    Processa fila de melhorias P3 e gera código concreto para cada uma.

    Args:
        arquivo_fonte: Arquivo Python a analisar
        arquivo_fila: Arquivo JSON com fila de melhorias

    Returns:
        Dict com estatísticas e melhorias atualizadas
    """
    print("=" * 70)
    print("FASE 1: GERADOR DE MELHORIAS CONCRETAS")
    print("=" * 70)

    # Carregar fila
    with open(arquivo_fila, 'r', encoding='utf-8') as f:
        fila = json.load(f)

    melhorias_pendentes = fila.get('pendentes', [])
    print(f"\n📊 Total de melhorias na fila: {len(melhorias_pendentes)}")

    # Filtrar apenas P3 (documentação)
    melhorias_p3 = [m for m in melhorias_pendentes if m['prioridade'] == 3]
    print(f"📋 Melhorias P3 (documentação): {len(melhorias_p3)}")

    # Carregar código fonte
    with open(arquivo_fonte, 'r', encoding='utf-8') as f:
        codigo_fonte = f.read()

    tree = ast.parse(codigo_fonte)

    # Processar cada melhoria
    sucessos = 0
    falhas = 0
    melhorias_atualizadas = []

    for i, melhoria in enumerate(melhorias_p3, 1):
        print(f"\n{'─' * 70}")
        print(f"[{i}/{len(melhorias_p3)}] Processando: {melhoria['alvo']}")

        try:
            # Encontrar a função/classe no AST
            alvo = melhoria['alvo']
            node_encontrado = encontrar_node_ast(tree, alvo, codigo_fonte)

            if not node_encontrado:
                print(f"⚠️  Node '{alvo}' não encontrado no AST")
                falhas += 1
                melhorias_atualizadas.append(melhoria)  # Manter template
                continue

            # Gerar docstring concreta
            docstring_concreta = gerar_docstring_concreta(node_encontrado, codigo_fonte)

            # Montar código completo (def + docstring)
            if isinstance(node_encontrado, ast.FunctionDef):
                assinatura = ast.get_source_segment(codigo_fonte, node_encontrado).split('\n')[0]
                codigo_concreto = f"{assinatura}\n{docstring_concreta}"
            elif isinstance(node_encontrado, ast.ClassDef):
                assinatura = f"class {node_encontrado.name}:"
                codigo_concreto = f"{assinatura}\n{docstring_concreta}"
            else:
                print(f"⚠️  Tipo de node não suportado: {type(node_encontrado)}")
                falhas += 1
                melhorias_atualizadas.append(melhoria)
                continue

            # Atualizar melhoria com código concreto
            melhoria_atualizada = melhoria.copy()
            melhoria_atualizada['codigo'] = codigo_concreto
            melhoria_atualizada['codigo_original_template'] = melhoria['codigo']  # Backup
            melhoria_atualizada['gerado_por'] = 'gerador_concreto_v1'

            melhorias_atualizadas.append(melhoria_atualizada)
            sucessos += 1

            print(f"✅ Código concreto gerado ({len(codigo_concreto)} chars)")
            print(f"   Preview: {codigo_concreto[:80]}...")

        except Exception as e:
            print(f"❌ Erro ao processar: {e}")
            falhas += 1
            melhorias_atualizadas.append(melhoria)  # Manter template

    # Atualizar fila
    fila['pendentes'] = melhorias_atualizadas

    # Salvar fila atualizada
    arquivo_fila_nova = arquivo_fila.replace('.json', '_concreta.json')
    with open(arquivo_fila_nova, 'w', encoding='utf-8') as f:
        json.dump(fila, f, indent=2, ensure_ascii=False)

    print(f"\n{'=' * 70}")
    print("📊 ESTATÍSTICAS FINAIS")
    print(f"{'=' * 70}")
    print(f"✅ Sucessos: {sucessos}/{len(melhorias_p3)} ({sucessos/len(melhorias_p3)*100:.1f}%)")
    print(f"❌ Falhas: {falhas}/{len(melhorias_p3)} ({falhas/len(melhorias_p3)*100:.1f}%)")
    print(f"\n📁 Fila atualizada salva em: {arquivo_fila_nova}")
    print(f"{'=' * 70}")

    return {
        'total': len(melhorias_p3),
        'sucessos': sucessos,
        'falhas': falhas,
        'taxa_sucesso': sucessos/len(melhorias_p3)*100 if melhorias_p3 else 0,
        'arquivo_saida': arquivo_fila_nova
    }


def encontrar_node_ast(tree: ast.AST, nome_alvo: str, codigo_fonte: str) -> ast.AST:
    """
    Encontra node no AST pelo nome do alvo.

    Args:
        tree: Árvore AST
        nome_alvo: Nome da função/classe a encontrar
        codigo_fonte: Código fonte completo

    Returns:
        Node AST encontrado ou None
    """
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            if node.name == nome_alvo:
                return node

    return None


if __name__ == "__main__":
    resultado = processar_fila_melhorias_p3()

    print(f"\n🎯 RESULTADO FASE 1:")
    if resultado['taxa_sucesso'] >= 80:
        print(f"✅ META ATINGIDA! Taxa de sucesso: {resultado['taxa_sucesso']:.1f}%")
        print(f"   (Meta era ≥80%)")
    else:
        print(f"⚠️  Meta não atingida. Taxa: {resultado['taxa_sucesso']:.1f}%")
        print(f"   (Meta: ≥80%)")

    print(f"\n🎯 PRÓXIMO PASSO:")
    print(f"   Testar aplicação manual das melhorias geradas")
