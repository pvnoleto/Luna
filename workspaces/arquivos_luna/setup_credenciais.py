#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 SETUP RÁPIDO DE CREDENCIAIS
================================

Script para adicionar rapidamente credenciais de serviços populares.
Já vem com seletores CSS pré-configurados!

Uso: python setup_credenciais.py
"""

import getpass
from cofre_credenciais import Cofre


# ============================================================================
# TEMPLATES DE SERVIÇOS POPULARES
# ============================================================================

SERVICOS = {
    "notion": {
        "nome": "Notion",
        "url_login": "https://www.notion.so/login",
        "seletor_usuario": "input[type='email']",
        "seletor_senha": "input[type='password']",
        "seletor_botao": "button[type='submit'], div[role='button']",
        "instrucoes": "Email e senha da sua conta Notion"
    },
    "github": {
        "nome": "GitHub",
        "url_login": "https://github.com/login",
        "seletor_usuario": "#login_field",
        "seletor_senha": "#password",
        "seletor_botao": "input[type='submit'][value='Sign in']",
        "instrucoes": "Username ou email e senha do GitHub"
    },
    "gmail": {
        "nome": "Gmail/Google",
        "url_login": "https://accounts.google.com/",
        "seletor_usuario": "input[type='email']",
        "seletor_senha": "input[type='password']",
        "seletor_botao": "button[type='button']",
        "instrucoes": "⚠️ Pode precisar de 2FA. Email e senha Google"
    },
    "linkedin": {
        "nome": "LinkedIn",
        "url_login": "https://www.linkedin.com/login",
        "seletor_usuario": "#username",
        "seletor_senha": "#password",
        "seletor_botao": "button[type='submit']",
        "instrucoes": "Email e senha do LinkedIn"
    },
    "twitter": {
        "nome": "Twitter/X",
        "url_login": "https://twitter.com/i/flow/login",
        "seletor_usuario": "input[autocomplete='username']",
        "seletor_senha": "input[type='password']",
        "seletor_botao": "button[type='button']",
        "instrucoes": "Username ou email e senha do Twitter"
    },
    "facebook": {
        "nome": "Facebook",
        "url_login": "https://www.facebook.com/login",
        "seletor_usuario": "#email",
        "seletor_senha": "#pass",
        "seletor_botao": "button[name='login']",
        "instrucoes": "Email ou telefone e senha do Facebook"
    },
    "instagram": {
        "nome": "Instagram",
        "url_login": "https://www.instagram.com/accounts/login/",
        "seletor_usuario": "input[name='username']",
        "seletor_senha": "input[name='password']",
        "seletor_botao": "button[type='submit']",
        "instrucoes": "Username ou email e senha do Instagram"
    },
    "wordpress": {
        "nome": "WordPress",
        "url_login": "https://wordpress.com/log-in",
        "seletor_usuario": "#usernameOrEmail",
        "seletor_senha": "#password",
        "seletor_botao": "button[type='submit']",
        "instrucoes": "Username ou email e senha do WordPress"
    },
    "trello": {
        "nome": "Trello",
        "url_login": "https://trello.com/login",
        "seletor_usuario": "#username",
        "seletor_senha": "#password",
        "seletor_botao": "#login-submit",
        "instrucoes": "Email e senha do Trello"
    },
    "slack": {
        "nome": "Slack",
        "url_login": "https://slack.com/signin",
        "seletor_usuario": "#email",
        "seletor_senha": "#password",
        "seletor_botao": "#signin_btn",
        "instrucoes": "Email e senha do Slack"
    },
    "custom": {
        "nome": "Customizado",
        "instrucoes": "Você fornecerá URL e seletores manualmente"
    }
}


def configurar_servico(cofre: Cofre, servico_id: str):
    """Configura um serviço específico"""
    
    if servico_id not in SERVICOS:
        print(f"❌ Serviço '{servico_id}' não encontrado")
        return False
    
    config = SERVICOS[servico_id]
    
    print(f"\n{'='*60}")
    print(f"CONFIGURAR: {config['nome']}")
    print(f"{'='*60}")
    print(f"ℹ️  {config['instrucoes']}\n")
    
    # Pedir credenciais
    usuario = input("👤 Usuário/Email: ").strip()
    if not usuario:
        print("❌ Cancelado")
        return False
    
    senha = getpass.getpass("🔑 Senha: ")
    if not senha:
        print("❌ Cancelado")
        return False
    
    # Extras
    extras = {}
    
    if servico_id == "custom":
        # Modo customizado
        extras["url_login"] = input("🔗 URL de login: ").strip()
        extras["seletor_usuario"] = input("👤 Seletor CSS do campo usuário: ").strip()
        extras["seletor_senha"] = input("🔑 Seletor CSS do campo senha: ").strip()
        extras["seletor_botao"] = input("🖱️ Seletor CSS do botão: ").strip()
    else:
        # Usar template
        extras["url_login"] = config["url_login"]
        extras["seletor_usuario"] = config["seletor_usuario"]
        extras["seletor_senha"] = config["seletor_senha"]
        extras["seletor_botao"] = config["seletor_botao"]
    
    # Notas opcionais
    notas = input("📝 Notas (opcional): ").strip()
    if notas:
        extras["notas"] = notas
    
    # Adicionar ao cofre
    try:
        cofre.adicionar_credencial(servico_id, usuario, senha, extras)
        print(f"\n✅ Credencial '{servico_id}' configurada com sucesso!")
        return True
    except Exception as e:
        print(f"\n❌ Erro ao adicionar: {e}")
        return False


def menu_principal():
    """Menu interativo de setup"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  🚀 SETUP RÁPIDO DE CREDENCIAIS                             ║
