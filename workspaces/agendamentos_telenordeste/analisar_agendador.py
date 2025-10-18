#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import ast

def analisar_arquivo_python(caminho):
    """Analisa um arquivo Python e extrai informações estruturais."""
    
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            conteudo = f.read()
    except:
        with open(caminho, 'r', encoding='latin-1') as f:
            conteudo = f.read()
    
    print("=" * 80)
    print("ANÁLISE DO ARQUIVO: agendador_final_corrigido.py")
    print("=" * 80)
    
    # Estatísticas básicas
    linhas = conteudo.split('\n')
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   - Total de linhas: {len(linhas)}")
    print(f"   - Total de caracteres: {len(conteudo)}")
    
    # Extrair imports
    print(f"\n📦 BIBLIOTECAS IMPORTADAS:")
    imports = re.findall(r'^(?:from|import)\s+([a-zA-Z0-9_\.]+)', conteudo, re.MULTILINE)
    for imp in sorted(set(imports)):
        print(f"   - {imp}")
    
    # Extrair funções definidas
    print(f"\n🔧 FUNÇÕES DEFINIDAS:")
    funcoes = re.findall(r'^def\s+([a-zA-Z0-9_]+)\s*\([^)]*\)', conteudo, re.MULTILINE)
    for i, func in enumerate(funcoes, 1):
        print(f"   {i}. {func}")
    
    # Extrair classes
    print(f"\n🏗️ CLASSES DEFINIDAS:")
    classes = re.findall(r'^class\s+([a-zA-Z0-9_]+)', conteudo, re.MULTILINE)
    if classes:
        for classe in classes:
            print(f"   - {classe}")
    else:
        print("   (Nenhuma classe definida)")
    
    # Buscar integrações principais
    print(f"\n🔌 INTEGRAÇÕES IDENTIFICADAS:")
    
    integracoes = {
        "Notion": ["notion", "NOTION", "Client", "DATABASE_ID"],
        "Google Calendar": ["google", "calendar", "googleapiclient", "Calendar API"],
        "Playwright": ["playwright", "chromium", "browser", "page."],
        "Selenium": ["selenium", "webdriver", "driver"],
    }
    
    for nome, keywords in integracoes.items():
        encontrado = any(keyword in conteudo for keyword in keywords)
        if encontrado:
            print(f"   ✅ {nome}")
            # Encontrar linhas relacionadas
            for keyword in keywords:
                if keyword in conteudo:
                    count = conteudo.count(keyword)
                    if count > 0 and count < 50:
                        print(f"      → '{keyword}' usado {count}x")
    
    # Buscar variáveis de configuração/ambiente
    print(f"\n🔑 VARIÁVEIS DE AMBIENTE/CONFIG:")
    env_vars = re.findall(r'[A-Z_]{3,}\s*=\s*(?:os\.getenv|os\.environ)', conteudo)
    env_vars += re.findall(r'([A-Z_]{5,})\s*=\s*["\']', conteudo)
    for var in sorted(set(env_vars[:10])):  # Limitar a 10
        print(f"   - {var}")
    
    # Buscar URLs e endpoints
    print(f"\n🌐 URLs/ENDPOINTS IDENTIFICADOS:")
    urls = re.findall(r'https?://[^\s\'"]+', conteudo)
    for url in sorted(set(urls[:10])):  # Primeiras 10 URLs únicas
        print(f"   - {url}")
    
    # Buscar comentários de seção/documentação principal
    print(f"\n📝 SEÇÕES/COMENTÁRIOS PRINCIPAIS:")
    comentarios_importantes = re.findall(r'#\s*={3,}.*?={3,}|#\s*[A-Z][A-Z\s]{10,}', conteudo)
    for i, com in enumerate(comentarios_importantes[:15], 1):  # Primeiros 15
        print(f"   {i}. {com.strip()}")
    
    # Buscar docstrings de módulo
    print(f"\n📖 DOCSTRING DO MÓDULO:")
    docstring_match = re.search(r'^"""(.*?)"""', conteudo, re.MULTILINE | re.DOTALL)
    if docstring_match:
        doc = docstring_match.group(1).strip()
        for linha in doc.split('\n')[:5]:  # Primeiras 5 linhas
            print(f"   {linha}")
    
    # Fluxo principal (main)
    print(f"\n🚀 FLUXO PRINCIPAL (if __name__ == '__main__'):")
    main_match = re.search(r'if __name__\s*==\s*[\'"]__main__[\'"]:(.*?)(?=\n(?:def|class|if __name__|$))', 
                          conteudo, re.DOTALL)
    if main_match:
        main_code = main_match.group(1)
        linhas_main = [l.strip() for l in main_code.split('\n') if l.strip() and not l.strip().startswith('#')]
        print("   Passos identificados:")
        for i, linha in enumerate(linhas_main[:20], 1):  # Primeiros 20 passos
            if len(linha) > 80:
                linha = linha[:77] + "..."
            print(f"   {i}. {linha}")
    
    # Análise de estrutura lógica
    print(f"\n🧠 ESTRUTURAS LÓGICAS:")
    print(f"   - Loops 'for': {conteudo.count('for ')}")
    print(f"   - Loops 'while': {conteudo.count('while ')}")
    print(f"   - Condicionais 'if': {conteudo.count('if ')}")
    print(f"   - Try/Except: {conteudo.count('try:')}")
    print(f"   - Funções async: {conteudo.count('async def')}")
    
    # Buscar padrões de automação web
    print(f"\n🤖 PADRÕES DE AUTOMAÇÃO WEB:")
    padroes_web = {
        "Navegação": ["goto", "navigate", "get(", "open("],
        "Cliques": ["click(", ".click", "click_button"],
        "Preenchimento": ["fill(", "send_keys", "type(", "input"],
        "Espera": ["wait", "sleep", "timeout", "delay"],
        "Seletores": ["querySelector", "xpath", "css=", "text=", "id="],
        "Screenshots": ["screenshot", "capture", "snap"],
    }
    
    for categoria, keywords in padroes_web.items():
        count = sum(conteudo.count(kw) for kw in keywords)
        if count > 0:
            print(f"   - {categoria}: {count} ocorrências")
    
    print("\n" + "=" * 80)
    print("FIM DA ANÁLISE")
    print("=" * 80)
    
    return conteudo

if __name__ == "__main__":
    caminho = r"C:\Users\Pedro Victor\OneDrive\Área de Trabalho\Documentos\Projetos Automações e Digitais\Luna\agendador_final_corrigido.py"
    conteudo = analisar_arquivo_python(caminho)
    
    # Salvar uma versão legível
    print("\n💾 Salvando análise em arquivo...")
    with open("analise_agendador.txt", "w", encoding="utf-8") as f:
        f.write(conteudo)
    print("✅ Análise salva em: analise_agendador.txt")
