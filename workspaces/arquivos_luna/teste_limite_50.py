#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
from agente_completo_final import AgenteCompletoFinal

load_dotenv()

def testar_limite():
    print("="*70)
    print("TESTE DO LIMITE DE ITERACOES (deve ser 50)")
    print("="*70)
    
    # Tarefa simples mas que vai gerar múltiplas iterações
    tarefa = """
    Crie 3 arquivos Python simples na pasta teste_limite/:
    1. calculadora.py - com funções de soma, subtração, multiplicação e divisão
    2. teste_calculadora.py - com testes unitários 
    3. main.py - que importa e usa a calculadora
    
    Depois execute os testes para verificar que funciona.
    """
    
    agente = AgenteCompletoFinal(
        api_key=os.getenv('ANTHROPIC_API_KEY'),
        master_password=None,
        usar_memoria=False
    )
    
    print("\nIniciando teste com limite de 50 iteracoes...")
    print()
    
    try:
        agente.executar_tarefa(tarefa)
        print("\n" + "="*70)
        print("TESTE CONCLUIDO")
        print("="*70)
    except Exception as e:
        print(f"\nErro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_limite()
