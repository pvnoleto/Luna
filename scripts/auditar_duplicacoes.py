#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Auditoria de Duplicações

Detecta duplicações de funções/classes em código Python causadas por
problemas de targeting no sistema de auto-evolução.

Uso:
    python scripts/auditar_duplicacoes.py luna_v3_FINAL_OTIMIZADA.py
"""

import ast
import sys
from typing import Dict, List, Tuple
from collections import defaultdict


class DuplicationAuditor:
    """Auditor de duplicações em código Python."""

    def __init__(self, arquivo: str):
        self.arquivo = arquivo
        self.duplicacoes: Dict[str, List[int]] = defaultdict(list)

    def auditar(self) -> Tuple[int, Dict[str, List[int]]]:
        """
        Audita o arquivo em busca de duplicações.

        Returns:
            (total_duplicacoes, dicionário com nome -> lista de linhas)
        """
        try:
            with open(self.arquivo, 'r', encoding='utf-8') as f:
                codigo = f.read()

            arvore = ast.parse(codigo)

            # Mapear todos os nomes de funções/classes com suas linhas
            nomes = defaultdict(list)

            for node in ast.walk(arvore):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if hasattr(node, 'name') and hasattr(node, 'lineno'):
                        nomes[node.name].append(node.lineno)

            # Identificar duplicações (mesmo nome aparecendo mais de uma vez)
            for nome, linhas in nomes.items():
                if len(linhas) > 1:
                    self.duplicacoes[nome] = sorted(linhas)

            return len(self.duplicacoes), self.duplicacoes

        except Exception as e:
            print(f"ERRO ao auditar: {e}", file=sys.stderr)
            return 0, {}

    def exibir_relatorio(self):
        """Exibe relatório de duplicações encontradas."""
        total, dups = self.auditar()

        print("=" * 80)
        print("RELATÓRIO DE AUDITORIA DE DUPLICAÇÕES")
        print("=" * 80)
        print(f"Arquivo: {self.arquivo}")
        print(f"Total de duplicações encontradas: {total}")
        print("=" * 80)

        if total == 0:
            print("✅ NENHUMA DUPLICAÇÃO DETECTADA")
            print("\nO arquivo está limpo, sem funções/classes duplicadas.")
            return 0

        print("❌ DUPLICAÇÕES DETECTADAS:")
        print()

        for nome, linhas in sorted(self.duplicacoes.items()):
            tipo = self._detectar_tipo(nome, linhas[0])
            print(f"{'='*80}")
            print(f"🔴 {tipo}: '{nome}'")
            print(f"   Ocorrências: {len(linhas)}")
            print(f"   Linhas: {', '.join(map(str, linhas))}")
            print()

            # Exibir contexto das primeiras linhas de cada ocorrência
            for i, linha in enumerate(linhas, 1):
                print(f"   Ocorrência {i} (linha {linha}):")
                self._exibir_contexto(linha)
                print()

        print("=" * 80)
        print("RECOMENDAÇÕES:")
        print()
        print("1. Revisar cada duplicação manualmente")
        print("2. Manter apenas a versão mais recente/correta")
        print("3. Remover as outras ocorrências")
        print("4. Validar sintaxe após remoção: python -m py_compile arquivo.py")
        print("5. Executar testes para garantir funcionamento")
        print("=" * 80)

        return total

    def _detectar_tipo(self, nome: str, linha: int) -> str:
        """Detecta se é função ou classe baseado no código."""
        try:
            with open(self.arquivo, 'r', encoding='utf-8') as f:
                linhas = f.readlines()

            if linha <= len(linhas):
                linha_codigo = linhas[linha - 1].strip()
                if linha_codigo.startswith('class '):
                    return "Classe"
                elif linha_codigo.startswith('def ') or linha_codigo.startswith('async def '):
                    return "Função"

            return "Definição"

        except:
            return "Definição"

    def _exibir_contexto(self, linha: int, contexto: int = 3):
        """Exibe algumas linhas de contexto ao redor da definição."""
        try:
            with open(self.arquivo, 'r', encoding='utf-8') as f:
                linhas = f.readlines()

            inicio = max(0, linha - 1)
            fim = min(len(linhas), linha + contexto)

            for i in range(inicio, fim):
                prefixo = "      >>> " if i == linha - 1 else "          "
                # Truncar linhas muito longas
                linha_texto = linhas[i].rstrip()
                if len(linha_texto) > 70:
                    linha_texto = linha_texto[:67] + "..."
                print(f"{prefixo}{linha_texto}")

        except Exception as e:
            print(f"      (Erro ao ler contexto: {e})")


def main():
    """Função principal."""
    if len(sys.argv) < 2:
        print("Uso: python auditar_duplicacoes.py <arquivo.py>")
        print()
        print("Exemplo:")
        print("  python scripts/auditar_duplicacoes.py luna_v3_FINAL_OTIMIZADA.py")
        sys.exit(1)

    arquivo = sys.argv[1]

    try:
        auditor = DuplicationAuditor(arquivo)
        total = auditor.exibir_relatorio()

        # Código de saída: 0 se não há duplicações, 1 se há
        sys.exit(1 if total > 0 else 0)

    except FileNotFoundError:
        print(f"ERRO: Arquivo '{arquivo}' não encontrado", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"ERRO: {e}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
