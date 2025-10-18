# -*- coding: utf-8 -*-
import re

# Ler arquivo
with open(r"C:\Users\Pedro Victor\OneDrive\Área de Trabalho\Documentos\Projetos Automações e Digitais\Luna\agendador_final_corrigido.py", 'r', encoding='utf-8') as f:
    conteudo = f.read()

# Criar análise
analise = []
analise.append("# ANÁLISE COMPLETA: agendador_final_corrigido.py\n")
analise.append("=" * 80 + "\n\n")

# Docstring principal
docstring = re.search(r'^"""(.*?)"""', conteudo, re.MULTILINE | re.DOTALL)
if docstring:
    analise.append("## DESCRIÇÃO DO ARQUIVO\n")
    analise.append(docstring.group(1).strip() + "\n\n")

# Estatísticas
linhas = conteudo.split('\n')
analise.append("## ESTATÍSTICAS\n")
analise.append(f"- **Total de linhas**: {len(linhas)}\n")
analise.append(f"- **Tamanho**: {len(conteudo):,} caracteres\n")
analise.append(f"- **Funções definidas**: {conteudo.count('def ')}\n")
analise.append(f"- **Classes**: {conteudo.count('class ')}\n\n")

# Imports
analise.append("## BIBLIOTECAS E DEPENDÊNCIAS\n\n")
imports = re.findall(r'^((?:from|import)\s+.*?)$', conteudo, re.MULTILINE)
analise.append("```python\n")
for imp in imports[:20]:
    analise.append(imp + "\n")
analise.append("```\n\n")

# Funções
analise.append("## FUNÇÕES PRINCIPAIS\n\n")
funcoes_completas = re.findall(r'^def\s+([a-zA-Z0-9_]+)\s*\([^)]*\):\s*(?:"""(.*?)"""|\'\'\'(.*?)\'\'\')?', 
                               conteudo, re.MULTILINE | re.DOTALL)

for i, (nome, doc1, doc2) in enumerate(funcoes_completas, 1):
    doc = doc1 or doc2 or ""
    analise.append(f"### {i}. `{nome}()`\n")
    if doc:
        primeira_linha = doc.strip().split('\n')[0]
        analise.append(f"**Descrição**: {primeira_linha}\n")
    analise.append("\n")

# Integrações
analise.append("## INTEGRAÇÕES IDENTIFICADAS\n\n")

integracoes_info = {
    "Notion API": {
        "keywords": ["notion_client", "Client", "DATABASE_ID", "database"],
        "desc": "Extrai tarefas de um banco de dados Notion"
    },
    "Google Calendar API": {
        "keywords": ["google", "calendar", "googleapiclient"],
        "desc": "Verifica disponibilidade de horários"
    },
    "Playwright": {
        "keywords": ["playwright", "sync_api", "chromium", "browser"],
        "desc": "Automação web para agendamento no site Telenordeste"
    }
}

for nome, info in integracoes_info.items():
    encontrado = any(kw in conteudo for kw in info["keywords"])
    if encontrado:
        count = sum(conteudo.count(kw) for kw in info["keywords"])
        analise.append(f"### ✅ {nome}\n")
        analise.append(f"- **Função**: {info['desc']}\n")
        analise.append(f"- **Referências no código**: {count}\n\n")

# Variáveis de configuração
analise.append("## CONFIGURAÇÕES E VARIÁVEIS\n\n")
vars_config = re.findall(r'^([A-Z_]{3,})\s*=\s*(.+?)$', conteudo, re.MULTILINE)
if vars_config:
    analise.append("```python\n")
    for var, valor in vars_config[:15]:
        if len(valor) > 60:
            valor = valor[:57] + "..."
        analise.append(f"{var} = {valor}\n")
    analise.append("```\n\n")

# URLs
analise.append("## URLs E ENDPOINTS\n\n")
urls = re.findall(r'https?://[^\s\'"<>]+', conteudo)
for url in sorted(set(urls)):
    analise.append(f"- `{url}`\n")
