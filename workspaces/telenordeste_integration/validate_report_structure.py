#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validação da estrutura do relatório JSON.

Verifica:
- Presença de todas as chaves obrigatórias
- Tipos de dados corretos
- Estruturas aninhadas válidas
- Valores None não intencionais
- Conformidade com formato JSON
"""

import json
import sys
from typing import Dict, List, Any, Tuple
from pathlib import Path


class ReportValidator:
    """Validador de estrutura de relatório de análise AST."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def validate_report(self, report: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """
        Valida estrutura completa do relatório.
        
        Returns:
            Tuple[bool, List[str], List[str]]: (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        # Validar chaves principais obrigatórias
        self._validate_main_keys(report)
        
        # Validar cada seção
        if 'summary' in report:
            self._validate_summary(report['summary'])
        
        if 'top_imports' in report:
            self._validate_top_imports(report['top_imports'])
            
        if 'files_by_comments' in report:
            self._validate_files_by_comments(report['files_by_comments'])
            
        if 'file_details' in report:
            self._validate_file_details(report['file_details'])
            
        if 'metadata' in report:
            self._validate_metadata(report['metadata'])
        
        # Validar serializabilidade JSON
        self._validate_json_serializable(report)
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings
    
    def _validate_main_keys(self, report: Dict[str, Any]) -> None:
        """Valida presença das chaves principais obrigatórias."""
        required_keys = {'summary', 'top_imports', 'files_by_comments', 'file_details', 'metadata'}
        missing_keys = required_keys - set(report.keys())
        
        if missing_keys:
            self.errors.append(f"Chaves obrigatórias faltando: {missing_keys}")
        
        # Verificar tipos das chaves principais
        if 'summary' in report and not isinstance(report['summary'], dict):
            self.errors.append(f"'summary' deve ser dict, encontrado: {type(report['summary'])}")
            
        if 'top_imports' in report and not isinstance(report['top_imports'], list):
            self.errors.append(f"'top_imports' deve ser list, encontrado: {type(report['top_imports'])}")
            
        if 'files_by_comments' in report and not isinstance(report['files_by_comments'], list):
            self.errors.append(f"'files_by_comments' deve ser list, encontrado: {type(report['files_by_comments'])}")
            
        if 'file_details' in report and not isinstance(report['file_details'], list):
            self.errors.append(f"'file_details' deve ser list, encontrado: {type(report['file_details'])}")
            
        if 'metadata' in report and not isinstance(report['metadata'], dict):
            self.errors.append(f"'metadata' deve ser dict, encontrado: {type(report['metadata'])}")
    
    def _validate_summary(self, summary: Dict[str, Any]) -> None:
        """Valida estrutura da seção summary."""
        required_fields = {
            'total_files': int,
            'total_lines': int,
            'total_code_lines': int,
            'total_comment_lines': int,
            'total_blank_lines': int,
            'total_functions': int,
            'total_classes': int,
            'total_imports': int,
            'files_with_errors': int,
            'average_lines_per_file': (int, float),
            'average_functions_per_file': (int, float),
            'average_classes_per_file': (int, float)
        }
        
        for field, expected_type in required_fields.items():
            if field not in summary:
                self.errors.append(f"summary.{field} está faltando")
            elif summary[field] is None:
                self.errors.append(f"summary.{field} não deve ser None")
            elif not isinstance(summary[field], expected_type):
                self.errors.append(
                    f"summary.{field} deve ser {expected_type}, encontrado: {type(summary[field])}"
                )
        
        # Validações de lógica
        if 'total_lines' in summary and 'total_code_lines' in summary:
            if summary['total_code_lines'] > summary['total_lines']:
                self.warnings.append(
                    "total_code_lines não deveria ser maior que total_lines"
                )
    
    def _validate_top_imports(self, top_imports: List[Dict[str, Any]]) -> None:
        """Valida estrutura da seção top_imports."""
        if not isinstance(top_imports, list):
            self.errors.append(f"top_imports deve ser list, encontrado: {type(top_imports)}")
            return
        
        for idx, import_entry in enumerate(top_imports):
            if not isinstance(import_entry, dict):
                self.errors.append(f"top_imports[{idx}] deve ser dict")
                continue
            
            required_fields = {'module': str, 'count': int, 'percentage': (int, float)}
            
            for field, expected_type in required_fields.items():
                if field not in import_entry:
                    self.errors.append(f"top_imports[{idx}].{field} está faltando")
                elif import_entry[field] is None:
                    self.errors.append(f"top_imports[{idx}].{field} não deve ser None")
                elif not isinstance(import_entry[field], expected_type):
                    self.errors.append(
                        f"top_imports[{idx}].{field} deve ser {expected_type}, "
                        f"encontrado: {type(import_entry[field])}"
                    )
            
            # Validar lógica de percentage
            if 'percentage' in import_entry:
                if not 0 <= import_entry['percentage'] <= 100:
                    self.warnings.append(
                        f"top_imports[{idx}].percentage fora do range 0-100: {import_entry['percentage']}"
                    )
    
    def _validate_files_by_comments(self, files_by_comments: List[Dict[str, Any]]) -> None:
        """Valida estrutura da seção files_by_comments."""
        if not isinstance(files_by_comments, list):
            self.errors.append(f"files_by_comments deve ser list, encontrado: {type(files_by_comments)}")
            return
        
        for idx, file_entry in enumerate(files_by_comments):
            if not isinstance(file_entry, dict):
                self.errors.append(f"files_by_comments[{idx}] deve ser dict")
                continue
            
            required_fields = {
                'filepath': str,
                'comment_lines': int,
                'code_lines': int,
                'comment_ratio': (int, float),
                'total_lines': int
            }
            
            for field, expected_type in required_fields.items():
                if field not in file_entry:
                    self.errors.append(f"files_by_comments[{idx}].{field} está faltando")
                elif file_entry[field] is None:
                    self.errors.append(f"files_by_comments[{idx}].{field} não deve ser None")
                elif not isinstance(file_entry[field], expected_type):
                    self.errors.append(
                        f"files_by_comments[{idx}].{field} deve ser {expected_type}, "
                        f"encontrado: {type(file_entry[field])}"
                    )
            
            # Validar comment_ratio
            if 'comment_ratio' in file_entry:
                if not 0 <= file_entry['comment_ratio'] <= 1:
                    self.warnings.append(
                        f"files_by_comments[{idx}].comment_ratio fora do range 0-1: "
                        f"{file_entry['comment_ratio']}"
                    )
    
    def _validate_file_details(self, file_details: List[Dict[str, Any]]) -> None:
        """Valida estrutura da seção file_details."""
        if not isinstance(file_details, list):
            self.errors.append(f"file_details deve ser list, encontrado: {type(file_details)}")
            return
        
        for idx, file_entry in enumerate(file_details):
            if not isinstance(file_entry, dict):
                self.errors.append(f"file_details[{idx}] deve ser dict")
                continue
            
            required_fields = {
                'filepath': str,
                'total_lines': int,
                'code_lines': int,
                'comment_lines': int,
                'blank_lines': int,
                'functions': int,
                'classes': int,
                'imports': list,
                'has_errors': bool
            }
            
            for field, expected_type in required_fields.items():
                if field not in file_entry:
                    self.errors.append(f"file_details[{idx}].{field} está faltando")
                elif file_entry[field] is None:
                    self.errors.append(f"file_details[{idx}].{field} não deve ser None")
                elif not isinstance(file_entry[field], expected_type):
                    self.errors.append(
                        f"file_details[{idx}].{field} deve ser {expected_type}, "
                        f"encontrado: {type(file_entry[field])}"
                    )
            
            # Validar lista de imports
            if 'imports' in file_entry and isinstance(file_entry['imports'], list):
                for imp_idx, imp in enumerate(file_entry['imports']):
                    if not isinstance(imp, str):
                        self.errors.append(
                            f"file_details[{idx}].imports[{imp_idx}] deve ser str, "
                            f"encontrado: {type(imp)}"
                        )
    
    def _validate_metadata(self, metadata: Dict[str, Any]) -> None:
        """Valida estrutura da seção metadata."""
        required_fields = {
            'timestamp': str,
            'analyzer_version': str,
            'format_version': str
        }
        
        for field, expected_type in required_fields.items():
            if field not in metadata:
                self.errors.append(f"metadata.{field} está faltando")
            elif metadata[field] is None:
                self.errors.append(f"metadata.{field} não deve ser None")
            elif not isinstance(metadata[field], expected_type):
                self.errors.append(
                    f"metadata.{field} deve ser {expected_type}, "
                    f"encontrado: {type(metadata[field])}"
                )
    
    def _validate_json_serializable(self, report: Dict[str, Any]) -> None:
        """Verifica se o relatório pode ser serializado para JSON."""
        try:
            json.dumps(report)
        except (TypeError, ValueError) as e:
            self.errors.append(f"Relatório não é serializável para JSON: {e}")
    
    def print_results(self, is_valid: bool, errors: List[str], warnings: List[str]) -> None:
        """Imprime resultados da validação de forma formatada."""
        print("\n" + "="*70)
        print("RESULTADO DA VALIDAÇÃO DO RELATÓRIO")
        print("="*70)
        
        if is_valid:
            print("\n✅ ESTRUTURA VÁLIDA - Todos os critérios foram atendidos!")
        else:
            print("\n❌ ESTRUTURA INVÁLIDA - Problemas encontrados!")
        
        if errors:
            print(f"\n🔴 ERROS ENCONTRADOS ({len(errors)}):")
            print("-" * 70)
            for i, error in enumerate(errors, 1):
                print(f"  {i}. {error}")
        
        if warnings:
            print(f"\n⚠️  AVISOS ({len(warnings)}):")
            print("-" * 70)
            for i, warning in enumerate(warnings, 1):
                print(f"  {i}. {warning}")
        
        if not errors and not warnings:
            print("\n✨ Nenhum erro ou aviso encontrado!")
        
        print("\n" + "="*70)
        print("RESUMO DA VALIDAÇÃO")
        print("="*70)
        print(f"Status: {'✅ VÁLIDO' if is_valid else '❌ INVÁLIDO'}")
        print(f"Erros: {len(errors)}")
        print(f"Avisos: {len(warnings)}")
        print("="*70 + "\n")


def main():
    """Função principal."""
    # Carregar relatório do arquivo
    report_file = Path("example_report.json")
    
    if not report_file.exists():
        print(f"❌ Erro: Arquivo '{report_file}' não encontrado!")
        sys.exit(1)
    
    try:
        with open(report_file, 'r', encoding='utf-8') as f:
            report = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao fazer parse do JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        sys.exit(1)
    
    # Validar relatório
    validator = ReportValidator()
    is_valid, errors, warnings = validator.validate_report(report)
    
    # Imprimir resultados
    validator.print_results(is_valid, errors, warnings)
    
    # Retornar código de saída apropriado
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
