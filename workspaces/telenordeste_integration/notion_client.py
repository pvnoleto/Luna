"""
Cliente Notion - TeleNordeste Integration
Busca e gerencia tarefas do Notion
"""

import requests
from typing import List, Dict, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotionClient:
    """Cliente para interação com a API do Notion"""
    
    BASE_URL = "https://api.notion.com/v1"
    API_VERSION = "2022-06-28"
    
    def __init__(self, api_token: str, database_id: str):
        self.api_token = api_token
        self.database_id = database_id
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Notion-Version": self.API_VERSION,
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict]:
        """Faz requisição à API do Notion"""
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição ao Notion: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Resposta: {e.response.text}")
            return None
    
    def query_database(self, filter_dict: Optional[Dict] = None) -> List[Dict]:
        """
        Consulta database do Notion com filtros
        
        Args:
            filter_dict: Filtro para a query (opcional)
        
        Returns:
            Lista de páginas (tarefas) encontradas
        """
        payload = {}
        if filter_dict:
            payload["filter"] = filter_dict
        
        response = self._make_request(
            "POST",
            f"databases/{self.database_id}/query",
            json=payload
        )
        
        if response:
            return response.get("results", [])
        return []
    
    def get_pending_tasks(self, status_property: str = "Status", 
                         status_value: str = "A Fazer") -> List[Dict]:
        """
        Busca tarefas com status específico
        
        Args:
            status_property: Nome da propriedade de status
            status_value: Valor do status a buscar
        
        Returns:
            Lista de tarefas pendentes
        """
        filter_dict = {
            "property": status_property,
            "select": {
                "equals": status_value
            }
        }
        
        tasks = self.query_database(filter_dict)
        logger.info(f"📥 {len(tasks)} tarefas encontradas com status '{status_value}'")
        return tasks
    
    def get_tasks_by_date(self, date_property: str = "Data", 
                         start_date: Optional[datetime] = None,
                         end_date: Optional[datetime] = None) -> List[Dict]:
        """
        Busca tarefas por intervalo de datas
        
        Args:
            date_property: Nome da propriedade de data
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
        
        Returns:
            Lista de tarefas no intervalo
        """
        filter_dict = {
            "property": date_property,
            "date": {}
        }
        
        if start_date:
            filter_dict["date"]["on_or_after"] = start_date.isoformat()
        
        if end_date:
            filter_dict["date"]["on_or_before"] = end_date.isoformat()
        
        tasks = self.query_database(filter_dict)
        logger.info(f"📅 {len(tasks)} tarefas encontradas no período")
        return tasks
    
    def extract_task_data(self, page: Dict, mapping: Dict) -> Dict:
        """
        Extrai dados relevantes de uma página do Notion
        
        Args:
            page: Objeto page do Notion
            mapping: Mapeamento de campos
        
        Returns:
            Dicionário com dados estruturados da tarefa
        """
        properties = page.get("properties", {})
        
        task_data = {
            "id": page.get("id"),
            "url": page.get("url"),
            "created_time": page.get("created_time"),
            "last_edited_time": page.get("last_edited_time"),
        }
        
        # Extrair título
        title_field = mapping.get("title_field", "Name")
        if title_field in properties:
            title_prop = properties[title_field]
            if title_prop.get("type") == "title":
                title_array = title_prop.get("title", [])
                task_data["title"] = "".join([t.get("plain_text", "") for t in title_array])
        
        # Extrair data
        date_field = mapping.get("date_field", "Data")
        if date_field in properties:
            date_prop = properties[date_field]
            if date_prop.get("type") == "date":
                date_obj = date_prop.get("date")
                if date_obj:
                    task_data["start_date"] = date_obj.get("start")
                    task_data["end_date"] = date_obj.get("end")
        
        # Extrair descrição
        desc_field = mapping.get("description_field", "Descrição")
        if desc_field in properties:
            desc_prop = properties[desc_field]
            if desc_prop.get("type") == "rich_text":
                desc_array = desc_prop.get("rich_text", [])
                task_data["description"] = "".join([t.get("plain_text", "") for t in desc_array])
        
        # Extrair duração
        duration_field = mapping.get("duration_field", "Duração")
        if duration_field in properties:
            duration_prop = properties[duration_field]
            if duration_prop.get("type") == "number":
                task_data["duration"] = duration_prop.get("number")
        
        # Extrair status
        if "Status" in properties:
            status_prop = properties["Status"]
            if status_prop.get("type") == "select":
                status_obj = status_prop.get("select")
                if status_obj:
                    task_data["status"] = status_obj.get("name")
        
        return task_data
    
    def update_task_status(self, page_id: str, status_property: str, 
                          new_status: str) -> bool:
        """
        Atualiza o status de uma tarefa
        
        Args:
            page_id: ID da página/tarefa
            status_property: Nome da propriedade de status
            new_status: Novo valor do status
        
        Returns:
            True se sucesso, False caso contrário
        """
        payload = {
            "properties": {
                status_property: {
                    "select": {
                        "name": new_status
                    }
                }
            }
        }
        
        response = self._make_request(
            "PATCH",
            f"pages/{page_id}",
            json=payload
        )
        
        if response:
            logger.info(f"✅ Status atualizado para '{new_status}'")
            return True
        
        logger.error(f"❌ Falha ao atualizar status")
        return False
    
    def test_connection(self) -> bool:
        """Testa conexão com o Notion"""
        try:
            response = self._make_request("GET", f"databases/{self.database_id}")
            if response:
                db_title = response.get("title", [{}])[0].get("plain_text", "Sem título")
                logger.info(f"✅ Conexão com Notion OK - Database: {db_title}")
                return True
        except Exception as e:
            logger.error(f"❌ Erro ao conectar com Notion: {e}")
        
        return False


if __name__ == "__main__":
    # Teste básico
    print("🧪 Teste do NotionClient")
    print("Configure as credenciais em config.json para testar")
