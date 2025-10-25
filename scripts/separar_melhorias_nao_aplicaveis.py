#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Separar Melhorias Auto-Aplicáveis das Não-Aplicáveis

Identifica melhorias que contêm apenas sugestões (comentários) e as separa
das melhorias com código executável concreto.

Uso:
    python scripts/separar_melhorias_nao_aplicaveis.py [--dry-run] [--apply]

Opções:
    --dry-run: Apenas analisa sem modificar arquivos
    --apply: Aplica a separação (move melhorias não-aplicáveis)
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple


class SeparadorMelhorias:
    """Separa melhorias auto-aplicáveis das que precisam intervenção manual."""

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.fila_path = Path("Luna/.melhorias/fila_melhorias.json")
        self.manual_path = Path("Luna/.melhorias/fila_manual_only.json")
        self.relatorio_path = Path("LOGS_EXECUCAO/separacao_melhorias.json")

        # Estatísticas
        self.total_analisadas = 0
        self.auto_aplicaveis = 0
        self.manual_only = 0

        # Criar diretórios
        self.relatorio_path.parent.mkdir(parents=True, exist_ok=True)

    def eh_auto_aplicavel(self, melhoria: Dict) -> Tuple[bool, str]:
        """
        Verifica se uma melhoria é auto-aplicável.

        Returns:
            (eh_aplicavel, motivo)
        """
        codigo = melhoria.get('codigo', '').strip()

        # Vazio
        if not codigo:
            return False, "Código vazio"

        # Começa com comentário sugestão
        if codigo.startswith("# Substituir:") or codigo.startswith("# Por:"):
            return False, "Contém template de sugestão (# Substituir/Por)"

        # Apenas comentários (todas as linhas começam com #)
        linhas = codigo.split('\n')
        linhas_codigo = [l for l in linhas if l.strip() and not l.strip().startswith('#')]

        if not linhas_codigo:
            return False, "Contém apenas comentários, sem código executável"

        # Contém código executável
        return True, "Código executável presente"

    def carregar_fila(self) -> Dict:
        """Carrega fila de melhorias."""
        if not self.fila_path.exists():
            print(f"❌ Arquivo de fila não encontrado: {self.fila_path}")
            sys.exit(1)

        with open(self.fila_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def salvar_fila(self, data: Dict):
        """Salva fila de melhorias."""
        with open(self.fila_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def salvar_manual_only(self, melhorias: List[Dict]):
        """Salva melhorias que precisam intervenção manual."""
        data = {
            "manual_only": melhorias,
            "total": len(melhorias),
            "criado_em": datetime.now().isoformat(),
            "descricao": "Melhorias que contêm sugestões/templates e precisam de conversão manual para código executável"
        }

        with open(self.manual_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def salvar_relatorio(self, auto_aplicaveis: List[Dict], manual_only: List[Dict]):
        """Salva relatório da separação."""
        relatorio = {
            "timestamp": datetime.now().isoformat(),
            "total_analisadas": self.total_analisadas,
            "auto_aplicaveis": {
                "total": len(auto_aplicaveis),
                "por_prioridade": {},
                "por_tipo": {},
                "ids": [m.get('id') for m in auto_aplicaveis]
            },
            "manual_only": {
                "total": len(manual_only),
                "por_prioridade": {},
                "por_tipo": {},
                "ids": [m.get('id') for m in manual_only],
                "motivos": {}
            }
        }

        # Estatísticas auto-aplicáveis
        for m in auto_aplicaveis:
            p = f"P{m.get('prioridade')}"
            t = m.get('tipo')
            relatorio["auto_aplicaveis"]["por_prioridade"][p] = \
                relatorio["auto_aplicaveis"]["por_prioridade"].get(p, 0) + 1
            relatorio["auto_aplicaveis"]["por_tipo"][t] = \
                relatorio["auto_aplicaveis"]["por_tipo"].get(t, 0) + 1

        # Estatísticas manual-only
        for m in manual_only:
            p = f"P{m.get('prioridade')}"
            t = m.get('tipo')
            relatorio["manual_only"]["por_prioridade"][p] = \
                relatorio["manual_only"]["por_prioridade"].get(p, 0) + 1
            relatorio["manual_only"]["por_tipo"][t] = \
                relatorio["manual_only"]["por_tipo"].get(t, 0) + 1

            # Motivo
            _, motivo = self.eh_auto_aplicavel(m)
            relatorio["manual_only"]["motivos"][motivo] = \
                relatorio["manual_only"]["motivos"].get(motivo, 0) + 1

        with open(self.relatorio_path, 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)

    def executar(self):
        """Executa a separação."""
        print("="*80)
        print("SEPARAÇÃO DE MELHORIAS AUTO-APLICÁVEIS vs MANUAL-ONLY")
        print("="*80)
        print()

        # Carregar fila
        print("[*] Carregando fila de melhorias...")
        data = self.carregar_fila()
        pendentes = data.get('pendentes', [])
        print(f"   Total na fila: {len(pendentes)}")
        print()

        # Analisar cada melhoria
        print("[*] Analisando melhorias...")
        auto_aplicaveis = []
        manual_only = []

        for melhoria in pendentes:
            self.total_analisadas += 1
            eh_aplicavel, motivo = self.eh_auto_aplicavel(melhoria)

            if eh_aplicavel:
                auto_aplicaveis.append(melhoria)
            else:
                manual_only.append(melhoria)
                # Adicionar motivo à melhoria
                melhoria['nao_aplicavel_motivo'] = motivo

        print(f"   Auto-aplicáveis: {len(auto_aplicaveis)}")
        print(f"   Manual-only: {len(manual_only)}")
        print()

        # Análise detalhada por prioridade
        print("[*] Distribuição por prioridade:")
        for p in range(1, 11):
            total_p = sum(1 for m in pendentes if m.get('prioridade') == p)
            auto_p = sum(1 for m in auto_aplicaveis if m.get('prioridade') == p)
            manual_p = sum(1 for m in manual_only if m.get('prioridade') == p)

            if total_p > 0:
                pct_auto = (auto_p / total_p * 100) if total_p > 0 else 0
                print(f"   P{p}: {total_p} total | {auto_p} auto ({pct_auto:.0f}%) | {manual_p} manual")

        print()

        # Análise de motivos
        print("[*] Motivos para classificação como manual-only:")
        motivos_count = {}
        for m in manual_only:
            motivo = m.get('nao_aplicavel_motivo', 'Desconhecido')
            motivos_count[motivo] = motivos_count.get(motivo, 0) + 1

        for motivo, count in sorted(motivos_count.items(), key=lambda x: x[1], reverse=True):
            print(f"   - {motivo}: {count}")

        print()

        # Modo dry-run
        if self.dry_run:
            print("[DRY-RUN] Modo dry-run - Nenhuma modificação será feita")
            print()
            print("Para aplicar as mudanças, execute:")
            print("  python scripts/separar_melhorias_nao_aplicaveis.py --apply")
            print()
        else:
            print("[>>] Aplicando separação...")

            # Atualizar fila principal (apenas auto-aplicáveis)
            data['pendentes'] = auto_aplicaveis
            data['ultima_atualizacao'] = datetime.now().isoformat()
            data['observacao'] = f"Removidas {len(manual_only)} melhorias não-aplicáveis (movidas para fila_manual_only.json)"
            self.salvar_fila(data)
            print(f"   [OK] Fila principal atualizada: {len(auto_aplicaveis)} melhorias auto-aplicáveis")

            # Salvar melhorias manual-only
            self.salvar_manual_only(manual_only)
            print(f"   [OK] Melhorias manual-only salvas: {self.manual_path}")

            print()

        # Salvar relatório
        self.salvar_relatorio(auto_aplicaveis, manual_only)
        print(f"[*] Relatório salvo em: {self.relatorio_path}")

        # Resumo final
        print()
        print("="*80)
        print("RESUMO")
        print("="*80)
        print(f"Total analisadas: {self.total_analisadas}")
        print(f"Auto-aplicáveis: {len(auto_aplicaveis)} ({len(auto_aplicaveis)/self.total_analisadas*100:.1f}%)")
        print(f"Manual-only: {len(manual_only)} ({len(manual_only)/self.total_analisadas*100:.1f}%)")
        print()

        if len(manual_only) > 0:
            print("[!] ATENÇÃO: Melhorias manual-only precisam de conversão antes de serem aplicáveis")
            print(f"[!] Veja detalhes em: {self.manual_path}")
            print()

        if len(auto_aplicaveis) > 0:
            print("[OK] Melhorias auto-aplicáveis prontas para processamento")
            print(f"[OK] Execute: python scripts/aplicar_melhorias_p7_p8.py")
            print()

        print("="*80)


def main():
    """Função principal."""
    import argparse

    parser = argparse.ArgumentParser(description="Separar melhorias auto-aplicáveis das manual-only")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Apenas analisar sem modificar (padrão)")
    parser.add_argument("--apply", action="store_true", help="Aplicar a separação (modificar arquivos)")

    args = parser.parse_args()

    # Se --apply foi passado, desabilitar dry-run
    dry_run = not args.apply

    # Criar separador
    separador = SeparadorMelhorias(dry_run=dry_run)

    # Executar
    try:
        separador.executar()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
