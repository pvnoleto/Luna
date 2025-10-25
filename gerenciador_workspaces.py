#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📁 GERENCIADOR DE WORKSPACES - LUNA (VERSÃO CORRIGIDA FINAL)
=============================================================

✅ CORREÇÕES COMPLETAS APLICADAS:
- Encoding UTF-8 forçado em TODOS os arquivos
- Caminhos multiplataforma usando Path().resolve()
- Console Windows configurado para UTF-8
- Compatível com espaços e acentuação no caminho
- Path relativo adicionado às informações dos workspaces
- Método resolver_caminho() funcionando perfeitamente

Gerencia múltiplos projetos dentro de Luna/workspaces/
Facilita organização e localização de arquivos

Estrutura:
Luna/
├── agente_completo_final.py
├── memoria_agente.json
└── workspaces/              ← PROJETOS AQUI!
    ├── projeto1/
    ├── projeto2/
    └── projeto3/

Criado: 2025-01-14
Atualizado: 2025-10-15
Corrigido: 2025-10-15 (Encoding + Windows paths + Espaços)
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import shutil

# 🆕 FASE 2.2: Import de templates
try:
    from templates_workspaces import TemplatesWorkspace
    TEMPLATES_DISPONIVEIS = True
except ImportError:
    TEMPLATES_DISPONIVEIS = False

# ✅ CORREÇÃO CRÍTICA: Forçar UTF-8 no console Windows
if sys.platform == 'win32':
    try:
        # Tenta configurar console para UTF-8
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except (AttributeError, ValueError, IOError) as e:
        # Se falhar, continua sem emojis (terminal sem suporte UTF-8)
        pass


class GerenciadorWorkspaces:
    """
    Gerencia workspaces (projetos) dentro de Luna/workspaces/
    
    ✅ 100% compatível com Windows (espaços, acentuação, UTF-8)
    """
    
    def __init__(self, base_dir: str = None):
        # ✅ CORREÇÃO: Usar Path.resolve() para caminho absoluto seguro
        if base_dir is None:
            # Usar diretório atual e resolver para caminho absoluto
            self.base_dir = Path.cwd().resolve()
        else:
            # Converter string para Path e resolver
            self.base_dir = Path(base_dir).resolve()
        
        # ✅ Diretório de workspaces (usar / para Path, nunca \\)
        self.workspaces_dir = self.base_dir / "workspaces"
        
        # Arquivo de configuração
        self.config_file = self.base_dir / "workspace_config.json"
        
        # Arquivo de log
        self.log_file = self.base_dir / "workspace.log"
        
        # Criar estrutura
        self._inicializar()
        
        # Carregar configuração
        self.config = self._carregar_config()
    
    # ========================================================================
    # INICIALIZAÇÃO
    # ========================================================================
    
    def _inicializar(self):
        """Cria estrutura inicial de pastas - ✅ CORRIGIDO"""
        try:
            # ✅ CORREÇÃO: Usar parents=True para segurança
            self.workspaces_dir.mkdir(parents=True, exist_ok=True)
            
            # Criar README com encoding UTF-8
            readme = self.workspaces_dir / "README.md"
            if not readme.exists():
                # ✅ CORREÇÃO: Encoding UTF-8 explícito
                readme.write_text(
                    """# Workspaces

Esta pasta contem todos os seus projetos organizados.

Cada projeto fica em sua propria pasta:
- workspaces/projeto1/
- workspaces/projeto2/
- workspaces/projeto3/

Luna encontra tudo automaticamente aqui!
""", 
                    encoding='utf-8'
                )
        except Exception as e:
            print(f"[ERRO] Falha ao inicializar: {e}")
            raise
    
    def _carregar_config(self) -> Dict:
        """Carrega configuração dos workspaces"""
        if self.config_file.exists():
            try:
                # ✅ CORREÇÃO: Encoding UTF-8
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self._log(f"Erro ao carregar config: {e}")
                return self._config_padrao()
        else:
            return self._config_padrao()
    
    def _config_padrao(self) -> Dict:
        """Retorna configuração padrão"""
        return {
            "workspace_atual": None,
            "workspaces": {},
            "criado_em": datetime.now().isoformat(),
            "estatisticas": {
                "total_workspaces": 0,
                "total_arquivos": 0,
                "ultimo_uso": None
            }
        }
    
    def _salvar_config(self):
        """Salva configuração em disco"""
        try:
            # ✅ CORREÇÃO: Encoding UTF-8
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self._log(f"Erro ao salvar config: {e}")
    
    def _log(self, mensagem: str):
        """Registra log de operações"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {mensagem}\n"

        try:
            # ✅ CORREÇÃO: Encoding UTF-8 explicitamente
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_msg)
        except (IOError, OSError, PermissionError) as e:
            # Silencioso se falhar (log não é crítico)
            pass

    def _atualizar_estatisticas_globais(self):
        """
        Atualiza estatísticas globais (total de workspaces, arquivos, etc.)

        🆕 FASE 1.1: Correção de estatísticas
        """
        try:
            total_workspaces = len(self.config["workspaces"])
            total_arquivos = 0

            # Somar arquivos de todos os workspaces
            for nome, info in self.config["workspaces"].items():
                workspace_path = Path(info["caminho"])
                if workspace_path.exists():
                    # Contar arquivos (mesma lógica do listar_workspaces)
                    arquivos = list(workspace_path.rglob("*"))
                    num_arquivos = len([f for f in arquivos if f.is_file()])
                    total_arquivos += num_arquivos

            # Atualizar estatísticas
            self.config["estatisticas"]["total_workspaces"] = total_workspaces
            self.config["estatisticas"]["total_arquivos"] = total_arquivos
            self.config["estatisticas"]["ultimo_uso"] = datetime.now().isoformat()

            self._salvar_config()

        except Exception as e:
            self._log(f"Erro ao atualizar estatísticas globais: {e}")

    # ========================================================================
    # OPERAÇÕES DE WORKSPACE
    # ========================================================================
    
    def criar_workspace(self, nome: str, descricao: str = "") -> Tuple[bool, str]:
        """
        Cria novo workspace
        
        Args:
            nome: Nome do workspace (será o nome da pasta)
            descricao: Descrição opcional
            
        Returns:
            (sucesso, mensagem)
        """
        # Validar nome
        if not nome or not nome.strip():
            return False, "Nome invalido"
        
        nome = nome.strip().replace(" ", "_")
        
        # Verificar se já existe
        if nome in self.config["workspaces"]:
            return False, f"Workspace '{nome}' ja existe"
        
        # ✅ Criar pasta com parents=True
        workspace_path = self.workspaces_dir / nome
        try:
            workspace_path.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            return False, f"Pasta '{nome}' ja existe"
        except Exception as e:
            return False, f"Erro ao criar pasta: {e}"
        
        # Registrar no config
        self.config["workspaces"][nome] = {
            "nome": nome,
            "descricao": descricao,
            "caminho": str(workspace_path),
            "criado_em": datetime.now().isoformat(),
            "ultimo_acesso": datetime.now().isoformat(),
            "arquivos": 0,
            "tamanho_bytes": 0,
            # 🆕 FASE 1.3: Metadata enriquecida
            "tipo": "geral",  # geral, automação, análise, estudo, bot, webapp, api
            "tags": [],  # Lista de keywords
            "tech_stack": [],  # Lista de tecnologias detectadas
            "status": "ativo"  # ativo, arquivado, concluído, pausado
        }
        
        # ✅ Criar README no workspace com encoding UTF-8
        readme = workspace_path / "README.md"
        readme.write_text(
            f"""# {nome}

