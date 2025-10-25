"""
Módulo orquestrador de análise de arquivo Python único.

Combina todas as funções de análise (leitura, contagem de linhas, AST)
em uma única função que retorna estatísticas completas.
"""

import os
from typing import Union
from file_stats import FileStats
from file_reader import read_file_with_fallback
from line_counter import count_lines_and_comments
from ast_analyzer import analyze_ast


def analyze_single_file(filepath: str) -> FileStats:
    """
    Analisa arquivo Python único e retorna estatísticas completas.
    
    Esta função orquestra todo o processo de análise:
    1. Lê o arquivo com fallback de encoding (read_file_with_fallback)
    2. Conta linhas e comentários (count_lines_and_comments)
    3. Analisa AST para extrair funções, classes e imports (analyze_ast)
    4. Consolida tudo em objeto FileStats
    
    A função NUNCA lança exceções não tratadas - todos os erros são
    capturados e registrados no objeto FileStats retornado.
    
    Args:
        filepath: Caminho absoluto ou relativo do arquivo Python a analisar
        
    Returns:
        FileStats: Objeto contendo todas as estatísticas coletadas
        
    Comportamento de erro:
        - FileNotFoundError: Retorna FileStats com has_read_error=True
        - PermissionError: Retorna FileStats com has_read_error=True
        - SyntaxError no AST: Retorna FileStats com has_syntax_error=True
        - Qualquer outra exceção: Capturada e registrada em error_message
        
    Exemplo:
        >>> stats = analyze_single_file("example.py")
        >>> if stats.is_valid:
        ...     print(f"Funções: {stats.functions}")
        ...     print(f"Classes: {stats.classes}")
        ... else:
        ...     print(f"Erro: {stats.error_message}")
        
    Garantias:
        - SEMPRE retorna um objeto FileStats válido
        - NUNCA lança exceções não tratadas
        - Todos os campos do FileStats são preenchidos (com valores padrão se necessário)
    """
    
    # Normaliza o caminho para absoluto
    filepath = os.path.abspath(filepath)
    
    # Cria objeto FileStats base
    stats = FileStats(filepath=filepath)
    
    try:
        # PASSO 1: Leitura do arquivo com fallback de encoding
        try:
            content, encoding_used, encoding_success = read_file_with_fallback(filepath)
            stats.encoding_used = encoding_used
            stats.encoding_success = encoding_success
            
        except FileNotFoundError as e:
            stats.has_read_error = True
            stats.error_message = f"Arquivo não encontrado: {filepath}"
            return stats
            
        except PermissionError as e:
            stats.has_read_error = True
            stats.error_message = f"Permissão negada ao ler arquivo: {filepath}"
            return stats
            
        except Exception as e:
            stats.has_read_error = True
            stats.error_message = f"Erro ao ler arquivo: {type(e).__name__}: {str(e)}"
            return stats
        
        # PASSO 2: Contagem de linhas e comentários
        try:
            line_stats = count_lines_and_comments(content)
            stats.total_lines = line_stats['total_lines']
            stats.blank_lines = line_stats['blank_lines']
            stats.comment_lines = line_stats['comment_lines']
            stats.code_lines = line_stats['code_lines']
            
        except Exception as e:
            # Se falhar contagem de linhas, usa fallback simples
            stats.total_lines = len(content.split('\n'))
            stats.error_message = f"⚠️  Aviso na contagem de linhas: {str(e)}"
        
        # PASSO 3: Análise AST
        try:
            ast_stats = analyze_ast(content, filepath)
            stats.functions = ast_stats.get('functions', 0)
            stats.classes = ast_stats.get('classes', 0)
            stats.imports_list = ast_stats.get('imports_list', [])
            stats.has_syntax_error = ast_stats.get('has_syntax_error', False)
            
            # Se há erro de sintaxe, registra a mensagem
            if stats.has_syntax_error:
                stats.error_message = ast_stats.get('error_message', 'Erro de sintaxe desconhecido')
                
        except Exception as e:
            # Se análise AST falhar completamente, registra mas continua
            stats.has_syntax_error = True
            stats.error_message = f"Erro na análise AST: {type(e).__name__}: {str(e)}"
        
    except Exception as e:
        # Captura qualquer erro inesperado no nível mais alto
        stats.has_read_error = True
        stats.error_message = f"Erro inesperado: {type(e).__name__}: {str(e)}"
    
    return stats


