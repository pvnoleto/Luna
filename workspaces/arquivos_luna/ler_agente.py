import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('agente_completo_final.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Procurar pelo loop principal
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'while iteration' in line.lower() or 'for iteration' in line.lower():
        print(f"Linha {i}: {line}")
        # Mostrar contexto (10 linhas antes e depois)
        start = max(0, i-10)
        end = min(len(lines), i+20)
        print("\n=== CONTEXTO ===")
        for j in range(start, end):
            print(f"{j:4d}: {lines[j]}")
        print("\n" + "="*50 + "\n")
