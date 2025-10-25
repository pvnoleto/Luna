"""
TeleNordeste - Sistema de Integração Notion + Google Calendar
Aplicação principal com interface de linha de comando
"""

import os
import sys
import argparse
from datetime import datetime
from dotenv import load_dotenv
from notion_client import NotionTaskClient
from calendar_client import GoogleCalendarClient
from sync_manager import SyncManager


def print_banner():
    """Exibe banner do sistema"""
    banner = """
    ╔════════════════════════════════════════════════════════╗
    ║                                                        ║
    ║           📋 TELENORDESTE - SYNC SYSTEM 📅            ║
    ║                                                        ║
    ║        Notion Task Manager + Google Calendar          ║
    ║                                                        ║
    ╚════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_configuration():
    """Verifica se as configurações necessárias estão presentes"""
    required_vars = ["NOTION_API_KEY", "NOTION_DATABASE_ID"]
    missing = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print("❌ Configuração incompleta!")
        print("\nVariáveis faltando no arquivo .env:")
        for var in missing:
            print(f"  • {var}")
        print("\n📝 Copie .env.example para .env e configure as variáveis")
        return False
    
    # Verificar credentials do Google
    if not os.path.exists("config/credentials.json"):
        print("⚠️ Aviso: config/credentials.json não encontrado")
        print("📥 Baixe em: https://console.cloud.google.com/apis/credentials")
        print("   1. Crie um projeto no Google Cloud")
        print("   2. Ative a Google Calendar API")
        print("   3. Crie credenciais OAuth 2.0")
        print("   4. Baixe e salve como config/credentials.json\n")
        return False
    
    return True


def initialize_clients():
    """Inicializa os clientes Notion e Google Calendar"""
    print("🔧 Inicializando clientes...")
    
    try:
        # Cliente Notion
        notion_client = NotionTaskClient(
            api_key=os.getenv("NOTION_API_KEY"),
            database_id=os.getenv("NOTION_DATABASE_ID"),
            timezone=os.getenv("TIMEZONE", "America/Fortaleza")
        )
        print("✅ Cliente Notion inicializado")
        
        # Cliente Google Calendar
        calendar_client = GoogleCalendarClient(
            credentials_path="config/credentials.json",
            calendar_id=os.getenv("GOOGLE_CALENDAR_ID", "primary"),
            timezone=os.getenv("TIMEZONE", "America/Fortaleza")
        )
        print("✅ Cliente Google Calendar inicializado")
        
        return notion_client, calendar_client
        
    except Exception as e:
        print(f"❌ Erro ao inicializar clientes: {e}")
        return None, None


def cmd_sync_all(args, manager):
    """Comando: Sincronizar todas as tarefas"""
    print("\n🔄 Sincronizando todas as tarefas...")
    manager.sync_notion_to_calendar()


def cmd_sync_status(args, manager):
    """Comando: Sincronizar tarefas por status"""
    status = args.status
    print(f"\n🔄 Sincronizando tarefas com status: {status}")
    manager.sync_notion_to_calendar(status_filter=status)


def cmd_auto_sync(args, manager):
    """Comando: Sincronização automática contínua"""
    interval = args.interval or int(os.getenv("SYNC_INTERVAL_MINUTES", 15))
    manager.auto_sync_loop(interval_minutes=interval)


def cmd_list_tasks(args, notion_client):
    """Comando: Listar tarefas do Notion"""
    print("\n📋 Buscando tarefas do Notion...")
    
    status = args.status if hasattr(args, 'status') else None
    tasks = notion_client.get_tasks(filter_status=status)
    
    if not tasks:
        print("ℹ️ Nenhuma tarefa encontrada")
        return
    
    print(f"\n✅ Encontradas {len(tasks)} tarefas:\n")
    
    for i, task in enumerate(tasks, 1):
        print(f"{i}. 📋 {task['title']}")
        print(f"   📊 Status: {task['status']}")
        print(f"   🎯 Prioridade: {task['priority']}")
        if task.get('date_start'):
            print(f"   📅 Data: {task['date_start']}")
        if task.get('assignee'):
            print(f"   👤 Responsável: {task['assignee']}")
        print(f"   🔗 {task['url']}")
        print()


def cmd_list_events(args, calendar_client):
    """Comando: Listar próximos eventos do calendário"""
    print("\n📅 Buscando eventos do Google Calendar...")
    
    max_results = args.max if hasattr(args, 'max') else 10
    events = calendar_client.list_upcoming_events(max_results=max_results)
    
    if not events:
        print("ℹ️ Nenhum evento encontrado")
        return
    
    print(f"\n✅ Próximos {len(events)} eventos:\n")
    
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        summary = event.get('summary', 'Sem título')
        print(f"  📅 {summary}")
        print(f"     🕐 {start}")
        if event.get('description'):
            desc = event['description'][:100]
            print(f"     📝 {desc}...")
        print()


def cmd_cleanup(args, manager):
    """Comando: Limpar eventos de tarefas concluídas"""
    print("\n🗑️ Limpando eventos de tarefas concluídas...")
    manager.remove_completed_events()


def cmd_info(args, manager):
    """Comando: Mostrar informações de sincronização"""
    info = manager.get_sync_info()
    
    print("\n" + "="*60)
    print("ℹ️  INFORMAÇÕES DE SINCRONIZAÇÃO")
    print("="*60)
    
    if info['last_sync']:
        last_sync = datetime.fromisoformat(info['last_sync'])
        print(f"🕐 Última sincronização: {last_sync.strftime('%d/%m/%Y %H:%M:%S')}")
    else:
        print("🕐 Última sincronização: Nunca")
    
    print(f"📊 Total de tarefas sincronizadas: {info['total_synced']}")
    print("="*60)
    
    if args.verbose and info['total_synced'] > 0:
        print("\n📋 Mapeamento de tarefas:")
        for task_id, event_id in list(info['mappings'].items())[:10]:
            print(f"  • {task_id[:8]}... → {event_id}")
        
        if info['total_synced'] > 10:
            print(f"  ... e mais {info['total_synced'] - 10} tarefas")


def main():
    """Função principal"""
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Parser de argumentos
    parser = argparse.ArgumentParser(
        description="TeleNordeste - Sincronização Notion + Google Calendar",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py sync                    # Sincronizar todas as tarefas
  python main.py sync --status "A Fazer" # Sincronizar por status
  python main.py auto                    # Sincronização automática
  python main.py auto --interval 30      # Auto-sync a cada 30 minutos
  python main.py list-tasks              # Listar tarefas do Notion
  python main.py list-events             # Listar eventos do Calendar
  python main.py cleanup                 # Limpar tarefas concluídas
  python main.py info                    # Informações de sincronização
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')
    
    # Comando: sync
    sync_parser = subparsers.add_parser('sync', help='Sincronizar tarefas')
    sync_parser.add_argument('--status', help='Filtrar por status')
    
    # Comando: auto
    auto_parser = subparsers.add_parser('auto', help='Sincronização automática')
    auto_parser.add_argument('--interval', type=int, help='Intervalo em minutos')
    
    # Comando: list-tasks
    list_tasks_parser = subparsers.add_parser('list-tasks', help='Listar tarefas do Notion')
    list_tasks_parser.add_argument('--status', help='Filtrar por status')
    
    # Comando: list-events
    list_events_parser = subparsers.add_parser('list-events', help='Listar eventos do Calendar')
    list_events_parser.add_argument('--max', type=int, default=10, help='Máximo de eventos')
    
    # Comando: cleanup
    subparsers.add_parser('cleanup', help='Limpar tarefas concluídas')
    
    # Comando: info
    info_parser = subparsers.add_parser('info', help='Informações de sincronização')
    info_parser.add_argument('--verbose', '-v', action='store_true', help='Modo detalhado')
    
    args = parser.parse_args()
    
    # Exibir banner
    print_banner()
    
    # Verificar configuração
    if not check_configuration():
        sys.exit(1)
    
    # Se nenhum comando, mostrar ajuda
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Inicializar clientes
    notion_client, calendar_client = initialize_clients()
    
    if not notion_client or not calendar_client:
        sys.exit(1)
    
    # Criar gerenciador de sincronização
    manager = SyncManager(notion_client, calendar_client)
    
    # Executar comando
    try:
        if args.command == 'sync':
            if args.status:
                cmd_sync_status(args, manager)
            else:
                cmd_sync_all(args, manager)
        
        elif args.command == 'auto':
            cmd_auto_sync(args, manager)
        
        elif args.command == 'list-tasks':
            cmd_list_tasks(args, notion_client)
        
        elif args.command == 'list-events':
            cmd_list_events(args, calendar_client)
        
        elif args.command == 'cleanup':
            cmd_cleanup(args, manager)
        
        elif args.command == 'info':
            cmd_info(args, manager)
        
        print("\n✅ Comando executado com sucesso!")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Operação interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
