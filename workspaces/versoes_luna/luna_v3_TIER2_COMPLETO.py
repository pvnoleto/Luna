#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 LUNA V3 - COM TIER 2 CORRIGIDO + PLANEJAMENTO AVANÇADO + PROCESSAMENTO PARALELO
===================================================================================

✨ NOVIDADES DESTA VERSÃO:
1. ✅ LIMITES CORRETOS: Tier 2 = 1000 RPM, 450K ITPM, 90K OTPM (OFICIAL!)
2. 🧠 SISTEMA DE PLANEJAMENTO AVANÇADO: Planos detalhados antes de executar
3. 🔄 PROCESSAMENTO PARALELO AGRESSIVO: 15-20 tarefas simultâneas
4. 🛡️ ANTI-RATE LIMIT: Monitora e previne erros 429
5. 🔧 RECUPERAÇÃO INTELIGENTE: Prioriza corrigir erros
6. 🛑 HANDLER DE INTERRUPÇÃO: Ctrl+C tratado graciosamente

VALORES OFICIAIS DOS TIERS (Fonte: Alex Albert - Anthropic):
┌────────┬─────────┬────────────┬────────────┐
│ Tier   │ RPM     │ ITPM       │ OTPM       │
├────────┼─────────┼────────────┼────────────┤
│ Tier 1 │ 50      │ 30,000     │ 8,000      │
│ Tier 2 │ 1,000   │ 450,000    │ 90,000     │  ← CORRIGIDO!
│ Tier 3 │ 2,000   │ 800,000    │ 160,000    │  ← CORRIGIDO!
│ Tier 4 │ 4,000   │ 2,000,000  │ 400,000    │  ← CORRIGIDO!
└────────┴─────────┴────────────┴────────────┘

