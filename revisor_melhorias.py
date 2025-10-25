#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
✅ FASE 6: INTERFACE DE REVISÃO EM LOTE (P3)
============================================

Interface interativa para revisar e aprovar/rejeitar melhorias em lote.

Funcionalidades:
- Preview detalhado de mudanças
- Aprovação/rejeição em lote
- Filtros por tipo, prioridade, risco
- Estatísticas em tempo real
"""

import sys
import os
from typing import List, Dict, Optional

# Configurar encoding
os.environ['PYTHONUTF8'] = '1'
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Reconfigurar stdout/stderr para UTF-8 (Windows compatibility)
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class RevisorMelhorias:
    """
    Interface de revisão em lote para melhorias
    """

    def __init__(self, fila):
        """
        Inicializa revisor

        Args:
            fila: Instância de FilaDeMelhorias
        """
        self.fila = fila
        self.selecionadas = []
        self.filtros = {}

    def listar_com_preview(self, melhorias: List[Dict], mostrar_codigo: bool = False):
        """
        Lista melhorias com preview formatado

        Args:
            melhorias: Lista de melhorias
            mostrar_codigo: Se deve mostrar código completo
        """
        if not melhorias:
            print("\n📭 Nenhuma melhoria encontrada.")
            return

        print(f"\n📋 {len(melhorias)} melhoria(s) encontrada(s)\n")

        for i, m in enumerate(melhorias, 1):
            nivel_risco = m.get('nivel_risco', '?')
            prioridade = m.get('prioridade', 0)

            # Ícone de risco
            icone_risco = {
                'SAFE': '✅',
                'MEDIUM': '⚠️',
                'RISKY': '🔴'
            }.get(nivel_risco, '❓')

            print(f"[{i}] {icone_risco} {m['tipo']:20} | P={prioridade} | {m['alvo'][:40]}")
            print(f"    Motivo: {m['motivo'][:70]}")

            if mostrar_codigo:
                print(f"    Código: {m['codigo'][:100]}{'...' if len(m['codigo']) > 100 else ''}")

            print()

    def filtrar(self, melhorias: List[Dict], **criterios) -> List[Dict]:
        """
        Filtra melhorias por critérios

        Args:
            melhorias: Lista de melhorias
            **criterios: Filtros (tipo, nivel_risco, min_prioridade, max_prioridade)

        Returns:
            Lista filtrada
        """
        resultado = melhorias

        if 'tipo' in criterios:
            resultado = [m for m in resultado if m['tipo'] == criterios['tipo']]

        if 'nivel_risco' in criterios:
            resultado = [m for m in resultado if m.get('nivel_risco') == criterios['nivel_risco']]

        if 'min_prioridade' in criterios:
            resultado = [m for m in resultado if m.get('prioridade', 0) >= criterios['min_prioridade']]

        if 'max_prioridade' in criterios:
            resultado = [m for m in resultado if m.get('prioridade', 0) <= criterios['max_prioridade']]

        return resultado

    def revisar_interativo(self):
        """
        Modo interativo de revisão

        Permite ao usuário revisar melhorias uma a uma ou em lote
        """
        melhorias = self.fila.obter_pendentes(ordenar_por_prioridade=True)

        if not melhorias:
            print("\n✅ Nenhuma melhoria pendente para revisar!")
            return

        print("\n" + "="*70)
        print("📝 REVISOR DE MELHORIAS - MODO INTERATIVO")
        print("="*70)

        aprovadas = []
        rejeitadas = []

        while melhorias:
            self.listar_com_preview(melhorias[:5])  # Mostrar 5 por vez

            print("\nOpções:")
            print("  [a] Aprovar primeira")
            print("  [r] Rejeitar primeira")
            print("  [A] Aprovar todas SAFE")
            print("  [M] Aprovar todas MEDIUM com prioridade >= 7")
            print("  [p] Ver próximas 5")
            print("  [d] Ver detalhes da primeira")
            print("  [q] Sair")

            escolha = input("\nEscolha: ").strip().lower()

            if escolha == 'q':
                break

            elif escolha == 'a':
                if melhorias:
                    aprovadas.append(melhorias.pop(0))
                    print("✅ Aprovada!")

            elif escolha == 'r':
                if melhorias:
                    rejeitadas.append(melhorias.pop(0))
                    print("❌ Rejeitada!")

            elif escolha == 'A':
                safe = [m for m in melhorias if m.get('nivel_risco') == 'SAFE']
                aprovadas.extend(safe)
                melhorias = [m for m in melhorias if m.get('nivel_risco') != 'SAFE']
                print(f"✅ {len(safe)} melhorias SAFE aprovadas!")

            elif escolha == 'M':
                medium_high = [m for m in melhorias
                              if m.get('nivel_risco') == 'MEDIUM' and m.get('prioridade', 0) >= 7]
                aprovadas.extend(medium_high)
                melhorias = [m for m in melhorias if m not in medium_high]
                print(f"✅ {len(medium_high)} melhorias MEDIUM (P>=7) aprovadas!")

            elif escolha == 'p':
                # Rotacionar para ver próximas
                if len(melhorias) > 5:
                    melhorias = melhorias[5:] + melhorias[:5]
                print("📄 Próximas 5 melhorias...")

            elif escolha == 'd':
                if melhorias:
                    self._mostrar_detalhes(melhorias[0])

        # Resumo
        print("\n" + "="*70)
        print("📊 RESUMO DA REVISÃO")
        print("="*70)
        print(f"✅ Aprovadas: {len(aprovadas)}")
        print(f"❌ Rejeitadas: {len(rejeitadas)}")
        print(f"⏸️  Pendentes: {len(melhorias)}")

        return {
            'aprovadas': aprovadas,
            'rejeitadas': rejeitadas,
            'pendentes': melhorias
        }

    def _mostrar_detalhes(self, melhoria: Dict):
        """Mostra detalhes completos de uma melhoria"""
        print("\n" + "="*70)
        print("🔍 DETALHES DA MELHORIA")
        print("="*70)
        print(f"ID: {melhoria['id']}")
        print(f"Tipo: {melhoria['tipo']}")
        print(f"Nível de Risco: {melhoria.get('nivel_risco', '?')}")
        print(f"Prioridade: {melhoria.get('prioridade', 0)}/10")
        print(f"Alvo: {melhoria['alvo']}")
        print(f"\nMotivo:\n{melhoria['motivo']}")
        print(f"\nCódigo sugerido:\n{melhoria['codigo']}")
        print("="*70)

    def aprovar_em_lote(self, criterios: Dict) -> int:
        """
        Aprova melhorias em lote baseado em critérios

        Args:
            criterios: Filtros para aprovação automática

        Returns:
            Número de melhorias aprovadas
        """
        melhorias = self.fila.obter_pendentes(ordenar_por_prioridade=True)
        aprovadas = self.filtrar(melhorias, **criterios)

        print(f"\n📊 {len(aprovadas)} melhoria(s) atendem aos critérios:")
        self.listar_com_preview(aprovadas[:10])  # Mostrar até 10

        if len(aprovadas) > 10:
            print(f"... e mais {len(aprovadas) - 10} melhorias")

        confirmar = input(f"\n✅ Aprovar todas {len(aprovadas)} melhorias? (s/N): ").strip().lower()

        if confirmar == 's':
            print(f"✅ {len(aprovadas)} melhorias aprovadas em lote!")
            return aprovadas
        else:
            print("❌ Operação cancelada.")
            return []


def revisar_modo_rapido(arquivo_fila: str = "Luna/.melhorias/fila_melhorias.json"):
    """
    Modo rápido: Aprova automaticamente melhorias seguras

    Args:
        arquivo_fila: Caminho da fila de melhorias
    """
    from sistema_auto_evolucao import FilaDeMelhorias

    fila = FilaDeMelhorias(arquivo=arquivo_fila)
    revisor = RevisorMelhorias(fila)

    print("\n" + "="*70)
    print("⚡ MODO RÁPIDO: AUTO-APROVAÇÃO DE MELHORIAS SEGURAS")
    print("="*70)

    # Aprovar SAFE
    safe = revisor.aprovar_em_lote({'nivel_risco': 'SAFE'})

    # Aprovar MEDIUM alta prioridade
    medium_high = revisor.aprovar_em_lote({
        'nivel_risco': 'MEDIUM',
        'min_prioridade': 8
    })

    total = len(safe) + len(medium_high)

    print(f"\n✅ Total aprovado automaticamente: {total} melhorias")
    print(f"   - {len(safe)} SAFE")
    print(f"   - {len(medium_high)} MEDIUM (P>=8)")

    return safe + medium_high


def main():
    """Ponto de entrada principal"""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--rapido':
        # Modo rápido
        aprovadas = revisar_modo_rapido()
        print(f"\n✅ {len(aprovadas)} melhorias aprovadas!")
    else:
        # Modo interativo
        from sistema_auto_evolucao import FilaDeMelhorias

        fila = FilaDeMelhorias()
        revisor = RevisorMelhorias(fila)

        resultado = revisor.revisar_interativo()

        if resultado:
            print(f"\n✅ Revisão concluída!")
            print(f"   Aprovadas: {len(resultado['aprovadas'])}")
            print(f"   Rejeitadas: {len(resultado['rejeitadas'])}")


if __name__ == "__main__":
    main()
