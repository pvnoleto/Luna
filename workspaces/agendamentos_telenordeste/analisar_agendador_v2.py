#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
import re

# Forçar UTF-8 no stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def analisar_arquivo_python(caminho):
    """Analisa um arquivo Python e extrai informações estruturais."""
    
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            conteudo = f.read()
    except:
        with open(caminho, 'r', encoding='latin-1') as f:
            conteudo = f.read()
    
    print("=" * 80)
    print("ANALISE DO ARQUIVO: agendador_final_corrigido.py")
    print("=" * 80)
    
    # Estatísticas básicas
    linhas = conteudo.split('\n')
    print(f"\nESTATISTICAS:")
    print(f"   - Total de linhas: {len(linhas)}")
    print(f"   - Total de caracteres: {len(conteudo)}")
    
    # Extrair imports
    print(f"\nBIBLIOTECAS IMPORTADAS:")
    imports = re.findall(r'^(?:from|import)\s+([a-zA-Z0-9_\.]+)', conteudo, re.MULTILINE)
    for imp in sorted(set(imports)):
        print(f"   - {imp}")
    
    # Extrair funções definidas
    print(f"\nFUNCOES DEFINIDAS ({len(set(re.findall(r'^def\s+([a-zA-Z0-9_]+)', conteudo, re.MULTILINE)))}):")
    funcoes = re.findall(r'^def\s+([a-zA-Z0-9_]+)\s*\([^)]*\)', conteudo, re.MULTILINE)
    for i, func in enumerate(funcoes[:30], 1):  # Primeiras 30
        print(f"   {i}. {func}")
    if len(funcoes) > 30:
        print(f"   ... e mais {len(funcoes)-30} funcoes")
    
    # Extrair classes
    print(f"\nCLASSES DEFINIDAS:")
    classes = re.findall(r'^class\s+([a-zA-Z0-9_]+)', conteudo, re.MULTILINE)
    if classes:
        for classe in classes:
            print(f"   - {classe}")
    else:
        print("   (Nenhuma classe definida)")
    
    # Buscar integrações principais
    print(f"\nINTEGRACOES IDENTIFICADAS:")
    
    integracoes = {
        "Notion API": ["notion", "NOTION", "Client", "DATABASE_ID", "database"],
        "Google Calendar": ["google", "calendar", "googleapiclient", "Calendar API", "build("],
        "Playwright": ["playwright", "chromium", "async_playwright", "browser", "page.goto"],
        "Selenium": ["selenium", "webdriver", "driver"],
    }
    
    for nome, keywords in integracoes.items():
        encontrado = any(keyword in conteudo for keyword in keywords)
        if encontrado:
            print(f"   [OK] {nome}")
            # Encontrar linhas relacionadas
            total_refs = 0
            for keyword in keywords:
                count = conteudo.count(keyword)
                total_refs += count
            if total_refs > 0 and total_refs < 200:
                print(f"        -> {total_refs} referencias no codigo")
    
    # Buscar variáveis de configuração/ambiente
    print(f"\nVARIAVEIS DE AMBIENTE/CONFIG:")
    env_vars = re.findall(r'([A-Z_]{4,})\s*=', conteudo)
    for var in sorted(set(env_vars[:15])):  # Limitar a 15
        if len(var) > 3:
            print(f"   - {var}")
    
    # Buscar URLs e endpoints
    print(f"\nURLs/ENDPOINTS IDENTIFICADOS:")
    urls = re.findall(r'https?://[^\s\'"<>]+', conteudo)
    for url in sorted(set(urls[:10])):  # Primeiras 10 URLs únicas
        print(f"   - {url}")
    
    # Buscar docstrings de módulo
    print(f"\nDOCSTRING DO MODULO:")
    docstring_match = re.search(r'^"""(.*?)"""', conteudo, re.MULTILINE | re.DOTALL)
    if docstring_match:
        doc = docstring_match.group(1).strip()
        for linha in doc.split('\n')[:10]:  # Primeiras 10 linhas
            print(f"   {linha}")
    
    # Análise de estrutura lógica
    print(f"\nESTRUTURAS LOGICAS:")
    print(f"   - Loops 'for': {conteudo.count('for ')}")
    print(f"   - Loops 'while': {conteudo.count('while ')}")
    print(f"   - Condicionais 'if': {conteudo.count('if ')}")
    print(f"   - Try/Except: {conteudo.count('try:')}")
    print(f"   - Funcoes async: {conteudo.count('async def')}")
    
    # Buscar padrões de automação web
    print(f"\nPADROES DE AUTOMACAO WEB:")
    padroes_web = {
        "Navegacao": ["goto", "navigate", ".get("],
        "Cliques": ["click(", ".click", "click_button"],
        "Preenchimento": ["fill(", "send_keys", "type("],
        "Espera": ["wait_for", "sleep(", "timeout", "wait("],
        "Seletores": ["querySelector", "xpath", "css=", "text=", "id=", "selector"],
        "Screenshots": ["screenshot", "capture"],
    }
    
    for categoria, keywords in padroes_web.items():
        count = sum(conteudo.count(kw) for kw in keywords)
        if count > 0:
            print(f"   - {categoria}: {count} ocorrencias")
    
    # Buscar funções principais do fluxo
    print(f"\nFLUXO PRINCIPAL - Funcoes de Alto Nivel:")
    funcoes_principais = [
        "main", "processar", "agendar", "executar", "iniciar",
        "conectar", "buscar", "verificar", "atualizar", "criar"
    ]
    
    for func in funcoes_principais:
        matches = re.findall(rf'^def\s+({func}[a-zA-Z0-9_]*)\s*\(', conteudo, re.MULTILINE)
        if matches:
            for match in matches:
                print(f"   -> {match}()")
    
    print("\n" + "=" * 80)
    
    # Análise detalhada do fluxo
    print("\nANALISE DETALHADA DO FLUXO:")
    print("=" * 80)
    
    # Procurar função main ou similar
    main_funcs = re.findall(r'def\s+(main|executar_agendamento|processar_agendamento)[^:]*:\s*"""(.*?)"""', 
                           conteudo, re.DOTALL)
    
    if main_funcs:
        for func_name, docstring in main_funcs:
            print(f"\nFuncao principal: {func_name}()")
            print(f"Documentacao:")
            for linha in docstring.strip().split('\n')[:10]:
                print(f"   {linha.strip()}")
    
    # Buscar sequência de operações
    print(f"\nSEQUENCIA DE OPERACOES (baseada em comentarios e funcoes):")
    
    # Extrair seções comentadas
    secoes = re.findall(r'#\s*((?:PASSO|ETAPA|FASE|Passo|Etapa).*?)$', conteudo, re.MULTILINE)
    if secoes:
        for i, secao in enumerate(secoes[:20], 1):
            print(f"   {i}. {secao.strip()}")
    
    # Buscar chamadas de funções principais em sequência
    print(f"\nCHAMADAS DE FUNCOES CHAVE:")
    chamadas_importantes = re.findall(r'^\s{4,}(\w+\([^)]*\))', conteudo, re.MULTILINE)
    funcoes_filtradas = [c for c in chamadas_importantes if any(x in c for x in 
        ['conectar', 'buscar', 'agendar', 'verificar', 'processar', 'criar', 'atualizar', 'log_'])]
    
    for i, chamada in enumerate(funcoes_filtradas[:25], 1):
        if len(chamada) > 70:
            chamada = chamada[:67] + "..."
        print(f"   {i}. {chamada}")
    
    print("\n" + "=" * 80)
    print("FIM DA ANALISE")
    print("=" * 80)
    
    return conteudo

