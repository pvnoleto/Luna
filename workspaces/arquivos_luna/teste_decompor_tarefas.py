#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste do sistema de decomposição de tarefas
Verifica se o limite de iterações está em 50
"""

import os
from dotenv import load_dotenv
from agente_completo_final import AgenteCompletoFinal

load_dotenv()

def testar_limite_iteracoes():
    """Testa com tarefa complexa para verificar limite"""
    
    print("="*70)
    print("🧪 TESTE DO LIMITE DE ITERAÇÕES (deve ser 50)")
    print("="*70)
    
    # Tarefa complexa que vai decompor em várias etapas
    tarefa_complexa = """
    Crie um sistema completo de análise de dados com os seguintes componentes:
    
    1. Um módulo de coleta de dados (data_collector.py) que:
       - Lê dados de múltiplas fontes (CSV, JSON, API)
       - Valida os dados recebidos
       - Trata erros e exceções
    
    2. Um módulo de processamento (data_processor.py) que:
       - Limpa dados duplicados
       - Normaliza valores
       - Calcula estatísticas básicas (média, mediana, desvio padrão)
    
    3. Um módulo de visualização (data_visualizer.py) que:
       - Gera gráficos com matplotlib
       - Cria relatórios em HTML
       - Exporta resultados em PDF
    
    4. Um arquivo main.py que:
       - Integra todos os módulos
       - Tem interface de linha de comando
       - Gera logs de execução
    
    5. Testes unitários para cada módulo
    
    6. Um README.md completo com documentação
    
    Após criar tudo, execute os testes para verificar que funciona.
    """
    
    # Inicializar agente (sem senha para teste)
    agente = AgenteCompletoFinal(
        api_key=os.getenv('ANTHROPIC_API_KEY'),
        master_password=None,
        usar_memoria=False  # Desabilitar memória para teste puro
    )
    
    print("\n📋 Tarefa complexa definida")
    print("⏱️  Iniciando execução com limite de 50 iterações...")
    print()
    
    try:
        agente.executar_tarefa(tarefa_complexa)
        print("\n" + "="*70)
        print("✅ TESTE CONCLUÍDO")
        print("="*70)
    except Exception as e:
        print(f"\n❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_limite_iteracoes()
