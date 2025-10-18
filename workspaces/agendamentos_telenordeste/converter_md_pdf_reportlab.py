#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para converter Markdown para PDF usando apenas ReportLab
Sem dependências externas complexas
"""

import os
import glob
import re
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus import Table, TableStyle, Preformatted
from reportlab.lib import colors
from reportlab.lib.colors import HexColor

class MarkdownToPDF:
    """Conversor de Markdown para PDF"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._criar_estilos_customizados()
    
    def _criar_estilos_customizados(self):
        """Cria estilos customizados para o documento"""
        
        # Título principal
        self.styles.add(ParagraphStyle(
            name='CustomH1',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12,
            borderWidth=0,
            borderPadding=0,
            borderColor=HexColor('#3498db'),
            borderRadius=None,
        ))
        
        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='CustomH2',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=HexColor('#34495e'),
            spaceAfter=10,
            spaceBefore=10,
        ))
        
        # Subtítulo menor
        self.styles.add(ParagraphStyle(
            name='CustomH3',
            parent=self.styles['Heading3'],
            fontSize=13,
            textColor=HexColor('#5d6d7e'),
            spaceAfter=8,
            spaceBefore=8,
        ))
        
        # Código inline
        self.styles.add(ParagraphStyle(
            name='Code',
            parent=self.styles['Code'],
            fontSize=9,
            fontName='Courier',
            textColor=HexColor('#c7254e'),
            backColor=HexColor('#f9f2f4'),
        ))
        
        # Bloco de código
        self.styles.add(ParagraphStyle(
            name='CodeBlock',
            parent=self.styles['Code'],
            fontSize=8,
            fontName='Courier',
            leftIndent=20,
            rightIndent=20,
            backColor=HexColor('#f4f4f4'),
        ))
        
        # Lista
        self.styles.add(ParagraphStyle(
            name='CustomBullet',
            parent=self.styles['Normal'],
            fontSize=10,
            leftIndent=20,
            bulletIndent=10,
        ))
    
    def _processar_linha(self, linha):
        """Processa uma linha de Markdown e retorna elemento PDF"""
        linha = linha.rstrip()
        
        # Linha vazia
        if not linha:
            return Spacer(1, 0.2*cm)
        
        # Títulos
        if linha.startswith('# '):
            texto = linha[2:].strip()
            return Paragraph(texto, self.styles['CustomH1'])
        
        elif linha.startswith('## '):
            texto = linha[3:].strip()
            return Paragraph(texto, self.styles['CustomH2'])
        
        elif linha.startswith('### '):
            texto = linha[4:].strip()
            return Paragraph(texto, self.styles['CustomH3'])
        
        # Lista com marcadores
        elif linha.startswith('- ') or linha.startswith('* '):
            texto = linha[2:].strip()
            # Processa negrito e código inline
            texto = self._processar_formatacao(texto)
            return Paragraph(f"• {texto}", self.styles['CustomBullet'])
        
        # Lista numerada
        elif re.match(r'^\d+\.\s', linha):
            texto = re.sub(r'^\d+\.\s', '', linha).strip()
            texto = self._processar_formatacao(texto)
            numero = re.match(r'^(\d+)\.', linha).group(1)
            return Paragraph(f"{numero}. {texto}", self.styles['CustomBullet'])
        
        # Bloco de código (linhas que começam com 4 espaços ou tab)
        elif linha.startswith('    ') or linha.startswith('\t'):
            codigo = linha.strip()
            return Preformatted(codigo, self.styles['CodeBlock'])
        
        # Linha horizontal
        elif linha.strip() in ['---', '***', '___']:
            return Spacer(1, 0.5*cm)
        
        # Parágrafo normal
        else:
            texto = self._processar_formatacao(linha)
            return Paragraph(texto, self.styles['Normal'])
    
    def _processar_formatacao(self, texto):
        """Processa formatação inline (negrito, itálico, código)"""
        
        # Código inline `código`
        texto = re.sub(
            r'`([^`]+)`',
            r'<font name="Courier" color="#c7254e" backColor="#f9f2f4">\1</font>',
            texto
        )
        
        # Negrito **texto** ou __texto__
        texto = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', texto)
        texto = re.sub(r'__([^_]+)__', r'<b>\1</b>', texto)
        
        # Itálico *texto* ou _texto_
        texto = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', texto)
        texto = re.sub(r'_([^_]+)_', r'<i>\1</i>', texto)
        
        # Links [texto](url) - simplificado
        texto = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<u>\1</u>', texto)
        
        return texto
    
    def _processar_bloco_codigo(self, linhas, indice):
        """Processa bloco de código com ``` ```"""
        codigo_linhas = []
        i = indice + 1
        
        while i < len(linhas) and not linhas[i].strip().startswith('```'):
            codigo_linhas.append(linhas[i])
            i += 1
        
        codigo = '\n'.join(codigo_linhas)
        return Preformatted(codigo, self.styles['CodeBlock']), i
    
    def converter(self, arquivo_md, arquivo_pdf=None):
        """Converte arquivo Markdown para PDF"""
        try:
            if arquivo_pdf is None:
                arquivo_pdf = arquivo_md.replace('.md', '.pdf')
            
            print(f"📄 Convertendo: {arquivo_md} -> {arquivo_pdf}")
            
            # Lê o arquivo Markdown
            with open(arquivo_md, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
            
            # Cria documento PDF
            doc = SimpleDocTemplate(
                arquivo_pdf,
                pagesize=A4,
                rightMargin=2*cm,
                leftMargin=2*cm,
                topMargin=2*cm,
                bottomMargin=2*cm
            )
            
            # Processa linhas
            elementos = []
            i = 0
            em_bloco_codigo = False
            
            while i < len(linhas):
                linha = linhas[i]
                
                # Detecta início de bloco de código
                if linha.strip().startswith('```'):
                    elemento, nova_pos = self._processar_bloco_codigo(linhas, i)
                    elementos.append(elemento)
                    elementos.append(Spacer(1, 0.3*cm))
                    i = nova_pos + 1
                    continue
                
                # Processa linha normal
                elemento = self._processar_linha(linha)
                if elemento:
                    elementos.append(elemento)
                
                i += 1
            
            # Gera PDF
            doc.build(elementos)
            
            print(f"✅ Sucesso! PDF criado: {arquivo_pdf}\n")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao converter {arquivo_md}: {e}\n")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Converte todos os arquivos .md do diretório atual"""
    print("=" * 60)
    print("🔄 CONVERSOR DE MARKDOWN PARA PDF (ReportLab)")
    print("=" * 60)
    print()
    
    # Busca todos os arquivos .md
    arquivos_md = glob.glob("*.md")
    
    if not arquivos_md:
        print("❌ Nenhum arquivo .md encontrado no diretório atual")
        return
    
    print(f"📋 Encontrados {len(arquivos_md)} arquivos Markdown:")
    for arq in arquivos_md:
        print(f"   - {arq}")
    print()
    
    # Cria conversor
    conversor = MarkdownToPDF()
    
    # Converte cada arquivo
    sucessos = 0
    falhas = 0
    
    for arquivo_md in arquivos_md:
        if conversor.converter(arquivo_md):
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
        for pdf in sorted(pdfs):
            tamanho = os.path.getsize(pdf) / 1024  # KB
            print(f"   - {pdf} ({tamanho:.1f} KB)")

if __name__ == "__main__":
    main()
