#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TEST RUNNER UNIFICADO - Luna V3
===================================

Executa todos os arquivos de teste automaticamente e gera relatório consolidado.

Funcionalidades:
- Executa 9 test files em sequência
- Captura saídas (stdout/stderr)
- Detecta sucessos e falhas
- Gera relatório consolidado com métricas
- Identifica regressões comparando com última execução

Uso:
    python run_all_tests.py                    # Executar todos os testes
    python run_all_tests.py --only basic       # Executar apenas testes básicos
    python run_all_tests.py --skip google      # Pular testes do Google
    python run_all_tests.py --verbose          # Output detalhado

Criado: 2025-10-20
Parte do sistema de melhorias Luna V3
"""

import sys
import os
import subprocess
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse

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


# ============================================================================
# CONFIGURAÇÃO DOS TESTES
# ============================================================================

# Diretório do script (para paths relativos)
SCRIPT_DIR = Path(__file__).parent

# Lista de todos os test files disponíveis
TEST_FILES = {
    'basic': [
        'test_ferramentas_basicas.py',
    ],
    'planning': [
        'test_sistema_planejamento_basico.py',
        'test_planejamento_automatico.py',
        'test_planejamento_tarefa_real.py',
    ],
    'parallel': [
        'test_processamento_paralelo.py',
        'test_speedup_real.py',
    ],
    'integration': [
        'test_integracao_completa.py',
        'test_improvements_integration.py',
    ],
    'google': [
        'test_integracao_google.py',
    ]
}

# Arquivo para salvar histórico de execuções
HISTORY_FILE = SCRIPT_DIR / '.test_history.json'


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def print_section(title: str, char: str = '='):
    """Imprime seção formatada"""
    print(f"\n{char*70}")
    print(f"{title}")
    print(f"{char*70}\n")


def load_test_history() -> Dict:
    """Carrega histórico de execuções anteriores"""
    try:
        if Path(HISTORY_FILE).exists():
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return {'executions': []}


def save_test_history(results: Dict):
    """Salva resultados da execução no histórico"""
    try:
        history = load_test_history()
        history['executions'].append({
            'timestamp': datetime.now().isoformat(),
            'results': results
        })

        # Manter apenas últimas 10 execuções
        history['executions'] = history['executions'][-10:]

        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️  Aviso: Não foi possível salvar histórico: {e}")


def run_test_file(test_file: str, verbose: bool = False) -> Tuple[bool, str, float]:
    """
    Executa um arquivo de teste e retorna resultado

    Returns:
        (sucesso, output, tempo_execucao)
    """
    start_time = time.time()

    try:
        # Executar teste como subprocess (com path absoluto)
        test_path = SCRIPT_DIR / test_file
        result = subprocess.run(
            [sys.executable, str(test_path)],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=300  # 5 minutos máximo por teste
        )

        elapsed_time = time.time() - start_time
        output = result.stdout + result.stderr

        # Detectar sucesso/falha baseado em padrões comuns
        sucesso = (
            result.returncode == 0 and
            'ERRO' not in output.upper() and
            'FALHOU' not in output.upper() and
            'EXCEPTION' not in output.upper() and
            ('PASSOU' in output.upper() or 'SUCESSO' in output.upper() or 'OK' in output.upper())
        )

        if verbose:
            print(output)

        return sucesso, output, elapsed_time

    except subprocess.TimeoutExpired:
        elapsed_time = time.time() - start_time
        return False, f"TIMEOUT após {elapsed_time:.1f}s", elapsed_time

    except Exception as e:
        elapsed_time = time.time() - start_time
        return False, f"ERRO ao executar: {str(e)}", elapsed_time


def detect_regressions(current_results: Dict, history: Dict) -> List[str]:
    """Detecta regressões comparando com última execução"""
    regressions = []

    if not history.get('executions'):
        return regressions

    last_execution = history['executions'][-1]
    last_results = last_execution.get('results', {})

    for test_file in current_results.get('tests', []):
        current_status = test_file['status']
        test_name = test_file['file']

        # Buscar resultado anterior deste teste
        last_test = next(
            (t for t in last_results.get('tests', []) if t['file'] == test_name),
            None
        )

        if last_test and last_test['status'] == 'PASSOU' and current_status == 'FALHOU':
            regressions.append(test_name)

    return regressions


def generate_report(results: Dict, history: Dict):
    """Gera relatório consolidado formatado"""

    print_section("🎯 RESUMO EXECUTIVO", '=')

    total_tests = results['total']
    passed = results['passed']
    failed = results['failed']
    skipped = results['skipped']
    total_time = results['total_time']

    print(f"Total de testes:    {total_tests}")
    print(f"✅ Passaram:        {passed} ({passed/total_tests*100:.0f}%)")
    print(f"❌ Falharam:        {failed} ({failed/total_tests*100:.0f}%)")
    print(f"⏭️  Pulados:         {skipped}")
    print(f"⏱️  Tempo total:     {total_time:.1f}s")

    # Detectar regressões
    regressions = detect_regressions(results, history)
    if regressions:
        print(f"\n⚠️  REGRESSÕES DETECTADAS: {len(regressions)} teste(s) que passavam agora falharam")
        for test in regressions:
            print(f"   • {test}")

    # Detalhes por teste
    print_section("📋 DETALHES POR TESTE", '-')

    for test in results['tests']:
        status_icon = {
            'PASSOU': '✅',
            'FALHOU': '❌',
            'PULADO': '⏭️',
            'TIMEOUT': '⏱️'
        }.get(test['status'], '❓')

        print(f"{status_icon} {test['file']:<45} {test['time']:>6.1f}s")

        if test['status'] == 'FALHOU' and 'error_summary' in test:
            # Mostrar primeiras linhas do erro
            error_lines = test['error_summary'].split('\n')[:3]
            for line in error_lines:
                if line.strip():
                    print(f"      {line[:60]}")

    # Comparação com última execução
    if history.get('executions'):
        last_exec = history['executions'][-1]
        last_results = last_exec.get('results', {})

        if last_results:
            print_section("📊 COMPARAÇÃO COM ÚLTIMA EXECUÇÃO", '-')

            last_passed = last_results.get('passed', 0)
            last_failed = last_results.get('failed', 0)
            last_time = last_results.get('total_time', 0)

            delta_passed = passed - last_passed
            delta_failed = failed - last_failed
            delta_time = total_time - last_time

            print(f"Testes passando:  {last_passed} → {passed} ({delta_passed:+d})")
            print(f"Testes falhando:  {last_failed} → {failed} ({delta_failed:+d})")
            print(f"Tempo execução:   {last_time:.1f}s → {total_time:.1f}s ({delta_time:+.1f}s)")

            if delta_passed > 0 and delta_failed <= 0:
                print("\n🎉 MELHORIA! Mais testes passando que antes.")
            elif delta_passed < 0 or delta_failed > 0:
                print("\n⚠️  PIORA! Menos testes passando que antes.")

    # Status final
    print_section("🏁 STATUS FINAL", '=')

    if failed == 0:
        print("🎉 SUCESSO! Todos os testes passaram!")
        print("\n✅ Sistema Luna V3 validado e pronto para produção")
        return 0
    else:
        print(f"⚠️  ATENÇÃO: {failed} teste(s) falharam")
        print("\n❌ Corrija os erros antes de fazer deploy")
        return 1


# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    """Executa todos os testes e gera relatório"""

    # Parser de argumentos
    parser = argparse.ArgumentParser(description='Test Runner Unificado Luna V3')
    parser.add_argument('--only', choices=['basic', 'planning', 'parallel', 'integration', 'google'],
                       help='Executar apenas uma categoria de testes')
    parser.add_argument('--skip', choices=['basic', 'planning', 'parallel', 'integration', 'google'],
                       help='Pular uma categoria de testes')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Output detalhado de cada teste')

    args = parser.parse_args()

    # Banner
    print_section("🧪 TEST RUNNER UNIFICADO - LUNA V3", '=')
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Determinar quais testes executar
    tests_to_run = []

    if args.only:
        tests_to_run = TEST_FILES[args.only]
        print(f"Modo: Executando apenas categoria '{args.only}'")
    else:
        for category, files in TEST_FILES.items():
            if args.skip and category == args.skip:
                print(f"Pulando categoria: {category}")
                continue
            tests_to_run.extend(files)

    # Verificar se todos os arquivos existem
    missing_files = [f for f in tests_to_run if not (SCRIPT_DIR / f).exists()]
    if missing_files:
        print(f"\n⚠️  Aviso: {len(missing_files)} arquivo(s) de teste não encontrado(s):")
        for f in missing_files:
            print(f"   • {f}")
        tests_to_run = [f for f in tests_to_run if (SCRIPT_DIR / f).exists()]

    print(f"\nTotal de testes a executar: {len(tests_to_run)}\n")

    # Executar testes
    results = {
        'total': len(tests_to_run),
        'passed': 0,
        'failed': 0,
        'skipped': 0,
        'total_time': 0,
        'tests': []
    }

    for i, test_file in enumerate(tests_to_run, 1):
        print(f"[{i}/{len(tests_to_run)}] Executando {test_file}...", end=' ', flush=True)

        sucesso, output, tempo = run_test_file(test_file, args.verbose)

        status = 'PASSOU' if sucesso else 'FALHOU'
        if 'TIMEOUT' in output:
            status = 'TIMEOUT'

        if sucesso:
            results['passed'] += 1
            print(f"✅ PASSOU ({tempo:.1f}s)")
        else:
            results['failed'] += 1
            print(f"❌ FALHOU ({tempo:.1f}s)")

            if not args.verbose:
                # Mostrar resumo do erro
                error_lines = [l for l in output.split('\n') if 'ERRO' in l.upper() or 'EXCEPTION' in l.upper()]
                if error_lines:
                    print(f"   Erro: {error_lines[0][:80]}")

        results['total_time'] += tempo
        results['tests'].append({
            'file': test_file,
            'status': status,
            'time': tempo,
            'output': output[:500],  # Primeiros 500 chars apenas
            'error_summary': output if not sucesso else ''
        })

    # Carregar histórico
    history = load_test_history()

    # Gerar relatório
    exit_code = generate_report(results, history)

    # Salvar histórico
    save_test_history(results)

    return exit_code


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Execução interrompida pelo usuário")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ ERRO FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
