#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📧 INTEGRAÇÃO COM GOOGLE (GMAIL + CALENDAR) - LUNA
===================================================

Integração direta com Gmail e Google Calendar usando APIs oficiais do Google.
Permite acesso rápido e eficiente sem precisar de navegador.

Funcionalidades Gmail:
- Conectar via OAuth2 ou Service Account
- Listar emails com filtros (remetente, assunto, data, etc.)
- Ler conteúdo completo de emails
- Enviar emails (texto e HTML)
- Marcar como lido/não lido
- Deletar e arquivar emails
- Buscar com query do Gmail

Funcionalidades Google Calendar:
- Conectar via OAuth2 ou Service Account
- Listar eventos com filtros
- Criar eventos (simples e recorrentes)
- Atualizar eventos existentes
- Deletar eventos
- Buscar eventos por texto

Segurança:
- Credenciais OAuth2 armazenadas no cofre de credenciais
- Suporte a múltiplas contas Google
- Tokens de acesso renovados automaticamente

Instalação:
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

Autor: Sistema Luna
Data: 2025-10-19
"""

from typing import Dict, List, Optional, Any, Tuple
import json
import base64
import os
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Tentar importar SDKs do Google
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_DISPONIVEL = True
except ImportError:
    GOOGLE_DISPONIVEL = False
    print("⚠️  Google APIs não instaladas. Execute:")
    print("   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")


# Escopos necessários para acesso completo
SCOPES_GMAIL = ['https://www.googleapis.com/auth/gmail.modify']
SCOPES_CALENDAR = ['https://www.googleapis.com/auth/calendar']


class IntegracaoGmail:
    """
    Gerenciador de integração com Gmail via API oficial do Google.

    Uso básico:
        # Primeira vez (gera arquivo de credenciais)
        gmail = IntegracaoGmail(credentials_path="credentials.json")

        # Sessões seguintes (usa token salvo)
        gmail = IntegracaoGmail(token_path="token_gmail.json")

        # Listar emails não lidos
        emails = gmail.listar_emails(max_results=10, apenas_nao_lidos=True)

        # Enviar email
        gmail.enviar_email(
            destinatario="exemplo@gmail.com",
            assunto="Teste",
            corpo="Olá do Luna!"
        )
    """

    def __init__(
        self,
        credentials_path: Optional[str] = None,
        token_path: str = "token_gmail.json",
        credentials_dict: Optional[Dict] = None
    ):
        """
        Inicializa a integração com Gmail.

        Args:
            credentials_path: Caminho para arquivo credentials.json do Google Cloud
            token_path: Caminho onde salvar/carregar token de acesso
            credentials_dict: Credenciais em formato dict (alternativa a credentials_path)

        Raises:
            ValueError: Se bibliotecas do Google não estiverem instaladas
            Exception: Se autenticação falhar
        """
        if not GOOGLE_DISPONIVEL:
            raise ValueError(
                "Bibliotecas do Google não instaladas. Execute:\n"
                "pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client"
            )

        self.token_path = token_path
        self.credentials_path = credentials_path
        self.credentials_dict = credentials_dict
        self.service = None
        self._conectar()

    def _conectar(self) -> None:
        """Conecta ao Gmail usando OAuth2."""
        try:
            creds = None

            # Tentar carregar token existente
            if os.path.exists(self.token_path):
                creds = Credentials.from_authorized_user_file(self.token_path, SCOPES_GMAIL)

            # Se não houver credenciais válidas, fazer login
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    # Renovar token expirado
                    creds.refresh(Request())
                else:
                    # Fazer login pela primeira vez
                    if self.credentials_dict:
                        # Usar credenciais do dict
                        flow = InstalledAppFlow.from_client_config(
                            self.credentials_dict,
                            SCOPES_GMAIL
                        )
                    elif self.credentials_path:
                        # Usar credenciais do arquivo
                        flow = InstalledAppFlow.from_client_secrets_file(
                            self.credentials_path,
                            SCOPES_GMAIL
                        )
                    else:
                        raise ValueError("É necessário fornecer credentials_path ou credentials_dict")

                    creds = flow.run_local_server(port=0)

                # Salvar credenciais para próxima vez
                with open(self.token_path, 'w', encoding='utf-8') as token:
                    token.write(creds.to_json())

            # Criar serviço Gmail
            self.service = build('gmail', 'v1', credentials=creds)

            # Testar conexão pegando perfil do usuário
            profile = self.service.users().getProfile(userId='me').execute()
            print(f"[OK] Conectado ao Gmail: {profile['emailAddress']}")

        except Exception as e:
            raise Exception(f"Erro ao conectar ao Gmail: {e}")

    def listar_emails(
        self,
        max_results: int = 10,
        query: str = "",
        apenas_nao_lidos: bool = False,
        remetente: Optional[str] = None,
        assunto: Optional[str] = None,
        depois_de: Optional[str] = None,
        antes_de: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Lista emails da caixa de entrada.

        Args:
            max_results: Número máximo de emails a retornar
            query: Query de busca do Gmail (formato Gmail search)
            apenas_nao_lidos: Se True, retorna apenas emails não lidos
            remetente: Filtrar por email do remetente
            assunto: Filtrar por assunto (busca parcial)
            depois_de: Data mínima no formato YYYY/MM/DD
            antes_de: Data máxima no formato YYYY/MM/DD

        Returns:
            Lista de emails com metadados básicos

        Exemplo de query:
            "from:exemplo@gmail.com subject:reunião after:2025/01/01"
        """
        try:
            # Construir query
            query_parts = []
            if query:
                query_parts.append(query)
            if apenas_nao_lidos:
                query_parts.append("is:unread")
            if remetente:
                query_parts.append(f"from:{remetente}")
            if assunto:
                query_parts.append(f"subject:{assunto}")
            if depois_de:
                query_parts.append(f"after:{depois_de}")
            if antes_de:
                query_parts.append(f"before:{antes_de}")

            query_final = " ".join(query_parts) if query_parts else None

            # Listar mensagens
            params = {
                'userId': 'me',
                'maxResults': max_results
            }
            if query_final:
                params['q'] = query_final

            results = self.service.users().messages().list(**params).execute()
            messages = results.get('messages', [])

            if not messages:
                return []

            # Buscar detalhes de cada mensagem
            emails = []
            for msg in messages:
                email_data = self._obter_email_completo(msg['id'])
                emails.append(email_data)

            return emails

        except HttpError as error:
            raise Exception(f"Erro ao listar emails: {error}")

    def _obter_email_completo(self, msg_id: str) -> Dict[str, Any]:
        """
        Obtém todos os detalhes de um email específico.

        Args:
            msg_id: ID da mensagem

        Returns:
            Dicionário com todos os dados do email
        """
        try:
            msg = self.service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()

            # Extrair headers importantes
            headers = msg['payload'].get('headers', [])
            headers_dict = {h['name']: h['value'] for h in headers}

            # Extrair corpo do email
            corpo = self._extrair_corpo(msg['payload'])

            email_data = {
                'id': msg['id'],
                'thread_id': msg['threadId'],
                'remetente': headers_dict.get('From', ''),
                'destinatario': headers_dict.get('To', ''),
                'assunto': headers_dict.get('Subject', ''),
                'data': headers_dict.get('Date', ''),
                'corpo_texto': corpo['texto'],
                'corpo_html': corpo['html'],
                'snippet': msg.get('snippet', ''),
                'labels': msg.get('labelIds', []),
                'lido': 'UNREAD' not in msg.get('labelIds', []),
                'importante': 'IMPORTANT' in msg.get('labelIds', []),
                'interno_data': msg.get('internalDate', '')
            }

            return email_data

        except HttpError as error:
            raise Exception(f"Erro ao obter email {msg_id}: {error}")

    def _extrair_corpo(self, payload: Dict) -> Dict[str, str]:
        """
        Extrai corpo de texto e HTML de um email.

        Args:
            payload: Payload da mensagem

        Returns:
            Dict com 'texto' e 'html'
        """
        corpo = {'texto': '', 'html': ''}

        if 'parts' in payload:
            # Email multipart
            for part in payload['parts']:
                mime_type = part.get('mimeType', '')

                if mime_type == 'text/plain':
                    if 'data' in part['body']:
                        corpo['texto'] = base64.urlsafe_b64decode(
                            part['body']['data']
                        ).decode('utf-8', errors='ignore')

                elif mime_type == 'text/html':
                    if 'data' in part['body']:
                        corpo['html'] = base64.urlsafe_b64decode(
                            part['body']['data']
                        ).decode('utf-8', errors='ignore')

                elif 'parts' in part:
                    # Recursivo para parts aninhadas
                    corpo_aninhado = self._extrair_corpo(part)
                    if not corpo['texto']:
                        corpo['texto'] = corpo_aninhado['texto']
                    if not corpo['html']:
                        corpo['html'] = corpo_aninhado['html']
        else:
            # Email simples
            if 'data' in payload.get('body', {}):
                data = base64.urlsafe_b64decode(
                    payload['body']['data']
                ).decode('utf-8', errors='ignore')

                if payload.get('mimeType') == 'text/html':
                    corpo['html'] = data
                else:
                    corpo['texto'] = data

        return corpo

    def ler_email(self, email_id: str) -> Dict[str, Any]:
        """
        Lê um email específico pelo ID.

        Args:
            email_id: ID do email

        Returns:
            Dicionário com todos os dados do email
        """
        return self._obter_email_completo(email_id)

    def enviar_email(
        self,
        destinatario: str,
        assunto: str,
        corpo: str,
        html: bool = False,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> str:
        """
        Envia um email.

        Args:
            destinatario: Email do destinatário
            assunto: Assunto do email
            corpo: Corpo do email (texto ou HTML)
            html: Se True, corpo é interpretado como HTML
            cc: Lista de emails em cópia
            bcc: Lista de emails em cópia oculta

        Returns:
            ID do email enviado

        Exemplo:
            gmail.enviar_email(
                destinatario="teste@gmail.com",
                assunto="Reunião",
                corpo="<h1>Olá!</h1><p>Confirma a reunião?</p>",
                html=True
            )
        """
        try:
            # Criar mensagem
            if html:
                message = MIMEMultipart('alternative')
                part = MIMEText(corpo, 'html')
                message.attach(part)
            else:
                message = MIMEText(corpo)

            message['To'] = destinatario
            message['Subject'] = assunto

            if cc:
                message['Cc'] = ', '.join(cc)
            if bcc:
                message['Bcc'] = ', '.join(bcc)

            # Codificar mensagem
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

            # Enviar
            send_message = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()

            print(f"[OK] Email enviado: {send_message['id']}")
            return send_message['id']

        except HttpError as error:
            raise Exception(f"Erro ao enviar email: {error}")

    def marcar_como_lido(self, email_id: str) -> bool:
        """
        Marca um email como lido.

        Args:
            email_id: ID do email

        Returns:
            True se sucesso
        """
        try:
            self.service.users().messages().modify(
                userId='me',
                id=email_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            return True
        except HttpError as error:
            raise Exception(f"Erro ao marcar como lido: {error}")

    def marcar_como_nao_lido(self, email_id: str) -> bool:
        """
        Marca um email como não lido.

        Args:
            email_id: ID do email

        Returns:
            True se sucesso
        """
        try:
            self.service.users().messages().modify(
                userId='me',
                id=email_id,
                body={'addLabelIds': ['UNREAD']}
            ).execute()
            return True
        except HttpError as error:
            raise Exception(f"Erro ao marcar como não lido: {error}")

    def deletar_email(self, email_id: str, permanente: bool = False) -> bool:
        """
        Deleta um email.

        Args:
            email_id: ID do email
            permanente: Se True, deleta permanentemente. Se False, move para lixeira

        Returns:
            True se sucesso
        """
        try:
            if permanente:
                self.service.users().messages().delete(
                    userId='me',
                    id=email_id
                ).execute()
            else:
                # Mover para lixeira
                self.service.users().messages().trash(
                    userId='me',
                    id=email_id
                ).execute()
            return True
        except HttpError as error:
            raise Exception(f"Erro ao deletar email: {error}")

    def arquivar_email(self, email_id: str) -> bool:
        """
        Arquiva um email (remove da caixa de entrada).

        Args:
            email_id: ID do email

        Returns:
            True se sucesso
        """
        try:
            self.service.users().messages().modify(
                userId='me',
                id=email_id,
                body={'removeLabelIds': ['INBOX']}
            ).execute()
            return True
        except HttpError as error:
            raise Exception(f"Erro ao arquivar email: {error}")


class IntegracaoGoogleCalendar:
    """
    Gerenciador de integração com Google Calendar via API oficial.

    Uso básico:
        # Primeira vez (gera arquivo de credenciais)
        calendar = IntegracaoGoogleCalendar(credentials_path="credentials.json")

        # Sessões seguintes (usa token salvo)
        calendar = IntegracaoGoogleCalendar(token_path="token_calendar.json")

        # Listar próximos eventos
        eventos = calendar.listar_eventos(max_results=10)

        # Criar evento
        calendar.criar_evento(
            titulo="Reunião",
            inicio="2025-10-20T10:00:00",
            fim="2025-10-20T11:00:00",
            descricao="Discussão do projeto"
        )
    """

    def __init__(
        self,
        credentials_path: Optional[str] = None,
        token_path: str = "token_calendar.json",
        credentials_dict: Optional[Dict] = None
    ):
        """
        Inicializa a integração com Google Calendar.

        Args:
            credentials_path: Caminho para arquivo credentials.json do Google Cloud
            token_path: Caminho onde salvar/carregar token de acesso
            credentials_dict: Credenciais em formato dict (alternativa a credentials_path)

        Raises:
            ValueError: Se bibliotecas do Google não estiverem instaladas
            Exception: Se autenticação falhar
        """
        if not GOOGLE_DISPONIVEL:
            raise ValueError(
                "Bibliotecas do Google não instaladas. Execute:\n"
                "pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client"
            )

        self.token_path = token_path
        self.credentials_path = credentials_path
        self.credentials_dict = credentials_dict
        self.service = None
        self._conectar()

    def _conectar(self) -> None:
        """Conecta ao Google Calendar usando OAuth2."""
        try:
            creds = None

            # Tentar carregar token existente
            if os.path.exists(self.token_path):
                creds = Credentials.from_authorized_user_file(self.token_path, SCOPES_CALENDAR)

            # Se não houver credenciais válidas, fazer login
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    # Renovar token expirado
                    creds.refresh(Request())
                else:
                    # Fazer login pela primeira vez
                    if self.credentials_dict:
                        # Usar credenciais do dict
                        flow = InstalledAppFlow.from_client_config(
                            self.credentials_dict,
                            SCOPES_CALENDAR
                        )
                    elif self.credentials_path:
                        # Usar credenciais do arquivo
                        flow = InstalledAppFlow.from_client_secrets_file(
                            self.credentials_path,
                            SCOPES_CALENDAR
                        )
                    else:
                        raise ValueError("É necessário fornecer credentials_path ou credentials_dict")

                    creds = flow.run_local_server(port=0)

                # Salvar credenciais para próxima vez
                with open(self.token_path, 'w', encoding='utf-8') as token:
                    token.write(creds.to_json())

            # Criar serviço Calendar
            self.service = build('calendar', 'v3', credentials=creds)

            # Testar conexão listando calendários
            calendar_list = self.service.calendarList().list(maxResults=1).execute()
            print(f"[OK] Conectado ao Google Calendar")

        except Exception as e:
            raise Exception(f"Erro ao conectar ao Google Calendar: {e}")

    def listar_eventos(
        self,
        max_results: int = 10,
        calendar_id: str = 'primary',
        time_min: Optional[str] = None,
        time_max: Optional[str] = None,
        query: Optional[str] = None,
        apenas_futuros: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Lista eventos do calendário.

        Args:
            max_results: Número máximo de eventos a retornar
            calendar_id: ID do calendário (padrão: 'primary' para calendário principal)
            time_min: Data/hora mínima no formato ISO 8601 (ex: 2025-10-20T00:00:00Z)
            time_max: Data/hora máxima no formato ISO 8601
            query: Texto para buscar em título/descrição
            apenas_futuros: Se True, retorna apenas eventos futuros

        Returns:
            Lista de eventos
        """
        try:
            params = {
                'calendarId': calendar_id,
                'maxResults': max_results,
                'singleEvents': True,
                'orderBy': 'startTime'
            }

            if time_min:
                params['timeMin'] = time_min
            elif apenas_futuros:
                # Usar data/hora atual
                params['timeMin'] = datetime.utcnow().isoformat() + 'Z'

            if time_max:
                params['timeMax'] = time_max

            if query:
                params['q'] = query

            events_result = self.service.events().list(**params).execute()
            events = events_result.get('items', [])

            # Parsear eventos
            eventos_parseados = []
            for event in events:
                evento_data = self._parsear_evento(event)
                eventos_parseados.append(evento_data)

            return eventos_parseados

        except HttpError as error:
            raise Exception(f"Erro ao listar eventos: {error}")

    def _parsear_evento(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parseia um evento do Google Calendar.

        Args:
            event: Objeto de evento da API

        Returns:
            Dicionário com dados do evento parseados
        """
        # Extrair início e fim
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))

        evento_data = {
            'id': event['id'],
            'titulo': event.get('summary', 'Sem título'),
            'descricao': event.get('description', ''),
            'localizacao': event.get('location', ''),
            'inicio': start,
            'fim': end,
            'dia_inteiro': 'date' in event['start'],
            'criador': event.get('creator', {}).get('email', ''),
            'organizador': event.get('organizer', {}).get('email', ''),
            'participantes': [
                {
                    'email': att.get('email'),
                    'resposta': att.get('responseStatus'),
                    'opcional': att.get('optional', False)
                }
                for att in event.get('attendees', [])
            ],
            'link_meet': event.get('hangoutLink', ''),
            'status': event.get('status', ''),
            'html_link': event.get('htmlLink', ''),
            'recorrente': 'recurrence' in event,
            'recorrencia': event.get('recurrence', []),
            'criado_em': event.get('created', ''),
            'atualizado_em': event.get('updated', '')
        }

        return evento_data

    def criar_evento(
        self,
        titulo: str,
        inicio: str,
        fim: str,
        descricao: str = "",
        localizacao: str = "",
        participantes: Optional[List[str]] = None,
        calendar_id: str = 'primary',
        dia_inteiro: bool = False,
        recorrencia: Optional[List[str]] = None,
        lembrete_minutos: Optional[List[int]] = None
    ) -> str:
        """
        Cria um novo evento no calendário.

        Args:
            titulo: Título do evento
            inicio: Data/hora de início (ISO 8601 ou YYYY-MM-DD para dia inteiro)
            fim: Data/hora de fim (ISO 8601 ou YYYY-MM-DD para dia inteiro)
            descricao: Descrição do evento
            localizacao: Local do evento
            participantes: Lista de emails dos participantes
            calendar_id: ID do calendário onde criar
            dia_inteiro: Se True, evento de dia inteiro
            recorrencia: Regras de recorrência (formato RRULE)
            lembrete_minutos: Lista de minutos antes para lembretes (ex: [10, 30])

        Returns:
            ID do evento criado

        Exemplo:
            calendar.criar_evento(
                titulo="Reunião Semanal",
                inicio="2025-10-20T10:00:00",
                fim="2025-10-20T11:00:00",
                descricao="Reunião de planejamento",
                participantes=["exemplo@gmail.com"],
                recorrencia=["RRULE:FREQ=WEEKLY;COUNT=10"]
            )
        """
        try:
            evento = {
                'summary': titulo,
                'description': descricao,
                'location': localizacao
            }

            # Configurar data/hora
            if dia_inteiro:
                evento['start'] = {'date': inicio}
                evento['end'] = {'date': fim}
            else:
                evento['start'] = {'dateTime': inicio, 'timeZone': 'America/Sao_Paulo'}
                evento['end'] = {'dateTime': fim, 'timeZone': 'America/Sao_Paulo'}

            # Adicionar participantes
            if participantes:
                evento['attendees'] = [{'email': email} for email in participantes]

            # Adicionar recorrência
            if recorrencia:
                evento['recurrence'] = recorrencia

            # Adicionar lembretes
            if lembrete_minutos:
                evento['reminders'] = {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': mins}
                        for mins in lembrete_minutos
                    ]
                }

            # Criar evento
            event_result = self.service.events().insert(
                calendarId=calendar_id,
                body=evento
            ).execute()

            print(f"[OK] Evento criado: {event_result['htmlLink']}")
            return event_result['id']

        except HttpError as error:
            raise Exception(f"Erro ao criar evento: {error}")

    def atualizar_evento(
        self,
        evento_id: str,
        calendar_id: str = 'primary',
        titulo: Optional[str] = None,
        inicio: Optional[str] = None,
        fim: Optional[str] = None,
        descricao: Optional[str] = None,
        localizacao: Optional[str] = None
    ) -> bool:
        """
        Atualiza um evento existente.

        Args:
            evento_id: ID do evento a atualizar
            calendar_id: ID do calendário
            titulo: Novo título (opcional)
            inicio: Nova data/hora de início (opcional)
            fim: Nova data/hora de fim (opcional)
            descricao: Nova descrição (opcional)
            localizacao: Nova localização (opcional)

        Returns:
            True se sucesso
        """
        try:
            # Buscar evento atual
            event = self.service.events().get(
                calendarId=calendar_id,
                eventId=evento_id
            ).execute()

            # Atualizar campos fornecidos
            if titulo is not None:
                event['summary'] = titulo
            if descricao is not None:
                event['description'] = descricao
            if localizacao is not None:
                event['location'] = localizacao
            if inicio is not None:
                if 'dateTime' in event['start']:
                    event['start']['dateTime'] = inicio
                else:
                    event['start']['date'] = inicio
            if fim is not None:
                if 'dateTime' in event['end']:
                    event['end']['dateTime'] = fim
                else:
                    event['end']['date'] = fim

            # Atualizar evento
            self.service.events().update(
                calendarId=calendar_id,
                eventId=evento_id,
                body=event
            ).execute()

            return True

        except HttpError as error:
            raise Exception(f"Erro ao atualizar evento: {error}")

    def deletar_evento(
        self,
        evento_id: str,
        calendar_id: str = 'primary'
    ) -> bool:
        """
        Deleta um evento do calendário.

        Args:
            evento_id: ID do evento a deletar
            calendar_id: ID do calendário

        Returns:
            True se sucesso
        """
        try:
            self.service.events().delete(
                calendarId=calendar_id,
                eventId=evento_id
            ).execute()
            return True
        except HttpError as error:
            raise Exception(f"Erro ao deletar evento: {error}")

    def buscar_eventos(
        self,
        texto: str,
        max_results: int = 10,
        calendar_id: str = 'primary'
    ) -> List[Dict[str, Any]]:
        """
        Busca eventos por texto em título ou descrição.

        Args:
            texto: Texto para buscar
            max_results: Número máximo de resultados
            calendar_id: ID do calendário

        Returns:
            Lista de eventos encontrados
        """
        return self.listar_eventos(
            max_results=max_results,
            calendar_id=calendar_id,
            query=texto,
            apenas_futuros=False
        )


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("📧 Teste de Integração com Google (Gmail + Calendar)")
    print("=" * 60)

    # Exemplo de uso (descomente e configure com seus dados reais)
    """
    # ===== GMAIL =====
    # Conectar (primeira vez usa credentials.json, depois usa token salvo)
    gmail = IntegracaoGmail(credentials_path="credentials.json")

    # Listar emails não lidos
    emails = gmail.listar_emails(max_results=5, apenas_nao_lidos=True)
    print(f"\n📨 {len(emails)} emails não lidos:")
    for email in emails:
        print(f"  - De: {email['remetente']}")
        print(f"    Assunto: {email['assunto']}")
        print(f"    Preview: {email['snippet']}")

    # Enviar email
    gmail.enviar_email(
        destinatario="exemplo@gmail.com",
        assunto="Teste do Luna",
        corpo="Olá! Este é um email de teste enviado via Luna.",
        html=False
    )

    # ===== GOOGLE CALENDAR =====
    # Conectar
    calendar = IntegracaoGoogleCalendar(credentials_path="credentials.json")

    # Listar próximos eventos
    eventos = calendar.listar_eventos(max_results=5)
    print(f"\n📅 {len(eventos)} próximos eventos:")
    for evento in eventos:
        print(f"  - {evento['titulo']}")
        print(f"    Quando: {evento['inicio']} até {evento['fim']}")
        if evento['localizacao']:
            print(f"    Onde: {evento['localizacao']}")

    # Criar evento
    calendar.criar_evento(
        titulo="Teste Luna",
        inicio="2025-10-20T14:00:00",
        fim="2025-10-20T15:00:00",
        descricao="Evento criado pelo sistema Luna",
        lembrete_minutos=[10, 30]
    )
    """

    print("\n[OK] Modulo carregado com sucesso!")
    print("Importe e use:")
    print("   from integracao_google import IntegracaoGmail, IntegracaoGoogleCalendar")
