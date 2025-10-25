#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analisador de Telemetria - Luna V3
Processa todos os dados de telemetria coletados durante os testes automatizados
"""

import json
import os
from pathlib import Path
from collections import defaultdict
from typing import Dict, List
import statistics

def processar_arquivo_jsonl(arquivo: Path) -> List[Dict]:
    """Lê um arquivo JSONL e retorna lista de dicionários"""
    dados = []
    if not arquivo.exists():
        return dados

    with open(arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            linha = linha.strip()
            if linha:
                try:
                    dados.append(json.loads(linha))
                except json.JSONDecodeError:
                    continue
    return dados

def analisar_tarefa(tarefa_id: int, dir_telemetria: Path) -> Dict:
    """Analisa telemetria de uma tarefa específica"""

    # Ler arquivos de telemetria
    api_antes = processar_arquivo_jsonl(dir_telemetria / "telemetria_api_antes.jsonl")
    api_depois = processar_arquivo_jsonl(dir_telemetria / "telemetria_api_depois.jsonl")
    ferramentas_antes = processar_arquivo_jsonl(dir_telemetria / "telemetria_ferramentas_antes.jsonl")
    ferramentas_depois = processar_arquivo_jsonl(dir_telemetria / "telemetria_ferramentas_depois.jsonl")

    # Combinar antes e depois
    api_calls = api_antes + api_depois
    tool_calls = ferramentas_antes + ferramentas_depois

    # Análise de API
    total_input_tokens = sum(call.get('tokens_input', 0) for call in api_calls)
    total_output_tokens = sum(call.get('tokens_output', 0) for call in api_calls)
    total_cache_creation = sum(call.get('tokens_cache_creation', 0) for call in api_calls)
    total_cache_read = sum(call.get('tokens_cache_read', 0) for call in api_calls)

    cache_hits = sum(1 for call in api_calls if call.get('cache_hit', False))
    cache_hit_rate = (cache_hits / len(api_calls) * 100) if api_calls else 0

    latencias = [call.get('tempo_latencia', 0) for call in api_calls if call.get('tempo_latencia', 0) > 0]
    latencia_media = statistics.mean(latencias) if latencias else 0
    latencia_p50 = statistics.median(latencias) if latencias else 0
    latencia_p95 = statistics.quantiles(latencias, n=20)[18] if len(latencias) > 20 else (max(latencias) if latencias else 0)

    # Análise de ferramentas
    ferramentas_usadas = defaultdict(int)
    for call in tool_calls:
        ferramenta = call.get('ferramenta', 'desconhecida')
        ferramentas_usadas[ferramenta] += 1

    ferramentas_com_erro = sum(1 for call in tool_calls if call.get('resultado_tipo') == 'erro')

    tempos_ferramentas = [call.get('tempo_execucao', 0) for call in tool_calls if call.get('tempo_execucao', 0) > 0]
    tempo_medio_ferramentas = statistics.mean(tempos_ferramentas) if tempos_ferramentas else 0

    return {
        "tarefa_id": tarefa_id,
        "api": {
            "total_chamadas": len(api_calls),
            "tokens_input": total_input_tokens,
            "tokens_output": total_output_tokens,
            "tokens_cache_creation": total_cache_creation,
            "tokens_cache_read": total_cache_read,
            "cache_hit_rate": round(cache_hit_rate, 2),
            "latencia_media_s": round(latencia_media, 2),
            "latencia_p50_s": round(latencia_p50, 2),
            "latencia_p95_s": round(latencia_p95, 2)
        },
        "ferramentas": {
            "total_chamadas": len(tool_calls),
            "ferramentas_usadas": dict(ferramentas_usadas),
            "ferramentas_com_erro": ferramentas_com_erro,
            "tempo_medio_execucao_s": round(tempo_medio_ferramentas, 3)
        }
    }

def main():
    base_dir = Path(__file__).parent / "LOGS_EXECUCAO"

    resultados = []

    print("=" * 80)
    print("ANALISADOR DE TELEMETRIA - LUNA V3")
    print("=" * 80)
    print()

    # Processar cada tarefa
    for tarefa_id in range(1, 13):
        dir_telemetria = base_dir / f"tarefa_{tarefa_id:02d}_telemetria"

        if not dir_telemetria.exists():
            print(f"[AVISO] Telemetria da tarefa {tarefa_id} não encontrada")
            continue

        print(f"Processando tarefa {tarefa_id}...")
        resultado = analisar_tarefa(tarefa_id, dir_telemetria)
        resultados.append(resultado)

    print()
    print("=" * 80)
    print("RESUMO QUANTITATIVO")
    print("=" * 80)
    print()

    # Estatísticas globais
    total_api_calls = sum(r['api']['total_chamadas'] for r in resultados)
    total_input = sum(r['api']['tokens_input'] for r in resultados)
    total_output = sum(r['api']['tokens_output'] for r in resultados)
    total_cache_read = sum(r['api']['tokens_cache_read'] for r in resultados)

    cache_hit_rates = [r['api']['cache_hit_rate'] for r in resultados if r['api']['total_chamadas'] > 0]
    avg_cache_hit_rate = statistics.mean(cache_hit_rates) if cache_hit_rates else 0

    total_tool_calls = sum(r['ferramentas']['total_chamadas'] for r in resultados)

    # Ferramentas mais usadas (global)
    ferramentas_global = defaultdict(int)
    for r in resultados:
        for ferramenta, count in r['ferramentas']['ferramentas_usadas'].items():
            ferramentas_global[ferramenta] += count

    ferramentas_top_10 = sorted(ferramentas_global.items(), key=lambda x: x[1], reverse=True)[:10]

    print(f"Total de chamadas de API: {total_api_calls}")
    print(f"Total de tokens de input: {total_input:,}")
    print(f"Total de tokens de output: {total_output:,}")
    print(f"Total de tokens de cache lidos: {total_cache_read:,}")
    print(f"Cache hit rate médio: {avg_cache_hit_rate:.2f}%")
    print(f"Total de chamadas de ferramentas: {total_tool_calls}")
    print()
    print("Top 10 ferramentas mais usadas:")
    for ferramenta, count in ferramentas_top_10:
        print(f"  - {ferramenta}: {count} vezes")

    # Salvar relatório completo
    relatorio = {
        "resumo_global": {
            "total_api_calls": total_api_calls,
            "total_input_tokens": total_input,
            "total_output_tokens": total_output,
            "total_cache_read_tokens": total_cache_read,
            "cache_hit_rate_medio": round(avg_cache_hit_rate, 2),
            "total_tool_calls": total_tool_calls,
            "ferramentas_top_10": dict(ferramentas_top_10)
        },
        "detalhes_por_tarefa": resultados
    }

    output_file = base_dir / "ANALISE_TELEMETRIA.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)

    print()
    print(f"Relatório completo salvo em: {output_file}")
    print("=" * 80)

if __name__ == "__main__":
    main()
