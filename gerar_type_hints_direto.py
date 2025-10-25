#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador Direto de Type Hints
==============================

Abordagem simplificada: detecta funções sem hints e gera diretamente.
"""

import ast
import json
import sys
sys.path.insert(0, '/workspace')
from poc_gerador_type_hints import (
    inferir_tipo_retorno,
    inferir_tipo_parametro,
    gerar_assinatura_com_type_hints
)

def detectar_e_gerar_type_hints(arquivo: str = 'luna_v3_FINAL_OTIMIZADA.py'):
    """Detecta funções sem hints e gera type hints concretos."""

    print("="*70)
    print("GERADOR DIRETO DE TYPE HINTS")
    print("="*70)

    # Carregar arquivo
    with open(arquivo, 'r', encoding='utf-8') as f:
        codigo = f.read()

    tree = ast.parse(codigo)

    # Detectar funções sem type hints
    funcoes_sem_hints = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Pular __init__, __str__, etc que já devem ter hints ou são especiais
            if node.name.startswith('__') and node.name.endswith('__'):
                continue

            # Verificar se tem hints
            tem_hints_params = any(arg.annotation for arg in node.args.args)
            tem_hint_retorno = node.returns is not None

            # Se não tem nenhum hint, adicionar à lista
            if not tem_hints_params and not tem_hint_retorno:
                funcoes_sem_hints.append(node)

    print(f"\n📊 Funções sem type hints: {len(funcoes_sem_hints)}")

    # Gerar type hints para cada uma
    melhorias = []
    sucessos = 0
    falhas = 0

    for i, func in enumerate(funcoes_sem_hints, 1):
        print(f"\r[{i}/{len(funcoes_sem_hints)}] Gerando type hints...", end='', flush=True)

        try:
            # Gerar assinatura com type hints
            nova_assinatura = gerar_assinatura_com_type_hints(func, codigo)

            # Pegar código completo da função
            codigo_completo = ast.unparse(func)

            # Substituir primeira linha
            linhas = codigo_completo.split('\n')
            linhas[0] = nova_assinatura
            codigo_com_hints = '\n'.join(linhas)

            # Criar melhoria
            melhoria = {
                'alvo': func.name,
                'tipo': 'type_hints',
                'prioridade': 5,
                'codigo': codigo_com_hints,
                'assinatura_original': ast.unparse(func).split('\n')[0],
                'assinatura_nova': nova_assinatura,
                'gerado_por': 'gerador_direto_v1'
            }

            melhorias.append(melhoria)
            sucessos += 1

        except Exception as e:
            falhas += 1

    print()  # Nova linha

    # Salvar
    fila = {
        'pendentes': melhorias,
        'aplicadas': [],
        'metadata': {
            'total': len(funcoes_sem_hints),
            'sucessos': sucessos,
            'falhas': falhas
        }
    }

    arquivo_saida = 'Luna/.melhorias/fila_type_hints_direto.json'
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        json.dump(fila, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*70}")
    print("📊 ESTATÍSTICAS FINAIS")
    print(f"{'='*70}")
    print(f"Total processado: {len(funcoes_sem_hints)}")
    print(f"✅ Type hints gerados: {sucessos}")
    print(f"❌ Falhas: {falhas}")
    print(f"📈 Taxa de sucesso: {sucessos/len(funcoes_sem_hints)*100 if funcoes_sem_hints else 0:.1f}%")
    print(f"\n📁 Fila salva: {arquivo_saida}")
    print(f"{'='*70}")

    return {
        'total': len(funcoes_sem_hints),
        'sucessos': sucessos,
        'falhas': falhas,
        'arquivo_saida': arquivo_saida
    }

if __name__ == "__main__":
    resultado = detectar_e_gerar_type_hints()

    if resultado['sucessos'] > 0:
        print(f"\n🎉 {resultado['sucessos']} type hints prontos para aplicação!")
