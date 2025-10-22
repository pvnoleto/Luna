#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Executor de Teste do Planning System - Sprint 3
Executa Luna V4 com planning system HABILITADO (LUNA_DISABLE_PLANNING=0)
"""

import sys
import os

def main():
    # Ler a tarefa do arquivo
    with open('tarefa_planning_sprint3.txt', 'r', encoding='utf-8') as f:
        tarefa = f.read().strip()

    print("="*80)
    print("TESTE DO PLANNING SYSTEM - SPRINT 3 LUNA V4")
    print("="*80)
    print("[OK] Planning System: HABILITADO (LUNA_DISABLE_PLANNING=0)")
    print("[OK] Tier: 2 (1000 RPM)")
    print("[OK] Rate Mode: 2 (balanced - 85%)")
    print(f"[OK] Tarefa: {tarefa[:100]}...")
    print("="*80)
    print()

    # Preparar inputs simulados (mesma sequência do batch_executor)
    inputs_queue = [
        "2",        # Escolha de tier (2 = 1000 RPM)
        "2",        # Escolha de modo (2 = balanced)
        "n",        # Não usar cofre
        tarefa,     # O prompt da tarefa
        "",         # Confirmar prompt (Enter)
        "sair"      # Sair após completar
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
        # Adicionar diretório ao path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

        # Definir variáveis de ambiente
        os.environ['PYTHONUTF8'] = '1'
        os.environ['PYTHONIOENCODING'] = 'utf-8'

        # *** DIFERENCA CRITICA: HABILITAR PLANNING SYSTEM ***
        os.environ['LUNA_DISABLE_PLANNING'] = '0'  # 0 = HABILITADO (nao '1' como no batch_executor)

        # Importar main da Luna
        from luna_v3_FINAL_OTIMIZADA import main as luna_main

        print("[INICIO] Iniciando Luna V4 com Planning System habilitado...")
        print("[INFO] Esperado: Decomposicao em subtarefas + execucao coordenada")
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

if __name__ == "__main__":
    exit_code = main()
    print(f"\n[INFO] Processo finalizado com exit code: {exit_code}")
    sys.exit(exit_code)
