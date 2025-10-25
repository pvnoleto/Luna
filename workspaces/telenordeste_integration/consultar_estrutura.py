#!/usr/bin/env python3
"""
Script para consultar e validar a estrutura de diretórios do projeto.
Uso: python consultar_estrutura.py [comando]

Comandos:
  - show: Mostra estrutura completa
  - validate: Valida organização atual
  - locate <tipo>: Mostra onde salvar arquivo de determinado tipo
  - stats: Mostra estatísticas
"""

import json
import os
import sys
from pathlib import Path

class EstruturaDiretorios:
    def __init__(self):
        self.arquivo_json = "estrutura_mapeada.json"
        self.carregar_estrutura()
    
    def carregar_estrutura(self):
        """Carrega estrutura do arquivo JSON"""
        if os.path.exists(self.arquivo_json):
            with open(self.arquivo_json, 'r', encoding='utf-8') as f:
                self.estrutura = json.load(f)
        else:
            print(f"❌ Arquivo {self.arquivo_json} não encontrado!")
            sys.exit(1)
    
    def show(self):
        """Mostra estrutura completa"""
        print("\n" + "="*60)
        print("📁 ESTRUTURA DE DIRETÓRIOS - Telenordeste Integration")
        print("="*60)
        
        print(f"\n📍 Workspace: {self.estrutura['workspace']}")
        print(f"📂 Base Path: {self.estrutura['base_path']}")
        
        print("\n🗂️  PASTAS EXISTENTES:")
        for pasta, info in self.estrutura['estrutura_atual']['pastas'].items():
            print(f"\n  └─ {pasta}/ ({info['descricao']})")
            for arquivo in info['arquivos']:
                print(f"     ├─ {arquivo}")
        
        print("\n📊 MÉTRICAS:")
        for metrica, valor in self.estrutura['metricas'].items():
            print(f"  • {metrica.replace('_', ' ').title()}: {valor}")
    
    def validate(self):
        """Valida organização atual"""
        print("\n" + "="*60)
        print("🔍 VALIDAÇÃO DA ESTRUTURA")
        print("="*60)
        
        print("\n⚠️  PROBLEMAS IDENTIFICADOS:")
        for i, problema in enumerate(self.estrutura['problemas_identificados'], 1):
            print(f"  {i}. {problema}")
        
        print("\n✅ RECOMENDAÇÕES:")
        print("  • Criar pastas faltantes")
        print("  • Mover arquivos duplicados")
        print("  • Consolidar documentação em docs/")
        print("  • Organizar dados em data/")
        print("  • Limpar arquivos da raiz")
    
    def locate(self, tipo):
        """Mostra onde salvar arquivo de determinado tipo"""
        print("\n" + "="*60)
        print(f"📍 LOCALIZAÇÃO PARA: {tipo.upper()}")
        print("="*60)
        
        locais = self.estrutura['locais_salvamento']
        
        # Mapeia tipos comuns
        mapeamento = {
            'python': 'codigo_fonte',
            'py': 'codigo_fonte',
            'script': 'scripts_automacao',
            'doc': 'documentacao',
            'md': 'documentacao',
            'relatorio': 'relatorios',
            'config': 'configuracoes',
            'json': 'dados_analise',
            'txt': 'resultados',
            'png': 'screenshots',
            'jpg': 'screenshots',
            'html': 'html',
            'test': 'testes',
            'cliente': 'clientes_api',
            'bot': 'bots'
        }
        
        tipo_lower = tipo.lower()
        
        if tipo_lower in mapeamento:
            chave = mapeamento[tipo_lower]
            local = locais.get(chave, 'Não definido')
            print(f"\n✅ Salvar em: {local}")
            print(f"   Tipo: {chave.replace('_', ' ').title()}")
        else:
            print(f"\n❓ Tipo '{tipo}' não reconhecido.")
            print("\n📋 Tipos disponíveis:")
            for tipo_disp, chave in mapeamento.items():
                print(f"  • {tipo_disp} → {locais.get(chave, 'N/A')}")
    
    def stats(self):
        """Mostra estatísticas detalhadas"""
        print("\n" + "="*60)
        print("📊 ESTATÍSTICAS DETALHADAS")
        print("="*60)
        
        metricas = self.estrutura['metricas']
        
        print(f"\n📁 Total de Arquivos: {metricas['total_arquivos']}")
        print(f"📂 Total de Pastas: {metricas['total_pastas']}")
        
        print("\n📝 Distribuição por Tipo:")
        print(f"  • Python Scripts: {metricas['arquivos_python']}")
        print(f"  • Documentação: {metricas['arquivos_documentacao']}")
        print(f"  • Configuração: {metricas['arquivos_configuracao']}")
        print(f"  • Dados/Resultados: {metricas['arquivos_dados']}")
        print(f"  • Imagens: {metricas['arquivos_imagem']}")
        print(f"  • Batch Scripts: {metricas['scripts_batch']}")
        
        print("\n📈 Análise:")
        total = metricas['total_arquivos']
        print(f"  • Código: {metricas['arquivos_python']/total*100:.1f}%")
        print(f"  • Docs: {metricas['arquivos_documentacao']/total*100:.1f}%")
        print(f"  • Config: {metricas['arquivos_configuracao']/total*100:.1f}%")
        print(f"  • Dados: {metricas['arquivos_dados']/total*100:.1f}%")
    
    def help(self):
        """Mostra ajuda"""
        print(__doc__)

def main():
    estrutura = EstruturaDiretorios()
    
    if len(sys.argv) < 2:
        estrutura.show()
        return
    
    comando = sys.argv[1].lower()
    
    if comando == 'show':
        estrutura.show()
    elif comando == 'validate':
        estrutura.validate()
    elif comando == 'locate':
        if len(sys.argv) < 3:
            print("❌ Uso: python consultar_estrutura.py locate <tipo>")
            print("   Exemplo: python consultar_estrutura.py locate python")
        else:
            estrutura.locate(sys.argv[2])
    elif comando == 'stats':
        estrutura.stats()
    elif comando in ['help', '-h', '--help']:
        estrutura.help()
    else:
        print(f"❌ Comando '{comando}' não reconhecido.")
        estrutura.help()

if __name__ == "__main__":
    main()
