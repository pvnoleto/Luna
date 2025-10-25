#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Batch Executor - Versão para execução automatizada

Este é um wrapper da Luna V3 que permite execução em batch mode
para testes automatizados. Recebe o prompt como argumento e executa
sem interação.
"""

import sys
import os
import argparse

# Adicionar o diretório atual ao path para importar Luna
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    parser = argparse.ArgumentParser(description='Luna V3 - Batch Mode Executor')
    parser.add_argument('prompt', help='Prompt/tarefa a executar')
    parser.add_argument('--tier', type=int, default=2, help='API Tier (1-4)')
    parser.add_argument('--rate-mode', type=int, default=2, help='Rate limit mode (1-3)')
    parser.add_argument('--no-cofre', action='store_true', help='Não usar cofre de credenciais')

    args = parser.parse_args()

    # Importar módulos da Luna
    from luna_v3_FINAL_OTIMIZADA import AgenteCompletoV3

    print("="*80)
    print("LUNA V3 - BATCH MODE")
    print("="*80)
    print(f"Tier: {args.tier}")
    print(f"Rate Mode: {args.rate_mode}")
    print(f"Prompt: {args.prompt[:100]}...")
    print("="*80)
    print()

    # Configurar tier e modo
    os.environ['LUNA_BATCH_MODE'] = '1'
    os.environ['LUNA_TIER'] = str(args.tier)
    os.environ['LUNA_RATE_MODE'] = str(args.rate_mode)
    os.environ['LUNA_NO_COFRE'] = '1' if args.no_cofre else '0'

    # Criar agente
    try:
        tier_escolhido = args.tier
        modo_escolhido = args.rate_mode
        usar_cofre = not args.no_cofre

        # Importar componentes necessários
        from luna_v3_FINAL_OTIMIZADA import (
            RateLimitManager,
            InterruptHandler,
            SistemaFerramentasCompleto
        )

        # Mapear tier e modo para strings
        tier_map = {1: "tier1", 2: "tier2", 3: "tier3", 4: "tier4"}
        modo_map = {1: "conservador", 2: "balanceado", 3: "agressivo"}

        tier_str = tier_map.get(tier_escolhido, "tier2")
        modo_str = modo_map.get(modo_escolhido, "balanceado")

        # Inicializar rate limiter
        rate_limiter = RateLimitManager(tier=tier_str, modo=modo_str)

        # Inicializar sistema de ferramentas
        # master_password=None desabilita o cofre
        sistema_ferramentas = SistemaFerramentasCompleto(
            master_password=None,
            usar_memoria=True
        )

        # Inicializar interrupt handler
        interrupt_handler = InterruptHandler(
            navegador=sistema_ferramentas.navegador if hasattr(sistema_ferramentas, 'navegador') else None,
            rate_limiter=rate_limiter
        )

        # Criar agente
        agente = AgenteCompletoV3(
            sistema_ferramentas=sistema_ferramentas,
            rate_limiter=rate_limiter,
            usar_iteracao_profunda=False,  # Desabilitar para batch
            usar_planejamento_avancado=True
        )

        print("\n" + "="*80)
        print("EXECUTANDO TAREFA...")
        print("="*80 + "\n")

        # Executar tarefa
        resposta_final = agente.executar_com_recuperacao(args.prompt)

        print("\n" + "="*80)
        print("TAREFA CONCLUÍDA")
        print("="*80)
        print(f"\nResposta final:\n{resposta_final}\n")

        # Limpeza
        interrupt_handler.cleanup()

        return 0

    except Exception as e:
        print(f"\n[ERRO] Falha na execução: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
