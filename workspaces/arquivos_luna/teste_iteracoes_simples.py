#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# Forçar UTF-8 para evitar problemas de encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from dotenv import load_dotenv

load_dotenv()

# Vamos apenas inspecionar o código sem executar
import inspect
from agente_completo_final import AgenteCompletoFinal

print("="*70)
print("ANALISE DETALHADA DO LIMITE DE ITERACOES")
print("="*70)

# 1. Verificar o valor padrão do parâmetro
metodo = AgenteCompletoFinal.executar_tarefa
assinatura = inspect.signature(metodo)
max_iter_param = assinatura.parameters['max_iteracoes']
valor_padrao = max_iter_param.default

print(f"\n1. PARAMETRO DA FUNCAO")
print(f"   Metodo: executar_tarefa()")
print(f"   Parametro: max_iteracoes")
print(f"   Valor padrao: {valor_padrao}")

# 2. Verificar o código fonte
codigo_fonte = inspect.getsource(metodo)
linhas_relevantes = []
for i, linha in enumerate(codigo_fonte.split('\n'), 1):
    if 'max_iteracoes' in linha.lower() or 'range' in linha:
        linhas_relevantes.append((i, linha.strip()))

print(f"\n2. LINHAS RELEVANTES NO CODIGO")
for num, linha in linhas_relevantes[:10]:  # Primeiras 10 linhas
    print(f"   Linha {num}: {linha[:80]}")

# 3. Resumo
print(f"\n3. RESUMO")
print(f"   {'='*66}")
if valor_padrao == 50:
    print(f"   [OK] Limite configurado corretamente para 50 iteracoes")
else:
    print(f"   [ERRO] Limite em {valor_padrao}, deveria ser 50")
print(f"   {'='*66}")

# 4. Teste prático (sem executar Claude, apenas verificando a estrutura)
print(f"\n4. TESTE ESTRUTURAL")
try:
    agente = AgenteCompletoFinal(
        api_key="test_key_dummy",
        master_password=None,
        usar_memoria=False
    )
    print(f"   [OK] Agente instanciado com sucesso")
    print(f"   [OK] Ferramentas disponiveis: {len(agente.sistema_ferramentas.ferramentas_descricao)}")
except Exception as e:
    print(f"   [ERRO] {e}")

print("\n" + "="*70)
print("CONCLUSAO: Limite de iteracoes esta configurado para", valor_padrao)
print("="*70)
