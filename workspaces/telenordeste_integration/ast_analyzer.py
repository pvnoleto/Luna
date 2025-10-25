"""
Módulo para análise AST de código Python.

Este módulo implementa análise de Abstract Syntax Tree (AST) para extrair
estatísticas e informações estruturais de arquivos Python, incluindo:
- Contagem de funções e classes
- Análise de imports
- Tratamento robusto de erros de sintaxe
"""

import ast
from typing import Dict, List, Any
from dataclasses import dataclass, field


@dataclass
class CodeStatistics:
    """
    Estrutura de dados para armazenar estatísticas de código Python.
    
    Attributes:
        functions: Número total de funções definidas
        classes: Número total de classes definidas
        imports_list: Lista de módulos importados
        has_syntax_error: Flag indicando erro de sintaxe
        error_message: Mensagem de erro (se houver)
        lines_of_code: Número total de linhas (opcional)
    """
    functions: int = 0
    classes: int = 0
    imports_list: List[str] = field(default_factory=list)
    has_syntax_error: bool = False
    error_message: str = ""
    lines_of_code: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte a estrutura para dicionário."""
        return {
            'functions': self.functions,
            'classes': self.classes,
            'imports_list': self.imports_list,
            'has_syntax_error': self.has_syntax_error,
            'error_message': self.error_message,
            'lines_of_code': self.lines_of_code
        }


class ASTAnalyzer(ast.NodeVisitor):
    """
    Analisador AST para extração de métricas de código Python.
    
    Utiliza o padrão Visitor para percorrer a árvore AST e coletar
    informações sobre funções, classes e imports.
    
    Attributes:
        functions: Contador de funções
        classes: Contador de classes
        imports_list: Lista de módulos importados
    """
    
    def __init__(self):
        """Inicializa contadores e listas."""
        self.functions = 0
        self.classes = 0
        self.imports_list: List[str] = []
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        Visita nó de definição de função.
        
        Args:
            node: Nó AST representando uma definição de função
        """
        self.functions += 1
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """
        Visita nó de definição de função assíncrona.
        
        Args:
            node: Nó AST representando uma definição de função async
        """
        self.functions += 1
        self.generic_visit(node)
    
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Visita nó de definição de classe.
        
        Args:
            node: Nó AST representando uma definição de classe
        """
        self.classes += 1
        self.generic_visit(node)
    
    def visit_Import(self, node: ast.Import) -> None:
        """
        Visita nó de import simples (import x).
        
        Args:
            node: Nó AST representando um import
        """
        for alias in node.names:
            self.imports_list.append(alias.name)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """
        Visita nó de import from (from x import y).
        
        Args:
            node: Nó AST representando um import from
        """
        if node.module:
            self.imports_list.append(node.module)
        self.generic_visit(node)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Retorna as estatísticas coletadas como dicionário.
        
        Returns:
            Dicionário com contadores de functions, classes e imports_list
        """
        return {
            'functions': self.functions,
            'classes': self.classes,
            'imports_list': self.imports_list,
            'has_syntax_error': False,
            'error_message': ''
        }


def analyze_ast(content: str, filepath: str) -> Dict[str, Any]:
    """
    Analisa código Python usando AST com tratamento robusto de erros.
    
    Faz parse do conteúdo usando ast.parse dentro de try-except para capturar
    erros de sintaxe. Se o parse for bem-sucedido, cria uma instância de
    ASTAnalyzer e percorre a árvore para coletar estatísticas.
    
    Args:
        content: Conteúdo do arquivo Python como string
        filepath: Caminho do arquivo para contexto de erro
        
    Returns:
        Dicionário contendo:
        - functions (int): Número de funções
        - classes (int): Número de classes
        - imports_list (list): Lista de imports
        - has_syntax_error (bool): True se houver erro de sintaxe
        - error_message (str): Mensagem de erro detalhada (se houver)
        
    Exemplo:
        >>> code = '''
        ... import os
        ... class MyClass:
        ...     pass
        ... def my_function():
        ...     pass
        ... '''
        >>> result = analyze_ast(code, 'example.py')
        >>> print(result['functions'])
        1
        >>> print(result['classes'])
        1
        >>> print('os' in result['imports_list'])
        True
        >>> print(result['has_syntax_error'])
        False
        
        >>> bad_code = 'def broken('
        >>> result = analyze_ast(bad_code, 'broken.py')
        >>> print(result['has_syntax_error'])
        True
        >>> print('SyntaxError' in result['error_message'])
        True
    """
    try:
        # Tenta fazer parse do conteúdo
        tree = ast.parse(content, filename=filepath)
        
        # Cria instância do analisador
        analyzer = ASTAnalyzer()
        
        # Percorre a árvore AST
        analyzer.visit(tree)
        
        # Retorna estatísticas coletadas
        return analyzer.get_statistics()
        
    except SyntaxError as e:
        # Captura erros de sintaxe e retorna informações detalhadas
        return {
            'functions': 0,
            'classes': 0,
            'imports_list': [],
            'has_syntax_error': True,
            'error_message': f"SyntaxError no arquivo '{filepath}' linha {e.lineno}: {e.msg}"
        }
    
    except Exception as e:
        # Captura outros erros inesperados
        return {
            'functions': 0,
            'classes': 0,
            'imports_list': [],
            'has_syntax_error': True,
            'error_message': f"Erro ao analisar '{filepath}': {type(e).__name__}: {str(e)}"
        }


