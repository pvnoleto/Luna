"""
Cliente Google Calendar - TeleNordeste Integration
Gerencia eventos no Google Calendar
"""

import os
import pickle
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime, timedelta
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GoogleCalendarClient:
    """Cliente para interação com Google Calendar API"""
    
    # Se modificar escopos, delete token.json para re-autenticar
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    def __init__(self, credentials_file: Path, token_file: Path, 
                 calendar_id: str = "primary", timezone: str = "America/Fortaleza"):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.calendar_id = calendar_id
        self.timezone = timezone
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Autentica com Google Calendar API"""
        creds = None
        
        # Token salvo de sessão anterior
        if self.token_file.exists():
            try:
                with open(self.token_file, 'rb') as token:
                    creds = pickle.load(token)
            except Exception as e:
                logger.warning(f"⚠️ Erro ao carregar token: {e}")
        
        # Se não há credenciais válidas, autenticar
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    logger.info("🔄 Token renovado com sucesso")
                except Exception as e:
                    logger.error(f"❌ Erro ao renovar token: {e}")
                    creds = None
            
            if not creds:
                if not self.credentials_file.exists():
                    raise FileNotFoundError(
                        f"Arquivo de credenciais não encontrado: {self.credentials_file}\n"
                        "Baixe em: https://console.cloud.google.com/apis/credentials"
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_file), self.SCOPES
                )
                creds = flow.run_local_server(port=0)
                logger.info("✅ Autenticação realizada com sucesso")
            
            # Salvar credenciais para próxima vez
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        try:
            self.service = build('calendar', 'v3', credentials=creds)
            logger.info("✅ Serviço Google Calendar inicializado")
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar serviço: {e}")
            raise
    
    def create_event(self, summary: str, start_time: datetime, 
                    end_time: Optional[datetime] = None,
                    description: str = "", location: str = "",
                    attendees: List[str] = None) -> Optional[str]:
        """
        Cria evento no Google Calendar
        
        Args:
            summary: Título do evento
            start_time: Data/hora de início
            end_time: Data/hora de fim (opcional, padrão 1h depois)
            description: Descrição do evento
            location: Local do evento
            attendees: Lista de emails dos participantes
        
        Returns:
            ID do evento criado ou None em caso de erro
        """
        if not end_time:
            end_time = start_time + timedelta(hours=1)
        
        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': self.timezone,
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': self.timezone,
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 30},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        
        if attendees:
            event['attendees'] = [{'email': email} for email in attendees]
        
        try:
            event = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event
            ).execute()
            
            event_id = event.get('id')
            event_link = event.get('htmlLink')
            logger.info(f"✅ Evento criado: {summary}")
            logger.info(f"🔗 Link: {event_link}")
            return event_id
        
        except HttpError as error:
            logger.error(f"❌ Erro ao criar evento: {error}")
            return None
    
    def get_events(self, time_min: Optional[datetime] = None,
                   time_max: Optional[datetime] = None,
                   max_results: int = 100) -> List[Dict]:
        """
        Busca eventos do calendário
        
        Args:
            time_min: Data/hora mínima (padrão: agora)
            time_max: Data/hora máxima (opcional)
            max_results: Número máximo de resultados
        
        Returns:
            Lista de eventos
        """
        if not time_min:
            time_min = datetime.now()
        
        try:
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=time_min.isoformat() + 'Z',
                timeMax=time_max.isoformat() + 'Z' if time_max else None,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            logger.info(f"📅 {len(events)} eventos encontrados")
            return events
        
        except HttpError as error:
            logger.error(f"❌ Erro ao buscar eventos: {error}")
            return []
    
    def update_event(self, event_id: str, updates: Dict) -> bool:
        """
        Atualiza um evento existente
        
        Args:
            event_id: ID do evento
            updates: Dicionário com campos a atualizar
        
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            # Buscar evento atual
            event = self.service.events().get(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()
            
            # Aplicar atualizações
            event.update(updates)
            
            # Atualizar evento
            updated_event = self.service.events().update(
                calendarId=self.calendar_id,
                eventId=event_id,
                body=event
            ).execute()
            
            logger.info(f"✅ Evento atualizado: {event_id}")
            return True
        
        except HttpError as error:
            logger.error(f"❌ Erro ao atualizar evento: {error}")
            return False
    
    def delete_event(self, event_id: str) -> bool:
        """
        Deleta um evento
        
        Args:
            event_id: ID do evento
        
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            self.service.events().delete(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()
            
            logger.info(f"🗑️ Evento deletado: {event_id}")
            return True
        
        except HttpError as error:
            logger.error(f"❌ Erro ao deletar evento: {error}")
            return False
    
    def find_event_by_summary(self, summary: str, 
                             time_min: Optional[datetime] = None) -> Optional[Dict]:
        """
        Busca evento por título
        
        Args:
            summary: Título do evento a buscar
            time_min: Data mínima (padrão: agora)
        
        Returns:
            Evento encontrado ou None
        """
        events = self.get_events(time_min=time_min)
        
        for event in events:
            if event.get('summary', '').lower() == summary.lower():
                return event
        
        return None
    
    def test_connection(self) -> bool:
        """Testa conexão com Google Calendar"""
        try:
            calendar = self.service.calendars().get(
                calendarId=self.calendar_id
            ).execute()
            
            calendar_name = calendar.get('summary', 'Sem nome')
            logger.info(f"✅ Conexão com Google Calendar OK - Calendário: {calendar_name}")
            return True
        
        except HttpError as error:
            logger.error(f"❌ Erro ao conectar com Google Calendar: {error}")
            return False


if __name__ == "__main__":
    print("🧪 Teste do GoogleCalendarClient")
    print("Configure as credenciais em config.json para testar")
