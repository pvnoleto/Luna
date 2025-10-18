#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para converter arquivos Markdown para PDF
Usa markdown2 para converter MD -> HTML e weasyprint para HTML -> PDF
"""

import os
import glob
import markdown2
from weasyprint import HTML, CSS
from pathlib import Path

def criar_html_estilizado(conteudo_html, titulo="Documento"):
    """Cria HTML completo com estilos CSS"""
    return f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{titulo}</title>
        <style>
            @page {{
                size: A4;
                margin: 2cm;
            }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 100%;
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
                margin-top: 30px;
            }}
            h2 {{
                color: #34495e;
                border-bottom: 2px solid #95a5a6;
                padding-bottom: 8px;
                margin-top: 25px;
            }}
            h3 {{
                color: #5d6d7e;
                margin-top: 20px;
            }}
            code {{
                background-color: #f4f4f4;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
            }}
            pre {{
                background-color: #f4f4f4;
                border-left: 4px solid #3498db;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
            }}
            pre code {{
                background-color: transparent;
                padding: 0;
            }}
            ul, ol {{
                margin-left: 20px;
            }}
            li {{
                margin-bottom: 8px;
            }}
            blockquote {{
                border-left: 4px solid #e74c3c;
                padding-left: 15px;
                margin-left: 0;
                color: #555;
                font-style: italic;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #3498db;
                color: white;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            .footer {{
                margin-top: 50px;
                padding-top: 20px;
                border-top: 1px solid #ccc;
                font-size: 0.9em;
                color: #777;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        {conteudo_html}
        <div class="footer">
            <p>Documento gerado automaticamente</p>
        </div>
    </body>
    </html>
    """

def converter_md_para_pdf(arquivo_md, arquivo_pdf=None):
    """Converte um arquivo Markdown para PDF"""
    try:
        # Se não especificou o arquivo PDF, usa o mesmo nome do MD
        if arquivo_pdf is None:
            arquivo_pdf = arquivo_md.replace('.md', '.pdf')
        
        # Lê o arquivo Markdown
        print(f"📄 Lendo: {arquivo_md}")
        with open(arquivo_md, 'r', encoding='utf-8') as f:
            conteudo_md = f.read()
        
        # Converte Markdown para HTML
        print(f"🔄 Convertendo para HTML...")
        conteudo_html = markdown2.markdown(
            conteudo_md, 
            extras=[
                'fenced-code-blocks',
                'tables',
                'break-on-newline',
                'header-ids',
                'code-friendly',
                'cuddled-lists'
            ]
        )
        
        # Cria HTML completo com estilos
        titulo = Path(arquivo_md).stem
        html_completo = criar_html_estilizado(conteudo_html, titulo)
        
        # Converte HTML para PDF
        print(f"📝 Gerando PDF: {arquivo_pdf}")
        HTML(string=html_completo).write_pdf(arquivo_pdf)
        
        print(f"✅ Sucesso! PDF criado: {arquivo_pdf}\n")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao converter {arquivo_md}: {e}\n")
        return False

def main():
    """Converte todos os arquivos .md do diretório atual"""
    print("=" * 60)
    print("🔄 CONVERSOR DE MARKDOWN PARA PDF")
    print("=" * 60)
    print()
    
    # Busca todos os arquivos .md no diretório atual
    arquivos_md = glob.glob("*.md")
    
    if not arquivos_md:
        print("❌ Nenhum arquivo .md encontrado no diretório atual")
        return
    
    print(f"📋 Encontrados {len(arquivos_md)} arquivos Markdown:")
    for arq in arquivos_md:
        print(f"   - {arq}")
    print()
    
    # Converte cada arquivo
    sucessos = 0
    falhas = 0
    
    for arquivo_md in arquivos_md:
        if converter_md_para_pdf(arquivo_md):
            sucessos += 1
        else:
            falhas += 1
    
    # Resumo
    print("=" * 60)
    print("📊 RESUMO DA CONVERSÃO")
    print("=" * 60)
    print(f"✅ Sucessos: {sucessos}")
    print(f"❌ Falhas: {falhas}")
    print(f"📁 Total: {len(arquivos_md)} arquivos")
    print()
    
    # Lista os PDFs criados
    if sucessos > 0:
        print("📄 PDFs criados:")
        pdfs = glob.glob("*.pdf")
        for pdf in pdfs:
            tamanho = os.path.getsize(pdf) / 1024  # KB
            print(f"   - {pdf} ({tamanho:.1f} KB)")

if __name__ == "__main__":
    main()
