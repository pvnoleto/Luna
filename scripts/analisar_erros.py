#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para analisar erros no arquivo luna_v3_TIER2_COMPLETO.py"""

import re
import sys

def analisar_arquivo(caminho):
    """Analisa o arquivo em busca de erros comuns"""
    
    print(f"🔍 Analisando: {caminho}\n")
    
    erros_encontrados = []
    
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            linhas = conteudo.split('\n')
        
        # 1. Procurar por "Fals" sem "e" no final (False)
        for i, linha in enumerate(linhas, 1):
            if re.search(r'\bFals\s', linha):
                erros_encontrados.append(f"Linha {i}: 'Fals' encontrado (deveria ser 'False')")
        
        # 2. Verificar se SistemaFerramentasCompleto está implementado
        if 'pass  # Adicionar ferramentas básicas' in conteudo:
            erros_encontrados.append("SistemaFerramentasCompleto._carregar_ferramentas_base() está vazio (apenas 'pass')")
        
        # 3. Procurar por imports não utilizados ou faltando
        has_import_playwright = 'from playwright' in conteudo
        uses_playwright = '_playwright' in conteudo or 'playwright' in conteudo.lower()
        
        # 4. Verificar se load_dotenv é chamado
        if 'load_dotenv()' not in conteudo:
            erros_encontrados.append("load_dotenv() não é chamado no código")
        
        # 5. Procurar por funções incompletas
        pattern_def = re.compile(r'def\s+(\w+)\s*\([^)]*\):')
        pattern_pass_only = re.compile(r'def\s+\w+\s*\([^)]*\):\s*\n\s*"""[^"]*"""\s*\n\s*pass\s*\n')
        
        funcoes_incompletas = pattern_pass_only.findall(conteudo)
        if funcoes_incompletas:
            erros_encontrados.append(f"Encontradas {len(funcoes_incompletas)} funções com apenas 'pass'")
        
        # 6. Verificar sintaxe básica Python
        try:
            compile(conteudo, caminho, 'exec')
            print("✅ Sintaxe Python válida\n")
        except SyntaxError as e:
            erros_encontrados.append(f"ERRO DE SINTAXE na linha {e.lineno}: {e.msg}")
        
        # Exibir erros
        if erros_encontrados:
            print("❌ ERROS ENCONTRADOS:\n")
            for erro in erros_encontrados:
                print(f"   • {erro}")
            print(f"\n📊 Total: {len(erros_encontrados)} erro(s)")
        else:
            print("✅ Nenhum erro crítico encontrado!")
        
        return erros_encontrados
        
    except Exception as e:
        print(f"❌ Erro ao analisar arquivo: {e}")
        import traceback
        traceback.print_exc()
        return [str(e)]


if __name__ == "__main__":
    caminho = "C:\\Users\\Pedro Victor\\OneDrive\\Área de Trabalho\\Documentos\\Projetos Automações e Digitais\\Luna\\luna_v3_TIER2_COMPLETO.py"
    
    erros = analisar_arquivo(caminho)
    
    sys.exit(0 if not erros else 1)
