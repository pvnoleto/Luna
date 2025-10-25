#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 SISTEMA DE TELEMETRIA E ANÁLISE - LUNA V3
============================================

Sistema completo de monitoramento, logging e análise automática de uso da Luna.

Funcionalidades:
- Registro de uso de ferramentas (nome, parâmetros, tempo, resultado)
- Registro de requisições API (tokens, cache, latência)
- Registro de sessões (início, fim, métricas totais)
- Análise automática de gargalos e padrões
- Sugestões de otimização baseadas em dados
- Detecção de regressões de performance
- Dashboard de métricas em tempo real

Criado: 2025-10-20
Parte do sistema de melhorias Luna V3
"""

import json
import time
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import statistics

# ============================================================================
# CONFIGURAÇÃO UTF-8 (Windows)
# ============================================================================
import sys
if sys.platform == 'win32':
    os.environ['PYTHONUTF8'] = '1'
    os.environ['PYTHONIOENCODING'] = 'utf-8'


# ============================================================================
# DATACLASSES PARA TELEMETRIA
# ============================================================================

@dataclass
class EventoFerramenta:
    """Evento de uso de ferramenta"""
    timestamp: str
    ferramenta: str
    parametros: Dict[str, Any]
    resultado_tipo: str  # sucesso, erro, timeout
    tempo_execucao: float
    tokens_estimados: int = 0
    erro_msg: Optional[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class EventoAPI:
    """Evento de requisição à API"""
    timestamp: str
    tokens_input: int
    tokens_output: int
    tokens_cache_read: int
    tokens_cache_creation: int
    cache_hit: bool
    tempo_latencia: float
    modelo: str

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class EventoSessao:
    """Evento de sessão completa"""
    timestamp_inicio: str
    timestamp_fim: str
    duracao_total: float
    total_requisicoes: int
    total_tokens_input: int
    total_tokens_output: int
    total_ferramentas_usadas: int
    ferramentas_por_tipo: Dict[str, int]
    taxa_cache_hit: float
    economia_tokens: int
    erros_count: int

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Gargalo:
    """Gargalo identificado na análise"""
    tipo: str  # ferramenta_lenta, api_lenta, erro_frequente
    descricao: str
    metricas: Dict[str, Any]
    severidade: str  # baixa, media, alta, critica
    sugestao_otimizacao: str


@dataclass
class Sugestao:
    """Sugestão de otimização"""
    titulo: str
    descricao: str
    impacto_estimado: str  # baixo, medio, alto
    facilidade_implementacao: str  # facil, moderada, dificil
    codigo_exemplo: Optional[str] = None


# ============================================================================
# TELEMETRIA MANAGER - Registro de Eventos
# ============================================================================

class TelemetriaManager:
    """
    Gerencia registro de eventos de telemetria em arquivos JSONL.

    Arquivos gerados:
    - luna_telemetria_ferramentas.jsonl: Uso de ferramentas
    - luna_telemetria_api.jsonl: Requisições API
    - luna_performance.json: Métricas de sessões
    """

    def __init__(self, base_dir: str = "."):
        """
        Inicializa o gerenciador de telemetria.

        Args:
            base_dir: Diretório base para salvar logs
        """
        self.base_dir = Path(base_dir)

        # Arquivos de log
        self.log_ferramentas = self.base_dir / "luna_telemetria_ferramentas.jsonl"
        self.log_api = self.base_dir / "luna_telemetria_api.jsonl"
        self.log_sessoes = self.base_dir / "luna_performance.json"

        # Métricas da sessão atual (em memória)
        self.sessao_inicio: Optional[float] = None
        self.sessao_metricas = {
            'requisicoes': 0,
            'tokens_input': 0,
            'tokens_output': 0,
            'tokens_cache_read': 0,
            'tokens_cache_creation': 0,
            'cache_hits': 0,
            'ferramentas_usadas': [],
            'erros': 0,
            'tempo_total_ferramentas': 0
        }

        # Criar arquivos se não existirem
        self._inicializar_logs()

    def _inicializar_logs(self):
        """Cria arquivos de log se não existirem"""
        for log_file in [self.log_ferramentas, self.log_api]:
            if not log_file.exists():
                log_file.touch()

        if not self.log_sessoes.exists():
            with open(self.log_sessoes, 'w', encoding='utf-8') as f:
                json.dump({'sessoes': []}, f, indent=2)

    def iniciar_sessao(self):
        """Marca início de uma sessão"""
        self.sessao_inicio = time.time()
        self.sessao_metricas = {
            'requisicoes': 0,
            'tokens_input': 0,
            'tokens_output': 0,
            'tokens_cache_read': 0,
            'tokens_cache_creation': 0,
            'cache_hits': 0,
            'ferramentas_usadas': [],
            'erros': 0,
            'tempo_total_ferramentas': 0
        }

    def registrar_uso_ferramenta(
        self,
        nome: str,
        parametros: Dict[str, Any],
        resultado: str,
        tempo_execucao: float,
        tokens_estimados: int = 0,
        erro: Optional[str] = None
    ):
        """
        Registra uso de uma ferramenta.

        Args:
            nome: Nome da ferramenta
            parametros: Parâmetros passados
            resultado: String com resultado da execução
            tempo_execucao: Tempo em segundos
            tokens_estimados: Estimativa de tokens consumidos
            erro: Mensagem de erro se houver
        """
        # Criar evento
        resultado_tipo = 'erro' if erro else 'sucesso'

        evento = EventoFerramenta(
            timestamp=datetime.now().isoformat(),
            ferramenta=nome,
            parametros=self._sanitizar_parametros(parametros),
            resultado_tipo=resultado_tipo,
            tempo_execucao=round(tempo_execucao, 3),
            tokens_estimados=tokens_estimados,
            erro_msg=erro
        )

        # Salvar em JSONL (uma linha por evento)
        with open(self.log_ferramentas, 'a', encoding='utf-8') as f:
            f.write(json.dumps(evento.to_dict(), ensure_ascii=False) + '\n')

        # Atualizar métricas da sessão
        self.sessao_metricas['ferramentas_usadas'].append(nome)
        self.sessao_metricas['tempo_total_ferramentas'] += tempo_execucao
        if erro:
            self.sessao_metricas['erros'] += 1

    def registrar_requisicao_api(
        self,
        tokens_input: int,
        tokens_output: int,
        tokens_cache_read: int = 0,
        tokens_cache_creation: int = 0,
        tempo_latencia: float = 0.0,
        modelo: str = "claude-sonnet-4"
    ):
        """
        Registra uma requisição à API do Claude.

        Args:
            tokens_input: Tokens de input
            tokens_output: Tokens de output
            tokens_cache_read: Tokens lidos do cache
            tokens_cache_creation: Tokens escritos no cache
            tempo_latencia: Tempo de resposta da API
            modelo: Modelo usado
        """
        cache_hit = tokens_cache_read > 0

        evento = EventoAPI(
            timestamp=datetime.now().isoformat(),
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            tokens_cache_read=tokens_cache_read,
            tokens_cache_creation=tokens_cache_creation,
            cache_hit=cache_hit,
            tempo_latencia=round(tempo_latencia, 3),
            modelo=modelo
        )

        # Salvar em JSONL
        with open(self.log_api, 'a', encoding='utf-8') as f:
            f.write(json.dumps(evento.to_dict(), ensure_ascii=False) + '\n')

        # Atualizar métricas da sessão
        self.sessao_metricas['requisicoes'] += 1
        self.sessao_metricas['tokens_input'] += tokens_input
        self.sessao_metricas['tokens_output'] += tokens_output
        self.sessao_metricas['tokens_cache_read'] += tokens_cache_read
        self.sessao_metricas['tokens_cache_creation'] += tokens_cache_creation
        if cache_hit:
            self.sessao_metricas['cache_hits'] += 1

    def finalizar_sessao(self):
        """Finaliza sessão e salva métricas consolidadas"""
        if self.sessao_inicio is None:
            return

        duracao = time.time() - self.sessao_inicio

        # Calcular métricas
        total_req = self.sessao_metricas['requisicoes']
        taxa_cache = (
            (self.sessao_metricas['cache_hits'] / total_req * 100)
            if total_req > 0 else 0
        )

        economia_tokens = self.sessao_metricas['tokens_cache_read']

        # Contar ferramentas por tipo
        ferramentas_count = Counter(self.sessao_metricas['ferramentas_usadas'])

        # Criar evento de sessão
        evento_sessao = EventoSessao(
            timestamp_inicio=datetime.fromtimestamp(self.sessao_inicio).isoformat(),
            timestamp_fim=datetime.now().isoformat(),
            duracao_total=round(duracao, 2),
            total_requisicoes=total_req,
            total_tokens_input=self.sessao_metricas['tokens_input'],
            total_tokens_output=self.sessao_metricas['tokens_output'],
            total_ferramentas_usadas=len(self.sessao_metricas['ferramentas_usadas']),
            ferramentas_por_tipo=dict(ferramentas_count),
            taxa_cache_hit=round(taxa_cache, 1),
            economia_tokens=economia_tokens,
            erros_count=self.sessao_metricas['erros']
        )

        # Salvar no arquivo de sessões
        try:
            with open(self.log_sessoes, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {'sessoes': []}

        data['sessoes'].append(evento_sessao.to_dict())

        # Manter apenas últimas 50 sessões
        data['sessoes'] = data['sessoes'][-50:]

        with open(self.log_sessoes, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _sanitizar_parametros(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Remove dados sensíveis dos parâmetros antes de logar"""
        sanitizado = {}

        campos_sensiveis = {'senha', 'password', 'token', 'api_key', 'secret', 'credential'}

        for key, value in params.items():
            # Verificar se é campo sensível
            if any(campo in key.lower() for campo in campos_sensiveis):
                sanitizado[key] = '***REDACTED***'
            # Limitar tamanho de strings grandes
            elif isinstance(value, str) and len(value) > 200:
                sanitizado[key] = value[:200] + '... (truncado)'
            else:
                sanitizado[key] = value

        return sanitizado

    def obter_metricas_sessao(self) -> Dict[str, Any]:
        """Retorna métricas da sessão atual"""
        if self.sessao_inicio is None:
            return {}

        duracao = time.time() - self.sessao_inicio
        total_req = self.sessao_metricas['requisicoes']
        taxa_cache = (
            (self.sessao_metricas['cache_hits'] / total_req * 100)
            if total_req > 0 else 0
        )

        return {
            'duracao_sessao': round(duracao, 2),
            'total_requisicoes': total_req,
            'total_tokens': self.sessao_metricas['tokens_input'] + self.sessao_metricas['tokens_output'],
            'taxa_cache_hit': round(taxa_cache, 1),
            'economia_tokens': self.sessao_metricas['tokens_cache_read'],
            'total_ferramentas': len(self.sessao_metricas['ferramentas_usadas']),
            'erros': self.sessao_metricas['erros']
        }


