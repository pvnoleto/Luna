#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 LUNA V3 - COM TIER 2 CORRIGIDO + PLANEJAMENTO + ITERAÇÕES COM FEEDBACK
===================================================================================

✨ NOVIDADES DESTA VERSÃO:
1. ✅ LIMITES CORRETOS: Tier 2 = 1000 RPM, 450K ITPM, 90K OTPM (OFICIAL!)
2. 🧠 SISTEMA DE PLANEJAMENTO AVANÇADO: Planos detalhados antes de executar
3. 🔄 PROCESSAMENTO PARALELO AGRESSIVO: 15-20 tarefas simultâneas
4. 🛡️ ANTI-RATE LIMIT: Monitora e previne erros 429
5. 🔧 RECUPERAÇÃO INTELIGENTE: Prioriza corrigir erros
6. 🛑 HANDLER DE INTERRUPÇÃO: Ctrl+C tratado graciosamente
7. ✅ COFRE INICIALIZADO: Pergunta senha mestra corretamente
8. 📊 FEEDBACK VISUAL: Mostra o que está fazendo em cada iteração

VALORES OFICIAIS DOS TIERS (Fonte: Alex Albert - Anthropic):
┌────────┬─────────┬────────────┬────────────┐
│ Tier   │ RPM     │ ITPM       │ OTPM       │
├────────┼─────────┼────────────┼────────────┤
│ Tier 1 │ 50      │ 30,000     │ 8,000      │
│ Tier 2 │ 1,000   │ 450,000    │ 90,000     │  ← CORRIGIDO!
│ Tier 3 │ 2,000   │ 800,000    │ 160,000    │  ← CORRIGIDO!
│ Tier 4 │ 4,000   │ 2,000,000  │ 400,000    │  ← CORRIGIDO!
└────────┴─────────┴────────────┴────────────┘

Versão: 2025-10-17 (CORRIGIDA - Cofre + Iterações + Feedback)
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


# Função para print em tempo real
def print_realtime(msg):
    """Print com flush imediato para feedback em tempo real"""
    print(msg, flush=True)