Versão: 2025-10-17 (Tier 2 Completo + Planejamento + Paralelismo)
"""

import anthropic
from anthropic import BadRequestError, RateLimitError
import os
import sys
import subprocess
import json
from dotenv import load_dotenv
from datetime import datetime, timedelta
import getpass
from pathlib import Path
import time
import signal
import atexit
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Configuração UTF-8
os.environ.setdefault("PYTHONUTF8", "1")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
os.environ["PYTHONUNBUFFERED"] = "1"

if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, 'reconfigure') else None
sys.stderr.reconfigure(line_buffering=True) if hasattr(sys.stderr, 'reconfigure') else None



# Importar sistema de auto-evolução
try:
    from sistema_auto_evolucao import FilaDeMelhorias, SistemaAutoEvolucao
    AUTO_EVOLUCAO_DISPONIVEL = True
except:
    AUTO_EVOLUCAO_DISPONIVEL = False
    print("⚠️  sistema_auto_evolucao.py não encontrado")

# Importar gerenciador de temporários
try:
    from gerenciador_temp import GerenciadorTemporarios
    GERENCIADOR_TEMP_DISPONIVEL = True
except:
    GERENCIADOR_TEMP_DISPONIVEL = False
    print("⚠️  gerenciador_temp.py não encontrado")

# Importar gerenciador de workspaces
try:
    from gerenciador_workspaces import GerenciadorWorkspaces
    GERENCIADOR_WORKSPACES_DISPONIVEL = True
except:
    GERENCIADOR_WORKSPACES_DISPONIVEL = False
    print("⚠️  gerenciador_workspaces.py não encontrado")

# Importar sistemas
try:
    from cofre_credenciais import Cofre
    COFRE_DISPONIVEL = True
except:
    COFRE_DISPONIVEL = False
    print("⚠️  cofre_credenciais.py não encontrado")

try:
    from memoria_permanente import MemoriaPermanente
    MEMORIA_DISPONIVEL = True
except:
    MEMORIA_DISPONIVEL = False
    print("⚠️  memoria_permanente.py não encontrado")

# ============================================================================
# CLASSES DE DADOS PARA PLANEJAMENTO
# ============================================================================

@dataclass
class Subtarefa:
    """Representa uma subtarefa executável"""
    id: str
    titulo: str
    descricao: str
    ferramentas: List[str]
    input_esperado: str
    output_esperado: str
    criterio_sucesso: str
    tokens_estimados: int
    tempo_estimado: str
    prioridade: str  # critica, importante, nice-to-have
    dependencias: List[str] = field(default_factory=list)
    concluida: bool = False
    resultado: Optional[str] = None


@dataclass
class Onda:
    """Representa uma onda de execução (subtarefas paralelas/sequenciais)"""
    numero: int
    descricao: str
    subtarefas: List[Subtarefa]
    pode_executar_paralelo: bool
    concluida: bool = False


@dataclass
class Plano:
    """Representa um plano completo de execução"""
    tarefa_original: str
    analise: Dict[str, Any]
    estrategia: Dict[str, Any]
    decomposicao: Dict[str, Any]
    ondas: List[Onda]
    criado_em: datetime
    executado_em: Optional[datetime] = None
    resultado: Optional[Dict[str, Any]] = None
    
    def salvar(self, caminho: str):
        """Salva o plano em arquivo JSON"""
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump({
                'tarefa_original': self.tarefa_original,
                'analise': self.analise,
                'estrategia': self.estrategia,
                'decomposicao': self.decomposicao,
                'criado_em': self.criado_em.isoformat(),
                'executado_em': self.executado_em.isoformat() if self.executado_em else None,
                'resultado': self.resultado
            }, f, indent=2, ensure_ascii=False)


# ============================================================================
# HANDLER DE INTERRUPÇÃO
# ============================================================================

class InterruptHandler:
    """Gerencia interrupções graciosamente"""
    
    def __init__(self, agente=None, sistema_ferramentas=None):
        self.agente = agente
        self.sistema_ferramentas = sistema_ferramentas
        self.interrompido = False
        self.limpeza_feita = False
        
        signal.signal(signal.SIGINT, self.handler_sigint)
        signal.signal(signal.SIGTERM, self.handler_sigterm)
        atexit.register(self.cleanup_final)
        
        print("✅ Handler de interrupção ativado (Ctrl+C será tratado graciosamente)")
    
    def handler_sigint(self, signum, frame):
        """Handler para Ctrl+C"""
        if self.interrompido:
            print("\n\n🔴 FORÇANDO SAÍDA... (segunda interrupção)")
            self.cleanup_forcado()
            sys.exit(1)
        
        self.interrompido = True
        print("\n\n⚠️  INTERRUPÇÃO DETECTADA (Ctrl+C)")
        print("   Limpando recursos... (Ctrl+C novamente para forçar saída)")
        
        self.cleanup_gracioso()
        sys.exit(0)
    
    def handler_sigterm(self, signum, frame):
        """Handler para SIGTERM"""
        print("\n\n⚠️  SIGTERM RECEBIDO")
        self.cleanup_gracioso()
        sys.exit(0)
    
    def cleanup_gracioso(self):
        """Limpeza graciosa de recursos"""
        if self.limpeza_feita:
            return
        
        print("\n📋 LIMPANDO RECURSOS:")
        
        if self.sistema_ferramentas:
            try:
                if hasattr(self.sistema_ferramentas, 'browser') and self.sistema_ferramentas.browser:
                    print("   🌐 Fechando navegador...")
                    self.sistema_ferramentas.executar('fechar_navegador', {})
                    print("   ✅ Navegador fechado")
            except Exception as e:
                print(f"   ⚠️  Erro ao fechar navegador: {e}")
        
        if self.agente and hasattr(self.agente, 'rate_limit_manager'):
            try:
                print("   📊 Salvando estatísticas...")
                stats = self.agente.rate_limit_manager.obter_estatisticas()
                
                stats_file = "Luna/.stats/rate_limit_interrupcao.json"
                os.makedirs(os.path.dirname(stats_file), exist_ok=True)
                
                with open(stats_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        'timestamp': datetime.now().isoformat(),
                        'stats': stats,
                        'motivo': 'interrupcao_ctrl_c'
                    }, f, indent=2)
                
                print(f"   ✅ Estatísticas salvas")
            except Exception as e:
                print(f"   ⚠️  Erro ao salvar stats: {e}")
        
        self.limpeza_feita = True
        print("\n✅ Limpeza concluída!")
    
    def cleanup_forcado(self):
        """Limpeza forçada"""
        print("🔴 SAÍDA FORÇADA - recursos podem não ser limpos!")
        if self.sistema_ferramentas and hasattr(self.sistema_ferramentas, 'browser'):
            try:
                if self.sistema_ferramentas.browser:
                    self.sistema_ferramentas.browser.close()
            except:
                pass
    
    def cleanup_final(self):
        """Cleanup final ao sair"""
        if not self.limpeza_feita:
            self.cleanup_gracioso()


# ============================================================================
# SISTEMA DE RATE LIMITING (COM LIMITES CORRETOS!)
# ============================================================================

class RateLimitManager:
    """Gerencia rate limits com valores OFICIAIS da Anthropic"""
    
    def __init__(self, tier: str = "tier1", modo: str = "balanceado"):
        # ✅ LIMITES CORRETOS (Fonte: Alex Albert - Anthropic)
        self.limites = {
            "tier1": {"rpm": 50, "itpm": 30000, "otpm": 8000},
            "tier2": {"rpm": 1000, "itpm": 450000, "otpm": 90000},      # ✅ CORRIGIDO!
            "tier3": {"rpm": 2000, "itpm": 800000, "otpm": 160000},     # ✅ CORRIGIDO!
            "tier4": {"rpm": 4000, "itpm": 2000000, "otpm": 400000}     # ✅ CORRIGIDO!
        }
        
        self.tier = tier
        self.limite_rpm = self.limites[tier]["rpm"]
        self.limite_itpm = self.limites[tier]["itpm"]
        self.limite_otpm = self.limites[tier]["otpm"]
        
        # Modos de operação
        self.modos = {
            "conservador": {"threshold": 0.75},
            "balanceado": {"threshold": 0.85},
            "agressivo": {"threshold": 0.95}
        }
        
        self.modo = modo
        self.threshold = self.modos[modo]["threshold"]
        
        # Tracking
        self.janela_tempo = timedelta(minutes=1)
        self.historico_requisicoes = []
        self.historico_tokens_input = []
        self.historico_tokens_output = []
        
        # Estatísticas
        self.total_requisicoes = 0
        self.total_tokens = 0
        self.total_esperas = 0
        self.tempo_total_espera = 0
        
        print(f"🛡️  Rate Limit Manager: {tier.upper()} - Modo {modo.upper()}", flush=True)
        print(f"   Limites: {self.limite_itpm:,} ITPM | {self.limite_otpm:,} OTPM | {self.limite_rpm} RPM", flush=True)
        print(f"   Threshold: {self.threshold*100:.0f}%", flush=True)
    
    def registrar_uso(self, tokens_input: int, tokens_output: int):
        """Registra uso de tokens e requisição"""
        agora = datetime.now()
        
        self.historico_requisicoes.append(agora)
        self.historico_tokens_input.append((agora, tokens_input))
        self.historico_tokens_output.append((agora, tokens_output))
        
        self.total_requisicoes += 1
        self.total_tokens += (tokens_input + tokens_output)
        
        self._limpar_historico_antigo(agora)
    
    def _limpar_historico_antigo(self, agora):
        """Remove entradas antigas do histórico"""
        limite_tempo = agora - self.janela_tempo
        
        self.historico_requisicoes = [t for t in self.historico_requisicoes if t > limite_tempo]
        self.historico_tokens_input = [(t, tokens) for t, tokens in self.historico_tokens_input if t > limite_tempo]
        self.historico_tokens_output = [(t, tokens) for t, tokens in self.historico_tokens_output if t > limite_tempo]
    
    def calcular_uso_atual(self):
        """Calcula uso atual (última janela de 1 min)"""
        agora = datetime.now()
        self._limpar_historico_antigo(agora)
        
        rpm_atual = len(self.historico_requisicoes)
        itpm_atual = sum(tokens for _, tokens in self.historico_tokens_input)
        otpm_atual = sum(tokens for _, tokens in self.historico_tokens_output)
        
        return {
            "rpm_atual": rpm_atual,
            "itpm_atual": itpm_atual,
            "otpm_atual": otpm_atual,
            "rpm_percent": (rpm_atual / self.limite_rpm) * 100,
            "itpm_percent": (itpm_atual / self.limite_itpm) * 100,
            "otpm_percent": (otpm_atual / self.limite_otpm) * 100,
            "rpm_disponivel": self.limite_rpm - rpm_atual,
            "itpm_disponivel": self.limite_itpm - itpm_atual,
            "otpm_disponivel": self.limite_otpm - otpm_atual
        }
    
    def estimar_tokens_proxima_req(self, tokens_input_estimados: int = None) -> Tuple[int, int]:
        """Estima tokens da próxima requisição"""
        if tokens_input_estimados is None:
            # Usar média recente
            if self.historico_tokens_input:
                tokens_input_estimados = int(sum(t for _, t in self.historico_tokens_input[-5:]) / min(5, len(self.historico_tokens_input[-5:])))
            else:
                tokens_input_estimados = 1000
        
        # Estimar output baseado no histórico
        if self.historico_tokens_output:
            tokens_output_estimados = int(sum(t for _, t in self.historico_tokens_output[-5:]) / min(5, len(self.historico_tokens_output[-5:])))
        else:
            tokens_output_estimados = 1000
        
        return tokens_input_estimados, tokens_output_estimados
    
    def precisa_esperar(self, tokens_input_estimados: int = None, tokens_output_estimados: int = None):
        """Verifica se precisa esperar antes de fazer requisição"""
        uso = self.calcular_uso_atual()
        
        tokens_input_est, tokens_output_est = self.estimar_tokens_proxima_req(tokens_input_estimados)
        
        if tokens_output_estimados is not None:
            tokens_output_est = tokens_output_estimados
        
        # Verificar thresholds
        rpm_ultrapassaria = (uso["rpm_atual"] + 1) > (self.limite_rpm * self.threshold)
        itpm_ultrapassaria = (uso["itpm_atual"] + tokens_input_est) > (self.limite_itpm * self.threshold)
        otpm_ultrapassaria = (uso["otpm_atual"] + tokens_output_est) > (self.limite_otpm * self.threshold)
        
        if rpm_ultrapassaria or itpm_ultrapassaria or otpm_ultrapassaria:
            if self.historico_requisicoes:
                tempo_mais_antigo = min(self.historico_requisicoes)
                tempo_passado = (datetime.now() - tempo_mais_antigo).total_seconds()
                tempo_espera = max(1, int(60 - tempo_passado + 1))
                
                motivos = []
                if rpm_ultrapassaria:
                    motivos.append(f"RPM: {uso['rpm_atual']+1}/{self.limite_rpm}")
                if itpm_ultrapassaria:
                    motivos.append(f"ITPM: {uso['itpm_atual']+tokens_input_est:,}/{self.limite_itpm:,}")
                if otpm_ultrapassaria:
                    motivos.append(f"OTPM: {uso['otpm_atual']+tokens_output_est:,}/{self.limite_otpm:,}")
                
                return True, tempo_espera, ", ".join(motivos)
            
            return True, 5, "Preventivo"
        
        return False, 0, None
    
    def aguardar_se_necessario(self, tokens_input_estimados: int = None, tokens_output_estimados: int = None):
        """Espera se necessário"""
        precisa, segundos, motivo = self.precisa_esperar(tokens_input_estimados, tokens_output_estimados)
        
        if precisa:
            uso = self.calcular_uso_atual()
            print(f"\n⏳ Aguardando {segundos}s para respeitar rate limit", flush=True)
            print(f"   Motivo: {motivo}", flush=True)
            print(f"   Uso atual: ITPM {uso['itpm_percent']:.1f}% | OTPM {uso['otpm_percent']:.1f}% | RPM {uso['rpm_percent']:.1f}%", flush=True)
            time.sleep(segundos)
            self.total_esperas += 1
            self.tempo_total_espera += segundos
    
    def exibir_status(self):
        """Mostra status atual"""
        uso = self.calcular_uso_atual()
        
        def barra(percent):
            largura = 20
            preenchido = int((min(percent, 100) / 100) * largura)
            barra_str = "█" * preenchido + "░" * (largura - preenchido)
            
            if percent > 95:
                cor = "🔴"
            elif percent > 85:
                cor = "🟡"
            else:
                cor = "🟢"
            
            return f"{cor} {barra_str} {min(percent, 100):.1f}%"
        
        print(f"\n📊 STATUS DO RATE LIMIT:", flush=True)
        print(f"   ITPM: {barra(uso['itpm_percent'])} ({uso['itpm_atual']:,}/{self.limite_itpm:,})", flush=True)
        print(f"   OTPM: {barra(uso['otpm_percent'])} ({uso['otpm_atual']:,}/{self.limite_otpm:,})", flush=True)
        print(f"   RPM:  {barra(uso['rpm_percent'])} ({uso['rpm_atual']}/{self.limite_rpm})", flush=True)
    
    def obter_estatisticas(self):
        """Retorna estatísticas gerais"""
        return {
            "total_requisicoes": self.total_requisicoes,
            "total_tokens": self.total_tokens,
            "total_esperas": self.total_esperas,
            "tempo_total_espera": self.tempo_total_espera,
            "media_tokens_req": self.total_tokens / max(1, self.total_requisicoes),
        }


# ============================================================================
# SISTEMA DE PLANEJAMENTO AVANÇADO
# ============================================================================

class PlanificadorAvancado:
    """
    Sistema de planejamento em 3 fases:
    1. ANÁLISE: Entende a tarefa profundamente (~30k tokens)
    2. ESTRATÉGIA: Cria plano otimizado (~20k tokens)
    3. DECOMPOSIÇÃO: Divide em subtarefas paralelas (~15k tokens)
    """
    
    def __init__(self, agente):
        self.agente = agente
        self.historico_planos = []
        self.metricas = {
            'planos_criados': 0,
            'taxa_sucesso': 0,
            'tempo_medio_economizado': 0
        }
    
    def planejar(self, tarefa: str, contexto: dict = None) -> Plano:
        """Cria um plano detalhado de execução"""
        print("\n🧠 SISTEMA DE PLANEJAMENTO ATIVADO")
        print("="*70)
        
        # Fase 1: ANÁLISE PROFUNDA (~30k tokens)
        print("\n📊 FASE 1: Análise Profunda da Tarefa...", flush=True)
        analise = self._analisar_tarefa(tarefa, contexto)
        
        # Fase 2: ESTRATÉGIA (~20k tokens)
        print("\n🎯 FASE 2: Criação de Estratégia Otimizada...", flush=True)
        estrategia = self._criar_estrategia(tarefa, analise)
        
        # Fase 3: DECOMPOSIÇÃO (~15k tokens)
        print("\n📋 FASE 3: Decomposição em Subtarefas...", flush=True)
        decomposicao = self._decompor_em_subtarefas(estrategia)
        
        # Criar ondas de execução
        ondas = self._criar_ondas(decomposicao)
        
        # Criar objeto Plano
        plano = Plano(
            tarefa_original=tarefa,
            analise=analise,
            estrategia=estrategia,
            decomposicao=decomposicao,
            ondas=ondas,
            criado_em=datetime.now()
        )
        
        self.historico_planos.append(plano)
        self.metricas['planos_criados'] += 1
        
        print(f"\n✅ PLANO CRIADO!")
        print(f"   Subtarefas: {len([st for onda in ondas for st in onda.subtarefas])}")
        print(f"   Ondas de execução: {len(ondas)}")
        
        return plano
    
    def _analisar_tarefa(self, tarefa: str, contexto: dict) -> dict:
        """Fase 1: Análise profunda da tarefa"""
        prompt = f"""ANÁLISE PROFUNDA DA TAREFA

