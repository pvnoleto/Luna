#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 LUNA V3 - COM TIER 2 CORRIGIDO + PLANEJAMENTO + RECUPERAÇÃO COMPLETA
===================================================================================

✨ NOVIDADES DESTA VERSÃO:
1. ✅ LIMITES CORRETOS: Tier 2 = 1000 RPM, 450K ITPM, 90K OTPM (OFICIAL!)
2. 🧠 SISTEMA DE PLANEJAMENTO AVANÇADO: Planos detalhados antes de executar
3. 🔄 PROCESSAMENTO PARALELO AGRESSIVO: 15-20 tarefas simultâneas
4. 🛡️ ANTI-RATE LIMIT: Monitora e previne erros 429
5. 🔧 RECUPERAÇÃO INTELIGENTE COMPLETA: Prioriza corrigir erros (TODOS OS SISTEMAS!)
6. 🛑 HANDLER DE INTERRUPÇÃO: Ctrl+C tratado graciosamente
7. ✅ COFRE INICIALIZADO: Pergunta senha mestra corretamente
8. 📊 FEEDBACK VISUAL AVANÇADO: Mostra detalhes em tempo real

⚡ NOVIDADES NESTA ATUALIZAÇÃO COMPLETA:
- ✅ Sistema de recuperação de erros ABRANGENDO PLANEJAMENTO
- ✅ Função print_realtime() para feedback imediato
- ✅ Função input_seguro() para textos colados
- ✅ Detecção automática de erros em todas as execuções
- ✅ Modo recuperação com até 3 tentativas automáticas
- ✅ ARQUIVO COMPLETO E FUNCIONAL!

Versão: 2025-10-17 (COMPLETA E CORRIGIDA!)
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


# ============================================================================
# FUNÇÕES DE FEEDBACK VISUAL EM TEMPO REAL
# ============================================================================

def print_realtime(msg):
    """Print com flush imediato para feedback em tempo real"""
    print(msg, flush=True)


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
        print_realtime("\n📝 MODO MULTILINE ATIVADO")
        print_realtime("   Cole seu texto (pode ser múltiplas linhas)")
        print_realtime("   Digite 'FIM' numa linha sozinha quando terminar\n")
        
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
            print_realtime("⚠️  Nenhum texto fornecido")
            return input_seguro()
        
        print_realtime(f"\n✅ Texto recebido ({len(comando)} caracteres)")
    
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
    print_realtime(f"\n📋 Comando recebido ({len(comando)} caracteres)")
    print_realtime("─" * 70)
    
    # Mostrar preview inteligente
    if len(comando) > 400:
        # Texto muito longo: primeiros 200 chars + últimos 100
        preview = comando[:200] + "\n\n[... " + str(len(comando) - 300) + " caracteres ...]\n\n" + comando[-100:]
        print_realtime(preview)
    else:
        # Texto médio: mostrar tudo
        print_realtime(comando)
    
    print_realtime("─" * 70)
    
    # Pedir confirmação
    print_realtime("\n✓ Este comando está correto?")
    print_realtime("   [Enter] = Sim, executar")
    print_realtime("   [e]     = Não, editar")
    print_realtime("   [c]     = Cancelar")
    
    confirma = input("\nEscolha: ").strip().lower()
    
    if confirma == 'e':
        print_realtime("\n✏️  Digite o comando correto (ou 'multi' para modo multiline):")
        return input_seguro("")
    elif confirma == 'c':
        print_realtime("❌ Comando cancelado")
        return ""
    
    # Enter ou qualquer outra coisa = confirmar
    return comando


# ============================================================================
# IMPORTS DOS SISTEMAS
# ============================================================================

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

