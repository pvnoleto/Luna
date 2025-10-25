"""
Módulo para descoberta de arquivos Python em diretórios.

Este módulo implementa função para encontrar arquivos .py recursivamente,
excluindo diretórios comuns de build/cache/venv.
"""

import os
from typing import List


def find_python_files(root_path: str) -> List[str]:
    """
    Descobre recursivamente todos os arquivos Python em um diretório.
    
    Percorre o diretório raiz recursivamente usando os.walk, filtra arquivos *.py
    e exclui diretórios comuns que não devem ser analisados (venv, cache, etc).
    
    Args:
        root_path: Caminho raiz do diretório para buscar arquivos Python
        
    Returns:
        Lista de caminhos absolutos para arquivos .py encontrados
        
    Exemplo:
        >>> python_files = find_python_files('/home/user/projeto')
        >>> print(len(python_files))
        42
        >>> print(python_files[0])
        /home/user/projeto/main.py
    """
    # Set de diretórios a excluir da busca
    excluded_dirs = {
        'venv',
        '__pycache__',
        '.git',
        'node_modules',
        '.venv',
        'dist',
        'build'
    }
    
    python_files = []
    
    # Percorre recursivamente o diretório
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Remove diretórios excluídos da lista de diretórios a visitar
        # Modifica dirnames in-place para que os.walk não entre neles
        dirnames[:] = [d for d in dirnames if d not in excluded_dirs]
        
        # Filtra apenas arquivos .py
        for filename in filenames:
            if filename.endswith('.py'):
                # Cria caminho absoluto
                full_path = os.path.abspath(os.path.join(dirpath, filename))
                python_files.append(full_path)
    
    return python_files


# Teste da função se executado diretamente
if __name__ == "__main__":
    import sys
    
    # Usa diretório atual se nenhum argumento for fornecido
    root = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    print(f"🔍 Buscando arquivos Python em: {os.path.abspath(root)}")
    print(f"📂 Diretórios excluídos: venv, __pycache__, .git, node_modules, .venv, dist, build\n")
    
    files = find_python_files(root)
    
    print(f"✅ Encontrados {len(files)} arquivos Python:\n")
    for file in sorted(files):
        print(f"  • {file}")
    
    # Validação dos critérios de sucesso
    print("\n" + "="*60)
    print("VALIDAÇÃO DOS CRITÉRIOS DE SUCESSO:")
    print("="*60)
    
    # Critério 1: Função retorna lista
    print(f"✓ Função retorna lista: {isinstance(files, list)}")
    
    # Critério 2: Todos elementos terminam com .py
    all_py = all(f.endswith('.py') for f in files)
    print(f"✓ Todos elementos terminam com .py: {all_py}")
    
    # Critério 3: Nenhum caminho contém diretórios excluídos
    excluded_dirs = {'venv', '__pycache__', '.git', 'node_modules', '.venv', 'dist', 'build'}
    no_excluded = all(
        not any(f"/{excluded_dir}/" in f or f"\\{excluded_dir}\\" in f 
                for excluded_dir in excluded_dirs)
        for f in files
    )
    print(f"✓ Nenhum caminho contém diretórios excluídos: {no_excluded}")
    
    if all_py and no_excluded and isinstance(files, list):
        print("\n🎉 TODOS OS CRITÉRIOS DE SUCESSO FORAM ATENDIDOS!")
    else:
        print("\n⚠️  ALGUNS CRITÉRIOS NÃO FORAM ATENDIDOS!")
