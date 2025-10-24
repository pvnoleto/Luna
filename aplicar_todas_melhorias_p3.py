#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicação Massiva de Melhorias P3
==================================

Aplica todas as 165 melhorias concretas geradas no arquivo real.
Processo incremental com validação constante.
"""

import ast
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List


def aplicar_docstring_segura(
    linhas: List[str],
    nome_alvo: str,
    docstring_nova: str,
    tipo: str
) -> tuple[List[str], bool]:
    """
    Aplica docstring em lista de linhas (não modifica arquivo ainda).

    Returns:
        (linhas_modificadas, sucesso)
    """
    # Encontrar definição
    pattern = f'def {nome_alvo}(' if tipo == 'funcao' else f'class {nome_alvo}'
    linha_def = -1

    for i, linha in enumerate(linhas):
        if pattern in linha and not linha.strip().startswith('#'):
            linha_def = i
            break

    if linha_def == -1:
        return linhas, False

    # Verificar se já tem docstring
    linha_apos_def = linha_def + 1
    if linha_apos_def < len(linhas):
        linha_seguinte = linhas[linha_apos_def].strip()
        if linha_seguinte.startswith('"""') or linha_seguinte.startswith("'''"):
            # Remover docstring antiga
            delimitador = '"""' if '"""' in linha_seguinte else "'''"

            # Docstring na mesma linha
            if linha_seguinte.count(delimitador) >= 2:
                linhas.pop(linha_apos_def)
            else:
                # Docstring multi-linha
                fim_docstring = linha_apos_def
                for j in range(linha_apos_def + 1, len(linhas)):
                    if delimitador in linhas[j]:
                        fim_docstring = j
                        break

                # Remover linhas antigas
                for _ in range(linha_apos_def, fim_docstring + 1):
                    linhas.pop(linha_apos_def)

    # Inserir nova docstring
    identacao = len(linhas[linha_def]) - len(linhas[linha_def].lstrip())
    docstring_identada = '\n'.join(
        ' ' * identacao + line if line.strip() else line
        for line in docstring_nova.split('\n')
    )

    linhas.insert(linha_def + 1, docstring_identada + '\n')
    return linhas, True


