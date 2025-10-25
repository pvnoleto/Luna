"""
Módulo de estrutura de dados para estatísticas de arquivos Python.

Define a estrutura FileStats que consolida todas as métricas coletadas
durante a análise de um arquivo Python.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class FileStats:
    """
    Estrutura completa de estatísticas de arquivo Python.
    
    Consolida todas as métricas coletadas de um arquivo:
    - Informações básicas do arquivo
    - Métricas de linhas (total, branco, comentários, código)
    - Métricas AST (funções, classes, imports)
    - Informações de encoding e erros
    
    Attributes:
        filepath: Caminho completo do arquivo analisado
        
        # Métricas de linhas
        total_lines: Total de linhas no arquivo
        blank_lines: Linhas em branco
        comment_lines: Linhas de comentário
        code_lines: Linhas de código
        
        # Métricas AST
        functions: Número de funções definidas
        classes: Número de classes definidas
        imports_list: Lista de módulos importados
        
        # Informações técnicas
        encoding_used: Encoding usado para ler o arquivo
        encoding_success: True se leitura foi sem erros
        
        # Tratamento de erros
        has_syntax_error: True se há erro de sintaxe
        has_read_error: True se houve erro ao ler arquivo
        error_message: Mensagem de erro detalhada (se houver)
        
    Exemplo:
        >>> stats = FileStats(
        ...     filepath="/path/to/file.py",
        ...     total_lines=100,
        ...     code_lines=80,
        ...     functions=5,
        ...     classes=2
        ... )
        >>> print(stats.filepath)
        /path/to/file.py
    """
    
    # Informações básicas
    filepath: str
    
    # Métricas de linhas
    total_lines: int = 0
    blank_lines: int = 0
    comment_lines: int = 0
    code_lines: int = 0
    
    # Métricas AST
    functions: int = 0
    classes: int = 0
    imports_list: List[str] = field(default_factory=list)
    
    # Informações técnicas
    encoding_used: str = "utf-8"
    encoding_success: bool = True
    
    # Tratamento de erros
    has_syntax_error: bool = False
    has_read_error: bool = False
    error_message: str = ""
    
    def to_dict(self) -> dict:
        """
        Converte FileStats para dicionário.
        
        Returns:
            Dicionário com todos os campos da estrutura
        """
        return {
            'filepath': self.filepath,
            'total_lines': self.total_lines,
            'blank_lines': self.blank_lines,
            'comment_lines': self.comment_lines,
            'code_lines': self.code_lines,
            'functions': self.functions,
            'classes': self.classes,
            'imports_list': self.imports_list,
            'encoding_used': self.encoding_used,
            'encoding_success': self.encoding_success,
            'has_syntax_error': self.has_syntax_error,
            'has_read_error': self.has_read_error,
            'error_message': self.error_message
        }
    
    @property
    def is_valid(self) -> bool:
        """
        Verifica se as estatísticas são válidas (sem erros críticos).
        
        Returns:
            True se não há erros de leitura ou sintaxe
        """
        return not self.has_read_error and not self.has_syntax_error
    
    @property
    def summary(self) -> str:
        """
        Retorna resumo formatado das estatísticas.
        
        Returns:
            String com resumo das principais métricas
        """
        if self.has_read_error:
            return f"❌ Erro ao ler arquivo: {self.error_message}"
        
        if self.has_syntax_error:
            return f"⚠️  Erro de sintaxe: {self.error_message}"
        
        return (
            f"📄 {self.filepath}\n"
            f"   Linhas: {self.total_lines} total "
            f"({self.code_lines} código, {self.comment_lines} comentários, "
            f"{self.blank_lines} branco)\n"
            f"   Estrutura: {self.functions} funções, {self.classes} classes\n"
            f"   Imports: {len(self.imports_list)} módulos\n"
            f"   Encoding: {self.encoding_used} "
            f"({'✓' if self.encoding_success else '⚠️ com erros'})"
        )
    
    def __str__(self) -> str:
        """Representação em string usando summary."""
        return self.summary


# Testes básicos
if __name__ == "__main__":
    print("🧪 Testando FileStats...")
    print("="*60)
    
    # Teste 1: Arquivo válido
    stats1 = FileStats(
        filepath="/path/to/example.py",
        total_lines=100,
        blank_lines=20,
        comment_lines=15,
        code_lines=65,
        functions=5,
        classes=2,
        imports_list=["os", "sys", "pathlib"],
        encoding_used="utf-8",
        encoding_success=True
    )
    
    print("\n📝 Teste 1: Arquivo válido")
    print(stats1.summary)
    print(f"✓ is_valid: {stats1.is_valid}")
    assert stats1.is_valid, "Arquivo válido deveria ter is_valid=True"
    assert len(stats1.imports_list) == 3, "Deveria ter 3 imports"
    print("✅ Teste 1 passou!")
    
    # Teste 2: Arquivo com erro de sintaxe
    stats2 = FileStats(
        filepath="/path/to/invalid.py",
        total_lines=50,
        code_lines=40,
        has_syntax_error=True,
        error_message="SyntaxError: invalid syntax at line 10"
    )
    
    print("\n📝 Teste 2: Erro de sintaxe")
    print(stats2.summary)
    print(f"✓ is_valid: {stats2.is_valid}")
    assert not stats2.is_valid, "Arquivo com erro deveria ter is_valid=False"
    print("✅ Teste 2 passou!")
    
    # Teste 3: Arquivo com erro de leitura
    stats3 = FileStats(
        filepath="/path/nonexistent.py",
        has_read_error=True,
        error_message="FileNotFoundError: File not found"
    )
    
    print("\n📝 Teste 3: Erro de leitura")
    print(stats3.summary)
    print(f"✓ is_valid: {stats3.is_valid}")
    assert not stats3.is_valid, "Arquivo com erro de leitura deveria ter is_valid=False"
    print("✅ Teste 3 passou!")
    
    # Teste 4: Conversão para dicionário
    stats4 = FileStats(
        filepath="/test.py",
        total_lines=10,
        functions=1
    )
    
    print("\n📝 Teste 4: Conversão para dicionário")
    dict_result = stats4.to_dict()
    print(f"✓ Dict keys: {list(dict_result.keys())}")
    assert 'filepath' in dict_result, "Deveria ter campo filepath"
    assert 'total_lines' in dict_result, "Deveria ter campo total_lines"
    assert dict_result['total_lines'] == 10, "total_lines deveria ser 10"
    assert dict_result['functions'] == 1, "functions deveria ser 1"
    print("✅ Teste 4 passou!")
    
    print("\n" + "="*60)
    print("✅ Todos os testes de FileStats passaram!")