# Testes e validação
if __name__ == "__main__":
    print("=" * 70)
    print("TESTE 1: Código Python válido")
    print("=" * 70)
    
    valid_code = """
import os
import sys
from typing import List

class MinhaClasse:
    def __init__(self):
        pass
    
    def metodo1(self):
        pass

def funcao_global():
    pass

async def funcao_async():
    pass
"""
    
    result1 = analyze_ast(valid_code, "test_valid.py")
    print(f"✓ Functions: {result1['functions']} (esperado: 4)")
    print(f"✓ Classes: {result1['classes']} (esperado: 1)")
    print(f"✓ Imports: {result1['imports_list']} (esperado: ['os', 'sys', 'typing'])")
    print(f"✓ Has syntax error: {result1['has_syntax_error']} (esperado: False)")
    print(f"✓ Error message: '{result1['error_message']}' (esperado: '')")
    
    assert result1['functions'] == 4, f"Esperado 4 funções, obteve {result1['functions']}"
    assert result1['classes'] == 1, f"Esperado 1 classe, obteve {result1['classes']}"
    assert 'os' in result1['imports_list'], "Import 'os' não encontrado"
    assert 'sys' in result1['imports_list'], "Import 'sys' não encontrado"
    assert 'typing' in result1['imports_list'], "Import 'typing' não encontrado"
    assert result1['has_syntax_error'] == False, "Não deveria ter erro de sintaxe"
    assert result1['error_message'] == '', "Mensagem de erro deveria estar vazia"
    
    print("\n✅ TESTE 1 PASSOU - Código válido analisado corretamente!\n")
    
    print("=" * 70)
    print("TESTE 2: Código com erro de sintaxe")
    print("=" * 70)
    
    invalid_code = """
def funcao_quebrada(
    print("faltou fechar parenteses")
"""
    
    result2 = analyze_ast(invalid_code, "test_invalid.py")
    print(f"✓ Functions: {result2['functions']} (esperado: 0)")
    print(f"✓ Classes: {result2['classes']} (esperado: 0)")
    print(f"✓ Imports: {result2['imports_list']} (esperado: [])")
    print(f"✓ Has syntax error: {result2['has_syntax_error']} (esperado: True)")
    print(f"✓ Error message: '{result2['error_message']}'")
    
    assert result2['functions'] == 0, f"Esperado 0 funções em código inválido"
    assert result2['classes'] == 0, f"Esperado 0 classes em código inválido"
    assert result2['imports_list'] == [], f"Esperado lista vazia de imports"
    assert result2['has_syntax_error'] == True, "Deveria detectar erro de sintaxe"
    assert 'SyntaxError' in result2['error_message'], "Mensagem deveria conter 'SyntaxError'"
    assert 'test_invalid.py' in result2['error_message'], "Mensagem deveria conter nome do arquivo"
    
    print("\n✅ TESTE 2 PASSOU - Erro de sintaxe detectado corretamente!\n")
    
    print("=" * 70)
    print("TESTE 3: Código vazio")
    print("=" * 70)
    
    empty_code = ""
    
    result3 = analyze_ast(empty_code, "test_empty.py")
    print(f"✓ Functions: {result3['functions']} (esperado: 0)")
    print(f"✓ Classes: {result3['classes']} (esperado: 0)")
    print(f"✓ Imports: {result3['imports_list']} (esperado: [])")
    print(f"✓ Has syntax error: {result3['has_syntax_error']} (esperado: False)")
    
    assert result3['functions'] == 0, f"Esperado 0 funções em código vazio"
    assert result3['classes'] == 0, f"Esperado 0 classes em código vazio"
    assert result3['imports_list'] == [], f"Esperado lista vazia de imports"
    assert result3['has_syntax_error'] == False, "Código vazio não é erro de sintaxe"
    
    print("\n✅ TESTE 3 PASSOU - Código vazio tratado corretamente!\n")
    
    print("=" * 70)
    print("VALIDAÇÃO DOS CRITÉRIOS DE SUCESSO")
    print("=" * 70)
    print("✅ Retorna contadores válidos para código correto")
    print("✅ Retorna has_syntax_error=True com mensagem para código inválido")
    print("✅ Tratamento de erros robusto com try-except")
    print("✅ Contexto de filepath incluído nas mensagens de erro")
    print("✅ Coleta functions, classes e imports_list corretamente")
    print("\n🎉 TODOS OS TESTES PASSARAM - SUBTAREFA 2.3 CONCLUÍDA COM SUCESSO!")
