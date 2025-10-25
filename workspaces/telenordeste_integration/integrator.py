"""
Integrator - TeleNordeste Integration
Orquestra a sincronização entre Notion e Google Calendar
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path

from config import ConfigManager
from notion_client import NotionClient
from google_calendar_client import GoogleCalendarClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NotionCalendarIntegrator:
    """Integrador entre Notion e Google Calendar"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        self.notion = None
        self.calendar = None
        self.sync_history = []
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Inicializa clientes Notion e Google Calendar"""
        try:
            # Inicializar Notion
            notion_token = self.config.get_notion_token()
            notion_db = self.config.get_notion_database_id()
            
            if notion_token and notion_db:
                self.notion = NotionClient(notion_token, notion_db)
                logger.info("✅ Cliente Notion inicializado")
            else:
                logger.warning("⚠️ Credenciais do Notion não configuradas")
            
            # Inicializar Google Calendar
            credentials_file = self.config.get_credentials_file()
            token_file = self.config.get_token_file()
            calendar_id = self.config.get_calendar_id()
            timezone = self.config.get_timezone()
            
            if credentials_file.exists():
                self.calendar = GoogleCalendarClient(
                    credentials_file, token_file, calendar_id, timezone
                )
                logger.info("✅ Cliente Google Calendar inicializado")
            else:
                logger.warning(f"⚠️ Arquivo de credenciais não encontrado: {credentials_file}")
        
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar clientes: {e}")
            raise
    
    def test_connections(self) -> bool:
        """Testa conexões com Notion e Google Calendar"""
        logger.info("🧪 Testando conexões...")
        
        notion_ok = False
        calendar_ok = False
        
        if self.notion:
            notion_ok = self.notion.test_connection()
        else:
            logger.error("❌ Cliente Notion não inicializado")
        
        if self.calendar:
            calendar_ok = self.calendar.test_connection()
        else:
            logger.error("❌ Cliente Google Calendar não inicializado")
        
        if notion_ok and calendar_ok:
            logger.info("✅ Todas as conexões OK!")
            return True
        else:
            logger.error("❌ Falha em uma ou mais conexões")
            return False
    
    def sync_tasks_to_calendar(self, status_filter: str = "A Fazer",
                              dry_run: bool = False) -> Dict:
        """
        Sincroniza tarefas do Notion para Google Calendar
        
        Args:
            status_filter: Filtrar tarefas por status
            dry_run: Se True, apenas simula sem criar eventos
        
        Returns:
            Dicionário com estatísticas da sincronização
        """
        logger.info(f"🔄 Iniciando sincronização de tarefas (Status: {status_filter})")
        
        stats = {
            "total_tasks": 0,
            "created": 0,
            "skipped": 0,
            "errors": 0,
            "dry_run": dry_run
        }
        
        if not self.notion or not self.calendar:
            logger.error("❌ Clientes não inicializados")
            return stats
        
        try:
            # Buscar tarefas do Notion
            tasks = self.notion.get_pending_tasks(
                status_property="Status",
                status_value=status_filter
            )
            stats["total_tasks"] = len(tasks)
            
            if not tasks:
                logger.info("ℹ️ Nenhuma tarefa encontrada")
                return stats
            
            mapping = self.config.get_mapping()
            
            # Processar cada tarefa
            for task in tasks:
                try:
                    task_data = self.notion.extract_task_data(task, mapping)
                    
                    # Validar dados obrigatórios
                    if not task_data.get("title"):
                        logger.warning(f"⚠️ Tarefa sem título, pulando: {task.get('id')}")
                        stats["skipped"] += 1
                        continue
                    
                    if not task_data.get("start_date"):
                        logger.warning(f"⚠️ Tarefa sem data, pulando: {task_data['title']}")
                        stats["skipped"] += 1
                        continue
                    
                    # Verificar se evento já existe
                    existing_event = self.calendar.find_event_by_summary(
                        task_data["title"],
                        time_min=datetime.now() - timedelta(days=30)
                    )
                    
                    if existing_event:
                        logger.info(f"⏭️ Evento já existe: {task_data['title']}")
                        stats["skipped"] += 1
                        continue
                    
                    # Preparar dados do evento
                    start_time = datetime.fromisoformat(
                        task_data["start_date"].replace('Z', '+00:00')
                    )
                    
                    # Calcular end_time
                    duration = task_data.get("duration", 60)  # padrão 60 minutos
                    end_time = start_time + timedelta(minutes=duration)
                    
                    description = task_data.get("description", "")
                    if task_data.get("url"):
                        description += f"\n\n🔗 Notion: {task_data['url']}"
                    
                    # Criar evento (ou simular)
                    if dry_run:
                        logger.info(f"🔍 [DRY RUN] Criaria evento: {task_data['title']}")
                        logger.info(f"   📅 Data: {start_time}")
                        stats["created"] += 1
                    else:
                        event_id = self.calendar.create_event(
                            summary=task_data["title"],
                            start_time=start_time,
                            end_time=end_time,
                            description=description
                        )
                        
                        if event_id:
                            stats["created"] += 1
                            
                            # Registrar sincronização
                            self.sync_history.append({
                                "notion_id": task_data["id"],
                                "calendar_id": event_id,
                                "title": task_data["title"],
                                "synced_at": datetime.now().isoformat()
                            })
                        else:
                            stats["errors"] += 1
                
                except Exception as e:
                    logger.error(f"❌ Erro ao processar tarefa: {e}")
                    stats["errors"] += 1
            
            # Relatório final
            logger.info("=" * 60)
            logger.info("📊 RELATÓRIO DE SINCRONIZAÇÃO")
            logger.info("=" * 60)
            logger.info(f"Total de tarefas encontradas: {stats['total_tasks']}")
            logger.info(f"✅ Eventos criados: {stats['created']}")
            logger.info(f"⏭️ Eventos pulados: {stats['skipped']}")
            logger.info(f"❌ Erros: {stats['errors']}")
            if dry_run:
                logger.info("🔍 Modo DRY RUN - Nenhum evento foi realmente criado")
            logger.info("=" * 60)
        
        except Exception as e:
            logger.error(f"❌ Erro na sincronização: {e}")
            stats["errors"] += 1
        
        return stats
    
    def sync_specific_task(self, task_id: str) -> bool:
        """
        Sincroniza uma tarefa específica do Notion
        
        Args:
            task_id: ID da tarefa no Notion
        
        Returns:
            True se sucesso, False caso contrário
        """
        # TODO: Implementar sincronização de tarefa específica
        logger.warning("⚠️ Sincronização de tarefa específica ainda não implementada")
        return False
    
    def get_sync_history(self) -> List[Dict]:
        """Retorna histórico de sincronizações"""
        return self.sync_history
    
    def clear_sync_history(self):
        """Limpa histórico de sincronizações"""
        self.sync_history = []
        logger.info("🗑️ Histórico de sincronização limpo")


def main():
    """Função principal para teste"""
    print("=" * 60)
    print("🚀 TeleNordeste Integration - Notion ↔ Google Calendar")
    print("=" * 60)
    
    # Carregar configuração
    config = ConfigManager()
    
    # Validar configuração
    is_valid, errors = config.validate_config()
    if not is_valid:
        print("\n❌ Erros na configuração:")
        for error in errors:
            print(f"  {error}")
        print("\n💡 Configure as credenciais em config.json")
        return
    
    # Criar integrador
    integrator = NotionCalendarIntegrator(config)
    
    # Testar conexões
    if not integrator.test_connections():
        print("\n❌ Falha ao conectar. Verifique as configurações.")
        return
    
    print("\n" + "=" * 60)
    print("Opções:")
    print("1. Sincronizar tarefas (DRY RUN)")
    print("2. Sincronizar tarefas (REAL)")
    print("3. Ver histórico de sincronização")
    print("=" * 60)
    
    choice = input("\nEscolha uma opção (1-3): ").strip()
    
    if choice == "1":
        print("\n🔍 Executando sincronização em modo DRY RUN...")
        stats = integrator.sync_tasks_to_calendar(dry_run=True)
    elif choice == "2":
        confirm = input("\n⚠️ Isso criará eventos reais no Google Calendar. Continuar? (s/n): ")
        if confirm.lower() == 's':
            print("\n🚀 Executando sincronização REAL...")
            stats = integrator.sync_tasks_to_calendar(dry_run=False)
        else:
            print("❌ Operação cancelada")
    elif choice == "3":
        history = integrator.get_sync_history()
        if history:
            print(f"\n📜 Histórico ({len(history)} itens):")
            for item in history:
                print(f"  • {item['title']} - {item['synced_at']}")
        else:
            print("\nℹ️ Nenhum item no histórico")
    else:
        print("❌ Opção inválida")


if __name__ == "__main__":
    main()