Tarefa solicitada:
{tarefa}

Contexto adicional:
{json.dumps(contexto, indent=2) if contexto else 'Nenhum'}

Faça uma análise EXTREMAMENTE detalhada e retorne JSON:

{{
    "requisitos_explicitos": ["lista de requisitos mencionados diretamente"],
    "requisitos_implicitos": ["lista de requisitos não mencionados mas necessários"],
    "dependencias": {{
        "ferramentas": ["lista de ferramentas necessárias"],
        "bibliotecas": ["lista de bibliotecas Python necessárias"],
        "arquivos": ["lista de arquivos necessários"]
    }},
    "riscos": [
        {{"descricao": "...", "probabilidade": "alta/media/baixa", "impacto": "alto/medio/baixo"}}
    ],
    "estimativa_complexidade": "simples/media/complexa/muito_complexa",
    "tempo_estimado": "tempo estimado total",
    "conhecimento_previo_relevante": ["aprendizados relevantes"]
}}

Responda APENAS com o JSON, sem texto adicional."""

        resultado = self.agente._executar_requisicao_simples(prompt, max_tokens=4096)
        
        try:
            # Limpar markdown se houver
            resultado_limpo = resultado.strip()
            if resultado_limpo.startswith("```json"):
                resultado_limpo = resultado_limpo[7:]
            if resultado_limpo.endswith("```"):
                resultado_limpo = resultado_limpo[:-3]
            
            return json.loads(resultado_limpo.strip())
        except:
            return {
                "requisitos_explicitos": [tarefa],
                "requisitos_implicitos": [],
                "dependencias": {"ferramentas": [], "bibliotecas": [], "arquivos": []},
                "riscos": [],
                "estimativa_complexidade": "media",
                "tempo_estimado": "desconhecido"
            }
    
    def _criar_estrategia(self, tarefa: str, analise: dict) -> dict:
        """Fase 2: Criação de estratégia otimizada"""
        prompt = f"""CRIAÇÃO DE ESTRATÉGIA OTIMIZADA

Tarefa original:
{tarefa}

Análise realizada:
{json.dumps(analise, indent=2)}

Crie a melhor estratégia de execução e retorne JSON:

{{
    "abordagem": "descrição da abordagem principal",
    "justificativa": "por que esta abordagem é a melhor",
    "sequencia_otima": [
        {{"ordem": 1, "acao": "descrição da ação", "razao": "por que fazer primeiro"}}
    ],
    "oportunidades_paralelizacao": [
        {{"acoes": ["acao1", "acao2"], "ganho_estimado": "estimativa de ganho"}}
    ],
    "pontos_validacao": [
        {{"apos": "qual ação", "validar": "o que validar", "criterio_sucesso": "como saber que está certo"}}
    ],
    "planos_contingencia": ["plano B caso algo falhe"]
}}

Responda APENAS com o JSON, sem texto adicional."""

        resultado = self.agente._executar_requisicao_simples(prompt, max_tokens=4096)
        
        try:
            resultado_limpo = resultado.strip()
            if resultado_limpo.startswith("```json"):
                resultado_limpo = resultado_limpo[7:]
            if resultado_limpo.endswith("```"):
                resultado_limpo = resultado_limpo[:-3]
            
            return json.loads(resultado_limpo.strip())
        except:
            return {
                "abordagem": "execução direta",
                "justificativa": "abordagem simples",
                "sequencia_otima": [],
                "oportunidades_paralelizacao": [],
                "pontos_validacao": []
            }
    
    def _decompor_em_subtarefas(self, estrategia: dict) -> dict:
        """Fase 3: Decomposição em subtarefas executáveis"""
        prompt = f"""DECOMPOSIÇÃO EM SUBTAREFAS EXECUTÁVEIS

Estratégia definida:
{json.dumps(estrategia, indent=2)}

Decomponha em subtarefas CONCRETAS e EXECUTÁVEIS. Retorne JSON:

{{
    "ondas": [
        {{
            "numero": 1,
            "descricao": "descrição da onda",
            "subtarefas": [
                {{
                    "id": "1.1",
                    "titulo": "título curto",
                    "descricao": "descrição detalhada",
                    "ferramentas": ["lista de ferramentas"],
                    "input": "input esperado",
                    "output_esperado": "output esperado",
                    "criterio_sucesso": "como validar",
                    "tokens_estimados": 5000,
                    "tempo_estimado": "30s",
                    "prioridade": "critica",
                    "dependencias": []
                }}
            ],
            "pode_executar_paralelo": true
        }}
    ],
    "total_subtarefas": 0,
    "tempo_estimado_sequencial": "tempo",
    "tempo_estimado_paralelo": "tempo"
}}

