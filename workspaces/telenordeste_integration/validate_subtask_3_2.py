"""
Script de validação final da SUBTAREFA 3.2.

Valida que todos os critérios de sucesso foram atendidos:
1. len(all_file_stats) == len(arquivos_encontrados)
2. Cada elemento possui estrutura FileStats válida
"""

import json
import sys


def validate_subtask_3_2():
    """
    Valida completamente a subtarefa 3.2.
    
    Returns:
        True se todos os critérios foram atendidos
    """
    print("\n" + "="*80)
    print("🔍 VALIDAÇÃO FINAL DA SUBTAREFA 3.2")
    print("="*80 + "\n")
    
    # Carrega lista original de arquivos
    try:
        with open('python_files_list.json', 'r', encoding='utf-8') as f:
            file_list_data = json.load(f)
            arquivos_encontrados = file_list_data.get('files', [])
            total_arquivos = file_list_data.get('total', len(arquivos_encontrados))
    except Exception as e:
        print(f"❌ ERRO ao carregar python_files_list.json: {e}")
        return False
    
    # Carrega resultados da análise
    try:
        with open('analysis_results.json', 'r', encoding='utf-8') as f:
            results = json.load(f)
            all_file_stats = results.get('files', [])
            summary = results.get('summary', {})
    except Exception as e:
        print(f"❌ ERRO ao carregar analysis_results.json: {e}")
        return False
    
    print(f"📋 Dados carregados:")
    print(f"   • Arquivos na lista original: {len(arquivos_encontrados)}")
    print(f"   • FileStats processados: {len(all_file_stats)}")
    print(f"   • Total declarado: {total_arquivos}\n")
    
    success = True
    
    # CRITÉRIO 1: len(all_file_stats) == len(arquivos_encontrados)
    print("="*80)
    print("CRITÉRIO 1: len(all_file_stats) == len(arquivos_encontrados)")
    print("="*80)
    
    criterion_1_pass = len(all_file_stats) == len(arquivos_encontrados)
    print(f"\n✓ Quantidade de FileStats: {len(all_file_stats)}")
    print(f"✓ Quantidade de arquivos originais: {len(arquivos_encontrados)}")
    print(f"✓ Igualdade: {len(all_file_stats)} == {len(arquivos_encontrados)}")
    
    if criterion_1_pass:
        print(f"\n✅ CRITÉRIO 1 PASSOU: Todos os arquivos foram processados!")
    else:
        print(f"\n❌ CRITÉRIO 1 FALHOU: Quantidade de FileStats não corresponde!")
        success = False
    
    # CRITÉRIO 2: Cada elemento possui estrutura FileStats válida
    print("\n" + "="*80)
    print("CRITÉRIO 2: Cada elemento possui estrutura FileStats válida")
    print("="*80 + "\n")
    
    required_fields = [
        'filepath',
        'total_lines',
        'blank_lines',
        'comment_lines',
        'code_lines',
        'functions',
        'classes',
        'imports_list',
        'encoding_used',
        'encoding_success',
        'has_syntax_error',
        'has_read_error',
        'error_message'
    ]
    
    invalid_stats = []
    
    for i, stats in enumerate(all_file_stats):
        # Verifica se é dicionário
        if not isinstance(stats, dict):
            invalid_stats.append({
                'index': i,
                'error': f'Não é dicionário: {type(stats)}'
            })
            continue
        
        # Verifica campos obrigatórios
        missing_fields = []
        for field in required_fields:
            if field not in stats:
                missing_fields.append(field)
        
        if missing_fields:
            invalid_stats.append({
                'index': i,
                'filepath': stats.get('filepath', 'UNKNOWN'),
                'error': f'Campos faltando: {", ".join(missing_fields)}'
            })
    
    criterion_2_pass = len(invalid_stats) == 0
    
    print(f"✓ Total de FileStats analisados: {len(all_file_stats)}")
    print(f"✓ FileStats válidos: {len(all_file_stats) - len(invalid_stats)}")
    print(f"✓ FileStats inválidos: {len(invalid_stats)}")
    
    if invalid_stats:
        print(f"\n⚠️  FileStats inválidos encontrados:")
        for invalid in invalid_stats[:5]:  # Mostra até 5 exemplos
            print(f"   • Índice {invalid['index']}: {invalid['error']}")
        if len(invalid_stats) > 5:
            print(f"   ... e mais {len(invalid_stats) - 5} inválidos")
    
    if criterion_2_pass:
        print(f"\n✅ CRITÉRIO 2 PASSOU: Todos os FileStats têm estrutura válida!")
    else:
        print(f"\n❌ CRITÉRIO 2 FALHOU: {len(invalid_stats)} FileStats inválidos!")
        success = False
    
    # RESUMO ESTATÍSTICO
    print("\n" + "="*80)
    print("📊 RESUMO ESTATÍSTICO DA ANÁLISE")
    print("="*80 + "\n")
    
    print(f"Total de arquivos processados: {summary.get('total_files_processed', 0)}")
    print(f"Análises bem-sucedidas: {summary.get('successful_analyses', 0)}")
    print(f"Erros de leitura: {summary.get('read_errors', 0)}")
    print(f"Erros de sintaxe: {summary.get('syntax_errors', 0)}")
    
    if 'aggregate_metrics' in summary:
        metrics = summary['aggregate_metrics']
        print(f"\nMétricas agregadas:")
        print(f"  • Total de linhas: {metrics.get('total_lines', 0):,}")
        print(f"  • Linhas de código: {metrics.get('total_code_lines', 0):,}")
        print(f"  • Total de funções: {metrics.get('total_functions', 0)}")
        print(f"  • Total de classes: {metrics.get('total_classes', 0)}")
    
    # VALIDAÇÃO ADICIONAL: Todos os caminhos correspondem?
    print("\n" + "="*80)
    print("🔍 VALIDAÇÃO ADICIONAL: Correspondência de caminhos")
    print("="*80 + "\n")
    
    processed_paths = {stats['filepath'] for stats in all_file_stats}
    original_paths = set(arquivos_encontrados)
    
    missing_paths = original_paths - processed_paths
    extra_paths = processed_paths - original_paths
    
    if not missing_paths and not extra_paths:
        print("✅ Todos os caminhos correspondem perfeitamente!")
    else:
        if missing_paths:
            print(f"⚠️  {len(missing_paths)} caminhos NÃO foram processados:")
            for path in list(missing_paths)[:3]:
                print(f"   • {path}")
            if len(missing_paths) > 3:
                print(f"   ... e mais {len(missing_paths) - 3}")
        
        if extra_paths:
            print(f"⚠️  {len(extra_paths)} caminhos EXTRAS foram processados:")
            for path in list(extra_paths)[:3]:
                print(f"   • {path}")
            if len(extra_paths) > 3:
                print(f"   ... e mais {len(extra_paths) - 3}")
    
    # RESULTADO FINAL
    print("\n" + "="*80)
    print("🎯 RESULTADO FINAL DA VALIDAÇÃO")
    print("="*80 + "\n")
    
    if success:
        print("🎉 ✅ TODOS OS CRITÉRIOS DE SUCESSO FORAM ATENDIDOS!")
        print("\n✓ SUBTAREFA 3.2 CONCLUÍDA COM SUCESSO!")
        print("\nOUTPUT GERADO:")
        print(f"  • Lista all_file_stats com {len(all_file_stats)} elementos")
        print(f"  • Cada elemento possui estrutura FileStats válida")
        print(f"  • Arquivo analysis_results.json salvo com sucesso")
        print(f"  • {summary.get('successful_analyses', 0)} arquivos analisados sem erros")
    else:
        print("❌ ALGUNS CRITÉRIOS FALHARAM!")
        print("\n⚠️  SUBTAREFA 3.2 PRECISA DE CORREÇÕES!")
    
    print("\n" + "="*80 + "\n")
    
    return success


if __name__ == "__main__":
    success = validate_subtask_3_2()
    sys.exit(0 if success else 1)
