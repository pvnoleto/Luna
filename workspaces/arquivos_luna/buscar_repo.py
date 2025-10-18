import subprocess
import re

# Tenta descobrir repos do GitHub via comandos git
try:
    # Verifica se há alguma configuração de remote nos logs
    result = subprocess.run(['git', 'log', '--all', '--decorate', '--oneline'], 
                          capture_output=True, text=True, timeout=10)
    print("Git log output:")
    print(result.stdout)
    print(result.stderr)
except Exception as e:
    print(f"Erro: {e}")

# Verifica arquivos de configuração
try:
    with open('.git/config', 'r', encoding='utf-8') as f:
        print("\nConteúdo .git/config:")
        print(f.read())
except Exception as e:
    print(f"Erro ao ler .git/config: {e}")
