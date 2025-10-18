#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para converter arquivos Markdown para PDF usando pypandoc
Requer pandoc instalado no sistema
"""

import os
import glob
import subprocess
from pathlib import Path

def verificar_pandoc():
    """Verifica se pandoc está instalado"""
    try:
        result = subprocess.run(['pandoc', '--version'], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        if result.returncode == 0:
            print("✅ Pandoc encontrado!")
            return True
    except:
        pass
    
    print("❌ Pandoc não encontrado. Tentando instalar...")
    return False

def instalar_pandoc():
    """Tenta instalar pandoc via pypandoc"""
    try:
        import pypandoc
        print("📦 Baixando e instalando Pandoc...")
        pypandoc.download_pandoc()
        print("✅ Pandoc instalado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao instalar pandoc: {e}")
        return False

def converter_md_para_pdf_pypandoc(arquivo_md, arquivo_pdf=None):
    """Converte MD para PDF usando pypandoc"""
    try:
        import pypandoc
        
        if arquivo_pdf is None:
            arquivo_pdf = arquivo_md.replace('.md', '.pdf')
        
        print(f"📄 Convertendo: {arquivo_md} -> {arquivo_pdf}")
        
        # Converte usando pypandoc
        pypandoc.convert_file(
            arquivo_md,
            'pdf',
            outputfile=arquivo_pdf,
            extra_args=[
                '--pdf-engine=xelatex',
                '-V', 'geometry:margin=2cm',
                '-V', 'fontsize=11pt',
                '--highlight-style=tango'
            ]
        )
        
        print(f"✅ Sucesso!\n")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}\n")
        return False

def converter_md_para_pdf_pandoc_direto(arquivo_md, arquivo_pdf=None):
    """Converte MD para PDF chamando pandoc diretamente"""
    try:
        if arquivo_pdf is None:
            arquivo_pdf = arquivo_md.replace('.md', '.pdf')
        
        print(f"📄 Convertendo: {arquivo_md} -> {arquivo_pdf}")
        
        # Chama pandoc diretamente
        cmd = [
            'pandoc',
            arquivo_md,
            '-o', arquivo_pdf,
            '--pdf-engine=xelatex',
            '-V', 'geometry:margin=2cm',
            '-V', 'fontsize=11pt',
            '--highlight-style=tango',
            '-V', 'mainfont=Arial'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ Sucesso!\n")
            return True
        else:
            print(f"❌ Erro: {result.stderr}\n")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}\n")
        return False

def converter_md_para_pdf_html(arquivo_md, arquivo_pdf=None):
    """Converte MD para PDF via HTML (fallback)"""
    try:
        import markdown2
        
        if arquivo_pdf is None:
            arquivo_pdf = arquivo_md.replace('.md', '.pdf')
        
        print(f"📄 Convertendo: {arquivo_md} -> {arquivo_pdf}")
        
        # Lê o Markdown
        with open(arquivo_md, 'r', encoding='utf-8') as f:
            conteudo_md = f.read()
        
        # Converte para HTML
        html = markdown2.markdown(
            conteudo_md,
            extras=['fenced-code-blocks', 'tables', 'break-on-newline']
        )
        
        # Cria HTML completo
        html_completo = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2cm; line-height: 1.6; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; }}
        h2 {{ color: #34495e; border-bottom: 1px solid #95a5a6; }}
        code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }}
        pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; }}
        th {{ background: #3498db; color: white; }}
    </style>
</head>
<body>
{html}
</body>
</html>
"""
        
        # Salva HTML temporário
        arquivo_html = arquivo_md.replace('.md', '_temp.html')
        with open(arquivo_html, 'w', encoding='utf-8') as f:
            f.write(html_completo)
        
        # Tenta converter HTML para PDF com pandoc
        cmd = ['pandoc', arquivo_html, '-o', arquivo_pdf, '--pdf-engine=xelatex']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        # Remove HTML temporário
        if os.path.exists(arquivo_html):
            os.remove(arquivo_html)
        
        if result.returncode == 0:
            print(f"✅ Sucesso!\n")
            return True
        else:
            print(f"❌ Erro: {result.stderr}\n")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}\n")
        return False

def main():
    """Converte todos os arquivos .md do diretório atual"""
    print("=" * 60)
    print("🔄 CONVERSOR DE MARKDOWN PARA PDF")
    print("=" * 60)
    print()
    
    # Verifica/instala pandoc
    pandoc_ok = verificar_pandoc()
    if not pandoc_ok:
        pandoc_ok = instalar_pandoc()
        if not pandoc_ok:
            print("\n⚠️  Pandoc não está disponível.")
            print("   Instale manualmente: https://pandoc.org/installing.html")
            print("   Ou instale via: choco install pandoc (Windows)")
            return
    
    print()
    
    # Busca arquivos .md
    arquivos_md = glob.glob("*.md")
    
    if not arquivos_md:
        print("❌ Nenhum arquivo .md encontrado")
        return
    
    print(f"📋 Encontrados {len(arquivos_md)} arquivos Markdown:")
    for arq in arquivos_md:
        print(f"   - {arq}")
    print()
    
    # Converte cada arquivo
    sucessos = 0
    falhas = 0
    
    for arquivo_md in arquivos_md:
        # Tenta primeiro com pypandoc
        if converter_md_para_pdf_pypandoc(arquivo_md):
            sucessos += 1
        # Se falhar, tenta chamando pandoc direto
        elif converter_md_para_pdf_pandoc_direto(arquivo_md):
            sucessos += 1
        # Se falhar, tenta via HTML
        elif converter_md_para_pdf_html(arquivo_md):
            sucessos += 1
        else:
            falhas += 1
    
    # Resumo
    print("=" * 60)
    print("📊 RESUMO")
    print("=" * 60)
    print(f"✅ Sucessos: {sucessos}")
    print(f"❌ Falhas: {falhas}")
    print(f"📁 Total: {len(arquivos_md)}")
    
    if sucessos > 0:
        print("\n📄 PDFs criados:")
        pdfs = glob.glob("*.pdf")
        for pdf in pdfs:
            tamanho = os.path.getsize(pdf) / 1024
            print(f"   - {pdf} ({tamanho:.1f} KB)")

if __name__ == "__main__":
    main()
