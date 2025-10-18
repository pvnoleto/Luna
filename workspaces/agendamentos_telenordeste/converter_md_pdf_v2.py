#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para converter Markdown para PDF - Versão melhorada
"""

import os
import glob
import re
import html
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.colors import HexColor

class MarkdownToPDF:
    """Conversor de Markdown para PDF"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._criar_estilos_customizados()
    
    def _criar_estilos_customizados(self):
        """Cria estilos customizados"""
        
        self.styles.add(ParagraphStyle(
            name='CustomH1',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12,
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomH2',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=HexColor('#34495e'),
            spaceAfter=10,
            spaceBefore=10,
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomH3',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=HexColor('#5d6d7e'),
            spaceAfter=8,
            spaceBefore=8,
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomCode',
            parent=self.styles['Code'],
            fontSize=8,
            fontName='Courier',
            leftIndent=15,
            rightIndent=15,
            backColor=HexColor('#f4f4f4'),
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBullet',
            parent=self.styles['Normal'],
            fontSize=10,
            leftIndent=20,
            bulletIndent=10,
        ))
    
    def _limpar_texto(self, texto):
        """Limpa e escapa texto para XML"""
        # Escapa caracteres especiais XML
        texto = html.escape(texto)
        # Reconverte entidades que precisamos manter
        texto = texto.replace('&lt;', '<').replace('&gt;', '>')
        return texto
    
    def _processar_formatacao(self, texto):
        """Processa formatação inline - versão simplificada e segura"""
        
        # Primeiro, remove todos os caracteres XML problemáticos
        texto_original = texto
        
        # Trata código inline PRIMEIRO (para evitar processar negrito/itálico dentro)
        partes_codigo = []
        def salvar_codigo(match):
            partes_codigo.append(match.group(1))
            return f"<<<CODIGO{len(partes_codigo)-1}>>>"
        
        texto = re.sub(r'`([^`]+)`', salvar_codigo, texto)
        
        # Agora processa negrito e itálico (sem conflito)
        # Negrito **texto**
        texto = re.sub(r'\*\*([^*]+?)\*\*', r'<b>\1</b>', texto)
        # Itálico *texto* (não pega ** já processado)
        texto = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<i>\1</i>', texto)
        
        # Links [texto](url) - simplificado, apenas sublinha
        texto = re.sub(r'\[([^\]]+?)\]\([^)]+?\)', r'<u>\1</u>', texto)
        
        # Restaura código inline
        for i, codigo in enumerate(partes_codigo):
            # Escapa o código e aplica formatação
            codigo_escapado = html.escape(codigo)
            texto = texto.replace(
                f"<<<CODIGO{i}>>>",
                f'<font name="Courier" color="#c7254e">{codigo_escapado}</font>'
            )
        
        return texto
    
    def _processar_linha(self, linha):
        """Processa uma linha de Markdown"""
        linha = linha.rstrip()
        
        if not linha:
            return Spacer(1, 0.2*cm)
        
        # Títulos
        if linha.startswith('# '):
            texto = linha[2:].strip()
            # Títulos não processam formatação inline para evitar problemas
            return Paragraph(html.escape(texto), self.styles['CustomH1'])
        
        elif linha.startswith('## '):
            texto = linha[3:].strip()
            return Paragraph(html.escape(texto), self.styles['CustomH2'])
        
        elif linha.startswith('### '):
            texto = linha[4:].strip()
            return Paragraph(html.escape(texto), self.styles['CustomH3'])
        
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
        
        # Bloco de código
        elif linha.startswith('    ') or linha.startswith('\t'):
            return Preformatted(linha.strip(), self.styles['CustomCode'])
        
        # Linha horizontal
        elif linha.strip() in ['---', '***', '___']:
            return Spacer(1, 0.5*cm)
        
        # Parágrafo
        else:
            texto = self._processar_formatacao(linha)
            return Paragraph(texto, self.styles['Normal'])
    
    def _processar_bloco_codigo(self, linhas, indice):
        """Processa bloco ```"""
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
            
            with open(arquivo_md, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
            
            doc = SimpleDocTemplate(
                arquivo_pdf,
                pagesize=A4,
                rightMargin=2*cm,
                leftMargin=2*cm,
                topMargin=2*cm,
                bottomMargin=2*cm
            )
            
            elementos = []
            i = 0
            
            while i < len(linhas):
                linha = linhas[i]
                
                if linha.strip().startswith('```'):
                    elemento, nova_pos = self._processar_bloco_codigo(linhas, i)
                    elementos.append(elemento)
                    elementos.append(Spacer(1, 0.3*cm))
                    i = nova_pos + 1
                    continue
                
                try:
                    elemento = self._processar_linha(linha)
                    if elemento:
                        elementos.append(elemento)
                except Exception as e:
                    # Se der erro, adiciona texto puro
                    print(f"   ⚠️  Linha {i}: {str(e)[:50]}")
                    elementos.append(Paragraph(html.escape(linha.strip()), self.styles['Normal']))
                
                i += 1
            
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
    print("🔄 CONVERSOR MARKDOWN → PDF (v2)")
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
    
    if sucessos > 0:
        print("\n📄 PDFs criados no workspace atual")

if __name__ == "__main__":
    main()
