#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔗 INTEGRAÇÃO COM NOTION - LUNA
================================

Integração direta com Notion usando SDK oficial (notion-client).
Permite acesso rápido e eficiente ao Notion sem precisar de navegador.

Funcionalidades:
- Conectar ao Notion via API token
- Buscar/filtrar itens em databases
- Atualizar propriedades de páginas
- Criar novas páginas em databases
- Ler propriedades complexas (title, rich_text, status, select, etc.)

Segurança:
- Token armazenado no cofre de credenciais
- Suporte a múltiplos workspaces/databases

Instalação:
    pip install notion-client

Autor: Sistema Luna
Data: 2025-10-18
"""

from typing import Dict, List, Optional, Any
import json
from datetime import datetime

# Tentar importar o SDK do Notion
try:
    from notion_client import Client
    NOTION_DISPONIVEL = True
except ImportError:
    NOTION_DISPONIVEL = False
    print("⚠️  notion-client não instalado. Execute: pip install notion-client")


class IntegracaoNotion:
    """
    Gerenciador de integração com Notion via SDK oficial.

    Uso básico:
        notion = IntegracaoNotion(token="seu_token_aqui")

        # Buscar itens
        resultados = notion.buscar_database(
            database_id="xxx",
            filtros={"Status": {"status": {"equals": "Não iniciado"}}}
        )

        # Atualizar página
        notion.atualizar_pagina(
            page_id="xxx",
            propriedades={"Status": {"status": {"name": "Em andamento"}}}
        )
    """

    def __init__(self, token: str = None):
        """
        Inicializa a integração com Notion.

        Args:
            token: Token de integração do Notion (começa com 'secret_' ou 'ntn_')

        Raises:
            ValueError: Se notion-client não estiver instalado
            ConnectionError: Se o token for inválido
        """
        if not NOTION_DISPONIVEL:
            raise ValueError(
                "notion-client não está instalado. "
                "Execute: pip install notion-client"
            )

        if not token:
            raise ValueError("Token do Notion é obrigatório")

        self.token = token
        self.client = None
        self._conectar()

    def _conectar(self) -> None:
        """Conecta ao Notion usando o token fornecido."""
        try:
            self.client = Client(auth=self.token)
            # Testar conexão fazendo uma busca vazia
            self.client.search(page_size=1)
            print("✅ Conectado ao Notion com sucesso")
        except Exception as e:
            raise ConnectionError(f"Erro ao conectar ao Notion: {e}")

    def buscar_database(
        self,
        database_id: str,
        filtros: Optional[Dict[str, Any]] = None,
        ordenacao: Optional[List[Dict[str, Any]]] = None,
        limite: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Busca itens em um database do Notion.

        Args:
            database_id: ID do database (sem hífens)
            filtros: Filtros no formato Notion API (opcional)
            ordenacao: Lista de ordenações (opcional)
            limite: Número máximo de resultados (padrão: 100)

        Returns:
            Lista de itens encontrados com propriedades parseadas

        Exemplo de filtros:
            {
                "property": "Status",
                "status": {
                    "equals": "Não iniciado"
                }
            }

        Exemplo de ordenação:
            [
                {
                    "property": "Data de criação",
                    "direction": "descending"
                }
            ]
        """
        try:
            query_params = {
                "database_id": database_id,
                "page_size": min(limite, 100)
            }

            if filtros:
                query_params["filter"] = filtros

            if ordenacao:
                query_params["sorts"] = ordenacao

            response = self.client.databases.query(**query_params)

            # Parsear resultados
            itens = []
            for page in response.get("results", []):
                item = self._parsear_pagina(page)
                itens.append(item)

            return itens

        except Exception as e:
            raise Exception(f"Erro ao buscar database: {e}")

    def _parsear_pagina(self, page: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parseia uma página do Notion extraindo propriedades importantes.

        Args:
            page: Objeto page retornado pela API do Notion

        Returns:
            Dicionário com dados parseados
        """
        item = {
            "id": page["id"],
            "url": page["url"],
            "criado_em": page["created_time"],
            "atualizado_em": page["last_edited_time"],
            "propriedades": {},
            "propriedades_raw": page["properties"]
        }

        # Parsear propriedades
        for nome_prop, valor_prop in page["properties"].items():
            prop_tipo = valor_prop["type"]

            try:
                if prop_tipo == "title":
                    # Título (array de rich text)
                    if valor_prop["title"]:
                        item["propriedades"][nome_prop] = valor_prop["title"][0]["text"]["content"]
                    else:
                        item["propriedades"][nome_prop] = ""

                elif prop_tipo == "rich_text":
                    # Texto rico
                    if valor_prop["rich_text"]:
                        item["propriedades"][nome_prop] = valor_prop["rich_text"][0]["text"]["content"]
                    else:
                        item["propriedades"][nome_prop] = ""

                elif prop_tipo == "number":
                    # Número
                    item["propriedades"][nome_prop] = valor_prop["number"]

                elif prop_tipo == "select":
                    # Select (escolha única)
                    if valor_prop["select"]:
                        item["propriedades"][nome_prop] = valor_prop["select"]["name"]
                    else:
                        item["propriedades"][nome_prop] = None

                elif prop_tipo == "multi_select":
                    # Multi-select (múltiplas escolhas)
                    item["propriedades"][nome_prop] = [
                        opt["name"] for opt in valor_prop["multi_select"]
                    ]

                elif prop_tipo == "status":
                    # Status
                    if valor_prop["status"]:
                        item["propriedades"][nome_prop] = valor_prop["status"]["name"]
                    else:
                        item["propriedades"][nome_prop] = None

                elif prop_tipo == "date":
                    # Data
                    if valor_prop["date"]:
                        item["propriedades"][nome_prop] = {
                            "inicio": valor_prop["date"]["start"],
                            "fim": valor_prop["date"].get("end")
                        }
                    else:
                        item["propriedades"][nome_prop] = None

                elif prop_tipo == "checkbox":
                    # Checkbox (booleano)
                    item["propriedades"][nome_prop] = valor_prop["checkbox"]

                elif prop_tipo == "url":
                    # URL
                    item["propriedades"][nome_prop] = valor_prop["url"]

                elif prop_tipo == "email":
                    # Email
                    item["propriedades"][nome_prop] = valor_prop["email"]

                elif prop_tipo == "phone_number":
                    # Telefone
                    item["propriedades"][nome_prop] = valor_prop["phone_number"]

                elif prop_tipo == "relation":
                    # Relação (array de IDs)
                    item["propriedades"][nome_prop] = [
                        rel["id"] for rel in valor_prop["relation"]
                    ]

                elif prop_tipo == "people":
                    # Pessoas (array de usuários)
                    item["propriedades"][nome_prop] = [
                        person["name"] for person in valor_prop["people"]
                    ]

                elif prop_tipo == "files":
                    # Arquivos (array de URLs)
                    item["propriedades"][nome_prop] = [
                        file["name"] for file in valor_prop["files"]
                    ]

                else:
                    # Tipo não tratado - deixar raw
                    item["propriedades"][nome_prop] = f"[{prop_tipo}]"

            except Exception as e:
                item["propriedades"][nome_prop] = f"[Erro ao parsear: {e}]"

        return item

    def atualizar_pagina(
        self,
        page_id: str,
        propriedades: Dict[str, Any]
    ) -> bool:
        """
        Atualiza propriedades de uma página no Notion.

        Args:
            page_id: ID da página (sem hífens)
            propriedades: Dicionário com propriedades a atualizar

        Returns:
            True se atualização bem-sucedida

        Exemplo de propriedades:
            {
                "Status": {
                    "status": {
                        "name": "Em andamento"
                    }
                },
                "Prioridade": {
                    "select": {
                        "name": "Alta"
                    }
                },
                "Notas": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Observação importante"
                            }
                        }
                    ]
                }
            }
        """
        try:
            self.client.pages.update(
                page_id=page_id,
                properties=propriedades
            )
            return True
        except Exception as e:
            raise Exception(f"Erro ao atualizar página: {e}")

    def criar_pagina(
        self,
        database_id: str,
        propriedades: Dict[str, Any],
        conteudo: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Cria uma nova página em um database do Notion.

        Args:
            database_id: ID do database onde criar a página
            propriedades: Dicionário com propriedades da nova página
            conteudo: Lista de blocos de conteúdo (opcional)

        Returns:
            ID da página criada

        Exemplo de propriedades:
            {
                "Nome da tarefa": {
                    "title": [
                        {
                            "text": {
                                "content": "Nova Tarefa"
                            }
                        }
                    ]
                },
                "Status": {
                    "status": {
                        "name": "Não iniciado"
                    }
                }
            }
        """
        try:
            params = {
                "parent": {"database_id": database_id},
                "properties": propriedades
            }

            if conteudo:
                params["children"] = conteudo

            response = self.client.pages.create(**params)
            return response["id"]

        except Exception as e:
            raise Exception(f"Erro ao criar página: {e}")

    def ler_pagina(self, page_id: str) -> Dict[str, Any]:
        """
        Lê todas as propriedades de uma página.

        Args:
            page_id: ID da página

        Returns:
            Dicionário com dados parseados da página
        """
        try:
            page = self.client.pages.retrieve(page_id=page_id)
            return self._parsear_pagina(page)
        except Exception as e:
            raise Exception(f"Erro ao ler página: {e}")

    def ler_database_schema(self, database_id: str) -> Dict[str, Any]:
        """
        Lê o schema (estrutura) de um database.

        Args:
            database_id: ID do database

        Returns:
            Dicionário com informações do database (título, propriedades, etc.)
        """
        try:
            database = self.client.databases.retrieve(database_id=database_id)

            schema = {
                "id": database["id"],
                "titulo": database["title"][0]["text"]["content"] if database["title"] else "Sem título",
                "url": database["url"],
                "criado_em": database["created_time"],
                "atualizado_em": database["last_edited_time"],
                "propriedades": {}
            }

            # Parsear estrutura das propriedades
            for nome_prop, config_prop in database["properties"].items():
                tipo = config_prop["type"]
                schema["propriedades"][nome_prop] = {"tipo": tipo}

                # Adicionar opções para select/multi-select/status
                if tipo in ["select", "multi_select"]:
                    schema["propriedades"][nome_prop]["opcoes"] = [
                        opt["name"] for opt in config_prop[tipo]["options"]
                    ]
                elif tipo == "status":
                    schema["propriedades"][nome_prop]["opcoes"] = [
                        opt["name"] for opt in config_prop["status"]["options"]
                    ]

            return schema

        except Exception as e:
            raise Exception(f"Erro ao ler schema do database: {e}")

    def buscar_paginas(
        self,
        query: str = "",
        filtro_tipo: Optional[str] = None,
        limite: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Busca páginas em todo o workspace.

        Args:
            query: Texto para buscar (opcional)
            filtro_tipo: Filtrar por tipo: "page" ou "database" (opcional)
            limite: Número máximo de resultados

        Returns:
            Lista de páginas encontradas
        """
        try:
            params = {"page_size": min(limite, 100)}

            if query:
                params["query"] = query

            if filtro_tipo:
                params["filter"] = {"property": "object", "value": filtro_tipo}

            response = self.client.search(**params)

            resultados = []
            for item in response.get("results", []):
                resultado = {
                    "id": item["id"],
                    "tipo": item["object"],
                    "url": item["url"],
                    "criado_em": item["created_time"],
                    "atualizado_em": item["last_edited_time"]
                }

                # Extrair título
                if item["object"] == "page":
                    if "properties" in item:
                        # É uma página de database
                        resultado["dados"] = self._parsear_pagina(item)
                    else:
                        # É uma página normal
                        resultado["titulo"] = item.get("title", [{}])[0].get("text", {}).get("content", "Sem título")
                elif item["object"] == "database":
                    resultado["titulo"] = item["title"][0]["text"]["content"] if item["title"] else "Sem título"

                resultados.append(resultado)

            return resultados

        except Exception as e:
            raise Exception(f"Erro ao buscar páginas: {e}")


# ============================================================================
# HELPERS PARA CRIAR PROPRIEDADES
# ============================================================================

def criar_prop_titulo(texto: str) -> Dict[str, Any]:
    """Cria propriedade do tipo título."""
    return {
        "title": [
            {
                "text": {
                    "content": texto
                }
            }
        ]
    }


def criar_prop_texto(texto: str) -> Dict[str, Any]:
    """Cria propriedade do tipo rich text."""
    return {
        "rich_text": [
            {
                "text": {
                    "content": texto
                }
            }
        ]
    }


def criar_prop_status(nome: str) -> Dict[str, Any]:
    """Cria propriedade do tipo status."""
    return {
        "status": {
            "name": nome
        }
    }


def criar_prop_select(nome: str) -> Dict[str, Any]:
    """Cria propriedade do tipo select."""
    return {
        "select": {
            "name": nome
        }
    }


def criar_prop_multi_select(nomes: List[str]) -> Dict[str, Any]:
    """Cria propriedade do tipo multi-select."""
    return {
        "multi_select": [
            {"name": nome} for nome in nomes
        ]
    }


def criar_prop_checkbox(valor: bool) -> Dict[str, Any]:
    """Cria propriedade do tipo checkbox."""
    return {
        "checkbox": valor
    }


def criar_prop_data(inicio: str, fim: Optional[str] = None) -> Dict[str, Any]:
    """
    Cria propriedade do tipo data.

    Args:
        inicio: Data de início no formato "YYYY-MM-DD" ou "YYYY-MM-DDTHH:MM:SS"
        fim: Data de fim (opcional)
    """
    prop = {
        "date": {
            "start": inicio
        }
    }
    if fim:
        prop["date"]["end"] = fim
    return prop


def criar_prop_numero(valor: float) -> Dict[str, Any]:
    """Cria propriedade do tipo número."""
    return {
        "number": valor
    }


def criar_prop_url(url: str) -> Dict[str, Any]:
    """Cria propriedade do tipo URL."""
    return {
        "url": url
    }


def criar_prop_email(email: str) -> Dict[str, Any]:
    """Cria propriedade do tipo email."""
    return {
        "email": email
    }


def criar_prop_telefone(telefone: str) -> Dict[str, Any]:
    """Cria propriedade do tipo telefone."""
    return {
        "phone_number": telefone
    }


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("🔗 Teste de Integração com Notion")
    print("=" * 60)

    # Exemplo de uso (descomente e configure com seus dados reais)
    """
    # Conectar
    notion = IntegracaoNotion(token="seu_token_aqui")

    # Buscar tarefas não iniciadas
    tarefas = notion.buscar_database(
        database_id="23b1f06b6b5f80659147d34f6084e0e0",
        filtros={
            "property": "Status",
            "status": {
                "equals": "Não iniciado"
            }
        }
    )

    print(f"Encontradas {len(tarefas)} tarefas")
    for tarefa in tarefas:
        print(f"- {tarefa['propriedades'].get('Nome da tarefa', 'Sem nome')}")

    # Atualizar status de uma tarefa
    if tarefas:
        tarefa_id = tarefas[0]["id"]
        notion.atualizar_pagina(
            page_id=tarefa_id,
            propriedades={
                "Status": criar_prop_status("Em andamento")
            }
        )
        print(f"✅ Tarefa atualizada!")
    """

    print("\n✅ Módulo carregado com sucesso!")
    print("💡 Importe e use: from integracao_notion import IntegracaoNotion")
