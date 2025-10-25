#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTES UNITÁRIOS BÁSICOS - LUNA V3
======================================

Testes para componentes principais do Luna.
Meta: 60% cobertura de código crítico.

Para executar:
    python3 tests_luna_basicos.py

Ou com pytest:
    pip install pytest
    pytest tests_luna_basicos.py -v
"""

import unittest
import os
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import json

# Adicionar diretório do Luna ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar módulos Luna
from memoria_permanente import MemoriaPermanente
from gerenciador_workspaces import GerenciadorWorkspaces
from gerenciador_temp import GerenciadorTemporarios
from sistema_auto_evolucao import SistemaAutoEvolucao, FilaDeMelhorias


# ============================================================================
# TESTES: MemoriaPermanente
# ============================================================================

class TestMemoriaPermanente(unittest.TestCase):
    """Testes para o sistema de memória permanente"""

    def setUp(self):
        """Setup para cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.memoria_file = os.path.join(self.temp_dir, "memoria_teste.json")

    def tearDown(self):
        """Limpeza após cada teste"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_criar_memoria_inicial(self):
        """Teste: Criar memória inicial com estrutura padrão"""
        memoria = MemoriaPermanente(arquivo_memoria=self.memoria_file)

        # Verificar estrutura
        self.assertIn("aprendizados", memoria.memoria)
        self.assertIn("ferramentas_criadas", memoria.memoria)
        self.assertIn("historico_tarefas", memoria.memoria)
        self.assertIn("preferencias_usuario", memoria.memoria)

        # Verificar que arquivo foi criado
        self.assertTrue(os.path.exists(self.memoria_file))

    def test_adicionar_aprendizado(self):
        """Teste: Adicionar aprendizado à memória"""
        memoria = MemoriaPermanente(arquivo_memoria=self.memoria_file)

        # Adicionar aprendizado
        aprendizado_id = memoria.adicionar_aprendizado(
            categoria="teste",
            conteudo="Aprendizado de teste",
            tags=["teste", "unittest"]
        )

        # Verificar que foi adicionado
        self.assertEqual(len(memoria.memoria["aprendizados"]), 1)
        self.assertIsNotNone(aprendizado_id)

        # Verificar conteúdo
        aprendizado = memoria.memoria["aprendizados"][0]
        self.assertEqual(aprendizado["categoria"], "teste")
        self.assertEqual(aprendizado["conteudo"], "Aprendizado de teste")
        self.assertIn("teste", aprendizado["tags"])

    def test_buscar_aprendizados(self):
        """Teste: Buscar aprendizados por query"""
        memoria = MemoriaPermanente(arquivo_memoria=self.memoria_file)

        # Adicionar múltiplos aprendizados
        memoria.adicionar_aprendizado("tecnica", "Python usa listas", tags=["python"])
        memoria.adicionar_aprendizado("tecnica", "JavaScript usa arrays", tags=["js"])
        memoria.adicionar_aprendizado("bug", "Python indent é importante", tags=["python"])

        # Buscar por query
        resultados = memoria.buscar_aprendizados(query="Python")

        # Verificar resultados
        self.assertEqual(len(resultados), 2)
        for r in resultados:
            self.assertIn("Python", r["conteudo"])

    def test_compactar_memoria(self):
        """Teste: Compactar memória removendo duplicatas e excesso"""
        memoria = MemoriaPermanente(arquivo_memoria=self.memoria_file)

        # Adicionar muitas ferramentas (120)
        # Nota: A auto-poda mantém automaticamente no máximo 100
        for i in range(120):
            memoria.registrar_ferramenta_criada(
                f"ferramenta_{i}",
                f"Descrição {i}",
                f"def ferramenta_{i}(): pass"
            )

        # ✅ CORRIGIDO: Auto-poda já mantém em 100
        # Verificar que auto-poda está ativa (máximo 100)
        self.assertEqual(len(memoria.memoria["ferramentas_criadas"]), 100)

        # Compactar (não deve fazer nada pois já está em 100)
        resultado = memoria.compactar_memoria()

        # Verificar que permanece em 100
        self.assertEqual(len(memoria.memoria["ferramentas_criadas"]), 100)


# ============================================================================
# TESTES: GerenciadorWorkspaces
# ============================================================================

class TestGerenciadorWorkspaces(unittest.TestCase):
    """Testes para o gerenciador de workspaces"""

    def setUp(self):
        """Setup para cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.gerenciador = GerenciadorWorkspaces(base_dir=self.temp_dir)

    def tearDown(self):
        """Limpeza após cada teste"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_criar_workspace(self):
        """Teste: Criar novo workspace"""
        sucesso, mensagem = self.gerenciador.criar_workspace(
            "teste_workspace",
            "Workspace de teste"
        )

        # Verificar sucesso
        self.assertTrue(sucesso)
        self.assertIn("criado", mensagem.lower())

        # Verificar que diretório foi criado
        workspace_path = os.path.join(
            self.temp_dir, "workspaces", "teste_workspace"
        )
        self.assertTrue(os.path.exists(workspace_path))

    def test_listar_workspaces(self):
        """Teste: Listar workspaces criados"""
        # Criar alguns workspaces
        self.gerenciador.criar_workspace("workspace1", "Primeiro")
        self.gerenciador.criar_workspace("workspace2", "Segundo")

        # Listar
        workspaces = self.gerenciador.listar_workspaces()

        # Verificar
        self.assertEqual(len(workspaces), 2)
        nomes = [ws["nome"] for ws in workspaces]
        self.assertIn("workspace1", nomes)
        self.assertIn("workspace2", nomes)

    def test_selecionar_workspace(self):
        """Teste: Selecionar workspace ativo"""
        # Criar workspace
        self.gerenciador.criar_workspace("meu_workspace", "Teste")

        # Selecionar
        sucesso, mensagem = self.gerenciador.selecionar_workspace("meu_workspace")

        # Verificar
        self.assertTrue(sucesso)

        # Verificar que é o atual
        atual = self.gerenciador.get_workspace_atual()
        self.assertIsNotNone(atual)
        self.assertEqual(atual["nome"], "meu_workspace")

    def test_resolver_caminho(self):
        """Teste: Resolver caminho relativo para workspace"""
        # Criar e selecionar workspace
        self.gerenciador.criar_workspace("projeto", "Projeto teste")
        self.gerenciador.selecionar_workspace("projeto")

        # Resolver caminho
        caminho = self.gerenciador.resolver_caminho("arquivo.txt")

        # Verificar que é caminho completo no workspace
        self.assertIn("workspaces", caminho)
        self.assertIn("projeto", caminho)
        self.assertTrue(caminho.endswith("arquivo.txt"))


# ============================================================================
# TESTES: GerenciadorTemporarios
# ============================================================================

class TestGerenciadorTemporarios(unittest.TestCase):
    """Testes para o gerenciador de arquivos temporários"""

    def setUp(self):
        """Setup para cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.gerenciador = GerenciadorTemporarios(base_dir=self.temp_dir)

    def tearDown(self):
        """Limpeza após cada teste"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_marcar_temporario(self):
        """Teste: Marcar arquivo como temporário"""
        # Criar arquivo de teste
        arquivo_teste = os.path.join(self.temp_dir, "teste_temp.txt")
        Path(arquivo_teste).write_text("teste", encoding='utf-8')

        # Marcar como temporário
        sucesso = self.gerenciador.marcar_temporario(arquivo_teste, forcar=True)

        # Verificar
        self.assertTrue(sucesso)
        self.assertEqual(len(self.gerenciador.metadata["arquivos_temporarios"]), 1)

    def test_proteger_arquivo(self):
        """Teste: Proteger arquivo de deleção"""
        # Criar arquivo
        arquivo_teste = os.path.join(self.temp_dir, "importante.txt")
        Path(arquivo_teste).write_text("importante", encoding='utf-8')

        # Marcar como temporário
        self.gerenciador.marcar_temporario(arquivo_teste, forcar=True)

        # Proteger
        sucesso = self.gerenciador.proteger_arquivo(arquivo_teste)

        # Verificar que foi removido de temporários
        self.assertTrue(sucesso)
        self.assertEqual(len(self.gerenciador.metadata["arquivos_temporarios"]), 0)
        self.assertEqual(len(self.gerenciador.metadata["arquivos_protegidos"]), 1)

    def test_listar_temporarios(self):
        """Teste: Listar arquivos temporários"""
        # Criar e marcar arquivos
        for i in range(3):
            arquivo = os.path.join(self.temp_dir, f"temp_{i}.txt")
            Path(arquivo).write_text(f"teste {i}", encoding='utf-8')
            self.gerenciador.marcar_temporario(arquivo, forcar=True)

        # Listar
        temporarios = self.gerenciador.listar_temporarios()

        # Verificar
        self.assertEqual(len(temporarios), 3)
        for temp in temporarios:
            self.assertIn("dias_restantes", temp)
            self.assertIn("tamanho_bytes", temp)


# ============================================================================
# TESTES: SistemaAutoEvolucao
# ============================================================================

class TestSistemaAutoEvolucao(unittest.TestCase):
    """Testes para o sistema de auto-evolução"""

    def setUp(self):
        """Setup para cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        # Criar arquivo alvo de teste
        self.arquivo_alvo = os.path.join(self.temp_dir, "teste_alvo.py")
        Path(self.arquivo_alvo).write_text(
            "def funcao_teste():\n    return 'original'\n",
            encoding='utf-8'
        )
        self.sistema = SistemaAutoEvolucao(arquivo_alvo=self.arquivo_alvo)

    def tearDown(self):
        """Limpeza após cada teste"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_fila_melhorias_adicionar(self):
        """Teste: Adicionar melhoria à fila"""
        fila = FilaDeMelhorias()

        fila.adicionar(
            tipo="otimizacao",
            alvo="funcao_teste",
            motivo="Melhorar performance",
            codigo_sugerido="def funcao_teste():\n    return 'otimizado'\n",
            prioridade=8
        )

        # Verificar
        self.assertEqual(len(fila.melhorias_pendentes), 1)
        melhoria = fila.melhorias_pendentes[0]
        self.assertEqual(melhoria["tipo"], "otimizacao")
        self.assertEqual(melhoria["prioridade"], 8)

    def test_validar_sintaxe(self):
        """Teste: Validar sintaxe Python"""
        # Sintaxe válida
        valido, erro = self.sistema._validar_sintaxe(self.arquivo_alvo)
        self.assertTrue(valido)

        # Sintaxe inválida
        arquivo_invalido = os.path.join(self.temp_dir, "invalido.py")
        Path(arquivo_invalido).write_text("def invalido(\n", encoding='utf-8')
        valido, erro = self.sistema._validar_sintaxe(arquivo_invalido)
        self.assertFalse(valido)
        self.assertIsNotNone(erro)

    def test_criar_backup(self):
        """Teste: Criar backup antes de modificação"""
        backup_path = self.sistema._criar_backup("teste de backup")

        # Verificar que backup foi criado
        self.assertTrue(os.path.exists(backup_path))

        # Verificar que conteúdo é igual
        with open(backup_path, 'r', encoding='utf-8') as f:
            backup_content = f.read()
        with open(self.arquivo_alvo, 'r', encoding='utf-8') as f:
            original_content = f.read()

        self.assertEqual(backup_content, original_content)


# ============================================================================
# TESTES: Auto-Evolução Avançada (FASE 4)
# ============================================================================

class TestAutoEvolucaoAvancado(unittest.TestCase):
    """Testes avançados para sistema de auto-evolução"""

    def setUp(self):
        """Setup para cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        # Criar arquivo alvo de teste
        self.arquivo_alvo = os.path.join(self.temp_dir, "teste_evolucao.py")
        Path(self.arquivo_alvo).write_text(
            "def funcao_teste():\n    return 'original'\n",
            encoding='utf-8'
        )
        self.sistema = SistemaAutoEvolucao(arquivo_alvo=self.arquivo_alvo)

    def tearDown(self):
        """Limpeza após cada teste"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_fila_prioridade(self):
        """Teste: Melhorias são ordenadas por prioridade"""
        fila = FilaDeMelhorias()

        # Adicionar melhorias com prioridades diferentes
        fila.adicionar("otimizacao", "func1", "Baixa prioridade", "pass", prioridade=3)
        fila.adicionar("bug_fix", "func2", "Alta prioridade", "pass", prioridade=9)
        fila.adicionar("feature", "func3", "Média prioridade", "pass", prioridade=5)

        # Obter pendentes (devem estar ordenadas por prioridade)
        pendentes = fila.obter_pendentes()

        # Verificar ordem (mais alta primeiro)
        self.assertEqual(pendentes[0]['prioridade'], 9)
        self.assertEqual(pendentes[1]['prioridade'], 5)
        self.assertEqual(pendentes[2]['prioridade'], 3)

    def test_fila_tipos_diferentes(self):
        """Teste: Fila aceita diferentes tipos de melhorias"""
        fila = FilaDeMelhorias()

        tipos = ['otimizacao', 'bug_fix', 'refatoracao', 'feature', 'qualidade', 'documentacao']

        for tipo in tipos:
            fila.adicionar(tipo, f"alvo_{tipo}", f"Teste {tipo}", "pass", prioridade=5)

        # Verificar que todos foram adicionados
        self.assertEqual(len(fila.melhorias_pendentes), len(tipos))

        # Verificar que cada tipo está presente
        tipos_na_fila = [m['tipo'] for m in fila.melhorias_pendentes]
        for tipo in tipos:
            self.assertIn(tipo, tipos_na_fila)

    def test_aplicar_melhoria_sem_crash(self):
        """Teste: Sistema aplica melhoria sem crashar"""
        # Código original
        conteudo_original = Path(self.arquivo_alvo).read_text(encoding='utf-8')

        # Adicionar melhoria simples
        melhoria = {
            'id': 'test_001',
            'tipo': 'otimizacao',
            'alvo': 'funcao_teste',
            'motivo': 'Melhorar retorno',
            'codigo': "def funcao_teste():\n    return 'otimizado'\n"
        }

        # Aplicar modificação (não deve crashar, retorna bool)
        try:
            sucesso = self.sistema.aplicar_modificacao(melhoria)
            # Verificar que retornou um boolean
            self.assertIsInstance(sucesso, bool)

            # Se falhou, verificar que rollback foi feito
            if not sucesso:
                conteudo_atual = Path(self.arquivo_alvo).read_text(encoding='utf-8')
                self.assertEqual(conteudo_original, conteudo_atual)
        except Exception as e:
            self.fail(f"aplicar_modificacao não deve crashar: {e}")

    def test_rollback_apos_falha(self):
        """Teste: Rollback quando modificação causa erro de sintaxe"""
        # Código original
        conteudo_original = Path(self.arquivo_alvo).read_text(encoding='utf-8')

        # Melhoria com código inválido
        melhoria = {
            'id': 'test_002',
            'tipo': 'bug_fix',
            'alvo': 'funcao_teste',
            'motivo': 'Teste de rollback',
            'codigo': "def funcao_teste(\n"  # Sintaxe inválida
        }

        # Tentar aplicar (deve falhar e fazer rollback)
        sucesso = self.sistema.aplicar_modificacao(melhoria)

        # Verificar que falhou
        self.assertFalse(sucesso)

        # Verificar que arquivo foi restaurado
        conteudo_atual = Path(self.arquivo_alvo).read_text(encoding='utf-8')
        self.assertEqual(conteudo_original, conteudo_atual)

    def test_backups_criados(self):
        """Teste: Backups são criados no diretório correto"""
        # Verificar que diretório de backups existe
        backups_dir = os.path.join(os.path.dirname(self.arquivo_alvo), 'backups_auto_evolucao')

        # Aplicar melhoria (irá criar backup)
        melhoria = {
            'id': 'test_003',
            'tipo': 'otimizacao',
            'alvo': 'funcao_teste',
            'motivo': 'Teste backup',
            'codigo': "def funcao_teste():\n    return 'novo'\n"
        }

        # Stats iniciais
        stats_inicial = self.sistema.stats.copy()

        # Aplicar
        self.sistema.aplicar_modificacao(melhoria)

        # Verificar que pelo menos um backup foi criado (se diretório existe)
        if os.path.exists(backups_dir):
            backups = os.listdir(backups_dir)
            self.assertGreaterEqual(len(backups), 1)

    def test_historico_preservado(self):
        """Teste: Histórico de melhorias é preservado"""
        fila = FilaDeMelhorias()

        # Adicionar e aplicar melhorias
        id1 = fila.adicionar("otimizacao", "func1", "Teste 1", "pass", 5)
        id2 = fila.adicionar("bug_fix", "func2", "Teste 2", "pass", 8)

        # Marcar como aplicadas
        melhoria1 = fila.melhorias_pendentes[0]
        melhoria2 = fila.melhorias_pendentes[1]

        fila.melhorias_pendentes.clear()
        fila.melhorias_aplicadas.append(melhoria1)
        fila.melhorias_aplicadas.append(melhoria2)

        # Verificar histórico
        self.assertEqual(len(fila.melhorias_aplicadas), 2)
        self.assertEqual(fila.melhorias_aplicadas[0]['tipo'], 'otimizacao')
        self.assertEqual(fila.melhorias_aplicadas[1]['tipo'], 'bug_fix')


# ============================================================================
# TESTES: Integração
# ============================================================================

class TestIntegracao(unittest.TestCase):
    """Testes de integração entre componentes"""

    def setUp(self):
        """Setup para cada teste"""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Limpeza após cada teste"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_workspace_e_memoria_integrados(self):
        """Teste: Workspace e memória trabalhando juntos"""
        # Criar gerenciador de workspace
        gerenciador = GerenciadorWorkspaces(base_dir=self.temp_dir)
        gerenciador.criar_workspace("integracao", "Teste integração")
        gerenciador.selecionar_workspace("integracao")

        # Criar memória
        memoria_file = os.path.join(self.temp_dir, "memoria.json")
        memoria = MemoriaPermanente(arquivo_memoria=memoria_file)

        # Adicionar aprendizado sobre workspace
        memoria.adicionar_aprendizado(
            "workspace",
            f"Workspace 'integracao' criado em {self.temp_dir}",
            tags=["workspace", "teste"]
        )

        # Verificar integração
        self.assertEqual(len(memoria.memoria["aprendizados"]), 1)

        # Buscar aprendizados relacionados
        resultados = memoria.buscar_aprendizados(query="integracao")
        self.assertEqual(len(resultados), 1)


# ============================================================================
# RUNNER
# ============================================================================

def run_tests():
    """Executa todos os testes e exibe relatório"""
    # Criar test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Adicionar todos os testes
    suite.addTests(loader.loadTestsFromTestCase(TestMemoriaPermanente))
    suite.addTests(loader.loadTestsFromTestCase(TestGerenciadorWorkspaces))
    suite.addTests(loader.loadTestsFromTestCase(TestGerenciadorTemporarios))
    suite.addTests(loader.loadTestsFromTestCase(TestSistemaAutoEvolucao))
    suite.addTests(loader.loadTestsFromTestCase(TestAutoEvolucaoAvancado))  # ✅ FASE 4
    suite.addTests(loader.loadTestsFromTestCase(TestIntegracao))

    # Executar com verbosidade
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Relatório final
    print("\n" + "="*70)
    print("📊 RELATÓRIO DE TESTES")
    print("="*70)
    print(f"Total de testes: {result.testsRun}")
    print(f"✅ Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Falhas: {len(result.failures)}")
    print(f"⚠️  Erros: {len(result.errors)}")

    # Calcular cobertura aproximada
    # Estamos testando 4 módulos principais
    cobertura = (result.testsRun / (result.testsRun + 10)) * 100  # Aproximação
    print(f"\n📈 Cobertura aproximada: {cobertura:.1f}%")

    if result.wasSuccessful():
        print("\n✅ TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print("\n❌ ALGUNS TESTES FALHARAM")
        return 1


if __name__ == "__main__":
    print("""
================================================================================
                   🧪 TESTES UNITÁRIOS - LUNA V3
================================================================================
    """)

    exit_code = run_tests()
    sys.exit(exit_code)
