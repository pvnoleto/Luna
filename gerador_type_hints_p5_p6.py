#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de Type Hints P5/P6 - Fase 2
=====================================

Gera type hints concretos para funções sem anotações.
Baseado no POC validado na Fase 3.
"""

import ast
import json
from typing import Dict, List
from pathlib import Path

# Importar funções do POC
import sys
sys.path.insert(0, '/workspace')
from poc_gerador_type_hints import (
    inferir_tipo_retorno,
    inferir_tipo_parametro,
    gerar_assinatura_com_type_hints
)


def encontrar_node_ast(tree: ast.AST, nome_alvo: str) -> ast.AST:
    """
    Encontra node no AST pelo nome do alvo.
    """
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            if node.name == nome_alvo:
                return node
    return None


def gerar_codigo_type_hints(node: ast.FunctionDef, codigo_fonte: str) -> str:
    """
    Gera código completo com type hints para uma função.

    Returns:
        Código Python com type hints aplicados
    """
    # Gerar nova assinatura com type hints
    nova_assinatura = gerar_assinatura_com_type_hints(node, codigo_fonte)

    # Pegar corpo da função original
    codigo_original = ast.unparse(node)
    linhas = codigo_original.split('\n')

    # Substituir primeira linha (assinatura) pela nova
    linhas[0] = nova_assinatura

    return '\n'.join(linhas)


def processar_fila_melhorias_p5_p6(
    arquivo_fonte: str = 'luna_v3_FINAL_OTIMIZADA.py',
    arquivo_fila: str = 'Luna/.melhorias/fila_melhorias.json'
) -> Dict:
    """
    Processa fila e gera type hints concretos para P5/P6.
    """
    print("=" * 70)
    print("FASE 2: GERADOR DE TYPE HINTS P5/P6")
    print("=" * 70)

    # Carregar fila
    with open(arquivo_fila, 'r', encoding='utf-8') as f:
        fila = json.load(f)

    melhorias_pendentes = fila.get('pendentes', [])
    print(f"\n📊 Total de melhorias na fila: {len(melhorias_pendentes)}")

    # Filtrar P5 e P6 (qualidade - type hints)
    melhorias_p5_p6 = [m for m in melhorias_pendentes if m['prioridade'] in [5, 6]]
    print(f"📋 Melhorias P5/P6 (type hints): {len(melhorias_p5_p6)}")

    # Carregar código fonte
    with open(arquivo_fonte, 'r', encoding='utf-8') as f:
        codigo_fonte = f.read()

    tree = ast.parse(codigo_fonte)

    # Processar cada melhoria
    sucessos = 0
    falhas = 0
    nao_encontrados = 0
    melhorias_atualizadas = []

    for i, melhoria in enumerate(melhorias_p5_p6, 1):
        print(f"\r[{i}/{len(melhorias_p5_p6)}] Processando melhorias...", end='', flush=True)

        try:
            # Remover prefixo "funcao_" do alvo
            alvo = melhoria['alvo']
            if alvo.startswith('funcao_'):
                alvo_limpo = alvo.replace('funcao_', '', 1)
            else:
                alvo_limpo = alvo

            node_encontrado = encontrar_node_ast(tree, alvo_limpo)

            if not node_encontrado:
                nao_encontrados += 1
                melhorias_atualizadas.append(melhoria)
                continue

            # Apenas funções (não classes)
            if not isinstance(node_encontrado, ast.FunctionDef):
                melhorias_atualizadas.append(melhoria)
                continue

            # Verificar se já tem type hints completos
            tem_hints = (
                node_encontrado.returns is not None or
                any(arg.annotation for arg in node_encontrado.args.args)
            )

            if tem_hints:
                # Já tem hints, não precisa gerar
                melhorias_atualizadas.append(melhoria)
                continue

            # Gerar código com type hints
            codigo_concreto = gerar_codigo_type_hints(node_encontrado, codigo_fonte)

            # Atualizar melhoria
            melhoria_atualizada = melhoria.copy()
            melhoria_atualizada['codigo'] = codigo_concreto
            melhoria_atualizada['codigo_original_template'] = melhoria['codigo']
            melhoria_atualizada['gerado_por'] = 'gerador_type_hints_v1'

            melhorias_atualizadas.append(melhoria_atualizada)
            sucessos += 1

        except Exception as e:
            falhas += 1
            melhorias_atualizadas.append(melhoria)

    print()  # Nova linha

    # Atualizar fila
    fila['pendentes'] = melhorias_atualizadas

    # Salvar
    arquivo_fila_nova = arquivo_fila.replace('.json', '_type_hints.json')
    with open(arquivo_fila_nova, 'w', encoding='utf-8') as f:
        json.dump(fila, f, indent=2, ensure_ascii=False)

    total_processado = len(melhorias_p5_p6)
    taxa_sucesso = (sucessos/total_processado*100) if total_processado > 0 else 0

    print(f"\n{'=' * 70}")
    print("📊 ESTATÍSTICAS FINAIS")
    print(f"{'=' * 70}")
    print(f"Total processado: {total_processado}")
    print(f"✅ Type hints gerados: {sucessos}")
    print(f"⚠️  Não encontrados: {nao_encontrados}")
    print(f"⚠️  Já com hints/classes: {total_processado - sucessos - nao_encontrados - falhas}")
    print(f"❌ Falhas: {falhas}")
    print(f"📈 Taxa de geração: {taxa_sucesso:.1f}%")
    print(f"\n📁 Fila atualizada: {arquivo_fila_nova}")
    print(f"{'=' * 70}")

    return {
        'total': total_processado,
        'sucessos': sucessos,
        'nao_encontrados': nao_encontrados,
        'falhas': falhas,
        'taxa_sucesso': taxa_sucesso,
        'arquivo_saida': arquivo_fila_nova
    }


if __name__ == "__main__":
    resultado = processar_fila_melhorias_p5_p6()

    if resultado['sucessos'] > 0:
        print(f"\n🎉 {resultado['sucessos']} type hints prontos para aplicação!")
    else:
        print("\n⚠️ Nenhum type hint foi gerado.")
