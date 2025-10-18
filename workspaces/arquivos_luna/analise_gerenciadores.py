#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análise completa dos gerenciadores de temporários e workspaces
"""

import inspect
import json
from gerenciador_temp import GerenciadorTemporarios
from gerenciador_workspaces import GerenciadorWorkspaces

def analisar_classe(classe, nome):
    """Analisa uma classe e retorna informações detalhadas"""
    print(f"\n{'='*80}")
    print(f"📦 ANÁLISE: {nome}")
    print(f"{'='*80}\n")
    
    # Docstring da classe
    print(f"📄 DESCRIÇÃO:\n{classe.__doc__}\n")
    
    # Métodos públicos
    metodos_publicos = [m for m in dir(classe) if not m.startswith('_') and callable(getattr(classe, m))]
    print(f"🔧 MÉTODOS PÚBLICOS ({len(metodos_publicos)}):")
    for metodo in metodos_publicos:
        func = getattr(classe, metodo)
        doc = func.__doc__ if func.__doc__ else "Sem documentação"
        # Primeira linha da docstring
        primeira_linha = doc.strip().split('\n')[0] if doc else ""
        print(f"  • {metodo}() - {primeira_linha}")
    
    # Métodos privados (começam com _)
    metodos_privados = [m for m in dir(classe) if m.startswith('_') and not m.startswith('__') and callable(getattr(classe, m))]
    print(f"\n🔒 MÉTODOS PRIVADOS ({len(metodos_privados)}):")
    for metodo in metodos_privados:
        print(f"  • {metodo}()")
    
    return {
        'nome': nome,
        'metodos_publicos': metodos_publicos,
        'metodos_privados': metodos_privados,
        'total_metodos': len(metodos_publicos) + len(metodos_privados)
    }

def analisar_uso():
    """Analisa o uso atual dos gerenciadores"""
    print(f"\n{'='*80}")
    print(f"📊 STATUS ATUAL DOS GERENCIADORES")
    print(f"{'='*80}\n")
    
    # Gerenciador de temporários
    print("🗑️ GERENCIADOR DE TEMPORÁRIOS:")
    try:
        gt = GerenciadorTemporarios()
        stats = gt.obter_estatisticas()
        print(f"  • Arquivos temporários: {stats['total_temporarios']}")
        print(f"  • Arquivos protegidos: {stats['total_protegidos']}")
        print(f"  • Total deletados: {stats['total_deletados']}")
        print(f"  • Total resgatados: {stats['total_resgatados']}")
        print(f"  • Espaço liberado: {stats['espaco_liberado_mb']:.2f} MB")
    except Exception as e:
        print(f"  ❌ Erro: {e}")
    
    # Gerenciador de workspaces
    print("\n📁 GERENCIADOR DE WORKSPACES:")
    try:
        gw = GerenciadorWorkspaces()
        workspaces = gw.listar_workspaces()
        print(f"  • Total de workspaces: {len(workspaces)}")
        print(f"  • Workspace atual: {gw.get_workspace_atual() or 'Nenhum'}")
        if workspaces:
            print(f"  • Workspaces criados:")
            for ws in workspaces:
                print(f"    - {ws['nome']}: {ws.get('descricao', 'Sem descrição')}")
    except Exception as e:
        print(f"  ❌ Erro: {e}")

def gerar_documentacao():
    """Gera documentação completa em formato markdown"""
    print(f"\n{'='*80}")
    print(f"📝 GERANDO DOCUMENTAÇÃO MARKDOWN")
    print(f"{'='*80}\n")
    
    doc = "# Documentação dos Gerenciadores Luna\n\n"
    doc += "## 🗑️ GerenciadorTemporarios\n\n"
    doc += "Gerencia arquivos temporários com auto-limpeza após 30 dias.\n\n"
    doc += "### Métodos Principais:\n\n"
    
    gt_metodos = {
        'marcar_temporario': 'Marca arquivo como temporário (será deletado em 30 dias)',
        'proteger_arquivo': 'Remove arquivo da lista de temporários e o protege',
        'listar_temporarios': 'Lista todos os arquivos temporários marcados',
        'limpar_arquivos_antigos': 'Deleta arquivos temporários antigos (>30 dias)',
        'obter_estatisticas': 'Retorna estatísticas de uso',
        'exibir_status': 'Exibe status formatado no console'
    }
    
    for metodo, desc in gt_metodos.items():
        doc += f"- **`{metodo}()`**: {desc}\n"
    
    doc += "\n## 📁 GerenciadorWorkspaces\n\n"
    doc += "Organiza projetos em pastas separadas dentro de `Luna/workspaces/`.\n\n"
    doc += "### Métodos Principais:\n\n"
    
    gw_metodos = {
        'criar_workspace': 'Cria novo workspace (projeto)',
        'selecionar_workspace': 'Define workspace ativo',
        'listar_workspaces': 'Lista todos os workspaces criados',
        'deletar_workspace': 'Remove workspace e seus arquivos',
        'renomear_workspace': 'Renomeia workspace existente',
        'resolver_caminho': 'Converte caminho relativo para absoluto no workspace atual',
        'criar_arquivo': 'Cria arquivo no workspace atual',
        'buscar_arquivo': 'Busca arquivo por nome em todos os workspaces',
        'listar_arquivos': 'Lista arquivos de um workspace',
        'exibir_arvore': 'Mostra árvore de diretórios',
        'get_workspace_atual': 'Retorna nome do workspace ativo',
        'get_caminho_workspace': 'Retorna caminho completo de um workspace'
    }
    
    for metodo, desc in gw_metodos.items():
        doc += f"- **`{metodo}()`**: {desc}\n"
    
    doc += "\n## 💡 Boas Práticas\n\n"
    doc += "### Gerenciador de Temporários:\n"
    doc += "1. Marque screenshots, logs de debug e arquivos de teste como temporários\n"
    doc += "2. Use `proteger_arquivo()` para arquivos importantes erroneamente marcados\n"
    doc += "3. Execute `limpar_arquivos_antigos()` periodicamente\n"
    doc += "4. Verifique `obter_estatisticas()` para monitorar espaço liberado\n\n"
    
    doc += "### Gerenciador de Workspaces:\n"
    doc += "1. Crie workspace separado para cada projeto\n"
    doc += "2. Use `resolver_caminho()` para garantir caminhos corretos\n"
    doc += "3. Sempre selecione workspace antes de criar arquivos\n"
    doc += "4. Use `buscar_arquivo()` quando não souber a localização exata\n"
    doc += "5. Execute `exibir_arvore()` para visualizar estrutura\n\n"
    
    doc += "## 🎯 Fluxo de Trabalho Recomendado\n\n"
    doc += "```python\n"
    doc += "# 1. Criar workspace para novo projeto\n"
    doc += "gw = GerenciadorWorkspaces()\n"
    doc += "gw.criar_workspace('meu_projeto', 'Descrição do projeto')\n"
    doc += "gw.selecionar_workspace('meu_projeto')\n\n"
    
    doc += "# 2. Criar arquivos no workspace\n"
    doc += "caminho = gw.resolver_caminho('codigo.py')\n"
    doc += "gw.criar_arquivo('codigo.py', 'print(\"Hello\")')\n\n"
    
    doc += "# 3. Marcar arquivos temporários de teste\n"
    doc += "gt = GerenciadorTemporarios()\n"
    doc += "gt.marcar_temporario('test_screenshot.png')\n"
    doc += "gt.marcar_temporario('debug.log')\n\n"
    
    doc += "# 4. Limpar periodicamente\n"
    doc += "gt.limpar_arquivos_antigos(exibir_resumo=True)\n"
    doc += "```\n"
    
    # Salvar documentação
    with open('DOCUMENTACAO_GERENCIADORES.md', 'w', encoding='utf-8') as f:
        f.write(doc)
    
    print("✅ Documentação salva em: DOCUMENTACAO_GERENCIADORES.md")
    
    return doc

if __name__ == "__main__":
    # Análise das classes
    info_temp = analisar_classe(GerenciadorTemporarios, "GerenciadorTemporarios")
    info_ws = analisar_classe(GerenciadorWorkspaces, "GerenciadorWorkspaces")
    
    # Status atual
    analisar_uso()
    
    # Gerar documentação
    gerar_documentacao()
    
    # Resumo final
    print(f"\n{'='*80}")
    print("✅ ANÁLISE COMPLETA CONCLUÍDA")
    print(f"{'='*80}\n")
    print(f"Total de funcionalidades descobertas:")
    print(f"  • GerenciadorTemporarios: {info_temp['total_metodos']} métodos")
    print(f"  • GerenciadorWorkspaces: {info_ws['total_metodos']} métodos")
    print(f"\nDocumentação gerada com sucesso! 🎉\n")
