"""
Exemplo de uso do módulo line_counter.

Demonstra como usar a função count_lines_and_comments para analisar
arquivos Python no projeto.
"""

from line_counter import count_lines_and_comments
from find_python_files import find_python_files
from file_reader import read_file_with_fallback


def analisar_projeto(root_path: str):
    """
    Analisa todos os arquivos Python de um projeto.
    
    Args:
        root_path: Caminho raiz do projeto
    """
    print(f"🔍 Analisando projeto em: {root_path}\n")
    
    # Encontra todos os arquivos Python
    arquivos = find_python_files(root_path)
    print(f"📂 Encontrados {len(arquivos)} arquivos Python\n")
    
    # Estatísticas totais
    total_stats = {
        'total_lines': 0,
        'blank_lines': 0,
        'comment_lines': 0,
        'code_lines': 0
    }
    
    arquivos_analisados = []
    
    # Analisa cada arquivo
    for filepath in arquivos:
        try:
            # Lê o arquivo
            content, encoding, success = read_file_with_fallback(filepath)
            
            # Conta linhas
            stats = count_lines_and_comments(content)
            
            # Acumula estatísticas
            for key in total_stats:
                total_stats[key] += stats[key]
            
            # Salva para relatório
            arquivos_analisados.append({
                'path': filepath,
                'stats': stats,
                'encoding': encoding
            })
            
        except Exception as e:
            print(f"⚠️  Erro ao analisar {filepath}: {e}")
    
    # Exibe relatório
    print("="*70)
    print("RELATÓRIO DE ANÁLISE")
    print("="*70)
    
    print(f"\n📊 ESTATÍSTICAS TOTAIS:")
    print(f"  Total de linhas:      {total_stats['total_lines']:,}")
    print(f"  Linhas em branco:     {total_stats['blank_lines']:,} ({total_stats['blank_lines']/max(total_stats['total_lines'],1)*100:.1f}%)")
    print(f"  Linhas de comentário: {total_stats['comment_lines']:,} ({total_stats['comment_lines']/max(total_stats['total_lines'],1)*100:.1f}%)")
    print(f"  Linhas de código:     {total_stats['code_lines']:,} ({total_stats['code_lines']/max(total_stats['total_lines'],1)*100:.1f}%)")
    
    # Top 5 maiores arquivos
    print(f"\n📈 TOP 5 MAIORES ARQUIVOS (por linhas de código):")
    arquivos_ordenados = sorted(
        arquivos_analisados, 
        key=lambda x: x['stats']['code_lines'], 
        reverse=True
    )[:5]
    
    for i, info in enumerate(arquivos_ordenados, 1):
        nome_arquivo = info['path'].split('\\')[-1]
        stats = info['stats']
        print(f"\n  {i}. {nome_arquivo}")
        print(f"     Total: {stats['total_lines']} linhas")
        print(f"     Código: {stats['code_lines']} linhas")
        print(f"     Comentários: {stats['comment_lines']} linhas")
        print(f"     Brancos: {stats['blank_lines']} linhas")
    
    return total_stats, arquivos_analisados


if __name__ == "__main__":
    import sys
    import os
    
    # Usa diretório atual se nenhum for especificado
    root = sys.argv[1] if len(sys.argv) > 1 else '.'
    root = os.path.abspath(root)
    
    print("=" * 70)
    print("ANALISADOR DE LINHAS E COMENTÁRIOS PYTHON")
    print("=" * 70)
    print()
    
    total_stats, arquivos = analisar_projeto(root)
    
    print("\n" + "="*70)
    print(f"✅ Análise concluída! {len(arquivos)} arquivos processados.")
    print("="*70)
