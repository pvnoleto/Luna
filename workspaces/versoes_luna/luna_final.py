#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 LUNA - VERSÃO COM RATE LIMITING E RECUPERAÇÃO INTELIGENTE
=============================================================

✨ NOVIDADES DESTA VERSÃO:
1. 🛡️ ANTI-RATE LIMIT: Monitora tokens e previne erros 429
2. 🔧 RECUPERAÇÃO INTELIGENTE: Prioriza corrigir erros antes de continuar
3. 📊 Dashboard de recursos: Mostra uso de tokens em tempo real
4. ⏱️ Delay automático quando aproxima do limite

SISTEMA DE RATE LIMITING:
- Monitora tokens/minuto (TPM)
- Delay progressivo quando se aproxima do limite
- Exponential backoff em erros 429
- Alerta visual quando > 80% do limite

SISTEMA DE RECUPERAÇÃO:
- Detecta erros automaticamente
- Entra em "modo recuperação"
- Prioriza diagnóstico e correção
- Só volta à tarefa após resolver

Versão: 2025-10-15 (Rate Limit + Error Recovery)
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

# ✅ CRÍTICO: Desabilitar buffer para feedback EM TEMPO REAL
os.environ["PYTHONUNBUFFERED"] = "1"

# ✅ CORREÇÃO CRÍTICA: Forçar UTF-8 em TODO o Python
try:
    os.environ.setdefault("PYTHONUTF8", "1")
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
except Exception:
    pass

# ✅ CORREÇÃO: Forçar UTF-8 no console Windows
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

# ✅ CRÍTICO: Desabilitar buffer para feedback em tempo real
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

# Carregar configuração
load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))


# ============================================================================
# SISTEMA DE RATE LIMITING
# ============================================================================

