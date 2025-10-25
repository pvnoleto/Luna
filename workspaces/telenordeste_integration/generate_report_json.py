"""
Módulo para geração de estrutura JSON do relatório de análise.

SUBTAREFA 5.1: Criar estrutura JSON do relatório

Implementa a função que monta o dicionário final com todas as seções
do relatório de análise de código Python, pronto para serialização JSON.

Estrutura do relatório:
- summary: Resumo geral da análise (subtarefa 4.1)
- top_imports: Módulos mais importados (subtarefa 4.2)
- files_by_comments: Arquivos ordenados por comentários (subtarefa 4.3)
- file_details: Detalhes de cada arquivo (subtarefa 4.4)
- metadata: Timestamp e versão do analisador
"""

from typing import Dict, List, Any
from datetime import datetime
import json


def generate_report_structure(
    summary: Dict[str, Any],
    top_imports: List[Dict[str, Any]],
    files_by_comments: List[Dict[str, Any]],
    file_details: List[Dict[str, Any]],
    analyzer_version: str = "1.0.0"
) -> Dict[str, Any]:
    """
    Gera estrutura JSON completa do relatório de análise.
    
    Monta dicionário final com todas as seções do relatório, incluindo
    metadados com timestamp ISO8601 e versão do analisador.
    
    Args:
        summary: Dicionário com resumo geral (da subtarefa 4.1)
            Exemplo: {
                'total_files': 50,
                'total_lines': 10000,
                'total_functions': 200,
                'total_classes': 50,
                'total_imports': 100,
                'files_with_errors': 2
            }
            
        top_imports: Lista de dicts com módulos mais importados (da subtarefa 4.2)
            Exemplo: [
                {'module': 'os', 'count': 25},
                {'module': 'sys', 'count': 20}
            ]
            
        files_by_comments: Lista de dicts com arquivos ordenados (da subtarefa 4.3)
            Exemplo: [
                {
                    'filepath': '/path/to/file.py',
                    'comment_lines': 50,
                    'comment_ratio': 0.25
                }
            ]
            
        file_details: Lista de dicts com detalhes completos (da subtarefa 4.4)
            Exemplo: [
                {
                    'filepath': '/path/to/file.py',
                    'total_lines': 100,
                    'code_lines': 70,
                    'functions': 5,
                    'classes': 2,
                    'imports': ['os', 'sys']
                }
            ]
            
        analyzer_version: Versão do analisador (default: "1.0.0")
        
    Returns:
        Dicionário Python completo com estrutura JSON do relatório,
        contendo todas as chaves obrigatórias e tipos JSON-serializáveis.
        
    Exemplo:
        >>> summary = {'total_files': 10, 'total_lines': 1000}
        >>> top_imports = [{'module': 'os', 'count': 5}]
        >>> files_by_comments = [{'filepath': 'test.py', 'comment_lines': 10}]
        >>> file_details = [{'filepath': 'test.py', 'total_lines': 100}]
        >>> report = generate_report_structure(
        ...     summary, top_imports, files_by_comments, file_details
        ... )
        >>> print(report.keys())
        dict_keys(['summary', 'top_imports', 'files_by_comments', 'file_details', 'metadata'])
    """
    
    # Gera timestamp ISO8601 no momento da criação do relatório
    timestamp_iso = datetime.now().isoformat()
    
    # Monta estrutura completa do relatório
    report = {
        'summary': summary,
        'top_imports': top_imports,
        'files_by_comments': files_by_comments,
        'file_details': file_details,
        'metadata': {
            'timestamp': timestamp_iso,
            'analyzer_version': analyzer_version,
            'format_version': '1.0'
        }
    }
    
    return report


