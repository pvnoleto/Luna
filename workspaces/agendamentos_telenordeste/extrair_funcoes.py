#!/usr/bin/env python3
"""Extrai funções do agendador para análise"""

with open('agendador_final_corrigido.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Extrair todas as definições de função
import re
funcoes = re.findall(r'^def (.+?):', content, re.MULTILINE)

print("=" * 80)
print("FUNÇÕES ENCONTRADAS NO AGENDADOR:")
print("=" * 80)
for i, func in enumerate(funcoes, 1):
    print(f"{i:2}. {func}")

print("\n" + "=" * 80)
print("VARIÁVEIS DE CONFIGURAÇÃO:")
print("=" * 80)

# Buscar variáveis importantes
linhas = content.split('\n')
for i, linha in enumerate(linhas[:100]):
    if 'NOTION_TOKEN' in linha or 'DATABASE_ID' in linha or 'URL' in linha:
        print(f"Linha {i+1}: {linha.strip()}")