Responda APENAS com o JSON, sem texto adicional."""

        resultado = self.agente._executar_requisicao_simples(prompt, max_tokens=4096)
        
        try:
            resultado_limpo = resultado.strip()
            if resultado_limpo.startswith("```json"):
                resultado_limpo = resultado_limpo[7:]
            if resultado_limpo.endswith("```"):
                resultado_limpo = resultado_limpo[:-3]
            
            decomp = json.loads(resultado_limpo.strip())
            # Atualizar total
            decomp['total_subtarefas'] = sum(len(onda.get('subtarefas', [])) for onda in decomp.get('ondas', []))
            return decomp
        except Exception as e:
            print(f"   ⚠️  Erro ao parsear decomposição: {e}")
            return {
                "ondas": [],
                "total_subtarefas": 0,
                "tempo_estimado_sequencial": "desconhecido",
                "tempo_estimado_paralelo": "desconhecido"
            }
    
    def _criar_ondas(self, decomposicao: dict) -> List[Onda]:
        """Cria objetos Onda a partir da decomposição"""
        ondas = []
        
        for onda_dict in decomposicao.get('ondas', []):
            subtarefas = []
            
            for st_dict in onda_dict.get('subtarefas', []):
                subtarefa = Subtarefa(
                    id=st_dict.get('id', ''),
                    titulo=st_dict.get('titulo', ''),
                    descricao=st_dict.get('descricao', ''),
                    ferramentas=st_dict.get('ferramentas', []),
                    input_esperado=st_dict.get('input', ''),
                    output_esperado=st_dict.get('output_esperado', ''),
                    criterio_sucesso=st_dict.get('criterio_sucesso', ''),
                    tokens_estimados=st_dict.get('tokens_estimados', 5000),
                    tempo_estimado=st_dict.get('tempo_estimado', '30s'),
                    prioridade=st_dict.get('prioridade', 'importante'),
                    dependencias=st_dict.get('dependencias', [])
                )
                subtarefas.append(subtarefa)
            
            onda = Onda(
                numero=onda_dict.get('numero', 0),
                descricao=onda_dict.get('descricao', ''),
                subtarefas=subtarefas,
                pode_executar_paralelo=onda_dict.get('pode_executar_paralelo', False)
            )
            ondas.append(onda)
        
        return ondas
    
    def executar_plano(self, plano: Plano) -> dict:
        """Executa o plano criado"""
        print("\n🚀 EXECUTANDO PLANO...")
        print("="*70)
        
        resultados = {}
        falhas = []
        
        for onda in plano.ondas:
            print(f"\n🌊 ONDA {onda.numero}: {onda.descricao}")
            print(f"   Subtarefas: {len(onda.subtarefas)}")
            print(f"   Paralelo: {'✅' if onda.pode_executar_paralelo else '❌'}")
            
            if onda.pode_executar_paralelo and len(onda.subtarefas) > 1:
                # Usar processador paralelo
                if hasattr(self.agente, 'processador_paralelo'):
                    resultados_onda = self.agente.processador_paralelo._processar_ondas_paralelas([onda])
                else:
                    # Fallback: execução sequencial
                    resultados_onda = self._executar_onda_sequencial(onda)
            else:
                resultados_onda = self._executar_onda_sequencial(onda)
            
            # Processar resultados
            for subtarefa_id, resultado in resultados_onda.items():
                if resultado.get('sucesso'):
                    resultados[subtarefa_id] = resultado
                    print(f"   ✅ {subtarefa_id}: Concluída")
                else:
                    falhas.append({
                        'subtarefa_id': subtarefa_id,
                        'erro': resultado.get('erro'),
                        'onda': onda.numero
                    })
                    print(f"   ❌ {subtarefa_id}: Falhou - {resultado.get('erro', 'erro desconhecido')}")
        
        resultado_final = {
            'sucesso': len(falhas) == 0,
            'total_subtarefas': sum(len(o.subtarefas) for o in plano.ondas),
            'concluidas': len(resultados),
            'falhas': len(falhas),
            'resultados': resultados,
            'detalhes_falhas': falhas
        }
        
        print("\n" + "="*70)
        if resultado_final['sucesso']:
            print("🎉 PLANO EXECUTADO COM SUCESSO!")
        else:
            print(f"⚠️  PLANO PARCIALMENTE EXECUTADO ({resultado_final['concluidas']}/{resultado_final['total_subtarefas']})")
        
        return resultado_final
    
    def _executar_onda_sequencial(self, onda: Onda) -> dict:
        """Executa ondas sequencialmente"""
        resultados = {}
        
        for st in onda.subtarefas:
            try:
                prompt = f"""SUBTAREFA {st.id}: {st.titulo}

DESCRIÇÃO:
{st.descricao}

INPUT:
{st.input_esperado}

OUTPUT ESPERADO:
{st.output_esperado}

CRITÉRIO DE SUCESSO:
{st.criterio_sucesso}

Execute esta subtarefa de forma completa e precisa."""
                
                resultado_texto = self.agente._executar_requisicao_simples(prompt, max_tokens=2048)
                
                resultados[st.id] = {
                    'sucesso': True,
                    'output': resultado_texto
                }
            except Exception as e:
                resultados[st.id] = {
                    'sucesso': False,
                    'erro': str(e)
                }
        
        return resultados


# ============================================================================
# PROCESSADOR PARALELO AGRESSIVO
# ============================================================================

class ProcessadorParalelo:
    """Executa múltiplas tarefas simultaneamente (Tier 2: 15-20 workers)"""
    
    def __init__(self, agente, max_workers: int = 15):
        self.agente = agente
        self.max_workers = max_workers
        self.semaphore = threading.Semaphore(max_workers)
        self.estatisticas = {
            'tarefas_processadas': 0,
            'tempo_total_economizado': 0
        }
    
    def processar_lista(self, tarefas: List[str]) -> List[str]:
        """Processa lista de tarefas em paralelo"""
        print(f"\n🚀 PROCESSAMENTO PARALELO INICIADO")
        print(f"   Total tarefas: {len(tarefas)}")
        print(f"   Workers: {self.max_workers}")
        print("="*70)
        
        inicio = time.time()
        resultados = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._processar_tarefa, tarefa): i
                for i, tarefa in enumerate(tarefas)
            }
            
            for future in as_completed(futures):
                idx = futures[future]
                try:
                    resultado = future.result()
                    resultados.append((idx, resultado))
                    print(f"   ✅ Tarefa {idx+1}/{len(tarefas)} concluída")
                except Exception as e:
                    print(f"   ❌ Tarefa {idx+1}/{len(tarefas)} falhou: {e}")
                    resultados.append((idx, {'erro': str(e)}))
        
        # Ordenar por índice original
        resultados.sort(key=lambda x: x[0])
        resultados = [r[1] for r in resultados]
        
        tempo_total = time.time() - inicio
        tempo_sequencial_estimado = len(tarefas) * 30
        tempo_economizado = tempo_sequencial_estimado - tempo_total
        
        self.estatisticas['tarefas_processadas'] += len(tarefas)
        self.estatisticas['tempo_total_economizado'] += tempo_economizado
        
        print(f"\n✅ PROCESSAMENTO PARALELO CONCLUÍDO!")
        print(f"   Tempo: {tempo_total:.1f}s")
        print(f"   Tempo economizado: {tempo_economizado:.1f}s")
        print(f"   Speedup: {tempo_sequencial_estimado/tempo_total:.1f}x")
        
        return resultados
    
    def _processar_tarefa(self, tarefa: str) -> str:
        """Processa uma tarefa individual"""
        with self.semaphore:
            return self.agente._executar_requisicao_simples(tarefa, max_tokens=2048)
    
    def _processar_ondas_paralelas(self, ondas: List[Onda]) -> dict:
        """Processa ondas de subtarefas em paralelo"""
        resultados = {}
        
        for onda in ondas:
            if onda.pode_executar_paralelo and len(onda.subtarefas) > 1:
                with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    futures = {
                        executor.submit(self._executar_subtarefa, st): st.id
                        for st in onda.subtarefas
                    }
                    
                    for future in as_completed(futures):
                        subtarefa_id = futures[future]
                        try:
                            resultado = future.result()
                            resultados[subtarefa_id] = resultado
                        except Exception as e:
                            resultados[subtarefa_id] = {
                                'sucesso': False,
                                'erro': str(e)
                            }
            else:
                # Execução sequencial
                for st in onda.subtarefas:
                    resultados[st.id] = self._executar_subtarefa(st)
        
        return resultados
    
    def _executar_subtarefa(self, subtarefa: Subtarefa) -> dict:
        """Executa uma subtarefa"""
        try:
            prompt = f"""SUBTAREFA {subtarefa.id}: {subtarefa.titulo}

{subtarefa.descricao}

