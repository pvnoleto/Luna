# Conteúdo temporário para extração das ferramentas de luna_final.py

import re

# Ler luna_final.py
with open("C:\\Users\\Pedro Victor\\OneDrive\\Área de Trabalho\\Documentos\\Projetos Automações e Digitais\\Luna\\luna_final.py", 'r', encoding='utf-8') as f:
    conteudo_final = f.read()

# Encontrar a classe SistemaFerramentasCompleto
inicio_classe = conteudo_final.find("class SistemaFerramentasCompleto:")
if inicio_classe == -1:
    print("Classe não encontrada!")
    exit(1)

# Encontrar o fim da classe (próxima classe ou fim do arquivo antes de "class Agente")
proximo_class = conteudo_final.find("\nclass Agente", inicio_classe + 1)
if proximo_class == -1:
    proximo_class = len(conteudo_final)

# Extrair a classe completa
classe_completa = conteudo_final[inicio_classe:proximo_class]

# Salvar em arquivo temporário
with open("C:\\Users\\Pedro Victor\\OneDrive\\Área de Trabalho\\Documentos\\Projetos Automações e Digitais\\Luna\\sistema_ferramentas_completo_temp.txt", 'w', encoding='utf-8') as f:
    f.write(classe_completa)

print(f"✅ Classe extraída ({len(classe_completa)} caracteres)")
print(f"   Início: linha {conteudo_final[:inicio_classe].count(chr(10)) + 1}")
print(f"   Tamanho: {len(classe_completa)} caracteres")
