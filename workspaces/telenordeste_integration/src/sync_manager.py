"""
Gerenciador de Sincronização entre Notion e Google Calendar
Coordena a sincronização bidirecional de tarefas e eventos
"""

import os
import json
import time
from typing import Dict, List, Set
from datetime import datetime
from notion_client import NotionTaskClient
from calendar_client import GoogleCalendarClient


class SyncManager:
    """Gerencia a sincronização entre Notion e Google Calendar"""
    
    def __init__(self, notion_client: NotionTaskClient, calendar_client: GoogleCalendarClient):
        """
        Inicializa o gerenciador de sincronização
        
        Args:
            notion_client: Cliente do Notion
            calendar_client: Cliente do Google Calendar
        """
        self.notion = notion_client
        self.calendar = calendar_client
        self.sync_state_file = "config/sync_state.json"
        self.sync_state = self._load_sync_state()
    
    def _load_sync_state(self) -> Dict:
        """Carrega estado da última sincronização"""
        if os.path.exists(self.sync_state_file):
            try:
                with open(self.sync_state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "last_sync": None,
            "task_to_event": {},  # Mapeia notion_task_id -> calendar_event_id
            "synced_tasks": set()
        }
    
    def _save_sync_state(self):
        """Salva estado da sincronização"""
        os.makedirs("config", exist_ok=True)
        
        # Converter set para list para JSON
        save_state = self.sync_state.copy()
        if isinstance(save_state.get("synced_tasks"), set):
            save_state["synced_tasks"] = list(save_state["synced_tasks"])
        
        with open(self.sync_state_file, 'w', encoding='utf-8') as f:
            json.dump(save_state, f, indent=2, ensure_ascii=False)
    
    def sync_notion_to_calendar(self, status_filter: str = None) -> Dict:
        """
        Sincroniza tarefas do Notion para o Google Calendar
        
        Args:
            status_filter: Filtrar tarefas por status (ex: "A Fazer")
            
        Returns:
            Estatísticas da sincronização
        """
        print("\n" + "="*60)
        print("🔄 SINCRONIZAÇÃO: Notion → Google Calendar")
        print("="*60)
        
        stats = {
            "total_tasks": 0,
            "created": 0,
            "updated": 0,
            "skipped": 0,
            "errors": 0
        }
        
        # Buscar tarefas do Notion
        print("\n📋 Buscando tarefas do Notion...")
        tasks = self.notion.get_tasks(filter_status=status_filter)
        stats["total_tasks"] = len(tasks)
        
        print(f"✅ Encontradas {len(tasks)} tarefas")
        
        # Processar cada tarefa
        for i, task in enumerate(tasks, 1):
            print(f"\n[{i}/{len(tasks)}] 🔄 Processando: {task['title']}")
            
            try:
                task_id = task['id']
                
                # Verificar se já existe evento
                event_id = self.sync_state["task_to_event"].get(task_id)
                
                if not event_id:
                    # Buscar no calendário
                    event_id = self.calendar.find_event_by_notion_id(task_id)
                
                if event_id:
                    # Atualizar evento existente
                    if self.calendar.update_event(event_id, task):
                        stats["updated"] += 1
                        self.sync_state["task_to_event"][task_id] = event_id
                    else:
                        stats["errors"] += 1
                else:
                    # Criar novo evento
                    event_id = self.calendar.create_event(task)
                    if event_id:
                        stats["created"] += 1
                        self.sync_state["task_to_event"][task_id] = event_id
                    else:
                        stats["errors"] += 1
                
            except Exception as e:
                print(f"❌ Erro ao processar tarefa: {e}")
                stats["errors"] += 1
        
        # Atualizar estado
        self.sync_state["last_sync"] = datetime.now().isoformat()
        self._save_sync_state()
        
        # Mostrar estatísticas
        print("\n" + "="*60)
        print("📊 ESTATÍSTICAS DA SINCRONIZAÇÃO")
        print("="*60)
        print(f"📋 Total de tarefas: {stats['total_tasks']}")
        print(f"✅ Eventos criados: {stats['created']}")
        print(f"🔄 Eventos atualizados: {stats['updated']}")
        print(f"⏭️  Ignorados: {stats['skipped']}")
        print(f"❌ Erros: {stats['errors']}")
        print("="*60)
        
        return stats
    
    def sync_specific_tasks(self, task_ids: List[str]) -> Dict:
        """
        Sincroniza tarefas específicas
        
        Args:
            task_ids: Lista de IDs de tarefas do Notion
            
        Returns:
            Estatísticas
        """
        print(f"\n🔄 Sincronizando {len(task_ids)} tarefas específicas...")
        
        stats = {
            "total_tasks": len(task_ids),
            "created": 0,
            "updated": 0,
            "errors": 0
        }
        
        for task_id in task_ids:
            try:
                # Buscar tarefa
                task = self.notion.get_task_by_id(task_id)
                if not task:
                    stats["errors"] += 1
                    continue
                
                # Verificar se já existe evento
                event_id = self.sync_state["task_to_event"].get(task_id)
                
                if event_id:
                    # Atualizar
                    if self.calendar.update_event(event_id, task):
                        stats["updated"] += 1
                    else:
                        stats["errors"] += 1
                else:
                    # Criar
                    event_id = self.calendar.create_event(task)
                    if event_id:
                        stats["created"] += 1
                        self.sync_state["task_to_event"][task_id] = event_id
                    else:
                        stats["errors"] += 1
                        
            except Exception as e:
                print(f"❌ Erro: {e}")
                stats["errors"] += 1
        
        self._save_sync_state()
        return stats
    
    def remove_completed_events(self):
        """Remove eventos do calendário para tarefas concluídas"""
        print("\n🗑️ Removendo eventos de tarefas concluídas...")
        
        removed = 0
        
        # Buscar tarefas concluídas
        completed_tasks = self.notion.get_tasks(filter_status="Concluído")
        
        for task in completed_tasks:
            task_id = task['id']
            event_id = self.sync_state["task_to_event"].get(task_id)
            
            if event_id:
                if self.calendar.delete_event(event_id):
                    removed += 1
                    # Remover do mapeamento
                    del self.sync_state["task_to_event"][task_id]
        
        if removed > 0:
            self._save_sync_state()
            print(f"✅ Removidos {removed} eventos")
        else:
            print("ℹ️ Nenhum evento para remover")
    
    def get_sync_info(self) -> Dict:
        """Retorna informações sobre o estado da sincronização"""
        return {
            "last_sync": self.sync_state.get("last_sync"),
            "total_synced": len(self.sync_state.get("task_to_event", {})),
            "mappings": self.sync_state.get("task_to_event", {})
        }
    
    def auto_sync_loop(self, interval_minutes: int = 15, run_once: bool = False):
        """
        Loop de sincronização automática
        
        Args:
            interval_minutes: Intervalo entre sincronizações
            run_once: Se True, executa apenas uma vez
        """
        print(f"\n🤖 Modo de sincronização automática")
        print(f"⏰ Intervalo: {interval_minutes} minutos")
        print(f"🔄 Pressione Ctrl+C para parar\n")
        
        try:
            while True:
                try:
                    # Sincronizar tarefas "A Fazer" e "Em Progresso"
                    for status in ["A Fazer", "Em Progresso"]:
                        self.sync_notion_to_calendar(status_filter=status)
                    
                    # Remover eventos concluídos
                    self.remove_completed_events()
                    
                    if run_once:
                        break
                    
                    # Aguardar próximo ciclo
                    print(f"\n💤 Aguardando {interval_minutes} minutos até próxima sincronização...")
                    time.sleep(interval_minutes * 60)
                    
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(f"\n❌ Erro na sincronização: {e}")
                    print(f"⏰ Tentando novamente em {interval_minutes} minutos...")
                    time.sleep(interval_minutes * 60)
                    
        except KeyboardInterrupt:
            print("\n\n⏹️ Sincronização interrompida pelo usuário")
            print("✅ Estado salvo com sucesso")


def test_sync():
    """Função de teste"""
    from dotenv import load_dotenv
    load_dotenv()
    
    # Inicializar clientes
    notion = NotionTaskClient(
        api_key=os.getenv("NOTION_API_KEY"),
        database_id=os.getenv("NOTION_DATABASE_ID")
    )
    
    calendar = GoogleCalendarClient(
        calendar_id=os.getenv("GOOGLE_CALENDAR_ID", "primary")
    )
    
    # Criar gerenciador
    manager = SyncManager(notion, calendar)
    
    # Executar sincronização
    manager.sync_notion_to_calendar()
    
    # Mostrar info
    info = manager.get_sync_info()
    print(f"\nℹ️ Última sincronização: {info['last_sync']}")
    print(f"📊 Total sincronizado: {info['total_synced']} tarefas")


if __name__ == "__main__":
    test_sync()
