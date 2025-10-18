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
            "tamanho_bytes": 0
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
        
        # Atualizar estatísticas
        self.config["estatisticas"]["total_workspaces"] += 1
        self.config["estatisticas"]["ultimo_uso"] = datetime.now().isoformat()
        
        self._salvar_config()
        self._log(f"Workspace '{nome}' criado")
        
        return True, f"Workspace '{nome}' criado com sucesso!"
    
    def listar_workspaces(self) -> List[Dict]:
        """
        Lista todos workspaces
        
        Returns:
            Lista de dicionários com info dos workspaces
        """
        workspaces = []
        
        for nome, info in self.config["workspaces"].items():
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
        self.config["estatisticas"]["ultimo_uso"] = datetime.now().isoformat()
        
        self._salvar_config()
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
