#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de Aplicação Manual - Fase 2
===================================

Testa aplicação de uma amostra de melhorias no arquivo real.
"""

import ast
import json
import shutil
from pathlib import Path
from typing import Dict, List


def selecionar_amostra(arquivo_fila: str, tamanho: int = 10) -> List[Dict]:
    """
    Seleciona amostra representativa de melhorias.

    Critérios:
    - Mix de funções e classes
    - Apenas melhorias com código concreto gerado
    - Alvos únicos (sem duplicatas)
    """
    with open(arquivo_fila, 'r', encoding='utf-8') as f:
        fila = json.load(f)

    melhorias = fila.get('pendentes', [])

    # Filtrar apenas com código concreto
    com_codigo = [m for m in melhorias if 'codigo_original_template' in m]

    # Separar funções e classes
    funcoes = []
    classes = []
    alvos_vistos = set()

    for m in com_codigo:
        alvo = m['alvo']
        if alvo in alvos_vistos:
            continue
        alvos_vistos.add(alvo)

        # Detectar se é classe ou função pelo código
        if m['codigo'].strip().startswith('class '):
            classes.append(m)
        else:
            funcoes.append(m)

    # Selecionar mix: 7 funções + 3 classes
    amostra = funcoes[:7] + classes[:3]

    return amostra[:tamanho]


def aplicar_docstring(
    arquivo_alvo: str,
    nome_alvo: str,
    docstring_nova: str,
    tipo: str = 'funcao'
) -> bool:
    """
    Aplica docstring em função ou classe.

    Args:
        arquivo_alvo: Caminho do arquivo
        nome_alvo: Nome da função/classe
        docstring_nova: Nova docstring
        tipo: 'funcao' ou 'classe'

    Returns:
        True se aplicado com sucesso
    """
    # Ler arquivo
    with open(arquivo_alvo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    # Encontrar definição
    pattern = f'def {nome_alvo}(' if tipo == 'funcao' else f'class {nome_alvo}'
    linha_def = -1

    for i, linha in enumerate(linhas):
        if pattern in linha:
            # Validar que não é comentário
            if not linha.strip().startswith('#'):
                linha_def = i
                break

    if linha_def == -1:
        print(f"  ❌ '{nome_alvo}' não encontrado")
        return False

    print(f"  ✓ Encontrado na linha {linha_def + 1}")

    # Verificar se já tem docstring
    linha_apos_def = linha_def + 1
    if linha_apos_def < len(linhas):
        linha_seguinte = linhas[linha_apos_def].strip()
        if linha_seguinte.startswith('"""') or linha_seguinte.startswith("'''"):
            print(f"  ℹ️  Já tem docstring - aplicando mesmo assim (sobrescreve)")

            # Remover docstring antiga
            delimitador = '"""' if '"""' in linha_seguinte else "'''"
            fim_docstring = linha_apos_def

            # Se docstring está na mesma linha
            if linha_seguinte.count(delimitador) >= 2:
                linhas.pop(linha_apos_def)
            else:
                # Docstring multi-linha
                for j in range(linha_apos_def + 1, len(linhas)):
                    if delimitador in linhas[j]:
                        fim_docstring = j
                        break

                # Remover linhas da docstring antiga
                for _ in range(linha_apos_def, fim_docstring + 1):
                    linhas.pop(linha_apos_def)

    # Inserir nova docstring
    identacao = len(linhas[linha_def]) - len(linhas[linha_def].lstrip())
    docstring_identada = '\n'.join(
        ' ' * identacao + line if line.strip() else line
        for line in docstring_nova.split('\n')
    )

    linhas.insert(linha_def + 1, docstring_identada + '\n')

    # Escrever arquivo modificado
    with open(arquivo_alvo, 'w', encoding='utf-8') as f:
        f.writelines(linhas)

    return True


def validar_sintaxe(arquivo: str) -> bool:
    """
    Valida sintaxe do arquivo Python.
    """
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        ast.parse(codigo)
        return True
    except SyntaxError as e:
        print(f"  ❌ ERRO DE SINTAXE: {e}")
        return False


