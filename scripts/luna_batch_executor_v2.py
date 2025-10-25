#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Batch Executor V2 - Versão simplificada

Executa Luna em modo batch com monkey patching de input()
"""

import sys
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='Luna V3 - Batch Mode Executor V2')
    parser.add_argument('prompt', help='Prompt/tarefa a executar')
    parser.add_argument('--tier', type=int, default=2, help='API Tier (1-4)')
    parser.add_argument('--rate-mode', type=int, default=2, help='Rate limit mode (1-3)')

    args = parser.parse_args()

    print("="*80)
    print("LUNA V3 - BATCH MODE V2")
    print("="*80)
    print(f"Tier: {args.tier}")
    print(f"Rate Mode: {args.rate_mode}")
    print(f"Prompt: {args.prompt[:100]}...")
    print("="*80)
    print()

    # Preparar inputs simulados
    inputs_queue = [
        str(args.tier),        # Escolha de tier
        str(args.rate_mode),   # Escolha de modo
        "n",                    # Não usar cofre
        args.prompt,            # O prompt da tarefa
        "",                     # Confirmar prompt (Enter)
        "sair"                  # Sair após completar
    ]

    input_index = [0]  # Usar lista para poder modificar no closure

    # Monkey patch input()
    original_input = __builtins__.input

    def mock_input(prompt_text=""):
        if input_index[0] < len(inputs_queue):
            valor = inputs_queue[input_index[0]]
            input_index[0] += 1
            print(f"{prompt_text}{valor}")  # Simular o que o usuário digitaria
            return valor
        else:
            # Se acabaram os inputs, sair
            return "sair"

    # Substituir input
    __builtins__.input = mock_input

    try:
        # Importar e executar Luna
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

        # Definir variáveis de ambiente
        os.environ['PYTHONUTF8'] = '1'
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        os.environ['LUNA_DISABLE_PLANNING'] = '1'  # Desabilitar planejamento avançado

        # Importar main da Luna
        from luna_v3_FINAL_OTIMIZADA import main as luna_main

        # Executar!
        luna_main()

        return 0

    except Exception as e:
        print(f"\n[ERRO] Falha na execução: {e}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        # Restaurar input original
        __builtins__.input = original_input

if __name__ == "__main__":
    sys.exit(main())
