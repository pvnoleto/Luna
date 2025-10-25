#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 SMOKE TESTS - LUNA V4
========================

✅ FASE 3: Validação Semântica (P1)

Testes rápidos para validar que componentes críticos funcionam após modificações.
Executados automaticamente pelo sistema de auto-evolução.

Objetivo: Detectar quebras funcionais que validação sintática não pega.
"""

import sys
import os

# Configurar encoding
os.environ['PYTHONUTF8'] = '1'
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Reconfigurar stdout/stderr para UTF-8 (Windows compatibility)
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports_basicos():
    """Testa que imports básicos funcionam"""
    try:
        # Imports principais
        from sistema_auto_evolucao import FilaDeMelhorias, SistemaAutoEvolucao
        from detector_melhorias import DetectorMelhorias
        from memoria_permanente import MemoriaPermanente

        return True, "Imports básicos OK"
    except Exception as e:
        return False, f"Falha no import: {e}"


def test_fila_melhorias_basico():
    """Testa funcionalidade básica da fila de melhorias"""
    try:
        import tempfile
        from sistema_auto_evolucao import FilaDeMelhorias

        # Criar fila temporária
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_file = f.name

        try:
            fila = FilaDeMelhorias(arquivo=temp_file)

            # Teste 1: Adicionar melhoria
            id1 = fila.adicionar(
                tipo='teste',
                alvo='funcao_teste',
                motivo='Teste smoke',
                codigo_sugerido='def teste(): pass',
                prioridade=5
            )

            if not id1:
                return False, "Falha ao adicionar melhoria"

            # Teste 2: Obter pendentes
            pendentes = fila.obter_pendentes()
            if len(pendentes) != 1:
                return False, f"Esperado 1 pendente, obtido {len(pendentes)}"

            # Teste 3: Marcar como aplicada
            fila.marcar_aplicada(id1, {'teste': True})

            if len(fila.melhorias_aplicadas) != 1:
                return False, "Falha ao marcar como aplicada"

            return True, "FilaDeMelhorias funcional"

        finally:
            # Limpar
            if os.path.exists(temp_file):
                os.unlink(temp_file)
            backup = f"{temp_file}.bak"
            if os.path.exists(backup):
                os.unlink(backup)

    except Exception as e:
        return False, f"Erro em FilaDeMelhorias: {e}"


def test_detector_melhorias_basico():
    """Testa funcionalidade básica do detector"""
    try:
        from detector_melhorias import DetectorMelhorias

        detector = DetectorMelhorias()

        # Código de teste simples
        codigo_teste = '''
def funcao_sem_docstring(x, y):
    return x + y
'''

        # Analisar
        melhorias = detector.analisar_codigo_executado("teste", codigo_teste)

        # Deve detectar falta de docstring
        if not melhorias:
            return False, "Detector não detectou melhorias óbvias"

        # Verificar que detectou tipo correto
        tipos = [m['tipo'] for m in melhorias]
        if 'documentacao' not in tipos and 'qualidade' not in tipos:
            return False, f"Tipos detectados incorretos: {tipos}"

        return True, "DetectorMelhorias funcional"

    except Exception as e:
        return False, f"Erro em DetectorMelhorias: {e}"


def test_memoria_permanente_basico():
    """Testa funcionalidade básica da memória"""
    try:
        import tempfile
        from memoria_permanente import MemoriaPermanente

        # Criar memória temporária
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_file = f.name

        try:
            memoria = MemoriaPermanente(arquivo_memoria=temp_file)

            # Teste 1: Adicionar aprendizado
            memoria.adicionar_aprendizado(
                categoria='teste',
                conteudo='Teste smoke - validação semântica',
                contexto='Execução de smoke tests',
                tags=['teste']
            )

            if len(memoria.memoria['aprendizados']) == 0:
                return False, "Falha ao adicionar aprendizado"

            # Teste 2: Buscar
            resultados = memoria.buscar_aprendizados('teste')
            if not resultados:
                return False, "Falha na busca de aprendizados"

            return True, "MemoriaPermanente funcional"

        finally:
            # Limpar
            if os.path.exists(temp_file):
                os.unlink(temp_file)
            backup = f"{temp_file}.bak"
            if os.path.exists(backup):
                os.unlink(backup)

    except Exception as e:
        return False, f"Erro em MemoriaPermanente: {e}"


def test_sistema_auto_evolucao_basico():
    """Testa funcionalidade básica do sistema de auto-evolução"""
    try:
        from sistema_auto_evolucao import SistemaAutoEvolucao

        # Verificar que pode ser instanciado
        sistema = SistemaAutoEvolucao()

        # Verificar atributos essenciais
        if not hasattr(sistema, 'arquivo_alvo'):
            return False, "Atributo arquivo_alvo ausente"

        if not hasattr(sistema, 'stats'):
            return False, "Atributo stats ausente"

        # Verificar métodos essenciais
        if not hasattr(sistema, 'aplicar_modificacao'):
            return False, "Método aplicar_modificacao ausente"

        if not hasattr(sistema, '_validar_codigo'):
            return False, "Método _validar_codigo ausente"

        return True, "SistemaAutoEvolucao funcional"

    except Exception as e:
        return False, f"Erro em SistemaAutoEvolucao: {e}"


def executar_todos_smoke_tests(verbose=False):
    """
    Executa todos os smoke tests

    Args:
        verbose: Se True, mostra detalhes de cada teste

    Returns:
        Tupla (todos_passaram: bool, resultados: list)
    """
    testes = [
        ("Imports básicos", test_imports_basicos),
        ("FilaDeMelhorias", test_fila_melhorias_basico),
        ("DetectorMelhorias", test_detector_melhorias_basico),
        ("MemoriaPermanente", test_memoria_permanente_basico),
        ("SistemaAutoEvolucao", test_sistema_auto_evolucao_basico),
    ]

    resultados = []
    todos_passaram = True

    if verbose:
        print("="*70)
        print("🧪 EXECUTANDO SMOKE TESTS")
        print("="*70)

    for nome, test_func in testes:
        try:
            passou, mensagem = test_func()
            resultados.append({
                'nome': nome,
                'passou': passou,
                'mensagem': mensagem
            })

            if not passou:
                todos_passaram = False

            if verbose:
                status = "✅ PASSOU" if passou else "❌ FALHOU"
                print(f"{status} {nome}: {mensagem}")

        except Exception as e:
            todos_passaram = False
            resultados.append({
                'nome': nome,
                'passou': False,
                'mensagem': f"Exceção: {e}"
            })

            if verbose:
                print(f"❌ FALHOU {nome}: Exceção: {e}")

    if verbose:
        print("="*70)
        passou_count = sum(1 for r in resultados if r['passou'])
        print(f"Resultado: {passou_count}/{len(resultados)} testes passaram")
        print("="*70)

    return todos_passaram, resultados


def main():
    """Executa smoke tests e retorna exit code"""
    todos_passaram, resultados = executar_todos_smoke_tests(verbose=True)

    if todos_passaram:
        print("\n✅ Todos os smoke tests passaram!")
        return 0
    else:
        falhas = [r for r in resultados if not r['passou']]
        print(f"\n❌ {len(falhas)} teste(s) falharam:")
        for r in falhas:
            print(f"   - {r['nome']}: {r['mensagem']}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
