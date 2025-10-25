#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open('fibonacci_results.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Verificar critérios de sucesso
criterios = {
    'Diferença absoluta': '0.196278 segundos' in content,
    'Fator multiplicativo': '49,070' in content and 'vezes mais lento' in content,
    'Diferença percentual': '4,906,950' in content and '%' in content,
    'Interpretação qualitativa': 'ORDENS DE MAGNITUDE' in content,
    'Seção ANÁLISE COMPARATIVA': 'ANÁLISE COMPARATIVA DETALHADA' in content,
    'Métricas quantitativas': 'MÉTRICAS QUANTITATIVAS' in content,
    'Interpretação qualitativa seção': 'INTERPRETAÇÃO QUALITATIVA' in content,
    'Implicações práticas': 'IMPLICAÇÕES PRÁTICAS' in content,
    'Conclusão qualitativa': 'CONCLUSÃO QUALITATIVA' in content,
    'Recomendações': 'RECOMENDAÇÕES' in content
}

print('=' * 80)
print('VALIDAÇÃO DOS CRITÉRIOS DE SUCESSO')
print('=' * 80)
print()

todos_ok = True
for criterio, resultado in criterios.items():
    status = '✅' if resultado else '❌'
    print(f'{status} {criterio}: {"PRESENTE" if resultado else "AUSENTE"}')
    if not resultado:
        todos_ok = False

print()
print('=' * 80)
if todos_ok:
    print('✅ TODOS OS CRITÉRIOS DE SUCESSO FORAM ATENDIDOS!')
else:
    print('❌ Alguns critérios não foram atendidos.')
print('=' * 80)
