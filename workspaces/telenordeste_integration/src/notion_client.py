"""
Cliente para integração com Notion API
Busca tarefas de um database específico
"""

import os
from typing import List, Dict, Optional
from datetime import datetime
from notion_client import Client
import pytz


class NotionTaskClient:
    """Cliente para buscar e gerenciar tarefas do Notion"""
    
    def __init__(self, api_key: str, database_id: str, timezone: str = "America/Fortaleza"):
        """
        Inicializa o cliente Notion
        
        Args:
            api_key: Token de API do Notion
            database_id: ID do database de tarefas
            timezone: Fuso horário para datas
        """
        self.client = Client(auth=api_key)
        self.database_id = database_id
        self.timezone = pytz.timezone(timezone)
        
    def get_tasks(self, filter_status: Optional[str] = None) -> List[Dict]:
        """
        Busca tarefas do database
        
        Args:
            filter_status: Filtrar por status (ex: "A Fazer", "Em Progresso")
            
        Returns:
            Lista de tarefas formatadas
        """
        try:
            # Construir filtro
            filter_params = {}
            if filter_status:
                filter_params = {
                    "property": "Status",
                    "select": {
                        "equals": filter_status
                    }
                }
            
            # Buscar páginas do database
            response = self.client.databases.query(
                database_id=self.database_id,
                filter=filter_params if filter_status else None
            )
            
            tasks = []
            for page in response.get("results", []):
                task = self._format_task(page)
                if task:
                    tasks.append(task)
            
            return tasks
            
        except Exception as e:
            print(f"❌ Erro ao buscar tarefas do Notion: {e}")
            return []
    
    def _format_task(self, page: Dict) -> Optional[Dict]:
        """
        Formata uma página do Notion como tarefa
        
        Args:
            page: Página do Notion
            
        Returns:
            Tarefa formatada ou None
        """
        try:
            properties = page.get("properties", {})
            
            # Extrair informações
            task_id = page.get("id")
            
            # Nome da tarefa
            title_prop = properties.get("Name") or properties.get("Título") or properties.get("Title")
            if not title_prop:
                return None
                
            title_list = title_prop.get("title", [])
            title = title_list[0].get("plain_text", "Sem título") if title_list else "Sem título"
            
            # Status
            status_prop = properties.get("Status")
            status = status_prop.get("select", {}).get("name", "Sem status") if status_prop else "Sem status"
            
            # Data
            date_prop = properties.get("Data") or properties.get("Date") or properties.get("Prazo")
            date_start = None
            date_end = None
            
            if date_prop and date_prop.get("date"):
                date_info = date_prop.get("date")
                date_start = date_info.get("start")
                date_end = date_info.get("end")
            
            # Descrição
            description = self._get_description(page)
            
            # Prioridade
            priority_prop = properties.get("Prioridade") or properties.get("Priority")
            priority = priority_prop.get("select", {}).get("name", "Média") if priority_prop else "Média"
            
            # Responsável
            assignee_prop = properties.get("Responsável") or properties.get("Assignee")
            assignee = None
            if assignee_prop and assignee_prop.get("people"):
                people = assignee_prop.get("people", [])
                if people:
                    assignee = people[0].get("name", "Não atribuído")
            
            return {
                "id": task_id,
                "title": title,
                "status": status,
                "date_start": date_start,
                "date_end": date_end,
                "description": description,
                "priority": priority,
                "assignee": assignee,
                "url": page.get("url"),
                "last_edited": page.get("last_edited_time")
            }
            
        except Exception as e:
            print(f"⚠️ Erro ao formatar tarefa: {e}")
            return None
    
    def _get_description(self, page: Dict) -> str:
        """Extrai descrição do conteúdo da página"""
        try:
            # Buscar conteúdo da página
            blocks = self.client.blocks.children.list(block_id=page["id"])
            
            description_parts = []
            for block in blocks.get("results", [])[:3]:  # Primeiros 3 blocos
                if block.get("type") == "paragraph":
                    text_list = block.get("paragraph", {}).get("rich_text", [])
                    for text in text_list:
                        description_parts.append(text.get("plain_text", ""))
            
            return " ".join(description_parts)[:500]  # Limitar a 500 caracteres
            
        except:
            return ""
    
    def update_task_status(self, task_id: str, status: str) -> bool:
        """
        Atualiza o status de uma tarefa
        
        Args:
            task_id: ID da tarefa
            status: Novo status
            
        Returns:
            True se sucesso
        """
        try:
            self.client.pages.update(
                page_id=task_id,
                properties={
                    "Status": {
                        "select": {
                            "name": status
                        }
                    }
                }
            )
            return True
        except Exception as e:
            print(f"❌ Erro ao atualizar status: {e}")
            return False
    
    def get_task_by_id(self, task_id: str) -> Optional[Dict]:
        """
        Busca uma tarefa específica por ID
        
        Args:
            task_id: ID da tarefa
            
        Returns:
            Tarefa formatada ou None
        """
        try:
            page = self.client.pages.retrieve(page_id=task_id)
            return self._format_task(page)
        except Exception as e:
            print(f"❌ Erro ao buscar tarefa {task_id}: {e}")
            return None


if __name__ == "__main__":
    # Teste do cliente
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("NOTION_API_KEY")
    database_id = os.getenv("NOTION_DATABASE_ID")
    
    if api_key and database_id:
        client = NotionTaskClient(api_key, database_id)
        print("🔍 Buscando tarefas do Notion...")
        tasks = client.get_tasks()
        print(f"✅ Encontradas {len(tasks)} tarefas")
        
        for task in tasks[:3]:  # Mostrar primeiras 3
            print(f"\n📋 {task['title']}")
            print(f"   Status: {task['status']}")
            print(f"   Data: {task['date_start']}")
            print(f"   Prioridade: {task['priority']}")
    else:
        print("⚠️ Configure NOTION_API_KEY e NOTION_DATABASE_ID no .env")
