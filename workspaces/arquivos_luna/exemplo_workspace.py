#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📋 EXEMPLO DE USO - GERENCIADOR DE WORKSPACES
==============================================

Demonstra todas as funcionalidades do workspace manager

"""

from gerenciador_workspaces import GerenciadorWorkspaces
import time


def separador(titulo: str = ""):
    """Imprime separador visual"""
    print("\n" + "="*70)
    if titulo:
        print(f"  {titulo}")
        print("="*70)
    print()


def exemplo_basico():
    """Exemplo básico de uso"""
    separador("🎯 EXEMPLO BÁSICO")
    
    # Inicializar gerenciador
    gw = GerenciadorWorkspaces()
    
    print("1️⃣ Criando workspaces...")
    sucesso, msg = gw.criar_workspace("projeto_web", "Site pessoal com Flask")
    print(f"   {msg}")
    
    sucesso, msg = gw.criar_workspace("bot_telegram", "Bot para automação")
    print(f"   {msg}")
    
    sucesso, msg = gw.criar_workspace("analise_dados", "Análise de dados CSV")
    print(f"   {msg}")
    
    print("\n2️⃣ Listando workspaces...")
    gw.exibir_status()
    
    print("3️⃣ Selecionando workspace 'projeto_web'...")
    sucesso, msg = gw.selecionar_workspace("projeto_web")
    print(f"   {msg}")
    
    print("\n4️⃣ Criando arquivos no workspace...")
    sucesso, msg, path = gw.criar_arquivo(
        "app.py",
        """# Flask App
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello Luna!'

if __name__ == '__main__':
    app.run(debug=True)
"""
    )
    print(f"   {msg}")
    print(f"   📍 {path}")
    
    sucesso, msg, path = gw.criar_arquivo(
        "requirements.txt",
        "Flask==2.3.0\ngunicorn==20.1.0\n"
    )
    print(f"   {msg}")
    
    sucesso, msg, path = gw.criar_arquivo(
        "templates/index.html",
        """<!DOCTYPE html>
<html>
<head>
    <title>Luna Web</title>
</head>
<body>
    <h1>Projeto criado por Luna! 🌙</h1>