def analyze_multiple_files(filepaths: list) -> dict:
    """
    Analisa múltiplos arquivos Python.
    
    Args:
        filepaths: Lista de caminhos de arquivos
        
    Returns:
        Dicionário mapeando filepath -> FileStats
    """
    results = {}
    
    for filepath in filepaths:
        results[filepath] = analyze_single_file(filepath)
    
    return results


def print_file_report(stats: FileStats) -> None:
    """
    Imprime relatório formatado das estatísticas de um arquivo.
    
    Args:
        stats: Objeto FileStats para imprimir
    """
    print("="*70)
    print(stats.summary)
    print("="*70)


# Testes e validação
if __name__ == "__main__":
    import tempfile
    
    print("🧪 Testando analyze_single_file...")
    print("="*70)
    
    # Teste 1: Arquivo Python válido
    print("\n📝 Teste 1: Arquivo Python válido")
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.py') as f:
        f.write("""# -*- coding: utf-8 -*-
'''Módulo de exemplo'''

import os
import sys
from pathlib import Path

class MinhaClasse:
    '''Classe de exemplo'''
    
    def __init__(self):
        self.valor = 0
    
    def metodo(self):
        return self.valor

def funcao_exemplo(x, y):
    '''Função de exemplo'''
    # Comentário interno
    return x + y

def outra_funcao():
    pass

# Fim do arquivo
""")
        test_file1 = f.name
    
    try:
        stats1 = analyze_single_file(test_file1)
        print_file_report(stats1)
        
        # Validações
        assert stats1.is_valid, "Arquivo válido deveria ter is_valid=True"
        assert stats1.functions >= 3, f"Deveria ter pelo menos 3 funções, obteve {stats1.functions}"
        assert stats1.classes >= 1, f"Deveria ter pelo menos 1 classe, obteve {stats1.classes}"
        assert len(stats1.imports_list) >= 2, f"Deveria ter pelo menos 2 imports, obteve {len(stats1.imports_list)}"
        assert stats1.total_lines > 0, "Deveria ter linhas"
        assert stats1.code_lines > 0, "Deveria ter linhas de código"
        assert not stats1.has_read_error, "Não deveria ter erro de leitura"
        assert not stats1.has_syntax_error, "Não deveria ter erro de sintaxe"
        
        print("✅ Teste 1 passou!")
        
    finally:
        os.unlink(test_file1)
    
    # Teste 2: Arquivo com erro de sintaxe
    print("\n📝 Teste 2: Arquivo com erro de sintaxe")
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.py') as f:
        f.write("""
def funcao_invalida(
    # Sintaxe inválida - parêntese não fechado
    return 42
""")
        test_file2 = f.name
    
    try:
        stats2 = analyze_single_file(test_file2)
        print_file_report(stats2)
        
        # Validações
        assert not stats2.is_valid, "Arquivo com erro deveria ter is_valid=False"
        assert stats2.has_syntax_error, "Deveria ter has_syntax_error=True"
        assert stats2.error_message, "Deveria ter mensagem de erro"
        assert not stats2.has_read_error, "Não deveria ter erro de leitura (só sintaxe)"
        assert stats2.total_lines > 0, "Deveria ter contado linhas mesmo com erro de sintaxe"
        
        print("✅ Teste 2 passou!")
        
    finally:
        os.unlink(test_file2)
    
    # Teste 3: Arquivo inexistente
    print("\n📝 Teste 3: Arquivo inexistente")
    stats3 = analyze_single_file("/caminho/totalmente/inexistente/arquivo.py")
    print_file_report(stats3)
    
    # Validações
    assert not stats3.is_valid, "Arquivo inexistente deveria ter is_valid=False"
    assert stats3.has_read_error, "Deveria ter has_read_error=True"
    assert stats3.error_message, "Deveria ter mensagem de erro"
    assert "não encontrado" in stats3.error_message.lower() or "not found" in stats3.error_message.lower(), \
        "Mensagem deveria mencionar arquivo não encontrado"
    
    print("✅ Teste 3 passou!")
    
    # Teste 4: Arquivo vazio
    print("\n📝 Teste 4: Arquivo vazio")
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.py') as f:
        f.write("")
        test_file4 = f.name
    
    try:
        stats4 = analyze_single_file(test_file4)
        print_file_report(stats4)
        
        # Validações
        assert stats4.is_valid, "Arquivo vazio é tecnicamente válido"
        assert stats4.functions == 0, "Arquivo vazio não deveria ter funções"
        assert stats4.classes == 0, "Arquivo vazio não deveria ter classes"
        assert len(stats4.imports_list) == 0, "Arquivo vazio não deveria ter imports"
        
        print("✅ Teste 4 passou!")
        
    finally:
        os.unlink(test_file4)
    
    # Teste 5: Arquivo complexo (este próprio arquivo)
    print("\n📝 Teste 5: Auto-análise (este arquivo)")
    stats5 = analyze_single_file(__file__)
    print_file_report(stats5)
    
    # Validações
    assert stats5.is_valid, "Este arquivo deveria ser válido"
    assert stats5.functions >= 3, f"Este arquivo tem pelo menos 3 funções, obteve {stats5.functions}"
    assert stats5.total_lines > 50, f"Este arquivo tem mais de 50 linhas, obteve {stats5.total_lines}"
    
    print("✅ Teste 5 passou!")
    
    # Teste 6: Múltiplos arquivos
    print("\n📝 Teste 6: Análise de múltiplos arquivos")
    
    # Cria arquivos temporários
    temp_files = []
    for i in range(3):
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.py') as f:
            f.write(f"# Arquivo {i}\ndef func_{i}():\n    pass\n")
            temp_files.append(f.name)
    
    try:
        results = analyze_multiple_files(temp_files)
        
        assert len(results) == 3, f"Deveria ter 3 resultados, obteve {len(results)}"
        
        for filepath, stats in results.items():
            print(f"\n📄 {os.path.basename(filepath)}")
            print(f"   Funções: {stats.functions}, Válido: {stats.is_valid}")
            assert stats.is_valid, f"Arquivo {filepath} deveria ser válido"
            assert stats.functions >= 1, f"Arquivo {filepath} deveria ter pelo menos 1 função"
        
        print("\n✅ Teste 6 passou!")
        
    finally:
        for temp_file in temp_files:
            os.unlink(temp_file)
    
    # VALIDAÇÃO FINAL DO CRITÉRIO DE SUCESSO
    print("\n" + "="*70)
    print("🎯 VALIDAÇÃO DO CRITÉRIO DE SUCESSO:")
    print("="*70)
    print("✅ Retorna estrutura FileStats válida com todos os campos preenchidos")
    print("✅ NUNCA lança exceção não tratada")
    print("✅ Combina read_file_with_fallback, count_lines_and_comments e analyze_ast")
    print("✅ Trata erros de arquivo inexistente")
    print("✅ Trata erros de sintaxe")
    print("✅ Trata arquivos vazios")
    print("✅ Funciona com arquivos reais")
    print("✅ Suporta análise de múltiplos arquivos")
    print("\n" + "="*70)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("✅ CRITÉRIO DE SUCESSO ATINGIDO!")
    print("="*70)