def testar_aplicacao_manual(
    arquivo_fonte: str = 'luna_v3_FINAL_OTIMIZADA.py',
    arquivo_fila: str = 'Luna/.melhorias/fila_melhorias_concreta.json',
    tamanho_amostra: int = 10
) -> Dict:
    """
    Testa aplicação manual de melhorias em amostra.

    Returns:
        Dict com estatísticas de sucesso/falha
    """
    print("=" * 70)
    print("FASE 2: TESTE DE APLICAÇÃO MANUAL")
    print("=" * 70)

    # Backup do arquivo original
    arquivo_backup = arquivo_fonte + '.backup_fase2'
    shutil.copy2(arquivo_fonte, arquivo_backup)
    print(f"\n✓ Backup criado: {arquivo_backup}")

    # Selecionar amostra
    amostra = selecionar_amostra(arquivo_fila, tamanho_amostra)
    print(f"\n📊 Amostra selecionada: {len(amostra)} melhorias")
    print(f"   - Funções: {sum(1 for m in amostra if m['codigo'].strip().startswith('def '))}")
    print(f"   - Classes: {sum(1 for m in amostra if m['codigo'].strip().startswith('class '))}")

    # Testar cada aplicação
    sucessos = 0
    falhas = 0
    detalhes = []

    for i, melhoria in enumerate(amostra, 1):
        print(f"\n{'─' * 70}")
        print(f"[{i}/{len(amostra)}] {melhoria['alvo']}")

        # Extrair docstring do código gerado
        codigo = melhoria['codigo']
        linhas_codigo = codigo.split('\n')

        # Encontrar docstring (linhas entre """)
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
        try:
            aplicado = aplicar_docstring(
                arquivo_fonte,
                melhoria['alvo'],
                docstring,
                tipo
            )

            if not aplicado:
                falhas += 1
                detalhes.append({
                    'alvo': melhoria['alvo'],
                    'status': 'falha_aplicacao',
                    'erro': 'Não encontrado no arquivo'
                })
                continue

            # Validar sintaxe
            if validar_sintaxe(arquivo_fonte):
                print(f"  ✅ Sintaxe VÁLIDA")
                sucessos += 1
                detalhes.append({
                    'alvo': melhoria['alvo'],
                    'status': 'sucesso'
                })
            else:
                print(f"  ❌ Sintaxe INVÁLIDA")
                falhas += 1
                detalhes.append({
                    'alvo': melhoria['alvo'],
                    'status': 'falha_sintaxe'
                })

                # Restaurar backup
                shutil.copy2(arquivo_backup, arquivo_fonte)
                print(f"  ↩️  Backup restaurado")

        except Exception as e:
            print(f"  ❌ ERRO: {e}")
            falhas += 1
            detalhes.append({
                'alvo': melhoria['alvo'],
                'status': 'falha_excecao',
                'erro': str(e)
            })

            # Restaurar backup
            shutil.copy2(arquivo_backup, arquivo_fonte)
            print(f"  ↩️  Backup restaurado")

    # Restaurar original
    shutil.copy2(arquivo_backup, arquivo_fonte)
    print(f"\n{'=' * 70}")
    print("📊 ESTATÍSTICAS FINAIS")
    print(f"{'=' * 70}")
    print(f"✅ Sucessos: {sucessos}/{len(amostra)} ({sucessos/len(amostra)*100:.1f}%)")
    print(f"❌ Falhas: {falhas}/{len(amostra)} ({falhas/len(amostra)*100:.1f}%)")
    print(f"\n✓ Arquivo original restaurado")
    print(f"{'=' * 70}")

    return {
        'total': len(amostra),
        'sucessos': sucessos,
        'falhas': falhas,
        'taxa_sucesso': sucessos/len(amostra)*100 if amostra else 0,
        'detalhes': detalhes
    }


if __name__ == "__main__":
    resultado = testar_aplicacao_manual()

    print(f"\n🎯 RESULTADO FASE 2:")
    if resultado['taxa_sucesso'] >= 80:
        print(f"✅ META ATINGIDA! Taxa de sucesso: {resultado['taxa_sucesso']:.1f}%")
        print(f"   (Meta era ≥80%)")
    else:
        print(f"⚠️  Meta não atingida. Taxa: {resultado['taxa_sucesso']:.1f}%")
        print(f"   (Meta: ≥80%)")

    print(f"\n🎯 PRÓXIMA FASE:")
    print(f"   - Documentar resultados")
    print(f"   - Expandir para P7 (otimizações)")
