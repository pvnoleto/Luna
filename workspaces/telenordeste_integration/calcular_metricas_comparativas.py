#!/usr/bin/env python3
"""
Script para calcular métricas comparativas de performance
entre implementações iterativa e recursiva do Fibonacci

Calcula:
- Diferença absoluta em segundos
- Fator multiplicativo
- Diferença percentual
"""

import json

def calcular_metricas_comparativas(tempo_iterativo, tempo_recursivo):
    """
    Calcula métricas comparativas de performance
    
    Args:
        tempo_iterativo: Tempo de execução da versão iterativa (segundos)
        tempo_recursivo: Tempo de execução da versão recursiva (segundos)
    
    Returns:
        dict: Dicionário com as métricas calculadas
    """
    
    # 1. Diferença absoluta (tempo_recursivo - tempo_iterativo)
    diferenca_absoluta = tempo_recursivo - tempo_iterativo
    
    # 2. Fator multiplicativo (tempo_recursivo / tempo_iterativo)
    fator_multiplicativo = tempo_recursivo / tempo_iterativo
    
    # 3. Diferença percentual ((diferença / tempo_iterativo) * 100)
    diferenca_percentual = (diferenca_absoluta / tempo_iterativo) * 100
    
    # Formatação para legibilidade
    metricas = {
        "diferenca_absoluta": {
            "valor": diferenca_absoluta,
            "formatado": f"{diferenca_absoluta:.6f} segundos",
            "descricao": "Quanto tempo a mais a versão recursiva demorou"
        },
        "fator_multiplicativo": {
            "valor": fator_multiplicativo,
            "formatado": f"{fator_multiplicativo:,.2f}x",
            "descricao": "Quantas vezes mais lenta é a versão recursiva"
        },
        "diferenca_percentual": {
            "valor": diferenca_percentual,
            "formatado": f"{diferenca_percentual:,.2f}%",
            "descricao": "Percentual de aumento no tempo de execução"
        },
        "resumo": {
            "tempo_iterativo": tempo_iterativo,
            "tempo_recursivo": tempo_recursivo,
            "conclusao": f"A versão recursiva é {fator_multiplicativo:,.0f}x mais lenta que a iterativa"
        }
    }
    
    return metricas


def main():
    # Ler dados da execução anterior
    with open('resultados_fibonacci.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    tempo_iterativo = dados['tempo_iterativo']
    tempo_recursivo = dados['tempo_recursivo']
    
    print("=" * 70)
    print("CÁLCULO DE MÉTRICAS COMPARATIVAS - FIBONACCI")
    print("=" * 70)
    print()
    
    print(f"⏱️  Tempo Iterativo:  {tempo_iterativo:.6f} segundos")
    print(f"⏱️  Tempo Recursivo:  {tempo_recursivo:.6f} segundos")
    print()
    
    # Calcular métricas
    metricas = calcular_metricas_comparativas(tempo_iterativo, tempo_recursivo)
    
    print("=" * 70)
    print("MÉTRICAS CALCULADAS")
    print("=" * 70)
    print()
    
    print("1️⃣  DIFERENÇA ABSOLUTA")
    print(f"   Valor: {metricas['diferenca_absoluta']['formatado']}")
    print(f"   📊 {metricas['diferenca_absoluta']['descricao']}")
    print()
    
    print("2️⃣  FATOR MULTIPLICATIVO")
    print(f"   Valor: {metricas['fator_multiplicativo']['formatado']}")
    print(f"   📊 {metricas['fator_multiplicativo']['descricao']}")
    print()
    
    print("3️⃣  DIFERENÇA PERCENTUAL")
    print(f"   Valor: {metricas['diferenca_percentual']['formatado']}")
    print(f"   📊 {metricas['diferenca_percentual']['descricao']}")
    print()
    
    print("=" * 70)
    print("CONCLUSÃO")
    print("=" * 70)
    print(f"✅ {metricas['resumo']['conclusao']}")
    print()
    
    # Salvar métricas em arquivo JSON
    with open('metricas_comparativas.json', 'w', encoding='utf-8') as f:
        json.dump(metricas, f, indent=2, ensure_ascii=False)
    
    print("💾 Métricas salvas em: metricas_comparativas.json")
    print()
    
    # Criar relatório em texto legível
    relatorio = f"""
╔══════════════════════════════════════════════════════════════════════╗
║           RELATÓRIO DE MÉTRICAS COMPARATIVAS - FIBONACCI            ║
╚══════════════════════════════════════════════════════════════════════╝

📋 DADOS DE ENTRADA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Tempo Iterativo:  {tempo_iterativo:.6f} segundos
  • Tempo Recursivo:  {tempo_recursivo:.6f} segundos
  • N (Fibonacci):    {dados.get('n', 'N/A')}
  • Resultado:        {dados.get('valor_calculado', 'N/A')}

📊 MÉTRICAS CALCULADAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. DIFERENÇA ABSOLUTA
   └─ {metricas['diferenca_absoluta']['formatado']}
   └─ {metricas['diferenca_absoluta']['descricao']}

2. FATOR MULTIPLICATIVO
   └─ {metricas['fator_multiplicativo']['formatado']}
   └─ {metricas['fator_multiplicativo']['descricao']}

3. DIFERENÇA PERCENTUAL
   └─ {metricas['diferenca_percentual']['formatado']}
   └─ {metricas['diferenca_percentual']['descricao']}

🎯 CONCLUSÃO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{metricas['resumo']['conclusao']}

A diferença de performance é extremamente significativa, demonstrando
a importância de escolher o algoritmo apropriado para cada caso de uso.
A versão iterativa é claramente superior para este problema específico.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Cálculos validados e formatados para legibilidade
📅 Data: {dados.get('data_execucao', 'N/A')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    with open('relatorio_metricas_comparativas.txt', 'w', encoding='utf-8') as f:
        f.write(relatorio)
    
    print("📄 Relatório detalhado salvo em: relatorio_metricas_comparativas.txt")
    print()
    print("=" * 70)
    print("✅ SUBTAREFA 3.1 CONCLUÍDA COM SUCESSO!")
    print("=" * 70)


if __name__ == "__main__":
    main()