class RateLimitManager:
    """Gerencia rate limits da API Anthropic com precisão"""
    
    def __init__(self, tier: str = "tier1", modo: str = "balanceado"):
        # Limites por tier (Anthropic)
        self.limites = {
            "tier1": {"tpm": 50000, "rpm": 50},
            "tier2": {"tpm": 100000, "rpm": 100},
            "tier3": {"tpm": 200000, "rpm": 200},
            "tier4": {"tpm": 400000, "rpm": 400}
        }
        
        self.tier = tier
        self.limite_tpm = self.limites[tier]["tpm"]
        self.limite_rpm = self.limites[tier]["rpm"]
        
        # Modo de operação (quanto mais agressivo, menos delays)
        # conservador: 75% threshold, seguro mas mais lento
        # balanceado: 85% threshold, bom equilíbrio (padrão)
        # agressivo: 95% threshold, máxima velocidade
        self.modos = {
            "conservador": {"tpm": 0.75, "rpm": 0.75},
            "balanceado": {"tpm": 0.85, "rpm": 0.85},
            "agressivo": {"tpm": 0.95, "rpm": 0.90}
        }
        
        self.modo = modo
        self.threshold_tpm = self.modos[modo]["tpm"]
        self.threshold_rpm = self.modos[modo]["rpm"]
        
        # Janela de 1 minuto
        self.janela_tempo = timedelta(minutes=1)
        self.historico_requisicoes = []
        self.historico_tokens = []
        
        # Estatísticas
        self.total_requisicoes = 0
        self.total_tokens = 0
        self.total_esperas = 0
        self.tempo_total_espera = 0
        
        # Tracking de tokens reais vs estimados
        self.tokens_estimados_total = 0
        self.tokens_reais_total = 0
        
        print(f"🛡️  Rate Limit Manager: {tier.upper()} - Modo {modo.upper()}", flush=True)
        print(f"   Limites: {self.limite_tpm:,} TPM | {self.limite_rpm} RPM", flush=True)
        print(f"   Thresholds: {self.threshold_tpm*100:.0f}% TPM | {self.threshold_rpm*100:.0f}% RPM", flush=True)
    
    def registrar_uso(self, tokens_input: int, tokens_output: int):
        """Registra uso de tokens e requisição"""
        agora = datetime.now()
        tokens_total = tokens_input + tokens_output
        
        self.historico_requisicoes.append(agora)
        self.historico_tokens.append((agora, tokens_total))
        
        self.total_requisicoes += 1
        self.total_tokens += tokens_total
        self.tokens_reais_total += tokens_total
        
        # Limpar histórico antigo (> 1 minuto)
        self._limpar_historico_antigo(agora)
    
    def _limpar_historico_antigo(self, agora):
        """Remove entradas antigas do histórico"""
        limite_tempo = agora - self.janela_tempo
        
        self.historico_requisicoes = [
            t for t in self.historico_requisicoes if t > limite_tempo
        ]
        
        self.historico_tokens = [
            (t, tokens) for t, tokens in self.historico_tokens if t > limite_tempo
        ]
    
    def calcular_uso_atual(self):
        """Calcula uso atual (última janela de 1 min)"""
        agora = datetime.now()
        self._limpar_historico_antigo(agora)
        
        rpm_atual = len(self.historico_requisicoes)
        tpm_atual = sum(tokens for _, tokens in self.historico_tokens)
        
        return {
            "rpm_atual": rpm_atual,
            "tpm_atual": tpm_atual,
            "rpm_percent": (rpm_atual / self.limite_rpm) * 100,
            "tpm_percent": (tpm_atual / self.limite_tpm) * 100,
            "rpm_disponivel": self.limite_rpm - rpm_atual,
            "tpm_disponivel": self.limite_tpm - tpm_atual
        }
    
    def estimar_tokens_proxima_req(self) -> int:
        """Estima tokens da próxima requisição baseado na média real"""
        if self.total_requisicoes == 0:
            return 2000  # Estimativa inicial
        
        # Usar média dos últimos 5 requests ou média geral
        tokens_recentes = [tokens for _, tokens in self.historico_tokens[-5:]]
        if tokens_recentes:
            media_recente = sum(tokens_recentes) / len(tokens_recentes)
            # Adicionar margem de segurança de 20%
            return int(media_recente * 1.2)
        
        # Fallback: média geral
        media_geral = self.total_tokens / self.total_requisicoes
        return int(media_geral * 1.2)
    
    def precisa_esperar(self, tokens_estimados: int = None):
        """Verifica se precisa esperar antes de fazer requisição"""
        uso = self.calcular_uso_atual()
        
        # Se não forneceu estimativa, usar cálculo inteligente
        if tokens_estimados is None:
            tokens_estimados = self.estimar_tokens_proxima_req()
        
        self.tokens_estimados_total += tokens_estimados
        
        # Verificar se vai ultrapassar thresholds
        rpm_ultrapassaria = (uso["rpm_atual"] + 1) > (self.limite_rpm * self.threshold_rpm)
        tpm_ultrapassaria = (uso["tpm_atual"] + tokens_estimados) > (self.limite_tpm * self.threshold_tpm)
        
        if rpm_ultrapassaria or tpm_ultrapassaria:
            # Calcular tempo de espera baseado na requisição mais antiga
            if self.historico_requisicoes:
                tempo_mais_antigo = min(self.historico_requisicoes)
                tempo_passado = (datetime.now() - tempo_mais_antigo).total_seconds()
                tempo_espera = max(1, int(60 - tempo_passado + 1))  # +1 segundo de margem
                
                # Mensagem mais informativa
                motivo = []
                if rpm_ultrapassaria:
                    motivo.append(f"RPM: {uso['rpm_atual']+1}/{self.limite_rpm}")
                if tpm_ultrapassaria:
                    motivo.append(f"TPM: {uso['tpm_atual']+tokens_estimados:,}/{self.limite_tpm:,}")
                
                return True, tempo_espera, ", ".join(motivo)
            
            return True, 5, "Preventivo"  # Espera padrão
        
        return False, 0, None
    
    def aguardar_se_necessario(self, tokens_estimados: int = None):
        """Espera se necessário para não bater no limite"""
        precisa, segundos, motivo = self.precisa_esperar(tokens_estimados)
        
        if precisa:
            uso = self.calcular_uso_atual()
            print(f"\n⏳ Aguardando {segundos}s para respeitar rate limit", flush=True)
            print(f"   Motivo: {motivo}", flush=True)
            print(f"   Uso atual: TPM {uso['tpm_percent']:.1f}% | RPM {uso['rpm_percent']:.1f}%", flush=True)
            time.sleep(segundos)
            self.total_esperas += 1
            self.tempo_total_espera += segundos
    
    def exibir_status(self):
        """Mostra status atual do rate limiting"""
        uso = self.calcular_uso_atual()
        
        # Barra de progresso visual
        def barra(percent):
            largura = 20
            preenchido = int((percent / 100) * largura)
            # Limitar a 20 para não estourar a barra
            preenchido = min(preenchido, largura)
            barra_str = "█" * preenchido + "░" * (largura - preenchido)
            
            # Cores baseadas no nível
            if percent > 95:
                cor = "🔴"
            elif percent > 85:
                cor = "🟡"
            else:
                cor = "🟢"
            
            return f"{cor} {barra_str} {min(percent, 100):.1f}%"
        
        print(f"\n📊 STATUS DO RATE LIMIT:", flush=True)
        print(f"   TPM: {barra(uso['tpm_percent'])} ({uso['tpm_atual']:,}/{self.limite_tpm:,})", flush=True)
        print(f"   RPM: {barra(uso['rpm_percent'])} ({uso['rpm_atual']}/{self.limite_rpm})", flush=True)
        
        # Mostrar precisão da estimativa
        if self.tokens_reais_total > 0 and self.tokens_estimados_total > 0:
            precisao = (self.tokens_reais_total / self.tokens_estimados_total) * 100
            print(f"   Precisão estimativa: {precisao:.1f}% (quanto mais perto de 100%, melhor)", flush=True)
    
    def obter_estatisticas(self):
        """Retorna estatísticas gerais"""
        precisao_estimativa = 0
        if self.tokens_estimados_total > 0:
            precisao_estimativa = (self.tokens_reais_total / self.tokens_estimados_total) * 100
        
        return {
            "total_requisicoes": self.total_requisicoes,
            "total_tokens": self.total_tokens,
            "total_esperas": self.total_esperas,
            "tempo_total_espera": self.tempo_total_espera,
            "media_tokens_req": self.total_tokens / max(1, self.total_requisicoes),
            "precisao_estimativa": precisao_estimativa,
            "tokens_economizados": max(0, self.tokens_estimados_total - self.tokens_reais_total)
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
# AGENTE COM RATE LIMITING E RECUPERAÇÃO DE ERROS
# ============================================================================

class AgenteCompletoFinal:
    """Agente com rate limiting e recuperação inteligente de erros"""
    
    def __init__(self, api_key: str, master_password: str = None, usar_memoria: bool = True, tier: str = "tier1", modo_rate_limit: str = "balanceado"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.sistema_ferramentas = SistemaFerramentasCompleto(master_password, usar_memoria)
        self.historico_conversa = []
        self.max_iteracoes_atual = 40
        
        # Rate limit manager com modo configurável
        self.rate_limit_manager = RateLimitManager(tier=tier, modo=modo_rate_limit)
        
        # Sistema de recuperação de erros
        self.modo_recuperacao = False
        self.erros_recentes = []
        self.tentativas_recuperacao = 0
        self.max_tentativas_recuperacao = 3
    
    def detectar_erro(self, resultado: str) -> tuple:
        """Detecta se há erro no resultado de uma ferramenta"""
        # Detectar padrões de erro
        padrao_erro = resultado.startswith("ERRO:") or "ERRO:" in resultado[:100]
        
        if padrao_erro:
            # Extrair informação do erro
            linhas = resultado.split("\n")
            erro_principal = linhas[0] if linhas else resultado[:200]
            
            return True, erro_principal
        
        return False, None
    
    def criar_prompt_recuperacao(self, erro: str, tarefa_original: str):
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
    
    def executar_tarefa(self, tarefa: str, max_iteracoes: int = None):
        """Executa tarefa com rate limiting e recuperação de erros"""
        
        if max_iteracoes is None:
            max_iteracoes = self.max_iteracoes_atual
        else:
            self.max_iteracoes_atual = max_iteracoes
        
        # Limpeza automática
        if self.sistema_ferramentas.gerenciador_temp_disponivel:
            self.sistema_ferramentas.gerenciador_temp.limpar_arquivos_antigos(exibir_resumo=True)
        
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

FERRAMENTAS ESPECIAIS:
- Workspaces: criar_workspace, listar_workspaces, selecionar_workspace, listar_arquivos_workspace, buscar_arquivo_workspace, arvore_workspace
- Memória: salvar_aprendizado, buscar_aprendizados, salvar_preferencia
- Credenciais: obter_credencial, login_automatico
- Web: navegar_url, tirar_screenshot, clicar_elemento, preencher_campo
- Meta: criar_ferramenta, instalar_biblioteca

INSTRUÇÕES CRÍTICAS:
1. ANTES de tarefas, BUSQUE aprendizados relevantes
2. DEPOIS de resolver algo novo, SALVE o aprendizado
3. NUNCA mostre senhas ao usuário
4. USE login_automatico sempre que precisar de login
5. APRENDA com erros e sucessos
6. USE workspaces para organizar projetos (crie workspace para cada projeto)
7. Arquivos são criados NO WORKSPACE ATUAL automaticamente
8. SE ENCONTRAR ERRO: PARE e CORRIJA antes de continuar!

{contexto_aprendizados}{contexto_workspace}

TAREFA DO USUÁRIO:
{tarefa}

Comece BUSCANDO aprendizados relevantes, depois execute a tarefa!"""
        
        self.historico_conversa = [{"role": "user", "content": prompt_sistema}]
        
        # Reset estado de recuperação
        self.modo_recuperacao = False
        self.erros_recentes = []
        self.tentativas_recuperacao = 0
        
        print("\n" + "="*70)
        print(f"🎯 TAREFA: {tarefa}")
        print("="*70)
        
        # Status com ícones
        status = []
        if self.sistema_ferramentas.cofre_disponivel:
            status.append("🔑 Cofre")
        if self.sistema_ferramentas.memoria_disponivel:
            stats = self.sistema_ferramentas.memoria.obter_estatisticas()
            status.append(f"💾 Memória ({stats['total_aprendizados']})")
        if self.sistema_ferramentas.gerenciador_workspaces_disponivel:
            total_ws = len(self.sistema_ferramentas.gerenciador_workspaces.listar_workspaces())
            status.append(f"📁 Workspaces ({total_ws})")
        status.append(f"🔧 {len(self.sistema_ferramentas.ferramentas_descricao)} ferramentas")
        status.append(f"🔄 Max: {max_iteracoes}")
        status.append(f"🛡️ Rate Limit: {self.rate_limit_manager.tier.upper()}")
        
        print(" | ".join(status))
        print("-" * 70)
        
        # Exibir status inicial do rate limit
        self.rate_limit_manager.exibir_status()
        
        for iteracao in range(1, max_iteracoes + 1):
            # Indicador de modo recuperação
            modo_tag = "🔧 RECUPERAÇÃO" if self.modo_recuperacao else f"🔄 Iteração {iteracao}/{max_iteracoes}"
            print(f"\n{modo_tag}", flush=True)
            
            # Rate limiting antes da requisição (estimativa automática baseada em histórico)
            self.rate_limit_manager.aguardar_se_necessario()
            
            try:
                response = self.client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=4096,
                    tools=self.sistema_ferramentas.obter_descricoes(),
                    messages=self.historico_conversa
                )
                
                # Registrar uso de tokens
                tokens_input = response.usage.input_tokens
                tokens_output = response.usage.output_tokens
                self.rate_limit_manager.registrar_uso(tokens_input, tokens_output)
                
            except RateLimitError as e:
                print(f"\n⚠️  RATE LIMIT ATINGIDO!")
                print(f"   Aguardando 60 segundos...")
                time.sleep(60)
                continue
                
            except BadRequestError as e:
                error_msg = str(e)
                if "JSON schema is invalid" in error_msg:
                    print(f"\n❌ Schema JSON inválido")
                    if len(self.sistema_ferramentas.ferramentas_descricao) > 20:
                        ultima = self.sistema_ferramentas.ferramentas_descricao.pop()
                        print(f"⚠️  Removendo ferramenta: {ultima['name']}")
                        continue
                    else:
                        break
                else:
                    print(f"\n❌ {e}")
                    break
            except Exception as e:
                print(f"\n❌ API: {e}")
                break
            
            if response.stop_reason == "end_turn":
                resposta_final = ""
                for block in response.content:
                    if hasattr(block, "text"):
                        resposta_final += block.text
                
                # Verificar se estava em modo recuperação
                if self.modo_recuperacao:
                    print("\n✅ Erro resolvido! Voltando à tarefa principal...")
                    self.modo_recuperacao = False
                    self.tentativas_recuperacao = 0
                    continue  # Continuar com a tarefa
                
                if self.sistema_ferramentas.memoria_disponivel:
                    ferramentas_usadas = [h["name"] for h in self.historico_conversa 
                                        if isinstance(h.get("content"), list)
                                        for item in h["content"]
                                        if isinstance(item, dict) and item.get("type") == "tool_use"]
                    
                    self.sistema_ferramentas.memoria.registrar_tarefa(
                        tarefa, resposta_final[:500], ferramentas_usadas, True
                    )
                
                print("\n" + "="*70)
                print("✅ CONCLUÍDO!")
                print("="*70)
                print(resposta_final)
                print("="*70)
                
                # Estatísticas finais
                print("\n📊 ESTATÍSTICAS DA SESSÃO:")
                stats_rate = self.rate_limit_manager.obter_estatisticas()
                print(f"   Requisições: {stats_rate['total_requisicoes']}")
                print(f"   Tokens usados: {stats_rate['total_tokens']:,}")
                print(f"   Média tokens/req: {stats_rate['media_tokens_req']:.0f}")
                if stats_rate['precisao_estimativa'] > 0:
                    print(f"   Precisão estimativa: {stats_rate['precisao_estimativa']:.1f}%")
                if stats_rate['total_esperas'] > 0:
                    print(f"   Esperas: {stats_rate['total_esperas']} ({stats_rate['tempo_total_espera']:.0f}s total)")
                print()
                
                if self.sistema_ferramentas.auto_evolucao_disponivel:
                    self.processar_auto_melhorias()
                
                return resposta_final
            
            if response.stop_reason == "tool_use":
                self.historico_conversa.append({"role": "assistant", "content": response.content})
                
                # Mostrar pensamento da Luna
                pensamento = ""
                for block in response.content:
                    if hasattr(block, "text") and block.text:
                        pensamento = block.text[:120]
                        break
                
                if pensamento:
                    print(f"💭 {pensamento}...", flush=True)
                
                tool_results = []
                ferramentas_usadas = []
                erro_detectado = False
                ultimo_erro = None
                
                for block in response.content:
                    if block.type == "tool_use":
                        nome = block.name
                        params = block.input
                        
                        # Ocultar senhas
                        params_display = params.copy()
                        if 'senha' in params_display:
                            params_display['senha'] = '***'
                        
                        # Mostrar qual ferramenta está usando
                        print(f"🔧 {nome}", flush=True)
                        ferramentas_usadas.append(nome)
                        
                        resultado = self.sistema_ferramentas.executar(nome, params)
                        
                        # Detectar erro no resultado
                        tem_erro, erro_info = self.detectar_erro(resultado)
                        if tem_erro:
                            erro_detectado = True
                            ultimo_erro = erro_info
                            print(f"  ⚠️  ERRO DETECTADO: {erro_info[:80]}", flush=True)
                            self.erros_recentes.append({
                                'ferramenta': nome,
                                'erro': erro_info,
                                'iteracao': iteracao
                            })
                        
                        if isinstance(resultado, tuple):
                            resultado_str, novo_limite = resultado
                            if novo_limite:
                                max_iteracoes = novo_limite
                                self.max_iteracoes_atual = novo_limite
                                print(f"  ⚙️  Limite → {novo_limite}", flush=True)
                            resultado = resultado_str
                        
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": resultado
                        })
                
                # Resumo da iteração
                if len(ferramentas_usadas) > 1:
                    print(f"📊 {len(ferramentas_usadas)} ferramenta(s) usadas", flush=True)
                
                self.historico_conversa.append({"role": "user", "content": tool_results})
                
                # SISTEMA DE RECUPERAÇÃO DE ERROS
                if erro_detectado and not self.modo_recuperacao:
                    print(f"\n🚨 ENTRANDO EM MODO DE RECUPERAÇÃO DE ERRO", flush=True)
                    self.modo_recuperacao = True
                    self.tentativas_recuperacao = 1
                    
                    # Adicionar prompt de recuperação
                    prompt_recuperacao = self.criar_prompt_recuperacao(ultimo_erro, tarefa)
                    self.historico_conversa.append({
                        "role": "user",
                        "content": prompt_recuperacao
                    })
                    
                elif erro_detectado and self.modo_recuperacao:
                    self.tentativas_recuperacao += 1
                    if self.tentativas_recuperacao >= self.max_tentativas_recuperacao:
                        print(f"\n⚠️  Muitas tentativas de recuperação ({self.tentativas_recuperacao})")
                        print(f"   Continuando com a tarefa mesmo com erro...")
                        self.modo_recuperacao = False
                        self.tentativas_recuperacao = 0
                
                # Exibir status do rate limit periodicamente
                if iteracao % 5 == 0:
                    self.rate_limit_manager.exibir_status()
        
        print("\n⚠️  Limite de iterações atingido")
        
        # Estatísticas finais
        print("\n📊 ESTATÍSTICAS DA SESSÃO:")
        stats_rate = self.rate_limit_manager.obter_estatisticas()
        print(f"   Requisições: {stats_rate['total_requisicoes']}")
        print(f"   Tokens usados: {stats_rate['total_tokens']:,}")
        print(f"   Média tokens/req: {stats_rate['media_tokens_req']:.0f}")
        if stats_rate['precisao_estimativa'] > 0:
            print(f"   Precisão estimativa: {stats_rate['precisao_estimativa']:.1f}%")
        if stats_rate['total_esperas'] > 0:
            print(f"   Esperas: {stats_rate['total_esperas']} ({stats_rate['tempo_total_espera']:.0f}s total)")
        
        return None
    
    def processar_auto_melhorias(self):
        """Processa melhorias anotadas"""
        if not self.sistema_ferramentas.fila_melhorias:
            return
        
        melhorias_pendentes = self.sistema_ferramentas.fila_melhorias.obter_pendentes()
        if not melhorias_pendentes:
            return
        
        resultados = self.sistema_ferramentas.sistema_evolucao.processar_fila(
            self.sistema_ferramentas.fila_melhorias,
            self.sistema_ferramentas.memoria if self.sistema_ferramentas.memoria_disponivel else None
        )
        
        self.sistema_ferramentas.fila_melhorias.limpar()


# ============================================================================
# INTERFACE
# ============================================================================

def main():
    print("""
════════════════════════════════════════════════════════════════════════════════

  🌙 LUNA - AGENTE COM RATE LIMITING E RECUPERAÇÃO INTELIGENTE

  🛡️ Rate Limit | 🔧 Error Recovery | ✨ Auto-evolução | 🌐 Computer Use
  🔑 Credenciais | 💾 Memória | 📁 Workspaces

════════════════════════════════════════════════════════════════════════════════
    """)
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ Configure ANTHROPIC_API_KEY no .env")
        return
    
    # Perguntar o tier
    print("\n🛡️  CONFIGURAÇÃO DE RATE LIMITING")
    print("   Qual é o seu tier da API Anthropic?")
    print("   1. Tier 1 (50k TPM, 50 RPM) - Padrão")
    print("   2. Tier 2 (100k TPM, 100 RPM)")
    print("   3. Tier 3 (200k TPM, 200 RPM)")
    print("   4. Tier 4 (400k TPM, 400 RPM)")
    
    tier_input = input("\n   Escolha (1-4, Enter=1): ").strip()
    tier_map = {"1": "tier1", "2": "tier2", "3": "tier3", "4": "tier4", "": "tier1"}
    tier = tier_map.get(tier_input, "tier1")
    
    # Perguntar o modo
    print("\n   Qual modo de rate limiting você quer?")
    print("   1. Conservador (75% threshold) - Mais seguro, mais lento")
    print("   2. Balanceado (85% threshold) - Equilíbrio (RECOMENDADO)")
    print("   3. Agressivo (95% threshold) - Máxima velocidade, menos delays")
    
    modo_input = input("\n   Escolha (1-3, Enter=2): ").strip()
    modo_map = {"1": "conservador", "2": "balanceado", "3": "agressivo", "": "balanceado"}
    modo_rate_limit = modo_map.get(modo_input, "balanceado")
    
    usar_memoria = MEMORIA_DISPONIVEL
    if usar_memoria:
        print("\n✅ Sistema de memória permanente: ATIVADO")
    
    if GERENCIADOR_WORKSPACES_DISPONIVEL:
        print("✅ Sistema de workspaces: ATIVADO")
    
    print("✅ Sistema de recuperação de erros: ATIVADO")
    
    usar_cofre = COFRE_DISPONIVEL
    if usar_cofre:
        print("\n✅ Sistema de credenciais disponível")
        usar = input("   Usar cofre de credenciais? (s/n): ").strip().lower()
        if usar != 's':
            usar_cofre = False
            master_password = None
        else:
            master_password = getpass.getpass("   🔑 Master Password: ")
    else:
        master_password = None
    
    try:
        agente = AgenteCompletoFinal(api_key, master_password if usar_cofre else None, usar_memoria, tier=tier, modo_rate_limit=modo_rate_limit)
    except Exception as e:
        print(f"\n❌ {e}")
        return
    
    if agente.sistema_ferramentas.gerenciador_workspaces_disponivel:
        workspaces = agente.sistema_ferramentas.gerenciador_workspaces.listar_workspaces()
        if workspaces:
            print(f"\n📁 {len(workspaces)} workspace(s) encontrado(s):")
            for ws in workspaces[:3]:
                marcador = "🎯" if ws['atual'] else "  "
                print(f"   {marcador} {ws['nome']}")
    
    # Dica sobre paste e multiline
    print("\n💡 DICA: Para textos grandes, Cole normalmente (Ctrl+V) - a Luna vai confirmar!")
    print("         Ou digite 'multi' para modo multiline (útil para prompts complexos)")
    
    while True:
        print("\n" + "─"*70)
        comando = input_seguro()
        
        if comando.lower() in ['sair', 'exit', 'quit', '']:
            print("\n👋 Até logo!")
            if agente.sistema_ferramentas.browser:
                agente.sistema_ferramentas.executar('fechar_navegador', {})
            
            # Estatísticas finais do rate limit
            print("\n📊 ESTATÍSTICAS FINAIS DE RATE LIMITING:")
            stats = agente.rate_limit_manager.obter_estatisticas()
            print(f"   Total de requisições: {stats['total_requisicoes']}")
            print(f"   Total de tokens: {stats['total_tokens']:,}")
            print(f"   Média tokens/req: {stats['media_tokens_req']:.0f}")
            if stats['precisao_estimativa'] > 0:
                print(f"   Precisão estimativa: {stats['precisao_estimativa']:.1f}%")
                if stats['precisao_estimativa'] < 80:
                    print(f"   ⚠️  Estimativas imprecisas - considere modo mais conservador")
                elif stats['precisao_estimativa'] > 120:
                    print(f"   💡 Estimativas muito altas - considere modo mais agressivo")
            if stats['total_esperas'] > 0:
                print(f"   Total de esperas: {stats['total_esperas']}")
                print(f"   Tempo total esperado: {stats['tempo_total_espera']:.0f}s")
            
            if agente.sistema_ferramentas.memoria_disponivel:
                agente.sistema_ferramentas.memoria.mostrar_resumo()
            
            if agente.sistema_ferramentas.gerenciador_workspaces_disponivel:
                print("\n📊 Status final dos workspaces:")
                agente.sistema_ferramentas.gerenciador_workspaces.exibir_status()
            
            break
        
        agente.executar_tarefa(comando)
        input("\n⏸️  Pressione ENTER...")


if __name__ == "__main__":
    main()