def aplicar_melhorias_massivo(
    arquivo_fonte: str = 'luna_v3_FINAL_OTIMIZADA.py',
    arquivo_fila: str = 'Luna/.melhorias/fila_melhorias_concreta.json',
    batch_size: int = 20
) -> Dict:
    """
    Aplica todas as melhorias em batches com validação incremental.

    Args:
        arquivo_fonte: Arquivo Python a modificar
        arquivo_fila: Fila de melhorias concretas
        batch_size: Tamanho do batch (validação a cada N aplicações)

    Returns:
        Dict com estatísticas
    """
    print("=" * 70)
    print("APLICAÇÃO MASSIVA DE MELHORIAS P3")
    print("=" * 70)

    # Backup completo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo_backup = f"{arquivo_fonte}.backup_antes_aplicacao_{timestamp}"
    shutil.copy2(arquivo_fonte, arquivo_backup)
    print(f"\n✓ Backup criado: {arquivo_backup}")

    # Carregar melhorias
    with open(arquivo_fila, 'r', encoding='utf-8') as f:
        fila = json.load(f)

    melhorias = fila.get('pendentes', [])

    # Filtrar apenas com código concreto
    melhorias_aplicaveis = [
        m for m in melhorias
        if 'codigo_original_template' in m
    ]

    # Remover duplicatas (mesmo alvo)
    alvos_vistos = set()
    melhorias_unicas = []
    for m in melhorias_aplicaveis:
        if m['alvo'] not in alvos_vistos:
            alvos_vistos.add(m['alvo'])
            melhorias_unicas.append(m)

    print(f"\n📊 Melhorias a aplicar: {len(melhorias_unicas)}")
    print(f"   (Removidas {len(melhorias_aplicaveis) - len(melhorias_unicas)} duplicatas)")

    # Carregar arquivo em memória
    with open(arquivo_fonte, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    # Estatísticas
    sucessos = 0
    falhas = 0
    nao_encontrados = 0
    batches_processados = 0

    # Processar em batches
    for i, melhoria in enumerate(melhorias_unicas, 1):
        # Extrair docstring
        codigo = melhoria['codigo']
        linhas_codigo = codigo.split('\n')

        docstring_linhas = []
        em_docstring = False

        for linha in linhas_codigo:
            if '"""' in linha:
                if not em_docstring:
                    em_docstring = True
                    docstring_linhas.append(linha)
                else:
                    docstring_linhas.append(linha)
                    break
            elif em_docstring:
                docstring_linhas.append(linha)

        docstring = '\n'.join(docstring_linhas)

        # Detectar tipo
        tipo = 'classe' if codigo.strip().startswith('class ') else 'funcao'

        # Aplicar
        linhas_novas, aplicado = aplicar_docstring_segura(
            linhas,
            melhoria['alvo'],
            docstring,
            tipo
        )

        if aplicado:
            linhas = linhas_novas
            sucessos += 1
            print(f"[{i}/{len(melhorias_unicas)}] ✓ {melhoria['alvo']}", end='')
        else:
            nao_encontrados += 1
            print(f"[{i}/{len(melhorias_unicas)}] ⚠ {melhoria['alvo']} (não encontrado)", end='')
            falhas += 1

        # Validar a cada batch
        if i % batch_size == 0 or i == len(melhorias_unicas):
            print(f"\n   → Validando batch {batches_processados + 1}...", end=' ')

            # Escrever temporariamente
            with open(arquivo_fonte, 'w', encoding='utf-8') as f:
                f.writelines(linhas)

            # Validar sintaxe
            try:
                with open(arquivo_fonte, 'r', encoding='utf-8') as f:
                    ast.parse(f.read())
                print("✅ Sintaxe válida")
                batches_processados += 1
            except SyntaxError as e:
                print(f"❌ ERRO DE SINTAXE: {e}")
                print(f"\n⚠️  ROLLBACK: Restaurando backup...")
                shutil.copy2(arquivo_backup, arquivo_fonte)

                return {
                    'status': 'falha_sintaxe',
                    'processados': i,
                    'sucessos': sucessos,
                    'falhas': falhas,
                    'erro': str(e)
                }

        else:
            print()  # Nova linha

    # Validação final completa
    print(f"\n{'─' * 70}")
    print("🔍 VALIDAÇÃO FINAL COMPLETA...")

    try:
        with open(arquivo_fonte, 'r', encoding='utf-8') as f:
            codigo_final = f.read()
        ast.parse(codigo_final)
        print("✅ Sintaxe final: VÁLIDA")
    except SyntaxError as e:
        print(f"❌ ERRO NA VALIDAÇÃO FINAL: {e}")
        shutil.copy2(arquivo_backup, arquivo_fonte)
        return {
            'status': 'falha_validacao_final',
            'erro': str(e)
        }

    # Estatísticas finais
    print(f"\n{'=' * 70}")
    print("📊 ESTATÍSTICAS FINAIS")
    print(f"{'=' * 70}")
    print(f"✅ Aplicadas com sucesso: {sucessos}")
    print(f"⚠️  Não encontradas: {nao_encontrados}")
    print(f"❌ Falhas: {falhas - nao_encontrados}")
    print(f"📦 Batches validados: {batches_processados}")
    print(f"\n💾 Backup disponível em: {arquivo_backup}")
    print(f"{'=' * 70}")

    return {
        'status': 'sucesso',
        'total': len(melhorias_unicas),
        'sucessos': sucessos,
        'nao_encontrados': nao_encontrados,
        'falhas': falhas,
        'batches': batches_processados,
        'backup': arquivo_backup
    }


if __name__ == "__main__":
    resultado = aplicar_melhorias_massivo()

    print(f"\n🎯 RESULTADO FINAL:")
    if resultado['status'] == 'sucesso':
        print(f"✅ APLICAÇÃO MASSIVA CONCLUÍDA COM SUCESSO!")
        print(f"\n📊 Resumo:")
        print(f"   - Total processado: {resultado['total']}")
        print(f"   - Aplicadas: {resultado['sucessos']}")
        print(f"   - Taxa de sucesso: {resultado['sucessos']/resultado['total']*100:.1f}%")
        print(f"\n🎉 O arquivo luna_v3_FINAL_OTIMIZADA.py agora possui {resultado['sucessos']} docstrings!")
    else:
        print(f"❌ FALHA: {resultado.get('erro', 'Erro desconhecido')}")
        print(f"   Arquivo restaurado do backup")