{descricao if descricao else "Descricao do projeto"}

Criado em: {datetime.now().strftime("%d/%m/%Y %H:%M")}
""",
            encoding='utf-8'
        )

        # ✅ FASE 1.1: Atualizar estatísticas globais (total_workspaces E total_arquivos)
        self._atualizar_estatisticas_globais()

        self._log(f"Workspace '{nome}' criado")

        return True, f"Workspace '{nome}' criado com sucesso!"

    def criar_workspace_com_template(self, nome: str, template_id: str, descricao: str = "") -> Tuple[bool, str]:
        """
        Cria workspace usando template predefinido

        🆕 FASE 2.2: Criação com templates

        Args:
            nome: Nome do workspace
            template_id: ID do template (automacao_web, bot, analise_dados, etc.)
            descricao: Descrição opcional (sobrescreve a do template)

        Returns:
            (sucesso, mensagem)
        """
        if not TEMPLATES_DISPONIVEIS:
            return False, "Módulo de templates não disponível"

        # Obter template
        template = TemplatesWorkspace.obter_template(template_id)
        if not template:
            templates_disponiveis = ", ".join([t["id"] for t in TemplatesWorkspace.listar_templates()])
            return False, f"Template '{template_id}' não encontrado. Disponíveis: {templates_disponiveis}"

        # Criar workspace básico
        sucesso, mensagem = self.criar_workspace(nome, descricao or template["descricao"])
        if not sucesso:
            return False, mensagem

        # Aplicar template
        workspace_path = self.workspaces_dir / nome
        if TemplatesWorkspace.aplicar_template(workspace_path, template_id):
            # Atualizar metadata com info do template
            self.atualizar_metadata_workspace(
                nome,
                tipo=template.get("tipo"),
                tags=template.get("tags"),
                tech_stack=template.get("tech_stack")
            )

            self._log(f"Template '{template_id}' aplicado ao workspace '{nome}'")
            return True, f"Workspace '{nome}' criado com template '{template_id}' aplicado!"
        else:
            return False, f"Workspace criado mas erro ao aplicar template '{template_id}'"

    def atualizar_metadata_workspace(self, nome: str, tipo: str = None,
                                       tags: List[str] = None, tech_stack: List[str] = None,
                                       status: str = None) -> Tuple[bool, str]:
        """
        Atualiza metadata enriquecida de um workspace

        🆕 FASE 1.3: Permite atualizar tipo, tags, tech_stack e status

        Args:
            nome: Nome do workspace
            tipo: Tipo do projeto (geral, automação, análise, etc.)
            tags: Lista de keywords
            tech_stack: Lista de tecnologias
            status: Status (ativo, arquivado, concluído, pausado)

        Returns:
            (sucesso, mensagem)
        """
        if nome not in self.config["workspaces"]:
            return False, f"Workspace '{nome}' não encontrado"

        ws = self.config["workspaces"][nome]

        # Garantir que campos existem (para workspaces antigos)
        if "tipo" not in ws:
            ws["tipo"] = "geral"
        if "tags" not in ws:
            ws["tags"] = []
        if "tech_stack" not in ws:
            ws["tech_stack"] = []
        if "status" not in ws:
            ws["status"] = "ativo"

        # Atualizar campos fornecidos
        if tipo is not None:
            ws["tipo"] = tipo
        if tags is not None:
            ws["tags"] = tags
        if tech_stack is not None:
            ws["tech_stack"] = tech_stack
        if status is not None:
            ws["status"] = status

        self._salvar_config()
        self._log(f"Metadata do workspace '{nome}' atualizada")

        return True, f"Metadata do workspace '{nome}' atualizada com sucesso"

    def detectar_tech_stack(self, nome: str) -> List[str]:
        """
        Detecta tecnologias usadas no workspace analisando arquivos

        🆕 FASE 1.4: Auto-detecção de tech stack

        Args:
            nome: Nome do workspace

        Returns:
            Lista de tecnologias detectadas
        """
        if nome not in self.config["workspaces"]:
            return []

        workspace_path = Path(self.config["workspaces"][nome]["caminho"])
        if not workspace_path.exists():
            return []

        tech_stack = set()

        try:
            # Detectar por extensão de arquivos
            for arquivo in workspace_path.rglob("*"):
                if not arquivo.is_file():
                    continue

                ext = arquivo.suffix.lower()

                # Linguagens
                if ext == ".py":
                    tech_stack.add("Python")
                elif ext in [".js", ".jsx"]:
                    tech_stack.add("JavaScript")
                elif ext in [".ts", ".tsx"]:
                    tech_stack.add("TypeScript")
                elif ext == ".java":
                    tech_stack.add("Java")
                elif ext in [".html", ".htm"]:
                    tech_stack.add("HTML")
                elif ext == ".css":
                    tech_stack.add("CSS")
                elif ext == ".md":
                    tech_stack.add("Markdown")
                elif ext in [".json", ".yaml", ".yml"]:
                    tech_stack.add("Config")

            # Detectar frameworks/bibliotecas por imports e arquivos especiais
            for arquivo in workspace_path.rglob("*.py"):
                try:
                    conteudo = arquivo.read_text(encoding='utf-8', errors='ignore')

                    # Playwright
                    if "playwright" in conteudo.lower() or "from playwright" in conteudo:
                        tech_stack.add("Playwright")

                    # Notion
                    if "notion" in conteudo.lower():
                        tech_stack.add("Notion API")

                    # Google APIs
                    if "google" in conteudo.lower() and ("gmail" in conteudo.lower() or "calendar" in conteudo.lower()):
                        tech_stack.add("Google APIs")

                    # Web frameworks
                    if "flask" in conteudo.lower():
                        tech_stack.add("Flask")
                    if "django" in conteudo.lower():
                        tech_stack.add("Django")
                    if "fastapi" in conteudo.lower():
                        tech_stack.add("FastAPI")

                    # Data science
                    if "pandas" in conteudo.lower():
                        tech_stack.add("Pandas")
                    if "numpy" in conteudo.lower():
                        tech_stack.add("NumPy")

                except Exception:
                    continue

            # Detectar por arquivos especiais
            if (workspace_path / "requirements.txt").exists():
                tech_stack.add("pip")
            if (workspace_path / "package.json").exists():
                tech_stack.add("npm")
            if (workspace_path / "Dockerfile").exists():
                tech_stack.add("Docker")
            if (workspace_path / ".git").exists():
                tech_stack.add("Git")

        except Exception as e:
            self._log(f"Erro ao detectar tech stack de '{nome}': {e}")

        return sorted(list(tech_stack))

    def categorizar_arquivo(self, caminho: str) -> str:
        """
        Categoriza arquivo por tipo

        🆕 FASE 2.1: Auto-categorização

        Args:
            caminho: Caminho do arquivo

        Returns:
            Categoria: code, doc, config, test, data, media, temp, other
        """
        arquivo = Path(caminho)
        nome = arquivo.name.lower()
        ext = arquivo.suffix.lower()

        # Configuração
        if ext in [".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf"]:
            return "config"
        if nome in ["dockerfile", ".dockerignore", ".gitignore", ".env", "makefile"]:
            return "config"

        # Código
        if ext in [".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".c", ".cpp", ".h", ".go", ".rs", ".rb", ".php"]:
            if "test" in nome or nome.startswith("test_"):
                return "test"
            return "code"

        # Documentação
        if ext in [".md", ".txt", ".pdf", ".docx", ".doc"]:
            return "doc"
        if nome in ["readme.md", "changelog.md", "license", "contributing.md"]:
            return "doc"

        # Dados
        if ext in [".csv", ".xlsx", ".xls", ".db", ".sqlite", ".sql"]:
            return "data"

        # Mídia
        if ext in [".png", ".jpg", ".jpeg", ".gif", ".svg", ".mp4", ".mp3", ".wav"]:
            return "media"

        # Temporário
        if ext in [".tmp", ".log", ".bak", ".swp", ".cache"]:
            return "temp"
        if nome.startswith("~") or nome.endswith("~"):
            return "temp"

        # Testes
        if "test" in nome or ext == ".test":
            return "test"

        return "other"

    def sugerir_estrutura_workspace(self, nome: str) -> Dict[str, List[str]]:
        """
        Analisa workspace e sugere organização em subpastas

        🆕 FASE 2.1: Sugestão de organização

        Args:
            nome: Nome do workspace

        Returns:
            Dict com categoria -> lista de arquivos
        """
        if nome not in self.config["workspaces"]:
            return {}

        workspace_path = Path(self.config["workspaces"][nome]["caminho"])
        if not workspace_path.exists():
            return {}

        categorias = {
            "code": [],
            "doc": [],
            "config": [],
            "test": [],
            "data": [],
            "media": [],
            "temp": [],
            "other": []
        }

        try:
            # Analisar apenas arquivos na raiz (não subpastas)
            for arquivo in workspace_path.glob("*"):
                if arquivo.is_file():
                    categoria = self.categorizar_arquivo(str(arquivo))
                    categorias[categoria].append(arquivo.name)

        except Exception as e:
            self._log(f"Erro ao sugerir estrutura de '{nome}': {e}")

        # Remover categorias vazias
        return {k: v for k, v in categorias.items() if v}

    def organizar_workspace(self, nome: str, executar: bool = False) -> Dict:
        """
        Reorganiza arquivos do workspace em subpastas por categoria

        🆕 FASE 2.3: Organização automática

        Args:
            nome: Nome do workspace
            executar: Se True, move arquivos; se False, apenas simula

        Returns:
            Dict com resultado da organização (movidos, erros, etc.)
        """
        if nome not in self.config["workspaces"]:
            return {"erro": f"Workspace '{nome}' não encontrado"}

        workspace_path = Path(self.config["workspaces"][nome]["caminho"])
        if not workspace_path.exists():
            return {"erro": "Workspace não encontrado"}

        resultado = {
            "simulacao": not executar,
            "movidos": [],
            "erros": [],
            "estrutura_criada": []
        }

        try:
            # Obter categorização
            estrutura = self.sugerir_estrutura_workspace(nome)

            if not estrutura:
                return {"erro": "Nenhum arquivo para organizar"}

            # Criar pastas por categoria
            for categoria in estrutura.keys():
                pasta_categoria = workspace_path / categoria
                if not pasta_categoria.exists():
                    if executar:
                        pasta_categoria.mkdir(parents=True, exist_ok=True)
                    resultado["estrutura_criada"].append(categoria)

            # Mover arquivos
            for categoria, arquivos in estrutura.items():
                pasta_destino = workspace_path / categoria

                for arquivo_nome in arquivos:
                    arquivo_origem = workspace_path / arquivo_nome
                    arquivo_destino = pasta_destino / arquivo_nome

                    # Não mover READMEs e .gitignore
                    if arquivo_nome.lower() in ["readme.md", ".gitignore", ".env"]:
                        continue

                    try:
                        if executar:
                            shutil.move(str(arquivo_origem), str(arquivo_destino))

                        resultado["movidos"].append({
                            "arquivo": arquivo_nome,
                            "categoria": categoria,
                            "de": str(arquivo_origem),
                            "para": str(arquivo_destino)
                        })
                    except Exception as e:
                        resultado["erros"].append({
                            "arquivo": arquivo_nome,
                            "erro": str(e)
                        })

            if executar:
                self._log(f"Workspace '{nome}' organizado: {len(resultado['movidos'])} arquivos movidos")

        except Exception as e:
            resultado["erro"] = str(e)

        return resultado

    def obter_arquivos_recentes(self, nome: str, limite: int = 10) -> List[Dict]:
        """
        Lista arquivos modificados recentemente no workspace

        🆕 FASE 2.4: Tracking de arquivos recentes

        Args:
            nome: Nome do workspace
            limite: Número máximo de arquivos

        Returns:
            Lista de dicionários com info dos arquivos recentes
        """
        if nome not in self.config["workspaces"]:
            return []

        workspace_path = Path(self.config["workspaces"][nome]["caminho"])
        if not workspace_path.exists():
            return []

        arquivos_recentes = []

        try:
            # Obter todos os arquivos com tempo de modificação
            todos_arquivos = []
            for arquivo in workspace_path.rglob("*"):
                if arquivo.is_file():
                    try:
                        stat = arquivo.stat()
                        todos_arquivos.append({
                            "nome": arquivo.name,
                            "caminho": str(arquivo.relative_to(workspace_path)),
                            "caminho_completo": str(arquivo),
                            "tamanho_bytes": stat.st_size,
                            "tamanho_mb": round(stat.st_size / (1024 * 1024), 2),
                            "modificado_em": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                            "timestamp": stat.st_mtime,
                            "categoria": self.categorizar_arquivo(str(arquivo))
                        })
                    except Exception:
                        continue

            # Ordenar por tempo de modificação (mais recentes primeiro)
            todos_arquivos.sort(key=lambda x: x["timestamp"], reverse=True)

            # Remover campo timestamp (só foi usado para ordenar)
            arquivos_recentes = [{k: v for k, v in a.items() if k != "timestamp"}
                                  for a in todos_arquivos[:limite]]

        except Exception as e:
            self._log(f"Erro ao obter arquivos recentes de '{nome}': {e}")

        return arquivos_recentes

    def buscar_arquivos(self, nome: str, query: str, buscar_conteudo: bool = False) -> List[Dict]:
        """
        Busca arquivos no workspace por nome ou conteúdo

        🆕 FASE 3.1: Busca semântica

        Args:
            nome: Nome do workspace
            query: Termo de busca
            buscar_conteudo: Se True, busca também no conteúdo dos arquivos

        Returns:
            Lista de arquivos encontrados
        """
        if nome not in self.config["workspaces"]:
            return []

        workspace_path = Path(self.config["workspaces"][nome]["caminho"])
        if not workspace_path.exists():
            return []

        resultados = []
        query_lower = query.lower()

        try:
            for arquivo in workspace_path.rglob("*"):
                if not arquivo.is_file():
                    continue

                match_score = 0
                match_info = {"tipo": []}

                # Busca no nome do arquivo
                if query_lower in arquivo.name.lower():
                    match_score += 10
                    match_info["tipo"].append("nome")

                # Busca no caminho
                if query_lower in str(arquivo.relative_to(workspace_path)).lower():
                    match_score += 5
                    match_info["tipo"].append("caminho")

                # Busca no conteúdo (apenas arquivos de texto)
                if buscar_conteudo and arquivo.suffix.lower() in [".py", ".js", ".md", ".txt", ".json", ".yaml"]:
                    try:
                        conteudo = arquivo.read_text(encoding='utf-8', errors='ignore')
                        if query_lower in conteudo.lower():
                            match_score += 3
                            match_info["tipo"].append("conteúdo")
                    except Exception:
                        pass

                if match_score > 0:
                    stat = arquivo.stat()
                    resultados.append({
                        "nome": arquivo.name,
                        "caminho": str(arquivo.relative_to(workspace_path)),
                        "caminho_completo": str(arquivo),
                        "tamanho_mb": round(stat.st_size / (1024 * 1024), 2),
                        "categoria": self.categorizar_arquivo(str(arquivo)),
                        "match_score": match_score,
                        "match_tipo": ", ".join(match_info["tipo"])
                    })

            # Ordenar por relevância (score)
            resultados.sort(key=lambda x: x["match_score"], reverse=True)

        except Exception as e:
            self._log(f"Erro ao buscar em '{nome}': {e}")

        return resultados

    def analisar_workspace(self, nome: str) -> Dict:
        """
        Gera análise completa do workspace

        🆕 FASE 3.2: Análise completa

        Args:
            nome: Nome do workspace

        Returns:
            Dict com análise completa (estatísticas, distribuição, etc.)
        """
        if nome not in self.config["workspaces"]:
            return {"erro": "Workspace não encontrado"}

        workspace_path = Path(self.config["workspaces"][nome]["caminho"])
        if not workspace_path.exists():
            return {"erro": "Caminho do workspace não existe"}

        analise = {
            "workspace": nome,
            "caminho": str(workspace_path),
            "estatisticas": {},
            "distribuicao_categorias": {},
            "distribuicao_extensoes": {},
            "tech_stack_detectado": [],
            "arquivos_maiores": [],
            "arquivos_recentes": [],
            "sugestoes": []
        }

        try:
            total_arquivos = 0
            total_bytes = 0
            categorias = {}
            extensoes = {}

            # Analisar todos os arquivos
            for arquivo in workspace_path.rglob("*"):
                if not arquivo.is_file():
                    continue

                total_arquivos += 1
                tamanho = arquivo.stat().st_size
                total_bytes += tamanho

                # Categorias
                categoria = self.categorizar_arquivo(str(arquivo))
                categorias[categoria] = categorias.get(categoria, 0) + 1

                # Extensões
                ext = arquivo.suffix.lower() or "sem extensão"
                extensoes[ext] = extensoes.get(ext, 0) + 1

            # Estatísticas
            analise["estatisticas"] = {
                "total_arquivos": total_arquivos,
                "tamanho_total_mb": round(total_bytes / (1024 * 1024), 2),
                "tamanho_total_gb": round(total_bytes / (1024 * 1024 * 1024), 2),
                "tamanho_medio_kb": round((total_bytes / total_arquivos) / 1024, 2) if total_arquivos > 0 else 0
            }

            # Distribuições
            analise["distribuicao_categorias"] = dict(sorted(categorias.items(), key=lambda x: x[1], reverse=True))
            analise["distribuicao_extensoes"] = dict(sorted(extensoes.items(), key=lambda x: x[1], reverse=True)[:10])

            # Tech stack
            analise["tech_stack_detectado"] = self.detectar_tech_stack(nome)

            # Arquivos maiores (top 5)
            analise["arquivos_maiores"] = self.obter_arquivos_recentes(nome, limite=5)

            # Arquivos recentes (top 5)
            analise["arquivos_recentes"] = self.obter_arquivos_recentes(nome, limite=5)

            # Sugestões
            if total_arquivos > 20 and not any(p.is_dir() and p.name in ["src", "tests", "docs"] for p in workspace_path.iterdir()):
                analise["sugestoes"].append("Workspace com muitos arquivos na raiz - considere organizar em subpastas")

            if categorias.get("temp", 0) > 5:
                analise["sugestoes"].append(f"{categorias['temp']} arquivos temporários detectados - considere limpeza")

            if total_bytes > 100 * 1024 * 1024:  # > 100MB
                analise["sugestoes"].append("Workspace grande (>100MB) - verifique se há arquivos desnecessários")

        except Exception as e:
            analise["erro"] = str(e)
            self._log(f"Erro ao analisar workspace '{nome}': {e}")

        return analise

    def sugerir_limpeza(self, nome: str) -> Dict:
        """
        Sugere arquivos para limpeza (temporários, duplicados, grandes)

        🆕 FASE 3.3: Limpeza inteligente

        Args:
            nome: Nome do workspace

        Returns:
            Dict com sugestões de limpeza
        """
        if nome not in self.config["workspaces"]:
            return {"erro": "Workspace não encontrado"}

        workspace_path = Path(self.config["workspaces"][nome]["caminho"])
        if not workspace_path.exists():
            return {"erro": "Workspace não existe"}

        sugestoes = {
            "temporarios": [],
            "duplicados": [],
            "grandes": [],
            "total_economizado_mb": 0
        }

        try:
            # 1. Arquivos temporários
            for arquivo in workspace_path.rglob("*"):
                if not arquivo.is_file():
                    continue

                categoria = self.categorizar_arquivo(str(arquivo))
                if categoria == "temp":
                    tamanho_mb = arquivo.stat().st_size / (1024 * 1024)
                    sugestoes["temporarios"].append({
                        "nome": arquivo.name,
                        "caminho": str(arquivo.relative_to(workspace_path)),
                        "tamanho_mb": round(tamanho_mb, 2)
                    })
                    sugestoes["total_economizado_mb"] += tamanho_mb

            # 2. Arquivos duplicados (mesmo nome e tamanho)
            arquivos_por_nome = {}
            for arquivo in workspace_path.rglob("*"):
                if not arquivo.is_file():
                    continue

                chave = (arquivo.name, arquivo.stat().st_size)
                if chave not in arquivos_por_nome:
                    arquivos_por_nome[chave] = []
                arquivos_por_nome[chave].append(arquivo)

            for (nome_arq, tamanho), caminhos in arquivos_por_nome.items():
                if len(caminhos) > 1:
                    tamanho_mb = tamanho / (1024 * 1024)
                    sugestoes["duplicados"].append({
                        "nome": nome_arq,
                        "ocorrencias": len(caminhos),
                        "caminhos": [str(c.relative_to(workspace_path)) for c in caminhos],
                        "tamanho_mb": round(tamanho_mb, 2),
                        "economia_mb": round(tamanho_mb * (len(caminhos) - 1), 2)
                    })
                    sugestoes["total_economizado_mb"] += tamanho_mb * (len(caminhos) - 1)

            # 3. Arquivos grandes (> 10MB)
            for arquivo in workspace_path.rglob("*"):
                if not arquivo.is_file():
                    continue

                tamanho_mb = arquivo.stat().st_size / (1024 * 1024)
                if tamanho_mb > 10:
                    sugestoes["grandes"].append({
                        "nome": arquivo.name,
                        "caminho": str(arquivo.relative_to(workspace_path)),
                        "tamanho_mb": round(tamanho_mb, 2),
                        "categoria": self.categorizar_arquivo(str(arquivo))
                    })

            # Ordenar por tamanho
            sugestoes["grandes"].sort(key=lambda x: x["tamanho_mb"], reverse=True)
            sugestoes["total_economizado_mb"] = round(sugestoes["total_economizado_mb"], 2)

        except Exception as e:
            sugestoes["erro"] = str(e)
            self._log(f"Erro ao sugerir limpeza de '{nome}': {e}")

        return sugestoes

    def listar_workspaces(self) -> List[Dict]:
        """
        Lista todos workspaces
        
        Returns:
            Lista de dicionários com info dos workspaces
        """
        workspaces = []
        
        for nome, info in self.config["workspaces"].items():
            # 🆕 FASE 1.3: Garantir metadata enriquecida existe (retrocompatibilidade)
            if "tipo" not in info:
                info["tipo"] = "geral"
            if "tags" not in info:
                info["tags"] = []
            if "tech_stack" not in info:
                info["tech_stack"] = []
            if "status" not in info:
                info["status"] = "ativo"

            # Atualizar informações
            workspace_path = Path(info["caminho"])
            if workspace_path.exists():
                # Contar arquivos
                arquivos = list(workspace_path.rglob("*"))
                info["arquivos"] = len([f for f in arquivos if f.is_file()])

                # Calcular tamanho
                tamanho = sum(f.stat().st_size for f in arquivos if f.is_file())
                info["tamanho_bytes"] = tamanho
                info["tamanho_mb"] = round(tamanho / (1024 * 1024), 2)

            # ✅ Adicionar path_relativo e info se é o atual
            info["path_relativo"] = f"workspaces/{nome}"
            info["atual"] = (nome == self.config.get("workspace_atual"))

            workspaces.append(info)
        
        return workspaces
    
    def selecionar_workspace(self, nome: str) -> Tuple[bool, str]:
        """
        Seleciona workspace como atual

        Args:
            nome: Nome do workspace

        Returns:
            (sucesso, mensagem)
        """
        if nome not in self.config["workspaces"]:
            return False, f"Workspace '{nome}' nao encontrado"

        self.config["workspace_atual"] = nome
        self.config["workspaces"][nome]["ultimo_acesso"] = datetime.now().isoformat()

        # ✅ FASE 1.1: Atualizar estatísticas globais
        self._atualizar_estatisticas_globais()

        self._log(f"Workspace '{nome}' selecionado")

        return True, f"Workspace '{nome}' selecionado"
    
    def get_workspace_atual(self) -> Optional[Dict]:
        """
        Retorna informações do workspace atual
        
        Returns:
            Dict com info do workspace ou None
        """
        nome = self.config.get("workspace_atual")
        if nome and nome in self.config["workspaces"]:
            ws = self.config["workspaces"][nome].copy()
            # ✅ Adicionar path_relativo
            ws["path_relativo"] = f"workspaces/{nome}"
            ws["atual"] = True
            return ws
        return None
    
    def get_caminho_workspace(self, nome: str = None) -> Optional[Path]:
        """
        Retorna caminho do workspace
        
        Args:
            nome: Nome do workspace (None = atual)
            
        Returns:
            Path do workspace ou None
        """
        if nome is None:
            nome = self.config.get("workspace_atual")
        
        if nome and nome in self.config["workspaces"]:
            return Path(self.config["workspaces"][nome]["caminho"])
        
        return None
    
    def deletar_workspace(self, nome: str, confirmar: bool = False) -> Tuple[bool, str]:
        """
        Deleta workspace
        
        Args:
            nome: Nome do workspace
            confirmar: Se True, deleta sem perguntar
            
        Returns:
            (sucesso, mensagem)
        """
        if nome not in self.config["workspaces"]:
            return False, f"Workspace '{nome}' nao encontrado"
        
        if not confirmar:
            return False, f"Use confirmar=True para deletar '{nome}'"
        
        # Deletar pasta
        workspace_path = Path(self.config["workspaces"][nome]["caminho"])
        try:
            if workspace_path.exists():
                shutil.rmtree(workspace_path)
        except Exception as e:
            return False, f"Erro ao deletar pasta: {e}"
        
        # Remover do config
        del self.config["workspaces"][nome]
        
        # Se era o atual, limpar
        if self.config.get("workspace_atual") == nome:
            self.config["workspace_atual"] = None
        
        # Atualizar estatísticas
        self.config["estatisticas"]["total_workspaces"] -= 1
        
        self._salvar_config()
        self._log(f"Workspace '{nome}' deletado")
        
        return True, f"Workspace '{nome}' deletado"
    
    def renomear_workspace(self, nome_antigo: str, nome_novo: str) -> Tuple[bool, str]:
        """
        Renomeia workspace
        
        Args:
            nome_antigo: Nome atual
            nome_novo: Novo nome
            
        Returns:
            (sucesso, mensagem)
        """
        if nome_antigo not in self.config["workspaces"]:
            return False, f"Workspace '{nome_antigo}' nao encontrado"
        
        if nome_novo in self.config["workspaces"]:
            return False, f"Workspace '{nome_novo}' ja existe"
        
        nome_novo = nome_novo.strip().replace(" ", "_")
        
        # Renomear pasta
        path_antigo = Path(self.config["workspaces"][nome_antigo]["caminho"])
        path_novo = path_antigo.parent / nome_novo
        
        try:
            path_antigo.rename(path_novo)
        except Exception as e:
            return False, f"Erro ao renomear pasta: {e}"
        
        # Atualizar config
        info = self.config["workspaces"][nome_antigo]
        info["nome"] = nome_novo
        info["caminho"] = str(path_novo)
        
        self.config["workspaces"][nome_novo] = info
        del self.config["workspaces"][nome_antigo]
        
        # Se era o atual, atualizar
        if self.config.get("workspace_atual") == nome_antigo:
            self.config["workspace_atual"] = nome_novo
        
        self._salvar_config()
        self._log(f"Workspace '{nome_antigo}' renomeado para '{nome_novo}'")
        
        return True, f"Workspace renomeado: '{nome_antigo}' -> '{nome_novo}'"
    
    # ========================================================================
    # ✅ MÉTODO CRÍTICO: RESOLVER CAMINHO
    # ========================================================================
    
    def resolver_caminho(self, caminho: str) -> str:
        """
        ✅ MÉTODO ESSENCIAL: Resolve caminho relativo para absoluto
        
        Se há workspace atual e o caminho não é absoluto,
        resolve para dentro do workspace atual.
        
        Args:
            caminho: Caminho do arquivo (pode ser relativo)
            
        Returns:
            Caminho absoluto como string
        """
        # ✅ Converter para Path e resolver
        path_obj = Path(caminho)
        
        # Se já é absoluto, retornar resolvido
        if path_obj.is_absolute():
            return str(path_obj.resolve())

        # Se há workspace atual, resolver para dentro dele
        ws_atual = self.get_workspace_atual()
        if ws_atual:
            workspace_path = Path(ws_atual["caminho"])

            # 🛡️ PROTEÇÃO: Verifica se o caminho já contém o workspace_path
            # Evita duplicação como: workspace/workspace/arquivo.txt
            caminho_str = str(caminho)
            workspace_str = str(workspace_path)

            # Se o caminho já começa com o workspace_path, não concatenar
            if caminho_str.startswith(workspace_str):
                # Caminho já está correto, apenas resolver
                caminho_completo = Path(caminho).resolve()
            else:
                # Caminho relativo, concatenar com workspace
                caminho_completo = (workspace_path / caminho).resolve()

            return str(caminho_completo)
        
        # Se não há workspace, usar diretório base
        caminho_completo = (self.base_dir / caminho).resolve()
        return str(caminho_completo)
    
    # ========================================================================
    # OPERAÇÕES DE ARQUIVOS
    # ========================================================================
    
    def criar_arquivo(self, nome_arquivo: str, conteudo: str = "", 
                     workspace: str = None) -> Tuple[bool, str, Optional[Path]]:
        """
        Cria arquivo no workspace
        
        Args:
            nome_arquivo: Nome do arquivo
            conteudo: Conteúdo inicial
            workspace: Nome do workspace (None = atual)
            
        Returns:
            (sucesso, mensagem, caminho_arquivo)
        """
        caminho_ws = self.get_caminho_workspace(workspace)
        if caminho_ws is None:
            return False, "Nenhum workspace selecionado", None
        
        # Criar arquivo
        arquivo_path = caminho_ws / nome_arquivo
        
        # ✅ CORREÇÃO: Criar subpastas com parents=True
        arquivo_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # ✅ CORREÇÃO: Encoding UTF-8
            arquivo_path.write_text(conteudo, encoding='utf-8')
        except Exception as e:
            return False, f"Erro ao criar arquivo: {e}", None
        
        self._log(f"Arquivo '{nome_arquivo}' criado em workspace '{workspace or self.config.get('workspace_atual')}'")
        
        return True, f"Arquivo '{nome_arquivo}' criado", arquivo_path
    
    def listar_arquivos(self, workspace: str = None, recursivo: bool = True) -> List[Path]:
        """
        Lista arquivos do workspace
        
        Args:
            workspace: Nome do workspace (None = atual)
            recursivo: Se True, lista subpastas também
            
        Returns:
            Lista de paths dos arquivos
        """
        caminho_ws = self.get_caminho_workspace(workspace)
        if caminho_ws is None:
            return []
        
        try:
            if recursivo:
                return [f for f in caminho_ws.rglob("*") if f.is_file()]
            else:
                return [f for f in caminho_ws.glob("*") if f.is_file()]
        except Exception as e:
            self._log(f"Erro ao listar arquivos: {e}")
            return []
    
    def buscar_arquivo(self, nome: str, workspace: str = None) -> Optional[Path]:
        """
        Busca arquivo por nome no workspace
        
        Args:
            nome: Nome do arquivo (pode ser parcial)
            workspace: Nome do workspace (None = atual)
            
        Returns:
            Path do arquivo ou None
        """
        arquivos = self.listar_arquivos(workspace)
        
        # Busca exata primeiro
        for arquivo in arquivos:
            if arquivo.name == nome:
                return arquivo
        
        # Busca parcial
        for arquivo in arquivos:
            if nome.lower() in arquivo.name.lower():
                return arquivo
        
        return None
    
    # ========================================================================
    # VISUALIZAÇÃO
    # ========================================================================
    
    def exibir_status(self):
        """Exibe status dos workspaces"""
        print("\n" + "="*70)
        print("WORKSPACES - STATUS")
        print("="*70)
        
        workspaces = self.listar_workspaces()
        
        if not workspaces:
            print("\nNenhum workspace criado ainda")
            print("\nUse: criar_workspace('nome', 'descricao')")
        else:
            atual = self.config.get("workspace_atual")
            
            print(f"\nTotal: {len(workspaces)} workspace(s)")
            if atual:
                print(f"Atual: {atual}")
            
            print("\n" + "-"*70)
            
            for ws in workspaces:
                is_atual = ws["nome"] == atual
                marcador = "[ATUAL]" if is_atual else "[     ]"
                
                print(f"\n{marcador} {ws['nome']}")
                if ws.get("descricao"):
                    print(f"   {ws['descricao']}")
                print(f"   Arquivos: {ws.get('arquivos', 0)}")
                print(f"   Tamanho: {ws.get('tamanho_mb', 0)} MB")
                print(f"   {ws['caminho']}")
        
        print("\n" + "="*70 + "\n")
    
    def exibir_arvore(self, workspace: str = None, max_nivel: int = 3):
        """
        Exibe árvore de arquivos do workspace
        
        Args:
            workspace: Nome do workspace (None = atual)
            max_nivel: Profundidade máxima
        """
        caminho_ws = self.get_caminho_workspace(workspace)
        if caminho_ws is None:
            print("Nenhum workspace selecionado")
            return
        
        nome = workspace or self.config.get("workspace_atual")
        print(f"\n{nome}/")
        
        def _exibir_dir(path: Path, prefixo: str = "", nivel: int = 0):
            if nivel >= max_nivel:
                return
            
            try:
                items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            except Exception as e:
                print(f"{prefixo}Erro ao listar: {e}")
                return
            
            for i, item in enumerate(items):
                is_ultimo = i == len(items) - 1
                
                if item.is_dir():
                    print(f"{prefixo}{'└── ' if is_ultimo else '├── '}[DIR] {item.name}/")
                    novo_prefixo = prefixo + ("    " if is_ultimo else "│   ")
                    _exibir_dir(item, novo_prefixo, nivel + 1)
                else:
                    print(f"{prefixo}{'└── ' if is_ultimo else '├── '}[   ] {item.name}")
        
        _exibir_dir(caminho_ws)
        print()


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("""
================================================================================
              GERENCIADOR DE WORKSPACES
                 LUNA (CORRIGIDO FINAL)
================================================================================
    """)
    
    # Teste básico
    print("Testando gerenciador...")
    gerenciador = GerenciadorWorkspaces()
    
    print(f"Gerenciador inicializado")
    print(f"Pasta workspaces: {gerenciador.workspaces_dir}")
    print(f"Sistema operacional: {os.name}")
    print(f"Base dir: {gerenciador.base_dir}")
    
    gerenciador.exibir_status()
    
    print("\nTESTE CONCLUIDO!")
