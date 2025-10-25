#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚙️ AUTO-TUNING DE PARÂMETROS - Luna V3

Sistema que ajusta automaticamente parâmetros com base em histórico de performance.

Features:
- Ajuste automático de thresholds
- Análise de tendências
- Identificação de valores ótimos
- Modos de operação: manual, automático, agressivo

Uso:
    tuner = ParameterTuner(agente)
    tuner.analisar_historico()
    tuner.sugerir_ajustes()
    tuner.aplicar_ajustes(modo='manual')  # ou 'automatico', 'agressivo'

Criado: 2025-10-23
Parte das Melhorias Adicionais - Nível 1 (1.2)
"""

import sys, os
if sys.platform == 'win32':
    os.environ['PYTHONUTF8'] = '1'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except: pass

from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import json
import statistics


class ParameterTuner:
    """
    Auto-tuning de parâmetros do Luna V3.

    Ajusta automaticamente:
    - quality_threshold (default: 90 → 85-95)
    - batch_threshold (default: 50 → 30-100)
    - stagnation_limit (default: 5 → 3-10)
    - timeout_iteracao_segundos (default: 120 → 60-300)
    """

    # Ranges seguros para parâmetros
    PARAM_RANGES = {
        "quality_threshold": (75, 95),  # Min, Max
        "batch_threshold": (20, 150),
        "stagnation_limit": (2, 15),
        "timeout_iteracao_segundos": (60, 600),
        "max_iteracoes": (10, 50),
    }

    # Valores padrão
    DEFAULTS = {
        "quality_threshold": 90,
        "batch_threshold": 50,
        "stagnation_limit": 5,
        "timeout_iteracao_segundos": 120,
        "max_iteracoes": 20,
    }

    def __init__(self, history_file: str = "tuner_history.json"):
        """
        Inicializa o Parameter Tuner.

        Args:
            history_file: Arquivo JSON com histórico de performance
        """
        self.history_file = Path(history_file)
        self.history: List[Dict[str, Any]] = []
        self.recommendations: Dict[str, Dict[str, Any]] = {}

        self._carregar_historico()

    def _carregar_historico(self):
        """Carrega histórico de execuções anteriores."""
        if self.history_file.exists():
            try:
                self.history = json.loads(self.history_file.read_text(encoding='utf-8'))
                print(f"📊 {len(self.history)} execução(ões) carregada(s) do histórico")
            except Exception as e:
                print(f"⚠️ Erro ao carregar histórico: {e}")
                self.history = []
        else:
            self.history = []

    def salvar_execucao(
        self,
        parametros: Dict[str, Any],
        metricas: Dict[str, Any]
    ):
        """
        Salva uma execução no histórico.

        Args:
            parametros: Parâmetros usados na execução
            metricas: Métricas coletadas (tokens, tempo, qualidade, etc)
        """
        execucao = {
            "timestamp": datetime.now().isoformat(),
            "parametros": parametros,
            "metricas": metricas
        }

        self.history.append(execucao)

        # Salvar no arquivo
        try:
            self.history_file.write_text(
                json.dumps(self.history, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
        except Exception as e:
            print(f"⚠️ Erro ao salvar histórico: {e}")

    def analisar_historico(self, ultimas_n: int = 10) -> Dict[str, Any]:
        """
        Analisa as últimas N execuções.

        Args:
            ultimas_n: Número de execuções recentes a analisar

        Returns:
            Dicionário com estatísticas agregadas
        """
        if not self.history:
            return {"erro": "Nenhum histórico disponível"}

        # Pegar últimas N execuções
        execucoes_recentes = self.history[-ultimas_n:]

        analise = {
            "total_execucoes": len(execucoes_recentes),
            "periodo": {
                "inicio": execucoes_recentes[0]["timestamp"],
                "fim": execucoes_recentes[-1]["timestamp"]
            },
            "metricas": {}
        }

        # Agregar métricas
        for metrica in ["quality_score", "tokens_usados", "tempo_total", "num_iteracoes"]:
            valores = []
            for exec in execucoes_recentes:
                if metrica in exec["metricas"]:
                    valores.append(exec["metricas"][metrica])

            if valores:
                analise["metricas"][metrica] = {
                    "media": statistics.mean(valores),
                    "mediana": statistics.median(valores),
                    "min": min(valores),
                    "max": max(valores),
                    "desvio_padrao": statistics.stdev(valores) if len(valores) > 1 else 0
                }

        # Parâmetros mais comuns
        analise["parametros_mais_usados"] = self._parametros_mais_usados(execucoes_recentes)

        return analise

    def _parametros_mais_usados(self, execucoes: List[Dict]) -> Dict[str, Any]:
        """Identifica os parâmetros mais usados."""
        contadores = {}

        for exec in execucoes:
            for param, valor in exec["parametros"].items():
                if param not in contadores:
                    contadores[param] = {}

                if valor not in contadores[param]:
                    contadores[param][valor] = 0

                contadores[param][valor] += 1

        # Valor mais comum para cada parâmetro
        mais_usados = {}
        for param, valores in contadores.items():
            mais_usados[param] = max(valores, key=valores.get)

        return mais_usados

    def sugerir_ajustes(self, modo: str = "conservador") -> Dict[str, Dict[str, Any]]:
        """
        Sugere ajustes de parâmetros baseado no histórico.

        Args:
            modo: 'conservador', 'moderado', ou 'agressivo'

        Returns:
            Dicionário com sugestões de ajuste
        """
        if len(self.history) < 3:
            return {"erro": "Histórico insuficiente (mínimo 3 execuções)"}

        analise = self.analisar_historico()
        sugestoes = {}

        # 1. Quality Threshold
        if "quality_score" in analise["metricas"]:
            quality_stats = analise["metricas"]["quality_score"]
            sugestoes["quality_threshold"] = self._sugerir_quality_threshold(
                quality_stats, modo
            )

        # 2. Batch Threshold
        if "num_iteracoes" in analise["metricas"]:
            iter_stats = analise["metricas"]["num_iteracoes"]
            sugestoes["batch_threshold"] = self._sugerir_batch_threshold(
                iter_stats, modo
            )

        # 3. Timeout
        if "tempo_total" in analise["metricas"]:
            tempo_stats = analise["metricas"]["tempo_total"]
            sugestoes["timeout_iteracao_segundos"] = self._sugerir_timeout(
                tempo_stats, modo
            )

        self.recommendations = sugestoes
        return sugestoes

    def _sugerir_quality_threshold(self, stats: Dict, modo: str) -> Dict[str, Any]:
        """Sugere ajuste no quality threshold."""
        media = stats["media"]
        mediana = stats["mediana"]

        # Se qualidade média está alta, podemos reduzir threshold
        if media >= 88 and mediana >= 87:
            if modo == "agressivo":
                novo_valor = 85
            elif modo == "moderado":
                novo_valor = 87
            else:  # conservador
                novo_valor = 88

            return {
                "valor_atual": self.DEFAULTS["quality_threshold"],
                "valor_sugerido": novo_valor,
                "motivo": f"Qualidade média alta ({media:.1f}). Podemos reduzir threshold.",
                "ganho_esperado": "10-15% menos iterações"
            }

        # Se qualidade está baixa, aumentar threshold
        elif media < 85:
            return {
                "valor_atual": self.DEFAULTS["quality_threshold"],
                "valor_sugerido": 92,
                "motivo": f"Qualidade média baixa ({media:.1f}). Aumentar exigência.",
                "ganho_esperado": "Melhor qualidade das respostas"
            }

        return None  # Sem sugestão

    def _sugerir_batch_threshold(self, stats: Dict, modo: str) -> Optional[Dict[str, Any]]:
        """Sugere ajuste no batch threshold."""
        media_iter = stats["media"]

        # Se tarefas são frequentemente pequenas, reduzir threshold
        if media_iter < 8:
            if modo == "agressivo":
                novo_valor = 30
            elif modo == "moderado":
                novo_valor = 40
            else:
                novo_valor = 45

            return {
                "valor_atual": self.DEFAULTS["batch_threshold"],
                "valor_sugerido": novo_valor,
                "motivo": f"Tarefas pequenas (média {media_iter:.1f} iterações). Batch pode processar menos.",
                "ganho_esperado": "20-30% mais tarefas usando batch"
            }

        # Se tarefas são muito grandes, aumentar threshold
        elif media_iter > 15:
            return {
                "valor_atual": self.DEFAULTS["batch_threshold"],
                "valor_sugerido": 70,
                "motivo": f"Tarefas grandes (média {media_iter:.1f} iterações). Aumentar threshold.",
                "ganho_esperado": "Menos overhead, melhor qualidade"
            }

        return None

    def _sugerir_timeout(self, stats: Dict, modo: str) -> Optional[Dict[str, Any]]:
        """Sugere ajuste no timeout de iteração."""
        media_tempo = stats["media"]
        max_tempo = stats["max"]

        # Se execuções são rápidas, podemos reduzir timeout
        if media_tempo < 60 and max_tempo < 100:
            return {
                "valor_atual": self.DEFAULTS["timeout_iteracao_segundos"],
                "valor_sugerido": 90,
                "motivo": f"Iterações rápidas (média {media_tempo:.1f}s). Timeout pode ser menor.",
                "ganho_esperado": "Detecção mais rápida de travamentos"
            }

        # Se execuções são lentas, aumentar timeout
        elif media_tempo > 80:
            return {
                "valor_atual": self.DEFAULTS["timeout_iteracao_segundos"],
                "valor_sugerido": 180,
                "motivo": f"Iterações lentas (média {media_tempo:.1f}s). Aumentar timeout.",
                "ganho_esperado": "Menos falsos positivos de timeout"
            }

        return None

    def exibir_recomendacoes(self):
        """Exibe recomendações formatadas."""
        if not self.recommendations:
            print("📊 Nenhuma recomendação disponível. Execute sugerir_ajustes() primeiro.")
            return

        print("\n" + "="*70)
        print("📊 AUTO-TUNING RECOMENDAÇÕES")
        print("="*70)

        for param, sugestao in self.recommendations.items():
            if sugestao:
                print(f"\n{param}:")
                print(f"   Atual: {sugestao['valor_atual']}")
                print(f"   Sugerido: {sugestao['valor_sugerido']}")
                print(f"   Motivo: {sugestao['motivo']}")
                print(f"   Ganho esperado: {sugestao['ganho_esperado']}")

        print("\n" + "="*70)

    def aplicar_ajustes(
        self,
        agente,
        modo: str = "manual",
        auto_confirmar: bool = False
    ) -> Dict[str, Any]:
        """
        Aplica ajustes ao agente.

        Args:
            agente: Instância do AgenteCompletoV3
            modo: 'manual', 'automatico', ou 'agressivo'
            auto_confirmar: Se True, aplica sem pedir confirmação (modo automático)

        Returns:
            Dicionário com parâmetros aplicados
        """
        if not self.recommendations:
            self.sugerir_ajustes(modo=modo)

        if not self.recommendations:
            print("⚠️ Nenhuma sugestão de ajuste disponível")
            return {}

        self.exibir_recomendacoes()

        # Pedir confirmação (se não for auto)
        if not auto_confirmar and modo != "automatico":
            resposta = input("\n💬 Aplicar ajustes? [S/n]: ").strip().lower()
            if resposta == 'n':
                print("⏹️ Ajustes cancelados")
                return {}

        # Aplicar ajustes
        aplicados = {}
        for param, sugestao in self.recommendations.items():
            if sugestao and hasattr(agente, param):
                valor_antigo = getattr(agente, param)
                setattr(agente, param, sugestao['valor_sugerido'])
                aplicados[param] = {
                    "antigo": valor_antigo,
                    "novo": sugestao['valor_sugerido']
                }
                print(f"✅ {param}: {valor_antigo} → {sugestao['valor_sugerido']}")

        return aplicados


# ===== TESTES =====
if __name__ == "__main__":
    print("🧪 Testando ParameterTuner...")

    # Criar tuner
    tuner = ParameterTuner("tuner_history_test.json")

    # Simular algumas execuções
    for i in range(5):
        tuner.salvar_execucao(
            parametros={
                "quality_threshold": 90,
                "batch_threshold": 50,
                "timeout_iteracao_segundos": 120
            },
            metricas={
                "quality_score": 88 + i,
                "tokens_usados": 3000 + i*100,
                "tempo_total": 45 + i*5,
                "num_iteracoes": 6 + i
            }
        )

    # Analisar
    print("\n📊 Análise do histórico:")
    analise = tuner.analisar_historico()
    print(json.dumps(analise, indent=2, ensure_ascii=False))

    # Sugerir ajustes
    print("\n⚙️ Sugestões de ajuste:")
    sugestoes = tuner.sugerir_ajustes(modo="moderado")
    tuner.exibir_recomendacoes()

    print("\n✅ Testes concluídos!")