Execute de forma completa e precisa."""
            
            resultado = self.agente._executar_requisicao_simples(prompt, max_tokens=2048)
            
            return {
                'sucesso': True,
                'output': resultado
            }
        except Exception as e:
            return {
                'sucesso': False,
                'erro': str(e)
            }


# ============================================================================
# SISTEMA DE FERRAMENTAS (PLACEHOLDER - USAR CÓDIGO COMPLETO ORIGINAL)
# ============================================================================

class SistemaFerramentasCompleto:
    """Sistema de ferramentas com TODAS as capacidades"""
    
    def __init__(self, master_password: str = None, usar_memoria: bool = True):
        self.ferramentas_codigo = {}
        self.ferramentas_descricao = []
        self.historico = []
        self.browser = None
        self.page = None
        
        # Auto-evolução
        self.auto_evolucao_disponivel = AUTO_EVOLUCAO_DISPONIVEL
        self.fila_melhorias = FilaDeMelhorias() if AUTO_EVOLUCAO_DISPONIVEL else None
        self.sistema_evolucao = SistemaAutoEvolucao() if AUTO_EVOLUCAO_DISPONIVEL else None
        
        # Gerenciador de temporários
        self.gerenciador_temp_disponivel = GERENCIADOR_TEMP_DISPONIVEL
        self.gerenciador_temp = GerenciadorTemporarios() if GERENCIADOR_TEMP_DISPONIVEL else None
        
        # Gerenciador de workspaces
        self.gerenciador_workspaces_disponivel = GERENCIADOR_WORKSPACES_DISPONIVEL
        self.gerenciador_workspaces = GerenciadorWorkspaces() if GERENCIADOR_WORKSPACES_DISPONIVEL else None
                  
        # Cofre de credenciais
        self.cofre = None
        self.cofre_disponivel = False
        if COFRE_DISPONIVEL and master_password:
            try:
                self.cofre = Cofre()
                self.cofre.inicializar(master_password)
                self.cofre_disponivel = True
            except Exception as e:
                print(f"⚠️  Cofre não disponível: {e}")
        
        # Memória permanente
        self.memoria = None
        self.memoria_disponivel = False
        if MEMORIA_DISPONIVEL and usar_memoria:
            try:
                self.memoria = MemoriaPermanente()
                self.memoria_disponivel = True
            except Exception as e:
                print(f"⚠️  Memória não disponível: {e}")
        
        # Carregar ferramentas
        self._carregar_ferramentas_base()
    
    def _carregar_ferramentas_base(self):
        """Todas as ferramentas base"""
        
        # BASH - ✅ CORRIGIDO COM ENCODING
        self.adicionar_ferramenta(
            "bash_avancado",
            '''def bash_avancado(comando: str, timeout: int = 60) -> str:
    import subprocess, os
    print(f"  ⚡ Bash: {comando[:70]}...", flush=True)
    try:
        resultado = subprocess.run(
            comando, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout, 
            cwd=os.getcwd(), 
            encoding="utf-8",
            errors="replace"
        )
        saida = f"STDOUT:\\n{resultado.stdout}\\nSTDERR:\\n{resultado.stderr}\\nCODE: {resultado.returncode}"
        print(f"  ✓ Concluído (código {resultado.returncode})", flush=True)
        return saida[:3000]
    except Exception as e:
        print(f"  ✗ ERRO: {str(e)[:50]}", flush=True)
        return f"ERRO: {e}"''',
            "Executa comandos bash/terminal",
            {"comando": {"type": "string"}, "timeout": {"type": "integer"}}
        )
        
        # ARQUIVOS
        self.adicionar_ferramenta(
            "criar_arquivo",
            '''def criar_arquivo(caminho: str, conteudo: str) -> str:
    from pathlib import Path
    print(f"  📝 Criando: {Path(caminho).name}")
    try:
        global _gerenciador_workspaces
        if _gerenciador_workspaces:
            caminho_completo = _gerenciador_workspaces.resolver_caminho(caminho)
        else:
            caminho_completo = caminho
        
        Path(caminho_completo).parent.mkdir(parents=True, exist_ok=True)
        with open(caminho_completo, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        print(f"  ✓ Arquivo criado: {Path(caminho_completo).name}")
        return f"Arquivo '{caminho}' criado em: {caminho_completo}"
    except Exception as e:
        print(f"  ✗ ERRO: {str(e)[:50]}")
        return f"ERRO: {e}"''',
            "Cria arquivo. Se workspace estiver selecionado, cria no workspace atual automaticamente.",
            {"caminho": {"type": "string"}, "conteudo": {"type": "string"}}
        )
        
        self.adicionar_ferramenta(
            "ler_arquivo",
            '''def ler_arquivo(caminho: str) -> str:
    print(f"  📖 Lendo: {caminho}")
    try:
        global _gerenciador_workspaces
        if _gerenciador_workspaces:
            try:
                caminho_completo = _gerenciador_workspaces.resolver_caminho(caminho)
            except:
                caminho_completo = caminho
        else:
            caminho_completo = caminho
        
        with open(caminho_completo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        print(f"  ✓ Lido ({len(conteudo)} caracteres)")
        return conteudo[:5000]
    except Exception as e:
        print(f"  ✗ ERRO: {str(e)[:50]}")
        return f"ERRO: {e}"''',
            "Lê arquivo. Busca no workspace atual se disponível.",
            {"caminho": {"type": "string"}}
        )
        
        # GERENCIAMENTO DE TEMPORÁRIOS
        if self.gerenciador_temp_disponivel:
            self.adicionar_ferramenta(
                "marcar_temporario",
                '''def marcar_temporario(caminho: str, forcar: bool = False) -> str:
    print(f"  🗑️  Marcando temporário: {caminho}")
    try:
        global _gerenciador_temp
        sucesso = _gerenciador_temp.marcar_temporario(caminho, forcar)
        if sucesso:
            print(f"  ✓ Marcado (delete em 30 dias)")
            return f"Arquivo '{caminho}' marcado como temporário. Será deletado em 30 dias se não for usado."
        else:
            print(f"  ⚠️  Não pode ser marcado (protegido)")
            return f"Arquivo '{caminho}' não pode ser marcado (protegido ou não é temporário)"
    except Exception as e:
        return f"ERRO: {e}"''',
                "Marca arquivo como temporário para auto-limpeza em 30 dias.",
                {"caminho": {"type": "string"}, "forcar": {"type": "boolean"}}
            )
            
            self.adicionar_ferramenta(
                "listar_temporarios",
                '''def listar_temporarios() -> str:
    print(f"  📋 Listando temporários...")
    try:
        global _gerenciador_temp
        temporarios = _gerenciador_temp.listar_temporarios()
        
        if not temporarios:
            return "Nenhum arquivo temporário no momento"
        
        resultado = f"Total: {len(temporarios)} arquivo(s) temporário(s)\\n\\n"
        for arq in temporarios[:20]:
            resultado += f"- {arq['nome']} ({arq['tamanho_mb']:.2f} MB)\\n"
            resultado += f"  Delete em: {arq['dias_restantes']} dias\\n"
            resultado += f"  Motivo: {arq['motivo']}\\n\\n"
        
        if len(temporarios) > 20:
            resultado += f"... e mais {len(temporarios) - 20} arquivo(s)"
        
        print(f"  ✓ {len(temporarios)} encontrados")
        return resultado
    except Exception as e:
        return f"ERRO: {e}"''',
                "Lista todos arquivos temporários",
                {}
            )
            
            self.adicionar_ferramenta(
                "status_temporarios",
                '''def status_temporarios() -> str:
    print(f"  📊 Status de temporários...")
    try:
        global _gerenciador_temp
        stats = _gerenciador_temp.obter_estatisticas()
        
        resultado = "STATUS DO GERENCIADOR DE TEMPORÁRIOS\\n\\n"
        resultado += f"Arquivos temporários: {stats['arquivos_temporarios_atuais']}\\n"
        resultado += f"Arquivos protegidos: {stats['arquivos_protegidos']}\\n"
        resultado += f"Total deletados: {stats['total_deletados']}\\n"
        resultado += f"Total resgatados: {stats['total_resgatados']}\\n"
        resultado += f"Taxa de resgate: {stats['taxa_resgate_percent']:.1f}%\\n"
        resultado += f"Espaço liberado: {stats['espaco_liberado_mb']:.2f} MB"
        
        print(f"  ✓ Status obtido")
        return resultado
    except Exception as e:
        return f"ERRO: {e}"''',
                "Mostra estatísticas do gerenciador de temporários",
                {}
            )
        
        # GERENCIAMENTO DE WORKSPACES
        if self.gerenciador_workspaces_disponivel:
            self.adicionar_ferramenta(
                "criar_workspace",
                '''def criar_workspace(nome: str, descricao: str = "") -> str:
    print(f"  📁 Criando workspace: {nome}")
    try:
        global _gerenciador_workspaces
        sucesso, mensagem = _gerenciador_workspaces.criar_workspace(nome, descricao)
        if sucesso:
            _gerenciador_workspaces.selecionar_workspace(nome)
            print(f"  ✓ Workspace '{nome}' criado e selecionado")
            return mensagem + f"\\nWorkspace '{nome}' está selecionado. Novos arquivos serão criados nele."
        return mensagem
    except Exception as e:
        return f"ERRO: {e}"''',
                "Cria novo workspace (projeto) em Luna/workspaces/nome/",
                {"nome": {"type": "string"}, "descricao": {"type": "string"}}
            )
            
            self.adicionar_ferramenta(
                "listar_workspaces",
                '''def listar_workspaces() -> str:
    print(f"  📂 Listando workspaces...")
    try:
        global _gerenciador_workspaces
        workspaces = _gerenciador_workspaces.listar_workspaces()
        
        if not workspaces:
            return "Nenhum workspace criado ainda. Use criar_workspace('nome') para criar."
        
        resultado = f"Total: {len(workspaces)} workspace(s)\\n\\n"
        for ws in workspaces:
            marcador = "🎯 " if ws['atual'] else "   "
            resultado += f"{marcador}{ws['nome']}"
            if ws['descricao']:
                resultado += f" - {ws['descricao']}"
            resultado += f"\\n   {ws['path_relativo']}\\n"
            resultado += f"   {ws.get('arquivos', 0)} arquivo(s) - {ws['tamanho_mb']:.2f} MB\\n\\n"
        
        print(f"  ✓ {len(workspaces)} workspace(s) encontrados")
        return resultado
    except Exception as e:
        return f"ERRO: {e}"''',
                "Lista todos workspaces criados",
                {}
            )
            
            self.adicionar_ferramenta(
                "selecionar_workspace",
                '''def selecionar_workspace(nome: str) -> str:
    print(f"  🎯 Selecionando: {nome}")
    try:
        global _gerenciador_workspaces
        sucesso, mensagem = _gerenciador_workspaces.selecionar_workspace(nome)
        if sucesso:
            ws = _gerenciador_workspaces.get_workspace_atual()
            print(f"  ✓ Workspace selecionado")
            return mensagem + f"\\nNovos arquivos serão criados em: {ws['path_relativo']}"
        return mensagem
    except Exception as e:
        return f"ERRO: {e}"''',
                "Seleciona workspace como atual",
                {"nome": {"type": "string"}}
            )
            
            self.adicionar_ferramenta(
                "listar_arquivos_workspace",
                '''def listar_arquivos_workspace() -> str:
    print(f"  📑 Listando arquivos do workspace...")
    try:
        global _gerenciador_workspaces
        ws = _gerenciador_workspaces.get_workspace_atual()
        if not ws:
            return "Nenhum workspace selecionado. Use selecionar_workspace() primeiro."
        
        arquivos = _gerenciador_workspaces.listar_arquivos()
        
        if not arquivos:
            return f"Workspace '{ws['nome']}' está vazio."
        
        resultado = f"Workspace: {ws['nome']}\\n"
        resultado += f"{ws['path_relativo']}\\n\\n"
        resultado += f"{len(arquivos)} arquivo(s):\\n\\n"
        
        for arq in arquivos[:50]:
            tamanho_kb = arq.stat().st_size / 1024
            resultado += f"  - {arq.name} ({tamanho_kb:.2f} KB)\\n"
        
        if len(arquivos) > 50:
            resultado += f"\\n... e mais {len(arquivos) - 50} arquivo(s)"
        
        print(f"  ✓ {len(arquivos)} arquivo(s) listados")
        return resultado
    except Exception as e:
        return f"ERRO: {e}"''',
                "Lista arquivos do workspace atual",
                {}
            )
            
            self.adicionar_ferramenta(
                "buscar_arquivo_workspace",
                '''def buscar_arquivo_workspace(nome: str) -> str:
    print(f"  🔍 Buscando: {nome}")
    try:
        global _gerenciador_workspaces
        resultado = _gerenciador_workspaces.buscar_arquivo(nome)
        if resultado:
            print(f"  ✓ Arquivo encontrado")
            return f"Arquivo encontrado: {resultado}"
        print(f"  ⚠️  Arquivo não encontrado")
        return f"Arquivo '{nome}' não encontrado no workspace atual"
    except Exception as e:
        return f"ERRO: {e}"''',
                "Busca arquivo no workspace atual pelo nome",
                {"nome": {"type": "string"}}
            )
            
            self.adicionar_ferramenta(
                "arvore_workspace",
                '''def arvore_workspace(max_nivel: int = 3) -> str:
    print(f"  🌳 Gerando árvore do workspace...")
    try:
        global _gerenciador_workspaces
        _gerenciador_workspaces.exibir_arvore(max_nivel=max_nivel)
        return "Árvore exibida acima"
    except Exception as e:
        return f"ERRO: {e}"''',
                "Mostra estrutura de arquivos do workspace atual",
                {"max_nivel": {"type": "integer"}}
            )
            
            self.adicionar_ferramenta(
                "status_workspace",
                '''def status_workspace() -> str:
    print(f"  📊 Status dos workspaces...")
    try:
        global _gerenciador_workspaces
        _gerenciador_workspaces.exibir_status()
        return "Status exibido acima"
    except Exception as e:
        return f"ERRO: {e}"''',
                "Mostra status geral de todos workspaces",
                {}
            )
        
        # PLAYWRIGHT
        self.adicionar_ferramenta(
            "instalar_playwright",
            '''def instalar_playwright() -> str:
    import subprocess
    print("  📦 Instalando Playwright...")
    try:
        subprocess.run("pip install playwright", shell=True, timeout=120, 
                      encoding="utf-8", errors="replace")
        subprocess.run("playwright install chromium", shell=True, timeout=300,
                      encoding="utf-8", errors="replace")
        print("  ✓ Playwright instalado")
        return "Playwright instalado!"
    except Exception as e:
        return f"ERRO: {e}"''',
            "Instala Playwright",
            {}
        )
        
        self.adicionar_ferramenta(
            "iniciar_navegador",
            '''def iniciar_navegador(headless: bool = True) -> str:
    print("  🌐 Iniciando navegador...")
    try:
        from playwright.sync_api import sync_playwright
        global _playwright_instance, _browser, _page
        _playwright_instance = sync_playwright().start()
        _browser = _playwright_instance.chromium.launch(headless=headless)
        _page = _browser.new_page()
        print("  ✓ Navegador pronto")
        return "Navegador iniciado!"
    except Exception as e:
        return f"ERRO: {e}"''',
            "Inicia navegador Playwright",
            {"headless": {"type": "boolean"}}
        )
        
        self.adicionar_ferramenta(
            "navegar_url",
            '''def navegar_url(url: str) -> str:
    print(f"  🌐 Navegando: {url[:50]}...")
    try:
        global _page
        _page.goto(url, timeout=30000)
        titulo = _page.title()
        print(f"  ✓ Página: {titulo[:50]}")
        return f"Navegado para '{url}'"
    except Exception as e:
        return f"ERRO: {e}"''',
            "Navega para URL",
            {"url": {"type": "string"}}
        )
        
        self.adicionar_ferramenta(
            "tirar_screenshot",
            '''def tirar_screenshot(caminho: str = "screenshot.png") -> str:
    print(f"  📸 Screenshot: {caminho}")
    try:
        global _page, _gerenciador_workspaces
        
        if _gerenciador_workspaces:
            caminho_completo = _gerenciador_workspaces.resolver_caminho(caminho)
        else:
            caminho_completo = caminho
        
        _page.screenshot(path=caminho_completo)
        print(f"  ✓ Salvo")
        return f"Screenshot salvo: {caminho_completo}"
    except Exception as e:
        return f"ERRO: {e}"''',
            "Tira screenshot da página atual",
            {"caminho": {"type": "string"}}
        )
        
        self.adicionar_ferramenta(
            "clicar_elemento",
            '''def clicar_elemento(seletor: str) -> str:
    print(f"  👆 Clicando: {seletor[:40]}...")
    try:
        global _page
        _page.click(seletor, timeout=5000)
        print(f"  ✓ Clicado")
        return f"Clicado em '{seletor}'"
    except Exception as e:
        return f"ERRO: {e}"''',
            "Clica em elemento",
            {"seletor": {"type": "string"}}
        )
        
        self.adicionar_ferramenta(
            "preencher_campo",
            '''def preencher_campo(seletor: str, valor: str) -> str:
    print(f"  ✏️  Preenchendo: {seletor[:40]}...")
    try:
        global _page
        _page.fill(seletor, valor, timeout=5000)
        print(f"  ✓ Preenchido")
        return "Campo preenchido"
    except Exception as e:
        return f"ERRO: {e}"''',
            "Preenche campo",
            {"seletor": {"type": "string"}, "valor": {"type": "string"}}
        )
        
        self.adicionar_ferramenta(
            "fechar_navegador",
            '''def fechar_navegador() -> str:
    print("  🌐 Fechando navegador...")
    try:
        global _browser, _page, _playwright_instance
        if _page: _page.close()
        if _browser: _browser.close()
        if _playwright_instance: _playwright_instance.stop()
        _page = _browser = _playwright_instance = None
        print("  ✓ Navegador fechado")
        return "Navegador fechado"
    except Exception as e:
        return f"ERRO: {e}"''',
            "Fecha navegador",
            {}
        )
        
        # CREDENCIAIS
        if self.cofre_disponivel:
            self.adicionar_ferramenta(
                "obter_credencial",
                '''def obter_credencial(servico: str) -> str:
    print(f"  🔑 Obtendo credencial: {servico}")
    try:
        global _cofre
        import json
        cred = _cofre.obter_credencial(servico)
        print(f"  ✓ Obtida para: {cred['usuario']}")
        return json.dumps(cred)
    except Exception as e:
        return f"ERRO: {e}"''',
                "Obtém credencial do cofre",
                {"servico": {"type": "string"}}
            )
            
            self.adicionar_ferramenta(
                "login_automatico",
                '''def login_automatico(servico: str, url_login: str = None) -> str:
    print(f"  🔐 Login em: {servico}")
    try:
        global _cofre, _page
        cred = _cofre.obter_credencial(servico)
        usuario = cred['usuario']
        senha = cred['senha']
        extras = cred.get('extras', {})
        
        url = url_login or extras.get('url_login')
        if not url:
            return "ERRO: URL não fornecida"
        
        sel_user = extras.get('seletor_usuario', 'input[type="email"]')
        sel_pass = extras.get('seletor_senha', 'input[type="password"]')
        sel_btn = extras.get('seletor_botao', 'button[type="submit"]')
        
        _page.goto(url, timeout=30000)
        _page.fill(sel_user, usuario, timeout=10000)
        _page.fill(sel_pass, senha, timeout=10000)
        _page.click(sel_btn, timeout=10000)
        _page.wait_for_load_state('networkidle', timeout=15000)
        
        print(f"  ✓ Login realizado")
        return f"Login em '{servico}' realizado!"
    except Exception as e:
        return f"ERRO: {e}"''',
                "Faz login automático",
                {"servico": {"type": "string"}, "url_login": {"type": "string"}}
            )
        
        # MEMÓRIA
        if self.memoria_disponivel:
            self.adicionar_ferramenta(
                "salvar_aprendizado",
                '''def salvar_aprendizado(categoria: str, conteudo: str, tags: str = "") -> str:
    print(f"  💾 Salvando: {categoria}")
    try:
        global _memoria
        tags_list = [t.strip() for t in tags.split(",")] if tags else []
        _memoria.adicionar_aprendizado(categoria, conteudo, tags=tags_list)
        print(f"  ✓ Aprendizado salvo")
        return f"Aprendizado salvo em '{categoria}'"
    except Exception as e:
        return f"ERRO: {e}"''',
                "Salva aprendizado na memória permanente",
                {"categoria": {"type": "string"}, "conteudo": {"type": "string"}, "tags": {"type": "string"}}
            )
            
            self.adicionar_ferramenta(
                "buscar_aprendizados",
                '''def buscar_aprendizados(query: str = "", categoria: str = "") -> str:
    print(f"  🔍 Buscando: {query or 'todos'}")
    try:
        global _memoria
        resultados = _memoria.buscar_aprendizados(
            query=query if query else None,
            categoria=categoria if categoria else None,
            limite=5
        )
        
        if not resultados:
            return "Nenhum aprendizado encontrado"
        
        texto = f"Encontrados {len(resultados)} aprendizados:\\n"
        for r in resultados:
            texto += f"- [{r['categoria']}] {r['conteudo']}\\n"
        
        print(f"  ✓ {len(resultados)} encontrados")
        return texto
    except Exception as e:
        return f"ERRO: {e}"''',
                "Busca aprendizados salvos",
                {"query": {"type": "string"}, "categoria": {"type": "string"}}
            )
            
            self.adicionar_ferramenta(
                "salvar_preferencia",
                '''def salvar_preferencia(chave: str, valor: str) -> str:
    print(f"  ⚙️  Preferência: {chave}")
    try:
        global _memoria
        _memoria.salvar_preferencia(chave, valor)
        print(f"  ✓ Salva")
        return f"Preferência '{chave}' salva"
    except Exception as e:
        return f"ERRO: {e}"''',
                "Salva preferência do usuário",
                {"chave": {"type": "string"}, "valor": {"type": "string"}}
            )
        
        # AUTO-EVOLUÇÃO
        if self.auto_evolucao_disponivel:
            self.adicionar_ferramenta(
                "anotar_melhoria",
                '''def anotar_melhoria(tipo: str, alvo: str, motivo: str, codigo_sugerido: str, prioridade: int = 5) -> str:
    print(f"  📝 Melhoria: {tipo}")
    try:
        global _fila_melhorias
        melhoria_id = _fila_melhorias.adicionar(tipo, alvo, motivo, codigo_sugerido, prioridade)
        return f"Melhoria anotada (ID: {melhoria_id})! Será aplicada após conclusão da tarefa atual."
    except Exception as e:
        return f"ERRO: {e}"''',
                "Anota melhoria para aplicar depois",
                {
                    "tipo": {"type": "string", "enum": ["otimizacao", "bug_fix", "nova_feature", "refatoracao"]},
                    "alvo": {"type": "string"},
                    "motivo": {"type": "string"},
                    "codigo_sugerido": {"type": "string"},
                    "prioridade": {"type": "integer"}
                }
            )
        
        # META-FERRAMENTAS
        self.adicionar_ferramenta(
            "criar_ferramenta",
            '''def criar_ferramenta(nome: str, codigo_python: str, descricao: str, parametros_json: str) -> str:
    import json
    print(f"  🔧 Nova ferramenta: {nome}")
    try:
        global _nova_ferramenta_info
        _nova_ferramenta_info = {
            'nome': nome,
            'codigo': codigo_python,
            'descricao': descricao,
            'parametros': json.loads(parametros_json)
        }
        print(f"  ✓ Ferramenta '{nome}' criada")
        return f"Ferramenta '{nome}' criada!"
    except Exception as e:
        return f"ERRO: {e}"''',
            "Cria nova ferramenta dinamicamente",
            {"nome": {"type": "string"}, "codigo_python": {"type": "string"}, 
             "descricao": {"type": "string"}, "parametros_json": {"type": "string"}}
        )
        
        self.adicionar_ferramenta(
            "alterar_limite_iteracoes",
            '''def alterar_limite_iteracoes(novo_limite: int) -> str:
    print(f"  ⚙️  Limite: {novo_limite}")
    try:
        global _novo_limite_iteracoes
        if novo_limite < 10:
            return "ERRO: Limite mínimo é 10 iterações"
        if novo_limite > 200:
            return "ERRO: Limite máximo é 200 iterações"
        
        _novo_limite_iteracoes = novo_limite
        print(f"  ✓ Limite atualizado")
        return f"Limite de iterações alterado para {novo_limite}. Efeito imediato!"
    except Exception as e:
        return f"ERRO: {e}"''',
            "Altera o limite máximo de iterações",
            {"novo_limite": {"type": "integer"}}
        )
        
        self.adicionar_ferramenta(
            "instalar_biblioteca",
            '''def instalar_biblioteca(nome_pacote: str) -> str:
    import subprocess
    print(f"  📦 Instalando: {nome_pacote}")
    try:
        resultado = subprocess.run(
            f"pip install {nome_pacote}", 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=120, 
            encoding="utf-8",
            errors="replace"
        )
        if resultado.returncode == 0:
            print(f"  ✓ '{nome_pacote}' instalado")
            return f"'{nome_pacote}' instalado!"
        return f"ERRO: {resultado.stderr[:500]}"
    except Exception as e:
        return f"ERRO: {e}"''',
            "Instala biblioteca Python via pip",
            {"nome_pacote": {"type": "string"}}
        )
    
    def adicionar_ferramenta(self, nome: str, codigo: str, descricao: str, parametros: dict):
        """Adiciona ferramenta ao sistema"""
        self.ferramentas_codigo[nome] = codigo
        
        properties = {}
        for param_name, param_def in parametros.items():
            if isinstance(param_def, dict):
                properties[param_name] = param_def
            else:
                properties[param_name] = {"type": "string"}
        
        tool_desc = {
            "name": nome,
            "description": descricao,
            "input_schema": {
                "type": "object",
                "properties": properties,
                "required": list(parametros.keys()) if parametros else []
            }
        }
        
        self.ferramentas_descricao = [t for t in self.ferramentas_descricao if t["name"] != nome]
        self.ferramentas_descricao.append(tool_desc)
        
        if self.memoria_disponivel and nome not in ["salvar_aprendizado", "buscar_aprendizados", "salvar_preferencia"]:
            self.memoria.registrar_ferramenta_criada(nome, descricao, codigo)
    
    def executar(self, nome: str, parametros: dict) -> str:
        """Executa ferramenta"""
        if nome not in self.ferramentas_codigo:
            return f"ERRO: Ferramenta '{nome}' não existe"
        
        try:
            namespace = {
                '_nova_ferramenta_info': None,
                '_novo_limite_iteracoes': None,
                '_fila_melhorias': self.fila_melhorias,
                '_gerenciador_temp': self.gerenciador_temp,
                '_gerenciador_workspaces': self.gerenciador_workspaces,
                '_playwright_instance': None,
                '_browser': self.browser,
                '_page': self.page,
                '_cofre': self.cofre,
                '_memoria': self.memoria,
                '__builtins__': __builtins__,
                'os': __import__('os')
            }
            
            exec(self.ferramentas_codigo[nome], namespace)
            
            func = None
            for key, value in namespace.items():
                if callable(value) and key == nome:
                    func = value
                    break
            
            if not func:
                return f"ERRO: Função não encontrada"
            
            resultado = func(**parametros)
            
            if '_browser' in namespace:
                self.browser = namespace['_browser']
            if '_page' in namespace:
                self.page = namespace['_page']
            
            if nome == "criar_ferramenta" and namespace['_nova_ferramenta_info']:
                info = namespace['_nova_ferramenta_info']
                self.adicionar_ferramenta(
                    info['nome'], info['codigo'], info['descricao'], info['parametros']
                )
            
            novo_limite = namespace.get('_novo_limite_iteracoes')
            if novo_limite:
                return (str(resultado), novo_limite)
            
            return str(resultado)
            
        except Exception as e:
            import traceback
            erro_completo = traceback.format_exc()
            print(f"  ✗ ERRO CRÍTICO: {str(e)[:100]}")
            return f"ERRO: {erro_completo[:1000]}"
    
    def obter_descricoes(self) -> list:
        return self.ferramentas_descricao

# ============================================================================
# AGENTE COMPLETO COM TODAS AS FUNCIONALIDADES
# ============================================================================

class AgenteComTier2Completo:
    """Agente com Tier 2, Planejamento Avançado e Processamento Paralelo"""
    
    def __init__(
        self, 
        api_key: str, 
        master_password: str = None, 
        usar_memoria: bool = True,
        tier: str = "tier2",
        modo_rate_limit: str = "agressivo",
        usar_planejamento: bool = True,
        usar_paralelismo: bool = True
    ):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.sistema_ferramentas = SistemaFerramentasCompleto(master_password, usar_memoria)
        self.historico_conversa = []
        self.max_iteracoes_atual = 40
        
        # Rate limit manager com modo configurável
        self.rate_limit_manager = RateLimitManager(tier=tier, modo=modo_rate_limit)
        
        # Sistema de planejamento
        self.usar_planejamento = usar_planejamento
        self.planificador = PlanificadorAvancado(self) if usar_planejamento else None
        
        # Sistema de paralelismo
        self.usar_paralelismo = usar_paralelismo
        # Tier 2: 15-20 workers
        max_workers = 15 if tier == "tier2" else (20 if tier in ["tier3", "tier4"] else 5)
        self.processador_paralelo = ProcessadorParalelo(self, max_workers=max_workers) if usar_paralelismo else None
        
        # Sistema de recuperação de erros
        self.modo_recuperacao = False
        self.erros_recentes = []
    
    def _executar_requisicao_simples(self, prompt: str, max_tokens: int = 4096) -> str:
        """Executa uma requisição simples à API"""
        self.rate_limit_manager.aguardar_se_necessario()
        
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Registrar uso
            tokens_input = response.usage.input_tokens
            tokens_output = response.usage.output_tokens
            self.rate_limit_manager.registrar_uso(tokens_input, tokens_output)
            
            # Extrair texto
            texto = ""
            for block in response.content:
                if hasattr(block, "text"):
                    texto += block.text
            
            return texto
            
        except RateLimitError as e:
            print(f"\n⚠️  RATE LIMIT ATINGIDO! Aguardando 60s...")
            time.sleep(60)
            return self._executar_requisicao_simples(prompt, max_tokens)
        except Exception as e:
            return f"ERRO: {e}"
    
    def _tarefa_e_complexa(self, tarefa: str) -> bool:
        """Detecta se tarefa é complexa o suficiente para planejamento"""
        indicadores_complexidade = [
            'criar', 'desenvolver', 'implementar', 'sistema', 'completo',
            'api', 'aplicação', 'projeto', 'arquitetura', 'integrar',
            'múltiplos', 'vários', 'todos', 'completo', 'end-to-end'
        ]
        
        tarefa_lower = tarefa.lower()
        matches = sum(1 for ind in indicadores_complexidade if ind in tarefa_lower)
        
        return matches >= 2 or len(tarefa) > 200
    
    def executar_tarefa(self, tarefa: str, max_iteracoes: int = None, usar_planejamento_forcado: bool = None):
        """Executa tarefa com planejamento e paralelismo"""
        
        if max_iteracoes is None:
            max_iteracoes = self.max_iteracoes_atual
        
        print("\n" + "="*70)
        print(f"🎯 TAREFA: {tarefa}")
        print("="*70)
        
        # Decidir se usa planejamento
        usar_plan = usar_planejamento_forcado if usar_planejamento_forcado is not None else (
            self.usar_planejamento and self._tarefa_e_complexa(tarefa)
        )
        
        if usar_plan and self.planificador:
            print("\n🧠 Tarefa complexa detectada. Ativando sistema de planejamento...")
            
            # Criar plano
            plano = self.planificador.planejar(tarefa)
            
            # Salvar plano
            plano_path = f"Luna/planos/plano_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            plano.salvar(plano_path)
            print(f"   💾 Plano salvo em: {plano_path}")
            
            # Executar plano
            resultado = self.planificador.executar_plano(plano)
            
            return resultado
        else:
            # Execução normal (sem planejamento)
            print("\n⚡ Execução direta (sem planejamento)")
            resultado = self._executar_requisicao_simples(tarefa, max_tokens=4096)
            
            print("\n" + "="*70)
            print("✅ CONCLUÍDO!")
            print("="*70)
            print(resultado)
            
            return resultado


# ============================================================================
# INTERFACE PRINCIPAL
# ============================================================================

def main():
    print("""
