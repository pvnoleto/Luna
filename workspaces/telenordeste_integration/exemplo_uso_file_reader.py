"""
Exemplo de uso da função read_file_with_fallback.

Demonstra como usar a função em cenários reais.
"""

from file_reader import read_file_with_fallback, read_multiple_files
import os


def exemplo_basico():
    """Exemplo básico de leitura de um arquivo."""
    print("📖 Exemplo 1: Leitura básica")
    print("-" * 60)
    
    # Tenta ler este próprio arquivo
    filepath = __file__
    
    content, encoding, success = read_file_with_fallback(filepath)
    
    print(f"Arquivo: {os.path.basename(filepath)}")
    print(f"Encoding detectado: {encoding}")
    print(f"Leitura com sucesso: {success}")
    print(f"Tamanho do conteúdo: {len(content)} caracteres")
    print(f"Primeiras linhas:\n{content[:200]}...\n")


def exemplo_tratamento_erro():
    """Exemplo de tratamento de erros."""
    print("📖 Exemplo 2: Tratamento de erros")
    print("-" * 60)
    
    filepath = "arquivo_inexistente.py"
    
    try:
        content, encoding, success = read_file_with_fallback(filepath)
        print(f"Conteúdo lido com sucesso!")
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {filepath}")
        print("✅ Erro tratado corretamente!\n")


def exemplo_multiplos_arquivos():
    """Exemplo de leitura de múltiplos arquivos."""
    print("📖 Exemplo 3: Leitura de múltiplos arquivos")
    print("-" * 60)
    
    # Lista arquivos Python no diretório atual
    arquivos = [f for f in os.listdir('.') if f.endswith('.py')][:3]
    
    if not arquivos:
        print("Nenhum arquivo Python encontrado no diretório atual.\n")
        return
    
    results = read_multiple_files(arquivos)
    
    for filepath, result in results.items():
        if len(result) == 3:
            content, encoding, success = result
            print(f"✅ {filepath}")
            print(f"   Encoding: {encoding}, Sucesso: {success}")
            print(f"   Tamanho: {len(content)} caracteres")
        else:
            print(f"❌ {filepath}: {result[3]}")
    
    print()


def exemplo_verificacao_encoding():
    """Exemplo de verificação de encoding de arquivos."""
    print("📖 Exemplo 4: Análise de encoding")
    print("-" * 60)
    
    arquivos = [f for f in os.listdir('.') if f.endswith('.py')]
    
    if not arquivos:
        print("Nenhum arquivo Python encontrado.\n")
        return
    
    encodings_count = {}
    
    for filepath in arquivos:
        try:
            _, encoding, success = read_file_with_fallback(filepath)
            encodings_count[encoding] = encodings_count.get(encoding, 0) + 1
        except Exception:
            pass
    
    print("Distribuição de encodings:")
    for encoding, count in sorted(encodings_count.items(), key=lambda x: x[1], reverse=True):
        print(f"  {encoding}: {count} arquivo(s)")
    
    print()


def exemplo_validacao_conteudo():
    """Exemplo de validação de conteúdo lido."""
    print("📖 Exemplo 5: Validação de conteúdo")
    print("-" * 60)
    
    filepath = __file__
    content, encoding, success = read_file_with_fallback(filepath)
    
    # Validações
    print(f"✓ Conteúdo é string: {isinstance(content, str)}")
    print(f"✓ Conteúdo não está vazio: {len(content) > 0}")
    print(f"✓ Encoding é válido: {encoding in ['utf-8', 'latin-1', 'cp1252']}")
    print(f"✓ Success é booleano: {isinstance(success, bool)}")
    
    # Verifica se é Python válido
    linhas_codigo = [l for l in content.split('\n') if l.strip() and not l.strip().startswith('#')]
    print(f"✓ Linhas de código: {len(linhas_codigo)}")
    
    print()


if __name__ == "__main__":
    print("🚀 EXEMPLOS DE USO: read_file_with_fallback")
    print("=" * 60)
    print()
    
    exemplo_basico()
    exemplo_tratamento_erro()
    exemplo_multiplos_arquivos()
    exemplo_verificacao_encoding()
    exemplo_validacao_conteudo()
    
    print("=" * 60)
    print("✅ Todos os exemplos executados com sucesso!")
    print()
    print("💡 DICA: Use read_file_with_fallback() sempre que precisar ler")
    print("   arquivos Python de origem desconhecida ou legados.")
