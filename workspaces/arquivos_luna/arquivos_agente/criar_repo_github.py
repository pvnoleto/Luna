import requests
import json
import sys
import subprocess

def criar_repositorio_github(username, password, repo_name, description=""):
    """Cria um repositorio no GitHub usando a API"""
    
    # URL da API do GitHub
    url = "https://api.github.com/user/repos"
    
    # Dados do repositorio
    data = {
        "name": repo_name,
        "description": description,
        "private": False,
        "auto_init": False
    }
    
    # Fazer requisicao
    response = requests.post(
        url,
        auth=(username, password),
        json=data,
        headers={"Accept": "application/vnd.github.v3+json"}
    )
    
    if response.status_code == 201:
        repo_info = response.json()
        print("SUCESSO: Repositorio criado!")
        print(f"URL: {repo_info['html_url']}")
        print(f"Clone URL: {repo_info['clone_url']}")
        return repo_info
    else:
        print(f"ERRO ao criar repositorio: {response.status_code}")
        print(f"Resposta: {response.text}")
        return None

if __name__ == "__main__":
    username = "pvnoleto@gmail.com"
    password = "quize180994"
    repo_name = "Luna"
    description = "Luna AI Agent - Sistema avancado com memoria permanente, cofre de credenciais, auto-evolucao e capacidades de Computer Use"
    
    resultado = criar_repositorio_github(username, password, repo_name, description)
    
    if resultado:
        # Adicionar remote ao git local
        clone_url = resultado['clone_url']
        subprocess.run(["git", "remote", "add", "origin", clone_url])
        subprocess.run(["git", "branch", "-M", "main"])
        print("\nRemote adicionado ao repositorio local!")
