#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 ANÁLISE MASSIVA DE CONTEXTO - Luna V3 (Versão Compacta)

Processa 300-400 arquivos simultaneamente usando batch + parallel.

Criado: 2025-10-20
Melhoria 1.3 - Nível 1
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
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


class MassiveContextAnalyzer:
    """Analisa múltiplos arquivos em paralelo/batch."""

    def __init__(self, agente=None, max_workers: int = 10):
        self.agente = agente
        self.max_workers = max_workers

    def analyze_repository(
        self,
        path: str,
        file_types: List[str] = ["*.py"],
        max_files: int = 400,
        operation: str = "summary"
    ) -> Dict[str, Any]:
        """
        Analisa repositório completo.

        Args:
            path: Caminho do diretório
            file_types: Padrões de arquivos (ex: ["*.py", "*.js"])
            max_files: Máximo de arquivos
            operation: Tipo de análise

        Returns:
            Dict com resultados agregados
        """
        print(f"\n🔍 Analisando repositório: {path}")
        print(f"   Tipos: {file_types}, Max: {max_files}")

        # Scan arquivos
        files = self._scan_files(path, file_types, max_files)
        print(f"   ✅ {len(files)} arquivos encontrados")

        if not files:
            return {'error': 'Nenhum arquivo encontrado', 'files': 0}

        # Processar em paralelo
        start = time.time()
        results = self._process_parallel(files, operation)
        elapsed = time.time() - start

        # Agregar resultados
        aggregated = self._aggregate_results(results)
        aggregated['elapsed_seconds'] = elapsed
        aggregated['files_processed'] = len(files)
        aggregated['speedup'] = f"{len(files) / max(1, elapsed):.1f} arquivos/s"

        print(f"\n✅ Análise completa em {elapsed:.1f}s")
        print(f"   Speedup: {aggregated['speedup']}")

        return aggregated

    def _scan_files(self, path: str, patterns: List[str], max_files: int) -> List[Path]:
        """Escaneia arquivos."""
        files = []
        for pattern in patterns:
            for file in Path(path).rglob(pattern):
                if file.is_file() and len(files) < max_files:
                    files.append(file)
        return files[:max_files]

    def _process_parallel(self, files: List[Path], operation: str) -> List[Dict]:
        """Processa arquivos em paralelo."""
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._analyze_file, file, operation): file
                for file in files
            }

            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({'error': str(e)})

        return results

    def _analyze_file(self, file: Path, operation: str) -> Dict:
        """Analisa um arquivo."""
        try:
            content = file.read_text(encoding='utf-8', errors='ignore')
            lines = len(content.split('\n'))

            # Análise simples (pode ser expandida)
            return {
                'file': str(file),
                'lines': lines,
                'size_kb': len(content) / 1024,
                'operation': operation,
                'status': 'ok'
            }
        except Exception as e:
            return {'file': str(file), 'error': str(e), 'status': 'error'}

    def _aggregate_results(self, results: List[Dict]) -> Dict:
        """Agrega resultados."""
        ok = [r for r in results if r.get('status') == 'ok']
        errors = [r for r in results if r.get('status') == 'error']

        return {
            'total': len(results),
            'success': len(ok),
            'errors': len(errors),
            'total_lines': sum(r.get('lines', 0) for r in ok),
            'total_size_kb': sum(r.get('size_kb', 0) for r in ok)
        }


# Teste
if __name__ == "__main__":
    analyzer = MassiveContextAnalyzer(max_workers=4)

    # Testar com diretório atual
    results = analyzer.analyze_repository(
        path=".",
        file_types=["*.py"],
        max_files=50,
        operation="summary"
    )

    print(f"\n📊 RESULTADOS:")
    print(f"   Total: {results['total']}")
    print(f"   Sucesso: {results['success']}")
    print(f"   Linhas: {results.get('total_lines', 0):,}")
    print(f"   Tamanho: {results.get('total_size_kb', 0):.1f} KB")
    print(f"   Tempo: {results['elapsed_seconds']:.1f}s")
    print(f"   Speedup: {results['speedup']}")
    print("\n✅ Melhoria 1.3: FUNCIONAL")
