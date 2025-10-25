"""
Exemplos de Uso - TeleNordeste Integration
Exemplos práticos de como usar a integração programaticamente
"""

from datetime import datetime, timedelta
from config import ConfigManager
from notion_client import NotionClient
from google_calendar_client import GoogleCalendarClient
from integrator import NotionCalendarIntegrator


def example_1_basic_sync():
    """Exemplo 1: Sincronização básica"""
    print("\n" + "=" * 60)
    print("EXEMPLO 1: Sincronização Básica")
    print("=" * 60)
    
    # Inicializar
    config = ConfigManager()
    integrator = NotionCalendarIntegrator(config)
    
    # Sincronizar (dry run)
    stats = integrator.sync_tasks_to_calendar(dry_run=True)
    
    print(f"\n📊 Resultados:")
    print(f"  Total de tarefas: {stats['total_tasks']}")
    print(f"  Seriam criados: {stats['created']} eventos")
    print(f"  Pulados: {stats['skipped']}")


def example_2_filter_by_status():
    """Exemplo 2: Filtrar por status específico"""
    print("\n" + "=" * 60)
    print("EXEMPLO 2: Filtrar por Status")
    print("=" * 60)
    
    config = ConfigManager()
    integrator = NotionCalendarIntegrator(config)
    
    # Diferentes status
    for status in ["A Fazer", "Em Progresso", "Urgente"]:
        print(f"\n🔍 Buscando tarefas: {status}")
        stats = integrator.sync_tasks_to_calendar(
            status_filter=status,
            dry_run=True
        )
        print(f"  Encontradas: {stats['total_tasks']} tarefas")


def example_3_notion_only():
    """Exemplo 3: Usar apenas o cliente Notion"""
    print("\n" + "=" * 60)
    print("EXEMPLO 3: Apenas Notion Client")
    print("=" * 60)
    
    config = ConfigManager()
    
    # Criar cliente Notion
    notion = NotionClient(
        api_token=config.get_notion_token(),
        database_id=config.get_notion_database_id()
    )
    
    # Testar conexão
    notion.test_connection()
    
    # Buscar tarefas
    tasks = notion.get_pending_tasks(status_value="A Fazer")
    
    print(f"\n📋 Tarefas encontradas: {len(tasks)}")
    
    # Mostrar primeiras 3 tarefas
    mapping = config.get_mapping()
    for i, task in enumerate(tasks[:3], 1):
        task_data = notion.extract_task_data(task, mapping)
        print(f"\n{i}. {task_data.get('title', 'Sem título')}")
        print(f"   📅 Data: {task_data.get('start_date', 'Não definida')}")
        print(f"   📝 Status: {task_data.get('status', 'N/A')}")


def example_4_calendar_only():
    """Exemplo 4: Usar apenas o cliente Google Calendar"""
    print("\n" + "=" * 60)
    print("EXEMPLO 4: Apenas Google Calendar Client")
    print("=" * 60)
    
    config = ConfigManager()
    
    # Criar cliente Calendar
    calendar = GoogleCalendarClient(
        credentials_file=config.get_credentials_file(),
        token_file=config.get_token_file(),
        calendar_id=config.get_calendar_id(),
        timezone=config.get_timezone()
    )
    
    # Testar conexão
    calendar.test_connection()
    
    # Buscar eventos dos próximos 7 dias
    now = datetime.now()
    next_week = now + timedelta(days=7)
    
    events = calendar.get_events(time_min=now, time_max=next_week)
    
    print(f"\n📅 Eventos nos próximos 7 dias: {len(events)}")
    
    for i, event in enumerate(events[:5], 1):
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"\n{i}. {event.get('summary', 'Sem título')}")
        print(f"   📅 Início: {start}")