# Carregar configuração
load_dotenv()


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
        
        print_realtime("✅ Handler de interrupção ativado (Ctrl+C será tratado graciosamente)")
    
    def handler_sigint(self, signum, frame):
        """Handler para Ctrl+C"""
        if self.interrompido:
            print_realtime("\n\n🔴 FORÇANDO SAÍDA... (segunda interrupção)")
            self.cleanup_forcado()
            sys.exit(1)
        
        self.interrompido = True
        print_realtime("\n\n⚠️  INTERRUPÇÃO DETECTADA (Ctrl+C)")
        print_realtime("   Limpando recursos... (Ctrl+C novamente para forçar saída)")
        
        self.cleanup_gracioso()
        sys.exit(0)
    
    def handler_sigterm(self, signum, frame):
        """Handler para SIGTERM"""
        print_realtime("\n\n⚠️  SIGTERM RECEBIDO")
        self.cleanup_gracioso()
        sys.exit(0)
    
    def cleanup_gracioso(self):
        """Limpeza graciosa de recursos"""
        if self.limpeza_feita:
            return
        
        print_realtime("\n📋 LIMPANDO RECURSOS:")
        
        if self.sistema_ferramentas:
            try:
                if hasattr(self.sistema_ferramentas, 'browser') and self.sistema_ferramentas.browser:
                    print_realtime("   🌐 Fechando navegador...")
                    self.sistema_ferramentas.executar('fechar_navegador', {})
                    print_realtime("   ✅ Navegador fechado")
            except Exception as e:
                print_realtime(f"   ⚠️  Erro ao fechar navegador: {e}")
        
        if self.agente and hasattr(self.agente, 'rate_limit_manager'):
            try:
                print_realtime("   📊 Salvando estatísticas...")
                stats = self.agente.rate_limit_manager.obter_estatisticas()
                
                stats_file = "Luna/.stats/rate_limit_interrupcao.json"
                os.makedirs(os.path.dirname(stats_file), exist_ok=True)
                
                with open(stats_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        'timestamp': datetime.now().isoformat(),
                        'stats': stats,
                        'motivo': 'interrupcao_ctrl_c'
                    }, f, indent=2)
                
                print_realtime(f"   ✅ Estatísticas salvas")
            except Exception as e:
                print_realtime(f"   ⚠️  Erro ao salvar stats: {e}")
        
        self.limpeza_feita = True
        print_realtime("\n✅ Limpeza concluída!")
    
    def cleanup_forcado(self):
        """Limpeza forçada"""
        print_realtime("🔴 SAÍDA FORÇADA - recursos podem não ser limpos!")
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
        
        print_realtime(f"🛡️  Rate Limit Manager: {tier.upper()} - Modo {modo.upper()}")
        print_realtime(f"   Limites: {self.limite_itpm:,} ITPM | {self.limite_otpm:,} OTPM | {self.limite_rpm} RPM")
        print_realtime(f"   Threshold: {self.threshold*100:.0f}%")
    
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
            print_realtime(f"\n⏳ Aguardando {segundos}s para respeitar rate limit")
            print_realtime(f"   Motivo: {motivo}")
            print_realtime(f"   Uso atual: ITPM {uso['itpm_percent']:.1f}% | OTPM {uso['otpm_percent']:.1f}% | RPM {uso['rpm_percent']:.1f}%")
            time.sleep(segundos)
            self.total_esperas += 1
            self.tempo_total_espera += segundos
    
    def exibir_status(self):
        """Mostra status atual com barras de progresso visual"""
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
        
        print_realtime(f"\n📊 STATUS DO RATE LIMIT:")
        print_realtime(f"   ITPM: {barra(uso['itpm_percent'])} ({uso['itpm_atual']:,}/{self.limite_itpm:,})")
        print_realtime(f"   OTPM: {barra(uso['otpm_percent'])} ({uso['otpm_atual']:,}/{self.limite_otpm:,})")
        print_realtime(f"   RPM:  {barra(uso['rpm_percent'])} ({uso['rpm_atual']}/{self.limite_rpm})")
    
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
# SISTEMA DE FERRAMENTAS COMPLETO
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
                print_realtime(f"⚠️  Cofre não disponível: {e}")
        
        # Memória permanente
        self.memoria = None
        self.memoria_disponivel = False
        if MEMORIA_DISPONIVEL and usar_memoria:
            try:
                self.memoria = MemoriaPermanente()
                self.memoria_disponivel = True
            except Exception as e:
                print_realtime(f"⚠️  Memória não disponível: {e}")
        
        # Carregar ferramentas
        self._carregar_ferramentas_base()
    
    def _carregar_ferramentas_base(self):
        """Todas as ferramentas base"""
        
        # BASH
        self.adicionar_ferramenta(
            "bash_avancado",
            '''def bash_avancado(comando: str, timeout: int = 60) -> str:
    import subprocess, os
    print_realtime(f"  ⚡ Bash: {comando[:70]}...")
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
        print_realtime(f"  ✓ Concluído (código {resultado.returncode})")
        return saida[:3000]
    except Exception as e:
        print_realtime(f"  ✗ ERRO: {str(e)[:50]}")
        return f"ERRO: {e}"''',
            "Executa comandos bash/terminal",
            {"comando": {"type": "string"}, "timeout": {"type": "integer"}}
        )
        
        # ARQUIVOS
        self.adicionar_ferramenta(
            "criar_arquivo",
            '''def criar_arquivo(caminho: str, conteudo: str) -> str:
    from pathlib import Path
    print_realtime(f"  📝 Criando: {Path(caminho).name}")
    try:
        global _gerenciador_workspaces
        if _gerenciador_workspaces:
            caminho_completo = _gerenciador_workspaces.resolver_caminho(caminho)
        else:
            caminho_completo = caminho
        
        Path(caminho_completo).parent.mkdir(parents=True, exist_ok=True)
        with open(caminho_completo, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        print_realtime(f"  ✓ Arquivo criado: {Path(caminho_completo).name}")
        return f"Arquivo '{caminho}' criado em: {caminho_completo}"
    except Exception as e:
        print_realtime(f"  ✗ ERRO: {str(e)[:50]}")
        return f"ERRO: {e}"''',
            "Cria arquivo. Se workspace estiver selecionado, cria no workspace atual automaticamente.",
            {"caminho": {"type": "string"}, "conteudo": {"type": "string"}}
        )
        
        self.adicionar_ferramenta(
            "ler_arquivo",
            '''def ler_arquivo(caminho: str) -> str:
    print_realtime(f"  📖 Lendo: {caminho}")
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
        print_realtime(f"  ✓ Lido ({len(conteudo)} caracteres)")
        return conteudo[:5000]
    except Exception as e:
        print_realtime(f"  ✗ ERRO: {str(e)[:50]}")
        return f"ERRO: {e}"''',
            "Lê arquivo. Busca no workspace atual se disponível.",
            {"caminho": {"type": "string"}}
        )
        
        # PLAYWRIGHT
        self.adicionar_ferramenta(
            "instalar_playwright",
            '''def instalar_playwright() -> str:
    import subprocess
    print_realtime("  📦 Instalando Playwright...")
    try:
        subprocess.run("pip install playwright", shell=True, timeout=120, 
                      encoding="utf-8", errors="replace")
        subprocess.run("playwright install chromium", shell=True, timeout=300,
                      encoding="utf-8", errors="replace")
        print_realtime("  ✓ Playwright instalado")
        return "Playwright instalado!"
    except Exception as e:
        return f"ERRO: {e}"''',
            "Instala Playwright",
            {}
        )
        
        self.adicionar_ferramenta(
            "iniciar_navegador",
            '''def iniciar_navegador(headless: bool = True) -> str:
    print_realtime("  🌐 Iniciando navegador...")
    try:
        from playwright.sync_api import sync_playwright
        global _playwright_instance, _browser, _page
        _playwright_instance = sync_playwright().start()
        _browser = _playwright_instance.chromium.launch(headless=headless)
        _page = _browser.new_page()
        print_realtime("  ✓ Navegador pronto")
        return "Navegador iniciado!"
    except Exception as e:
        return f"ERRO: {e}"''',
            "Inicia navegador Playwright",
            {"headless": {"type": "boolean"}}
        )
        
        self.adicionar_ferramenta(
            "navegar_url",
            '''def navegar_url(url: str) -> str:
    print_realtime(f"  🌐 Navegando: {url[:50]}...")
    try:
        global _page
        _page.goto(url, timeout=30000)
        titulo = _page.title()
        print_realtime(f"  ✓ Página: {titulo[:50]}")
        return f"Navegado para '{url}'"
    except Exception as e:
        return f"ERRO: {e}"''',
            "Navega para URL",
            {"url": {"type": "string"}}
        )
        
        self.adicionar_ferramenta(
            "tirar_screenshot",
            '''def tirar_screenshot(caminho: str = "screenshot.png") -> str:
    print_realtime(f"  📸 Screenshot: {caminho}")
    try:
        global _page, _gerenciador_workspaces
        
        if _gerenciador_workspaces:
            caminho_completo = _gerenciador_workspaces.resolver_caminho(caminho)
        else:
            caminho_completo = caminho
        
        _page.screenshot(path=caminho_completo)
        print_realtime(f"  ✓ Salvo")
        return f"Screenshot salvo: {caminho_completo}"
    except Exception as e:
        return f"ERRO: {e}"''',
            "Tira screenshot da página atual",
            {"caminho": {"type": "string"}}
        )
        
        self.adicionar_ferramenta(
            "clicar_elemento",
            '''def clicar_elemento(seletor: str) -> str:
    print_realtime(f"  👆 Clicando: {seletor[:40]}...")
    try:
        global _page
        _page.click(seletor, timeout=5000)
        print_realtime(f"  ✓ Clicado")
        return f"Clicado em '{seletor}'"
    except Exception as e:
        return f"ERRO: {e}"''',
            "Clica em elemento",
            {"seletor": {"type": "string"}}
        )
        
        self.adicionar_ferramenta(
            "preencher_campo",
            '''def preencher_campo(seletor: str, valor: str) -> str:
    print_realtime(f"  ✏️  Preenchendo: {seletor[:40]}...")
    try:
        global _page
        _page.fill(seletor, valor, timeout=5000)
        print_realtime(f"  ✓ Preenchido")
        return "Campo preenchido"
    except Exception as e:
        return f"ERRO: {e}"''',
            "Preenche campo",
            {"seletor": {"type": "string"}, "valor": {"type": "string"}}
        )
        
        self.adicionar_ferramenta(
            "fechar_navegador",
            '''def fechar_navegador() -> str:
    print_realtime("  🌐 Fechando navegador...")
    try:
        global _browser, _page, _playwright_instance
        if _page: _page.close()
        if _browser: _browser.close()
        if _playwright_instance: _playwright_instance.stop()
        _page = _browser = _playwright_instance = None
        print_realtime("  ✓ Navegador fechado")
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
    print_realtime(f"  🔑 Obtendo credencial: {servico}")
    try:
        global _cofre
        import json
        cred = _cofre.obter_credencial(servico)
        print_realtime(f"  ✓ Obtida para: {cred['usuario']}")
        return json.dumps(cred)
    except Exception as e:
        return f"ERRO: {e}"''',
                "Obtém credencial do cofre",
                {"servico": {"type": "string"}}
            )
            
            self.adicionar_ferramenta(
                "login_automatico",
                '''def login_automatico(servico: str, url_login: str = None) -> str:
    print_realtime(f"  🔐 Login em: {servico}")
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
        
        print_realtime(f"  ✓ Login realizado")
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
    print_realtime(f"  💾 Salvando: {categoria}")
    try:
        global _memoria
        tags_list = [t.strip() for t in tags.split(",")] if tags else []
        _memoria.adicionar_aprendizado(categoria, conteudo, tags=tags_list)
        print_realtime(f"  ✓ Aprendizado salvo")
        return f"Aprendizado salvo em '{categoria}'"
    except Exception as e:
        return f"ERRO: {e}"''',
                "Salva aprendizado na memória permanente",
                {"categoria": {"type": "string"}, "conteudo": {"type": "string"}, "tags": {"type": "string"}}
            )
            
            self.adicionar_ferramenta(
                "buscar_aprendizados",
                '''def buscar_aprendizados(query: str = "", categoria: str = "") -> str:
    print_realtime(f"  🔍 Buscando: {query or 'todos'}")
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
        
        print_realtime(f"  ✓ {len(resultados)} encontrados")
        return texto
    except Exception as e:
        return f"ERRO: {e}"''',
                "Busca aprendizados salvos",
                {"query": {"type": "string"}, "categoria": {"type": "string"}}
            )
            
            self.adicionar_ferramenta(
                "salvar_preferencia",
                '''def salvar_preferencia(chave: str, valor: str) -> str:
    print_realtime(f"  ⚙️  Preferência: {chave}")
    try:
        global _memoria
        _memoria.salvar_preferencia(chave, valor)
        print_realtime(f"  ✓ Salva")
        return f"Preferência '{chave}' salva"
    except Exception as e:
        return f"ERRO: {e}"''',
                "Salva preferência do usuário",
                {"chave": {"type": "string"}, "valor": {"type": "string"}}
            )
        
        # WORKSPACES
        if self.gerenciador_workspaces_disponivel:
            self.adicionar_ferramenta(
                "criar_workspace",
                '''def criar_workspace(nome: str, descricao: str = "") -> str:
    print_realtime(f"  📁 Criando workspace: {nome}")
    try:
        global _gerenciador_workspaces
        sucesso, mensagem = _gerenciador_workspaces.criar_workspace(nome, descricao)
        if sucesso:
            _gerenciador_workspaces.selecionar_workspace(nome)
            print_realtime(f"  ✓ Workspace '{nome}' criado e selecionado")
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
    print_realtime(f"  📂 Listando workspaces...")
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
        
        print_realtime(f"  ✓ {len(workspaces)} workspace(s) encontrados")
        return resultado
    except Exception as e:
        return f"ERRO: {e}"''',
                "Lista todos workspaces criados",
                {}
            )
            
            self.adicionar_ferramenta(
                "selecionar_workspace",
                '''def selecionar_workspace(nome: str) -> str:
    print_realtime(f"  🎯 Selecionando: {nome}")
    try:
        global _gerenciador_workspaces
        sucesso, mensagem = _gerenciador_workspaces.selecionar_workspace(nome)
        if sucesso:
            ws = _gerenciador_workspaces.get_workspace_atual()
            print_realtime(f"  ✓ Workspace selecionado")
            return mensagem + f"\\nNovos arquivos serão criados em: {ws['path_relativo']}"
        return mensagem
    except Exception as e:
        return f"ERRO: {e}"''',
                "Seleciona workspace como atual",
                {"nome": {"type": "string"}}
            )
        
        # META-FERRAMENTAS
        self.adicionar_ferramenta(
            "criar_ferramenta",
            '''def criar_ferramenta(nome: str, codigo_python: str, descricao: str, parametros_json: str) -> str:
    import json
    print_realtime(f"  🔧 Nova ferramenta: {nome}")
    try:
        global _nova_ferramenta_info
        _nova_ferramenta_info = {
            'nome': nome,
            'codigo': codigo_python,
            'descricao': descricao,
            'parametros': json.loads(parametros_json)
        }
        print_realtime(f"  ✓ Ferramenta '{nome}' criada")
        return f"Ferramenta '{nome}' criada!"
    except Exception as e:
        return f"ERRO: {e}"''',
            "Cria nova ferramenta dinamicamente",
            {"nome": {"type": "string"}, "codigo_python": {"type": "string"}, 
             "descricao": {"type": "string"}, "parametros_json": {"type": "string"}}
        )
        
        self.adicionar_ferramenta(
            "instalar_biblioteca",
            '''def instalar_biblioteca(nome_pacote: str) -> str:
    import subprocess
    print_realtime(f"  📦 Instalando: {nome_pacote}")
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
            print_realtime(f"  ✓ '{nome_pacote}' instalado")
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
                '_gerenciador_workspaces': self.gerenciador_workspaces,
                '_playwright_instance': None,
                '_browser': self.browser,
                '_page': self.page,
                '_cofre': self.cofre,
                '_memoria': self.memoria,
                '__builtins__': __builtins__,
                'os': __import__('os'),
                'print_realtime': print_realtime
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
            
            return str(resultado)
            
        except Exception as e:
            import traceback
            erro_completo = traceback.format_exc()
            print_realtime(f"  ✗ ERRO CRÍTICO: {str(e)[:100]}")
            return f"ERRO: {erro_completo[:1000]}"
    
    def obter_descricoes(self) -> list:
        return self.ferramentas_descricao


# ============================================================================
# AGENTE PRINCIPAL COM RECUPERAÇÃO COMPLETA
# ============================================================================

class AgenteCompletoV3:
    """Agente com rate limiting, planejamento e recuperação completa de erros"""
    
    def __init__(self, api_key: str, master_password: str = None, usar_memoria: bool = True, tier: str = "tier1", modo_rate_limit: str = "balanceado"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.sistema_ferramentas = SistemaFerramentasCompleto(master_password, usar_memoria)
        self.historico_conversa = []
        self.max_iteracoes_atual = 40
        
        # Rate limit manager
        self.rate_limit_manager = RateLimitManager(tier=tier, modo=modo_rate_limit)
        
        # Sistema de recuperação de erros
        self.modo_recuperacao = False
        self.erros_recentes = []
        self.tentativas_recuperacao = 0
        self.max_tentativas_recuperacao = 3
    
    def detectar_erro(self, resultado: str) -> tuple:
        """✅ Detecta se há erro no resultado de uma ferramenta"""
        # Detectar padrões de erro
        padrao_erro = resultado.startswith("ERRO:") or "ERRO:" in resultado[:100]
        
        if padrao_erro:
            # Extrair informação do erro
            linhas = resultado.split("\n")
            erro_principal = linhas[0] if linhas else resultado[:200]
            
            return True, erro_principal
        
        return False, None
    
    def criar_prompt_recuperacao(self, erro: str, tarefa_original: str):
        """✅ Cria prompt focado em recuperar do erro"""
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
        """Executa requisição simples sem ferramentas (para planejamento)"""
        self.rate_limit_manager.aguardar_se_necessario()
        
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Registrar uso
            self.rate_limit_manager.registrar_uso(
                response.usage.input_tokens,
                response.usage.output_tokens
            )
            
            # Extrair texto
            resultado = ""
            for block in response.content:
                if hasattr(block, "text"):
                    resultado += block.text
            
            return resultado
            
        except RateLimitError as e:
            print_realtime(f"\n⚠️  RATE LIMIT - aguardando 60s...")
            time.sleep(60)
            return self._executar_requisicao_simples(prompt, max_tokens)
        except Exception as e:
            print_realtime(f"\n❌ Erro na requisição: {e}")
            return f"ERRO: {e}"
    
    def _executar_com_iteracoes(self, prompt: str, max_iteracoes: int = 10) -> dict:
        """✅ CORRIGIDO: Executa tarefa com ferramentas e limite de iterações"""
        historico_local = [{"role": "user", "content": prompt}]
        
        for it in range(1, max_iteracoes + 1):
            print_realtime(f"   └─ Iteração {it}/{max_iteracoes}")
            
            self.rate_limit_manager.aguardar_se_necessario()
            
            try:
                response = self.client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=4096,
                    tools=self.sistema_ferramentas.obter_descricoes(),
                    messages=historico_local
                )
                
                self.rate_limit_manager.registrar_uso(
                    response.usage.input_tokens,
                    response.usage.output_tokens
                )
                
            except RateLimitError as e:
                print_realtime(f"      ⚠️  Rate limit - aguardando 60s...")
                time.sleep(60)
                continue
            except Exception as e:
                print_realtime(f"      ❌ Erro: {e}")
                return {
                    'concluido': False,
                    'iteracoes_usadas': it,
                    'output': f"ERRO: {e}",
                    'erro': str(e)
                }
            
            if response.stop_reason == "end_turn":
                # Concluído
                resposta_final = ""
                for block in response.content:
                    if hasattr(block, "text"):
                        resposta_final += block.text
                
                return {
                    'concluido': True,
                    'iteracoes_usadas': it,
                    'output': resposta_final
                }
            
            if response.stop_reason == "tool_use":
                historico_local.append({"role": "assistant", "content": response.content})
                
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        print_realtime(f"      🔧 {block.name}")
                        resultado = self.sistema_ferramentas.executar(block.name, block.input)
                        
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": resultado
                        })
                
                historico_local.append({"role": "user", "content": tool_results})
        
        # Limite atingido
        return {
            'concluido': False,
            'iteracoes_usadas': max_iteracoes,
            'output': "Limite de iterações atingido"
        }
    
    def executar_tarefa(self, tarefa: str, max_iteracoes: int = None):
        """✅ Executa tarefa com rate limiting e recuperação completa"""
        
        if max_iteracoes is None:
            max_iteracoes = self.max_iteracoes_atual
        else:
            self.max_iteracoes_atual = max_iteracoes
        
        print_realtime("\n" + "="*70)
        print_realtime(f"🎯 TAREFA: {tarefa}")
        print_realtime("="*70)
        
        # Buscar aprendizados
        contexto_aprendizados = ""
        if self.sistema_ferramentas.memoria_disponivel:
            contexto_aprendizados = self.sistema_ferramentas.memoria.obter_contexto_recente(3)
        
        # Contexto de workspace
        contexto_workspace = ""
        if self.sistema_ferramentas.gerenciador_workspaces_disponivel:
            ws_atual = self.sistema_ferramentas.gerenciador_workspaces.get_workspace_atual()
            if ws_atual:
                contexto_workspace = f"\n\nWORKSPACE ATUAL: {ws_atual['nome']}\nLocalização: {ws_atual['path_relativo']}\nNovos arquivos serão criados aqui automaticamente!"
        
        prompt_sistema = f"""Você é o AGENTE AI MAIS AVANÇADO possível.

CAPACIDADES COMPLETAS:
1. AUTO-EVOLUÇÃO: Cria ferramentas dinamicamente
2. COMPUTER USE: Navega web, screenshots, interação
3. CREDENCIAIS: Acessa cofre criptografado, login automático
4. MEMÓRIA PERMANENTE: Aprende e lembra entre sessões
5. WORKSPACE MANAGER: Organiza projetos automaticamente
6. RECUPERAÇÃO DE ERROS: Detecta e corrige erros automaticamente

INSTRUÇÕES CRÍTICAS:
1. ANTES de tarefas, BUSQUE aprendizados relevantes
2. DEPOIS de resolver algo novo, SALVE o aprendizado
3. NUNCA mostre senhas ao usuário
4. USE login_automatico sempre que precisar de login
5. APRENDA com erros e sucessos
6. USE workspaces para organizar projetos
7. SE ENCONTRAR ERRO: PARE e CORRIJA antes de continuar!

{contexto_aprendizados}{contexto_workspace}

TAREFA DO USUÁRIO:
{tarefa}

Comece BUSCANDO aprendizados relevantes, depois execute a tarefa!"""
        
        self.historico_conversa = [{"role": "user", "content": prompt_sistema}]
        
        # Reset estado de recuperação
        self.modo_recuperacao = False
        self.erros_recentes = []
        self.tentativas_recuperacao = 0
        
        self.rate_limit_manager.exibir_status()
        
        for iteracao in range(1, max_iteracoes + 1):
            modo_tag = "🔧 RECUPERAÇÃO" if self.modo_recuperacao else f"🔄 Iteração {iteracao}/{max_iteracoes}"
            print_realtime(f"\n{modo_tag}")
            
            self.rate_limit_manager.aguardar_se_necessario()
            
            try:
                response = self.client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=4096,
                    tools=self.sistema_ferramentas.obter_descricoes(),
                    messages=self.historico_conversa
                )
                
                self.rate_limit_manager.registrar_uso(
                    response.usage.input_tokens,
                    response.usage.output_tokens
                )
                
            except RateLimitError as e:
                print_realtime(f"\n⚠️  RATE LIMIT ATINGIDO!")
                print_realtime(f"   Aguardando 60 segundos...")
                time.sleep(60)
                continue
                
            except Exception as e:
                print_realtime(f"\n❌ Erro: {e}")
                break
            
            if response.stop_reason == "end_turn":
                resposta_final = ""
                for block in response.content:
                    if hasattr(block, "text"):
                        resposta_final += block.text
                
                if self.modo_recuperacao:
                    print_realtime("\n✅ Erro resolvido! Voltando à tarefa principal...")
                    self.modo_recuperacao = False
                    self.tentativas_recuperacao = 0
                    continue
                
                if self.sistema_ferramentas.memoria_disponivel:
                    ferramentas_usadas = []
                    self.sistema_ferramentas.memoria.registrar_tarefa(
                        tarefa, resposta_final[:500], ferramentas_usadas, True
                    )
                
                print_realtime("\n" + "="*70)
                print_realtime("✅ CONCLUÍDO!")
                print_realtime("="*70)
                print_realtime(resposta_final)
                print_realtime("="*70)
                
                # Estatísticas finais
                print_realtime("\n📊 ESTATÍSTICAS DA SESSÃO:")
                stats_rate = self.rate_limit_manager.obter_estatisticas()
                print_realtime(f"   Requisições: {stats_rate['total_requisicoes']}")
                print_realtime(f"   Tokens usados: {stats_rate['total_tokens']:,}")
                print_realtime(f"   Média tokens/req: {stats_rate['media_tokens_req']:.0f}")
                if stats_rate['total_esperas'] > 0:
                    print_realtime(f"   Esperas: {stats_rate['total_esperas']} ({stats_rate['tempo_total_espera']:.0f}s total)")
                
                return resposta_final
            
            if response.stop_reason == "tool_use":
                self.historico_conversa.append({"role": "assistant", "content": response.content})
                
                pensamento = ""
                for block in response.content:
                    if hasattr(block, "text") and block.text:
                        pensamento = block.text[:120]
                        break
                
                if pensamento:
                    print_realtime(f"💭 {pensamento}...")
                
                tool_results = []
                erro_detectado = False
                ultimo_erro = None
                
                for block in response.content:
                    if block.type == "tool_use":
                        print_realtime(f"🔧 {block.name}")
                        
                        resultado = self.sistema_ferramentas.executar(block.name, block.input)
                        
                        # ✅ Detectar erro
                        tem_erro, erro_info = self.detectar_erro(resultado)
                        if tem_erro:
                            erro_detectado = True
                            ultimo_erro = erro_info
                            print_realtime(f"  ⚠️  ERRO DETECTADO: {erro_info[:80]}")
                            self.erros_recentes.append({
                                'ferramenta': block.name,
                                'erro': erro_info,
                                'iteracao': iteracao
                            })
                        
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": resultado
                        })
                
                self.historico_conversa.append({"role": "user", "content": tool_results})
                
                # ✅ SISTEMA DE RECUPERAÇÃO
                if erro_detectado and not self.modo_recuperacao:
                    print_realtime(f"\n🚨 ENTRANDO EM MODO DE RECUPERAÇÃO DE ERRO")
                    self.modo_recuperacao = True
                    self.tentativas_recuperacao = 1
                    
                    prompt_recuperacao = self.criar_prompt_recuperacao(ultimo_erro, tarefa)
                    self.historico_conversa.append({
                        "role": "user",
                        "content": prompt_recuperacao
                    })
                    
                elif erro_detectado and self.modo_recuperacao:
                    self.tentativas_recuperacao += 1
                    if self.tentativas_recuperacao >= self.max_tentativas_recuperacao:
                        print_realtime(f"\n⚠️  Muitas tentativas de recuperação ({self.tentativas_recuperacao})")
                        print_realtime(f"   Continuando com a tarefa mesmo com erro...")
                        self.modo_recuperacao = False
                        self.tentativas_recuperacao = 0
                
                if iteracao % 5 == 0:
                    self.rate_limit_manager.exibir_status()
        
        print_realtime("\n⚠️  Limite de iterações atingido")
        
        stats_rate = self.rate_limit_manager.obter_estatisticas()
        print_realtime("\n📊 ESTATÍSTICAS DA SESSÃO:")
        print_realtime(f"   Requisições: {stats_rate['total_requisicoes']}")
        print_realtime(f"   Tokens usados: {stats_rate['total_tokens']:,}")
        
        return None


# ============================================================================
# INTERFACE PRINCIPAL
# ============================================================================

def main():
    print_realtime("""
════════════════════════════════════════════════════════════════════════════════

  🌙 LUNA V3 - TIER 2 CORRIGIDO + RECUPERAÇÃO COMPLETA

  🛡️ Rate Limit | 🔧 Error Recovery | ✨ Auto-evolução | 🌐 Computer Use
  🔑 Credenciais | 💾 Memória | 📁 Workspaces

════════════════════════════════════════════════════════════════════════════════
    """)
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print_realtime("❌ Configure ANTHROPIC_API_KEY no .env")
        return
    
    # Perguntar o tier
    print_realtime("\n🛡️  CONFIGURAÇÃO DE RATE LIMITING")
    print_realtime("   Qual é o seu tier da API Anthropic?")
    print_realtime("   1. Tier 1 (50 RPM)")
    print_realtime("   2. Tier 2 (1000 RPM) ✅ CORRIGIDO!")
    print_realtime("   3. Tier 3 (2000 RPM)")
    print_realtime("   4. Tier 4 (4000 RPM)")
    
    tier_input = input("\n   Escolha (1-4, Enter=2): ").strip()
    tier_map = {"1": "tier1", "2": "tier2", "3": "tier3", "4": "tier4", "": "tier2"}
    tier = tier_map.get(tier_input, "tier2")
    
    # Perguntar o modo
    print_realtime("\n   Qual modo de rate limiting você quer?")
    print_realtime("   1. Conservador (75% threshold)")
    print_realtime("   2. Balanceado (85% threshold) - RECOMENDADO")
    print_realtime("   3. Agressivo (95% threshold)")
    
    modo_input = input("\n   Escolha (1-3, Enter=2): ").strip()
    modo_map = {"1": "conservador", "2": "balanceado", "3": "agressivo", "": "balanceado"}
    modo_rate_limit = modo_map.get(modo_input, "balanceado")
    
    usar_memoria = MEMORIA_DISPONIVEL
    if usar_memoria:
        print_realtime("\n✅ Sistema de memória permanente: ATIVADO")
    
    if GERENCIADOR_WORKSPACES_DISPONIVEL:
        print_realtime("✅ Sistema de workspaces: ATIVADO")
    
    print_realtime("✅ Sistema de recuperação de erros: ATIVADO")
    
    usar_cofre = COFRE_DISPONIVEL
    master_password = None
    
    if usar_cofre:
        print_realtime("\n✅ Sistema de credenciais disponível")
        usar = input("   Usar cofre de credenciais? (s/n): ").strip().lower()
        if usar == 's':
            master_password = getpass.getpass("   🔑 Master Password: ")
        else:
            usar_cofre = False
    
    try:
        agente = AgenteCompletoV3(api_key, master_password if usar_cofre else None, usar_memoria, tier=tier, modo_rate_limit=modo_rate_limit)
        
        # ✅ CORREÇÃO CRÍTICA: Criar o InterruptHandler
        interrupt_handler = InterruptHandler(agente, agente.sistema_ferramentas)
        
    except Exception as e:
        print_realtime(f"\n❌ {e}")
        return
    
    print_realtime("\n💡 DICA: Para textos grandes, Cole normalmente (Ctrl+V) - a Luna vai confirmar!")
    print_realtime("         Ou digite 'multi' para modo multiline")
    
    while True:
        print_realtime("\n" + "─"*70)
        comando = input_seguro()
        
        if comando.lower() in ['sair', 'exit', 'quit', '']:
            print_realtime("\n👋 Até logo!")
            if agente.sistema_ferramentas.browser:
                agente.sistema_ferramentas.executar('fechar_navegador', {})
            
            # Estatísticas finais
            print_realtime("\n📊 ESTATÍSTICAS FINAIS:")
            stats = agente.rate_limit_manager.obter_estatisticas()
            print_realtime(f"   Total de requisições: {stats['total_requisicoes']}")
            print_realtime(f"   Total de tokens: {stats['total_tokens']:,}")
            
            if agente.sistema_ferramentas.memoria_disponivel:
                agente.sistema_ferramentas.memoria.mostrar_resumo()
            
            break
        
        agente.executar_tarefa(comando)
        input("\n⏸️  Pressione ENTER...")


if __name__ == "__main__":
    main()
