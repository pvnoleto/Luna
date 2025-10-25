#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para copiar SistemaFerramentasCompleto do luna_final.py para luna_v3_TIER2_COMPLETO.py
"""

import re

print("🔧 COPIANDO SISTEMA DE FERRAMENTAS COMPLETO...")
print("="*70)

# Ler luna_final.py
print("\n1️⃣ Lendo luna_final.py...")
with open("luna_final.py", 'r', encoding='utf-8') as f:
    conteudo_final = f.read()

# Ler luna_v3_TIER2_COMPLETO.py
print("2️⃣ Lendo luna_v3_TIER2_COMPLETO.py...")
with open("luna_v3_TIER2_COMPLETO.py", 'r', encoding='utf-8') as f:
    conteudo_v3 = f.read()

# Extrair classe SistemaFerramentasCompleto do luna_final.py
print("3️⃣ Extraindo SistemaFerramentasCompleto do luna_final.py...")

# Encontrar início
inicio_final = conteudo_final.find("class SistemaFerramentasCompleto:")
if inicio_final == -1:
    print("❌ ERRO: Classe não encontrada em luna_final.py!")
    exit(1)

# Encontrar fim (próxima classe principal)
fim_final = conteudo_final.find("\nclass AgenteCompletoFinal:", inicio_final + 1)
if fim_final == -1:
    fim_final = conteudo_final.find("\n\n# ============", inicio_final + 5000)  # Próxima seção
if fim_final == -1:
    print("❌ ERRO: Fim da classe não encontrado!")
    exit(1)

classe_completa = conteudo_final[inicio_final:fim_final]

print(f"   ✅ Extraído {len(classe_completa)} caracteres")
print(f"   ✅ {classe_completa.count('def adicionar_ferramenta')} métodos 'adicionar_ferramenta'")
print(f"   ✅ {classe_completa.count('self.adicionar_ferramenta')} chamadas de ferramentas")

# Verificar conteúdo
if "def bash_avancado" not in classe_completa:
    print("   ⚠️  AVISO: bash_avancado não encontrado na string!")
if "def criar_arquivo" not in classe_completa:
    print("   ⚠️  AVISO: criar_arquivo não encontrado na string!")

# Localizar e substituir no luna_v3
print("\n4️⃣ Localizando classe vazia no luna_v3_TIER2_COMPLETO.py...")

inicio_v3 = conteudo_v3.find("class SistemaFerramentasCompleto:")
if inicio_v3 == -1:
    print("❌ ERRO: Classe não encontrada em luna_v3!")
    exit(1)

# Encontrar fim da classe vazia
fim_v3 = conteudo_v3.find("\nclass AgenteComTier2Completo:", inicio_v3 + 1)
if fim_v3 == -1:
    fim_v3 = conteudo_v3.find("\n\n# ============", inicio_v3 + 500)
if fim_v3 == -1:
    print("❌ ERRO: Fim da classe não encontrado em luna_v3!")
    exit(1)

print(f"   ✅ Classe vazia localizada (posição {inicio_v3}-{fim_v3})")

# Fazer backup
print("\n5️⃣ Criando backup...")
with open("luna_v3_TIER2_COMPLETO.py.backup", 'w', encoding='utf-8') as f:
    f.write(conteudo_v3)
print("   ✅ Backup criado: luna_v3_TIER2_COMPLETO.py.backup")

# Substituir
print("\n6️⃣ Substituindo classe...")
novo_conteudo = conteudo_v3[:inicio_v3] + classe_completa + conteudo_v3[fim_v3:]

# Salvar
print("7️⃣ Salvando arquivo atualizado...")
with open("luna_v3_TIER2_COMPLETO.py", 'w', encoding='utf-8') as f:
    f.write(novo_conteudo)

print("\n" + "="*70)
print("✅ SUBSTITUIÇÃO CONCLUÍDA COM SUCESSO!")
print("="*70)

# Estatísticas
print("\n📊 ESTATÍSTICAS:")
print(f"   Arquivo original: {len(conteudo_v3):,} caracteres")
print(f"   Arquivo novo: {len(novo_conteudo):,} caracteres")
print(f"   Diferença: {len(novo_conteudo) - len(conteudo_v3):+,} caracteres")

print("\n🔍 VERIFICAÇÃO:")
# Contar ferramentas no arquivo novo
ferramentas = novo_conteudo.count("self.adicionar_ferramenta(")
print(f"   Ferramentas encontradas: {ferramentas}")

if ferramentas > 10:
    print("   ✅ Sistema de ferramentas parece completo!")
else:
    print("   ⚠️  AVISO: Poucas ferramentas detectadas!")

print("\n✅ Pronto! Agora você pode executar:")
print("   python luna_v3_TIER2_COMPLETO.py")
