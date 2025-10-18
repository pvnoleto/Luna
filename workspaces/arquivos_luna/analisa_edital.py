with open('edital_texto_completo.txt', 'r', encoding='utf-8') as f:
    texto = f.read()

# Busca informações sobre Cirurgião Dentista
print("=== BUSCA 1: Cargo Cirurgião-Dentista ===")
if 'Cirurgião Dentista' in texto or 'Cirurgião-Dentista' in texto:
    inicio = texto.find('Cirurgião Dentista')
    if inicio == -1:
        inicio = texto.find('Cirurgião-Dentista')
    print(texto[max(0, inicio-200):inicio+800])
    
print("\n\n=== BUSCA 2: Tabela de Cargos ===")
tabela_inicio = texto.find('4. Cirurgião Dentista')
if tabela_inicio != -1:
    print(texto[tabela_inicio:tabela_inicio+300])

print("\n\n=== BUSCA 3: Anexos e Conteúdo Programático ===")
# Busca por anexos
for i in range(1, 10):
    anexo = f"ANEXO {i}"
    pos = texto.find(anexo)
    if pos != -1:
        print(f"\n{anexo} encontrado na posição {pos}")
        print(texto[pos:pos+500])

print("\n\n=== BUSCA 4: Conteúdo Programático ===")
prog = texto.find('CONTEÚDO PROGRAMÁTICO')
if prog == -1:
    prog = texto.find('Conteúdo Programático')
if prog != -1:
    print(texto[prog:prog+2000])

# Salva seções específicas
with open('info_cirurgiao_dentista.txt', 'w', encoding='utf-8') as f:
    f.write("INFORMAÇÕES EXTRAÍDAS DO EDITAL - CIRURGIÃO-DENTISTA\n")
    f.write("="*60 + "\n\n")
    
    # Busca cargo na tabela
    if '4. Cirurgião Dentista' in texto:
        idx = texto.find('4. Cirurgião Dentista')
        f.write("CARGO E REQUISITOS:\n")
        f.write(texto[idx:idx+500] + "\n\n")

print("\n\nArquivo 'info_cirurgiao_dentista.txt' criado!")