</body>
</html>
"""
    )
    print(f"   {msg}")
    
    print("\n5️⃣ Exibindo árvore de arquivos...")
    gw.exibir_arvore()
    
    print("6️⃣ Listando arquivos do workspace...")
    arquivos = gw.listar_arquivos()
    print(f"   📁 {len(arquivos)} arquivo(s) encontrado(s):")
    for arquivo in arquivos:
        print(f"      • {arquivo.name}")
    
    print("\n7️⃣ Buscando arquivo...")
    resultado = gw.buscar_arquivo("app.py")
    if resultado:
        print(f"   ✅ Encontrado: {resultado}")
    else:
        print("   ❌ Não encontrado")


def exemplo_multiplos_workspaces():
    """Exemplo com múltiplos workspaces"""
    separador("🔄 TRABALHANDO COM MÚLTIPLOS WORKSPACES")
    
    gw = GerenciadorWorkspaces()
    
    # Criar vários projetos
    projetos = [
        ("dashboard_vendas", "Dashboard de vendas em React"),
        ("api_rest", "API REST em FastAPI"),
        ("scraper_noticias", "Web scraper de notícias"),
    ]
    
    print("Criando múltiplos projetos...\n")
    for nome, desc in projetos:
        sucesso, msg = gw.criar_workspace(nome, desc)
        print(f"{msg}")
        time.sleep(0.1)  # Visual
    
    print("\n📊 Status geral:")
    gw.exibir_status()
    
    # Trabalhar em cada um
    print("Trabalhando em cada workspace...\n")
    
    for nome, _ in projetos:
        gw.selecionar_workspace(nome)
        print(f"📌 Workspace atual: {nome}")
        
        # Criar arquivo README
        gw.criar_arquivo(
            "README.md",
            f"# {nome}\n\nProjeto gerenciado por Luna 🌙\n"
        )
        print(f"   ✅ README.md criado\n")


def exemplo_organizacao_avancada():
    """Exemplo de organização avançada"""
    separador("📚 ORGANIZAÇÃO AVANÇADA")
    
    gw = GerenciadorWorkspaces()
    
    # Criar projeto completo
    print("Criando projeto completo com estrutura...\n")
    
    gw.criar_workspace("app_completo", "Aplicação full-stack")
    gw.selecionar_workspace("app_completo")
    
    # Estrutura de pastas
    estrutura = [
        ("backend/app.py", "# Backend principal\n"),
        ("backend/config.py", "# Configurações\n"),
        ("backend/requirements.txt", "fastapi\nuvicorn\n"),
        ("frontend/index.html", "<!-- Frontend -->\n"),
        ("frontend/style.css", "/* Estilos */\n"),
        ("frontend/script.js", "// JavaScript\n"),
        ("database/models.py", "# Modelos do banco\n"),
        ("database/migrations/001_initial.sql", "-- SQL migration\n"),
        ("tests/test_app.py", "# Testes unitários\n"),
        ("docs/API.md", "# Documentação da API\n"),
        ("README.md", "# App Completo\n"),
    ]
    
    for arquivo, conteudo in estrutura:
        gw.criar_arquivo(arquivo, conteudo)
        print(f"✅ {arquivo}")
    
    print("\n📁 Estrutura criada:")
    gw.exibir_arvore(max_nivel=4)


def exemplo_gerenciamento():
    """Exemplo de operações de gerenciamento"""
    separador("⚙️  OPERAÇÕES DE GERENCIAMENTO")
    
    gw = GerenciadorWorkspaces()
    
    # Criar workspace temporário
    print("1️⃣ Criando workspace temporário...")
    gw.criar_workspace("temp_teste", "Workspace para teste")
    print("   ✅ Criado\n")
    
    # Renomear
    print("2️⃣ Renomeando workspace...")
    sucesso, msg = gw.renomear_workspace("temp_teste", "projeto_teste")
    print(f"   {msg}\n")
    
    # Status
    print("3️⃣ Verificando status...")
    gw.exibir_status()
    
    # Deletar
    print("4️⃣ Deletando workspace...")
    sucesso, msg = gw.deletar_workspace("projeto_teste", confirmar=True)
    print(f"   {msg}\n")
    
    # Status final
    print("5️⃣ Status final:")
    gw.exibir_status()


def exemplo_busca_arquivos():
    """Exemplo de busca de arquivos"""
    separador("🔍 BUSCA DE ARQUIVOS")
    
    gw = GerenciadorWorkspaces()
    
    # Criar workspace com vários arquivos
    gw.criar_workspace("busca_teste", "Teste de busca")
    gw.selecionar_workspace("busca_teste")
    
    arquivos_teste = [
        "config.json",
        "settings.yaml",
        "database.sqlite",
        "app_config.py",
        "test_config.py",
        "README.md",
        "src/main.py",
        "src/utils.py",
        "data/users.csv",
        "data/products.json",
    ]
    
    print("Criando arquivos de teste...\n")
    for arquivo in arquivos_teste:
        gw.criar_arquivo(arquivo, f"# {arquivo}\n")
        print(f"✅ {arquivo}")
    
    # Testes de busca
    print("\n" + "-"*70)
    print("🔍 Testes de busca:\n")
    
    testes = [
        "config.json",      # Busca exata
        "config",           # Busca parcial
        "main.py",          # Arquivo em subpasta
        "inexistente.txt",  # Arquivo que não existe
    ]
    
    for busca in testes:
        print(f"Buscando: '{busca}'")
        resultado = gw.buscar_arquivo(busca)
        if resultado:
            print(f"   ✅ Encontrado: {resultado.relative_to(gw.workspaces_dir)}")
        else:
            print(f"   ❌ Não encontrado")
        print()


def menu_interativo():
    """Menu interativo para testar funcionalidades"""
    separador("🎮 MENU INTERATIVO")
    
    gw = GerenciadorWorkspaces()
    
    while True:
        print("\n" + "="*70)
        print("📁 WORKSPACE MANAGER - MENU")
        print("="*70)
        print("\n1. Criar workspace")
        print("2. Listar workspaces")
        print("3. Selecionar workspace")
        print("4. Criar arquivo")
        print("5. Listar arquivos")
        print("6. Exibir árvore")
        print("7. Buscar arquivo")
        print("8. Renomear workspace")
        print("9. Deletar workspace")
        print("0. Sair")
        
        opcao = input("\n👉 Escolha uma opção: ").strip()
        
        if opcao == "0":
            print("\n👋 Até logo!\n")
            break
        
        elif opcao == "1":
            nome = input("Nome do workspace: ").strip()
            desc = input("Descrição: ").strip()
            sucesso, msg = gw.criar_workspace(nome, desc)
            print(f"\n{msg}")
        
        elif opcao == "2":
            gw.exibir_status()
        
        elif opcao == "3":
            nome = input("Nome do workspace: ").strip()
            sucesso, msg = gw.selecionar_workspace(nome)
            print(f"\n{msg}")
        
        elif opcao == "4":
            nome = input("Nome do arquivo: ").strip()
            conteudo = input("Conteúdo (opcional): ").strip()
            sucesso, msg, path = gw.criar_arquivo(nome, conteudo)
            print(f"\n{msg}")
            if path:
                print(f"📍 {path}")
        
        elif opcao == "5":
            arquivos = gw.listar_arquivos()
            print(f"\n📁 {len(arquivos)} arquivo(s):")
            for arq in arquivos:
                print(f"   • {arq.name}")
        
        elif opcao == "6":
            gw.exibir_arvore()
        
        elif opcao == "7":
            busca = input("Nome do arquivo: ").strip()
            resultado = gw.buscar_arquivo(busca)
            if resultado:
                print(f"\n✅ Encontrado: {resultado}")
            else:
                print("\n❌ Não encontrado")
        
        elif opcao == "8":
            antigo = input("Nome atual: ").strip()
            novo = input("Novo nome: ").strip()
            sucesso, msg = gw.renomear_workspace(antigo, novo)
            print(f"\n{msg}")
        
        elif opcao == "9":
            nome = input("Nome do workspace: ").strip()
            confirmar = input("Tem certeza? (sim/não): ").strip().lower()
            if confirmar == "sim":
                sucesso, msg = gw.deletar_workspace(nome, confirmar=True)
                print(f"\n{msg}")
            else:
                print("\n❌ Operação cancelada")
        
        else:
            print("\n❌ Opção inválida")
        
        input("\n[Pressione ENTER para continuar]")


def main():
    """Menu principal de exemplos"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        📁 WORKSPACE MANAGER - EXEMPLOS E TESTES             ║
║                      🌙 LUNA 🌙                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    print("\n📚 Escolha um exemplo:\n")
    print("1. Exemplo básico")
    print("2. Múltiplos workspaces")
    print("3. Organização avançada")
    print("4. Operações de gerenciamento")
    print("5. Busca de arquivos")
    print("6. Menu interativo")
    print("7. Executar todos os exemplos")
    print("0. Sair")
    
    opcao = input("\n👉 Escolha: ").strip()
    
    if opcao == "1":
        exemplo_basico()
    elif opcao == "2":
        exemplo_multiplos_workspaces()
    elif opcao == "3":
        exemplo_organizacao_avancada()
    elif opcao == "4":
        exemplo_gerenciamento()
    elif opcao == "5":
        exemplo_busca_arquivos()
    elif opcao == "6":
        menu_interativo()
    elif opcao == "7":
        exemplo_basico()
        exemplo_multiplos_workspaces()
        exemplo_organizacao_avancada()
        exemplo_gerenciamento()
        exemplo_busca_arquivos()
    else:
        print("\n👋 Até logo!\n")


if __name__ == "__main__":
    main()
