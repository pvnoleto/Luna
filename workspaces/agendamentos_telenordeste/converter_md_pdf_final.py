#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para converter Markdown para PDF usando apenas ReportLab
"""

import os
import glob
import re
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.colors import HexColor

class MarkdownToPDF:
    """Conversor de Markdown para PDF"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._criar_estilos_customizados()
    
    def _criar_estilos_customizados(self):
        """Cria estilos customizados"""
        
        # H1
        self.styles.add(ParagraphStyle(
            name='CustomH1',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12,
        ))
        
        # H2
        self.styles.add(ParagraphStyle(
            name='CustomH2',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=HexColor('#34495e'),
            spaceAfter=10,
            spaceBefore=10,
        ))
        
        # H3
        self.styles.add(ParagraphStyle(
            name='CustomH3',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=HexColor('#5d6d7e'),
            spaceAfter=8,
            spaceBefore=8,
        ))
        
        # Bloco de código
        self.styles.add(ParagraphStyle(
            name='CustomCode',
            parent=self.styles['Code'],
            fontSize=8,
            fontName='Courier',
            leftIndent=15,
            rightIndent=15,
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
        """Processa uma linha de Markdown"""
        linha = linha.rstrip()
        
        if not linha:
            return Spacer(1, 0.2*cm)
        
        # Títulos
        if linha.startswith('# '):
            return Paragraph(linha[2:].strip(), self.styles['CustomH1'])
        
        elif linha.startswith('## '):
            return Paragraph(linha[3:].strip(), self.styles['CustomH2'])
        
        elif linha.startswith('### '):
            return Paragraph(linha[4:].strip(), self.styles['CustomH3'])
        
        # Lista
        elif linha.startswith('- ') or linha.startswith('* '):
            texto = self._processar_formatacao(linha[2:].strip())
            return Paragraph(f"• {texto}", self.styles['CustomBullet'])
        
        # Lista numerada
        elif re.match(r'^\d+\.\s', linha):
            texto = re.sub(r'^\d+\.\s', '', linha).strip()
            texto = self._processar_formatacao(texto)
            numero = re.match(r'^(\d+)\.', linha).group(1)
            return Paragraph(f"{numero}. {texto}", self.styles['CustomBullet'])
        
        # Bloco de código (4 espaços ou tab)
        elif linha.startswith('    ') or linha.startswith('\t'):
            return Preformatted(linha.strip(), self.styles['CustomCode'])
        
        # Linha horizontal
        elif linha.strip() in ['---', '***', '___']:
            return Spacer(1, 0.5*cm)
        
        # Parágrafo
        else:
            texto = self._processar_formatacao(linha)
            return Paragraph(texto, self.styles['Normal'])
    
    def _processar_formatacao(self, texto):
        """Processa formatação inline"""
        
        # Código inline
        texto = re.sub(
            r'`([^`]+)`',
            r'<font name="Courier" color="#c7254e">\1</font>',
            texto
        )
        
        # Negrito
        texto = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', texto)
        texto = re.sub(r'__([^_]+)__', r'<b>\1</b>', texto)
        
        # Itálico
        texto = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', texto)
        texto = re.sub(r'_([^_]+)_', r'<i>\1</i>', texto)
        
        # Links
        texto = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<u>\1</u>', texto)
        
        return texto
    
    def _processar_bloco_codigo(self, linhas, indice):
        """Processa bloco ``` ```"""
        codigo_linhas = []
        i = indice + 1
        
        while i < len(linhas) and not linhas[i].strip().startswith('```'):
            codigo_linhas.append(linhas[i].rstrip())
            i += 1
        
        codigo = '\n'.join(codigo_linhas)
        return Preformatted(codigo, self.styles['CustomCode']), i
    
    def converter(self, arquivo_md, arquivo_pdf=None):
        """Converte MD para PDF"""
        try:
            if arquivo_pdf is None:
                arquivo_pdf = arquivo_md.replace('.md', '.pdf')
            
            print(f"📄 {os.path.basename(arquivo_md)}")
            
            # Lê MD
            with open(arquivo_md, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
            
            # Cria PDF
            doc = SimpleDocTemplate(
                arquivo_pdf,
                pagesize=A4,
                rightMargin=2*cm,
                leftMargin=2*cm,
                topMargin=2*cm,
                bottomMargin=2*cm
            )
            
            # Processa
            elementos = []
            i = 0
            
            while i < len(linhas):
                linha = linhas[i]
                
                # Bloco de código
                if linha.strip().startswith('```'):
                    elemento, nova_pos = self._processar_bloco_codigo(linhas, i)
                    elementos.append(elemento)
                    elementos.append(Spacer(1, 0.3*cm))
                    i = nova_pos + 1
                    continue
                
                # Linha normal
                elemento = self._processar_linha(linha)
                if elemento:
                    elementos.append(elemento)
                
                i += 1
            
            # Gera
            doc.build(elementos)
            
            tamanho = os.path.getsize(arquivo_pdf) / 1024
            print(f"   ✅ {os.path.basename(arquivo_pdf)} ({tamanho:.1f} KB)\n")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro: {e}\n")
            return False

def main():
    """Converte todos MD para PDF"""
    print("=" * 60)
    print("🔄 CONVERSOR MARKDOWN → PDF")
    print("=" * 60)
    print()
    
    arquivos_md = glob.glob("*.md")
    
    if not arquivos_md:
        print("❌ Nenhum arquivo .md encontrado")
        return
    
    print(f"📋 {len(arquivos_md)} arquivos encontrados\n")
    
    conversor = MarkdownToPDF()
    
    sucessos = 0
    falhas = 0
    
    for arquivo_md in sorted(arquivos_md):
        if conversor.converter(arquivo_md):
            sucessos += 1
        else:
            falhas += 1
    
    print("=" * 60)
    print("📊 RESUMO")
    print("=" * 60)
    print(f"✅ Convertidos: {sucessos}")
    print(f"❌ Falhas: {falhas}")
    print(f"📁 Total: {len(arquivos_md)}")

if __name__ == "__main__":
    main()
