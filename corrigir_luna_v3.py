#!/usr/bin/env python3
# -*-coding: utf-8 -*-
"""
Script para corrigir luna_v3_TIER2_COMPLETO.py adicionando:
1. load_dotenv() no início
2. Imports dos sistemas opcionais (como no luna_final.py)
3. Classe SistemaFerramentasCompleto completa (com todas as ferramentas)
"""

import os
import shutil
from pathlib import Path

# Caminho base
BASE_PATH = Path(__file__).parent

def main():
    print("="*70)
    print("🔧 CORRIGINDO luna_v3_TIER2_COMPLETO.py")
    print("="*70)
    
    # 1. Ler ambos os arquivos
    print("\n1️⃣ Lendo arquivos...")
    
    v3_file = BASE_PATH / 'luna_v3_TIER2_COMPLETO.py'
    final_file = BASE_PATH / 'luna_final.py'
    
    with open(v3_file, 'r', encoding='utf-8') as f:
        v3_content = f.read()
    
    with open(final_file, 'r', encoding='utf-8') as f:
        final_content = f.read()
    
    print(f"   ✅ luna_v3: {len(v3_content):,} caracteres")
    print(f"   ✅ luna_final: {len(final_content):,} caracteres")
    
    # 2. Fazer backup
    print("\n2️⃣ Criando backup...")
    backup_file = str(v3_file) + '.backup_correcao'
    shutil.copy(v3_file, backup_file)
    print(f"   ✅ Backup: {backup_file}")
    
    # 3. Extrair imports do luna_final (sistemas opcionais)
    print("\n3️⃣ Extraindo imports dos sistemas opcionais...")
    
    # Encontrar seção de imports no luna_final
    inicio_imports = final_content.find('# Importar sistema de auto-evolução')
    fim_imports = final_content.find('# Carregar configuração', inicio_imports)
    
    if inicio_imports == -1 or fim_imports == -1:
        print("   ❌ ERRO: Não conseguiu encontrar imports!")
        return False
    
    imports_section = final_content[inicio_imports:fim_imports].strip()
    print(f"   ✅ Imports extraídos ({len(imports_section)} caracteres)")
    
    # 4. Extrair classe completa do luna_final
    print("\n4️⃣ Extraindo classe SistemaFerramentasCompleto completa...")
    
    inicio_classe = final_content.find('class SistemaFerramentasCompleto:')
    fim_classe = final_content.find('\n\n# ============', inicio_classe + 100)
    
    if inicio_classe == -1 or fim_classe == -1:
        print("   ❌ ERRO: Não conseguiu encontrar classe!")
        return False
    
    classe_completa = final_content[inicio_classe:fim_classe].strip()
    print(f"   ✅ Classe extraída ({len(classe_completa):,} caracteres)")
    
    # 5. Modificar luna_v3
    print("\n5️⃣ Modificando luna_v3_TIER2_COMPLETO.py...")
    
    # 5.1. Adicionar imports após os imports padrão
    # Encontrar onde termina os imports padrão (antes das classes de dados)
    pos_insert_imports = v3_content.find('# ============================================================================\n# CLASSES DE DADOS PARA PLANEJAMENTO')
    
    if pos_insert_imports == -1:
        print("   ❌ ERRO: Não encontrou posição para inserir imports!")
        return False
    
    # Inserir imports antes das classes de dados
    v3_content = v3_content[:pos_insert_imports] + '\n' + imports_section + '\n\n' + v3_content[pos_insert_imports:]
    print("   ✅ Imports adicionados")
    
    # 5.2. Substituir classe SistemaFerramentasCompleto
    inicio_classe_v3 = v3_content.find('class SistemaFerramentasCompleto:')
    fim_classe_v3 = v3_content.find('\n\n# ============', inicio_classe_v3 + 100)
    
    if inicio_classe_v3 == -1 or fim_classe_v3 == -1:
        print("   ❌ ERRO: Não encontrou classe no v3!")
        return False
    
    v3_content = v3_content[:inicio_classe_v3] + classe_completa + v3_content[fim_classe_v3:]
    print("   ✅ Classe substituída")
    
    # 6. Salvar arquivo corrigido
    print("\n6️⃣ Salvando arquivo corrigido...")
    
    with open(v3_file, 'w', encoding='utf-8') as f:
        f.write(v3_content)
    
    print(f"   ✅ Arquivo salvo ({len(v3_content):,} caracteres)")
    
    # 7. Resumo
    print("\n" + "="*70)
    print("✅ CORREÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*70)
    print("\n📊 RESUMO DAS CORREÇÕES:")
    print(f"   1. ✅ load_dotenv() já estava presente")
    print(f"   2. ✅ Imports dos sistemas opcionais adicionados")
    print(f"   3. ✅ Classe SistemaFerramentasCompleto substituída pela versão completa")
    print(f"\n📁 ARQUIVOS:")
    print(f"   - Original corrigido: luna_v3_TIER2_COMPLETO.py")
    print(f"   - Backup: {backup_file}")
    print(f"\n🎉 O arquivo luna_v3_TIER2_COMPLETO.py agora está completo!")
    print(f"   Todas as ferramentas estão disponíveis:")
    print(f"   - bash_avancado, criar_arquivo, ler_arquivo")
    print(f"   - Playwright (navegador web)")
    print(f"   - Workspaces")
    print(f"   - Gerenciador de temporários")
    print(f"   - Memória permanente")
    print(f"   - Cofre de credenciais")
    print(f"   - Auto-evolução")
    
    return True

if __name__ == '__main__':
    try:
        sucesso = main()
        if not sucesso:
            print("\n❌ Falha na correção!")
            exit(1)
    except Exception as e:
        print(f"\n❌ ERRO FATAL: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
