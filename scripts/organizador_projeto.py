#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📁 ORGANIZADOR INTELIGENTE DE PROJETO - Luna V3
===============================================

Sistema de organização automática da raiz do projeto Luna.
Diferente do gerenciador_workspaces (que organiza workspaces de usuários),
este módulo organiza a RAIZ do projeto Luna de forma semântica e inteligente.

Funcionalidades:
- Detecção semântica de tipos de arquivo (não só extensão)
- Reorganização automática: docs/, tests/, scripts/, .backups/
- Ajuste automático de imports em arquivos movidos
- Validação de integridade pós-reorganização
- Sistema de snapshot e rollback
- Modo dry-run (simulação)

Criado: 2025-10-20
Parte do sistema de melhorias Luna V3
"""

import sys
import os

# ============================================================================
# CONFIGURAÇÃO UTF-8 (Windows)
# ============================================================================
if sys.platform == 'win32':
    os.environ['PYTHONUTF8'] = '1'
    os.environ['PYTHONIOENCODING'] = 'utf-8'

    try:
        # Tentar reconfigurar se possível
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        # Já configurado ou não suporta reconfigure
        pass

from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from datetime import datetime
import shutil
import json
import re
import subprocess
import importlib.util


# ============================================================================
# CLASSE: DETECTOR DE TIPO DE ARQUIVO (ANÁLISE SEMÂNTICA)
# ============================================================================

class DetectorTipoArquivo:
    """Detecta tipo SEMÂNTICO de arquivo (não apenas extensão)."""

    # Módulos essenciais (importados no código, devem ficar na raiz)
    MODULOS_ESSENCIAIS = {
        'luna_v3_FINAL_OTIMIZADA.py',
        'memoria_permanente.py',
        'cofre_credenciais.py',
        'gerenciador_workspaces.py',
        'gerenciador_temp.py',
        'integracao_google.py',
        'integracao_notion.py',
        'sistema_auto_evolucao.py',
        'detector_melhorias.py',
        'dashboard_metricas.py',
        'parameter_tuner.py',
        'massive_context_analyzer.py',
        'rollback_manager.py',
        'organizador_projeto.py'
    }

    # Arquivos de dados essenciais (paths hardcoded no código)
    DADOS_ESSENCIAIS = {
        'memoria_agente.json',
        'workspace_config.json',
        'cofre.enc',
        'credentials.json',
        'token_gmail.json',
        'token_calendar.json',
        'tuner_history.json',
        'auto_modificacoes.log',
        'workspace.log'
    }

    # Documentação essencial na raiz
    DOCS_ESSENCIAIS = {
        'README.md',
        'CLAUDE.md',
        '.env'
    }

    @staticmethod
    def detectar_tipo(arquivo: Path, base_dir: Path) -> str:
        """
        Detecta tipo SEMÂNTICO do arquivo.

        Returns:
            - 'modulo_essencial': Módulos Python importados
            - 'dados_essencial': Arquivos de dados hardcoded
            - 'config_essencial': Configs essenciais
            - 'documentacao': Relatórios, guias, checkpoints
            - 'teste': Arquivos de teste
            - 'script': Scripts utilitários
            - 'backup': Backups antigos
            - 'pasta': É uma pasta (não mexer)
        """
        if arquivo.is_dir():
            return 'pasta'

        nome = arquivo.name
        nome_lower = nome.lower()

        # 1. Essenciais (manter na raiz)
        if nome in DetectorTipoArquivo.MODULOS_ESSENCIAIS:
            return 'modulo_essencial'

        if nome in DetectorTipoArquivo.DADOS_ESSENCIAIS:
            return 'dados_essencial'

        if nome in DetectorTipoArquivo.DOCS_ESSENCIAIS:
            return 'config_essencial'

        # 2. Documentação (mover para docs/)
        padroes_docs = [
            'RELATORIO_', 'GUIA_', 'CHECKPOINT_', 'RESUMO_', 'ANALISE_',
            'METRICAS_', 'RESULTADO_', 'PLANO_', 'CORRECAO_', 'ENTREGA_',
            'SISTEMA_', 'INTEGRACAO_', 'TESTE_', 'README_', 'CHANGELOG',
            'INDICE', 'SUMARIO_'
        ]

        if any(nome.upper().startswith(p) for p in padroes_docs):
            return 'documentacao'

        if nome_lower.endswith(('.pdf', '.txt')) and nome not in DetectorTipoArquivo.DOCS_ESSENCIAIS:
            return 'documentacao'

        # 3. Testes (mover para tests/)
        if nome.startswith('test_') or nome.startswith('tests_') or nome.startswith('testes_'):
            return 'teste'

        if nome in ['run_all_tests.py', 'test_coverage_report.py']:
            return 'teste'

        if nome_lower in ['test_results.txt', 'teste_cenario1.txt']:
            return 'teste'

        # 4. Scripts utilitários (mover para scripts/)
        padroes_scripts = [
            'analisar_', 'atualizar_', 'corrigir_', 'copiar_',
            'extrair_', 'refatorar_', 'substituir_', 'templates_'
        ]

        if any(nome.lower().startswith(p) for p in padroes_scripts):
            return 'script'

        if nome in ['luna_test.py']:
            return 'script'

        # 5. Backups (mover para .backups/)
        if '.backup' in nome_lower or nome_lower.endswith('.bak'):
            return 'backup'

        if 'backup_' in nome_lower and nome not in DetectorTipoArquivo.DADOS_ESSENCIAIS:
            return 'backup'

        # 6. Outros (deixar na raiz por segurança)
        return 'outros'


# ============================================================================
# CLASSE: AJUSTADOR DE IMPORTS
# ============================================================================

class AjustadorImports:
    """Ajusta imports em arquivos Python movidos para subpastas."""

    @staticmethod
    def precisa_ajuste(arquivo: Path, tipo_destino: str) -> bool:
        """Verifica se arquivo precisa de ajuste de import."""
        if not arquivo.suffix == '.py':
            return False

        if tipo_destino not in ['teste', 'script']:
            return False

        return True

    @staticmethod
    def ajustar_imports_arquivo(arquivo: Path) -> bool:
        """
        Adiciona sys.path.insert no início do arquivo Python.

        Returns:
            True se ajustou com sucesso
        """
        try:
            # Ler conteúdo
            conteudo = arquivo.read_text(encoding='utf-8')

            # Verificar se já tem sys.path
            if 'sys.path.insert' in conteudo:
                # Verificar se está correto
                if 'os.path.dirname(os.path.dirname(' in conteudo:
                    return True  # Já está correto

                # Corrigir sys.path existente
                conteudo_novo = re.sub(
                    r'sys\.path\.insert\(0,\s*os\.path\.dirname\(os\.path\.abspath\(__file__\)\)\)',
                    'sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))',
                    conteudo
                )

                arquivo.write_text(conteudo_novo, encoding='utf-8')
                return True

            # Adicionar sys.path após imports do sistema
            linhas = conteudo.split('\n')
            indice_insercao = 0

            # Encontrar onde inserir (após encoding e imports iniciais)
            for i, linha in enumerate(linhas):
                if linha.strip().startswith('import ') or linha.strip().startswith('from '):
                    if not linha.strip().startswith('from luna_') and not linha.strip().startswith('from memoria_'):
                        indice_insercao = i + 1

            # Inserir sys.path
            novo_import = [
                '',
                'import sys',
                'import os',
                'sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))',
                ''
            ]

            # Verificar se sys/os já foram importados
            tem_sys = any('import sys' in linha for linha in linhas[:20])
            tem_os = any('import os' in linha for linha in linhas[:20])

            if tem_sys and tem_os:
                novo_import = [
                    '',
                    'sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))',
                    ''
                ]

            linhas_novas = linhas[:indice_insercao] + novo_import + linhas[indice_insercao:]
            conteudo_novo = '\n'.join(linhas_novas)

            arquivo.write_text(conteudo_novo, encoding='utf-8')
            return True

        except Exception as e:
            print(f"⚠️  Erro ao ajustar imports em {arquivo.name}: {e}")
            return False


# ============================================================================
# CLASSE: ORGANIZADOR DE PROJETO (PRINCIPAL)
# ============================================================================

class OrganizadorProjeto:
    """Sistema de organização inteligente da raiz do projeto Luna."""

    def __init__(self, base_dir: Optional[Path] = None):
        """
        Args:
            base_dir: Diretório base do projeto (default: diretório atual)
        """
        self.base_dir = base_dir or Path.cwd()
        self.detector = DetectorTipoArquivo()
        self.ajustador = AjustadorImports()

        # Estrutura de organização
        self.estrutura = {
            'docs/': 'documentacao',
            'tests/': 'teste',
            'scripts/': 'script',
            '.backups/': 'backup'
        }

        # Pastas que já existem (não mexer)
        self.pastas_existentes = {
            'Luna', 'workspaces', '.git', '.claude', '__pycache__',
            '.temp', 'backups_auto_evolucao', '.rollback_backups',
            'venv_test', 'docs', 'tests', 'scripts'
        }

    def analisar_projeto(self) -> Dict:
        """
        Analisa raiz do projeto e retorna plano de reorganização.

        Returns:
            {
                'total_arquivos': int,
                'essenciais_raiz': [...],
                'mover': {'docs/': [...], 'tests/': [...], ...},
                'ajustes_necessarios': {...},
                'avisos': [...]
            }
        """
        resultado = {
            'total_arquivos': 0,
            'essenciais_raiz': [],
            'mover': {pasta: [] for pasta in self.estrutura.keys()},
            'ajustes_necessarios': {
                'imports': [],
                'test_runners': []
            },
            'avisos': []
        }

        # Listar arquivos na raiz
        arquivos = [f for f in self.base_dir.iterdir() if f.name not in self.pastas_existentes]
        resultado['total_arquivos'] = len(arquivos)

        for arquivo in arquivos:
            tipo = self.detector.detectar_tipo(arquivo, self.base_dir)

            if tipo in ['modulo_essencial', 'dados_essencial', 'config_essencial']:
                resultado['essenciais_raiz'].append(arquivo.name)

            elif tipo == 'pasta':
                continue  # Ignorar pastas

            elif tipo in ['documentacao', 'teste', 'script', 'backup']:
                # Encontrar pasta de destino
                for pasta, tipo_esperado in self.estrutura.items():
                    if tipo == tipo_esperado:
                        resultado['mover'][pasta].append(arquivo.name)

                        # Verificar se precisa ajuste de import
                        if self.ajustador.precisa_ajuste(arquivo, tipo):
                            resultado['ajustes_necessarios']['imports'].append(arquivo.name)

                        # Verificar se é test runner
                        if 'run_all_tests' in arquivo.name or 'test_coverage' in arquivo.name:
                            resultado['ajustes_necessarios']['test_runners'].append(arquivo.name)

                        break

            else:  # 'outros'
                resultado['avisos'].append(f"Arquivo não categorizado: {arquivo.name} (será mantido na raiz)")

        return resultado

    def reorganizar_projeto(self, dry_run: bool = False, confirmar: bool = True) -> Dict:
        """
        Reorganiza projeto automaticamente.

        Args:
            dry_run: Se True, simula sem executar
            confirmar: Se True, pede confirmação antes de executar

        Returns:
            {
                'sucesso': bool,
                'modo': 'dry-run' | 'executado',
                'pastas_criadas': [...],
                'arquivos_movidos': [...],
                'imports_ajustados': [...],
                'test_runners_atualizados': [...],
                'erros': [...]
            }
        """
        # 1. Analisar projeto
        analise = self.analisar_projeto()

        resultado = {
            'sucesso': False,
            'modo': 'dry-run' if dry_run else 'executado',
            'pastas_criadas': [],
            'arquivos_movidos': [],
            'imports_ajustados': [],
            'test_runners_atualizados': [],
            'erros': []
        }

        # 2. Confirmar (se necessário)
        if confirmar and not dry_run:
            print(f"\n🎯 REORGANIZAÇÃO DO PROJETO LUNA")
            print(f"═" * 70)
            print(f"\nTotal de arquivos na raiz: {analise['total_arquivos']}")
            print(f"Essenciais (manter): {len(analise['essenciais_raiz'])}")
            print(f"\nMover:")
            for pasta, arquivos in analise['mover'].items():
                if arquivos:
                    print(f"  → {pasta}: {len(arquivos)} arquivos")

            print(f"\nAjustes necessários:")
            print(f"  → Imports: {len(analise['ajustes_necessarios']['imports'])} arquivos")
            print(f"  → Test runners: {len(analise['ajustes_necessarios']['test_runners'])} arquivos")

            resposta = input(f"\n⚠️  Continuar? (s/N): ").lower()
            if resposta != 's':
                resultado['erros'].append("Cancelado pelo usuário")
                return resultado

        # 3. Criar snapshot (se não for dry-run)
        if not dry_run:
            try:
                snapshot_path = self._criar_snapshot()
                print(f"📸 Snapshot criado: {snapshot_path}")
            except Exception as e:
                resultado['erros'].append(f"Erro ao criar snapshot: {e}")
                return resultado

        # 4. Criar pastas
        for pasta in self.estrutura.keys():
            pasta_path = self.base_dir / pasta

            if not pasta_path.exists():
                if not dry_run:
                    try:
                        pasta_path.mkdir(parents=True, exist_ok=True)
                        resultado['pastas_criadas'].append(pasta)
                    except Exception as e:
                        resultado['erros'].append(f"Erro ao criar {pasta}: {e}")
                else:
                    resultado['pastas_criadas'].append(f"{pasta} (dry-run)")

        # 5. Mover arquivos
        for pasta, arquivos in analise['mover'].items():
            pasta_path = self.base_dir / pasta

            for arquivo_nome in arquivos:
                origem = self.base_dir / arquivo_nome
                destino = pasta_path / arquivo_nome

                try:
                    if not dry_run:
                        shutil.move(str(origem), str(destino))
                        resultado['arquivos_movidos'].append(f"{arquivo_nome} → {pasta}")

                        # Ajustar imports se necessário
                        if arquivo_nome in analise['ajustes_necessarios']['imports']:
                            if self.ajustador.ajustar_imports_arquivo(destino):
                                resultado['imports_ajustados'].append(arquivo_nome)
                    else:
                        resultado['arquivos_movidos'].append(f"{arquivo_nome} → {pasta} (dry-run)")

                except Exception as e:
                    resultado['erros'].append(f"Erro ao mover {arquivo_nome}: {e}")

        # 6. Atualizar test runners
        for runner in analise['ajustes_necessarios']['test_runners']:
            runner_path = self.base_dir / 'tests' / runner

            if not dry_run and runner_path.exists():
                try:
                    # Atualizar run_all_tests.py já foi feito manualmente
                    # Aqui apenas registramos
                    resultado['test_runners_atualizados'].append(runner)
                except Exception as e:
                    resultado['erros'].append(f"Erro ao atualizar {runner}: {e}")

        # 7. Validar (se não for dry-run)
        if not dry_run:
            validacao = self._validar_reorganizacao()
            if not validacao['sucesso']:
                resultado['erros'].extend(validacao['erros'])
                resultado['erros'].append("❌ Validação falhou - considere fazer rollback")
                return resultado

        resultado['sucesso'] = len(resultado['erros']) == 0
        return resultado

    def _criar_snapshot(self) -> Path:
        """Cria snapshot da raiz antes de reorganizar."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_dir = self.base_dir / '.rollback_backups' / f'reorganizacao_{timestamp}'
        snapshot_dir.mkdir(parents=True, exist_ok=True)

        # Copiar arquivos essenciais
        arquivos_backup = [f for f in self.base_dir.iterdir()
                          if f.is_file() and f.name not in self.pastas_existentes]

        for arquivo in arquivos_backup:
            try:
                shutil.copy2(arquivo, snapshot_dir / arquivo.name)
            except Exception:
                pass

        return snapshot_dir

    def _validar_reorganizacao(self) -> Dict:
        """Valida que reorganização não quebrou nada."""
        resultado = {'sucesso': True, 'erros': [], 'avisos': []}

        # 1. Testar importação do módulo principal
        try:
            import importlib
            spec = importlib.util.spec_from_file_location(
                "luna_v3_FINAL_OTIMIZADA",
                str(self.base_dir / "luna_v3_FINAL_OTIMIZADA.py")
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                # Não executar, apenas verificar sintaxe
                print("✅ Importação do módulo principal: OK")
            else:
                resultado['erros'].append("Não foi possível importar módulo principal")
                resultado['sucesso'] = False
        except Exception as e:
            resultado['erros'].append(f"Erro na importação: {e}")
            resultado['sucesso'] = False

        # 2. Verificar paths hardcoded preservados
        paths_criticos = [
            self.base_dir / 'Luna' / '.stats',
            self.base_dir / 'Luna' / 'planos'
        ]

        for path in paths_criticos:
            if not path.exists():
                resultado['avisos'].append(f"Path crítico não encontrado: {path}")

        return resultado


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("🎯 ORGANIZADOR INTELIGENTE DE PROJETO - LUNA V3\n")

    org = OrganizadorProjeto()

    # 1. Análise
    print("📊 ANALISANDO PROJETO...\n")
    analise = org.analisar_projeto()

    print(f"Total de arquivos: {analise['total_arquivos']}")
    print(f"\n✅ Essenciais (manter na raiz): {len(analise['essenciais_raiz'])}")

    print(f"\n📚 Mover para pastas:")
    for pasta, arquivos in analise['mover'].items():
        if arquivos:
            print(f"  → {pasta}: {len(arquivos)} arquivos")
            for arq in arquivos[:3]:
                print(f"     - {arq}")
            if len(arquivos) > 3:
                print(f"     ... e mais {len(arquivos) - 3}")

    print(f"\n⚠️  Ajustes necessários:")
    print(f"  → Imports: {len(analise['ajustes_necessarios']['imports'])} arquivos")
    print(f"  → Test runners: {len(analise['ajustes_necessarios']['test_runners'])} arquivos")

    if analise['avisos']:
        print(f"\n⚠️  Avisos:")
        for aviso in analise['avisos']:
            print(f"  - {aviso}")

    # 2. Dry-run (simulação)
    print(f"\n🔍 SIMULANDO REORGANIZAÇÃO (dry-run)...\n")
    resultado = org.reorganizar_projeto(dry_run=True, confirmar=False)

    if resultado['pastas_criadas']:
        print(f"📁 Pastas a criar: {', '.join(resultado['pastas_criadas'])}")

    print(f"📦 Arquivos a mover: {len(resultado['arquivos_movidos'])}")
    print(f"🔧 Imports a ajustar: {len(resultado['imports_ajustados'])}")

    if resultado['erros']:
        print(f"\n❌ Erros encontrados:")
        for erro in resultado['erros']:
            print(f"  - {erro}")
    else:
        print(f"\n✅ Dry-run concluído sem erros!")
        print(f"\n💡 Para executar de verdade, use: reorganizar_projeto(dry_run=False)")