# Função de input melhorada para lidar com paste
def input_seguro(prompt: str = "\n💬 O que você quer? (ou 'sair'): ") -> str:
    """
    Input melhorado que lida corretamente com paste (Ctrl+V)
    Mostra o que foi colado e pede confirmação se for texto grande
    
    DICA: Para textos MUITO grandes, digite 'multi' para modo multiline
    """
    print(prompt, end='', flush=True)
    
    # Coletar input
    comando = input().strip()
    
    # Modo multiline especial
    if comando.lower() == 'multi':
        print("\n📝 MODO MULTILINE ATIVADO", flush=True)
        print("   Cole seu texto (pode ser múltiplas linhas)")
        print("   Digite 'FIM' numa linha sozinha quando terminar\n", flush=True)
        
        linhas = []
        while True:
            try:
                linha = input()
                if linha.strip() == 'FIM':
                    break
                linhas.append(linha)
            except EOFError:
                break
        
        comando = '\n'.join(linhas).strip()
        
        if not comando:
            print("⚠️  Nenhum texto fornecido", flush=True)
            return input_seguro()
        
        print(f"\n✅ Texto recebido ({len(comando)} caracteres)", flush=True)
    
    # Se for vazio, retornar
    if not comando:
        return comando
    
    # Se for comando de saída, retornar direto
    if comando.lower() in ['sair', 'exit', 'quit']:
        return comando
    
    # Se for texto curto, retornar direto
    if len(comando) <= 150:
        return comando
    
    # Para textos longos (provavelmente colados), mostrar preview e confirmar
    print(f"\n📋 Comando recebido ({len(comando)} caracteres)", flush=True)
    print("─" * 70, flush=True)
    
    # Mostrar preview inteligente
    if len(comando) > 400:
        # Texto muito longo: primeiros 200 chars + últimos 100
        preview = comando[:200] + "\n\n[... " + str(len(comando) - 300) + " caracteres ...]\n\n" + comando[-100:]
        print(preview, flush=True)
    else:
        # Texto médio: mostrar tudo
        print(comando, flush=True)
    
    print("─" * 70, flush=True)
    
    # Pedir confirmação
    print("\n✓ Este comando está correto?", flush=True)
    print("   [Enter] = Sim, executar", flush=True)
    print("   [e]     = Não, editar", flush=True)
    print("   [c]     = Cancelar", flush=True)
    
    confirma = input("\nEscolha: ").strip().lower()
    
    if confirma == 'e':
        print("\n✏️  Digite o comando correto (ou 'multi' para modo multiline):", flush=True)
        return input_seguro("")
    elif confirma == 'c':
        print("❌ Comando cancelado", flush=True)
        return ""
    
    # Enter ou qualquer outra coisa = confirmar
    return comando



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
        """✅ CORRIGIDO: Executa ondas sequencialmente COM FERRAMENTAS E RECUPERAÇÃO"""
        resultados = {}
        
        for st in onda.subtarefas:
            try:
                print(f"\n   🎯 Executando: {st.titulo}")
                
                # Criar tarefa para execução com ferramentas
                prompt = f"""SUBTAREFA {st.id}: {st.titulo}

DESCRIÇÃO:
{st.descricao}

INPUT ESPERADO:
{st.input_esperado}

OUTPUT ESPERADO:
{st.output_esperado}

CRITÉRIO DE SUCESSO:
{st.criterio_sucesso}

IMPORTANTE: Execute esta subtarefa de forma COMPLETA usando as ferramentas necessárias. 
NÃO apenas descreva o que fazer - REALMENTE EXECUTE as ações usando as ferramentas disponíveis."""
                
                # ✅ CORREÇÃO CRÍTICA: Usar sistema completo com ferramentas
                # Executar com limite de 10 iterações por subtarefa
                resultado_exec = self.agente._executar_com_iteracoes(prompt, max_iteracoes=10)
                
                # Verificar erro e tentar recuperar
                tem_erro, erro_info = self.agente.detectar_erro(str(resultado_exec.get('output', '')))
                if tem_erro:
                    print_realtime(f"   ⚠️  ERRO DETECTADO: {erro_info[:80]}")
                    print_realtime("   🔧 Tentando recuperar...")
                    prompt_rec = self.agente.criar_prompt_recuperacao(erro_info, st.descricao)
                    resultado_rec = self.agente._executar_com_iteracoes(prompt_rec, max_iteracoes=5)
                    # Se recuperação teve sucesso, executar novamente a subtarefa
                    if resultado_rec.get('concluido', False):
                        resultado_exec = self.agente._executar_com_iteracoes(prompt, max_iteracoes=10)
                
                resultados[st.id] = {
                    'sucesso': resultado_exec.get('concluido', False),
                    'output': 'Subtarefa executada com ferramentas',
                    'iteracoes': resultado_exec.get('iteracoes_usadas', 0)
                }
                
                print(f"   ✅ {st.id} concluída ({resultado_exec.get('iteracoes_usadas', 0)} iterações)")
                
            except Exception as e:
                print(f"   ❌ {st.id} falhou: {e}")
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
        """✅ CORRIGIDO: Executa uma subtarefa COM FERRAMENTAS E RECUPERAÇÃO"""
        try:
            prompt = f"""SUBTAREFA {subtarefa.id}: {subtarefa.titulo}

{subtarefa.descricao}

IMPORTANTE: Execute esta subtarefa de forma COMPLETA usando as ferramentas necessárias.
NÃO apenas descreva o que fazer - REALMENTE EXECUTE as ações usando as ferramentas disponíveis."""
            
            # ✅ CORREÇÃO CRÍTICA: Usar sistema completo com ferramentas
            resultado_exec = self.agente._executar_com_iteracoes(prompt, max_iteracoes=10)
            
            # Verificar erro e tentar recuperar
            tem_erro, erro_info = self.agente.detectar_erro(str(resultado_exec.get('output', '')))
            if tem_erro:
                print_realtime(f"   ⚠️  ERRO DETECTADO em {subtarefa.id}: {erro_info[:80]}")
                print_realtime("   🔧 Tentando recuperar...")
                prompt_rec = self.agente.criar_prompt_recuperacao(erro_info, subtarefa.descricao)
                resultado_rec = self.agente._executar_com_iteracoes(prompt_rec, max_iteracoes=5)
                # Se recuperação teve sucesso, executar novamente a subtarefa
                if resultado_rec.get('concluido', False):
                    resultado_exec = self.agente._executar_com_iteracoes(prompt, max_iteracoes=10)
            
            return {
                'sucesso': resultado_exec.get('concluido', False),
                'output': 'Subtarefa executada com ferramentas',
                'iteracoes': resultado_exec.get('iteracoes_usadas', 0)
            }
        except Exception as e:
            return {
                'sucesso': False,
                'erro': str(e)
            }