def example_5_create_manual_event():
    """Exemplo 5: Criar evento manualmente"""
    print("\n" + "=" * 60)
    print("EXEMPLO 5: Criar Evento Manual")
    print("=" * 60)
    
    config = ConfigManager()
    
    calendar = GoogleCalendarClient(
        credentials_file=config.get_credentials_file(),
        token_file=config.get_token_file(),
        calendar_id=config.get_calendar_id()
    )
    
    # Criar evento de teste
    start_time = datetime.now() + timedelta(days=1, hours=2)
    end_time = start_time + timedelta(hours=1)
    
    print(f"\n📝 Criando evento de teste...")
    print(f"   Título: Reunião de Teste")
    print(f"   Início: {start_time}")
    print(f"   Fim: {end_time}")
    
    # Comentado para não criar evento real
    # Descomente para testar:
    """
    event_id = calendar.create_event(
        summary="Reunião de Teste - TeleNordeste",
        start_time=start_time,
        end_time=end_time,
        description="Evento criado automaticamente pela integração",
        location="Online"
    )
    
    if event_id:
        print(f"✅ Evento criado com ID: {event_id}")
    """
    
    print("⚠️ Código comentado - descomente para criar evento real")


def example_6_sync_with_date_filter():
    """Exemplo 6: Sincronizar tarefas de período específico"""
    print("\n" + "=" * 60)
    print("EXEMPLO 6: Sincronizar Período Específico")
    print("=" * 60)
    
    config = ConfigManager()
    notion = NotionClient(
        api_token=config.get_notion_token(),
        database_id=config.get_notion_database_id()
    )
    
    # Buscar tarefas da próxima semana
    start_date = datetime.now()
    end_date = start_date + timedelta(days=7)
    
    print(f"\n🔍 Buscando tarefas entre:")
    print(f"   {start_date.date()} e {end_date.date()}")
    
    tasks = notion.get_tasks_by_date(
        date_property="Data",
        start_date=start_date,
        end_date=end_date
    )
    
    mapping = config.get_mapping()
    
    print(f"\n📋 Tarefas encontradas: {len(tasks)}")
    for i, task in enumerate(tasks[:5], 1):
        task_data = notion.extract_task_data(task, mapping)
        print(f"{i}. {task_data.get('title', 'Sem título')}")


def example_7_check_sync_history():
    """Exemplo 7: Verificar histórico de sincronização"""
    print("\n" + "=" * 60)
    print("EXEMPLO 7: Histórico de Sincronização")
    print("=" * 60)
    
    config = ConfigManager()
    integrator = NotionCalendarIntegrator(config)
    
    # Executar sincronização (dry run)
    stats = integrator.sync_tasks_to_calendar(dry_run=True)
    
    # Ver histórico
    history = integrator.get_sync_history()
    
    print(f"\n📜 Itens no histórico: {len(history)}")
    
    if history:
        print("\nÚltimas sincronizações:")
        for item in history[-5:]:
            print(f"  • {item['title']} - {item['synced_at']}")


def main():
    """Menu de exemplos"""
    print("\n" + "=" * 60)
    print("EXEMPLOS DE USO - TeleNordeste Integration")
    print("=" * 60)
    
    examples = [
        ("Sincronização Básica", example_1_basic_sync),
        ("Filtrar por Status", example_2_filter_by_status),
        ("Apenas Notion Client", example_3_notion_only),
        ("Apenas Calendar Client", example_4_calendar_only),
        ("Criar Evento Manual", example_5_create_manual_event),
        ("Sincronizar Período Específico", example_6_sync_with_date_filter),
        ("Histórico de Sincronização", example_7_check_sync_history),
    ]
    
    print("\nEscolha um exemplo:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print("  0. Executar todos")
    
    try:
        choice = int(input("\nOpção: ").strip())
        
        if choice == 0:
            for name, func in examples:
                try:
                    func()
                except Exception as e:
                    print(f"\n❌ Erro no exemplo '{name}': {e}")
        elif 1 <= choice <= len(examples):
            examples[choice - 1][1]()
        else:
            print("❌ Opção inválida")
    
    except ValueError:
        print("❌ Digite um número válido")
    except Exception as e:
        print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()
