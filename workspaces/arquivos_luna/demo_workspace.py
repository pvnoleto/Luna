#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ DEMO RÁPIDA - WORKSPACE MANAGER
==================================

Demonstração rápida das funcionalidades principais

"""

from gerenciador_workspaces import GerenciadorWorkspaces
import time


def animacao(texto: str, delay: float = 0.3):
    """Imprime texto com delay"""
    print(texto)
    time.sleep(delay)


def demo_rapida():
    """Demonstração rápida"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         ⚡ DEMONSTRAÇÃO RÁPIDA - WORKSPACE MANAGER          ║
║                      🌙 LUNA 🌙                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Inicializar
    animacao("\n🔧 Inicializando Workspace Manager...", 0.5)
    gw = GerenciadorWorkspaces()
    animacao("✅ Inicializado!\n", 0.5)
    
    # Criar workspace
    animacao("📁 Criando workspace 'demo_projeto'...", 0.5)
    sucesso, msg = gw.criar_workspace("demo_projeto", "Projeto de demonstração")
    animacao(f"   {msg}\n", 0.5)
    
    # Selecionar
    animacao("📌 Selecionando workspace...", 0.5)
    sucesso, msg = gw.selecionar_workspace("demo_projeto")
    animacao(f"   {msg}\n", 0.5)
    
    # Criar arquivos
    animacao("📝 Criando arquivos...", 0.5)
    
    arquivos = [
        ("app.py", "print('Hello Luna! 🌙')"),
        ("config.json", '{"version": "1.0"}'),
        ("README.md", "# Demo Projeto\n\nProjeto criado por Luna!"),
        ("src/main.py", "# Código principal"),
        ("tests/test_app.py", "# Testes"),
    ]
    
    for nome, conteudo in arquivos:
        sucesso, msg, path = gw.criar_arquivo(nome, conteudo)
        animacao(f"   {msg}", 0.2)
    
    print()
    
    # Exibir árvore
    animacao("🌳 Estrutura criada:\n", 0.5)
    gw.exibir_arvore()
    time.sleep(1)
    
    # Listar arquivos
    animacao("📋 Listando arquivos...\n", 0.5)
    arquivos = gw.listar_arquivos()
    for arquivo in arquivos:
        animacao(f"   • {arquivo.name}", 0.1)
    
    print()
    time.sleep(0.5)
    
    # Buscar arquivo
    animacao("\n🔍 Buscando 'app.py'...", 0.5)
    resultado = gw.buscar_arquivo("app.py")
    if resultado:
        animacao(f"   ✅ Encontrado: {resultado.name}\n", 0.5)
    
    # Status
    animacao("📊 Status geral:\n", 0.5)
    gw.exibir_status()
    time.sleep(1)
    
    # Resumo
    print("\n" + "="*70)
    print("✅ DEMONSTRAÇÃO CONCLUÍDA!")
    print("="*70)
    print("""
🎯 O que foi feito:

✅ Criado workspace 'demo_projeto'
✅ Selecionado como workspace atual
✅ Criado 5 arquivos organizados
✅ Listados e buscados arquivos
✅ Exibido status completo

📚 Workspace criado em: ./workspaces/demo_projeto/

Para ver mais exemplos, execute:
   python exemplo_workspace.py

Para ver documentação completa:
   cat README_WORKSPACE.md
    """)


if __name__ == "__main__":
    try:
        demo_rapida()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrompida pelo usuário\n")
    except Exception as e:
        print(f"\n❌ Erro na demonstração: {e}")
        import traceback
        traceback.print_exc()
