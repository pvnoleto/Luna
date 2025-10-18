#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para substituir a classe SistemaFerramentasCompleto"""

import re

# Ler luna_v3
with open('luna_v3_TIER2_COMPLETO.py', 'r', encoding='utf-8') as f:
    conteudo_v3 = f.read()

# Ler luna_final para pegar a classe completa
with open('luna_final.py', 'r', encoding='utf-8') as f:
    conteudo_final = f.read()

# Extrair a classe completa do luna_final
inicio_classe_final = conteudo_final.find('class SistemaFerramentasCompleto:')
if inicio_classe_final == -1:
    print("❌ ERRO: Classe não encontrada em luna_final.py!")
    exit(1)

# Encontrar o fim da classe (próxima classe ou seção)
fim_classe_final = conteudo_final.find('\n\n# ====', inicio_classe_final + 100)
if fim_classe_final == -1:
    fim_classe_final = conteudo_final.find('\nclass Agente', inicio_classe_final + 100)

if fim_classe_final == -1:
    print("❌ ERRO: Fim da classe não encontrado em luna_final.py!")
    exit(1)

classe_completa = conteudo_final[inicio_classe_final:fim_classe_final].strip()

print("✅ Classe extraída do luna_final.py")
print(f"   Tamanho: {len(classe_completa)} caracteres")

# Encontrar e substituir no luna_v3
inicio_classe_v3 = conteudo_v3.find('class SistemaFerramentasCompleto:')
if inicio_classe_v3 == -1:
    print("❌ ERRO: Classe não encontrada em luna_v3_TIER2_COMPLETO.py!")
    exit(1)

# Encontrar fim da classe (próxima seção ou classe)
fim_classe_v3 = conteudo_v3.find('\n\n# ====', inicio_classe_v3 + 100)
if fim_classe_v3 == -1:
    print("❌ ERRO: Fim da classe não encontrado em luna_v3_TIER2_COMPLETO.py!")
    exit(1)

print(f"✅ Localizou classe em luna_v3_TIER2_COMPLETO.py")

# Fazer backup
import shutil
shutil.copy('luna_v3_TIER2_COMPLETO.py', 'luna_v3_TIER2_COMPLETO.py.backup')
print("✅ Backup criado: luna_v3_TIER2_COMPLETO.py.backup")

# Substituir
novo_conteudo = conteudo_v3[:inicio_classe_v3] + classe_completa + conteudo_v3[fim_classe_v3:]

# Salvar
with open('luna_v3_TIER2_COMPLETO.py', 'w', encoding='utf-8') as f:
    f.write(novo_conteudo)

print("\n" + "="*70)
print("✅ SUBSTITUIÇÃO CONCLUÍDA COM SUCESSO!")
print("="*70)
print(f"   Arquivo original: {len(conteudo_v3):,} caracteres")
print(f"   Arquivo novo: {len(novo_conteudo):,} caracteres")
print(f"   Diferença: {len(novo_conteudo) - len(conteudo_v3):+,} caracteres")
print("\n🎉 A classe SistemaFerramentasCompleto foi substituída pela versão completa!")
print("   Todas as ferramentas (bash, arquivos, playwright, workspaces, etc) estão disponíveis agora!")
