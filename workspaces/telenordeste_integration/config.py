"""
Gerenciador de Configurações - TeleNordeste Integration
Gerencia credenciais e configurações de forma segura
"""

import os
import json
from pathlib import Path
from typing import Dict, Optional

class ConfigManager:
    """Gerencia configurações e credenciais da integração"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(__file__).parent / config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Carrega configurações do arquivo"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._create_default_config()
    
    def _create_default_config(self) -> Dict:
        """Cria configuração padrão"""
        config = {
            "notion": {
                "api_token": "",
                "database_id": "",
                "filter_property": "Status",
                "filter_value": "A Fazer"
            },
            "google_calendar": {
                "calendar_id": "primary",
                "credentials_file": "credentials.json",
                "token_file": "token.json"
            },
            "sync": {
                "auto_sync_interval": 3600,  # 1 hora em segundos
                "timezone": "America/Fortaleza",
                "default_duration": 60  # minutos
            },
            "mapping": {
                "title_field": "Name",
                "date_field": "Data",
                "description_field": "Descrição",
                "duration_field": "Duração"
            }
        }
        self.save_config(config)
        return config
    
    def save_config(self, config: Optional[Dict] = None):
        """Salva configurações no arquivo"""
        if config:
            self.config = config
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def get_notion_token(self) -> str:
        """Retorna token do Notion"""
        return self.config.get("notion", {}).get("api_token", "")
    
    def get_notion_database_id(self) -> str:
        """Retorna ID do database do Notion"""
        return self.config.get("notion", {}).get("database_id", "")
    
    def get_calendar_id(self) -> str:
        """Retorna ID do Google Calendar"""
        return self.config.get("google_calendar", {}).get("calendar_id", "primary")
    
    def get_credentials_file(self) -> Path:
        """Retorna caminho do arquivo de credenciais do Google"""
        filename = self.config.get("google_calendar", {}).get("credentials_file", "credentials.json")
        return Path(__file__).parent / filename
    
    def get_token_file(self) -> Path:
        """Retorna caminho do arquivo de token do Google"""
        filename = self.config.get("google_calendar", {}).get("token_file", "token.json")
        return Path(__file__).parent / filename
    
    def get_timezone(self) -> str:
        """Retorna timezone configurado"""
        return self.config.get("sync", {}).get("timezone", "America/Fortaleza")
    
    def get_mapping(self) -> Dict:
        """Retorna mapeamento de campos"""
        return self.config.get("mapping", {})
    
    def set_notion_credentials(self, api_token: str, database_id: str):
        """Define credenciais do Notion"""
        if "notion" not in self.config:
            self.config["notion"] = {}
        
        self.config["notion"]["api_token"] = api_token
        self.config["notion"]["database_id"] = database_id
        self.save_config()
    
    def validate_config(self) -> tuple[bool, list[str]]:
        """Valida se todas as configurações necessárias estão presentes"""
        errors = []
        
        # Validar Notion
        if not self.get_notion_token():
            errors.append("❌ Notion API Token não configurado")
        
        if not self.get_notion_database_id():
            errors.append("❌ Notion Database ID não configurado")
        
        # Validar Google Calendar
        if not self.get_credentials_file().exists():
            errors.append(f"❌ Arquivo de credenciais do Google não encontrado: {self.get_credentials_file()}")
        
        return len(errors) == 0, errors


if __name__ == "__main__":
    # Teste
    config = ConfigManager()
    is_valid, errors = config.validate_config()
    
    if is_valid:
        print("✅ Configuração válida!")
    else:
        print("⚠️ Erros na configuração:")
        for error in errors:
            print(f"  {error}")
