import re

with open('edital_texto_completo.txt', 'r', encoding='utf-8') as f:
    texto = f.read()

print("="*80)
print("BUSCANDO CONTEÚDO PROGRAMÁTICO ESPECÍFICO - CIRURGIÃO DENTISTA")
print("="*80)

# Busca por "CIRURGIÃO DENTISTA" ou "ODONTOLOGIA" em seções de conteúdo
padroes = [
    'CIRURGIÃO DENTISTA',
    'Cirurgião Dentista',
    'ODONTOLOGIA',
    'Odontologia',
    'CARGO: CIRURGIÃO DENTISTA',
    'CONHECIMENTOS ESPECÍFICOS'
]

for padrao in padroes:
    posicoes = []
    inicio = 0
    while True:
        pos = texto.find(padrao, inicio)
        if pos == -1:
            break
        posicoes.append(pos)
        inicio = pos + 1
    
    if posicoes:
        print(f"\n📍 '{padrao}' encontrado em {len(posicoes)} posição(ões)")
        for i, pos in enumerate(posicoes[:3], 1):  # Mostra apenas as 3 primeiras
            print(f"\n--- Ocorrência {i} (posição {pos}) ---")
            print(texto[max(0, pos-100):pos+1000])
            print("\n" + "-"*80)

# Busca específica por anexos relacionados
print("\n\n" + "="*80)
print("BUSCANDO ANEXOS RELACIONADOS AO CARGO")
print("="*80)

# Procura por anexos
anexo_pattern = r'ANEXO [IVX0-9]+'
anexos = re.finditer(anexo_pattern, texto)

for match in anexos:
    pos = match.start()
    trecho = texto[pos:pos+500]
    if 'Cirurgião' in trecho or 'Dentista' in trecho or 'Odontologia' in trecho:
        print(f"\n📄 Anexo relevante encontrado na posição {pos}:")
        print(texto[pos:pos+1500])
        print("\n" + "="*80)

# Salva resultado
with open('conteudo_especifico_odontologia.txt', 'w', encoding='utf-8') as f:
    f.write("CONTEÚDO PROGRAMÁTICO ESPECÍFICO - CIRURGIÃO DENTISTA\n")
    f.write("="*80 + "\n\n")
    
    # Busca seção específica
    for termo in ['CIRURGIÃO DENTISTA:', 'Cirurgião Dentista:', 'ODONTOLOGIA:']:
        pos = texto.find(termo)
        if pos != -1:
            # Captura até o próximo cargo ou seção
            fim = texto.find('\n\n\n', pos)
            if fim == -1:
                fim = pos + 3000
            
            conteudo = texto[pos:fim]
            f.write(conteudo)
            f.write("\n\n")

print("\n✅ Arquivo 'conteudo_especifico_odontologia.txt' criado!")
