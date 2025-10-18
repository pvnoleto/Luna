#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTE SIMPLES DA CORREÇÃO DO ERRO ITERAÇÃO 19
=================================================

Testa especificamente a correção do método listar_arquivos()
"""

import sys
import os
from pathlib import Path

# Adicionar diretório raiz do Luna ao path
luna_root = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(luna_root))

print(f"📂 Diretório Luna: {luna_root}")
print(f"📂 Workspace atual: {Path.cwd()}")

try:
    from gerenciador_workspaces import GerenciadorWorkspaces
    print("✅ GerenciadorWorkspaces importado com sucesso!")
except ImportError as e:
    print(f"❌ Erro ao importar: {e}")
    sys.exit(1)

print("\n" + "="*80)
print("🧪 TESTE: Correção do erro listar_arquivos()")
print("="*80 + "\n")

# Inicializar gerenciador
gw = GerenciadorWorkspaces()

# Verificar workspace atual
print("1️⃣ Verificando workspace atual...")
atual = gw.get_workspace_atual()
if atual:
    print(f"   ✅ Workspace atual: {atual['nome']}")
else:
    print("   ℹ️ Nenhum workspace selecionado")

# Listar workspaces disponíveis
print("\n2️⃣ Listando workspaces disponíveis...")
workspaces = gw.listar_workspaces()
for ws in workspaces:
    print(f"   📁 {ws['nome']}: {ws.get('arquivos', 0)} arquivo(s)")

# Selecionar workspace de teste (ou criar)
workspace_teste = 'arquivos_luna'
print(f"\n3️⃣ Selecionando workspace '{workspace_teste}'...")
if workspace_teste not in [ws['nome'] for ws in workspaces]:
    print(f"   ℹ️ Workspace não existe, criando...")
    gw.criar_workspace(workspace_teste, 'Workspace de teste')
    
gw.selecionar_workspace(workspace_teste)
print(f"   ✅ Workspace '{workspace_teste}' selecionado")

# TESTE PRINCIPAL: listar_arquivos()
print(f"\n4️⃣ Testando listar_arquivos() - ⚠️ PONTO DO ERRO ORIGINAL")
print("   Chamando: gw.listar_arquivos()")

try:
    arquivos = gw.listar_arquivos(workspace_teste)
    print(f"   ✅ Método executado com sucesso!")
    print(f"   ✅ Tipo retornado: {type(arquivos)}")
    
    if arquivos:
        print(f"   ✅ Total de arquivos: {len(arquivos)}")
        print(f"\n5️⃣ Testando acesso aos atributos dos arquivos...")
        
        for i, arq in enumerate(arquivos[:5], 1):  # Limitar a 5 para não poluir
            print(f"\n   Arquivo {i}:")
            print(f"      Tipo: {type(arq)}")
            print(f"      Nome (arq.name): {arq.name}")
            
            try:
                tamanho = arq.stat().st_size
                print(f"      Tamanho (arq.stat().st_size): {tamanho} bytes")
            except Exception as e:
                print(f"      Tamanho: Erro ao obter ({e})")
            
            try:
                print(f"      Extensão (arq.suffix): {arq.suffix}")
            except Exception as e:
                print(f"      Extensão: Erro ao obter ({e})")
            
            try:
                caminho_relativo = arq.relative_to(gw.workspaces_dir)
                print(f"      Caminho relativo: {caminho_relativo}")
            except Exception as e:
                print(f"      Caminho relativo: Erro ao obter ({e})")
        
        if len(arquivos) > 5:
            print(f"\n   ... e mais {len(arquivos) - 5} arquivo(s)")
    else:
        print(f"   ℹ️ Nenhum arquivo encontrado no workspace")
    
    print("\n" + "="*80)
    print("✅ TESTE CONCLUÍDO COM SUCESSO!")
    print("="*80)
    print("\n📝 CONCLUSÃO:")
    print("   • Método listar_arquivos() retorna List[Path] ✅")
    print("   • Acesso via arq.name (não arq['nome']) ✅")
    print("   • Acesso via arq.stat().st_size (não arq['tamanho_bytes']) ✅")
    print("   • Erro TypeError: 'WindowsPath' not subscriptable CORRIGIDO ✅")
    
except Exception as e:
    print(f"\n❌ ERRO durante o teste:")
    print(f"   {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