def validate_report_structure(report: Dict[str, Any]) -> bool:
    """
    Valida se a estrutura do relatório está completa e correta.
    
    Verifica:
    - Presença de todas as chaves obrigatórias
    - Tipos corretos para cada seção
    - Estrutura aninhada válida
    - Tipos JSON-serializáveis
    
    Args:
        report: Dicionário do relatório a ser validado
        
    Returns:
        True se estrutura é válida, False caso contrário
    """
    required_keys = ['summary', 'top_imports', 'files_by_comments', 'file_details', 'metadata']
    
    # Verifica presença de todas as chaves obrigatórias
    for key in required_keys:
        if key not in report:
            print(f"❌ Chave obrigatória ausente: {key}")
            return False
    
    # Valida tipos das seções
    if not isinstance(report['summary'], dict):
        print(f"❌ 'summary' deve ser dict, recebido: {type(report['summary'])}")
        return False
    
    if not isinstance(report['top_imports'], list):
        print(f"❌ 'top_imports' deve ser list, recebido: {type(report['top_imports'])}")
        return False
    
    if not isinstance(report['files_by_comments'], list):
        print(f"❌ 'files_by_comments' deve ser list, recebido: {type(report['files_by_comments'])}")
        return False
    
    if not isinstance(report['file_details'], list):
        print(f"❌ 'file_details' deve ser list, recebido: {type(report['file_details'])}")
        return False
    
    if not isinstance(report['metadata'], dict):
        print(f"❌ 'metadata' deve ser dict, recebido: {type(report['metadata'])}")
        return False
    
    # Valida estrutura de metadata
    metadata_keys = ['timestamp', 'analyzer_version']
    for key in metadata_keys:
        if key not in report['metadata']:
            print(f"❌ Chave obrigatória ausente em metadata: {key}")
            return False
    
    # Testa serialização JSON
    try:
        json.dumps(report)
    except (TypeError, ValueError) as e:
        print(f"❌ Estrutura não é JSON-serializável: {e}")
        return False
    
    return True


