#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PATCH V2: Correção de Encoding para instalar_biblioteca
========================================================
"""

import sys
import shutil
from datetime import datetime

def aplicar_patch_instalar_biblioteca():
    """Corrige encoding na função instalar_biblioteca"""
    
    arquivo = 'luna_completo_workspaces_CORRIGIDO.py'
    arquivo_backup = f'luna_completo_workspaces_CORRIGIDO.backup_v2_{datetime.now().strftime("%Y%m%d_%H%M%S")}.py'
    
    print("🔧 Aplicando patch V2 para instalar_biblioteca...")
    
    # Backup
    shutil.copy(arquivo, arquivo_backup)
    print(f"💾 Backup: {arquivo_backup}")
    
    # Ler
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Patch específico para a linha 744-745
    codigo_antigo = '''resultado = subprocess.run(f"pip install {nome_pacote}", shell=True, 
                                 capture_output=True, text=True, timeout=120)'''
    
    codigo_novo = '''resultado = subprocess.run(f"pip install {nome_pacote}", shell=True, 
                                 capture_output=True, text=True, encoding='utf-8',
                                 errors='replace', timeout=120)'''
    
    if codigo_antigo in conteudo:
        conteudo = conteudo.replace(codigo_antigo, codigo_novo)
        print("✅ Correção aplicada: instalar_biblioteca com encoding='utf-8'")
        
        # Salvar
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        
        print("✅ Patch V2 aplicado com sucesso!")
        print("⚡ Reinicie o agente para usar as correções!")
    else:
        print("⚠️  Código não encontrado (pode já estar corrigido)")

if __name__ == "__main__":
    try:
        aplicar_patch_instalar_biblioteca()
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
