#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicador de Type Hints
=========================

Aplica type hints gerados nas funções.
"""

import ast
import json
import shutil
from datetime import datetime

def aplicar_type_hints(
    arquivo_fonte: str = 'luna_v3_FINAL_OTIMIZADA.py',
    arquivo_fila: str = 'Luna/.melhorias/fila_type_hints_direto.json'
):
    """Aplica type hints no arquivo."""

    print("="*70)
    print("APLICAÇÃO DE TYPE HINTS")
    print("="*70)

    # Backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo_backup = f"{arquivo_fonte}.backup_type_hints_{timestamp}"
    shutil.copy2(arquivo_fonte, arquivo_backup)
    print(f"\n✓ Backup criado: {arquivo_backup}")

    # Carregar fila
    with open(arquivo_fila, 'r', encoding='utf-8') as f:
        fila = json.load(f)

    melhorias = fila.get('pendentes', [])
    print(f"\n📊 Type hints a aplicar: {len(melhorias)}")

    # Carregar arquivo
    with open(arquivo_fonte, 'r', encoding='utf-8') as f:
        codigo = f.read()

    # Aplicar cada type hint (substituição de assinatura)
    sucessos = 0
    falhas = 0

    for i, melhoria in enumerate(melhorias, 1):
        try:
            assinatura_antiga = melhoria['assinatura_original']
            assinatura_nova = melhoria['assinatura_nova']

            # Se não houve mudança, pular
            if assinatura_antiga == assinatura_nova:
                continue

            # Substituir no código (primeira ocorrência)
            if assinatura_antiga in codigo:
                codigo = codigo.replace(assinatura_antiga, assinatura_nova, 1)
                sucessos += 1
                print(f"\r[{i}/{len(melhorias)}] Aplicando type hints...", end='', flush=True)
            else:
                falhas += 1

        except Exception as e:
            falhas += 1

    print()  # Nova linha

    # Salvar arquivo modificado
    with open(arquivo_fonte, 'w', encoding='utf-8') as f:
        f.write(codigo)

    # Validar sintaxe
    try:
        ast.parse(codigo)
        print("\n✅ Sintaxe válida!")
    except SyntaxError as e:
        print(f"\n❌ ERRO DE SINTAXE: {e}")
        print("⚠️ RESTAURANDO BACKUP...")
        shutil.copy2(arquivo_backup, arquivo_fonte)
        return {'status': 'erro', 'erro': str(e)}

    print(f"\n{'='*70}")
    print("📊 ESTATÍSTICAS FINAIS")
    print(f"{'='*70}")
    print(f"✅ Type hints aplicados: {sucessos}")
    print(f"⚠️  Sem mudanças: {len(melhorias) - sucessos - falhas}")
    print(f"❌ Falhas: {falhas}")
    print(f"\n💾 Backup: {arquivo_backup}")
    print(f"{'='*70}")

    return {
        'status': 'sucesso',
        'sucessos': sucessos,
        'falhas': falhas,
        'backup': arquivo_backup
    }

if __name__ == "__main__":
    resultado = aplicar_type_hints()

    if resultado['status'] == 'sucesso' and resultado['sucessos'] > 0:
        print(f"\n🎉 {resultado['sucessos']} type hints aplicados com sucesso!")
