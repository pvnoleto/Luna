"""
Script para processar análise sequencial de todos os arquivos Python encontrados.

Implementa a SUBTAREFA 3.2: Analisar cada arquivo sequencialmente
- Carrega lista de arquivos da subtarefa 3.1 (python_files_list.json)
- Itera sobre cada arquivo e executa analyze_single_file
- Armazena FileStats em lista all_file_stats
- Captura e loga qualquer exceção sem interromper loop
- Valida critério de sucesso ao final
"""

import json
import sys
import os
from typing import List
from datetime import datetime

# Importa funções necessárias
from analyze_single_file import analyze_single_file
from file_stats import FileStats


def load_file_list(json_path: str = "python_files_list.json") -> List[str]:
    """
    Carrega lista de arquivos do JSON da subtarefa 3.1.
    
    Args:
        json_path: Caminho para o arquivo JSON com lista de arquivos
        
    Returns:
        Lista de caminhos de arquivos Python
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('files', [])
    except FileNotFoundError:
        print(f"❌ ERRO: Arquivo {json_path} não encontrado")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ ERRO: Falha ao decodificar JSON: {e}")
        return []
    except Exception as e:
        print(f"❌ ERRO inesperado ao carregar lista: {type(e).__name__}: {e}")
        return []


def process_all_files(file_list: List[str]) -> List[FileStats]:
    """
    Processa análise sequencial de todos os arquivos.
    
    Esta é a função PRINCIPAL da subtarefa 3.2:
    - Itera sobre cada arquivo da lista
    - Executa analyze_single_file para cada um
    - Armazena resultado em all_file_stats
    - Captura TODAS as exceções sem interromper o loop
    - Loga progresso e erros
    
    Args:
        file_list: Lista de caminhos de arquivos para processar
        
    Returns:
        Lista de FileStats contendo estatísticas de todos os arquivos
    """
    all_file_stats = []
    total_files = len(file_list)
    
    print(f"\n{'='*80}")
    print(f"🔄 INICIANDO ANÁLISE SEQUENCIAL DE {total_files} ARQUIVOS")
    print(f"{'='*80}\n")
    
    for index, filepath in enumerate(file_list, start=1):
        try:
            # Mostra progresso
            filename = os.path.basename(filepath)
            print(f"[{index}/{total_files}] 📄 Processando: {filename}...", end=" ")
            
            # Executa análise do arquivo
            stats = analyze_single_file(filepath)
            
            # Armazena resultado
            all_file_stats.append(stats)
            
            # Mostra resultado
            if stats.has_read_error:
                print(f"⚠️  ERRO DE LEITURA")
                print(f"    └─ {stats.error_message}")
            elif stats.has_syntax_error:
                print(f"⚠️  ERRO DE SINTAXE")
                print(f"    └─ {stats.error_message}")
            else:
                print(f"✅ OK")
                print(f"    └─ {stats.total_lines} linhas, {stats.functions} funções, {stats.classes} classes")
                
        except Exception as e:
            # CAPTURA QUALQUER EXCEÇÃO NÃO PREVISTA
            # Cria FileStats com erro registrado
            error_stats = FileStats(
                filepath=filepath,
                has_read_error=True,
                error_message=f"Exceção não tratada: {type(e).__name__}: {str(e)}"
            )
            all_file_stats.append(error_stats)
            
            print(f"❌ EXCEÇÃO NÃO PREVISTA")
            print(f"    └─ {type(e).__name__}: {str(e)}")
            
            # Continua o loop sem interromper
            continue
    
    return all_file_stats


def validate_results(file_list: List[str], all_file_stats: List[FileStats]) -> bool:
    """
    Valida critérios de sucesso da subtarefa 3.2.
    
    Critérios:
    1. len(all_file_stats) == len(file_list)
    2. Cada elemento possui estrutura FileStats válida
    
    Args:
        file_list: Lista original de arquivos
        all_file_stats: Lista de FileStats processados
        
    Returns:
        True se todos os critérios foram atendidos
    """
    print(f"\n{'='*80}")
    print(f"✅ VALIDAÇÃO DOS CRITÉRIOS DE SUCESSO")
    print(f"{'='*80}\n")
    
    success = True
    
    # CRITÉRIO 1: Quantidade de resultados
    criterion_1 = len(all_file_stats) == len(file_list)
    print(f"1️⃣  len(all_file_stats) == len(arquivos_encontrados)")
    print(f"    └─ {len(all_file_stats)} == {len(file_list)}: {'✅ PASSOU' if criterion_1 else '❌ FALHOU'}")
    
    if not criterion_1:
        success = False
    
    # CRITÉRIO 2: Estrutura FileStats válida
    print(f"\n2️⃣  Cada elemento possui estrutura FileStats válida")
    
    invalid_count = 0
    for i, stats in enumerate(all_file_stats):
        # Verifica se é instância de FileStats
        if not isinstance(stats, FileStats):
            print(f"    ❌ Elemento {i} não é FileStats: {type(stats)}")
            invalid_count += 1
            continue
            
        # Verifica campos obrigatórios
        if not hasattr(stats, 'filepath'):
            print(f"    ❌ Elemento {i} não tem campo 'filepath'")
            invalid_count += 1
            continue
            
        if not hasattr(stats, 'total_lines'):
            print(f"    ❌ Elemento {i} não tem campo 'total_lines'")
            invalid_count += 1
            continue
    
    criterion_2 = invalid_count == 0
    print(f"    └─ {len(all_file_stats)} válidos, {invalid_count} inválidos: {'✅ PASSOU' if criterion_2 else '❌ FALHOU'}")
    
    if not criterion_2:
        success = False
    
    # Resumo final
    print(f"\n{'='*80}")
    if success:
        print(f"🎉 TODOS OS CRITÉRIOS DE SUCESSO FORAM ATENDIDOS!")
    else:
        print(f"❌ ALGUNS CRITÉRIOS FALHARAM - REVISAR IMPLEMENTAÇÃO")
    print(f"{'='*80}\n")
    
    return success


def generate_summary_report(all_file_stats: List[FileStats]) -> dict:
    """
    Gera relatório resumido da análise.
    
    Args:
        all_file_stats: Lista de FileStats processados
        
    Returns:
        Dicionário com estatísticas agregadas
    """
    total_files = len(all_file_stats)
    successful = sum(1 for s in all_file_stats if not s.has_read_error and not s.has_syntax_error)
    read_errors = sum(1 for s in all_file_stats if s.has_read_error)
    syntax_errors = sum(1 for s in all_file_stats if s.has_syntax_error)
    
    total_lines = sum(s.total_lines for s in all_file_stats)
    total_code_lines = sum(s.code_lines for s in all_file_stats)
    total_functions = sum(s.functions for s in all_file_stats)
    total_classes = sum(s.classes for s in all_file_stats)
    
    return {
        'timestamp': datetime.now().isoformat(),
        'total_files_processed': total_files,
        'successful_analyses': successful,
        'read_errors': read_errors,
        'syntax_errors': syntax_errors,
        'aggregate_metrics': {
            'total_lines': total_lines,
            'total_code_lines': total_code_lines,
            'total_functions': total_functions,
            'total_classes': total_classes
        }
    }


def save_results(all_file_stats: List[FileStats], output_path: str = "analysis_results.json"):
    """
    Salva resultados da análise em JSON.
    
    Args:
        all_file_stats: Lista de FileStats processados
        output_path: Caminho para salvar JSON
    """
    try:
        # Converte FileStats para dicionários
        results = {
            'summary': generate_summary_report(all_file_stats),
            'files': [stats.to_dict() for stats in all_file_stats]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Resultados salvos em: {output_path}")
        
    except Exception as e:
        print(f"❌ Erro ao salvar resultados: {type(e).__name__}: {e}")


def main():
    """
    Função principal que executa todo o fluxo da subtarefa 3.2.
    """
    print(f"\n{'#'*80}")
    print(f"# SUBTAREFA 3.2: ANÁLISE SEQUENCIAL DE ARQUIVOS PYTHON")
    print(f"{'#'*80}\n")
    
    # Passo 1: Carregar lista de arquivos da subtarefa 3.1
    print("📋 Passo 1: Carregando lista de arquivos...")
    file_list = load_file_list("python_files_list.json")
    
    if not file_list:
        print("❌ Nenhum arquivo para processar. Abortando.")
        return 1
    
    print(f"✅ {len(file_list)} arquivos carregados\n")
    
    # Passo 2: Processar todos os arquivos sequencialmente
    print("🔄 Passo 2: Processando arquivos...")
    all_file_stats = process_all_files(file_list)
    
    # Passo 3: Validar critérios de sucesso
    print("\n✅ Passo 3: Validando resultados...")
    validation_success = validate_results(file_list, all_file_stats)
    
    # Passo 4: Gerar relatório resumido
    print("\n📊 Passo 4: Gerando relatório...")
    summary = generate_summary_report(all_file_stats)
    
    print(f"\n{'='*80}")
    print(f"📊 RESUMO DA ANÁLISE")
    print(f"{'='*80}")
    print(f"Total de arquivos processados: {summary['total_files_processed']}")
    print(f"Análises bem-sucedidas: {summary['successful_analyses']}")
    print(f"Erros de leitura: {summary['read_errors']}")
    print(f"Erros de sintaxe: {summary['syntax_errors']}")
    print(f"\nMétricas agregadas:")
    print(f"  • Total de linhas: {summary['aggregate_metrics']['total_lines']}")
    print(f"  • Linhas de código: {summary['aggregate_metrics']['total_code_lines']}")
    print(f"  • Total de funções: {summary['aggregate_metrics']['total_functions']}")
    print(f"  • Total de classes: {summary['aggregate_metrics']['total_classes']}")
    print(f"{'='*80}\n")
    
    # Passo 5: Salvar resultados
    print("💾 Passo 5: Salvando resultados...")
    save_results(all_file_stats, "analysis_results.json")
    
    print(f"\n{'#'*80}")
    print(f"# SUBTAREFA 3.2 CONCLUÍDA COM {'SUCESSO' if validation_success else 'FALHAS'}!")
    print(f"{'#'*80}\n")
    
    return 0 if validation_success else 1


if __name__ == "__main__":
    sys.exit(main())
