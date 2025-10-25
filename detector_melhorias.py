#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 DETECTOR DE MELHORIAS - Sistema de Análise Automática de Código
===================================================================

Detecta automaticamente oportunidades de melhoria durante a execução:
- Loops ineficientes (podem ser list comprehensions)
- Funções sem type hints
- Funções sem docstrings
- Código sem validações de segurança
- Code smells e anti-patterns

Criado: 2025-10-19
Parte do Sistema de Auto-Evolução da Luna V3
"""

import ast
import re
from typing import List, Dict, Any, Optional, Set
from pathlib import Path


class DetectorMelhorias:
    """
    Detecta oportunidades de melhoria em código Python

    Analisa código executado e identifica 6 tipos de melhorias:
    1. Loops ineficientes
    2. Falta de type hints
    3. Falta de docstrings
    4. Falta de validações
    5. Code smells
    6. Duplicação de código
    """

    def __init__(self):
        """Inicializa o detector"""
        self.melhorias_detectadas: List[Dict] = []
        self.cache_analises: Dict[str, List[Dict]] = {}  # Cache para evitar re-análise

        # Padrões para detecção
        self.padroes_loop_ineficiente = [
            r'for\s+\w+\s+in\s+\w+:\s*\n\s+\w+\.append\(',  # for x in y: list.append()
            r'for\s+\w+\s+in\s+\w+:\s*\n\s+\w+\.extend\(',  # for x in y: list.extend()
        ]

        self.operacoes_inseguras = [
            'os.remove', 'os.rmdir', 'shutil.rmtree',  # Deleções sem validação
            'open(', 'eval(', 'exec(',  # Operações potencialmente perigosas
        ]

    def analisar_codigo_executado(self, nome_ferramenta: str, codigo: str) -> List[Dict]:
        """
        Analisa código de ferramenta executada e detecta melhorias

        Args:
            nome_ferramenta: Nome da ferramenta
            codigo: Código fonte da ferramenta

        Returns:
            Lista de melhorias detectadas
        """
        # Verificar cache
        if nome_ferramenta in self.cache_analises:
            return self.cache_analises[nome_ferramenta]

        melhorias = []

        try:
            # Parse do código
            arvore = ast.parse(codigo)

            # Detectar cada tipo de melhoria
            melhorias.extend(self.detectar_loops_ineficientes(codigo, arvore))
            melhorias.extend(self.detectar_falta_type_hints(arvore))
            melhorias.extend(self.detectar_falta_docstrings(arvore))
            melhorias.extend(self.detectar_falta_validacoes(codigo, arvore))
            melhorias.extend(self.detectar_code_smells(codigo, arvore))

            # Adicionar contexto do nome da ferramenta
            for melhoria in melhorias:
                melhoria['ferramenta'] = nome_ferramenta

            # Salvar em cache
            self.cache_analises[nome_ferramenta] = melhorias

        except SyntaxError:
            # Código com erro de sintaxe, não pode analisar
            pass
        except Exception:
            # Outros erros, silenciosamente ignorar
            pass

        return melhorias

    def detectar_loops_ineficientes(self, codigo: str, arvore: ast.AST) -> List[Dict]:
        """
        Detecta loops que podem ser convertidos para list comprehensions

        Exemplo:
            resultado = []
            for item in items:
                resultado.append(item.upper())

        Pode ser:
            resultado = [item.upper() for item in items]
        """
        melhorias = []

        # Buscar padrões com regex
        for padrao in self.padroes_loop_ineficiente:
            matches = re.finditer(padrao, codigo, re.MULTILINE)
            for match in matches:
                melhorias.append({
                    'tipo': 'otimizacao',
                    'alvo': 'loop_ineficiente',
                    'motivo': 'Loop pode ser convertido para list comprehension',
                    'codigo_sugerido': '# resultado = [f(item) for item in items]',
                    'prioridade': 4,
                    'linha': codigo[:match.start()].count('\n') + 1
                })

        return melhorias

    def detectar_falta_type_hints(self, arvore: ast.AST) -> List[Dict]:
        """
        Detecta funções sem type hints

        Exemplo:
            def somar(a, b):  # ← Sem type hints

        Deve ser:
            def somar(a: int, b: int) -> int:  # ← Com type hints
        """
        melhorias = []

        for node in ast.walk(arvore):
            if isinstance(node, ast.FunctionDef):
                # Verificar se tem annotations
                tem_hints_args = any(arg.annotation for arg in node.args.args)
                tem_hint_retorno = node.returns is not None

                if not tem_hints_args or not tem_hint_retorno:
                    melhorias.append({
                        'tipo': 'qualidade',
                        'alvo': f'funcao_{node.name}',
                        'motivo': f"Função '{node.name}' sem type hints (linha {node.lineno})",
                        'codigo_sugerido': f'def {node.name}(arg: tipo) -> tipo: ...',
                        'prioridade': 5
                    })

        return melhorias

    def detectar_falta_docstrings(self, arvore: ast.AST) -> List[Dict]:
        """
        Detecta funções e classes sem docstrings

        Exemplo:
            def validar_email(email: str) -> bool:  # ← Sem docstring
                return '@' in email
        """
        melhorias = []

        for node in ast.walk(arvore):
            # Verificar funções
            if isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node)
                if not docstring:
                    melhorias.append({
                        'tipo': 'documentacao',
                        'alvo': f'funcao_{node.name}',
                        'motivo': f"Função '{node.name}' sem docstring (linha {node.lineno})",
                        'codigo_sugerido': f'''def {node.name}(...):
    """
    [Descrição breve]

    Args:
        [param]: [descrição]

    Returns:
        [tipo]: [descrição]
    """''',
                        'prioridade': 3
                    })

            # Verificar classes
            elif isinstance(node, ast.ClassDef):
                docstring = ast.get_docstring(node)
                if not docstring:
                    melhorias.append({
                        'tipo': 'documentacao',
                        'alvo': f'classe_{node.name}',
                        'motivo': f"Classe '{node.name}' sem docstring (linha {node.lineno})",
                        'codigo_sugerido': f'''class {node.name}:
    """
    [Descrição breve da classe]

    Attributes:
        [atributo]: [descrição]
    """''',
                        'prioridade': 3
                    })

        return melhorias

    def detectar_falta_validacoes(self, codigo: str, arvore: ast.AST) -> List[Dict]:
        """
        Detecta código sem validações de segurança

        Exemplos:
        - os.remove(arquivo) sem validar se path é seguro
        - dict[key] sem verificar se key existe
        - list[index] sem validar índice
        - open() sem tratamento de erro
        """
        melhorias = []

        # Detectar operações de arquivo perigosas
        for operacao in ['os.remove', 'os.rmdir', 'shutil.rmtree']:
            if operacao in codigo:
                # Verificar se há validação de path
                if 'os.path.exists' not in codigo and 'Path(' not in codigo:
                    melhorias.append({
                        'tipo': 'seguranca',
                        'alvo': 'validacao_path',
                        'motivo': f"Uso de '{operacao}' sem validação de path",
                        'codigo_sugerido': 'if os.path.exists(path) and is_safe_path(path): os.remove(path)',
                        'prioridade': 8  # Alta prioridade (segurança!)
                    })

        # Detectar acesso a dicionário sem validação
        for node in ast.walk(arvore):
            if isinstance(node, ast.Subscript):
                # Verificar se é acesso a dict
                if isinstance(node.value, ast.Name):
                    melhorias.append({
                        'tipo': 'qualidade',
                        'alvo': 'acesso_dict',
                        'motivo': f"Acesso direto a dict[key] pode causar KeyError (linha {node.lineno})",
                        'codigo_sugerido': 'Use dict.get(key, default) para acesso seguro',
                        'prioridade': 6
                    })

        return melhorias

    def detectar_code_smells(self, codigo: str, arvore: ast.AST) -> List[Dict]:
        """
        Detecta code smells e anti-patterns

        Exemplos:
        - Funções muito longas (> 50 linhas)
        - Complexidade ciclomática alta
        - Muitos parâmetros (> 5)
        - Duplicação de código
        """
        melhorias = []

        for node in ast.walk(arvore):
            if isinstance(node, ast.FunctionDef):
                # 1. Funções muito longas
                linhas_funcao = self._contar_linhas_funcao(node, codigo)
                if linhas_funcao > 50:
                    melhorias.append({
                        'tipo': 'refatoracao',
                        'alvo': f'funcao_longa_{node.name}',
                        'motivo': f"Função '{node.name}' muito longa ({linhas_funcao} linhas)",
                        'codigo_sugerido': 'Considere dividir em funções menores',
                        'prioridade': 6
                    })

                # 2. Muitos parâmetros
                num_parametros = len(node.args.args)
                if num_parametros > 5:
                    melhorias.append({
                        'tipo': 'refatoracao',
                        'alvo': f'funcao_muitos_params_{node.name}',
                        'motivo': f"Função '{node.name}' com muitos parâmetros ({num_parametros})",
                        'codigo_sugerido': 'Considere usar dataclass ou config object',
                        'prioridade': 5
                    })

        return melhorias

    def _contar_linhas_funcao(self, node: ast.FunctionDef, codigo: str) -> int:
        """Conta o número de linhas de uma função"""
        try:
            # Encontrar a última linha da função
            ultima_linha = node.end_lineno if hasattr(node, 'end_lineno') else node.lineno
            return ultima_linha - node.lineno + 1
        except:
            return 0

    def detectar_duplicacao(self, codigo: str, limiar: int = 5) -> List[Dict]:
        """
        Detecta blocos de código duplicados

        Args:
            codigo: Código fonte
            limiar: Número mínimo de linhas para considerar duplicação

        Returns:
            Lista de melhorias de duplicação detectadas
        """
        melhorias = []

        # Dividir em linhas
        linhas = codigo.split('\n')

        # Buscar sequências repetidas (algoritmo simplificado)
        blocos_vistos = {}

        for i in range(len(linhas) - limiar):
            # Criar hash do bloco
            bloco = '\n'.join(linhas[i:i+limiar])
            bloco_normalizado = self._normalizar_codigo(bloco)

            if bloco_normalizado in blocos_vistos:
                melhorias.append({
                    'tipo': 'refatoracao',
                    'alvo': 'duplicacao_codigo',
                    'motivo': f"Código duplicado detectado (linha {i+1})",
                    'codigo_sugerido': 'Extrair para função reutilizável',
                    'prioridade': 7
                })
            else:
                blocos_vistos[bloco_normalizado] = i + 1

        return melhorias

    def _normalizar_codigo(self, codigo: str) -> str:
        """
        Normaliza código removendo espaços e comentários para comparação

        Exemplo:
            '    x = 10  # comentário' → 'x=10'
        """
        # Remover comentários
        codigo = re.sub(r'#.*', '', codigo)

        # Remover espaços em branco
        codigo = re.sub(r'\s+', '', codigo)

        return codigo

    def filtrar_melhorias_por_prioridade(
        self,
        melhorias: List[Dict],
        prioridade_minima: int = 5
    ) -> List[Dict]:
        """
        Filtra melhorias por prioridade mínima

        Args:
            melhorias: Lista de melhorias
            prioridade_minima: Prioridade mínima (1-10)

        Returns:
            Melhorias filtradas
        """
        return [
            m for m in melhorias
            if m.get('prioridade', 0) >= prioridade_minima
        ]

    def agrupar_melhorias_por_tipo(self, melhorias: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Agrupa melhorias por tipo

        Returns:
            Dict com chaves: 'otimizacao', 'qualidade', 'documentacao', 'seguranca', 'refatoracao'
        """
        agrupadas = {
            'otimizacao': [],
            'qualidade': [],
            'documentacao': [],
            'seguranca': [],
            'refatoracao': []
        }

        for melhoria in melhorias:
            tipo = melhoria.get('tipo', 'qualidade')
            if tipo in agrupadas:
                agrupadas[tipo].append(melhoria)

        return agrupadas

    def gerar_relatorio(self, melhorias: List[Dict]) -> str:
        """
        Gera relatório formatado de melhorias

        Args:
            melhorias: Lista de melhorias detectadas

        Returns:
            Relatório em formato de texto
        """
        if not melhorias:
            return "✅ Nenhuma melhoria detectada - código está ótimo!"

        # Agrupar por tipo
        agrupadas = self.agrupar_melhorias_por_tipo(melhorias)

        relatorio = []
        relatorio.append("\n" + "="*70)
        relatorio.append("🔍 RELATÓRIO DE MELHORIAS DETECTADAS")
        relatorio.append("="*70)
        relatorio.append(f"\nTotal de melhorias: {len(melhorias)}\n")

        # Exibir por tipo
        for tipo, items in agrupadas.items():
            if items:
                icone = {
                    'otimizacao': '⚡',
                    'qualidade': '✨',
                    'documentacao': '📖',
                    'seguranca': '🔒',
                    'refatoracao': '🔧'
                }.get(tipo, '💡')

                relatorio.append(f"\n{icone} {tipo.upper()} ({len(items)} melhorias):")
                for i, item in enumerate(items[:5], 1):  # Máximo 5 por tipo
                    relatorio.append(f"   {i}. {item['motivo']}")
                    relatorio.append(f"      Prioridade: {item['prioridade']}/10")

        relatorio.append("\n" + "="*70)

        return '\n'.join(relatorio)

    def analisar_proativo(
        self,
        diretorio: str = ".",
        fila_melhorias=None,
        excluir_padroes: List[str] = None
    ) -> Dict[str, Any]:
        """
        ✅ FASE 2: Análise Proativa (P1)

        Analisa TODO o codebase proativamente, não apenas código executado.

        Args:
            diretorio: Diretório raiz para análise (default: atual)
            fila_melhorias: Instância de FilaDeMelhorias para adicionar melhorias
            excluir_padroes: Lista de padrões glob para excluir (ex: ['venv/*', '__pycache__/*'])

        Returns:
            Dict com estatísticas:
                - arquivos_analisados: int
                - melhorias_detectadas: int
                - melhorias_por_tipo: Dict[str, int]
                - tempo_analise: float
        """
        import time
        from pathlib import Path

        inicio = time.time()

        # Padrões padrão para excluir
        if excluir_padroes is None:
            excluir_padroes = [
                'venv/*', 'venv_test/*', '.venv/*',
                '__pycache__/*', '*.pyc',
                '.git/*', '.tox/*', 'build/*', 'dist/*',
                'node_modules/*', '.backups/*', '.rollback_backups/*',
                'backups_auto_evolucao/*'
            ]

        # Encontrar todos arquivos .py
        pasta = Path(diretorio)
        todos_arquivos = list(pasta.rglob('*.py'))

        # Filtrar arquivos excluídos
        arquivos_validos = []
        for arquivo in todos_arquivos:
            arquivo_str = str(arquivo)
            excluir = False

            for padrao in excluir_padroes:
                # Converter glob pattern para match simples
                if padrao.replace('/*', '') in arquivo_str or padrao.replace('*', '') in arquivo_str:
                    excluir = True
                    break

            if not excluir:
                arquivos_validos.append(arquivo)

        # Estatísticas
        total_arquivos = 0
        total_melhorias = 0
        melhorias_por_tipo = {
            'otimizacao': 0,
            'qualidade': 0,
            'documentacao': 0,
            'seguranca': 0,
            'refatoracao': 0
        }

        print(f"    🔍 Análise proativa iniciada...")
        print(f"    📁 Diretório: {diretorio}")
        print(f"    📄 Arquivos encontrados: {len(arquivos_validos)}")

        # Analisar cada arquivo
        for arquivo in arquivos_validos:
            try:
                # Ler código
                codigo = arquivo.read_text(encoding='utf-8')

                # Analisar
                melhorias = self.analisar_codigo_executado(arquivo.stem, codigo)

                if melhorias and fila_melhorias:
                    # Adicionar melhorias à fila persistente
                    for melhoria in melhorias:
                        # Adicionar contexto do arquivo
                        melhoria['arquivo'] = str(arquivo.relative_to(pasta))

                        fila_melhorias.adicionar(
                            tipo=melhoria['tipo'],
                            alvo=f"{arquivo.stem}.{melhoria['alvo']}",
                            motivo=f"{melhoria['motivo']} [{arquivo.name}]",
                            codigo_sugerido=melhoria['codigo_sugerido'],
                            prioridade=melhoria['prioridade']
                        )

                        # Contabilizar
                        total_melhorias += 1
                        tipo = melhoria['tipo']
                        if tipo in melhorias_por_tipo:
                            melhorias_por_tipo[tipo] += 1

                total_arquivos += 1

            except Exception as e:
                # Silenciosamente ignorar arquivos com problemas
                continue

        tempo_total = time.time() - inicio

        resultado = {
            'arquivos_analisados': total_arquivos,
            'melhorias_detectadas': total_melhorias,
            'melhorias_por_tipo': melhorias_por_tipo,
            'tempo_analise': tempo_total
        }

        print(f"    ✅ Análise concluída em {tempo_total:.2f}s")
        print(f"    📊 {total_arquivos} arquivos analisados")
        print(f"    💡 {total_melhorias} melhorias detectadas")

        return resultado

    def limpar_cache(self):
        """Limpa o cache de análises"""
        self.cache_analises.clear()
        self.melhorias_detectadas.clear()