# ============================================================================
# ANALISADOR DE TELEMETRIA - Análise e Sugestões
# ============================================================================

class AnalisadorTelemetria:
    """
    Analisa logs de telemetria e gera insights, detecta gargalos e sugere otimizações.
    """

    def __init__(self, base_dir: str = "."):
        """
        Inicializa o analisador.

        Args:
            base_dir: Diretório com os arquivos de log
        """
        self.base_dir = Path(base_dir)
        self.log_ferramentas = self.base_dir / "luna_telemetria_ferramentas.jsonl"
        self.log_api = self.base_dir / "luna_telemetria_api.jsonl"
        self.log_sessoes = self.base_dir / "luna_performance.json"

    def carregar_eventos_ferramentas(self, limite: Optional[int] = None) -> List[Dict]:
        """Carrega eventos de ferramentas do JSONL"""
        eventos = []

        if not self.log_ferramentas.exists():
            return eventos

        with open(self.log_ferramentas, 'r', encoding='utf-8') as f:
            for linha in f:
                if linha.strip():
                    eventos.append(json.loads(linha))

        # Retornar os mais recentes
        if limite:
            return eventos[-limite:]
        return eventos

    def carregar_eventos_api(self, limite: Optional[int] = None) -> List[Dict]:
        """Carrega eventos de API do JSONL"""
        eventos = []

        if not self.log_api.exists():
            return eventos

        with open(self.log_api, 'r', encoding='utf-8') as f:
            for linha in f:
                if linha.strip():
                    eventos.append(json.loads(linha))

        if limite:
            return eventos[-limite:]
        return eventos

    def carregar_sessoes(self, limite: Optional[int] = None) -> List[Dict]:
        """Carrega histórico de sessões"""
        try:
            with open(self.log_sessoes, 'r', encoding='utf-8') as f:
                data = json.load(f)
                sessoes = data.get('sessoes', [])

                if limite:
                    return sessoes[-limite:]
                return sessoes
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def detectar_gargalos(self, limite_eventos: int = 1000) -> List[Gargalo]:
        """
        Detecta gargalos de performance.

        Analisa:
        - Ferramentas lentas (tempo > 5s)
        - Requisições API lentas (latência > 10s)
        - Erros frequentes (mesma ferramenta falhando)
        - Cache hit rate baixo (< 30%)

        Args:
            limite_eventos: Número de eventos recentes a analisar

        Returns:
            Lista de gargalos identificados
        """
        gargalos = []

        # Analisar ferramentas
        eventos_ferramentas = self.carregar_eventos_ferramentas(limite_eventos)

        if eventos_ferramentas:
            # 1. Ferramentas lentas
            ferramentas_tempo = defaultdict(list)
            for evento in eventos_ferramentas:
                ferramentas_tempo[evento['ferramenta']].append(evento['tempo_execucao'])

            for ferramenta, tempos in ferramentas_tempo.items():
                tempo_medio = statistics.mean(tempos)
                tempo_max = max(tempos)

                if tempo_medio > 5.0:  # Mais de 5 segundos em média
                    severidade = 'alta' if tempo_medio > 15 else 'media'

                    gargalos.append(Gargalo(
                        tipo='ferramenta_lenta',
                        descricao=f"Ferramenta '{ferramenta}' está lenta",
                        metricas={
                            'tempo_medio': round(tempo_medio, 2),
                            'tempo_max': round(tempo_max, 2),
                            'execucoes': len(tempos)
                        },
                        severidade=severidade,
                        sugestao_otimizacao=(
                            f"Considere otimizar '{ferramenta}' ou executar em paralelo. "
                            f"Tempo médio: {tempo_medio:.1f}s"
                        )
                    ))

            # 2. Erros frequentes
            erros_por_ferramenta = defaultdict(int)
            total_por_ferramenta = defaultdict(int)

            for evento in eventos_ferramentas:
                ferramenta = evento['ferramenta']
                total_por_ferramenta[ferramenta] += 1
                if evento['resultado_tipo'] == 'erro':
                    erros_por_ferramenta[ferramenta] += 1

            for ferramenta, erros in erros_por_ferramenta.items():
                total = total_por_ferramenta[ferramenta]
                taxa_erro = (erros / total * 100) if total > 0 else 0

                if taxa_erro > 20 and erros >= 3:  # Mais de 20% de erros e pelo menos 3 erros
                    severidade = 'critica' if taxa_erro > 50 else 'alta'

                    gargalos.append(Gargalo(
                        tipo='erro_frequente',
                        descricao=f"Ferramenta '{ferramenta}' falha frequentemente",
                        metricas={
                            'taxa_erro': round(taxa_erro, 1),
                            'total_erros': erros,
                            'total_execucoes': total
                        },
                        severidade=severidade,
                        sugestao_otimizacao=(
                            f"Revisar implementação de '{ferramenta}'. "
                            f"Taxa de erro: {taxa_erro:.1f}%"
                        )
                    ))

        # Analisar API
        eventos_api = self.carregar_eventos_api(limite_eventos)

        if eventos_api:
            # 3. API lenta
            latencias = [e['tempo_latencia'] for e in eventos_api if e['tempo_latencia'] > 0]

            if latencias:
                latencia_media = statistics.mean(latencias)
                latencia_max = max(latencias)

                if latencia_media > 10.0:  # Mais de 10s em média
                    gargalos.append(Gargalo(
                        tipo='api_lenta',
                        descricao="Latência da API está alta",
                        metricas={
                            'latencia_media': round(latencia_media, 2),
                            'latencia_max': round(latencia_max, 2),
                            'requisicoes': len(latencias)
                        },
                        severidade='media',
                        sugestao_otimizacao=(
                            f"Latência média: {latencia_media:.1f}s. "
                            "Verifique conexão ou use batching para reduzir requisições."
                        )
                    ))

            # 4. Cache hit rate baixo
            total_requisicoes = len(eventos_api)
            cache_hits = sum(1 for e in eventos_api if e['cache_hit'])
            cache_rate = (cache_hits / total_requisicoes * 100) if total_requisicoes > 0 else 0

            if cache_rate < 30 and total_requisicoes >= 10:  # Menos de 30% de cache hit
                gargalos.append(Gargalo(
                    tipo='cache_baixo',
                    descricao="Taxa de cache hit está baixa",
                    metricas={
                        'taxa_cache_hit': round(cache_rate, 1),
                        'cache_hits': cache_hits,
                        'total_requisicoes': total_requisicoes
                    },
                    severidade='media',
                    sugestao_otimizacao=(
                        f"Taxa de cache: {cache_rate:.1f}%. "
                        "Considere usar prompt caching em contextos repetidos."
                    )
                ))

        return gargalos

    def identificar_padroes_uso(self, limite_eventos: int = 1000) -> Dict[str, Any]:
        """
        Identifica padrões de uso das ferramentas.

        Returns:
            Dict com:
            - ferramentas_mais_usadas: Top 10 ferramentas
            - ferramentas_mais_lentas: Top 5 mais lentas
            - horarios_pico: Distribuição por hora do dia
            - tendencias: Mudanças ao longo do tempo
        """
        eventos = self.carregar_eventos_ferramentas(limite_eventos)

        if not eventos:
            return {}

        # 1. Ferramentas mais usadas
        contador_uso = Counter(e['ferramenta'] for e in eventos)
        ferramentas_mais_usadas = [
            {'ferramenta': f, 'usos': count}
            for f, count in contador_uso.most_common(10)
        ]

        # 2. Ferramentas mais lentas
        tempos_por_ferramenta = defaultdict(list)
        for evento in eventos:
            tempos_por_ferramenta[evento['ferramenta']].append(evento['tempo_execucao'])

        ferramentas_tempo_medio = [
            {'ferramenta': f, 'tempo_medio': round(statistics.mean(tempos), 2)}
            for f, tempos in tempos_por_ferramenta.items()
        ]
        ferramentas_mais_lentas = sorted(
            ferramentas_tempo_medio,
            key=lambda x: x['tempo_medio'],
            reverse=True
        )[:5]

        # 3. Distribuição por hora (se houver timestamps)
        horarios = defaultdict(int)
        for evento in eventos:
            try:
                dt = datetime.fromisoformat(evento['timestamp'])
                horarios[dt.hour] += 1
            except (ValueError, KeyError):
                pass

        horarios_pico = dict(sorted(horarios.items(), key=lambda x: x[1], reverse=True)[:5])

        return {
            'ferramentas_mais_usadas': ferramentas_mais_usadas,
            'ferramentas_mais_lentas': ferramentas_mais_lentas,
            'horarios_pico': horarios_pico,
            'total_eventos_analisados': len(eventos)
        }

    def sugerir_otimizacoes(self) -> List[Sugestao]:
        """
        Gera sugestões de otimização baseadas nos dados.

        Returns:
            Lista de sugestões priorizadas
        """
        sugestoes = []

        # Analisar gargalos
        gargalos = self.detectar_gargalos()

        # Sugestões baseadas em gargalos
        for gargalo in gargalos:
            if gargalo.tipo == 'ferramenta_lenta':
                ferramenta = gargalo.descricao.split("'")[1]
                tempo_medio = gargalo.metricas['tempo_medio']

                sugestoes.append(Sugestao(
                    titulo=f"Otimizar ferramenta '{ferramenta}'",
                    descricao=(
                        f"A ferramenta '{ferramenta}' tem tempo médio de {tempo_medio:.1f}s. "
                        "Isso pode impactar a experiência do usuário."
                    ),
                    impacto_estimado='alto' if tempo_medio > 15 else 'medio',
                    facilidade_implementacao='moderada',
                    codigo_exemplo=(
                        f"# Considere implementar cache para '{ferramenta}'\n"
                        "# ou executar operações pesadas em paralelo\n"
                        "import asyncio\n\n"
                        f"async def {ferramenta}_otimizado():\n"
                        "    # Implementação otimizada\n"
                        "    pass"
                    )
                ))

            elif gargalo.tipo == 'cache_baixo':
                taxa = gargalo.metricas['taxa_cache_hit']

                sugestoes.append(Sugestao(
                    titulo="Aumentar uso de Prompt Caching",
                    descricao=(
                        f"Taxa de cache hit atual: {taxa:.1f}%. "
                        "Usar prompt caching pode economizar tokens e reduzir latência."
                    ),
                    impacto_estimado='alto',
                    facilidade_implementacao='facil',
                    codigo_exemplo=(
                        "# Marcar blocos de sistema para cache\n"
                        "system=[\n"
                        "    {\n"
                        '        "type": "text",\n'
                        '        "text": "Contexto grande...",\n'
                        '        "cache_control": {"type": "ephemeral"}\n'
                        "    }\n"
                        "]"
                    )
                ))

            elif gargalo.tipo == 'erro_frequente':
                ferramenta = gargalo.descricao.split("'")[1]
                taxa_erro = gargalo.metricas['taxa_erro']

                sugestoes.append(Sugestao(
                    titulo=f"Corrigir erros em '{ferramenta}'",
                    descricao=(
                        f"Taxa de erro de {taxa_erro:.1f}% é muito alta. "
                        "Revisar validações e tratamento de erros."
                    ),
                    impacto_estimado='alto',
                    facilidade_implementacao='moderada',
                    codigo_exemplo=(
                        f"# Adicionar validação robusta em '{ferramenta}'\n"
                        "def validar_parametros(params):\n"
                        "    # Validações\n"
                        "    if not params.get('campo_obrigatorio'):\n"
                        "        raise ValueError('Campo obrigatório ausente')\n"
                        "    return True"
                    )
                ))

        # Sugestões baseadas em padrões de uso
        padroes = self.identificar_padroes_uso()

        if padroes and padroes.get('ferramentas_mais_usadas'):
            top_ferramenta = padroes['ferramentas_mais_usadas'][0]

            sugestoes.append(Sugestao(
                titulo=f"Otimizar '{top_ferramenta['ferramenta']}' (mais usada)",
                descricao=(
                    f"Ferramenta mais usada ({top_ferramenta['usos']} vezes). "
                    "Qualquer otimização terá grande impacto."
                ),
                impacto_estimado='alto',
                facilidade_implementacao='moderada'
            ))

        # Priorizar sugestões (alto impacto + fácil primeiro)
        prioridade = {
            ('alto', 'facil'): 1,
            ('alto', 'moderada'): 2,
            ('medio', 'facil'): 3,
            ('alto', 'dificil'): 4,
            ('medio', 'moderada'): 5,
            ('baixo', 'facil'): 6,
            ('medio', 'dificil'): 7,
            ('baixo', 'moderada'): 8,
            ('baixo', 'dificil'): 9
        }

        sugestoes.sort(
            key=lambda s: prioridade.get((s.impacto_estimado, s.facilidade_implementacao), 10)
        )

        return sugestoes

    def detectar_regressoes(self, janela_antiga: int = 100, janela_nova: int = 100) -> List[Dict]:
        """
        Detecta regressões de performance comparando períodos.

        Args:
            janela_antiga: Número de eventos do período antigo
            janela_nova: Número de eventos do período recente

        Returns:
            Lista de regressões detectadas
        """
        eventos = self.carregar_eventos_ferramentas()

        if len(eventos) < janela_antiga + janela_nova:
            return []

        # Separar em duas janelas
        eventos_antigos = eventos[-(janela_antiga + janela_nova):-janela_nova]
        eventos_novos = eventos[-janela_nova:]

        regressoes = []

        # Comparar tempo médio por ferramenta
        tempos_antigos = defaultdict(list)
        tempos_novos = defaultdict(list)

        for e in eventos_antigos:
            tempos_antigos[e['ferramenta']].append(e['tempo_execucao'])

        for e in eventos_novos:
            tempos_novos[e['ferramenta']].append(e['tempo_execucao'])

        for ferramenta in tempos_novos.keys():
            if ferramenta not in tempos_antigos:
                continue

            tempo_antigo = statistics.mean(tempos_antigos[ferramenta])
            tempo_novo = statistics.mean(tempos_novos[ferramenta])

            # Se aumentou mais de 50%
            if tempo_novo > tempo_antigo * 1.5:
                aumento_pct = ((tempo_novo - tempo_antigo) / tempo_antigo * 100)

                regressoes.append({
                    'ferramenta': ferramenta,
                    'tempo_antigo': round(tempo_antigo, 2),
                    'tempo_novo': round(tempo_novo, 2),
                    'aumento_percentual': round(aumento_pct, 1),
                    'severidade': 'alta' if aumento_pct > 100 else 'media'
                })

        return regressoes

    def gerar_relatorio_completo(self) -> str:
        """Gera relatório completo de análise formatado"""
        linhas = []

        linhas.append("=" * 80)
        linhas.append("📊 RELATÓRIO DE ANÁLISE DE TELEMETRIA - LUNA V3")
        linhas.append("=" * 80)
        linhas.append(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        linhas.append("")

        # 1. Gargalos
        gargalos = self.detectar_gargalos()

        if gargalos:
            linhas.append("🚨 GARGALOS IDENTIFICADOS")
            linhas.append("-" * 80)

            for g in gargalos:
                icone = {
                    'critica': '🔴',
                    'alta': '🟠',
                    'media': '🟡',
                    'baixa': '🟢'
                }.get(g.severidade, '⚪')

                linhas.append(f"\n{icone} {g.descricao} (Severidade: {g.severidade})")
                linhas.append(f"   Tipo: {g.tipo}")
                linhas.append(f"   Métricas: {g.metricas}")
                linhas.append(f"   💡 Sugestão: {g.sugestao_otimizacao}")
        else:
            linhas.append("✅ Nenhum gargalo crítico identificado")

        linhas.append("")

        # 2. Padrões de uso
        padroes = self.identificar_padroes_uso()

        if padroes:
            linhas.append("📈 PADRÕES DE USO")
            linhas.append("-" * 80)

            if padroes.get('ferramentas_mais_usadas'):
                linhas.append("\n🔧 Top 5 Ferramentas Mais Usadas:")
                for i, f in enumerate(padroes['ferramentas_mais_usadas'][:5], 1):
                    linhas.append(f"   {i}. {f['ferramenta']}: {f['usos']} usos")

            if padroes.get('ferramentas_mais_lentas'):
                linhas.append("\n⏱️  Top 5 Ferramentas Mais Lentas:")
                for i, f in enumerate(padroes['ferramentas_mais_lentas'][:5], 1):
                    linhas.append(f"   {i}. {f['ferramenta']}: {f['tempo_medio']:.2f}s médio")

            linhas.append(f"\n📊 Total de eventos analisados: {padroes['total_eventos_analisados']}")

        linhas.append("")

        # 3. Sugestões de otimização
        sugestoes = self.sugerir_otimizacoes()

        if sugestoes:
            linhas.append("💡 SUGESTÕES DE OTIMIZAÇÃO (Priorizadas)")
            linhas.append("-" * 80)

            for i, s in enumerate(sugestoes[:5], 1):
                impacto_icon = {'alto': '🔥', 'medio': '🟡', 'baixo': '🟢'}.get(s.impacto_estimado, '')

                linhas.append(f"\n{i}. {impacto_icon} {s.titulo}")
                linhas.append(f"   {s.descricao}")
                linhas.append(f"   Impacto: {s.impacto_estimado} | Facilidade: {s.facilidade_implementacao}")

                if s.codigo_exemplo:
                    linhas.append(f"\n   Exemplo de código:")
                    for linha_codigo in s.codigo_exemplo.split('\n'):
                        linhas.append(f"   {linha_codigo}")

        linhas.append("")

        # 4. Regressões
        regressoes = self.detectar_regressoes()

        if regressoes:
            linhas.append("⚠️  REGRESSÕES DE PERFORMANCE DETECTADAS")
            linhas.append("-" * 80)

            for r in regressoes:
                linhas.append(f"\n• {r['ferramenta']}")
                linhas.append(f"  Antes: {r['tempo_antigo']:.2f}s → Agora: {r['tempo_novo']:.2f}s")
                linhas.append(f"  Aumento: +{r['aumento_percentual']:.1f}%")
                linhas.append(f"  Severidade: {r['severidade']}")
        else:
            linhas.append("✅ Nenhuma regressão de performance detectada")

        linhas.append("")
        linhas.append("=" * 80)

        return '\n'.join(linhas)


# ============================================================================
# FUNÇÕES UTILITÁRIAS
# ============================================================================

def exibir_metricas_tempo_real(telemetria: TelemetriaManager):
    """Exibe métricas da sessão atual de forma formatada"""
    metricas = telemetria.obter_metricas_sessao()

    if not metricas:
        print("Nenhuma sessao ativa")
        return

    print("\n" + "=" * 60)
    print("METRICAS DA SESSAO ATUAL")
    print("=" * 60)
    print(f"Duracao: {metricas['duracao_sessao']:.1f}s")
    print(f"Requisicoes API: {metricas['total_requisicoes']}")
    print(f"Total de tokens: {metricas['total_tokens']:,}")
    print(f"Taxa de cache hit: {metricas['taxa_cache_hit']:.1f}%")
    print(f"Economia (tokens): {metricas['economia_tokens']:,}")
    print(f"Ferramentas usadas: {metricas['total_ferramentas']}")
    print(f"Erros: {metricas['erros']}")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    # Teste básico do sistema
    print("TESTE: Sistema de Telemetria\n")

    # 1. Criar manager
    telemetria = TelemetriaManager()
    telemetria.iniciar_sessao()

    # 2. Simular alguns eventos
    print("Simulando eventos de teste...")

    telemetria.registrar_uso_ferramenta(
        nome='bash',
        parametros={'comando': 'ls -la'},
        resultado='✅ Comando executado',
        tempo_execucao=0.5,
        tokens_estimados=100
    )

    telemetria.registrar_uso_ferramenta(
        nome='criar_arquivo',
        parametros={'caminho': '/tmp/teste.txt', 'conteudo': 'teste'},
        resultado='✅ Arquivo criado',
        tempo_execucao=0.1,
        tokens_estimados=50
    )

    telemetria.registrar_requisicao_api(
        tokens_input=1000,
        tokens_output=500,
        tokens_cache_read=200,
        tempo_latencia=2.5
    )

    telemetria.registrar_requisicao_api(
        tokens_input=800,
        tokens_output=400,
        tokens_cache_read=0,
        tempo_latencia=3.0
    )

    # 3. Exibir métricas
    exibir_metricas_tempo_real(telemetria)

    # 4. Finalizar sessão
    telemetria.finalizar_sessao()

    # 5. Analisar
    print("\nAnalise de telemetria:")
    analisador = AnalisadorTelemetria()

    # Padrões de uso
    padroes = analisador.identificar_padroes_uso()
    if padroes:
        print(f"\nTotal de eventos analisados: {padroes.get('total_eventos_analisados', 0)}")

        if padroes.get('ferramentas_mais_usadas'):
            print("\nFerramentas mais usadas:")
            for f in padroes['ferramentas_mais_usadas'][:3]:
                print(f"  - {f['ferramenta']}: {f['usos']} usos")

    print("\nSistema de telemetria funcionando!")
    print(f"\nArquivos criados:")
    print(f"  - {telemetria.log_ferramentas}")
    print(f"  - {telemetria.log_api}")
    print(f"  - {telemetria.log_sessoes}")
