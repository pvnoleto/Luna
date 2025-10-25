#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 AUTO-TUNING DE PARÂMETROS - Luna V3

Ajusta automaticamente parâmetros do sistema com base em histórico de performance.

Parâmetros ajustáveis:
- quality_threshold (90 → 85-95)
- batch_threshold (50 → 30-100)
- stagnation_limit (5 → 3-10)

Modos:
- manual: Sugere, usuário aprova
- automático: Ajusta dentro de ranges seguros
- agressivo: Explora ranges mais amplos

Criado: 2025-10-20
Melhoria Adicional 1.2 - Nível 1
"""

import sys
import os

# ============================================================================
# CONFIGURAÇÃO UTF-8 (Windows)
# ============================================================================
if sys.platform == 'win32':
    os.environ['PYTHONUTF8'] = '1'
    os.environ['PYTHONIOENCODING'] = 'utf-8'

    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from statistics import mean, median


class ParameterTuner:
    """
    Sistema de auto-tuning de parâmetros baseado em histórico.

    Aprende com execuções anteriores e sugere ajustes otimizados.
    """

    def __init__(self, agente=None, modo: str = "manual", historico_file: str = "tuner_history.json"):
        """
        Args:
            agente: Instância do AgenteCompletoV3
            modo: "manual", "automatico" ou "agressivo"
            historico_file: Arquivo para salvar histórico
        """
        self.agente = agente
        self.modo = modo
        self.historico_file = historico_file
        self.historico = self._carregar_historico()

        # Ranges seguros por parâmetro
        self.ranges = {
            'quality_threshold': {'min': 85, 'max': 95, 'default': 90},
            'batch_threshold': {'min': 30, 'max': 100, 'default': 50},
            'stagnation_limit': {'min': 3, 'max': 10, 'default': 5}
        }

        # Ajustes sugeridos
        self.ajustes_sugeridos = []

    def _carregar_historico(self) -> List[Dict]:
        """Carrega histórico de execuções."""
        try:
            if Path(self.historico_file).exists():
                with open(self.historico_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return []

    def _salvar_historico(self):
        """Salva histórico."""
        try:
            with open(self.historico_file, 'w', encoding='utf-8') as f:
                json.dump(self.historico, f, indent=2, default=str)
        except Exception as e:
            print(f"⚠️  Erro ao salvar histórico: {e}")

    def registrar_execucao(self, metricas: Dict[str, Any]):
        """
        Registra métricas de uma execução.

        Args:
            metricas: Dict com:
                - quality_threshold (usado)
                - quality_scores (lista)
                - batch_threshold (usado)
                - batches_usados (count)
                - stagnation_limit (usado)
                - estagnacoes (count)
        """
        execucao = {
            'timestamp': datetime.now().isoformat(),
            'params': {
                'quality_threshold': metricas.get('quality_threshold', 90),
                'batch_threshold': metricas.get('batch_threshold', 50),
                'stagnation_limit': metricas.get('stagnation_limit', 5)
            },
            'resultados': {
                'quality_scores': metricas.get('quality_scores', []),
                'avg_quality': mean(metricas.get('quality_scores', [90])),
                'batches_usados': metricas.get('batches_usados', 0),
                'estagnacoes': metricas.get('estagnacoes', 0)
            }
        }

        self.historico.append(execucao)
        self._salvar_historico()

    def analisar_e_sugerir(self) -> List[Dict]:
        """
        Analisa histórico e sugere ajustes.

        Returns:
            Lista de dicts com sugestões
        """
        if len(self.historico) < 5:
            return [{
                'tipo': 'info',
                'mensagem': f'Colete mais dados ({len(self.historico)}/5 execuções)'
            }]

        self.ajustes_sugeridos = []

        # Analisar quality_threshold
        self._analisar_quality_threshold()

        # Analisar batch_threshold
        self._analisar_batch_threshold()

        # Analisar stagnation_limit
        self._analisar_stagnation_limit()

        return self.ajustes_sugeridos

    def _analisar_quality_threshold(self):
        """Analisa e sugere ajuste de quality_threshold."""
        # Pegar últimas 10 execuções
        recent = self.historico[-10:]

        # Contar quantas vezes atingiu o threshold
        atingiu = 0
        quase_atingiu = 0  # 85-89 (se threshold é 90)

        for exec in recent:
            threshold = exec['params']['quality_threshold']
            scores = exec['resultados']['quality_scores']

            if scores:
                max_score = max(scores)
                if max_score >= threshold:
                    atingiu += 1
                elif max_score >= threshold - 5:
                    quase_atingiu += 1

        # Se muitos "quase atingiu", diminuir threshold
        if quase_atingiu >= 5 and atingiu < 3:
            novo_threshold = 85
            ganho_esperado = f"+{quase_atingiu*15}% economia de iterações"

            self.ajustes_sugeridos.append({
                'parametro': 'quality_threshold',
                'valor_atual': 90,
                'valor_sugerido': novo_threshold,
                'motivo': f'{quase_atingiu} tarefas atingem 85-89 e param',
                'ganho_esperado': ganho_esperado,
                'confianca': 'alta'
            })

    def _analisar_batch_threshold(self):
        """Analisa e sugere ajuste de batch_threshold."""
        recent = self.historico[-10:]

        # Contar quantos batches foram usados
        batches_usados = sum(e['resultados']['batches_usados'] for e in recent)

        # Se poucos batches, diminuir threshold
        if batches_usados < 2:
            novo_threshold = 35

            self.ajustes_sugeridos.append({
                'parametro': 'batch_threshold',
                'valor_atual': 50,
                'valor_sugerido': novo_threshold,
                'motivo': f'Apenas {batches_usados} batches em 10 execuções',
                'ganho_esperado': '+20% tarefas usando batch',
                'confianca': 'média'
            })

    def _analisar_stagnation_limit(self):
        """Analisa e sugere ajuste de stagnation_limit."""
        recent = self.historico[-10:]

        estagnacoes = sum(e['resultados']['estagnacoes'] for e in recent)

        # Se muitas estagnações, diminuir limit (detectar mais cedo)
        if estagnacoes >= 5:
            novo_limit = 3

            self.ajustes_sugeridos.append({
                'parametro': 'stagnation_limit',
                'valor_atual': 5,
                'valor_sugerido': novo_limit,
                'motivo': f'{estagnacoes} estagnações detectadas',
                'ganho_esperado': '+10% economia (detecta mais cedo)',
                'confianca': 'baixa'
            })

    def aplicar_ajustes(self, confirmar: bool = True) -> Dict[str, Any]:
        """
        Aplica ajustes ao agente.

        Args:
            confirmar: Se True, pede confirmação (modo manual)

        Returns:
            Dict com ajustes aplicados
        """
        if not self.ajustes_sugeridos:
            return {'aplicados': 0, 'ajustes': []}

        aplicados = []

        for ajuste in self.ajustes_sugeridos:
            # Modo manual: pedir confirmação
            if self.modo == "manual" and confirmar:
                print(f"\n🎯 AJUSTE SUGERIDO:")
                print(f"   Parâmetro: {ajuste['parametro']}")
                print(f"   {ajuste['valor_atual']} → {ajuste['valor_sugerido']}")
                print(f"   Motivo: {ajuste['motivo']}")
                print(f"   Ganho: {ajuste['ganho_esperado']}")

                resposta = input("   Aplicar? (s/N): ").lower()
                if resposta != 's':
                    continue

            # Aplicar ao agente
            if self.agente:
                self._aplicar_ao_agente(ajuste)
                aplicados.append(ajuste)

        return {'aplicados': len(aplicados), 'ajustes': aplicados}

    def _aplicar_ao_agente(self, ajuste: Dict):
        """Aplica ajuste no agente."""
        param = ajuste['parametro']
        valor = ajuste['valor_sugerido']

        if param == 'quality_threshold' and hasattr(self.agente, 'quality_threshold'):
            self.agente.quality_threshold = valor
        elif param == 'batch_threshold' and hasattr(self.agente, 'batch_threshold'):
            self.agente.batch_threshold = valor
        elif param == 'stagnation_limit' and hasattr(self.agente, 'stagnation_limit'):
            self.agente.stagnation_limit = valor

    def exibir_relatorio(self):
        """Exibe relatório de tuning."""
        print("\n" + "="*70)
        print("🎯 RELATÓRIO DE AUTO-TUNING")
        print("="*70)

        print(f"\nHistórico: {len(self.historico)} execuções")
        print(f"Modo: {self.modo}")

        if self.ajustes_sugeridos:
            print(f"\n📊 AJUSTES SUGERIDOS: {len(self.ajustes_sugeridos)}")
            for i, ajuste in enumerate(self.ajustes_sugeridos, 1):
                print(f"\n{i}. {ajuste['parametro']}")
                print(f"   {ajuste['valor_atual']} → {ajuste['valor_sugerido']}")
                print(f"   {ajuste['motivo']}")
                print(f"   Ganho: {ajuste['ganho_esperado']}")
        else:
            print("\n✅ Nenhum ajuste necessário no momento")

        print("\n" + "="*70)

    def resetar_historico(self):
        """Limpa histórico."""
        self.historico = []
        self._salvar_historico()


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("🎯 Testando Parameter Tuner\n")

    tuner = ParameterTuner(modo="manual")

    # Simular execuções
    for i in range(10):
        tuner.registrar_execucao({
            'quality_threshold': 90,
            'quality_scores': [82, 85, 87, 88],  # Quase atinge 90
            'batch_threshold': 50,
            'batches_usados': 0,  # Não usou batch
            'stagnation_limit': 5,
            'estagnacoes': 1
        })

    # Analisar e sugerir
    sugestoes = tuner.analisar_e_sugerir()

    # Exibir relatório
    tuner.exibir_relatorio()

    print("\n✅ Teste concluído!")