def save_report_json(report: Dict[str, Any], output_path: str = "analysis_report.json") -> bool:
    """
    Salva relatório em arquivo JSON formatado.
    
    Args:
        report: Dicionário do relatório
        output_path: Caminho do arquivo de saída
        
    Returns:
        True se salvou com sucesso, False caso contrário
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"✅ Relatório salvo em: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar relatório: {e}")
        return False


# ============================================================================
# TESTES E VALIDAÇÃO
# ============================================================================

def test_generate_report_structure():
    """Testa a geração de estrutura do relatório."""
    print("🧪 Testando generate_report_structure...")
    print("="*80)
    
    # Dados de exemplo simulando resultados das subtarefas 4.1, 4.2, 4.3, 4.4
    
    # Subtarefa 4.1: Summary
    summary = {
        'total_files': 50,
        'total_lines': 12500,
        'total_code_lines': 9000,
        'total_comment_lines': 2000,
        'total_blank_lines': 1500,
        'total_functions': 250,
        'total_classes': 75,
        'total_imports': 150,
        'files_with_errors': 3,
        'files_with_syntax_errors': 1,
        'files_with_read_errors': 2,
        'average_lines_per_file': 250.0,
        'average_functions_per_file': 5.0,
        'average_classes_per_file': 1.5
    }
    
    # Subtarefa 4.2: Top imports
    top_imports = [
        {'module': 'os', 'count': 35, 'percentage': 70.0},
        {'module': 'sys', 'count': 28, 'percentage': 56.0},
        {'module': 'json', 'count': 25, 'percentage': 50.0},
        {'module': 'datetime', 'count': 20, 'percentage': 40.0},
        {'module': 'pathlib', 'count': 18, 'percentage': 36.0}
    ]
    
    # Subtarefa 4.3: Files by comments
    files_by_comments = [
        {
            'filepath': '/project/src/main.py',
            'comment_lines': 150,
            'code_lines': 450,
            'comment_ratio': 0.25,
            'total_lines': 600
        },
        {
            'filepath': '/project/src/utils.py',
            'comment_lines': 80,
            'code_lines': 320,
            'comment_ratio': 0.20,
            'total_lines': 400
        },
        {
            'filepath': '/project/tests/test_main.py',
            'comment_lines': 45,
            'code_lines': 255,
            'comment_ratio': 0.15,
            'total_lines': 300
        }
    ]
    
    # Subtarefa 4.4: File details
    file_details = [
        {
            'filepath': '/project/src/main.py',
            'total_lines': 600,
            'code_lines': 450,
            'comment_lines': 150,
            'blank_lines': 0,
            'functions': 15,
            'classes': 5,
            'imports': ['os', 'sys', 'json', 'datetime'],
            'has_errors': False
        },
        {
            'filepath': '/project/src/utils.py',
            'total_lines': 400,
            'code_lines': 320,
            'comment_lines': 80,
            'blank_lines': 0,
            'functions': 20,
            'classes': 3,
            'imports': ['os', 'pathlib', 'typing'],
            'has_errors': False
        },
        {
            'filepath': '/project/tests/test_main.py',
            'total_lines': 300,
            'code_lines': 255,
            'comment_lines': 45,
            'blank_lines': 0,
            'functions': 10,
            'classes': 0,
            'imports': ['unittest', 'main'],
            'has_errors': False
        }
    ]
    
    # Gera estrutura do relatório
    print("\n📋 Gerando estrutura do relatório...")
    report = generate_report_structure(
        summary=summary,
        top_imports=top_imports,
        files_by_comments=files_by_comments,
        file_details=file_details,
        analyzer_version="1.0.0"
    )
    
    # Valida estrutura
    print("\n🔍 Validando estrutura...")
    is_valid = validate_report_structure(report)
    
    if is_valid:
        print("\n✅ ESTRUTURA VÁLIDA!")
        
        # Mostra informações sobre o relatório
        print("\n📊 Informações do relatório:")
        print(f"  - Chaves principais: {list(report.keys())}")
        print(f"  - Total de arquivos: {report['summary']['total_files']}")
        print(f"  - Total de linhas: {report['summary']['total_lines']}")
        print(f"  - Top imports: {len(report['top_imports'])} módulos")
        print(f"  - Files by comments: {len(report['files_by_comments'])} arquivos")
        print(f"  - File details: {len(report['file_details'])} arquivos")
        print(f"  - Timestamp: {report['metadata']['timestamp']}")
        print(f"  - Versão do analisador: {report['metadata']['analyzer_version']}")
        
        # Testa serialização JSON
        print("\n📝 Testando serialização JSON...")
        try:
            json_str = json.dumps(report, indent=2, ensure_ascii=False)
            json_size = len(json_str)
            print(f"  ✅ JSON serializado com sucesso ({json_size} bytes)")
            
            # Mostra primeiras linhas do JSON
            print("\n📄 Primeiras linhas do JSON gerado:")
            print("-"*80)
            first_lines = '\n'.join(json_str.split('\n')[:20])
            print(first_lines)
            print("...")
            print("-"*80)
            
        except Exception as e:
            print(f"  ❌ Erro na serialização: {e}")
            return False
        
        # Salva em arquivo de exemplo
        print("\n💾 Salvando relatório de exemplo...")
        save_report_json(report, "example_report.json")
        
        return True
    else:
        print("\n❌ ESTRUTURA INVÁLIDA!")
        return False


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🚀 SUBTAREFA 5.1: Criar estrutura JSON do relatório")
    print("="*80 + "\n")
    
    success = test_generate_report_structure()
    
    print("\n" + "="*80)
    if success:
        print("✅ SUBTAREFA 5.1 CONCLUÍDA COM SUCESSO!")
    else:
        print("❌ SUBTAREFA 5.1 FALHOU!")
    print("="*80 + "\n")
    
    # Retorna código de saída apropriado
    import sys
    sys.exit(0 if success else 1)