if __name__ == "__main__":
    caminho = r"C:\Users\Pedro Victor\OneDrive\Área de Trabalho\Documentos\Projetos Automações e Digitais\Luna\agendador_final_corrigido.py"
    
    try:
        conteudo = analisar_arquivo_python(caminho)
        
        # Salvar resumo
        print("\nSalvando resumo da analise...")
        with open("RESUMO_AGENDADOR.md", "w", encoding="utf-8") as f:
            f.write("# RESUMO DO BOT DE AGENDAMENTO\n\n")
            f.write("## Arquivo Analisado\n")
            f.write("agendador_final_corrigido.py\n\n")
            f.write("## Funcionalidade Principal\n")
            f.write("Bot de agendamento automatico que integra:\n")
            f.write("- Notion API (extrai tarefas)\n")
            f.write("- Google Calendar (verifica disponibilidade)\n")
            f.write("- Playwright (automacao web no site Telenordeste)\n\n")
            f.write(f"## Estatisticas\n")
            f.write(f"- Linhas: {len(conteudo.split(chr(10)))}\n")
            f.write(f"- Caracteres: {len(conteudo)}\n")
            
        print("OK - Analise salva em: RESUMO_AGENDADOR.md")
        
    except Exception as e:
        print(f"ERRO: {e}")
        import traceback
        traceback.print_exc()
