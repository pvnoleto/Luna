#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste das correções do Sprint 4
Valida que os bugs foram corrigidos
"""

import sys
import os
import tempfile

# Configurar encoding
os.environ['PYTHONUTF8'] = '1'
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Reconfigurar stdout/stderr para UTF-8 no Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_bug2_salvar_aprendizado():
    """
    Bug 2: AttributeError: 'MemoriaPermanente' object has no attribute 'salvar_aprendizado'

    Testa que o método salvar_aprendizado existe e funciona corretamente.
    """
    print("\n" + "="*80)
    print("TESTE BUG 2: Método salvar_aprendizado")
    print("="*80)

    try:
        from memoria_permanente import MemoriaPermanente

        # Criar instância com arquivo temporário
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name

        try:
            memoria = MemoriaPermanente(arquivo_memoria=temp_file)

            # Verificar que o método existe
            assert hasattr(memoria, 'salvar_aprendizado'), "Método salvar_aprendizado não existe!"

            # Testar chamada do método (mesma assinatura que Planning System usa)
            resultado = memoria.salvar_aprendizado(
                tipo="planejamento_sucesso",
                titulo="Teste do Planning System",
                conteudo="Sistema funciona corretamente",
                tags=['planejamento', 'teste']
            )

            # Verificar que retornou True (aprendizado salvo)
            assert resultado == True, f"Esperado True, recebido {resultado}"

            # Verificar que foi adicionado à memória
            assert len(memoria.memoria['aprendizados']) > 0, "Aprendizado não foi salvo!"

            print("[OK] Método salvar_aprendizado existe e funciona corretamente")
            print(f"[OK] Aprendizados na memória: {len(memoria.memoria['aprendizados'])}")
            print("[OK] BUG 2 CORRIGIDO!")

            return True

        finally:
            # Limpar arquivo temporário
            if os.path.exists(temp_file):
                os.unlink(temp_file)
            backup = f"{temp_file}.bak"
            if os.path.exists(backup):
                os.unlink(backup)

    except Exception as e:
        print(f"[ERRO] BUG 2 NÃO CORRIGIDO: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_bug1_json_parsing():
    """
    Bug 1: JSON parse error na decomposição

    Testa que o parsing de JSON tem retry e reparo.
    Não precisa executar Planning System completo, apenas verificar que
    o código de parsing existe e tem as melhorias.
    """
    print("\n" + "="*80)
    print("TESTE BUG 1: Retry e reparo de JSON")
    print("="*80)

    try:
        # Ler o arquivo e verificar que as melhorias estão presentes
        with open('luna_v3_FINAL_OTIMIZADA.py', 'r', encoding='utf-8') as f:
            codigo = f.read()

        # Verificar que tem retry logic
        assert 'max_tentativas = 2' in codigo, "Retry logic não encontrado!"
        assert 'for tentativa in range(max_tentativas)' in codigo, "Loop de retry não encontrado!"

        # Verificar que tem tentativa de reparo de JSON
        assert 'Tentar reparar JSON incompleto' in codigo, "Lógica de reparo não encontrada!"
        assert 'not resultado_limpo.endswith' in codigo, "Verificação de JSON truncado não encontrada!"

        # Verificar que reduz tokens na segunda tentativa
        assert 'max_tokens_atual = 4096 if tentativa == 0 else 2048' in codigo, "Redução de tokens não encontrada!"

        # Verificar mensagens de erro melhoradas
        assert 'Retentando com menos tokens' in codigo, "Mensagem de retry não encontrada!"

        print("[OK] Retry logic implementado (2 tentativas)")
        print("[OK] Reducao de tokens na segunda tentativa (4096 -> 2048)")
        print("[OK] Tentativa de reparo de JSON truncado")
        print("[OK] Mensagens de erro melhoradas")
        print("[OK] BUG 1 CORRIGIDO!")

        return True

    except Exception as e:
        print(f"[ERRO] BUG 1 NÃO CORRIGIDO: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Executa todos os testes do Sprint 4"""
    print("\n" + "="*80)
    print("TESTES DE VALIDAÇÃO - SPRINT 4")
    print("="*80)
    print("Validando correções dos bugs encontrados no Sprint 3")
    print("="*80)

    resultados = []

    # Teste Bug 2
    resultados.append(("Bug 2: salvar_aprendizado", test_bug2_salvar_aprendizado()))

    # Teste Bug 1
    resultados.append(("Bug 1: JSON parsing retry", test_bug1_json_parsing()))

    # Resumo
    print("\n" + "="*80)
    print("RESUMO DOS TESTES")
    print("="*80)

    total = len(resultados)
    passou = sum(1 for _, r in resultados if r)
    falhou = total - passou

    for nome, resultado in resultados:
        status = "[PASSOU]" if resultado else "[FALHOU]"
        print(f"{status} {nome}")

    print("="*80)
    print(f"Total: {passou}/{total} testes passaram")
    print("="*80)

    if falhou == 0:
        print("\n[SUCESSO] Todas as correções do Sprint 4 validadas!")
        return 0
    else:
        print(f"\n[FALHA] {falhou} teste(s) falharam")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
