#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Detector de Melhorias P7/P8 - Fase 3
=====================================

Executa detector no arquivo principal para identificar:
- P7: Otimizações (loops, comprehensions, etc.)
- P8: Qualidade (bare except, validações, etc.)
"""

import ast
import json
import sys
from pathlib import Path
from typing import List, Dict

# Importar detector existente
sys.path.insert(0, str(Path(__file__).parent))
from detector_melhorias import DetectorMelhorias


def detectar_melhorias_arquivo(
    arquivo: str = 'luna_v3_FINAL_OTIMIZADA.py'
) -> Dict:
    """
    Detecta melhorias P7/P8 no arquivo.

    Returns:
        Dict com melhorias por prioridade
    """
    print("=" * 70)
    print("DETECÇÃO DE MELHORIAS P7/P8 (Otimizações + Qualidade)")
    print("=" * 70)

    # Ler arquivo
    print(f"\n📁 Analisando: {arquivo}...")
    with open(arquivo, 'r', encoding='utf-8') as f:
        codigo = f.read()

    # Criar detector
    detector = DetectorMelhorias()

    # Analisar
    print("🔍 Executando detecção...")
    melhorias = detector.analisar_codigo_executado('luna_v3_FINAL_OTIMIZADA', codigo)

    # Categorizar por prioridade
    por_prioridade = {}
    por_tipo = {}

    for m in melhorias:
        p = m.get('prioridade', 0)
        tipo = m.get('tipo', 'desconhecido')

        por_prioridade[p] = por_prioridade.get(p, 0) + 1
        por_tipo[tipo] = por_tipo.get(tipo, 0) + 1

    # Estatísticas
    print(f"\n{'─' * 70}")
    print("📊 MELHORIAS DETECTADAS")
    print(f"{'─' * 70}")
    print(f"\nPor Prioridade:")
    for p in sorted(por_prioridade.keys()):
        print(f"  P{p}: {por_prioridade[p]} melhorias")

    print(f"\nPor Tipo:")
    for tipo, count in sorted(por_tipo.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {tipo}: {count}")

    print(f"\nTotal: {len(melhorias)} melhorias detectadas")

    # Filtrar P7 e P8
    p7_p8 = [m for m in melhorias if m.get('prioridade') in [7, 8]]
    print(f"\n✅ P7+P8: {len(p7_p8)} melhorias")

    # Exemplos
    if p7_p8:
        print(f"\n{'─' * 70}")
        print("EXEMPLOS DE MELHORIAS P7/P8")
        print(f"{'─' * 70}")

        for i, m in enumerate(p7_p8[:5], 1):
            print(f"\n{i}. P{m.get('prioridade')} - {m.get('tipo')}")
            print(f"   Alvo: {m.get('alvo', 'N/A')}")
            print(f"   Motivo: {m.get('motivo', '')[:100]}...")

    print(f"\n{'=' * 70}")

    return {
        'total': len(melhorias),
        'p7_p8': len(p7_p8),
        'melhorias': melhorias,
        'p7_p8_only': p7_p8
    }


if __name__ == "__main__":
    resultado = detectar_melhorias_arquivo()

    print(f"\n🎯 RESULTADO:")
    print(f"   Total de melhorias: {resultado['total']}")
    print(f"   P7+P8 (alvo Fase 3): {resultado['p7_p8']}")

    if resultado['p7_p8'] > 0:
        print(f"\n✅ Melhorias P7/P8 detectadas! Pronto para Fase 3.")
    else:
        print(f"\n⚠️  Nenhuma melhoria P7/P8 detectada.")
        print(f"   Fase 3 pode não ser necessária neste arquivo.")