analise.append("\n")

# Fluxo principal
analise.append("## FLUXO DE EXECUÇÃO PRINCIPAL\n\n")
analise.append("Baseado na análise do código, o bot segue este fluxo:\n\n")

# Buscar main ou similar
main_section = re.search(r'if __name__\s*==\s*[\'"]__main__[\'"]:(.*?)(?=\n\S|\Z)', 
                        conteudo, re.DOTALL)

if main_section:
    main_code = main_section.group(1)
    linhas_codigo = [l for l in main_code.split('\n') if l.strip() and not l.strip().startswith('#')]
    
    analise.append("```python\n")
    for linha in linhas_codigo[:30]:
        analise.append(linha + "\n")
    analise.append("```\n\n")

# Padrões de automação
analise.append("## PADRÕES DE AUTOMAÇÃO WEB\n\n")
padroes = {
    "Navegação": conteudo.count("goto") + conteudo.count("navigate"),
    "Cliques": conteudo.count("click(") + conteudo.count(".click"),
    "Preenchimento de formulários": conteudo.count("fill(") + conteudo.count("type("),
    "Esperas/Timeouts": conteudo.count("wait") + conteudo.count("sleep"),
    "Seletores": conteudo.count("querySelector") + conteudo.count("selector"),
    "Screenshots": conteudo.count("screenshot"),
}

for padrao, count in padroes.items():
    if count > 0:
        analise.append(f"- **{padrao}**: {count} ocorrências\n")

analise.append("\n")

# Estruturas de controle
analise.append("## ESTRUTURAS DE CONTROLE\n\n")
analise.append(f"- **Loops for**: {conteudo.count('for ')}\n")
analise.append(f"- **Loops while**: {conteudo.count('while ')}\n")
analise.append(f"- **Condicionais if**: {conteudo.count('if ')}\n")
analise.append(f"- **Try/Except**: {conteudo.count('try:')}\n")
analise.append(f"- **Funções assíncronas**: {conteudo.count('async def')}\n\n")

# Resumo funcional
analise.append("## RESUMO FUNCIONAL\n\n")
analise.append("### O que o bot faz:\n\n")
analise.append("1. **Conecta ao Notion**: Busca tarefas com status 'Não iniciado'\n")
analise.append("2. **Extrai dados da tarefa**: Nome, CPF, especialidade, motivo da consulta, etc.\n")
analise.append("3. **Verifica Google Calendar**: Confirma disponibilidade do horário desejado\n")
analise.append("4. **Acessa site Telenordeste**: Automação web com Playwright\n")
analise.append("5. **Navega pelo sistema**: Seleciona agenda (Adulto/Infantil) baseado no tipo\n")
analise.append("6. **Busca horários disponíveis**: Varre o calendário procurando vagas\n")
analise.append("7. **Preenche formulário**: Insere dados do paciente automaticamente\n")
analise.append("8. **Efetua reserva**: Clica no botão de confirmação\n")
analise.append("9. **Dupla checagem**: Verifica se o agendamento foi realmente efetuado\n")
analise.append("10. **Atualiza Notion**: Marca tarefa como concluída ou registra erro\n")
analise.append("11. **Cria evento no Google Calendar**: Sincroniza o agendamento\n\n")

analise.append("### Recursos de confiabilidade:\n\n")
analise.append("- ✅ Logs detalhados com timestamps\n")
analise.append("- ✅ Tratamento de erros com try/except\n")
analise.append("- ✅ Verificação dupla de confirmação\n")
analise.append("- ✅ Atualização automática de status no Notion\n")
analise.append("- ✅ Integração com Google Calendar para evitar conflitos\n\n")

# Salvar
with open("ANALISE_AGENDADOR_COMPLETA.md", "w", encoding="utf-8") as f:
    f.writelines(analise)

print("✅ Análise completa salva em: ANALISE_AGENDADOR_COMPLETA.md")
print(f"📄 {len(analise)} seções analisadas")
