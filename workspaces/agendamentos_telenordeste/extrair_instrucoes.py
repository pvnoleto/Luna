#!/usr/bin/env python3
"""Extrai instruções principais do agendador"""

with open('agendador_final_corrigido.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("=" * 100)
print("📋 INSTRUÇÕES DO PROCESSO DE AGENDAMENTO - TELENORDESTE")
print("=" * 100)

# Extrair comentários e docstrings importantes
dentro_funcao = None
for i, line in enumerate(lines):
    # Capturar definições de função com docstring
    if line.strip().startswith('def '):
        dentro_funcao = line.strip()
        print(f"\n{'='*80}")
        print(f"FUNÇÃO: {dentro_funcao}")
        print('='*80)
    
    # Capturar docstrings
    elif '"""' in line and dentro_funcao:
        start = i
        docstring = []
        for j in range(i, min(i+20, len(lines))):
            docstring.append(lines[j].strip().replace('"""', ''))
            if j > i and '"""' in lines[j]:
                break
        print("DESCRIÇÃO:", ' '.join(docstring).strip())
        dentro_funcao = None
    
    # Capturar comentários importantes
    elif line.strip().startswith('#') and 'PASSO' in line.upper() or 'TODO' in line or 'IMPORTANTE' in line:
        print(f"  → {line.strip()}")

print("\n" + "=" * 100)

# Buscar configurações específicas
print("\n📝 CONFIGURAÇÕES IDENTIFICADAS:")
print("=" * 100)
for i, line in enumerate(lines[:300]):
    if 'URL' in line and '=' in line and not line.strip().startswith('#'):
        print(f"  • {line.strip()}")
    elif 'ESPECIALIDADE' in line.upper() and '=' in line:
        print(f"  • {line.strip()}")
    elif 'NOTION' in line and '=' in line and not line.strip().startswith('#'):
        print(f"  • {line.strip()}")