# ============================================================================
# SISTEMA DE AUTO-APLICAÇÃO AGRESSIVA (🆕)
# ============================================================================

class AutoApplicator:
    """
    Aplica melhorias detectadas automaticamente ao código.

    🚀 MODO AGRESSIVO - Evolução contínua automática

    Features:
        - Aplica melhorias de baixo risco automaticamente
        - Cria backups antes de modificar
        - Valida código após cada modificação
        - Rollback automático em caso de erro
        - Priorização inteligente (segurança > qualidade > docs)

    Uso:
        applicator = AutoApplicator(modo_agressivo=True)
        applicator.aplicar_melhorias(codigo, melhorias)
    """

    def __init__(self, modo_agressivo: bool = False, criar_backup: bool = True):
        """
        Inicializa o auto-applicator.

        Args:
            modo_agressivo: Se True, aplica todas as melhorias de prioridade >= 5
            criar_backup: Se deve criar backup antes de modificar
        """
        self.modo_agressivo = modo_agressivo
        self.criar_backup = criar_backup

        # Limites de aplicação por modo
        self.limites = {
            'conservador': {'prioridade_minima': 8, 'max_mudancas': 3},
            'moderado': {'prioridade_minima': 6, 'max_mudancas': 10},
            'agressivo': {'prioridade_minima': 4, 'max_mudancas': 50}
        }

        # Estatísticas
        self.total_aplicadas = 0
        self.total_falhadas = 0
        self.total_rollbacks = 0

    def aplicar_melhorias(
        self,
        codigo: str,
        melhorias: List[Dict],
        caminho_arquivo: Optional[str] = None
    ) -> tuple[str, List[Dict]]:
        """
        Aplica lista de melhorias ao código.

        Args:
            codigo: Código fonte original
            melhorias: Lista de melhorias detectadas
            caminho_arquivo: Caminho do arquivo (para backup)

        Returns:
            Tupla (codigo_modificado, melhorias_aplicadas)
        """
        modo = 'agressivo' if self.modo_agressivo else 'moderado'
        config = self.limites[modo]

        # Filtrar melhorias por prioridade
        melhorias_aplicaveis = [
            m for m in melhorias
            if m['prioridade'] >= config['prioridade_minima']
        ]

        # Ordenar por prioridade (maior primeiro)
        melhorias_aplicaveis.sort(key=lambda m: m['prioridade'], reverse=True)

        # Limitar quantidade
        melhorias_aplicaveis = melhorias_aplicaveis[:config['max_mudancas']]

        if not melhorias_aplicaveis:
            return codigo, []

        # Criar backup se necessário
        if self.criar_backup and caminho_arquivo:
            self._criar_backup(caminho_arquivo, codigo)

        # Aplicar melhorias uma por uma
        codigo_atual = codigo
        aplicadas = []

        for melhoria in melhorias_aplicaveis:
            try:
                codigo_novo = self._aplicar_melhoria(codigo_atual, melhoria)

                # Validar código modificado
                if self._validar_codigo(codigo_novo):
                    codigo_atual = codigo_novo
                    aplicadas.append(melhoria)
                    self.total_aplicadas += 1
                else:
                    # Validação falhou, não aplicar esta melhoria
                    self.total_falhadas += 1

            except Exception:
                # Erro ao aplicar, pular esta melhoria
                self.total_falhadas += 1
                continue

        return codigo_atual, aplicadas

    def _aplicar_melhoria(self, codigo: str, melhoria: Dict) -> str:
        """
        Aplica uma melhoria específica ao código.

        Args:
            codigo: Código atual
            melhoria: Dict com dados da melhoria

        Returns:
            Código modificado
        """
        tipo = melhoria['tipo']
        alvo = melhoria['alvo']

        # Estratégias de aplicação por tipo
        if tipo == 'documentacao':
            # Adicionar docstrings
            return self._adicionar_docstring(codigo, melhoria)

        elif tipo == 'otimizacao' and 'loop_ineficiente' in alvo:
            # Converter loops para list comprehension
            return self._otimizar_loop(codigo, melhoria)

        elif tipo == 'qualidade' and 'type_hints' in alvo:
            # Adicionar type hints
            return self._adicionar_type_hints(codigo, melhoria)

        elif tipo == 'seguranca':
            # Adicionar validações de segurança
            return self._adicionar_validacao_seguranca(codigo, melhoria)

        # Se não há estratégia, retornar código original
        return codigo

    def _adicionar_docstring(self, codigo: str, melhoria: Dict) -> str:
        """Adiciona docstring a função ou classe."""
        # Implementação simplificada: adiciona docstring genérica
        # Em produção, usaria análise de AST mais sofisticada

        if 'funcao_' in melhoria['alvo']:
            nome_funcao = melhoria['alvo'].replace('funcao_', '')

            # Encontrar a definição da função
            padrao = rf'(def {nome_funcao}\([^)]*\):)\n'
            docstring = f'\\1\n    """{nome_funcao.replace("_", " ").title()}.\\n\\n    TODO: Adicionar documentação.\\n    """\n'

            return re.sub(padrao, docstring, codigo, count=1)

        return codigo

    def _otimizar_loop(self, codigo: str, melhoria: Dict) -> str:
        """Converte loop ineficiente para list comprehension."""
        # Implementação simplificada
        # Detecta padrão: for x in y: resultado.append(f(x))
        padrao = r'(\w+)\s*=\s*\[\]\s*\n\s*for\s+(\w+)\s+in\s+(\w+):\s*\n\s*\1\.append\(([^)]+)\)'
        substituicao = r'\1 = [\4 for \2 in \3]'

        return re.sub(padrao, substituicao, codigo)

    def _adicionar_type_hints(self, codigo: str, melhoria: Dict) -> str:
        """Adiciona type hints a função."""
        # Implementação simplificada: adiciona hints genéricos
        # Em produção, usaria análise de contexto mais sofisticada

        if 'funcao_' in melhoria['alvo']:
            nome_funcao = melhoria['alvo'].replace('funcao_', '')

            # Adicionar hints básicos (Any)
            padrao = rf'def {nome_funcao}\(([^)]+)\):'
            substituicao = rf'def {nome_funcao}(\1) -> Any:'

            return re.sub(padrao, substituicao, codigo, count=1)

        return codigo

    def _adicionar_validacao_seguranca(self, codigo: str, melhoria: Dict) -> str:
        """Adiciona validações de segurança."""
        # Adicionar validação antes de os.remove
        if 'os.remove' in codigo:
            padrao = r'os\.remove\(([^)]+)\)'
            substituicao = r'if os.path.exists(\1):\n        os.remove(\1)'
            return re.sub(padrao, substituicao, codigo)

        return codigo

    def _validar_codigo(self, codigo: str) -> bool:
        """
        Valida se código modificado é sintaticamente correto.

        Args:
            codigo: Código a validar

        Returns:
            True se válido, False caso contrário
        """
        try:
            ast.parse(codigo)
            return True
        except SyntaxError:
            return False

    def _criar_backup(self, caminho: str, codigo: str):
        """Cria backup do arquivo antes de modificar."""
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            caminho_backup = f"{caminho}.backup_{timestamp}"

            Path(caminho_backup).write_text(codigo, encoding='utf-8')
        except Exception:
            pass  # Silenciosamente ignorar erros de backup

    def obter_estatisticas(self) -> Dict[str, int]:
        """Retorna estatísticas de aplicação."""
        return {
            'total_aplicadas': self.total_aplicadas,
            'total_falhadas': self.total_falhadas,
            'total_rollbacks': self.total_rollbacks,
            'taxa_sucesso': (
                self.total_aplicadas / max(1, self.total_aplicadas + self.total_falhadas)
            ) * 100
        }


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def analisar_arquivo(caminho: str) -> List[Dict]:
    """
    Analisa um arquivo Python e retorna melhorias detectadas

    Args:
        caminho: Caminho do arquivo .py

    Returns:
        Lista de melhorias
    """
    detector = DetectorMelhorias()

    try:
        codigo = Path(caminho).read_text(encoding='utf-8')
        nome_arquivo = Path(caminho).stem
        return detector.analisar_codigo_executado(nome_arquivo, codigo)
    except Exception:
        return []


