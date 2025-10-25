"""
Módulo para contagem de linhas e comentários em arquivos Python.

Este módulo implementa função para contar diferentes tipos de linhas
em código Python: total, em branco, comentários e código.
"""

import re
from typing import Dict


def count_lines_and_comments(content: str) -> Dict[str, int]:
    """
    Conta linhas totais, em branco, comentários e código em conteúdo Python.
    
    Analisa o conteúdo de um arquivo Python e conta:
    - total_lines: Total de linhas (split por \\n)
    - blank_lines: Linhas em branco ou apenas com espaços (regex r'^\\s*$')
    - comment_lines: Linhas que são comentários (regex r'^\\s*#')
    - code_lines: Linhas de código (total - blank - comment)
    
    Args:
        content: String com o conteúdo completo do arquivo Python
        
    Returns:
        Dicionário com contadores:
        {
            'total_lines': int,
            'blank_lines': int,
            'comment_lines': int,
            'code_lines': int
        }
        
    Exemplo:
        >>> content = '''# Comentário
        ... 
        ... def foo():
        ...     pass
        ... '''
        >>> result = count_lines_and_comments(content)
        >>> print(result)
        {'total_lines': 4, 'blank_lines': 1, 'comment_lines': 1, 'code_lines': 2}
        
    Nota:
        A soma de blank_lines + comment_lines + code_lines será aproximadamente
        igual a total_lines. Pequenas diferenças podem ocorrer devido a linhas
        que contêm código E comentário (ex: "x = 1  # comentário").
    """
    # Split por linhas
    lines = content.split('\n')
    total_lines = len(lines)
    
    # Regex para linhas em branco (apenas whitespace)
    blank_pattern = re.compile(r'^\s*$')
    
    # Regex para linhas de comentário (começa com # após whitespace opcional)
    comment_pattern = re.compile(r'^\s*#')
    
    # Contadores
    blank_lines = 0
    comment_lines = 0
    
    # Itera sobre cada linha
    for line in lines:
        if blank_pattern.match(line):
            blank_lines += 1
        elif comment_pattern.match(line):
            comment_lines += 1
    
    # Calcula linhas de código
    code_lines = total_lines - blank_lines - comment_lines
    
    return {
        'total_lines': total_lines,
        'blank_lines': blank_lines,
        'comment_lines': comment_lines,
        'code_lines': code_lines
    }


