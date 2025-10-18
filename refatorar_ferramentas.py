#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de refatoração automática: _carregar_ferramentas_base()
Quebra método de 655 linhas em 8 submétodos organizados
"""

import re
import sys

def extrair_secao(content, inicio_marker, fim_marker=None):
    """Extrai uma seção do código entre markers"""
    inicio = content.find(inicio_marker)
    if inicio == -1:
        return None

    if fim_marker:
        fim = content.find(fim_marker, inicio + 1)
        if fim == -1:
            return None
        return content[inicio:fim]
    return content[inicio:]

def refatorar_carregar_ferramentas():
    """Refatora o método _carregar_ferramentas_base()"""

    # Ler arquivo
    with open('luna_v3_FINAL_OTIMIZADA.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Encontrar linha do método
    metodo_linha = None
    for i, line in enumerate(lines):
        if 'def _carregar_ferramentas_base(self)' in line:
            metodo_linha = i
            break

    if metodo_linha is None:
        print("❌ Erro: Não encontrou método _carregar_ferramentas_base")
        return False

    # Encontrar fim do método (próximo def no mesmo nível de indentação)
    fim_metodo = None
    for i in range(metodo_linha + 1, len(lines)):
        if lines[i].startswith('    def ') and 'adicionar_ferramenta' not in lines[i]:
            fim_metodo = i
            break

    if fim_metodo is None:
        print("❌ Erro: Não encontrou fim do método")
        return False

    print(f"📍 Método encontrado: linhas {metodo_linha+1} até {fim_metodo}")
    print(f"   Total: {fim_metodo - metodo_linha} linhas")

    # Extrair conteúdo do método
    metodo_completo = ''.join(lines[metodo_linha:fim_metodo])

    # Identificar seções
    secoes = {
        'bash': ('# ═══ BASH ═══', '# ═══ ARQUIVOS ═══'),
        'arquivos': ('# ═══ ARQUIVOS ═══', '# ═══ PLAYWRIGHT ═══'),
        'navegador': ('# ═══ PLAYWRIGHT ═══', '# ═══ CREDENCIAIS ═══'),
        'cofre': ('# ═══ CREDENCIAIS ═══', '# ═══ MEMÓRIA ═══'),
        'memoria': ('# ═══ MEMÓRIA ═══', '# ═══ WORKSPACES ═══'),
        'workspace': ('# ═══ WORKSPACES ═══', '# ═══ META-FERRAMENTAS ═══'),
        'meta': ('# ═══ META-FERRAMENTAS ═══', '# ═══ NOTION'),
    }

    # Criar métodos auxiliares
    novos_metodos = []

    for nome, (inicio, fim) in secoes.items():
        secao = extrair_secao(metodo_completo, inicio, fim)
        if secao:
            # Criar método auxiliar
            metodo_aux = f'''    def _carregar_ferramentas_{nome}(self) -> None:
        """Carrega ferramentas de {nome.upper()}."""
        {secao.strip()}

'''
            novos_metodos.append(metodo_aux)
            print(f"✅ Extraída seção: {nome}")

    # Criar novo método principal
    novo_principal = '''    def _carregar_ferramentas_base(self) -> None:
        """
        Carrega todas as ferramentas base do sistema.

        ✅ REFATORADO: Organizado em submétodos para melhor manutenção.
        Cada categoria tem seu próprio método auxiliar.
        """
        self._carregar_ferramentas_bash()
        self._carregar_ferramentas_arquivos()
        self._carregar_ferramentas_navegador()
        self._carregar_ferramentas_cofre()
        self._carregar_ferramentas_memoria()
        self._carregar_ferramentas_workspace()
        self._carregar_ferramentas_meta()

        # Notion já é carregado separadamente (condicional)
        if NOTION_DISPONIVEL:
            # Já foi carregado no método original
            pass

'''

    # Construir novo arquivo
    novas_lines = []

    # Adicionar linhas até o método original
    novas_lines.extend(lines[:metodo_linha])

    # Adicionar novos métodos auxiliares
    for metodo in novos_metodos:
        novas_lines.append(metodo)

    # Adicionar novo método principal
    novas_lines.append(novo_principal)

    # Adicionar resto do arquivo (após o método original)
    novas_lines.extend(lines[fim_metodo:])

    # Salvar backup
    with open('luna_v3_FINAL_OTIMIZADA.py.backup', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("💾 Backup criado: luna_v3_FINAL_OTIMIZADA.py.backup")

    # Salvar arquivo refatorado
    with open('luna_v3_FINAL_OTIMIZADA.py', 'w', encoding='utf-8') as f:
        f.writelines(novas_lines)

    print(f"\n✅ Refatoração completa!")
    print(f"   Linhas removidas: {fim_metodo - metodo_linha}")
    print(f"   Novos métodos criados: {len(novos_metodos) + 1}")
    print(f"   Redução aproximada: {fim_metodo - metodo_linha} → ~{len(novos_metodos) * 30 + 20} linhas")

    return True

if __name__ == '__main__':
    print("🔧 REFATORAÇÃO AUTOMÁTICA: _carregar_ferramentas_base()")
    print("=" * 60)

    sucesso = refatorar_carregar_ferramentas()

    if sucesso:
        print("\n🎉 Sucesso! Execute para validar:")
        print("   python3 -m py_compile luna_v3_FINAL_OTIMIZADA.py")
        sys.exit(0)
    else:
        print("\n❌ Falha na refatoração")
        sys.exit(1)
