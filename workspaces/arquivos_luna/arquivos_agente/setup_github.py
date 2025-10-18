import webbrowser
import subprocess
import time

print("=" * 70)
print("SETUP AUTOMATICO DO REPOSITORIO GITHUB - LUNA AI AGENT")
print("=" * 70)
print()

# Abrir o navegador na página de criação de repositório
print("1. Abrindo navegador no GitHub...")
webbrowser.open("https://github.com/new")
print("   -> Navegador aberto!")
print()

print("2. Por favor, faca o seguinte no navegador:")
print("   - Faca login se necessario")
print("   - Repository name: Luna")
print("   - Description: Luna AI Agent - Sistema avancado")  
print("   - Deixe como Public")
print("   - NAO marque 'Initialize with README'")
print("   - Clique em 'Create repository'")
print()

input("Pressione ENTER depois de criar o repositorio...")
print()

# Solicitar a URL do repositório
print("3. Informe a URL do repositorio criado:")
print("   Exemplo: https://github.com/seu-usuario/Luna.git")
repo_url = input("   URL: ").strip()
print()

if repo_url:
    print("4. Configurando repositorio local...")
    
    # Verificar se já existe remote origin
    result = subprocess.run(["git", "remote", "get-url", "origin"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("   Remote 'origin' ja existe. Removendo...")
        subprocess.run(["git", "remote", "remove", "origin"])
    
    # Adicionar novo remote
    subprocess.run(["git", "remote", "add", "origin", repo_url])
    print(f"   -> Remote adicionado: {repo_url}")
    
    # Renomear branch para main
    subprocess.run(["git", "branch", "-M", "main"])
    print("   -> Branch renomeado para 'main'")
    
    # Push para GitHub
    print("\n5. Enviando codigo para GitHub...")
    result = subprocess.run(["git", "push", "-u", "origin", "main"])
    
    if result.returncode == 0:
        print("\n" + "=" * 70)
        print("SUCESSO! Repositorio criado e codigo enviado!")
        print("=" * 70)
        print(f"\nAcesse seu repositorio em: {repo_url.replace('.git', '')}")
    else:
        print("\nErro ao fazer push. Tente manualmente:")
        print("git push -u origin main")
else:
    print("URL nao fornecida. Execute manualmente:")
    print("git remote add origin URL_DO_REPOSITORIO")
    print("git branch -M main")
    print("git push -u origin main")
