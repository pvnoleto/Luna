"""
Cliente para integração com Google Calendar API
Cria e gerencia eventos baseados em tarefas
"""

import os
import pickle
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pytz


# Se modificar estes escopos, delete o arquivo token.pickle
SCOPES = ['https://www.googleapis.com/auth/calendar']


class GoogleCalendarClient:
    """Cliente para criar e gerenciar eventos no Google Calendar"""
    
    def __init__(self, credentials_path: str = "config/credentials.json", 
                 calendar_id: str = "primary",
                 timezone: str = "America/Fortaleza"):
        """
        Inicializa o cliente Google Calendar
        
        Args:
            credentials_path: Caminho para credentials.json
            calendar_id: ID do calendário (default: primary)
            timezone: Fuso horário
        """
        self.credentials_path = credentials_path
        self.calendar_id = calendar_id
        self.timezone = pytz.timezone(timezone)
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Autentica com Google OAuth2"""
        creds = None
        token_path = "config/token.pickle"
        
        # Carregar token salvo
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # Se não há credenciais válidas, fazer login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"⚠️ Erro ao renovar token: {e}")
                    creds = None
            
            if not creds:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"Arquivo de credenciais não encontrado: {self.credentials_path}\n"
                        "Baixe em: https://console.cloud.google.com/apis/credentials"
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Salvar token
            os.makedirs("config", exist_ok=True)
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('calendar', 'v3', credentials=creds)
        print("✅ Autenticado com Google Calendar")
    
    def create_event(self, task: Dict) -> Optional[str]:
        """
        Cria evento no calendário baseado em uma tarefa
        
        Args:
            task: Dicionário com dados da tarefa
            
        Returns:
            ID do evento criado ou None
        """
        try:
            # Preparar datas
            start_datetime = self._parse_date(task.get("date_start"))
            end_datetime = self._parse_date(task.get("date_end"))
            
            if not start_datetime:
                # Se não tem data, agendar para amanhã às 9h
                start_datetime = datetime.now(self.timezone) + timedelta(days=1)
                start_datetime = start_datetime.replace(hour=9, minute=0, second=0, microsecond=0)
            
            if not end_datetime:
                # Duração padrão de 1 hora
                end_datetime = start_datetime + timedelta(hours=1)
            
            # Montar descrição
            description_parts = []
            
            if task.get("description"):
                description_parts.append(task["description"])
            
            description_parts.append(f"\n📊 Status: {task.get('status', 'N/A')}")
            description_parts.append(f"🎯 Prioridade: {task.get('priority', 'Média')}")
            
            if task.get("assignee"):
                description_parts.append(f"👤 Responsável: {task['assignee']}")
            
            if task.get("url"):
                description_parts.append(f"\n🔗 Ver no Notion: {task['url']}")
            
            description = "\n".join(description_parts)
            
            # Definir cor baseada na prioridade
            color_map = {
                "Alta": "11",  # Vermelho
                "Média": "9",  # Azul
                "Baixa": "2"   # Verde
            }
            color_id = color_map.get(task.get("priority", "Média"), "9")
            
            # Criar evento
            event = {
                'summary': f"📋 {task['title']}",
                'description': description,
                'start': {
                    'dateTime': start_datetime.isoformat(),
                    'timeZone': str(self.timezone),
                },
                'end': {
                    'dateTime': end_datetime.isoformat(),
                    'timeZone': str(self.timezone),
                },
                'colorId': color_id,
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 30},
                        {'method': 'email', 'minutes': 60},
                    ],
                },
                'extendedProperties': {
                    'private': {
                        'notionTaskId': task['id'],
                        'notionStatus': task.get('status', ''),
                    }
                }
            }
            
            # Inserir evento
            result = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event
            ).execute()
            
            event_id = result.get('id')
            event_link = result.get('htmlLink')
            
            print(f"✅ Evento criado: {task['title']}")
            print(f"   🔗 {event_link}")
            
            return event_id
            
        except Exception as e:
            print(f"❌ Erro ao criar evento: {e}")
            return None
    
    def update_event(self, event_id: str, task: Dict) -> bool:
        """
        Atualiza um evento existente
        
        Args:
            event_id: ID do evento no Google Calendar
            task: Dados atualizados da tarefa
            
        Returns:
            True se sucesso
        """
        try:
            # Buscar evento atual
            event = self.service.events().get(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()
            
            # Atualizar campos
            event['summary'] = f"📋 {task['title']}"
            
            # Atualizar descrição
            description_parts = []
            if task.get("description"):
                description_parts.append(task["description"])
            description_parts.append(f"\n📊 Status: {task.get('status', 'N/A')}")
            description_parts.append(f"🎯 Prioridade: {task.get('priority', 'Média')}")
            if task.get("assignee"):
                description_parts.append(f"👤 Responsável: {task['assignee']}")
            if task.get("url"):
                description_parts.append(f"\n🔗 Ver no Notion: {task['url']}")
            
            event['description'] = "\n".join(description_parts)
            
            # Atualizar propriedades estendidas
            if 'extendedProperties' not in event:
                event['extendedProperties'] = {'private': {}}
            event['extendedProperties']['private']['notionStatus'] = task.get('status', '')
            
            # Atualizar evento
            self.service.events().update(
                calendarId=self.calendar_id,
                eventId=event_id,
                body=event
            ).execute()
            
            print(f"✅ Evento atualizado: {task['title']}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao atualizar evento: {e}")
            return False
    
    def delete_event(self, event_id: str) -> bool:
        """
        Remove um evento do calendário
        
        Args:
            event_id: ID do evento
            
        Returns:
            True se sucesso
        """
        try:
            self.service.events().delete(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()
            print(f"✅ Evento removido: {event_id}")
            return True
        except Exception as e:
            print(f"❌ Erro ao remover evento: {e}")
            return False
    
    def find_event_by_notion_id(self, notion_task_id: str) -> Optional[str]:
        """
        Busca evento no calendário pelo ID da tarefa do Notion
        
        Args:
            notion_task_id: ID da tarefa no Notion
            
        Returns:
            ID do evento no Google Calendar ou None
        """
        try:
            # Buscar eventos dos próximos 30 dias
            now = datetime.now(self.timezone).isoformat()
            later = (datetime.now(self.timezone) + timedelta(days=30)).isoformat()
            
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=now,
                timeMax=later,
                maxResults=100,
                singleEvents=True,
                orderBy='startTime',
                privateExtendedProperty=f'notionTaskId={notion_task_id}'
            ).execute()
            
            events = events_result.get('items', [])
            
            if events:
                return events[0].get('id')
            
            return None
            
        except Exception as e:
            print(f"❌ Erro ao buscar evento: {e}")
            return None
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """
        Converte string de data para datetime
        
        Args:
            date_str: String de data ISO
            
        Returns:
            Objeto datetime ou None
        """
        if not date_str:
            return None
        
        try:
            # Parse ISO format
            if 'T' in date_str:
                dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                # Data sem hora - definir 9h
                dt = datetime.fromisoformat(date_str)
                dt = dt.replace(hour=9, minute=0, second=0)
            
            # Converter para timezone local
            if dt.tzinfo is None:
                dt = self.timezone.localize(dt)
            else:
                dt = dt.astimezone(self.timezone)
            
            return dt
            
        except Exception as e:
            print(f"⚠️ Erro ao parsear data {date_str}: {e}")
            return None
    
    def list_upcoming_events(self, max_results: int = 10) -> List[Dict]:
        """
        Lista próximos eventos do calendário
        
        Args:
            max_results: Número máximo de eventos
            
        Returns:
            Lista de eventos
        """
        try:
            now = datetime.now(self.timezone).isoformat()
            
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            return events
            
        except Exception as e:
            print(f"❌ Erro ao listar eventos: {e}")
            return []


if __name__ == "__main__":
    # Teste do cliente
    client = GoogleCalendarClient()
    
    print("\n📅 Próximos eventos:")
    events = client.list_upcoming_events(5)
    
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"  • {event['summary']} - {start}")
