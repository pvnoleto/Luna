#!/usr/bin/env python3
"""
Ferramenta de Análise de Performance - Fibonacci
Analisa resultados de testes de performance e gera insights detalhados
"""

import json
import re
from datetime import datetime
from pathlib import Path


class FibonacciAnalyzer:
    """Analisador de resultados de performance do Fibonacci"""
    
    def __init__(self, results_file="fibonacci_results.txt"):
        self.results_file = results_file
        self.data = {}
        
    def parse_results(self):
        """Faz parsing do arquivo de resultados"""
        with open(self.results_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extrair informações principais
        self.data['valor_testado'] = self._extract_pattern(content, r'Valor testado: Fibonacci\((\d+)\)')
        self.data['data_hora'] = self._extract_pattern(content, r'Data/Hora: ([\d\-: ]+)')
        
        # Dados iterativo
        self.data['iterativo'] = {
            'status': self._extract_pattern(content, r'ITERATIVA.*?Status: (\w+)', section='ITERATIVA'),
            'iteracoes': int(self._extract_pattern(content, r'ITERATIVA.*?Iterações: (\d+)', section='ITERATIVA')),
            'resultado': int(self._extract_pattern(content, r'ITERATIVA.*?Resultado: (\d+)', section='ITERATIVA')),
            'tempo_medio': float(self._extract_pattern(content, r'ITERATIVA.*?Tempo médio.*?: ([\d.]+) ms', section='ITERATIVA')),
            'tempo_total': float(self._extract_pattern(content, r'ITERATIVA.*?Tempo total: ([\d.]+) ms', section='ITERATIVA'))
        }
        
        # Dados recursivo
        self.data['recursivo'] = {
            'status': self._extract_pattern(content, r'RECURSIVA.*?Status: (\w+)', section='RECURSIVA'),
            'iteracoes': int(self._extract_pattern(content, r'RECURSIVA.*?Iterações: (\d+)', section='RECURSIVA')),
            'resultado': int(self._extract_pattern(content, r'RECURSIVA.*?Resultado: (\d+)', section='RECURSIVA')),
            'tempo_medio': float(self._extract_pattern(content, r'RECURSIVA.*?Tempo médio.*?: ([\d.]+) ms', section='RECURSIVA')),
            'tempo_total': float(self._extract_pattern(content, r'RECURSIVA.*?Tempo total: ([\d.]+) ms', section='RECURSIVA'))
        }
        
        # Análise comparativa
        self.data['diferenca_absoluta'] = float(self._extract_pattern(content, r'Diferença absoluta: ([\d.]+) ms'))
        self.data['fator_diferenca'] = float(self._extract_pattern(content, r'Fator de diferença: ([\d.]+)x'))
        
    def _extract_pattern(self, text, pattern, section=None):
        """Extrai padrão usando regex"""
        if section:
            # Extrair seção específica primeiro
            section_pattern = f"{section}.*?(?=IMPLEMENTAÇÃO|ANÁLISE|$)"
            section_match = re.search(section_pattern, text, re.DOTALL)
            if section_match:
                text = section_match.group(0)
        
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1) if match else "N/A"
    
    def generate_statistics(self):
        """Gera estatísticas avançadas"""
        stats = {
            'eficiencia': {
                'iterativo_vs_recursivo': {
                    'velocidade_relativa': f"{self.data['fator_diferenca']:.2f}x mais rápido",
                    'economia_tempo': f"{self.data['diferenca_absoluta']:.2f} ms por execução",
                    'throughput_iterativo': f"{1000 / self.data['iterativo']['tempo_medio']:.2f} ops/s",
                    'throughput_recursivo': f"{1000 / self.data['recursivo']['tempo_medio']:.2f} ops/s"
                }
            },
            'recursos': {
                'iterativo_total_iterations': self.data['iterativo']['iteracoes'],
                'recursivo_total_iterations': self.data['recursivo']['iteracoes'],
                'razao_iteracoes': f"{self.data['iterativo']['iteracoes'] / self.data['recursivo']['iteracoes']:.2f}x"
            },
            'escalabilidade': {
                'complexidade_iterativa': 'O(n) - Linear',
                'complexidade_recursiva': 'O(2^n) - Exponencial',
                'espaco_iterativo': 'O(1) - Constante',
                'espaco_recursivo': 'O(n) - Linear (stack)'
            }
        }
        return stats
    
    def generate_visual_comparison(self):
        """Gera comparação visual ASCII"""
        iter_time = self.data['iterativo']['tempo_medio']
        rec_time = self.data['recursivo']['tempo_medio']
        
        # Normalizar para visualização (máximo 50 caracteres)
        max_bars = 50
        iter_bars = 1  # Sempre mínimo para iterativo
        rec_bars = min(int((rec_time / iter_time) * iter_bars), max_bars)
        
        visual = f"""
╔═══════════════════════════════════════════════════════════════════╗
║           COMPARAÇÃO VISUAL DE PERFORMANCE - FIBONACCI            ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  ITERATIVO  [{iter_time:.4f} ms]                                 ║
║  {'█' * iter_bars}                                                ║
║                                                                   ║
║  RECURSIVO  [{rec_time:.2f} ms]                                  ║
║  {'█' * min(rec_bars, 50)}{'...' if rec_bars > 50 else ''}       ║
║                                                                   ║
║  Fator: {self.data['fator_diferenca']:.0f}x mais lento           ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"""
        return visual
    
    def generate_recommendations(self):
        """Gera recomendações baseadas na análise"""
        recommendations = [
            {
                'categoria': 'Performance',
                'prioridade': 'ALTA',
                'titulo': 'Preferir Implementação Iterativa',
                'descricao': f'A versão iterativa é {self.data["fator_diferenca"]:.0f}x mais rápida. Use-a sempre que possível.',
                'impacto': f'Economia de {self.data["diferenca_absoluta"]:.2f} ms por execução'
            },
            {
                'categoria': 'Escalabilidade',
                'prioridade': 'ALTA',
                'titulo': 'Evitar Recursão para n >= 30',
                'descricao': 'A implementação recursiva tem complexidade exponencial O(2^n), tornando-se impraticável.',
                'impacto': 'Previne timeouts e uso excessivo de recursos'
            },
            {
                'categoria': 'Otimização',
                'prioridade': 'MÉDIA',
                'titulo': 'Considerar Memoization para Recursão',
                'descricao': 'Se recursão for necessária, use cache/memoization para reduzir complexidade para O(n).',
                'impacto': 'Melhoria de até 1000x em performance recursiva'
            },
            {
                'categoria': 'Recursos',
                'prioridade': 'MÉDIA',
                'titulo': 'Monitorar Uso de Stack',
                'descricao': 'Versão recursiva usa O(n) espaço na call stack, podendo causar stack overflow.',
                'impacto': 'Previne crashes em valores grandes de n'
            }
        ]
        return recommendations
    
    def save_analysis(self, output_file="fibonacci_comparison.txt"):
        """Salva análise completa em arquivo"""
        stats = self.generate_statistics()
        visual = self.generate_visual_comparison()
        recommendations = self.generate_recommendations()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("ANÁLISE COMPLETA DE PERFORMANCE - FIBONACCI\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"📊 Dados Analisados: {self.results_file}\n")
            f.write(f"📅 Data do Teste: {self.data['data_hora']}\n")
            f.write(f"🔢 Valor Testado: Fibonacci({self.data['valor_testado']})\n\n")
            
            f.write(visual + "\n\n")
            
            f.write("="*70 + "\n")
            f.write("ESTATÍSTICAS DETALHADAS\n")
            f.write("="*70 + "\n\n")
            
            f.write("⚡ EFICIÊNCIA\n")
            f.write("-" * 70 + "\n")
            for key, value in stats['eficiencia']['iterativo_vs_recursivo'].items():
                f.write(f"  • {key.replace('_', ' ').title()}: {value}\n")
            f.write("\n")
            
            f.write("💾 USO DE RECURSOS\n")
            f.write("-" * 70 + "\n")
            for key, value in stats['recursos'].items():
                f.write(f"  • {key.replace('_', ' ').title()}: {value}\n")
            f.write("\n")
            
            f.write("📈 ESCALABILIDADE\n")
            f.write("-" * 70 + "\n")
            for key, value in stats['escalabilidade'].items():
                f.write(f"  • {key.replace('_', ' ').title()}: {value}\n")
            f.write("\n")
            
            f.write("="*70 + "\n")
            f.write("RECOMENDAÇÕES\n")
            f.write("="*70 + "\n\n")
            
            for i, rec in enumerate(recommendations, 1):
                f.write(f"{i}. [{rec['prioridade']}] {rec['titulo']}\n")
                f.write(f"   Categoria: {rec['categoria']}\n")
                f.write(f"   Descrição: {rec['descricao']}\n")
                f.write(f"   Impacto: {rec['impacto']}\n\n")
            
            f.write("="*70 + "\n")
            f.write("CONCLUSÃO\n")
            f.write("="*70 + "\n\n")
            f.write(f"A análise demonstra que a implementação ITERATIVA é superior em todos\n")
            f.write(f"os aspectos para o cálculo de Fibonacci. Com uma diferença de performance\n")
            f.write(f"de {self.data['fator_diferenca']:.0f}x, a escolha é clara para aplicações de produção.\n\n")
            f.write(f"Para casos onde recursão é necessária (legibilidade, elegância), considere\n")
            f.write(f"técnicas de otimização como memoization ou dynamic programming.\n\n")
        
        print(f"✅ Análise salva em: {output_file}")
        return output_file
    
    def save_json(self, output_file="fibonacci_analysis.json"):
        """Salva dados estruturados em JSON"""
        analysis_data = {
            'metadata': {
                'arquivo_origem': self.results_file,
                'data_analise': datetime.now().isoformat(),
                'valor_testado': self.data['valor_testado'],
                'data_teste': self.data['data_hora']
            },
            'resultados': self.data,
            'estatisticas': self.generate_statistics(),
            'recomendacoes': self.generate_recommendations()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Dados JSON salvos em: {output_file}")
        return output_file


def main():
    """Função principal"""
    print("🔍 Iniciando análise de performance do Fibonacci...\n")
    
    analyzer = FibonacciAnalyzer()
    
    print("📖 Fazendo parsing dos resultados...")
    analyzer.parse_results()
    
    print("📊 Gerando estatísticas...")
    stats = analyzer.generate_statistics()
    
    print("📈 Criando visualizações...")
    visual = analyzer.generate_visual_comparison()
    print(visual)
    
    print("\n💾 Salvando análises...")
    analyzer.save_analysis()
    analyzer.save_json()
    
    print("\n✅ Análise completa!")
    print("\nArquivos gerados:")
    print("  • fibonacci_comparison.txt")
    print("  • fibonacci_analysis.json")


if __name__ == "__main__":
    main()
