#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PATCH: Correção de Encoding para bash_avancado e instalar_biblioteca
=====================================================================
Corrige o problema de encoding UTF-8 no Windows
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime

def aplicar_patch():
    """Aplica correções de encoding no arquivo principal"""
    
    arquivo_original = 'luna_completo_workspaces_CORRIGIDO.py'
    arquivo_backup = f'luna_completo_workspaces_CORRIGIDO.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.py'
    
    print("🔧 Aplicando patch de encoding...")
    print(f"📄 Arquivo: {arquivo_original}")
    
    # Fazer backup
    shutil.copy(arquivo_original, arquivo_backup)
    print(f"💾 Backup criado: {arquivo_backup}")
    
    # Ler conteúdo
    with open(arquivo_original, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Correção 1: bash_avancado - adicionar encoding='utf-8'
    codigo_antigo_bash = '''def bash_avancado(comando: str, timeout: int = 60) -> str:
    import subprocess, os
    print(f"    [BASH] {comando[:100]}...")
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, 
                                 text=True, timeout=timeout, cwd=os.getcwd())
        saida = f"STDOUT:\\\\n{resultado.stdout}\\\\nSTDERR:\\\\n{resultado.stderr}\\\\nCODE: {resultado.returncode}"
        print(f"    [OK] Codigo {resultado.returncode}")
        return saida[:3000]
    except Exception as e:
        return f"Erro: {e}"'''
    
    codigo_novo_bash = '''def bash_avancado(comando: str, timeout: int = 60) -> str:
    import subprocess, os
    print(f"    [BASH] {comando[:100]}...")
    try:
        # ✅ CORREÇÃO: Encoding UTF-8 explícito para Windows
        resultado = subprocess.run(comando, shell=True, capture_output=True, 
                                 text=True, encoding='utf-8', errors='replace',
                                 timeout=timeout, cwd=os.getcwd())
        saida = f"STDOUT:\\\\n{resultado.stdout}\\\\nSTDERR:\\\\n{resultado.stderr}\\\\nCODE: {resultado.returncode}"
        print(f"    [OK] Codigo {resultado.returncode}")
        return saida[:3000]
    except Exception as e:
        return f"Erro: {e}"'''
    
    # Aplicar correção 1
    if codigo_antigo_bash in conteudo:
        conteudo = conteudo.replace(codigo_antigo_bash, codigo_novo_bash)
        print("✅ Correção 1 aplicada: bash_avancado com encoding='utf-8'")
    else:
        print("⚠️  Correção 1 não aplicada: código não encontrado (pode já estar corrigido)")
    
    # Correção 2: instalar_biblioteca - adicionar encoding='utf-8'
    codigo_antigo_install = '''def instalar_biblioteca(nome_pacote: str) -> str:
    import subprocess
    print(f"    [INSTALL] {nome_pacote}")
    try:
        resultado = subprocess.run([sys.executable, "-m", "pip", "install", nome_pacote],
                                 capture_output=True, text=True, timeout=120)
        if resultado.returncode == 0:
            return f"'{nome_pacote}' instalado!"
        else:
            return f"Erro ao instalar '{nome_pacote}': {resultado.stderr}"
    except Exception as e:
        return f"Erro: {e}"'''
    
    codigo_novo_install = '''def instalar_biblioteca(nome_pacote: str) -> str:
    import subprocess
    print(f"    [INSTALL] {nome_pacote}")
    try:
        # ✅ CORREÇÃO: Encoding UTF-8 explícito para Windows
        resultado = subprocess.run([sys.executable, "-m", "pip", "install", nome_pacote],
                                 capture_output=True, text=True, encoding='utf-8', 
                                 errors='replace', timeout=120)
        if resultado.returncode == 0:
            return f"'{nome_pacote}' instalado!"
        else:
            return f"Erro ao instalar '{nome_pacote}': {resultado.stderr}"
    except Exception as e:
        return f"Erro: {e}"'''
    
    # Aplicar correção 2
    if codigo_antigo_install in conteudo:
        conteudo = conteudo.replace(codigo_antigo_install, codigo_novo_install)
        print("✅ Correção 2 aplicada: instalar_biblioteca com encoding='utf-8'")
    else:
        print("⚠️  Correção 2 não aplicada: código não encontrado (pode já estar corrigido)")
    
    # Salvar arquivo corrigido
    with open(arquivo_original, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print(f"\n✅ Patch aplicado com sucesso!")
    print(f"📦 Backup disponível em: {arquivo_backup}")
    print("\n🎯 CORREÇÕES APLICADAS:")
    print("   1. bash_avancado: encoding='utf-8', errors='replace'")
    print("   2. instalar_biblioteca: encoding='utf-8', errors='replace'")
    print("\n⚡ Reinicie o agente para usar as correções!")

if __name__ == "__main__":
    try:
        aplicar_patch()
    except Exception as e:
        print(f"\n❌ Erro ao aplicar patch: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
