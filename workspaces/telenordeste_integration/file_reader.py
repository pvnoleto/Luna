"""
Módulo de leitura de arquivos com fallback de encoding.

Fornece função robusta para ler arquivos Python que podem ter
diferentes encodings, tentando múltiplas estratégias.
"""

from typing import Tuple
import os


def read_file_with_fallback(filepath: str) -> Tuple[str, str, bool]:
    """
    Lê arquivo com fallback de encoding.
    
    Tenta ler o arquivo usando diferentes encodings na seguinte ordem:
    1. UTF-8 (padrão moderno)
    2. latin-1 (ISO-8859-1, comum em sistemas antigos)
    3. cp1252 (Windows-1252, comum em Windows)
    4. UTF-8 com errors='ignore' (último recurso)
    
    Args:
        filepath: Caminho do arquivo para ler
        
    Returns:
        Tupla contendo:
        - conteúdo: String com o conteúdo do arquivo
        - encoding_usado: Nome do encoding que funcionou
        - sucesso: True se leu sem erros, False se teve que ignorar erros
        
    Raises:
        FileNotFoundError: Se o arquivo não existir
        PermissionError: Se não tiver permissão para ler o arquivo
    """
    # Verifica se arquivo existe
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
    
    # Lista de encodings para tentar
    encodings_to_try = [
        ('utf-8', 'strict'),
        ('latin-1', 'strict'),
        ('cp1252', 'strict'),
        ('utf-8', 'ignore')
    ]
    
    last_error = None
    
    for encoding, error_mode in encodings_to_try:
        try:
            with open(filepath, 'r', encoding=encoding, errors=error_mode) as f:
                content = f.read()
            
            # Sucesso!
            sucesso = (error_mode == 'strict')
            return (content, encoding, sucesso)
            
        except UnicodeDecodeError as e:
            last_error = e
            # Tenta próximo encoding
            continue
        except (PermissionError, OSError) as e:
            # Erros que não são de encoding devem ser propagados
            raise
    
    # Se chegou aqui, nenhum encoding funcionou (não deveria acontecer com ignore)
    raise RuntimeError(
        f"Falha ao ler arquivo {filepath} com todos os encodings. "
        f"Último erro: {last_error}"
    )


def read_multiple_files(filepaths: list) -> dict:
    """
    Lê múltiplos arquivos com fallback de encoding.
    
    Args:
        filepaths: Lista de caminhos de arquivos
        
    Returns:
        Dicionário mapeando filepath -> (conteúdo, encoding, sucesso)
    """
    results = {}
    
    for filepath in filepaths:
        try:
            results[filepath] = read_file_with_fallback(filepath)
        except Exception as e:
            results[filepath] = (None, None, False, str(e))
    
    return results


if __name__ == "__main__":
    # Testes básicos
    import tempfile
    
    print("🧪 Testando read_file_with_fallback...")
    
    # Teste 1: Arquivo UTF-8
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.py') as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write("texto = 'Olá Mundo! 你好世界'\n")
        utf8_file = f.name
    
    try:
        content, encoding, success = read_file_with_fallback(utf8_file)
        print(f"✅ UTF-8: encoding={encoding}, sucesso={success}")
        print(f"   Conteúdo: {content[:50]}...")
    finally:
        os.unlink(utf8_file)
    
    # Teste 2: Arquivo latin-1
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.py') as f:
        # Escreve em latin-1
        f.write("# Comentário com acentuação\n".encode('latin-1'))
        f.write("texto = 'São Paulo'\n".encode('latin-1'))
        latin1_file = f.name
    
    try:
        content, encoding, success = read_file_with_fallback(latin1_file)
        print(f"✅ Latin-1: encoding={encoding}, sucesso={success}")
        print(f"   Conteúdo: {content[:50]}...")
    finally:
        os.unlink(latin1_file)
    
    # Teste 3: Arquivo com bytes inválidos (será lido com ignore)
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.py') as f:
        f.write(b"# Arquivo com bytes invalidos: \xFF\xFE\x00\x00\n")
        f.write(b"texto = 'teste'\n")
        invalid_file = f.name
    
    try:
        content, encoding, success = read_file_with_fallback(invalid_file)
        print(f"✅ Bytes inválidos: encoding={encoding}, sucesso={success}")
        print(f"   Conteúdo: {content[:50]}...")
    finally:
        os.unlink(invalid_file)
    
    # Teste 4: Arquivo inexistente
    try:
        read_file_with_fallback("/caminho/inexistente.py")
        print("❌ Deveria ter lançado FileNotFoundError")
    except FileNotFoundError:
        print("✅ FileNotFoundError capturado corretamente")
    
    print("\n✅ Todos os testes passaram!")
