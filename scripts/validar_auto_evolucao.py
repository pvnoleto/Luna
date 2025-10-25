#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Script de Validação do Sistema de Auto-Evolução

Verifica que o sistema está funcional antes de usar.

Uso:
    python scripts/validar_auto_evolucao.py

Retorna:
    0 se tudo OK
    1 se houver problemas
"""

import os
import sys
from pathlib import Path

# ═══ CONFIGURAÇÃO UTF-8 PARA WINDOWS ═══
if sys.platform == 'win32':
    # Forçar UTF-8 no ambiente
    os.environ['PYTHONUTF8'] = '1'
    os.environ['PYTHONIOENCODING'] = 'utf-8'

    # Reconfigurar stdout/stderr para UTF-8
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Adicionar pasta raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

def validar():
    """Executa validação completa do sistema"""
    print("🔍 Validando Sistema de Auto-Evolução da Luna V3...\n")

    erros = []
    avisos = []

    # ═══ 1. Verificar arquivo alvo ═══
    print("1️⃣  Verificando arquivo alvo...")
    arquivo = "luna_v3_FINAL_OTIMIZADA.py"

    if not os.path.exists(arquivo):
        erros.append(f"Arquivo alvo não encontrado: {arquivo}")
        print(f"   ❌ Arquivo alvo não encontrado: {arquivo}\n")
    else:
        tamanho = os.path.getsize(arquivo)
        print(f"   ✅ Arquivo alvo existe: {arquivo} ({tamanho:,} bytes)\n")

    # ═══ 2. Tentar importar módulo ═══
    print("2️⃣  Importando módulo sistema_auto_evolucao...")
    try:
        from sistema_auto_evolucao import SistemaAutoEvolucao
        print(f"   ✅ Módulo importado com sucesso\n")
    except ImportError as e:
        erros.append(f"Erro ao importar sistema_auto_evolucao: {e}")
        print(f"   ❌ Erro ao importar: {e}\n")
        return False
    except Exception as e:
        erros.append(f"Erro inesperado ao importar: {e}")
        print(f"   ❌ Erro inesperado: {e}\n")
        return False

    # ═══ 3. Tentar inicializar sistema ═══
    print("3️⃣  Inicializando sistema...")
    try:
        sistema = SistemaAutoEvolucao(arquivo_alvo=arquivo)
        print(f"   ✅ Sistema inicializado com sucesso\n")
    except FileNotFoundError as e:
        erros.append(f"FileNotFoundError ao inicializar: {e}")
        print(f"   ❌ Arquivo não encontrado: {e}\n")
        return False
    except Exception as e:
        erros.append(f"Erro ao inicializar sistema: {e}")
        print(f"   ❌ Erro ao inicializar: {e}\n")
        return False

    # ═══ 4. Verificar diretório de backups ═══
    print("4️⃣  Verificando diretório de backups...")
    if not os.path.exists(sistema.dir_backups):
        avisos.append(f"Diretório de backups não existe: {sistema.dir_backups}")
        print(f"   ⚠️  Diretório não existe (será criado): {sistema.dir_backups}\n")
    else:
        # Contar backups existentes
        backups = list(Path(sistema.dir_backups).glob("*.py"))
        print(f"   ✅ Diretório existe: {sistema.dir_backups}")
        print(f"   📊 Backups existentes: {len(backups)}\n")

    # ═══ 5. Testar criação de backup ═══
    print("5️⃣  Testando criação de backup...")
    try:
        backup = sistema._criar_backup("Teste de validação - pode deletar")

        if not os.path.exists(backup):
            erros.append(f"Backup não foi criado: {backup}")
            print(f"   ❌ Backup não foi criado\n")
        else:
            tamanho_backup = os.path.getsize(backup)
            print(f"   ✅ Backup criado: {Path(backup).name} ({tamanho_backup:,} bytes)")

            # Verificar metadados
            meta_path = f"{backup}.meta"
            if os.path.exists(meta_path):
                print(f"   ✅ Metadados criados: {Path(meta_path).name}")
            else:
                avisos.append(f"Metadados não criados: {meta_path}")
                print(f"   ⚠️  Metadados não criados")

            # Limpar teste
            try:
                os.remove(backup)
                if os.path.exists(meta_path):
                    os.remove(meta_path)
                print(f"   🗑️  Backup de teste removido\n")
            except Exception as e:
                avisos.append(f"Erro ao remover backup de teste: {e}")
                print(f"   ⚠️  Erro ao remover: {e}\n")

    except Exception as e:
        erros.append(f"Erro ao criar backup de teste: {e}")
        print(f"   ❌ Erro ao criar backup: {e}\n")

    # ═══ 6. Verificar zonas protegidas ═══
    print("6️⃣  Verificando zonas protegidas...")
    zonas_protegidas = ['__init__', 'executar_tarefa', '_executar_chamada_api']
    for zona in zonas_protegidas:
        protegida = sistema._verificar_zona_protegida("", zona)
        if protegida:
            print(f"   ✅ Zona protegida: {zona}")
        else:
            avisos.append(f"Zona {zona} não está protegida")
            print(f"   ⚠️  Zona NÃO protegida: {zona}")
    print()

    # ═══ RESUMO ═══
    print("=" * 70)
    print("📊 RESUMO DA VALIDAÇÃO")
    print("=" * 70)

    if erros:
        print(f"\n❌ ERROS ENCONTRADOS ({len(erros)}):")
        for i, erro in enumerate(erros, 1):
            print(f"   {i}. {erro}")

    if avisos:
        print(f"\n⚠️  AVISOS ({len(avisos)}):")
        for i, aviso in enumerate(avisos, 1):
            print(f"   {i}. {aviso}")

    if not erros and not avisos:
        print("\n✅ VALIDAÇÃO COMPLETA - Sistema totalmente funcional!")
        print("\n🎉 O sistema de auto-evolução está pronto para uso!")
        return True
    elif not erros:
        print(f"\n⚠️  VALIDAÇÃO COMPLETA COM AVISOS - Sistema funcional mas com alertas")
        return True
    else:
        print(f"\n❌ VALIDAÇÃO FALHOU - Corrija os erros antes de usar")
        return False


if __name__ == "__main__":
    try:
        sucesso = validar()
        sys.exit(0 if sucesso else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Validação interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro inesperado durante validação: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
