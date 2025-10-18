#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import inspect
from agente_completo_final import AgenteCompletoFinal

# Obter a assinatura do método executar_tarefa
metodo = AgenteCompletoFinal.executar_tarefa
assinatura = inspect.signature(metodo)

print("="*70)
print("VERIFICACAO DO LIMITE DE ITERACOES")
print("="*70)

# Pegar o valor padrão do parâmetro max_iteracoes
parametros = assinatura.parameters
max_iter_param = parametros['max_iteracoes']
valor_padrao = max_iter_param.default

print(f"\nMetodo: AgenteCompletoFinal.executar_tarefa()")
print(f"Parametro: max_iteracoes")
print(f"Valor padrao: {valor_padrao}")
print()

if valor_padrao == 50:
    print("[OK] CORRETO! O limite esta configurado para 50 iteracoes")
    print("="*70)
    exit(0)
else:
    print(f"[ERRO] INCORRETO! O limite esta em {valor_padrao}, deveria ser 50")
    print("="*70)
    exit(1)
