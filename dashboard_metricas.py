#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 DASHBOARD DE MÉTRICAS - Luna V3

Sistema de visualização de métricas em tempo real durante execução.

Features:
- Cache hit rate e economia de tokens
- Quality scores com tendência
- Batch processing stats
- Auto-melhorias aplicadas
- Token usage e custo

Uso:
    dashboard = MetricsDashboard(agente)
    dashboard.atualizar()
    dashboard.exibir()

Criado: 2025-10-20
Parte das Melhorias Adicionais - Nível 1
"""

import time
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import json

# Tentar importar Rich (opcional)
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.live import Live
    from rich.progress import Progress, BarColumn, TextColumn
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class MetricsDashboard:
    """
    Dashboard de métricas em tempo real para Luna V3.

    Exibe:
    - Cache hit rate (atualizado a cada request)
    - Quality scores (gráfico de tendência)
    - Batch processing stats
    - Auto-melhorias aplicadas
    - Token usage e economia

    Modos de exibição:
    - rich: Dashboard interativo (requer pip install rich)
    - simple: Output simples em texto
    - silent: Apenas coleta dados (sem exibição)
    """

    def __init__(self, agente=None, modo: str = "auto"):
        """
        Inicializa o dashboard.

        Args:
            agente: Instância do AgenteCompletoV3 (opcional)
            modo: "rich", "simple", "silent" ou "auto" (detecta Rich)
        """
        self.agente = agente

        # Detectar modo
        if modo == "auto":
            self.modo = "rich" if RICH_AVAILABLE else "simple"
        else:
            self.modo = modo

        # Console Rich (se disponível)
        self.console = Console() if RICH_AVAILABLE else None

        # Métricas coletadas
        self.metricas = {
            'cache': {
                'total_requests': 0,
                'cache_hits': 0,
                'cache_misses': 0,
                'tokens_economizados': 0,
                'custo_economizado_usd': 0.0
            },
            'quality': {
                'scores': [],
                'current_score': 0.0,
                'best_score': 0.0,
                'avg_score': 0.0
            },
            'batch': {
                'total_batches': 0,
                'total_requests': 0,
                'avg_speedup': 0.0
            },
            'auto_improve': {
                'melhorias_detectadas': 0,
                'melhorias_aplicadas': 0,
                'taxa_sucesso': 0.0
            },
            'tokens': {
                'total_input': 0,
                'total_output': 0,
                'custo_total_usd': 0.0
            },
            'tempo': {
                'inicio': datetime.now(),
                'duracao_segundos': 0
            }
        }

        # Histórico para export
        self.historico = []

    def atualizar_do_agente(self):
        """
        Atualiza métricas diretamente do agente.
        """
        if not self.agente:
            return

        # Atualizar cache
        if hasattr(self.agente, 'cache_manager') and self.agente.cache_manager:
            cache_stats = self.agente.cache_manager.obter_estatisticas()
            self.metricas['cache'].update({
                'total_requests': cache_stats['total_requests'],
                'cache_hits': cache_stats['requests_with_hits'],
                'cache_misses': cache_stats['requests_with_misses'],
                'tokens_economizados': cache_stats['tokens_economizados'],
                'custo_economizado_usd': cache_stats['custo_economizado_usd']
            })

        # Atualizar quality
        if hasattr(self.agente, 'quality_scores') and self.agente.quality_scores:
            scores = self.agente.quality_scores
            self.metricas['quality'].update({
                'scores': scores,
                'current_score': scores[-1] if scores else 0.0,
                'best_score': max(scores) if scores else 0.0,
                'avg_score': sum(scores) / len(scores) if scores else 0.0
            })

        # Atualizar batch
        if hasattr(self.agente, 'batch_processor') and self.agente.batch_processor:
            batch_stats = self.agente.batch_processor.obter_estatisticas()
            self.metricas['batch'].update(batch_stats)

        # Atualizar tempo
        self.metricas['tempo']['duracao_segundos'] = (
            datetime.now() - self.metricas['tempo']['inicio']
        ).total_seconds()

    def atualizar_manual(self, categoria: str, dados: Dict[str, Any]):
        """
        Atualiza métricas manualmente.

        Args:
            categoria: 'cache', 'quality', 'batch', 'auto_improve', 'tokens'
            dados: Dict com novos valores
        """
        if categoria in self.metricas:
            self.metricas[categoria].update(dados)

    def exibir(self, limpar_tela: bool = False):
        """
        Exibe o dashboard.

        Args:
            limpar_tela: Se deve limpar a tela antes de exibir
        """
        if self.modo == "silent":
            return

        # Atualizar do agente se disponível
        self.atualizar_do_agente()

        if self.modo == "rich" and RICH_AVAILABLE:
            self._exibir_rich(limpar_tela)
        else:
            self._exibir_simple()

    def _exibir_rich(self, limpar_tela: bool = False):
        """Exibe dashboard usando Rich."""
        if limpar_tela:
            self.console.clear()

        # Criar tabela de métricas
        table = Table(title="📊 Luna V3 - Dashboard de Métricas", show_header=True)
        table.add_column("Categoria", style="cyan", width=15)
        table.add_column("Métrica", style="white", width=30)
        table.add_column("Valor", style="green", width=20)

        # Cache
        cache = self.metricas['cache']
        if cache['total_requests'] > 0:
            hit_rate = (cache['cache_hits'] / cache['total_requests']) * 100
            table.add_row(
                "💎 CACHE",
                "Hit Rate",
                f"{hit_rate:.1f}% ({cache['cache_hits']}/{cache['total_requests']})"
            )
            table.add_row(
                "",
                "Tokens Economizados",
                f"{cache['tokens_economizados']:,}"
            )
            table.add_row(
                "",
                "Economia USD",
                f"${cache['custo_economizado_usd']:.4f}"
            )

        # Quality
        quality = self.metricas['quality']
        if quality['current_score'] > 0:
            table.add_row(
                "✨ QUALITY",
                "Score Atual",
                f"{quality['current_score']:.1f}/100"
            )
            if len(quality['scores']) > 1:
                trend = quality['scores'][-1] - quality['scores'][-2]
                trend_symbol = "↗" if trend > 0 else "↘" if trend < 0 else "→"
                table.add_row(
                    "",
                    "Tendência",
                    f"{trend_symbol} {abs(trend):.1f} pontos"
                )

        # Batch
        batch = self.metricas['batch']
        if batch['total_batches'] > 0:
            table.add_row(
                "🚀 BATCH",
                "Total Batches",
                f"{batch['total_batches']}"
            )
            table.add_row(
                "",
                "Total Requests",
                f"{batch['total_requests']}"
            )
            if batch['avg_speedup'] > 0:
                table.add_row(
                    "",
                    "Speedup Médio",
                    f"{batch['avg_speedup']:.1f}x"
                )

        # Auto-Improve
        auto = self.metricas['auto_improve']
        if auto['melhorias_detectadas'] > 0:
            table.add_row(
                "🔧 AUTO-IMPROVE",
                "Melhorias Detectadas",
                f"{auto['melhorias_detectadas']}"
            )
            table.add_row(
                "",
                "Melhorias Aplicadas",
                f"{auto['melhorias_aplicadas']}"
            )
            if auto['melhorias_detectadas'] > 0:
                taxa = (auto['melhorias_aplicadas'] / auto['melhorias_detectadas']) * 100
                table.add_row(
                    "",
                    "Taxa de Sucesso",
                    f"{taxa:.0f}%"
                )

        # Tempo
        tempo = self.metricas['tempo']
        duracao_min = tempo['duracao_segundos'] / 60
        table.add_row(
            "⏱️  TEMPO",
            "Duração",
            f"{duracao_min:.1f} minutos"
        )

        # Exibir
        self.console.print(table)

    def _exibir_simple(self):
        """Exibe dashboard simples em texto."""
        print("\n" + "="*70)
        print("📊 LUNA V3 - DASHBOARD DE MÉTRICAS")
        print("="*70)

        # Cache
        cache = self.metricas['cache']
        if cache['total_requests'] > 0:
            hit_rate = (cache['cache_hits'] / cache['total_requests']) * 100
            print(f"\n💎 CACHE:")
            print(f"   Hit Rate: {hit_rate:.1f}% ({cache['cache_hits']}/{cache['total_requests']})")
            print(f"   Economia: {cache['tokens_economizados']:,} tokens (${cache['custo_economizado_usd']:.4f})")

        # Quality
        quality = self.metricas['quality']
        if quality['current_score'] > 0:
            print(f"\n✨ QUALITY:")
            print(f"   Current: {quality['current_score']:.1f}/100")
            if len(quality['scores']) > 1:
                trend = quality['scores'][-1] - quality['scores'][-2]
                trend_symbol = "↗" if trend > 0 else "↘" if trend < 0 else "→"
                print(f"   Trend: {trend_symbol} {abs(trend):.1f} pontos")

        # Batch
        batch = self.metricas['batch']
        if batch['total_batches'] > 0:
            print(f"\n🚀 BATCH:")
            print(f"   Batches: {batch['total_batches']}")
            print(f"   Requests: {batch['total_requests']}")

        # Auto-Improve
        auto = self.metricas['auto_improve']
        if auto['melhorias_detectadas'] > 0:
            print(f"\n🔧 AUTO-IMPROVE:")
            print(f"   Detectadas: {auto['melhorias_detectadas']}")
            print(f"   Aplicadas: {auto['melhorias_aplicadas']}")

        # Tempo
        tempo = self.metricas['tempo']
        duracao_min = tempo['duracao_segundos'] / 60
        print(f"\n⏱️  TEMPO: {duracao_min:.1f} minutos")

        print("\n" + "="*70)

    def salvar_historico(self, caminho: str = "dashboard_historico.json"):
        """
        Salva histórico de métricas em JSON.

        Args:
            caminho: Caminho do arquivo JSON
        """
        # Adicionar snapshot atual ao histórico
        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'metricas': self.metricas.copy()
        }
        self.historico.append(snapshot)

        # Salvar
        try:
            with open(caminho, 'w', encoding='utf-8') as f:
                json.dump(self.historico, f, indent=2, default=str)
            return True
        except Exception as e:
            print(f"⚠️  Erro ao salvar histórico: {e}")
            return False

    def obter_metricas(self) -> Dict[str, Any]:
        """
        Retorna todas as métricas coletadas.

        Returns:
            Dict com todas as métricas
        """
        self.atualizar_do_agente()
        return self.metricas.copy()

    def reset(self):
        """Reseta todas as métricas."""
        self.metricas = {
            'cache': {
                'total_requests': 0,
                'cache_hits': 0,
                'cache_misses': 0,
                'tokens_economizados': 0,
                'custo_economizado_usd': 0.0
            },
            'quality': {
                'scores': [],
                'current_score': 0.0,
                'best_score': 0.0,
                'avg_score': 0.0
            },
            'batch': {
                'total_batches': 0,
                'total_requests': 0,
                'avg_speedup': 0.0
            },
            'auto_improve': {
                'melhorias_detectadas': 0,
                'melhorias_aplicadas': 0,
                'taxa_sucesso': 0.0
            },
            'tokens': {
                'total_input': 0,
                'total_output': 0,
                'custo_total_usd': 0.0
            },
            'tempo': {
                'inicio': datetime.now(),
                'duracao_segundos': 0
            }
        }
        self.historico = []


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("📊 Testando Dashboard de Métricas\n")

    # Criar dashboard
    dashboard = MetricsDashboard(modo="simple")

    # Simular métricas
    dashboard.atualizar_manual('cache', {
        'total_requests': 10,
        'cache_hits': 8,
        'cache_misses': 2,
        'tokens_economizados': 4500,
        'custo_economizado_usd': 0.12
    })

    dashboard.atualizar_manual('quality', {
        'scores': [75.0, 78.0, 82.0, 85.0],
        'current_score': 85.0,
        'best_score': 85.0,
        'avg_score': 80.0
    })

    dashboard.atualizar_manual('batch', {
        'total_batches': 3,
        'total_requests': 150,
        'avg_speedup': 62.0
    })

    dashboard.atualizar_manual('auto_improve', {
        'melhorias_detectadas': 5,
        'melhorias_aplicadas': 4,
        'taxa_sucesso': 80.0
    })

    # Exibir
    dashboard.exibir()

    # Salvar histórico
    print("\n💾 Salvando histórico...")
    if dashboard.salvar_historico():
        print("✅ Histórico salvo em dashboard_historico.json")

    print("\n✅ Teste concluído!")
