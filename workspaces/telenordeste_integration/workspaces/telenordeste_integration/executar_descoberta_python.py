"""
Script para executar a descoberta de arquivos Python e validar critérios de sucesso.

SUBTAREFA 3.1: Descobrir todos os arquivos Python no workspace
"""

import os
import sys
from find_python_files import find_python_files


def main():
    """Executa descoberta e valida critérios de sucesso."""
    
    print("="*70)
    print("SUBTAREFA 3.1: Descobrir todos os arquivos Python no workspace")
    print("="*70)
    print()
    
    # INPUT: Diretório raiz do workspace (current directory)
    root_dir = '.'
    abs_root = os.path.abspath(root_dir)
    
    print(f"📂 INPUT: Diretório raiz = '{root_dir}'")
    print(f"   Caminho absoluto: {abs_root}")
    print()
    
    # Executar find_python_files('.')
    print("🔍 Executando: find_python_files('.')")
    print()
    
    try:
        python_files = find_python_files(root_dir)
        
        # Logar quantidade encontrada
        total_files = len(python_files)
        print(f"✅ SUCESSO: Função executada com sucesso!")
        print(f"📊 Quantidade encontrada: {total_files} arquivos Python")
        print()
        
        # Validar que lista não está vazia ou preparar para caso de 0 arquivos
        if total_files == 0:
            print("⚠️  ATENÇÃO: Nenhum arquivo Python encontrado no workspace.")
            print("   Isso pode ser normal se o workspace estiver vazio.")
        else:
            print(f"✓ Lista não está vazia: {total_files} arquivos encontrados")
        
        print()
        print("="*70)
        print("OUTPUT ESPERADO: Lista de caminhos de arquivos Python")
        print("="*70)
        print()
        
        # Mostrar os primeiros 10 arquivos como amostra
        print("📋 Amostra dos arquivos encontrados (primeiros 10):")
        for i, file_path in enumerate(sorted(python_files)[:10], 1):
            # Mostrar caminho relativo para melhor legibilidade
            rel_path = os.path.relpath(file_path, abs_root)
            print(f"   {i:2d}. {rel_path}")
        
        if total_files > 10:
            print(f"   ... e mais {total_files - 10} arquivos")
        
        print()
        print("="*70)
        print("VALIDAÇÃO DOS CRITÉRIOS DE SUCESSO")
        print("="*70)
        print()
        
        # Critério 1: Lista retornada (pode ser vazia)
        criterio_1 = isinstance(python_files, list)
        print(f"✓ Critério 1 - Lista retornada: {criterio_1}")
        if not criterio_1:
            print(f"  ✗ FALHOU: Tipo retornado = {type(python_files)}")
        
        # Critério 2: Todos elementos são strings terminando em .py
        criterio_2a = all(isinstance(f, str) for f in python_files)
        criterio_2b = all(f.endswith('.py') for f in python_files) if python_files else True
        criterio_2 = criterio_2a and criterio_2b
        
        print(f"✓ Critério 2 - Todos elementos são strings: {criterio_2a}")
        print(f"✓ Critério 3 - Todos elementos terminam em .py: {criterio_2b}")
        
        if not criterio_2a and python_files:
            tipos = set(type(f).__name__ for f in python_files)
            print(f"  ✗ FALHOU: Tipos encontrados = {tipos}")
        
        if not criterio_2b and python_files:
            invalidos = [f for f in python_files if not f.endswith('.py')]
            print(f"  ✗ FALHOU: {len(invalidos)} arquivos não terminam em .py")
            for inv in invalidos[:3]:
                print(f"     - {inv}")
        
        print()
        
        # Status final
        todos_criterios = criterio_1 and criterio_2
        
        print("="*70)
        if todos_criterios:
            print("🎉 TODOS OS CRITÉRIOS DE SUCESSO ATENDIDOS!")
            print("="*70)
            print()
            print("📊 RESUMO FINAL:")
            print(f"   • Total de arquivos Python: {total_files}")
            print(f"   • Lista válida retornada: ✓")
            print(f"   • Todos elementos são strings .py: ✓")
            print(f"   • Workspace: {abs_root}")
            return 0
        else:
            print("❌ FALHA: Alguns critérios não foram atendidos")
            print("="*70)
            return 1
            
    except Exception as e:
        print(f"❌ ERRO durante execução: {e}")
        print(f"   Tipo: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