════════════════════════════════════════════════════════════════════════════════

  🌙 LUNA V3 - TIER 2 COMPLETO + PLANEJAMENTO + PARALELISMO

  ✅ Limites corretos (1000 RPM, 450K ITPM, 90K OTPM)
  🧠 Sistema de Planejamento Avançado
  🔄 Processamento Paralelo (15-20 tarefas simultâneas)
  🛡️ Rate Limiting Inteligente
  🛑 Handler de Interrupção (Ctrl+C)

════════════════════════════════════════════════════════════════════════════════
    """)
    
    # ✅ CORREÇÃO CRÍTICA: Carregar variáveis de ambiente do .env
    load_dotenv()
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ Configure ANTHROPIC_API_KEY no .env")
        return
    
    # Configurar tier
    print("\n🛡️  CONFIGURAÇÃO")
    print("   Qual é o seu tier da API Anthropic?")
    print("   1. Tier 1 (50 RPM, 30K ITPM, 8K OTPM)")
    print("   2. Tier 2 (1000 RPM, 450K ITPM, 90K OTPM) ← RECOMENDADO")
    print("   3. Tier 3 (2000 RPM, 800K ITPM, 160K OTPM)")
    print("   4. Tier 4 (4000 RPM, 2M ITPM, 400K OTPM)")
    
    tier_input = input("\n   Escolha (1-4, Enter=2): ").strip()
    tier_map = {"1": "tier1", "2": "tier2", "3": "tier3", "4": "tier4", "": "tier2"}
    tier = tier_map.get(tier_input, "tier2")
    
    # Configurar modo
    print("\n   Modo de rate limiting:")
    print("   1. Conservador (75% threshold)")
    print("   2. Balanceado (85% threshold)")
    print("   3. Agressivo (95% threshold) ← RECOMENDADO para Tier 2+")
    
    modo_input = input("\n   Escolha (1-3, Enter=3): ").strip()
    modo_map = {"1": "conservador", "2": "balanceado", "3": "agressivo", "": "agressivo"}
    modo = modo_map.get(modo_input, "agressivo")
    
    # Criar agente
    try:
        agente = AgenteComTier2Completo(
            api_key, 
            tier=tier,
            modo_rate_limit=modo,
            usar_planejamento=True,
            usar_paralelismo=True
        )
    except Exception as e:
        print(f"\n❌ Erro ao criar agente: {e}")
        return
    
    # Criar handler de interrupção
    handler = InterruptHandler(agente=agente, sistema_ferramentas=agente.sistema_ferramentas)
    
    print("\n✅ Luna V3 iniciada!")
    print("   🧠 Sistema de Planejamento: ATIVADO")
    print("   🔄 Processamento Paralelo: ATIVADO")
    print(f"   🛡️  Rate Limit: {tier.upper()} - {modo.upper()}")
    
    print("\n💡 DICA: Para tarefas complexas, a Luna criará um plano detalhado antes de executar!")
    print("🛑 DICA: Pressione Ctrl+C para interromper graciosamente")
    
    # Loop principal
    while True:
        try:
            print("\n" + "─"*70)
            comando = input("\n💬 O que você quer? (ou 'sair'): ").strip()
            
            if comando.lower() in ['sair', 'exit', 'quit', '']:
                print("\n👋 Até logo!")
                
                # Estatísticas finais
                print("\n📊 ESTATÍSTICAS FINAIS:")
                stats = agente.rate_limit_manager.obter_estatisticas()
                print(f"   Requisições: {stats['total_requisicoes']}")
                print(f"   Tokens: {stats['total_tokens']:,}")
                print(f"   Média tokens/req: {stats['media_tokens_req']:.0f}")
                if stats['total_esperas'] > 0:
                    print(f"   Esperas: {stats['total_esperas']} ({stats['tempo_total_espera']:.0f}s total)")
                
                if agente.planificador:
                    print(f"\n   🧠 Planos criados: {agente.planificador.metricas['planos_criados']}")
                
                if agente.processador_paralelo:
                    print(f"   🔄 Tarefas paralelas: {agente.processador_paralelo.estatisticas['tarefas_processadas']}")
                
                break
            
            # Executar tarefa
            agente.executar_tarefa(comando)
            input("\n⏸️  Pressione ENTER para continuar...")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
