#!/usr/bin/env python3
"""
Script de validação do fibonacci_results.txt
"""
import re

# Leitura do arquivo
with open('fibonacci_results.txt', 'r', encoding='utf-8') as f:
    conteudo = f.read()

print("=" * 70)
print("VALIDAÇÃO DO ARQUIVO fibonacci_results.txt")
print("=" * 70)

# Critérios de validação
criterios = {
    "1. Valor correto Fibonacci(30) = 832040": False,
    "2. Tempo de execução iterativa": False,
    "3. Tempo de execução recursiva": False,
    "4. Comparação quantitativa (fator)": False,
    "5. Explicação sobre complexidade": False
}

# Validação 1: Número correto
if "832,040" in conteudo or "832040" in conteudo:
    criterios["1. Valor correto Fibonacci(30) = 832040"] = True
    print("✅ Critério 1: Valor 832040 encontrado")
else:
    print("❌ Critério 1: Valor 832040 NÃO encontrado")

# Validação 2: Tempo iterativa
if "ITERATIVA" in conteudo and "segundos" in conteudo:
    # Extrair tempo
    match_iter = re.search(r'ITERATIVA:\s+([\d.]+)\s+segundos', conteudo)
    if match_iter:
        tempo_iter = float(match_iter.group(1))
        criterios["2. Tempo de execução iterativa"] = True
        print(f"✅ Critério 2: Tempo iterativa = {tempo_iter} segundos")
    else:
        print("❌ Critério 2: Tempo iterativa NÃO encontrado")
else:
    print("❌ Critério 2: Tempo iterativa NÃO encontrado")

# Validação 3: Tempo recursiva
if "RECURSIVA" in conteudo and "segundos" in conteudo:
    match_rec = re.search(r'RECURSIVA:\s+([\d.]+)\s+segundos', conteudo)
    if match_rec:
        tempo_rec = float(match_rec.group(1))
        criterios["3. Tempo de execução recursiva"] = True
        print(f"✅ Critério 3: Tempo recursiva = {tempo_rec} segundos")
    else:
        print("❌ Critério 3: Tempo recursiva NÃO encontrado")
else:
    print("❌ Critério 3: Tempo recursiva NÃO encontrado")

# Validação 4: Comparação quantitativa
if "mais rápida" in conteudo or "vezes" in conteudo or "x mais" in conteudo:
    match_comp = re.search(r'([\d,]+(?:\.\d+)?)\s*x\s+mais rápida', conteudo)
    if match_comp:
        fator = match_comp.group(1).replace(',', '')
        fator_num = float(fator)
        criterios["4. Comparação quantitativa (fator)"] = True
        print(f"✅ Critério 4: Fator de velocidade = {fator_num}x")
        if fator_num > 1000:
            print(f"   ✓ Fator > 1000x confirmado ({fator_num:.2f}x)")
    else:
        print("❌ Critério 4: Fator de velocidade NÃO encontrado")
else:
    print("❌ Critério 4: Comparação NÃO encontrada")

# Validação 5: Explicação sobre complexidade
termos_complexidade = ["O(2^n)", "O(n)", "complexidade", "exponencial", "linear"]
termos_encontrados = [termo for termo in termos_complexidade if termo in conteudo]

if len(termos_encontrados) >= 2:
    criterios["5. Explicação sobre complexidade"] = True
    print(f"✅ Critério 5: Explicação sobre complexidade encontrada")
    print(f"   Termos encontrados: {', '.join(termos_encontrados)}")
else:
    print("❌ Critério 5: Explicação sobre complexidade INSUFICIENTE")

print("\n" + "=" * 70)
print("RESUMO DA VALIDAÇÃO")
print("=" * 70)

todos_ok = all(criterios.values())
total = len(criterios)
aprovados = sum(criterios.values())

for criterio, status in criterios.items():
    simbolo = "✅" if status else "❌"
    print(f"{simbolo} {criterio}")

print("\n" + "-" * 70)
print(f"RESULTADO: {aprovados}/{total} critérios atendidos")

if todos_ok:
    print("\n🎉 VALIDAÇÃO COMPLETA: Todos os critérios foram atendidos!")
    exit(0)
else:
    print("\n⚠️  VALIDAÇÃO PARCIAL: Alguns critérios não foram atendidos.")
    exit(1)
