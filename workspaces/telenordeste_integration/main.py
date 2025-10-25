"""
Main Script - TeleNordeste Integration
Interface principal para execução da integração
"""

import sys
import logging
from datetime import datetime
from pathlib import Path

from config import ConfigManager
from integrator import NotionCalendarIntegrator

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('integration.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def print_banner():
    """Exibe banner do sistema"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           🚀 TELENORDESTE INTEGRATION 🚀                     ║
║                                                              ║
║         Sincronização Notion ↔ Google Calendar               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def setup_wizard():
    """Assistente de configuração inicial"""
    print("\n" + "=" * 60)
    print("🔧 ASSISTENTE DE CONFIGURAÇÃO")
    print("=" * 60)
    
    config = ConfigManager()
    
    print("\n📋 CONFIGURAÇÃO DO NOTION")
    print("-" * 60)
    
    # Notion Token
    notion_token = input("Notion API Token (Integration Token): ").strip()
    if not notion_token:
        print("❌ Token é obrigatório!")
        return False
    
    # Notion Database ID
    notion_db = input("Notion Database ID: ").strip()
    if not notion_db:
        print("❌ Database ID é obrigatório!")
        return False
    
    config.set_notion_credentials(notion_token, notion_db)
    
    print("\n📅 CONFIGURAÇÃO DO GOOGLE CALENDAR")
    print("-" * 60)
    print("ℹ️ Você precisa do arquivo 'credentials.json' do Google Cloud Console")
    print("🔗 https://console.cloud.google.com/apis/credentials")
    
    creds_file = input("\nCaminho do arquivo credentials.json (ou Enter para 'credentials.json'): ").strip()
    if not creds_file:
        creds_file = "credentials.json"
    
    creds_path = Path(creds_file)
    if not creds_path.exists():
        print(f"⚠️ Arquivo não encontrado: {creds_path}")
        print("Coloque o arquivo credentials.json na pasta do projeto")
        return False
    
    # Atualizar config com caminho do arquivo
    config.config["google_calendar"]["credentials_file"] = creds_file
    config.save_config()
    
    print("\n✅ Configuração salva com sucesso!")
    return True


def show_menu():
    """Exibe menu principal"""
    menu = """
┌──────────────────────────────────────────────────────────────┐
│                        MENU PRINCIPAL                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. 🧪 Testar Conexões                                       │
│  2. 🔍 Sincronizar (Dry Run - Simulação)                     │
│  3. 🚀 Sincronizar (Real - Criar Eventos)                    │
│  4. 📊 Ver Estatísticas                                      │
│  5. 📜 Ver Histórico de Sincronização                        │
│  6. 🔧 Reconfigurar Credenciais                              │
│  7. 📖 Ajuda                                                 │
│  8. 🚪 Sair                                                  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
"""
    print(menu)


def show_help():
    """Exibe ajuda"""
    help_text = """
╔══════════════════════════════════════════════════════════════╗
║                           AJUDA                              ║
╚══════════════════════════════════════════════════════════════╝

📌 COMO FUNCIONA:

1. O sistema busca tarefas no Notion (database configurado)
2. Filtra por status (padrão: "A Fazer")
3. Para cada tarefa com data definida, cria evento no Google Calendar
4. Evita duplicação verificando eventos existentes

📌 CONFIGURAÇÃO DO NOTION:

• Crie uma integração em: https://www.notion.so/my-integrations
• Copie o "Internal Integration Token"
• Compartilhe seu database com a integração
• Copie o ID do database da URL

📌 CONFIGURAÇÃO DO GOOGLE CALENDAR:

• Acesse: https://console.cloud.google.com/apis/credentials
• Crie um projeto (se não tiver)
• Ative a API do Google Calendar
• Crie credenciais OAuth 2.0
• Baixe o arquivo JSON como "credentials.json"

📌 ESTRUTURA DO NOTION (Recomendada):

• Name (Título) - Obrigatório
• Data (Date) - Obrigatório para sincronização
• Status (Select) - Para filtrar tarefas
• Descrição (Rich Text) - Opcional
• Duração (Number) - Em minutos, opcional (padrão: 60)

📌 DRY RUN vs REAL:

• Dry Run: Apenas simula, não cria eventos (seguro para testar)
• Real: Cria eventos reais no Google Calendar

📌 LOGS:

• Arquivo: integration.log
• Contém histórico detalhado de todas as operações

╚══════════════════════════════════════════════════════════════╝
"""
    print(help_text)


def main():
    """Função principal"""
    print_banner()
    
    # Verificar configuração
    config = ConfigManager()
    is_valid, errors = config.validate_config()
    
    if not is_valid:
        print("⚠️ Configuração incompleta ou inválida!")
        print("\nProblemas encontrados:")
        for error in errors:
            print(f"  {error}")
        
        print("\n" + "=" * 60)
        choice = input("Deseja executar o assistente de configuração? (s/n): ")
        if choice.lower() == 's':
            if not setup_wizard():
                print("\n❌ Configuração não completada. Encerrando...")
                return
            print("\n✅ Configuração concluída! Reinicie o programa.")
            return
        else:
            print("❌ Configure manualmente o arquivo config.json")
            return
    
    # Inicializar integrador
    try:
        integrator = NotionCalendarIntegrator(config)
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar integrador: {e}")
        print(f"\n❌ Erro: {e}")
        return
    
    # Loop principal
    while True:
        show_menu()
        choice = input("Escolha uma opção (1-8): ").strip()
        
        if choice == "1":
            # Testar conexões
            print("\n🧪 Testando conexões...")
            print("-" * 60)
            integrator.test_connections()
            input("\nPressione Enter para continuar...")
        
        elif choice == "2":
            # Dry Run
            print("\n🔍 SINCRONIZAÇÃO - DRY RUN (Simulação)")
            print("-" * 60)
            status_filter = input("Filtrar por status (Enter para 'A Fazer'): ").strip()
            if not status_filter:
                status_filter = "A Fazer"
            
            stats = integrator.sync_tasks_to_calendar(
                status_filter=status_filter,
                dry_run=True
            )
            input("\nPressione Enter para continuar...")
        
        elif choice == "3":
            # Sincronização Real
            print("\n🚀 SINCRONIZAÇÃO REAL")
            print("-" * 60)
            print("⚠️ ATENÇÃO: Isso criará eventos reais no Google Calendar!")
            
            confirm = input("\nDeseja continuar? (digite 'SIM' para confirmar): ")
            if confirm.upper() == "SIM":
                status_filter = input("Filtrar por status (Enter para 'A Fazer'): ").strip()
                if not status_filter:
                    status_filter = "A Fazer"
                
                stats = integrator.sync_tasks_to_calendar(
                    status_filter=status_filter,
                    dry_run=False
                )
            else:
                print("❌ Operação cancelada")
            
            input("\nPressione Enter para continuar...")
        
        elif choice == "4":
            # Estatísticas
            print("\n📊 ESTATÍSTICAS")
            print("-" * 60)
            history = integrator.get_sync_history()
            print(f"Total de sincronizações: {len(history)}")
            
            if history:
                print(f"Primeira sincronização: {history[0]['synced_at']}")
                print(f"Última sincronização: {history[-1]['synced_at']}")
            
            input("\nPressione Enter para continuar...")
        
        elif choice == "5":
            # Histórico
            print("\n📜 HISTÓRICO DE SINCRONIZAÇÃO")
            print("-" * 60)
            history = integrator.get_sync_history()
            
            if history:
                for i, item in enumerate(history, 1):
                    print(f"{i}. {item['title']}")
                    print(f"   📅 Sincronizado em: {item['synced_at']}")
                    print(f"   🔗 Notion ID: {item['notion_id']}")
                    print(f"   📆 Calendar ID: {item['calendar_id']}")
                    print()
            else:
                print("ℹ️ Nenhum item no histórico")
            
            input("\nPressione Enter para continuar...")
        
        elif choice == "6":
            # Reconfigurar
            print("\n🔧 RECONFIGURAÇÃO")
            print("-" * 60)
            if setup_wizard():
                print("\n✅ Reconfigurando integrador...")
                try:
                    integrator = NotionCalendarIntegrator(ConfigManager())
                    print("✅ Integrador reconfigurado!")
                except Exception as e:
                    print(f"❌ Erro ao reconfigurar: {e}")
            
            input("\nPressione Enter para continuar...")
        
        elif choice == "7":
            # Ajuda
            show_help()
            input("\nPressione Enter para continuar...")
        
        elif choice == "8":
            # Sair
            print("\n👋 Até logo!")
            break
        
        else:
            print("\n❌ Opção inválida!")
            input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Operação interrompida pelo usuário")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}", exc_info=True)
        print(f"\n❌ Erro fatal: {e}")
        sys.exit(1)
