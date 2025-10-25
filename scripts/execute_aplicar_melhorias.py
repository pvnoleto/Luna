#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Executor para aplicação de melhorias pendentes
"""

import sys
import os

# Configurar encoding
os.environ['PYTHONUTF8'] = '1'
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Adicionar diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Executa Luna para aplicar melhorias"""
    try:
        # Ler a tarefa do arquivo
        with open('tarefa_aplicar_melhorias.txt', 'r', encoding='utf-8') as f:
            tarefa = f.read().strip()

        print("="*80)
        print("APLICACAO DE MELHORIAS PENDENTES - LUNA V4")
        print("="*80)
        print("[OK] Tarefa carregada")
        print("[OK] Tier: 2 (1000 RPM)")
        print("[OK] Rate Mode: 2 (balanced - 85%)")
        print("="*80)
        print()

        # Preparar inputs simulados
        inputs_queue = [
            "2",        # Escolha de tier (2 = 1000 RPM)
            "2",        # Escolha de modo (2 = balanced)
            "n",        # Não usar cofre
            tarefa,     # O prompt da tarefa
            "",         # Confirmar prompt (Enter)
            "sair"      # Sair após completar
        ]

        input_index = [0]

        # Monkey patch input()
        original_input = __builtins__.input

        def mock_input(prompt_text=""):
            if input_index[0] < len(inputs_queue):
                valor = inputs_queue[input_index[0]]
                input_index[0] += 1
                print(f"{prompt_text}{valor}")
                return valor
            else:
                return "sair"

        # Substituir input
        __builtins__.input = mock_input

        try:
            # Importar main da Luna
            from luna_v3_FINAL_OTIMIZADA import main as luna_main

            print("[INICIO] Iniciando Luna V4 para aplicar melhorias...")
            print()

            # Executar!
            luna_main()

            return 0

        except KeyboardInterrupt:
            print("\n\n[INFO] Execução interrompida pelo usuário (Ctrl+C)")
            return 130
        except Exception as e:
            print(f"\n[ERRO] Falha na execução: {e}")
            import traceback
            traceback.print_exc()
            return 1

        finally:
            # Restaurar input original
            __builtins__.input = original_input

    except Exception as e:
        print(f"[ERRO] Falha ao iniciar: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    print(f"\n[INFO] Processo finalizado com exit code: {exit_code}")
    sys.exit(exit_code)