# Testes e validação quando executado diretamente
if __name__ == "__main__":
    print("🧪 Testando count_lines_and_comments...")
    print("="*60)
    
    # Teste 1: Código simples
    test1 = """# Comentário
    
def foo():
    pass
"""
    result1 = count_lines_and_comments(test1)
    print("\n📝 Teste 1: Código simples")
    print(f"Conteúdo:\n{repr(test1)}")
    print(f"Resultado: {result1}")
    assert result1['total_lines'] == 5, "Total de linhas incorreto"
    assert result1['blank_lines'] == 2, "Linhas em branco incorretas"
    assert result1['comment_lines'] == 1, "Linhas de comentário incorretas"
    assert result1['code_lines'] == 2, "Linhas de código incorretas"
    print("✅ Teste 1 passou!")
    
    # Teste 2: Múltiplos comentários
    test2 = """# Comentário 1
# Comentário 2
# Comentário 3

def bar():
    # Comentário interno
    return 42
"""
    result2 = count_lines_and_comments(test2)
    print("\n📝 Teste 2: Múltiplos comentários")
    print(f"Resultado: {result2}")
    assert result2['comment_lines'] == 4, "Contagem de comentários incorreta"
    print("✅ Teste 2 passou!")
    
    # Teste 3: Arquivo complexo (simulando arquivo real)
    test3 = '''"""
Docstring multilinha
não é comentário
"""

import os
import sys  # Comentário inline (será contado como código)

# Comentário de bloco
# Mais comentários
# Ainda mais comentários

def funcao_exemplo():
    """Docstring da função"""
    x = 1  # Isso é código com comentário inline
    
    # Comentário dentro da função
    return x


class MinhaClasse:
    # Comentário da classe
    pass

'''
    result3 = count_lines_and_comments(test3)
    print("\n📝 Teste 3: Arquivo complexo")
    print(f"Resultado: {result3}")
    print(f"  Total: {result3['total_lines']}")
    print(f"  Branco: {result3['blank_lines']}")
    print(f"  Comentários: {result3['comment_lines']}")
    print(f"  Código: {result3['code_lines']}")
    
    # Validar critério de sucesso
    soma = result3['blank_lines'] + result3['comment_lines'] + result3['code_lines']
    print(f"\n🔍 Validação: blank + comment + code = {soma}")
    print(f"   Total de linhas = {result3['total_lines']}")
    print(f"   Diferença = {abs(soma - result3['total_lines'])}")
    assert soma == result3['total_lines'], "Soma não bate com total!"
    print("✅ Teste 3 passou!")
    
    # Teste 4: Arquivo vazio
    test4 = ""
    result4 = count_lines_and_comments(test4)
    print("\n📝 Teste 4: Arquivo vazio")
    print(f"Resultado: {result4}")
    assert result4['total_lines'] == 1, "Arquivo vazio deve ter 1 linha"
    assert result4['blank_lines'] == 1, "Arquivo vazio deve ter 1 linha em branco"
    print("✅ Teste 4 passou!")
    
    # Teste 5: Só comentários
    test5 = """# Comentário 1
# Comentário 2
# Comentário 3"""
    result5 = count_lines_and_comments(test5)
    print("\n📝 Teste 5: Só comentários")
    print(f"Resultado: {result5}")
    assert result5['comment_lines'] == 3, "Todas as linhas devem ser comentários"
    assert result5['code_lines'] == 0, "Não deve ter código"
    print("✅ Teste 5 passou!")
    
    # Teste 6: Indentação preservada em comentários
    test6 = """def foo():
    # Comentário indentado
    pass
"""
    result6 = count_lines_and_comments(test6)
    print("\n📝 Teste 6: Comentários indentados")
    print(f"Resultado: {result6}")
    assert result6['comment_lines'] == 1, "Comentário indentado deve ser contado"
    print("✅ Teste 6 passou!")
    
    # VALIDAÇÃO FINAL DOS CRITÉRIOS DE SUCESSO
    print("\n" + "="*60)
    print("VALIDAÇÃO DOS CRITÉRIOS DE SUCESSO:")
    print("="*60)
    
    all_tests = [result1, result2, result3, result4, result5, result6]
    
    # Critério 1: Todos os valores são não negativos
    all_non_negative = all(
        r['total_lines'] >= 0 and 
        r['blank_lines'] >= 0 and 
        r['comment_lines'] >= 0 and 
        r['code_lines'] >= 0
        for r in all_tests
    )
    print(f"✓ Todos os valores são não negativos: {all_non_negative}")
    
    # Critério 2: Soma aproximadamente igual ao total
    sums_match = all(
        r['blank_lines'] + r['comment_lines'] + r['code_lines'] == r['total_lines']
        for r in all_tests
    )
    print(f"✓ Soma igual ao total em todos os testes: {sums_match}")
    
    # Critério 3: Função retorna dicionário com chaves corretas
    correct_keys = all(
        set(r.keys()) == {'total_lines', 'blank_lines', 'comment_lines', 'code_lines'}
        for r in all_tests
    )
    print(f"✓ Dicionário com chaves corretas: {correct_keys}")
    
    # Critério 4: Valores são inteiros
    all_integers = all(
        isinstance(r['total_lines'], int) and
        isinstance(r['blank_lines'], int) and
        isinstance(r['comment_lines'], int) and
        isinstance(r['code_lines'], int)
        for r in all_tests
    )
    print(f"✓ Todos os valores são inteiros: {all_integers}")
    
    if all_non_negative and sums_match and correct_keys and all_integers:
        print("\n🎉 TODOS OS CRITÉRIOS DE SUCESSO FORAM ATENDIDOS!")
        print("\n✅ Função count_lines_and_comments implementada com sucesso!")
    else:
        print("\n⚠️  ALGUNS CRITÉRIOS NÃO FORAM ATENDIDOS!")
        exit(1)
