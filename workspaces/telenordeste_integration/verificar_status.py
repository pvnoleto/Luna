#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Verificação de Status do Projeto TeleNordeste Integration
Verifica dependências, arquivos e configurações
"""

import os
import sys
import json
from pathlib import Path

# Cores para terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_ok(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def check_python_version():
    """Verifica versão do Python"""
    print_header("1. Verificando Python")
    version = sys.version_info
    print(f"Versão: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print_ok("Python 3.8+ detectado")
        return True
    else:
        print_error("Python 3.8+ é necessário")
        return False

def check_dependencies():
    """Verifica dependências instaladas"""
    print_header("2. Verificando Dependências")
    
    dependencies = {
        'requests': 'Notion API',
        'google.auth': 'Google Auth',
        'googleapiclient': 'Google Calendar API',
        'google_auth_oauthlib': 'Google OAuth',
        'dateutil': 'Date Utils',
        'pytz': 'Timezone Support'
    }
    
    all_installed = True
    for module, description in dependencies.items():
        try:
            __import__(module.replace('.', '_'))
            print_ok(f"{description} ({module})")
        except ImportError:
            print_error(f"{description} ({module}) - NÃO INSTALADO")
            all_installed = False
    
    if not all_installed:
        print_warning("\nPara instalar: pip install -r requirements.txt")
    
    return all_installed

def check_files():
    """Verifica arquivos essenciais"""
    print_header("3. Verificando Arquivos Essenciais")
    
    essential_files = {
        'main.py': 'Interface principal',
        'integrator.py': 'Orquestrador',
        'notion_client.py': 'Cliente Notion',
        'google_calendar_client.py': 'Cliente Google Calendar',
        'telenordeste_bot.py': 'Bot de automação',
        'config.py': 'Gerenciador de configurações',
        'config.json': 'Arquivo de configuração',
        'requirements.txt': 'Lista de dependências'
    }
    
    all_found = True
    for file, description in essential_files.items():
        if os.path.exists(file):
            size = os.path.getsize(file)
            print_ok(f"{description} ({file}) - {size:,} bytes")
        else:
            print_error(f"{description} ({file}) - NÃO ENCONTRADO")
            all_found = False
    
    return all_found

def check_config():
    """Verifica configurações"""
    print_header("4. Verificando Configurações")
    
    if not os.path.exists('config.json'):
        print_error("config.json não encontrado")
        return False
    
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print_ok("config.json carregado com sucesso")
        
        # Verificar estrutura
        has_site = 'site' in config
        has_credenciais = 'credenciais' in config
        has_automacao = 'automacao' in config
        
        if has_site:
            print_ok("Seção 'site' configurada")
        else:
            print_error("Seção 'site' ausente")
        
        if has_credenciais:
            usuario = config['credenciais'].get('usuario', '')
            senha = config['credenciais'].get('senha', '')
            
            if usuario and senha:
                print_ok(f"Credenciais configuradas (usuário: {usuario[:3]}***)")
            else:
                print_warning("Credenciais vazias - configure antes de usar")
        else:
            print_error("Seção 'credenciais' ausente")
        
        if has_automacao:
            print_ok("Seção 'automacao' configurada")
        else:
            print_error("Seção 'automacao' ausente")
        
        return has_site and has_credenciais and has_automacao
        
    except json.JSONDecodeError as e:
        print_error(f"Erro ao ler config.json: {e}")
        return False

def check_credentials():
    """Verifica credenciais das APIs"""
    print_header("5. Verificando Credenciais das APIs")
    
    # Notion
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Verificar se há chaves Notion no config
        notion_token = config.get('notion', {}).get('token', '')
        notion_database = config.get('notion', {}).get('database_id', '')
        
        if notion_token:
            print_ok(f"Notion Token configurado (secret_{notion_token[7:10]}***)")
        else:
            print_warning("Notion Token não configurado")
        
        if notion_database:
            print_ok(f"Notion Database ID configurado ({notion_database[:8]}***)")
        else:
            print_warning("Notion Database ID não configurado")
    except:
        print_warning("Credenciais Notion não encontradas no config.json")
    
    # Google Calendar
    if os.path.exists('credentials.json'):
        size = os.path.getsize('credentials.json')
        print_ok(f"credentials.json encontrado ({size:,} bytes)")
    else:
        print_warning("credentials.json não encontrado")
        print_info("Baixe do Google Cloud Console: https://console.cloud.google.com/")
    
    if os.path.exists('token.json'):
        print_ok("token.json encontrado (autenticação já realizada)")
    else:
        print_warning("token.json não encontrado (primeira autenticação pendente)")
    
    return True

def check_documentation():
    """Verifica documentação"""
    print_header("6. Verificando Documentação")
    
    docs = {
        'README.md': 'README básico',
        'README_COMPLETO.md': 'Documentação completa',
        'QUICK_START.md': 'Guia rápido',
        'RESUMO_PROJETO.md': 'Resumo executivo',
        'STATUS_PROJETO.md': 'Status atual'
    }
    
    for doc, description in docs.items():
        if os.path.exists(doc):
            print_ok(f"{description} ({doc})")
        else:
            print_warning(f"{description} ({doc}) - não encontrado")
    
    return True

def generate_report():
    """Gera relatório final"""
    print_header("📊 RELATÓRIO FINAL")
    
    checks = {
        'Python 3.8+': check_python_version(),
        'Dependências': check_dependencies(),
        'Arquivos Essenciais': check_files(),
        'Configurações': check_config(),
        'Credenciais': check_credentials(),
        'Documentação': check_documentation()
    }
    
    print_header("RESUMO")
    
    total = len(checks)
    passed = sum(1 for v in checks.values() if v)
    
    for check, result in checks.items():
        status = "✅ OK" if result else "❌ FALHOU"
        print(f"{check:.<40} {status}")
    
    print(f"\n{Colors.BOLD}Total: {passed}/{total} verificações passaram{Colors.END}")
    
    percentage = (passed / total) * 100
    
    if percentage == 100:
        print_ok("\n🎉 Projeto 100% pronto!")
        print_info("Execute: python main.py")
    elif percentage >= 70:
        print_warning(f"\n⚠️  Projeto {percentage:.0f}% pronto")
        print_info("Algumas configurações pendentes - veja detalhes acima")
    else:
        print_error(f"\n❌ Projeto {percentage:.0f}% pronto")
        print_info("Várias configurações necessárias - veja detalhes acima")
    
    print_header("PRÓXIMOS PASSOS")
    
    if not checks['Dependências']:
        print("1️⃣  Instalar dependências:")
        print("   pip install -r requirements.txt\n")
    
    if not checks['Credenciais']:
        print("2️⃣  Configurar credenciais:")
        print("   • Notion: https://www.notion.so/my-integrations")
        print("   • Google: https://console.cloud.google.com/\n")
    
    print("3️⃣  Executar o programa:")
    print("   python main.py\n")
    
    print("📚 Documentação completa: README_COMPLETO.md")
    print("🚀 Guia rápido: QUICK_START.md")

if __name__ == "__main__":
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║         TELENORDESTE INTEGRATION - STATUS CHECK           ║")
    print("║                   Verificação de Status                   ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(Colors.END)
    
    try:
        generate_report()
    except KeyboardInterrupt:
        print_warning("\n\nVerificação interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n\nErro durante verificação: {e}")
        sys.exit(1)
    
    print("\n")