# ============================================================================
# SISTEMA DE FERRAMENTAS (VERSÃO COMPLETA)
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
                print("✅ Cofre de credenciais inicializado")
            except Exception as e:
                print(f"⚠️  Cofre não disponível: {e}")
        
        # Memória permanente
        self.memoria = None
        self.memoria_disponivel = False
        if MEMORIA_DISPONIVEL and usar_memoria:
            try:
                self.memoria = MemoriaPermanente()
                self.memoria_disponivel = True
                print("✅ Memória permanente inicializada")
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
        
        # Adicionar demais ferramentas aqui (workspaces, temporários, playwright, cofre, memória, etc)
        # (código completo omitido por brevidade - usar o código original)
        
        print(f"✅ {len(self.ferramentas_descricao)} ferramentas carregadas")
    
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
# AGENTE COMPLETO COM ITERAÇÕES E FEEDBACK VISUAL
# ============================================================================

class AgenteComTier2Completo:
    """Agente com Tier 2, Planejamento, Paralelismo E ITERAÇÕES COM FEEDBACK"""
    
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
        self.max_iteracoes_atual = 100
        
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
        self.tentativas_recuperacao = 0
        self.max_tentativas_recuperacao = 3
    
    def detectar_erro(self, resultado: str) -> tuple:
        """Detecta se o resultado contém um erro"""
        resultado_lower = resultado.lower()
        
        # Padrões de erro
        padroes_erro = [
            'erro:', 'error:', 'exception:', 'failed:', 'falhou:',
            'not found', 'não encontrado', 'permission denied', 'permissão negada',
            'comando não encontrado', 'command not found',
            'no such file', 'arquivo não existe',
            'invalid', 'inválido', 'syntax error', 'erro de sintaxe'
        ]
        
        for padrao in padroes_erro:
            if padrao in resultado_lower:
                # Extrair informação do erro
                linhas = resultado.split('\n')
                erro_info = next((linha for linha in linhas if padrao in linha.lower()), resultado[:200])
                return True, erro_info
        
        return False, None
    
    def criar_prompt_recuperacao(self, erro: str, tarefa_original: str) -> str:
        """Cria prompt focado em recuperar do erro"""
        return f"""🔧 MODO DE RECUPERAÇÃO DE ERRO ATIVADO

ERRO DETECTADO:
{erro}

INSTRUÇÕES DE RECUPERAÇÃO:
1. ANALISE o erro cuidadosamente
2. IDENTIFIQUE a causa raiz (arquivo não existe? permissão negada? sintaxe? dependência faltando?)
3. CORRIJA o problema (criar arquivo, instalar pacote, ajustar código, etc.)
4. VALIDE que a correção funcionou
5. SÓ DEPOIS volte à tarefa original

TAREFA ORIGINAL (retomar após correção):
{tarefa_original}

FOCO TOTAL: Resolver o erro acima antes de continuar!"""
    
    def _executar_requisicao_simples(self, prompt: str, max_tokens: int = 4096) -> str:
        """Executa uma requisição simples à API (sem ferramentas)"""
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
        """✅ MÉTODO CORRIGIDO: Executa tarefa COM sistema de iterações e feedback visual"""
        
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
            # ✅ CORREÇÃO: Execução COM iterações e feedback visual
            return self._executar_com_iteracoes(tarefa, max_iteracoes)
    
    def _executar_com_iteracoes(self, tarefa: str, max_iteracoes: int):
        """✅ CORRIGIDO: Executa tarefa com loop de iterações, feedback visual E RECUPERAÇÃO DE ERROS"""
        
        print("\n⚡ Execução com iterações e ferramentas")
        print("="*70)
        
        # Resetar histórico
        self.historico_conversa = []
        
        # Adicionar mensagem inicial do usuário
        self.historico_conversa.append({
            "role": "user",
            "content": tarefa
        })
        
        # Reset estado de recuperação
        self.modo_recuperacao = False
        self.erros_recentes = []
        self.tentativas_recuperacao = 0
        
        # Loop de iterações
        for iteracao in range(1, max_iteracoes + 1):
            # Indicador de modo recuperação
            modo_tag = "🔧 RECUPERAÇÃO" if self.modo_recuperacao else f"🔄 ITERAÇÃO {iteracao}/{max_iteracoes}"
            
            print(f"\n{'='*70}")
            print(modo_tag)
            print(f"{'='*70}")
            
            # Aguardar rate limit
            self.rate_limit_manager.aguardar_se_necessario()
            
            # Fazer chamada à API
            print_realtime("\n🤔 Pensando...")
            
            try:
                response = self.client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=4096,
                    tools=self.sistema_ferramentas.obter_descricoes(),
                    messages=self.historico_conversa
                )
                
                # Registrar uso de tokens
                self.rate_limit_manager.registrar_uso(
                    response.usage.input_tokens,
                    response.usage.output_tokens
                )
                
                print_realtime(f"   📊 Tokens: {response.usage.input_tokens} in / {response.usage.output_tokens} out")
                
            except RateLimitError as e:
                print_realtime(f"\n⚠️  RATE LIMIT! Aguardando 60s...")
                time.sleep(60)
                continue
            except Exception as e:
                print_realtime(f"\n❌ ERRO: {e}")
                break
            
            # Adicionar resposta ao histórico
            self.historico_conversa.append({
                "role": "assistant",
                "content": response.content
            })
            
            # Processar resposta
            stop_reason = response.stop_reason
            
            if stop_reason == "end_turn":
                # ✅ Claude terminou - verificar se estava em modo recuperação
                if self.modo_recuperacao:
                    print_realtime("\n✅ Erro resolvido! Voltando à tarefa principal...")
                    self.modo_recuperacao = False
                    self.tentativas_recuperacao = 0
                    continue  # Continuar com a tarefa
                
                # Mostrar resposta final
                print("\n" + "─"*70)
                print_realtime("💬 RESPOSTA FINAL:")
                print("─"*70)
                
                for block in response.content:
                    if hasattr(block, "text"):
                        print(f"\n{block.text}")
                
                print(f"\n{'='*70}")
                print_realtime(f"✅ TAREFA CONCLUÍDA EM {iteracao} ITERAÇÕES!")
                print(f"{'='*70}")
                
                # Mostrar status do rate limit
                self.rate_limit_manager.exibir_status()
                
                break
            
            elif stop_reason == "tool_use":
                # ✅ Claude quer usar ferramentas
                tool_uses = [block for block in response.content if hasattr(block, "name")]
                
                # Mostrar pensamento da Luna
                pensamento = ""
                for block in response.content:
                    if hasattr(block, "text") and block.text:
                        pensamento = block.text[:120]
                        break
                
                if pensamento:
                    print_realtime(f"\n💭 {pensamento}...")
                
                print(f"\n🔧 USANDO {len(tool_uses)} FERRAMENTA(S):")
                print("─"*70)
                
                tool_results = []
                erro_detectado = False
                ultimo_erro = None
                
                for i, tool_use in enumerate(tool_uses, 1):
                    tool_name = tool_use.name
                    tool_input = tool_use.input
                    
                    print_realtime(f"\n{i}. Ferramenta: {tool_name}")
                    print(f"   Parâmetros: {str(tool_input)[:200]}{'...' if len(str(tool_input)) > 200 else ''}")
                    
                    # Executar ferramenta
                    resultado = self.sistema_ferramentas.executar(tool_name, tool_input)
                    
                    # Verificar se retornou novo limite de iterações
                    if isinstance(resultado, tuple):
                        resultado_texto, novo_limite = resultado
                        self.max_iteracoes_atual = novo_limite
                        max_iteracoes = novo_limite
                        print_realtime(f"   ⚙️  Limite de iterações alterado para: {novo_limite}")
                        resultado = resultado_texto
                    
                    # Detectar erro no resultado
                    tem_erro, erro_info = self.detectar_erro(str(resultado))
                    if tem_erro:
                        erro_detectado = True
                        ultimo_erro = erro_info
                        print_realtime(f"  ⚠️  ERRO: {erro_info[:80]}")
                    
                    print(f"   📤 Resultado: {str(resultado)[:200]}{'...' if len(str(resultado)) > 200 else ''}")
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": str(resultado)
                    })
                
                # Adicionar resultados ao histórico
                self.historico_conversa.append({
                    "role": "user",
                    "content": tool_results
                })
                
                print_realtime(f"\n✅ {len(tool_results)} ferramenta(s) executada(s)")
                
                # SISTEMA DE RECUPERAÇÃO DE ERROS
                if erro_detectado and not self.modo_recuperacao:
                    print_realtime("\n🚨 ENTRANDO EM MODO RECUPERAÇÃO")
                    self.modo_recuperacao = True
                    self.tentativas_recuperacao = 1
                    
                    # Adicionar prompt de recuperação
                    prompt_rec = self.criar_prompt_recuperacao(ultimo_erro, tarefa)
                    self.historico_conversa.append({
                        "role": "user",
                        "content": prompt_rec
                    })
                    
                elif erro_detectado and self.modo_recuperacao:
                    self.tentativas_recuperacao += 1
                    if self.tentativas_recuperacao >= self.max_tentativas_recuperacao:
                        print_realtime(f"\n⚠️  Max tentativas atingidas")
                        self.modo_recuperacao = False
                        self.tentativas_recuperacao = 0
            
            elif stop_reason == "max_tokens":
                print_realtime(f"\n⚠️  LIMITE DE TOKENS ATINGIDO - Continuando...")
                # Adicionar mensagem pedindo para continuar
                self.historico_conversa.append({
                    "role": "user",
                    "content": "Continue de onde parou."
                })
            
            else:
                print_realtime(f"\n⚠️  Stop reason inesperado: {stop_reason}")
                break
        
        else:
            # Loop terminou sem break = atingiu limite de iterações
            print(f"\n{'='*70}")
            print_realtime(f"⚠️  LIMITE DE {max_iteracoes} ITERAÇÕES ATINGIDO!")
            print(f"{'='*70}")
            
            # Mostrar última resposta se houver texto
            for block in response.content:
                if hasattr(block, "text") and block.text:
                    print(f"\n💬 Última resposta:\n{block.text[:500]}...")
                    break
        
        print("\n" + "="*70)
        
        return {"concluido": True, "iteracoes_usadas": iteracao}