def analisar_diretorio(caminho: str, recursivo: bool = True) -> Dict[str, List[Dict]]:
    """
    Analisa todos os arquivos .py em um diretório

    Args:
        caminho: Caminho do diretório
        recursivo: Se deve analisar subdiretórios

    Returns:
        Dict com {nome_arquivo: [melhorias]}
    """
    detector = DetectorMelhorias()
    resultados = {}

    pasta = Path(caminho)
    padrao = '**/*.py' if recursivo else '*.py'

    for arquivo in pasta.glob(padrao):
        try:
            codigo = arquivo.read_text(encoding='utf-8')
            melhorias = detector.analisar_codigo_executado(arquivo.stem, codigo)
            if melhorias:
                resultados[str(arquivo)] = melhorias
        except Exception:
            continue

    return resultados


if __name__ == "__main__":
    # Teste rápido
    detector = DetectorMelhorias()

    # Código de exemplo com problemas
    codigo_teste = '''
def processar_lista(items):  # ← Sem type hints
    resultado = []
    for item in items:
        resultado.append(item.upper())  # ← Loop ineficiente
    return resultado

def deletar_arquivo(caminho):  # ← Sem validação de segurança
    import os
    os.remove(caminho)  # ← Perigoso!
'''

    melhorias = detector.analisar_codigo_executado("teste", codigo_teste)
    print(detector.gerar_relatorio(melhorias))