║                                                              ║
║  Configure facilmente credenciais para serviços populares   ║
║  (Seletores CSS já vêm prontos!)                            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Inicializar cofre
    print("🔐 Iniciando cofre...")
    cofre = Cofre()
    
    try:
        cofre.inicializar()
    except Exception as e:
        print(f"\n❌ Erro ao abrir cofre: {e}")
        return
    
    while True:
        print("\n" + "="*60)
        print("SERVIÇOS DISPONÍVEIS")
        print("="*60)
        
        # Listar serviços
        servicos_lista = list(SERVICOS.items())
        for i, (sid, config) in enumerate(servicos_lista, 1):
            # Verificar se já existe
            existe = "✅" if sid in cofre.listar_credenciais() else "➕"
            print(f"{i:2}. {existe} {config['nome']}")
        
        print("\n" + "-"*60)
        print("A. 📊 Mostrar resumo do cofre")
        print("0. 🚪 Sair")
        print("="*60)
        
        escolha = input("\nEscolha (número ou letra): ").strip().lower()
        
        try:
            if escolha == "0":
                print("\n👋 Configuração salva!")
                print("\n💡 Para usar com o agente:")
                print("   python agente_com_credenciais.py\n")
                break
            
            elif escolha == "a":
                cofre.mostrar_resumo()
            
            elif escolha.isdigit():
                idx = int(escolha) - 1
                if 0 <= idx < len(servicos_lista):
                    servico_id, _ = servicos_lista[idx]
                    
                    # Verificar se já existe
                    if servico_id in cofre.listar_credenciais():
                        confirmar = input(f"\n⚠️  '{servico_id}' já existe. Sobrescrever? (s/n): ")
                        if confirmar.lower() != 's':
                            continue
                    
                    configurar_servico(cofre, servico_id)
                else:
                    print("❌ Opção inválida")
            else:
                print("❌ Opção inválida")
        
        except KeyboardInterrupt:
            print("\n\n👋 Saindo...")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")


def setup_rapido_interativo():
    """Versão simplificada para setup inicial"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║  🎯 SETUP RÁPIDO - Configure 1-3 serviços principais        ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    cofre = Cofre()
    cofre.inicializar()
    
    print("\n💡 Vamos configurar os serviços que você mais usa!")
    print("   (Você pode adicionar mais depois)\n")
    
    # Sugerir os mais comuns
    sugestoes = ["notion", "gmail", "github"]
    
    for servico_id in sugestoes:
        config = SERVICOS[servico_id]
        
        print(f"\n{'─'*60}")
        configurar = input(f"Configurar {config['nome']}? (s/n): ").strip().lower()
        
        if configurar == 's':
            configurar_servico(cofre, servico_id)
    
    print(f"\n{'═'*60}")
    print("✅ Setup concluído!")
    print("\n💡 Para adicionar mais serviços:")
    print("   python setup_credenciais.py")
    print("\n💡 Para usar com o agente:")
    print("   python agente_com_credenciais.py")
    print(f"{'═'*60}\n")


# ============================================================================
# MODO DE USO
# ============================================================================

if __name__ == "__main__":
    import sys
    
    # Verificar dependências
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        print("❌ Instale: pip install cryptography")
        exit(1)
    
    if len(sys.argv) > 1 and sys.argv[1] == "rapido":
        # Modo setup rápido
        setup_rapido_interativo()
    else:
        # Modo completo
        menu_principal()