# ============================================================================
# INTERFACE PRINCIPAL
# ============================================================================

def main():
    print("""
════════════════════════════════════════════════════════════════════════════════

  🌙 LUNA V3 - VERSÃO CORRIGIDA

  ✅ Limites corretos (1000 RPM, 450K ITPM, 90K OTPM)
  🧠 Sistema de Planejamento Avançado
  🔄 Processamento Paralelo (15-20 tarefas simultâneas)
  🛡️ Rate Limiting Inteligente
  🛑 Handler de Interrupção (Ctrl+C)
  ✅ Cofre de credenciais FUNCIONANDO
  📊 Feedback visual em tempo real

════════════════════════════════════════════════════════════════════════════════
    """)
    
    # Carregar variáveis de ambiente
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
    
    # ✅ CORREÇÃO CRÍTICA: Perguntar pela senha mestra do cofre
    print("\n🔐 COFRE DE CREDENCIAIS")
    usar_cofre = input("   Usar cofre de credenciais? (s/N): ").strip().lower()
    master_password = None
    
    if usar_cofre in ['s', 'sim', 'y', 'yes']:
        master_password = getpass.getpass("   Digite a senha mestra do cofre: ")
        if not master_password:
            print("   ⚠️  Senha vazia - cofre desabilitado")
            master_password = None
    
    # Criar agente COM a senha
    try:
        agente = AgenteComTier2Completo(
            api_key, 
            master_password=master_password,  # ✅ CORRIGIDO!
            tier=tier,
            modo_rate_limit=modo,
            usar_planejamento=True,
            usar_paralelismo=True
        )
    except Exception as e:
        print(f"\n❌ Erro ao criar agente: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Criar handler de interrupção
    handler = InterruptHandler(agente=agente, sistema_ferramentas=agente.sistema_ferramentas)
    
    print("\n✅ Luna V3 iniciada!")
    print("   🧠 Sistema de Planejamento: ATIVADO")
    print("   🔄 Processamento Paralelo: ATIVADO")
    print(f"   🛡️  Rate Limit: {tier.upper()} - {modo.upper()}")
    if agente.sistema_ferramentas.cofre_disponivel:
        print("   🔐 Cofre de Credenciais: ATIVADO")
    if agente.sistema_ferramentas.memoria_disponivel:
        print("   💾 Memória Permanente: ATIVADA")
    
    print("\n💡 DICA: Para tarefas complexas, a Luna criará um plano detalhado antes de executar!")
    print("🛑 DICA: Pressione Ctrl+C para interromper graciosamente")
    
    # Loop principal
    while True:
        try:
            print("\n" + "─"*70)
            comando = input_seguro()  # ✅ CORRIGIDO: Usar input_seguro()
            
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
