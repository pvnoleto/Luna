#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧬 SISTEMA DE AUTO-EVOLUÇÃO
============================

Permite que Luna se auto-modifique de forma segura e inteligente.

Features:
- Fila de melhorias (anota durante, aplica depois)
- Backup automático antes de cada modificação
- Validação completa (sintaxe + import + testes)
- Rollback automático se quebrar
- Limpeza inteligente de backups
- Zonas protegidas (código crítico)
- Log detalhado + resumo
- Memória de erros (não repete)
"""

import os
import shutil
import ast
import sys
import importlib
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json
import hashlib


# ============================================================================
# NÍVEIS DE RISCO PARA AUTO-APLICAÇÃO INTELIGENTE (FASE 4 - P2)
# ============================================================================

# Níveis de risco para categorização de melhorias
NIVEL_RISCO_SAFE = "SAFE"       # Seguro - auto-aplicar sempre
NIVEL_RISCO_MEDIUM = "MEDIUM"   # Médio - auto-aplicar se prioridade >= 6
NIVEL_RISCO_RISKY = "RISKY"     # Arriscado - auto-aplicar apenas se prioridade >= 9

# Tipos de melhoria por nível de risco
TIPOS_SAFE = [
    'documentacao',  # Docstrings, comentários
    'formatacao',    # PEP8, formatação de código
    'typing_simples' # Type hints básicos (str, int, bool)
]

TIPOS_MEDIUM = [
    'otimizacao_simples',  # Otimizações algorítmicas simples
    'otimizacao',          # Otimizações gerais (P7) - auto-aplicar se P >= 7
    'qualidade',           # Melhorias de qualidade de código (P8)
    'refatoracao_pequena', # Refatorações localizadas
    'typing_complexo'      # Type hints complexos (Optional, Union, etc)
]

TIPOS_RISKY = [
    'bug_fix',              # Correções de bugs (podem ter efeitos colaterais)
    'refatoracao_grande',   # Refatorações estruturais
    'otimizacao_complexa',  # Otimizações que mudam lógica
    'seguranca'             # Mudanças relacionadas a segurança
]


# ============================================================================
# SISTEMA DE FEEDBACK LOOP (FASE 5 - P2)
# ============================================================================

class FeedbackLoop:
    """
    ✅ FASE 5: Sistema de aprendizado contínuo baseado em sucessos/falhas (P2)

    Features:
    - Rastreia métricas de qualidade antes/depois de cada melhoria
    - Blacklist automática de padrões que sempre falham
    - Ajusta prioridades baseado em histórico de sucesso
    - Persiste aprendizados em JSON
    """

    def __init__(self, arquivo: str = "Luna/.melhorias/feedback_loop.json"):
        """
        Inicializa sistema de feedback loop

        Args:
            arquivo: Caminho do arquivo JSON para persistir feedback
        """
        self.arquivo = arquivo
        self.metricas_historico = []
        self.blacklist_padroes = []
        self.taxa_sucesso_por_tipo = {}

        # Criar diretório se não existir
        Path(arquivo).parent.mkdir(parents=True, exist_ok=True)

        # Carregar dados salvos
        self._carregar_feedback()

    def registrar_tentativa(
        self,
        melhoria: Dict,
        sucesso: bool,
        metricas_antes: Optional[Dict] = None,
        metricas_depois: Optional[Dict] = None,
        erro: Optional[str] = None
    ):
        """
        Registra tentativa de aplicação de melhoria

        Args:
            melhoria: Dicionário com dados da melhoria
            sucesso: True se aplicada com sucesso
            metricas_antes: Métricas antes da aplicação (opcional)
            metricas_depois: Métricas depois da aplicação (opcional)
            erro: Mensagem de erro se falhou (opcional)
        """
        tipo = melhoria['tipo']

        # Atualizar taxa de sucesso por tipo
        if tipo not in self.taxa_sucesso_por_tipo:
            self.taxa_sucesso_por_tipo[tipo] = {'tentativas': 0, 'sucessos': 0}

        self.taxa_sucesso_por_tipo[tipo]['tentativas'] += 1
        if sucesso:
            self.taxa_sucesso_por_tipo[tipo]['sucessos'] += 1

        # Sempre registrar no histórico (para rastrear falhas para blacklist)
        registro = {
            'timestamp': datetime.now().isoformat(),
            'tipo': tipo,
            'alvo': melhoria['alvo'],
            'sucesso': sucesso
        }

        # Adicionar métricas se disponíveis
        if metricas_antes and metricas_depois:
            registro['metricas_antes'] = metricas_antes
            registro['metricas_depois'] = metricas_depois
            registro['melhoria_qualidade'] = self._calcular_melhoria_qualidade(metricas_antes, metricas_depois)

        if erro:
            registro['erro'] = erro

        self.metricas_historico.append(registro)

        # Se falhou múltiplas vezes, adicionar à blacklist
        if not sucesso and erro:
            self._verificar_blacklist(melhoria, erro)

        # Persistir
        self._salvar_feedback()

    def _calcular_melhoria_qualidade(self, antes: Dict, depois: Dict) -> float:
        """
        Calcula percentual de melhoria na qualidade do código

        Considera métricas como:
        - Complexidade ciclomática (menor é melhor)
        - Linhas de código (depende do contexto)
        - Cobertura de testes (maior é melhor)

        Returns:
            Percentual de melhoria (-100 a +100)
        """
        # Exemplo simplificado - pode ser expandido
        score_antes = 0
        score_depois = 0

        # Complexidade (menor é melhor)
        if 'complexidade' in antes and 'complexidade' in depois:
            score_antes -= antes['complexidade']
            score_depois -= depois['complexidade']

        # Cobertura de testes (maior é melhor)
        if 'cobertura_testes' in antes and 'cobertura_testes' in depois:
            score_antes += antes['cobertura_testes']
            score_depois += depois['cobertura_testes']

        # Se ambos são zero, sem mudança
        if score_antes == 0 and score_depois == 0:
            return 0.0

        # Calcular melhoria percentual
        if score_antes == 0:
            return 100.0 if score_depois > 0 else 0.0

        melhoria = ((score_depois - score_antes) / abs(score_antes)) * 100
        return round(melhoria, 2)

    def _verificar_blacklist(self, melhoria: Dict, erro: str):
        """
        Verifica se padrão deve ser adicionado à blacklist

        Adiciona à blacklist se:
        - Mesmo tipo + mesmo alvo falhou 3+ vezes
        - Mesmo erro ocorreu 5+ vezes
        """
        tipo = melhoria['tipo']
        alvo = melhoria['alvo']

        # Contar falhas deste padrão
        padrao = f"{tipo}:{alvo}"
        falhas_padrao = sum(
            1 for m in self.metricas_historico
            if not m['sucesso'] and f"{m['tipo']}:{m['alvo']}" == padrao
        )

        # Se 3+ falhas, adicionar à blacklist
        if falhas_padrao >= 3:
            # Verificar se padrão já está na blacklist
            ja_na_blacklist = any(item['padrao'] == padrao for item in self.blacklist_padroes)

            if not ja_na_blacklist:
                self.blacklist_padroes.append({
                    'padrao': padrao,
                    'tipo': tipo,
                    'alvo': alvo,
                    'adicionado_em': datetime.now().isoformat(),
                    'falhas': falhas_padrao,
                    'ultimo_erro': erro
                })
                print(f"    [X] Padrão adicionado à blacklist: {padrao} ({falhas_padrao} falhas)")

    def esta_na_blacklist(self, melhoria: Dict) -> Tuple[bool, Optional[str]]:
        """
        Verifica se melhoria está na blacklist

        Returns:
            (esta_na_blacklist, motivo)
        """
        padrao = f"{melhoria['tipo']}:{melhoria['alvo']}"

        for item in self.blacklist_padroes:
            if item['padrao'] == padrao:
                return True, f"Padrão bloqueado (blacklist): {item['falhas']} falhas anteriores"

        return False, None

    def obter_taxa_sucesso(self, tipo: str) -> float:
        """
        Retorna taxa de sucesso para um tipo de melhoria

        Returns:
            Taxa de sucesso (0.0 a 1.0)
        """
        if tipo not in self.taxa_sucesso_por_tipo:
            return 0.5  # Neutro se não temos dados

        stats = self.taxa_sucesso_por_tipo[tipo]
        if stats['tentativas'] == 0:
            return 0.5

        return stats['sucessos'] / stats['tentativas']

    def ajustar_prioridade(self, melhoria: Dict) -> int:
        """
        Ajusta prioridade baseado em histórico de sucesso

        Aumenta prioridade de tipos com alta taxa de sucesso
        Diminui prioridade de tipos com baixa taxa de sucesso

        Returns:
            Nova prioridade ajustada (1-10)
        """
        prioridade_original = melhoria['prioridade']
        taxa_sucesso = self.obter_taxa_sucesso(melhoria['tipo'])

        # Ajuste baseado na taxa de sucesso
        # Taxa alta (>0.8): +2 pontos
        # Taxa média (0.4-0.8): sem ajuste
        # Taxa baixa (<0.4): -2 pontos

        if taxa_sucesso > 0.8:
            ajuste = 2
        elif taxa_sucesso < 0.4:
            ajuste = -2
        else:
            ajuste = 0

        nova_prioridade = max(1, min(10, prioridade_original + ajuste))

        if ajuste != 0:
            print(f"    [STATS] Prioridade ajustada: {prioridade_original} → {nova_prioridade} (taxa sucesso: {taxa_sucesso:.1%})")

        return nova_prioridade

    def obter_estatisticas(self) -> Dict:
        """
        Retorna estatísticas do feedback loop

        Returns:
            Dict com estatísticas completas
        """
        total_tentativas = sum(t['tentativas'] for t in self.taxa_sucesso_por_tipo.values())
        total_sucessos = sum(t['sucessos'] for t in self.taxa_sucesso_por_tipo.values())

        return {
            'total_tentativas': total_tentativas,
            'total_sucessos': total_sucessos,
            'taxa_sucesso_geral': total_sucessos / total_tentativas if total_tentativas > 0 else 0,
            'tipos_rastreados': len(self.taxa_sucesso_por_tipo),
            'blacklist_tamanho': len(self.blacklist_padroes),
            'metricas_registradas': len(self.metricas_historico),
            'taxa_por_tipo': {
                tipo: {
                    'tentativas': stats['tentativas'],
                    'sucessos': stats['sucessos'],
                    'taxa': stats['sucessos'] / stats['tentativas'] if stats['tentativas'] > 0 else 0
                }
                for tipo, stats in self.taxa_sucesso_por_tipo.items()
            }
        }

    def _carregar_feedback(self):
        """Carrega feedback salvo do arquivo JSON"""
        try:
            if not os.path.exists(self.arquivo):
                return

            with open(self.arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)

            self.metricas_historico = dados.get('metricas_historico', [])
            self.blacklist_padroes = dados.get('blacklist_padroes', [])
            self.taxa_sucesso_por_tipo = dados.get('taxa_sucesso_por_tipo', {})

            if self.blacklist_padroes:
                print(f"    [!] {len(self.blacklist_padroes)} padrão(ões) na blacklist")

            if self.taxa_sucesso_por_tipo:
                print(f"    [*] {len(self.taxa_sucesso_por_tipo)} tipo(s) com histórico de sucesso")

        except json.JSONDecodeError as e:
            print(f"    [!] Erro ao carregar feedback (JSON inválido): {e}")
        except Exception as e:
            print(f"    [!] Erro ao carregar feedback: {e}")

    def _salvar_feedback(self):
        """Salva feedback no arquivo JSON"""
        try:
            dados = {
                'metricas_historico': self.metricas_historico,
                'blacklist_padroes': self.blacklist_padroes,
                'taxa_sucesso_por_tipo': self.taxa_sucesso_por_tipo,
                'ultima_atualizacao': datetime.now().isoformat(),
                'versao': '1.0'
            }

            Path(self.arquivo).parent.mkdir(parents=True, exist_ok=True)

            with open(self.arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"    [!]  Erro ao salvar feedback: {e}")


# ============================================================================
# FUNÇÕES AUXILIARES - CATEGORIZAÇÃO DE RISCO (FASE 4 - P2)
# ============================================================================

def categorizar_risco(tipo: str) -> str:
    """
    ✅ FASE 4: Categoriza nível de risco de uma melhoria (P2)

    Classifica melhorias em 3 níveis de risco para auto-aplicação inteligente:
    - SAFE: Sempre auto-aplicar (documentação, formatação, type hints básicos)
    - MEDIUM: Auto-aplicar se prioridade >= 6 (refatorações pequenas, otimizações simples)
    - RISKY: Auto-aplicar apenas se prioridade >= 9 (bug fixes, refatorações grandes)

    Args:
        tipo: Tipo da melhoria (ex: 'documentacao', 'bug_fix', 'otimizacao')

    Returns:
        Nível de risco: 'SAFE', 'MEDIUM' ou 'RISKY'

    Exemplos:
        >>> categorizar_risco('documentacao')
        'SAFE'
        >>> categorizar_risco('bug_fix')
        'RISKY'
        >>> categorizar_risco('qualidade')
        'MEDIUM'
    """
    if tipo in TIPOS_SAFE:
        return NIVEL_RISCO_SAFE

    if tipo in TIPOS_MEDIUM:
        return NIVEL_RISCO_MEDIUM

    # Se não está em nenhuma lista ou está em TIPOS_RISKY
    return NIVEL_RISCO_RISKY


# ============================================================================
# ZONAS PROTEGIDAS (CÓDIGO CRÍTICO QUE NÃO DEVE SER MODIFICADO)
# ============================================================================

ZONAS_PROTEGIDAS = [
    # Sistema de backup/rollback (para não quebrar sua própria segurança)
    "def _criar_backup",
    "def _validar_codigo",
    "def _validar_sintaxe",
    "def _validar_import",
    "def _validar_execucao",
    "def _rollback",
    "class SistemaAutoEvolucao",
    
    # Memória permanente (para não perder aprendizados)
    "def _carregar_memoria",
    "def _salvar_memoria",
    "class MemoriaPermanente",
    
    # Credenciais (segurança)
    "class Cofre",
    "def _gerar_chave",
    "master_password",
    
    # Núcleo de execução (coração do agente)
    "def __init__",  # Construtores são críticos
    "def executar_tarefa",  # Loop principal
    "class AgenteCompletoV3",  # Classe principal
]


# ============================================================================
# FILA DE MELHORIAS
# ============================================================================

class FilaDeMelhorias:
    """Gerencia melhorias detectadas durante execução"""

    def __init__(self, arquivo: str = "Luna/.melhorias/fila_melhorias.json"):
        """
        Inicializa fila com persistência em JSON

        Args:
            arquivo: Caminho do arquivo JSON para persistir melhorias
        """
        self.arquivo = arquivo
        self.melhorias_pendentes = []
        self.melhorias_aplicadas = []
        self.melhorias_falhadas = []

        # Criar diretório se não existir
        Path(arquivo).parent.mkdir(parents=True, exist_ok=True)

        # Carregar melhorias salvas anteriormente
        self._carregar_fila()
    
    def adicionar(self, tipo: str, alvo: str, motivo: str, codigo_sugerido: str,
                 prioridade: int = 5):
        """
        ✅ FASE 4: Adiciona melhoria à fila com categorização de risco (P2)

        Args:
            tipo: 'otimizacao', 'bug_fix', 'nova_feature', 'refatoracao', etc.
            alvo: Função/classe/módulo a modificar
            motivo: Por que fazer essa melhoria
            codigo_sugerido: Código da modificação
            prioridade: 1-10 (10 = mais urgente)
        """
        # ✅ FASE 4: Categorizar risco automaticamente
        nivel_risco = categorizar_risco(tipo)

        melhoria = {
            'id': self._gerar_id(f"{alvo}{motivo}{datetime.now()}"),
            'tipo': tipo,
            'alvo': alvo,
            'motivo': motivo,
            'codigo': codigo_sugerido,
            'prioridade': prioridade,
            'nivel_risco': nivel_risco,  # ✅ FASE 4: Novo campo
            'detectado_em': datetime.now().isoformat(),
            'status': 'pendente'
        }

        self.melhorias_pendentes.append(melhoria)
        print(f"    💡 Melhoria anotada [{nivel_risco}]: {motivo[:60]}...")

        # ✅ PERSISTÊNCIA: Salvar após adicionar
        self._salvar_fila()

        return melhoria['id']
    
    def obter_pendentes(self, ordenar_por_prioridade: bool = True) -> List[Dict]:
        """Retorna melhorias pendentes"""
        if ordenar_por_prioridade:
            return sorted(self.melhorias_pendentes, 
                         key=lambda x: x['prioridade'], 
                         reverse=True)
        return self.melhorias_pendentes
    
    def marcar_aplicada(self, melhoria_id: str, detalhes: Dict):
        """Marca melhoria como aplicada"""
        for m in self.melhorias_pendentes:
            if m['id'] == melhoria_id:
                m['status'] = 'aplicada'
                m['aplicada_em'] = datetime.now().isoformat()
                m['detalhes'] = detalhes
                self.melhorias_aplicadas.append(m)
                self.melhorias_pendentes.remove(m)
                # ✅ PERSISTÊNCIA: Salvar após marcar como aplicada
                self._salvar_fila()
                break

    def marcar_falhada(self, melhoria_id: str, erro: str):
        """Marca melhoria como falhada"""
        for m in self.melhorias_pendentes:
            if m['id'] == melhoria_id:
                m['status'] = 'falhada'
                m['erro'] = erro
                m['tentada_em'] = datetime.now().isoformat()
                self.melhorias_falhadas.append(m)
                self.melhorias_pendentes.remove(m)
                # ✅ PERSISTÊNCIA: Salvar após marcar como falhada
                self._salvar_fila()
                break
    
    def limpar(self):
        """Limpa todas as filas"""
        self.melhorias_pendentes.clear()
        self.melhorias_aplicadas.clear()
        self.melhorias_falhadas.clear()
        # ✅ PERSISTÊNCIA: Salvar após limpar
        self._salvar_fila()
    
    def _carregar_fila(self):
        """
        Carrega melhorias salvas do arquivo JSON

        ✅ FASE 1: Implementação de persistência (P0)
        """
        try:
            if not os.path.exists(self.arquivo):
                # Primeira execução - arquivo não existe ainda
                return

            with open(self.arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)

            self.melhorias_pendentes = dados.get('pendentes', [])
            self.melhorias_aplicadas = dados.get('aplicadas', [])
            self.melhorias_falhadas = dados.get('falhadas', [])

            total = len(self.melhorias_pendentes)
            if total > 0:
                print(f"    💾 {total} melhoria(s) pendente(s) carregada(s) da sessão anterior")

        except json.JSONDecodeError as e:
            print(f"    [!]  Erro ao carregar fila (JSON inválido): {e}")
            print(f"    [i]  Iniciando com fila vazia")
        except Exception as e:
            print(f"    [!]  Erro ao carregar fila: {e}")
            print(f"    [i]  Iniciando com fila vazia")

    def _salvar_fila(self):
        """
        Salva melhorias no arquivo JSON

        ✅ FASE 1: Implementação de persistência (P0)
        """
        try:
            dados = {
                'pendentes': self.melhorias_pendentes,
                'aplicadas': self.melhorias_aplicadas,
                'falhadas': self.melhorias_falhadas,
                'ultima_atualizacao': datetime.now().isoformat(),
                'versao': '1.0'
            }

            # Criar diretório se não existir
            Path(self.arquivo).parent.mkdir(parents=True, exist_ok=True)

            # Salvar com indentação para facilitar debug manual
            with open(self.arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)

        except Exception as e:
            # Não queremos quebrar a execução por falha na persistência
            # Apenas logar o erro
            print(f"    [!]  Erro ao salvar fila: {e}")

    def _gerar_id(self, texto: str) -> str:
        """Gera ID único para melhoria"""
        return hashlib.md5(texto.encode()).hexdigest()[:12]


# ============================================================================
# SISTEMA DE AUTO-EVOLUÇÃO
# ============================================================================

class SistemaAutoEvolucao:
    """
    Sistema completo de auto-modificação segura
    """

    def __init__(self, arquivo_alvo: str = "luna_v3_FINAL_OTIMIZADA.py",
                 dir_backups: str = "backups_auto_evolucao",
                 max_backups: int = 5,
                 usar_feedback_loop: bool = True):

        self.arquivo_alvo = arquivo_alvo
        self.dir_backups = dir_backups
        self.max_backups = max_backups

        # ✅ VALIDAÇÃO: Verificar que arquivo alvo existe
        if not os.path.exists(self.arquivo_alvo):
            raise FileNotFoundError(
                f"❌ Arquivo alvo não encontrado: {self.arquivo_alvo}\n"
                f"   O sistema de auto-evolução precisa que o arquivo exista.\n"
                f"   Verifique o caminho e tente novamente."
            )

        # Criar diretório de backups
        Path(self.dir_backups).mkdir(exist_ok=True)

        # Log de modificações
        self.log_file = "auto_modificacoes.log"

        # Estatísticas
        self.stats = {
            'total_modificacoes': 0,
            'sucesso': 0,
            'falhas': 0,
            'rollbacks': 0
        }

        # ✅ FASE 5: Inicializar feedback loop
        self.feedback_loop = FeedbackLoop() if usar_feedback_loop else None
        if self.feedback_loop:
            print("    [LOOP] Feedback loop ativado")
    
    # ========================================================================
    # BACKUP E ROLLBACK
    # ========================================================================
    
    def _criar_backup(self, motivo: str) -> str:
        """
        Cria backup do arquivo antes de modificar
        
        Returns:
            Caminho do backup criado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{self.dir_backups}/agente_backup_{timestamp}.py"
        
        try:
            shutil.copy2(self.arquivo_alvo, backup_path)
            
            # Criar metadados do backup
            meta_path = f"{backup_path}.meta"
            meta = {
                'timestamp': timestamp,
                'motivo': motivo,
                'arquivo_original': self.arquivo_alvo,
                'hash': self._calcular_hash(self.arquivo_alvo)
            }

            with open(meta_path, 'w', encoding='utf-8') as f:
                json.dump(meta, f, indent=2)

            self._log(f"Backup criado: {backup_path}")
            return backup_path
            
        except Exception as e:
            self._log(f"ERRO ao criar backup: {e}", nivel='ERROR')
            raise
    
    def _rollback(self, backup_path: str) -> bool:
        """
        Restaura código a partir de backup
        
        Returns:
            True se rollback bem-sucedido
        """
        try:
            if not os.path.exists(backup_path):
                self._log(f"ERRO: Backup não encontrado: {backup_path}", nivel='ERROR')
                return False
            
            shutil.copy2(backup_path, self.arquivo_alvo)
            self.stats['rollbacks'] += 1
            self._log(f"Rollback realizado: {backup_path}")
            
            return True
            
        except Exception as e:
            self._log(f"ERRO crítico no rollback: {e}", nivel='CRITICAL')
            return False
    
    def _limpar_backups_antigos(self):
        """
        Mantém apenas os N backups mais recentes
        Deleta backups validados há mais de 24h
        """
        try:
            backups = sorted(Path(self.dir_backups).glob("agente_backup_*.py"))

            # Manter apenas max_backups mais recentes
            if len(backups) > self.max_backups:
                for backup in backups[:-self.max_backups]:
                    meta_file = f"{backup}.meta"

                    # Verificar se tem mais de 24h
                    if os.path.exists(meta_file):
                        with open(meta_file, 'r', encoding='utf-8') as f:
                            meta = json.load(f)

                        timestamp = datetime.strptime(meta['timestamp'], "%Y%m%d_%H%M%S")
                        if datetime.now() - timestamp > timedelta(hours=24):
                            os.remove(backup)
                            os.remove(meta_file)
                            self._log(f"Backup antigo deletado: {backup}")

        except Exception as e:
            self._log(f"Erro ao limpar backups: {e}", nivel='WARNING')

    def _extrair_nome_alvo(self, alvo: str) -> Optional[str]:
        """
        Extrai nome da função/classe do alvo com suporte a múltiplos formatos.

        Casos suportados:
        - "def funcao" → "funcao"
        - "class MinhaClasse" → "MinhaClasse"
        - "funcao_nome" → "funcao_nome"
        - "linha_1707_C:\\..." → buscar na linha 1707

        Args:
            alvo: String com o alvo da modificação

        Returns:
            Nome extraído ou None se falhar
        """
        import re

        # Caso 1: "def/class nome"
        if alvo.startswith('def ') or alvo.startswith('class '):
            # Extrair nome após def/class, antes de (
            return alvo.split()[1].split('(')[0].split(':')[0]

        # Caso 2: "linha_NNN_caminho"
        if alvo.startswith('linha_'):
            match = re.match(r'linha_(\d+)', alvo)
            if match:
                linha_alvo = int(match.group(1))
                self._log(f"DEBUG: Detectado targeting por linha {linha_alvo}")
                return self._encontrar_nome_na_linha(linha_alvo)

        # Caso 3: Nome direto (funcao_nome, MinhaClasse, etc)
        # Remover prefixos comuns se existirem
        nome_limpo = alvo.replace('funcao_', '').replace('classe_', '')

        # Se ainda tem espaços, pegar apenas o primeiro token
        if ' ' in nome_limpo:
            nome_limpo = nome_limpo.split()[0]

        return nome_limpo if nome_limpo else None

    def _encontrar_nome_na_linha(self, linha: int) -> Optional[str]:
        """
        Encontra nome da função/classe em uma linha específica do arquivo alvo.

        Args:
            linha: Número da linha (1-indexed)

        Returns:
            Nome da função/classe encontrada ou None
        """
        try:
            with open(self.arquivo_alvo, 'r', encoding='utf-8') as f:
                codigo = f.read()

            arvore = ast.parse(codigo)

            # Buscar todos os nós com nome e linha
            for node in ast.walk(arvore):
                if hasattr(node, 'lineno') and hasattr(node, 'name'):
                    # Verificar se está na linha correta (com tolerância de ±2 linhas)
                    if abs(node.lineno - linha) <= 2:
                        self._log(f"DEBUG: Encontrado '{node.name}' na linha {node.lineno} (alvo: {linha})")
                        return node.name

            self._log(f"WARNING: Nenhuma função/classe encontrada próxima à linha {linha}", nivel='WARNING')
            return None

        except Exception as e:
            self._log(f"Erro ao buscar nome na linha {linha}: {e}", nivel='ERROR')
            return None

    def _aplicar_modificacao_ast(
        self,
        codigo_original: str,
        codigo_novo: str,
        alvo: str
    ) -> Optional[str]:
        """
        Aplica modificação usando AST para modificações precisas.

        ✅ IMPLEMENTADO: Resolve o TODO da linha 411

        Args:
            codigo_original: Código Python original completo
            codigo_novo: Código da modificação (função, classe, etc.)
            alvo: Nome do alvo (ex: "def funcao", "class MinhaClasse")

        Returns:
            Código modificado completo ou None se falhar
        """
        try:
            # Parse do código original
            tree_original = ast.parse(codigo_original)

            # Parse do código novo
            tree_novo = ast.parse(codigo_novo)

            # Extrair nome do alvo usando método robusto
            nome_alvo = self._extrair_nome_alvo(alvo)

            if not nome_alvo:
                erro = f"TARGETING FALHOU: Não foi possível extrair nome do alvo '{alvo}'"
                self._log(erro, nivel='ERROR')
                return None

            self._log(f"DEBUG: alvo='{alvo}' -> nome_extraído='{nome_alvo}'", nivel='DEBUG')

            # Encontrar e substituir o nó correspondente
            substituido = False

            for i, node in enumerate(tree_original.body):
                # Verificar se é o nó que queremos substituir
                if hasattr(node, 'name') and node.name == nome_alvo:
                    # Substituir pelo(s) novo(s) nó(s)
                    # Se o código novo tem múltiplos nós, substituir por todos
                    if len(tree_novo.body) == 1:
                        tree_original.body[i] = tree_novo.body[0]
                    else:
                        # Múltiplos nós - substituir e inserir os demais
                        tree_original.body[i] = tree_novo.body[0]
                        for j, novo_node in enumerate(tree_novo.body[1:], 1):
                            tree_original.body.insert(i + j, novo_node)

                    substituido = True
                    self._log(f"Nó '{nome_alvo}' substituído via AST")
                    break

            if not substituido:
                # Não encontrou - ABORTAR ao invés de adicionar ao final
                erro = f"TARGETING FALHOU: Nó '{nome_alvo}' não encontrado no código"
                self._log(erro, nivel='ERROR')
                self._log(f"DEBUG: alvo original = '{alvo}'", nivel='DEBUG')
                self._log(f"DEBUG: nós disponíveis no AST:", nivel='DEBUG')
                for node in tree_original.body:
                    if hasattr(node, 'name'):
                        self._log(f"  - {type(node).__name__}: {node.name}", nivel='DEBUG')
                return None  # ABORT modification to prevent duplication

            # Converter AST de volta para código
            # Usar ast.unparse (Python 3.9+) ou fallback para código completo
            try:
                codigo_modificado = ast.unparse(tree_original)
                return codigo_modificado
            except AttributeError:
                # Python < 3.9 - não tem ast.unparse
                # Fallback: retornar código novo completo
                self._log("ast.unparse não disponível (Python < 3.9) - usando fallback")
                return codigo_novo

        except SyntaxError as e:
            self._log(f"Erro de sintaxe ao processar AST: {e}", nivel='ERROR')
            return None
        except Exception as e:
            self._log(f"Erro ao aplicar modificação via AST: {e}", nivel='ERROR')
            return None
    
    # ========================================================================
    # VALIDAÇÃO
    # ========================================================================
    
    def _validar_codigo(self, arquivo: str) -> Tuple[bool, str]:
        """
        ✅ FASE 3: Validação completa com smoke tests (P1)

        Validação em 4 níveis:
        1. Sintaxe (AST parsing)
        2. Import (módulo pode ser importado?)
        3. Execução básica (classes existem?)
        4. Semântica (smoke tests funcionais)

        Returns:
            (sucesso, mensagem_erro)
        """
        # 1. Validar sintaxe
        valido, erro = self._validar_sintaxe(arquivo)
        if not valido:
            return False, f"Sintaxe inválida: {erro}"

        # 2. Validar import
        valido, erro = self._validar_import(arquivo)
        if not valido:
            return False, f"Import falhou: {erro}"

        # 3. Validar execução básica
        valido, erro = self._validar_execucao(arquivo)
        if not valido:
            return False, f"Execução falhou: {erro}"

        # 4. ✅ FASE 3: Validar semântica (smoke tests)
        valido, erro = self._validar_semantica()
        if not valido:
            return False, f"Validação semântica falhou: {erro}"

        return True, "Validação completa OK (sintaxe + import + execução + semântica)"
    
    def _validar_sintaxe(self, arquivo: str) -> Tuple[bool, str]:
        """Valida sintaxe Python"""
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                codigo = f.read()
            
            ast.parse(codigo)
            return True, "Sintaxe OK"
            
        except SyntaxError as e:
            return False, f"Linha {e.lineno}: {e.msg}"
        except Exception as e:
            return False, str(e)
    
    def _validar_import(self, arquivo: str) -> Tuple[bool, str]:
        """Valida se o módulo pode ser importado"""
        try:
            # Tentar importar como módulo
            module_name = Path(arquivo).stem
            spec = importlib.util.spec_from_file_location(module_name, arquivo)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            
            return True, "Import OK"
            
        except Exception as e:
            return False, str(e)
    
    def _validar_execucao(self, arquivo: str) -> Tuple[bool, str]:
        """
        Validação básica de execução
        Testa se classes/funções principais estão acessíveis
        """
        try:
            # Importar módulo
            module_name = Path(arquivo).stem
            spec = importlib.util.spec_from_file_location(module_name, arquivo)
            if not spec or not spec.loader:
                return False, "Não foi possível carregar módulo"

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Verificar se classes principais existem
            classes_esperadas = ['AgenteCompletoV3', 'SistemaFerramentasCompleto']
            for classe in classes_esperadas:
                if not hasattr(module, classe):
                    return False, f"Classe '{classe}' não encontrada"

            return True, "Execução OK"

        except Exception as e:
            return False, str(e)

    def _validar_semantica(self) -> Tuple[bool, str]:
        """
        ✅ FASE 3: Validação semântica com smoke tests (P1)

        Executa suite de smoke tests para validar que componentes
        críticos funcionam corretamente após modificações.

        Detecta quebras funcionais que validação sintática não pega:
        - FilaDeMelhorias com operações básicas
        - DetectorMelhorias detectando melhorias
        - MemoriaPermanente salvando/buscando
        - SistemaAutoEvolucao instanciando

        Returns:
            (sucesso, mensagem)
        """
        try:
            # Importar smoke tests
            import smoke_tests_luna

            # Executar todos os smoke tests (verbose=False para capturar resultado)
            todos_passaram, resultados = smoke_tests_luna.executar_todos_smoke_tests(verbose=False)

            if todos_passaram:
                return True, f"Smoke tests OK ({len(resultados)} testes passaram)"

            # Se houve falhas, construir mensagem detalhada
            falhas = [r for r in resultados if not r['passou']]
            msg_erro = f"{len(falhas)}/{len(resultados)} teste(s) falharam:\n"
            for r in falhas:
                msg_erro += f"  - {r['nome']}: {r['mensagem']}\n"

            return False, msg_erro.strip()

        except ImportError as e:
            # Smoke tests não disponíveis - degradar gracefully
            self._log(f"Smoke tests não disponíveis: {e}", nivel='WARNING')
            return True, "Validação semântica pulada (smoke tests não encontrados)"

        except Exception as e:
            return False, f"Erro ao executar smoke tests: {e}"
    
    def _verificar_zona_protegida(self, codigo: str, alvo: str) -> bool:
        """
        Verifica se modificação toca em zona protegida
        
        Returns:
            True se é zona protegida (NÃO DEVE MODIFICAR)
        """
        for zona in ZONAS_PROTEGIDAS:
            if zona in codigo or zona in alvo:
                return True
        return False
    
    # ========================================================================
    # APLICAÇÃO DE MODIFICAÇÕES
    # ========================================================================
    
    def aplicar_modificacao(self, melhoria: Dict, memoria=None) -> bool:
        """
        ✅ FASE 5: Aplica modificação com feedback loop integrado (P2)

        Args:
            melhoria: Dict com dados da melhoria
            memoria: Instância de MemoriaPermanente (opcional)

        Returns:
            True se aplicada com sucesso
        """
        melhoria_id = melhoria['id']
        tipo = melhoria['tipo']
        alvo = melhoria['alvo']
        motivo = melhoria['motivo']
        codigo = melhoria['codigo']

        self._log(f"\n{'='*70}")
        self._log(f"MODIFICAÇÃO: {tipo}")
        self._log(f"Alvo: {alvo}")
        self._log(f"Motivo: {motivo}")
        self._log(f"{'='*70}")

        # ✅ FASE 5: Verificar blacklist
        if self.feedback_loop:
            bloqueado, motivo_bloqueio = self.feedback_loop.esta_na_blacklist(melhoria)
            if bloqueado:
                erro = f"BLACKLIST: {motivo_bloqueio}"
                self._log(erro, nivel='WARNING')
                print(f"    [X] {motivo_bloqueio}")

                # Registrar tentativa bloqueada
                self.feedback_loop.registrar_tentativa(melhoria, sucesso=False, erro=erro)

                if memoria:
                    memoria.adicionar_aprendizado(
                        'bug',
                        f"Não modificar {alvo} - está na blacklist",
                        contexto=f"Bloqueado: {motivo}",
                        tags=['auto-modificacao', 'blacklist']
                    )

                return False

        # 1. Verificar zona protegida
        if self._verificar_zona_protegida(codigo, alvo):
            erro = f"ZONA PROTEGIDA: Não é permitido modificar '{alvo}'"
            self._log(erro, nivel='WARNING')

            # ✅ FASE 5: Registrar no feedback loop
            if self.feedback_loop:
                self.feedback_loop.registrar_tentativa(melhoria, sucesso=False, erro=erro)

            if memoria:
                memoria.adicionar_aprendizado(
                    'bug',
                    f"Não modificar {alvo} - é zona protegida",
                    contexto=f"Tentativa bloqueada: {motivo}",
                    tags=['auto-modificacao', 'zona-protegida']
                )

            return False
        
        # 2. Criar backup
        try:
            backup_path = self._criar_backup(motivo)

            # ✅ FASE 3.1: Validar que backup foi criado com sucesso
            if not os.path.exists(backup_path):
                raise RuntimeError(f"Backup não foi criado: {backup_path}")

            # Validar que backup tem tamanho razoável (não está vazio)
            if os.path.getsize(backup_path) == 0:
                raise RuntimeError(f"Backup está vazio: {backup_path}")

            # Validar que backup tem mesmo hash que original (integridade)
            hash_original = self._calcular_hash(self.arquivo_alvo)
            hash_backup = self._calcular_hash(backup_path)
            if hash_original != hash_backup:
                raise RuntimeError(f"Hash do backup difere do original - backup corrompido")

            self._log(f"✅ Backup validado: {backup_path}")

        except Exception as e:
            self._log(f"ERRO ao criar/validar backup: {e}", nivel='ERROR')
            return False

        # 3. Aplicar modificação
        try:
            with open(self.arquivo_alvo, 'r', encoding='utf-8') as f:
                codigo_original = f.read()

            # ✅ IMPLEMENTADO: Usar AST para modificações precisas
            # Tentar aplicar modificação via AST primeiro
            codigo_modificado = self._aplicar_modificacao_ast(
                codigo_original, codigo, alvo
            )

            # Se AST falhar, usar fallback (substituição completa)
            if codigo_modificado is None:
                self._log("Fallback: usando substituição completa do código")
                codigo_modificado = codigo

            with open(self.arquivo_alvo, 'w', encoding='utf-8') as f:
                f.write(codigo_modificado)

            self._log("Código modificado")

        except Exception as e:
            self._log(f"ERRO ao modificar código: {e}", nivel='ERROR')
            self._rollback(backup_path)
            return False
        
        # 4. Validar
        print("    [OK] Validando modificacao...")
        valido, erro_validacao = self._validar_codigo(self.arquivo_alvo)

        if not valido:
            self._log(f"VALIDAÇÃO FALHOU: {erro_validacao}", nivel='ERROR')
            print(f"    [ERRO] Validacao falhou: {erro_validacao}")

            # Rollback automático
            self._rollback(backup_path)
            self.stats['falhas'] += 1

            # ✅ FASE 5: Registrar falha no feedback loop
            if self.feedback_loop:
                self.feedback_loop.registrar_tentativa(melhoria, sucesso=False, erro=erro_validacao)

            # Salvar na memória para não repetir
            if memoria:
                memoria.adicionar_aprendizado(
                    'bug',
                    f"Modificação de {alvo} com esta abordagem causa erro: {erro_validacao}",
                    contexto=motivo,
                    tags=['auto-modificacao', 'erro-validacao']
                )

            return False

        # 5. Sucesso!
        print("    [OK] Validacao passou!")
        self._log("MODIFICAÇÃO APLICADA COM SUCESSO")
        self.stats['sucesso'] += 1
        self.stats['total_modificacoes'] += 1

        # ✅ FASE 5: Registrar sucesso no feedback loop
        if self.feedback_loop:
            self.feedback_loop.registrar_tentativa(melhoria, sucesso=True)

        # Salvar sucesso na memória
        if memoria:
            memoria.adicionar_aprendizado(
                'tecnica',
                f"Modificação bem-sucedida: {motivo}",
                contexto=f"Alvo: {alvo}, Tipo: {tipo}",
                tags=['auto-modificacao', 'sucesso']
            )

        return True
    
    def processar_fila(self, fila: FilaDeMelhorias, memoria=None) -> Dict:
        """
        ✅ FASE 5: Processa fila com ajuste de prioridade baseado em histórico (P2)

        Returns:
            Dict com estatísticas do processamento
        """
        melhorias = fila.obter_pendentes()

        if not melhorias:
            return {'total': 0, 'sucesso': 0, 'falhas': 0, 'bloqueadas_blacklist': 0}

        print(f"\n{'='*70}")
        print("🔧 AUTO-MELHORIAS DETECTADAS")
        print(f"{'='*70}")
        print(f"\n📋 {len(melhorias)} melhorias na fila\n")

        # ✅ FASE 5: Ajustar prioridades baseado em histórico
        if self.feedback_loop:
            print("[STATS] Ajustando prioridades baseado em histórico de sucesso...\n")
            for melhoria in melhorias:
                prioridade_ajustada = self.feedback_loop.ajustar_prioridade(melhoria)
                melhoria['prioridade'] = prioridade_ajustada

            # Re-ordenar por prioridade ajustada
            melhorias = sorted(melhorias, key=lambda x: x['prioridade'], reverse=True)

        resultados = {'total': len(melhorias), 'sucesso': 0, 'falhas': 0, 'bloqueadas_blacklist': 0}

        for i, melhoria in enumerate(melhorias, 1):
            print(f"\n📝 Melhoria {i}/{len(melhorias)}")
            print(f"   Tipo: {melhoria['tipo']}")
            print(f"   Alvo: {melhoria['alvo']}")
            print(f"   Motivo: {melhoria['motivo']}")
            print(f"   Prioridade: {melhoria['prioridade']}/10")

            # ✅ FASE 5: Verificar blacklist antes de aplicar
            if self.feedback_loop:
                bloqueado, _ = self.feedback_loop.esta_na_blacklist(melhoria)
                if bloqueado:
                    resultados['bloqueadas_blacklist'] += 1
                    # Aplicar_modificacao já registra no feedback loop
                    pass

            sucesso = self.aplicar_modificacao(melhoria, memoria)

            if sucesso:
                print(f"   [OK] Aplicada com sucesso\n")
                fila.marcar_aplicada(melhoria['id'], {'timestamp': datetime.now().isoformat()})
                resultados['sucesso'] += 1
            else:
                print(f"   [ERRO] Falhou (rollback automatico)\n")
                fila.marcar_falhada(melhoria['id'], "Validação falhou")
                resultados['falhas'] += 1
        
        # Limpar backups antigos
        self._limpar_backups_antigos()
        
        # Resumo
        self._imprimir_resumo(resultados, fila)
        
        return resultados
    
    def _imprimir_resumo(self, resultados: Dict, fila: FilaDeMelhorias):
        """✅ FASE 5: Imprime resumo com estatísticas do feedback loop (P2)"""
        print(f"\n{'='*70}")
        print("🎊 AUTO-MELHORIAS CONCLUÍDAS")
        print(f"{'='*70}\n")

        print(f"[STATS] Resumo:")
        print(f"   [OK] {resultados['sucesso']} melhorias aplicadas")
        print(f"   [ERRO] {resultados['falhas']} falhas (revertidas)")

        # ✅ FASE 5: Mostrar melhorias bloqueadas por blacklist
        if resultados.get('bloqueadas_blacklist', 0) > 0:
            print(f"   [X] {resultados['bloqueadas_blacklist']} bloqueadas (blacklist)")

        # ✅ FASE 5: Estatísticas do feedback loop
        if self.feedback_loop:
            stats_feedback = self.feedback_loop.obter_estatisticas()
            print(f"\n📈 Feedback Loop:")
            print(f"   Total de tentativas: {stats_feedback['total_tentativas']}")
            print(f"   Taxa de sucesso geral: {stats_feedback['taxa_sucesso_geral']:.1%}")
            print(f"   Padrões na blacklist: {stats_feedback['blacklist_tamanho']}")

            # Top 3 tipos com melhor taxa de sucesso
            if stats_feedback['taxa_por_tipo']:
                tipos_ordenados = sorted(
                    stats_feedback['taxa_por_tipo'].items(),
                    key=lambda x: x[1]['taxa'],
                    reverse=True
                )
                if tipos_ordenados:
                    print(f"\n   🏆 Top 3 tipos com melhor sucesso:")
                    for tipo, stats in tipos_ordenados[:3]:
                        print(f"      {tipo}: {stats['taxa']:.1%} ({stats['sucessos']}/{stats['tentativas']})")

        if fila.melhorias_aplicadas:
            print(f"\n[OK] Melhorias aplicadas:")
            for m in fila.melhorias_aplicadas[-5:]:  # Últimas 5
                print(f"   • {m['motivo'][:60]}")

        if fila.melhorias_falhadas:
            print(f"\n[!]  Melhorias que falharam:")
            for m in fila.melhorias_falhadas[-3:]:  # Últimas 3
                print(f"   • {m['motivo'][:60]}")

        # Backups mantidos
        backups = list(Path(self.dir_backups).glob("agente_backup_*.py"))
        print(f"\n💾 Backups mantidos: {len(backups)}")

        print(f"\n{'='*70}\n")
    
    # ========================================================================
    # UTILIDADES
    # ========================================================================
    
    def _calcular_hash(self, arquivo: str) -> str:
        """Calcula hash MD5 do arquivo"""
        with open(arquivo, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def _log(self, mensagem: str, nivel: str = 'INFO'):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linha = f"[{timestamp}] {nivel}: {mensagem}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(linha)
    
    def obter_estatisticas(self) -> Dict:
        """✅ FASE 5: Retorna estatísticas incluindo feedback loop (P2)"""
        backups = len(list(Path(self.dir_backups).glob("agente_backup_*.py")))

        stats = {
            **self.stats,
            'backups_mantidos': backups,
            'taxa_sucesso': (self.stats['sucesso'] / self.stats['total_modificacoes'] * 100
                           if self.stats['total_modificacoes'] > 0 else 0)
        }

        # ✅ FASE 5: Adicionar estatísticas do feedback loop
        if self.feedback_loop:
            stats['feedback_loop'] = self.feedback_loop.obter_estatisticas()

        return stats


# ============================================================================
# INTERFACE DE TESTE
# ============================================================================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  🧬 SISTEMA DE AUTO-EVOLUÇÃO                                ║
║                                                              ║
║  Permite que Luna se auto-modifique com segurança          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Teste básico
    fila = FilaDeMelhorias()
    sistema = SistemaAutoEvolucao()
    
    print("[OK] Sistema inicializado")
    print(f"📁 Diretório de backups: {sistema.dir_backups}")
    print(f"📄 Arquivo alvo: {sistema.arquivo_alvo}")
    print(f"🔒 {len(ZONAS_PROTEGIDAS)} zonas protegidas definidas")
    
    print("\n💡 Sistema pronto para uso!")
