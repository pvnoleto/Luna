import PyPDF2
import os

# Renomeia para .pdf
if os.path.exists('edital_page.html'):
    os.rename('edital_page.html', 'edital_concurso.pdf')
    print('Arquivo renomeado para edital_concurso.pdf')

# Extrai texto do PDF
with open('edital_concurso.pdf', 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    num_pages = len(pdf_reader.pages)
    print(f'Total de páginas: {num_pages}')
    
    full_text = ''
    for i, page in enumerate(pdf_reader.pages):
        text = page.extract_text()
        full_text += f'\n\n=== PÁGINA {i+1} ===\n\n' + text
        
    # Salva texto completo
    with open('edital_texto_completo.txt', 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    print(f'Texto extraído com sucesso! Total de caracteres: {len(full_text)}')
    print('\n--- Primeiras 3000 caracteres ---')
    print(full_text[:3000])
