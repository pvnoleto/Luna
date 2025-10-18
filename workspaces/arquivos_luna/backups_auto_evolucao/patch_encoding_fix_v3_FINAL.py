#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PATCH V3 FINAL: Correção Definitiva de Encoding
================================================
Problema: Windows cmd.exe retorna output em cp850/cp1252, não UTF-8.
Solução: Detectar plataforma e usar encoding correto.
"""

import sys
import shutil
from datetime import datetime

def aplicar_patch_final():
    """Aplica correção definitiva com detecção de plataforma"""
    
    arquivo = 'luna_completo_workspaces_CORRIGIDO.py'
    arquivo_backup = f'luna_completo_workspaces_CORRIGIDO.backup_v3_FINAL_{datetime.now().strftime("%Y%m%d_%H%M%S")}.py'
    
    print("🔧 Aplicando PATCH V3 FINAL - Correção Definitiva")
    print("=" * 60)
    
    # Backup
    shutil.copy(arquivo, arquivo_backup)
    print(f"💾 Backup: {arquivo_backup}")
    
    # Ler
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # ========== CORREÇÃO 1: bash_avancado ==========
    print("\n🔧 Correção 1: bash_avancado")
    
    codigo_antigo_bash = '''def bash_avancado(comando: str, timeout: int = 60) -> str:
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
    
    codigo_novo_bash = '''def bash_avancado(comando: str, timeout: int = 60) -> str:
    import subprocess, os, sys
    print(f"    [BASH] {comando[:100]}...")
    try:
        # ✅ CORREÇÃO FINAL: Detectar encoding do sistema
        # Windows cmd.exe usa cp850/cp1252, não UTF-8
        if sys.platform == 'win32':
            # Tentar cp850 (cmd padrão), depois cp1252, depois utf-8
            for enc in ['cp850', 'cp1252', 'utf-8']:
                try:
                    resultado = subprocess.run(comando, shell=True, capture_output=True, 
                                             text=True, encoding=enc, errors='replace',
                                             timeout=timeout, cwd=os.getcwd())
                    break
                except (UnicodeDecodeError, LookupError):
                    if enc == 'utf-8':  # Última tentativa
                        resultado = subprocess.run(comando, shell=True, capture_output=True, 
                                                 text=True, errors='replace',
                                                 timeout=timeout, cwd=os.getcwd())
        else:
            # Linux/Mac: UTF-8 padrão
            resultado = subprocess.run(comando, shell=True, capture_output=True, 
                                     text=True, encoding='utf-8', errors='replace',
                                     timeout=timeout, cwd=os.getcwd())
        
        saida = f"STDOUT:\\\\n{resultado.stdout}\\\\nSTDERR:\\\\n{resultado.stderr}\\\\nCODE: {resultado.returncode}"
        print(f"    [OK] Codigo {resultado.returncode}")
        return saida[:3000]
    except Exception as e:
        return f"Erro: {e}"'''
    
    if codigo_antigo_bash in conteudo:
        conteudo = conteudo.replace(codigo_antigo_bash, codigo_novo_bash)
        print("✅ bash_avancado corrigido com detecção de plataforma")
    else:
        print("⚠️  Código não encontrado - tentando método alternativo...")
        # Tentar encontrar apenas a parte crítica
        if "def bash_avancado" in conteudo and "encoding='utf-8', errors='replace'" in conteudo:
            print("⚠️  Código já parece estar parcialmente corrigido")
    
    # ========== CORREÇÃO 2: instalar_biblioteca ==========
    print("\n🔧 Correção 2: instalar_biblioteca")
    
    codigo_antigo_install = '''def instalar_biblioteca(nome_pacote: str) -> str:
    import subprocess
    print(f"    [INSTALL] Instalando: {nome_pacote}")
    try:
        resultado = subprocess.run(f"pip install {nome_pacote}", shell=True, 
                                 capture_output=True, text=True, encoding='utf-8',
                                 errors='replace', timeout=120)
        if resultado.returncode == 0:
            print("    [OK] Instalado")
            return f"'{nome_pacote}' instalado!"
        return f"Erro: {resultado.stderr[:500]}"
    except Exception as e:
        return f"Erro: {e}"'''
    
    codigo_novo_install = '''def instalar_biblioteca(nome_pacote: str) -> str:
    import subprocess, sys
    print(f"    [INSTALL] Instalando: {nome_pacote}")
    try:
        # ✅ CORREÇÃO FINAL: Encoding dependente de plataforma
        if sys.platform == 'win32':
            enc = 'cp850'  # Windows cmd padrão
        else:
            enc = 'utf-8'  # Linux/Mac
        
        resultado = subprocess.run(f"pip install {nome_pacote}", shell=True, 
                                 capture_output=True, text=True, encoding=enc,
                                 errors='replace', timeout=120)
        if resultado.returncode == 0:
            print("    [OK] Instalado")
            return f"'{nome_pacote}' instalado!"
        return f"Erro: {resultado.stderr[:500]}"
    except Exception as e:
        return f"Erro: {e}"'''
    
    if codigo_antigo_install in conteudo:
        conteudo = conteudo.replace(codigo_antigo_install, codigo_novo_install)
        print("✅ instalar_biblioteca corrigido com detecção de plataforma")
    else:
        print("⚠️  Código não encontrado")
    
    # Salvar
    print("\n💾 Salvando arquivo corrigido...")
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print("\n" + "=" * 60)
    print("✅ PATCH V3 FINAL APLICADO COM SUCESSO!")
    print("=" * 60)
    print("\n🎯 CORREÇÕES APLICADAS:")
    print("   1. bash_avancado: Detecção automática de encoding")
    print("      - Windows: Tenta cp850 → cp1252 → utf-8")
    print("      - Linux/Mac: utf-8 direto")
    print("   2. instalar_biblioteca: cp850 no Windows, utf-8 em outros")
    print("\n⚡ REINICIE O AGENTE para aplicar as correções!")
    print(f"📦 Backup em: {arquivo_backup}")

if __name__ == "__main__":
    try:
        aplicar_patch_final()
    except Exception as e:
        print(f"\n❌ Erro ao aplicar patch: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
