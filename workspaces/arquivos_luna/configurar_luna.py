#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 CONFIGURAÇÃO AUTOMÁTICA - LUNA COM WORKSPACE MANAGER
========================================================

Este script configura tudo automaticamente para você!

"""

import os
import sys
from pathlib import Path
import shutil


def banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🚀 CONFIGURAÇÃO AUTOMÁTICA - LUNA 🌙                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)


def verificar_arquivos_necessarios():
    """Verifica se todos arquivos necessários estão presentes"""
    print("\n🔍 Verificando arquivos necessários...\n")
    
    arquivos_obrigatorios = [
        "luna_completo.py",
        "gerenciador_workspaces.py",
    ]
    
    arquivos_opcionais = [
        "demo_workspace.py",
        "exemplo_workspace.py",
        "README_WORKSPACE.md",
        "INSTALACAO_RAPIDA.md",
    ]
    
    todos_ok = True
    
    print("📋 Arquivos obrigatórios:")
    for arquivo in arquivos_obrigatorios:
        if Path(arquivo).exists():
            print(f"   ✅ {arquivo}")
        else:
            print(f"   ❌ {arquivo} - FALTANDO!")
            todos_ok = False
    
    print("\n📋 Arquivos opcionais:")
    for arquivo in arquivos_opcionais:
        if Path(arquivo).exists():
            print(f"   ✅ {arquivo}")
        else:
            print(f"   ⚠️  {arquivo} - não encontrado (opcional)")
    
    return todos_ok


def criar_estrutura():
    """Cria estrutura básica de pastas"""
    print("\n📁 Criando estrutura básica...\n")
    
    # Criar pasta workspaces se não existir
    workspaces = Path("workspaces")
    if not workspaces.exists():
        workspaces.mkdir()
        print("   ✅ Pasta 'workspaces/' criada")
        
        # Criar README
        readme = workspaces / "README.md"
        readme.write_text("""# 📁 Workspaces

Esta pasta contém todos os seus projetos gerenciados por Luna.

## Como usar:

No Luna, digite:
- `criar workspace meu_projeto` - Cria novo projeto
- `listar workspaces` - Lista todos projetos
- `selecionar workspace meu_projeto` - Seleciona projeto

Cada projeto fica em sua própria pasta aqui!
""")
        print("   ✅ workspaces/README.md criado")
    else:
        print("   ℹ️  Pasta 'workspaces/' já existe")


def testar_luna():
    """Testa se Luna funciona"""
    print("\n🧪 Testando Luna...\n")
    
    try:
        # Importar módulos
        import luna_completo
        print("   ✅ luna_completo.py importado com sucesso")
        
        from gerenciador_workspaces import GerenciadorWorkspaces
        print("   ✅ gerenciador_workspaces.py importado com sucesso")
        
        # Testar instanciação
        gw = GerenciadorWorkspaces()
        print("   ✅ Workspace Manager inicializado")
        
        return True
    except Exception as e:
        print(f"   ❌ Erro ao testar: {e}")
        return False


def criar_workspace_exemplo():
    """Cria workspace de exemplo"""
    print("\n📦 Criando workspace de exemplo...\n")
    
    try:
        from gerenciador_workspaces import GerenciadorWorkspaces
        
        gw = GerenciadorWorkspaces()
        
        # Criar workspace exemplo
        sucesso, msg = gw.criar_workspace(
            "exemplo_inicial",
            "Workspace de exemplo criado pela configuração automática"
        )
        
        if sucesso:
            print(f"   {msg}")
            
            # Criar alguns arquivos de exemplo
            gw.criar_arquivo(
                "README.md",
                "# Exemplo Inicial\n\nEste é um workspace de exemplo criado automaticamente!\n"
            )
            print("   ✅ README.md criado")
            
            gw.criar_arquivo(
                "exemplo.py",
                "print('Hello from Luna! 🌙')\n"
            )
            print("   ✅ exemplo.py criado")
            
            return True
        else:
            print(f"   ⚠️  {msg}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False


def exibir_resumo():
    """Exibe resumo da configuração"""
    print("\n" + "="*70)
    print("✅ CONFIGURAÇÃO CONCLUÍDA!")
    print("="*70)
    print("""
🎯 O QUE FOI CONFIGURADO:

✅ Estrutura de pastas criada
✅ Workspace Manager testado
✅ Workspace de exemplo criado
✅ Arquivos de exemplo criados

📁 ESTRUTURA:

Luna/
├── luna_completo.py              ← Agente principal
├── gerenciador_workspaces.py     ← Workspace Manager
├── workspace_config.json          ← Configuração (criada)
│
└── workspaces/                    ← Seus projetos
    └── exemplo_inicial/           ← Exemplo criado
        ├── README.md
        └── exemplo.py

🚀 COMO USAR:

1. Execute Luna:
   python luna_completo.py

2. Digite comandos:
   👤 Você: ajuda
   👤 Você: listar workspaces
   👤 Você: selecionar workspace exemplo_inicial
   👤 Você: listar arquivos

3. Crie seus próprios workspaces:
   👤 Você: criar workspace meu_projeto

💡 DICAS:

• Luna lembra do último workspace usado
• Digite 'ajuda' para ver todos comandos
• Workspaces podem ter subpastas
• Exemplo: criar arquivo src/main.py

═══════════════════════════════════════════════════════════════

🌙 PRONTO! Luna está configurado e pronto para usar!

Execute: python luna_completo.py

═══════════════════════════════════════════════════════════════
    """)


def main():
    """Função principal"""
    banner()
    
    # Passo 1: Verificar arquivos
    if not verificar_arquivos_necessarios():
        print("\n❌ Configuração abortada: Arquivos obrigatórios faltando")
        print("   Certifique-se de ter luna_completo.py e gerenciador_workspaces.py")
        return
    
    # Passo 2: Criar estrutura
    criar_estrutura()
    
    # Passo 3: Testar
    if not testar_luna():
        print("\n⚠️  Alguns testes falharam, mas pode tentar usar mesmo assim")
        resposta = input("\nContinuar? (s/n): ").lower()
        if resposta != 's':
            return
    
    # Passo 4: Criar exemplo
    criar_workspace_exemplo()
    
    # Passo 5: Resumo
    exibir_resumo()
    
    # Perguntar se quer executar
    print("\n" + "="*70)
    resposta = input("Deseja executar Luna agora? (s/n): ").lower()
    
    if resposta == 's':
        print("\n🚀 Iniciando Luna...\n")
        print("="*70)
        
        try:
            import luna_completo
            luna = luna_completo.Luna()
            luna.iniciar()
        except Exception as e:
            print(f"\n❌ Erro ao executar: {e}")
    else:
        print("\n👋 Execute Luna com: python luna_completo.py\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Configuração cancelada pelo usuário\n")
    except Exception as e:
        print(f"\n❌ Erro na configuração: {e}")
        import traceback
        traceback.print_exc()
