#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧬 SISTEMA DE AUTO-EVOLUÇÃO
============================

Permite que Luna se auto-modifique de forma segura e inteligente.

Features:
- Fila de melhorias (anota durante, aplica depois)
- Backup automático antes de cada modificação
- Validação completa (sintaxe + import + testes)
- Rollback automático se quebrar
- Limpeza inteligente de backups
- Zonas protegidas (código crítico)
- Log detalhado + resumo
- Memória de erros (não repete)
"""

import os
import shutil
import ast
import sys
import importlib
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json
import hashlib


# ============================================================================
# ZONAS PROTEGIDAS (CÓDIGO CRÍTICO QUE NÃO DEVE SER MODIFICADO)
# ============================================================================

ZONAS_PROTEGIDAS = [
    # Sistema de backup/rollback (para não quebrar sua própria segurança)
    "def _criar_backup",
    "def _validar_codigo",
    "def _validar_sintaxe",
    "def _validar_import",
    "def _validar_execucao",
    "def _rollback",
    "class SistemaAutoEvolucao",
    
    # Memória permanente (para não perder aprendizados)
    "def _carregar_memoria",
    "def _salvar_memoria",
    "class MemoriaPermanente",
    
    # Credenciais (segurança)
    "class Cofre",
    "def _gerar_chave",
    "master_password",
    
    # Núcleo de execução (coração do agente)
    "def __init__",  # Construtores são críticos
    "def executar_tarefa",  # Loop principal
    "class AgenteCompletoFinal",  # Classe principal
]


# ============================================================================
# FILA DE MELHORIAS
# ============================================================================

class FilaDeMelhorias:
    """Gerencia melhorias detectadas durante execução"""
    
    def __init__(self):
        self.melhorias_pendentes = []
        self.melhorias_aplicadas = []
        self.melhorias_falhadas = []
    
    def adicionar(self, tipo: str, alvo: str, motivo: str, codigo_sugerido: str, 
                 prioridade: int = 5):
        """
        Adiciona melhoria à fila
        
        Args:
            tipo: 'otimizacao', 'bug_fix', 'nova_feature', 'refatoracao'
            alvo: Função/classe/módulo a modificar
            motivo: Por que fazer essa melhoria
            codigo_sugerido: Código da modificação
            prioridade: 1-10 (10 = mais urgente)
        """
        melhoria = {
            'id': self._gerar_id(f"{alvo}{motivo}{datetime.now()}"),
            'tipo': tipo,
            'alvo': alvo,
            'motivo': motivo,
            'codigo': codigo_sugerido,
            'prioridade': prioridade,
            'detectado_em': datetime.now().isoformat(),
            'status': 'pendente'
        }
        
        self.melhorias_pendentes.append(melhoria)
        print(f"    💡 Melhoria anotada: {motivo[:60]}...")
        
        return melhoria['id']
    
    def obter_pendentes(self, ordenar_por_prioridade: bool = True) -> List[Dict]:
        """Retorna melhorias pendentes"""
        if ordenar_por_prioridade:
            return sorted(self.melhorias_pendentes, 
                         key=lambda x: x['prioridade'], 
                         reverse=True)
        return self.melhorias_pendentes
    
    def marcar_aplicada(self, melhoria_id: str, detalhes: Dict):
        """Marca melhoria como aplicada"""
        for m in self.melhorias_pendentes:
            if m['id'] == melhoria_id:
                m['status'] = 'aplicada'
                m['aplicada_em'] = datetime.now().isoformat()
                m['detalhes'] = detalhes
                self.melhorias_aplicadas.append(m)
                self.melhorias_pendentes.remove(m)
                break
    
    def marcar_falhada(self, melhoria_id: str, erro: str):
        """Marca melhoria como falhada"""
        for m in self.melhorias_pendentes:
            if m['id'] == melhoria_id:
                m['status'] = 'falhada'
                m['erro'] = erro
                m['tentada_em'] = datetime.now().isoformat()
                self.melhorias_falhadas.append(m)
                self.melhorias_pendentes.remove(m)
                break
    
    def limpar(self):
        """Limpa todas as filas"""
        self.melhorias_pendentes.clear()
        self.melhorias_aplicadas.clear()
        self.melhorias_falhadas.clear()
    
    def _gerar_id(self, texto: str) -> str:
        """Gera ID único para melhoria"""
        return hashlib.md5(texto.encode()).hexdigest()[:12]


# ============================================================================
# SISTEMA DE AUTO-EVOLUÇÃO
# ============================================================================

class SistemaAutoEvolucao:
    """
    Sistema completo de auto-modificação segura
    """
    
    def __init__(self, arquivo_alvo: str = "luna_v3_FINAL_OTIMIZADA.py",
                 dir_backups: str = "backups_auto_evolucao",
                 max_backups: int = 5):
        
        self.arquivo_alvo = arquivo_alvo
        self.dir_backups = dir_backups
        self.max_backups = max_backups

        # ✅ VALIDAÇÃO: Verificar que arquivo alvo existe
        if not os.path.exists(self.arquivo_alvo):
            raise FileNotFoundError(
                f"❌ Arquivo alvo não encontrado: {self.arquivo_alvo}\n"
                f"   O sistema de auto-evolução precisa que o arquivo exista.\n"
                f"   Verifique o caminho e tente novamente."
            )

        # Criar diretório de backups
        Path(self.dir_backups).mkdir(exist_ok=True)
        
        # Log de modificações
        self.log_file = "auto_modificacoes.log"
        
        # Estatísticas
        self.stats = {
            'total_modificacoes': 0,
            'sucesso': 0,
            'falhas': 0,
            'rollbacks': 0
        }
    
    # ========================================================================
    # BACKUP E ROLLBACK
    # ========================================================================
    
    def _criar_backup(self, motivo: str) -> str:
        """
        Cria backup do arquivo antes de modificar
        
        Returns:
            Caminho do backup criado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{self.dir_backups}/agente_backup_{timestamp}.py"
        
        try:
            shutil.copy2(self.arquivo_alvo, backup_path)
            
            # Criar metadados do backup
            meta_path = f"{backup_path}.meta"
            meta = {
                'timestamp': timestamp,
                'motivo': motivo,
                'arquivo_original': self.arquivo_alvo,
                'hash': self._calcular_hash(self.arquivo_alvo)
            }

            with open(meta_path, 'w', encoding='utf-8') as f:
                json.dump(meta, f, indent=2)

            self._log(f"Backup criado: {backup_path}")
            return backup_path
            
        except Exception as e:
            self._log(f"ERRO ao criar backup: {e}", nivel='ERROR')
            raise
    
    def _rollback(self, backup_path: str) -> bool:
        """
        Restaura código a partir de backup
        
        Returns:
            True se rollback bem-sucedido
        """
        try:
            if not os.path.exists(backup_path):
                self._log(f"ERRO: Backup não encontrado: {backup_path}", nivel='ERROR')
                return False
            
            shutil.copy2(backup_path, self.arquivo_alvo)
            self.stats['rollbacks'] += 1
            self._log(f"Rollback realizado: {backup_path}")
            
            return True
            
        except Exception as e:
            self._log(f"ERRO crítico no rollback: {e}", nivel='CRITICAL')
            return False
    
    def _limpar_backups_antigos(self):
        """
        Mantém apenas os N backups mais recentes
        Deleta backups validados há mais de 24h
        """
        try:
            backups = sorted(Path(self.dir_backups).glob("agente_backup_*.py"))

            # Manter apenas max_backups mais recentes
            if len(backups) > self.max_backups:
                for backup in backups[:-self.max_backups]:
                    meta_file = f"{backup}.meta"

                    # Verificar se tem mais de 24h
                    if os.path.exists(meta_file):
                        with open(meta_file, 'r', encoding='utf-8') as f:
                            meta = json.load(f)

                        timestamp = datetime.strptime(meta['timestamp'], "%Y%m%d_%H%M%S")
                        if datetime.now() - timestamp > timedelta(hours=24):
                            os.remove(backup)
                            os.remove(meta_file)
                            self._log(f"Backup antigo deletado: {backup}")

        except Exception as e:
            self._log(f"Erro ao limpar backups: {e}", nivel='WARNING')

    def _aplicar_modificacao_ast(
        self,
        codigo_original: str,
        codigo_novo: str,
        alvo: str
    ) -> Optional[str]:
        """
        Aplica modificação usando AST para modificações precisas.

        ✅ IMPLEMENTADO: Resolve o TODO da linha 411

        Args:
            codigo_original: Código Python original completo
            codigo_novo: Código da modificação (função, classe, etc.)
            alvo: Nome do alvo (ex: "def funcao", "class MinhaClasse")

        Returns:
            Código modificado completo ou None se falhar
        """
        try:
            # Parse do código original
            tree_original = ast.parse(codigo_original)

            # Parse do código novo
            tree_novo = ast.parse(codigo_novo)

            # Extrair nome do alvo
            # Ex: "def funcao" -> "funcao", "class MinhaClasse" -> "MinhaClasse"
            nome_alvo = alvo.split()[-1] if ' ' in alvo else alvo

            # Encontrar e substituir o nó correspondente
            substituido = False

            for i, node in enumerate(tree_original.body):
                # Verificar se é o nó que queremos substituir
                if hasattr(node, 'name') and node.name == nome_alvo:
                    # Substituir pelo(s) novo(s) nó(s)
                    # Se o código novo tem múltiplos nós, substituir por todos
                    if len(tree_novo.body) == 1:
                        tree_original.body[i] = tree_novo.body[0]
                    else:
                        # Múltiplos nós - substituir e inserir os demais
                        tree_original.body[i] = tree_novo.body[0]
                        for j, novo_node in enumerate(tree_novo.body[1:], 1):
                            tree_original.body.insert(i + j, novo_node)

                    substituido = True
                    self._log(f"Nó '{nome_alvo}' substituído via AST")
                    break

            if not substituido:
                # Não encontrou - adicionar ao final (nova função/classe)
                self._log(f"Alvo '{nome_alvo}' não encontrado - adicionando ao final")
                tree_original.body.extend(tree_novo.body)

            # Converter AST de volta para código
            # Usar ast.unparse (Python 3.9+) ou fallback para código completo
            try:
                codigo_modificado = ast.unparse(tree_original)
                return codigo_modificado
            except AttributeError:
                # Python < 3.9 - não tem ast.unparse
                # Fallback: retornar código novo completo
                self._log("ast.unparse não disponível (Python < 3.9) - usando fallback")
                return codigo_novo

        except SyntaxError as e:
            self._log(f"Erro de sintaxe ao processar AST: {e}", nivel='ERROR')
            return None
        except Exception as e:
            self._log(f"Erro ao aplicar modificação via AST: {e}", nivel='ERROR')
            return None
    
    # ========================================================================
    # VALIDAÇÃO
    # ========================================================================
    
    def _validar_codigo(self, arquivo: str) -> Tuple[bool, str]:
        """
        Validação completa: sintaxe + import + execução básica
        
        Returns:
            (sucesso, mensagem_erro)
        """
        # 1. Validar sintaxe
        valido, erro = self._validar_sintaxe(arquivo)
        if not valido:
            return False, f"Sintaxe inválida: {erro}"
        
        # 2. Validar import
        valido, erro = self._validar_import(arquivo)
        if not valido:
            return False, f"Import falhou: {erro}"
        
        # 3. Validar execução básica
        valido, erro = self._validar_execucao(arquivo)
        if not valido:
            return False, f"Execução falhou: {erro}"
        
        return True, "Validação completa OK"
    
    def _validar_sintaxe(self, arquivo: str) -> Tuple[bool, str]:
        """Valida sintaxe Python"""
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                codigo = f.read()
            
            ast.parse(codigo)
            return True, "Sintaxe OK"
            
        except SyntaxError as e:
            return False, f"Linha {e.lineno}: {e.msg}"
        except Exception as e:
            return False, str(e)
    
    def _validar_import(self, arquivo: str) -> Tuple[bool, str]:
        """Valida se o módulo pode ser importado"""
        try:
            # Tentar importar como módulo
            module_name = Path(arquivo).stem
            spec = importlib.util.spec_from_file_location(module_name, arquivo)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            
            return True, "Import OK"
            
        except Exception as e:
            return False, str(e)
    
    def _validar_execucao(self, arquivo: str) -> Tuple[bool, str]:
        """
        Validação básica de execução
        Testa se classes/funções principais estão acessíveis
        """
        try:
            # Importar módulo
            module_name = Path(arquivo).stem
            spec = importlib.util.spec_from_file_location(module_name, arquivo)
            if not spec or not spec.loader:
                return False, "Não foi possível carregar módulo"
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Verificar se classes principais existem
            classes_esperadas = ['AgenteCompletoFinal', 'SistemaFerramentasCompleto']
            for classe in classes_esperadas:
                if not hasattr(module, classe):
                    return False, f"Classe '{classe}' não encontrada"
            
            return True, "Execução OK"
            
        except Exception as e:
            return False, str(e)
    
    def _verificar_zona_protegida(self, codigo: str, alvo: str) -> bool:
        """
        Verifica se modificação toca em zona protegida
        
        Returns:
            True se é zona protegida (NÃO DEVE MODIFICAR)
        """
        for zona in ZONAS_PROTEGIDAS:
            if zona in codigo or zona in alvo:
                return True
        return False
    
    # ========================================================================
    # APLICAÇÃO DE MODIFICAÇÕES
    # ========================================================================
    
    def aplicar_modificacao(self, melhoria: Dict, memoria=None) -> bool:
        """
        Aplica uma modificação ao código
        
        Args:
            melhoria: Dict com dados da melhoria
            memoria: Instância de MemoriaPermanente (opcional)
        
        Returns:
            True se aplicada com sucesso
        """
        melhoria_id = melhoria['id']
        tipo = melhoria['tipo']
        alvo = melhoria['alvo']
        motivo = melhoria['motivo']
        codigo = melhoria['codigo']
        
        self._log(f"\n{'='*70}")
        self._log(f"MODIFICAÇÃO: {tipo}")
        self._log(f"Alvo: {alvo}")
        self._log(f"Motivo: {motivo}")
        self._log(f"{'='*70}")
        
        # 1. Verificar zona protegida
        if self._verificar_zona_protegida(codigo, alvo):
            erro = f"ZONA PROTEGIDA: Não é permitido modificar '{alvo}'"
            self._log(erro, nivel='WARNING')
            
            if memoria:
                memoria.adicionar_aprendizado(
                    'bug',
                    f"Não modificar {alvo} - é zona protegida",
                    contexto=f"Tentativa bloqueada: {motivo}",
                    tags=['auto-modificacao', 'zona-protegida']
                )
            
            return False
        
        # 2. Criar backup
        try:
            backup_path = self._criar_backup(motivo)

            # ✅ FASE 3.1: Validar que backup foi criado com sucesso
            if not os.path.exists(backup_path):
                raise RuntimeError(f"Backup não foi criado: {backup_path}")

            # Validar que backup tem tamanho razoável (não está vazio)
            if os.path.getsize(backup_path) == 0:
                raise RuntimeError(f"Backup está vazio: {backup_path}")

            # Validar que backup tem mesmo hash que original (integridade)
            hash_original = self._calcular_hash(self.arquivo_alvo)
            hash_backup = self._calcular_hash(backup_path)
            if hash_original != hash_backup:
                raise RuntimeError(f"Hash do backup difere do original - backup corrompido")

            self._log(f"✅ Backup validado: {backup_path}")

        except Exception as e:
            self._log(f"ERRO ao criar/validar backup: {e}", nivel='ERROR')
            return False

        # 3. Aplicar modificação
        try:
            with open(self.arquivo_alvo, 'r', encoding='utf-8') as f:
                codigo_original = f.read()

            # ✅ IMPLEMENTADO: Usar AST para modificações precisas
            # Tentar aplicar modificação via AST primeiro
            codigo_modificado = self._aplicar_modificacao_ast(
                codigo_original, codigo, alvo
            )

            # Se AST falhar, usar fallback (substituição completa)
            if codigo_modificado is None:
                self._log("Fallback: usando substituição completa do código")
                codigo_modificado = codigo

            with open(self.arquivo_alvo, 'w', encoding='utf-8') as f:
                f.write(codigo_modificado)

            self._log("Código modificado")

        except Exception as e:
            self._log(f"ERRO ao modificar código: {e}", nivel='ERROR')
            self._rollback(backup_path)
            return False
        
        # 4. Validar
        print("    ✅ Validando modificação...")
        valido, erro_validacao = self._validar_codigo(self.arquivo_alvo)
        
        if not valido:
            self._log(f"VALIDAÇÃO FALHOU: {erro_validacao}", nivel='ERROR')
            print(f"    ❌ Validação falhou: {erro_validacao}")
            
            # Rollback automático
            self._rollback(backup_path)
            self.stats['falhas'] += 1
            
            # Salvar na memória para não repetir
            if memoria:
                memoria.adicionar_aprendizado(
                    'bug',
                    f"Modificação de {alvo} com esta abordagem causa erro: {erro_validacao}",
                    contexto=motivo,
                    tags=['auto-modificacao', 'erro-validacao']
                )
            
            return False
        
        # 5. Sucesso!
        print("    ✅ Validação passou!")
        self._log("MODIFICAÇÃO APLICADA COM SUCESSO")
        self.stats['sucesso'] += 1
        self.stats['total_modificacoes'] += 1
        
        # Salvar sucesso na memória
        if memoria:
            memoria.adicionar_aprendizado(
                'tecnica',
                f"Modificação bem-sucedida: {motivo}",
                contexto=f"Alvo: {alvo}, Tipo: {tipo}",
                tags=['auto-modificacao', 'sucesso']
            )
        
        return True
    
    def processar_fila(self, fila: FilaDeMelhorias, memoria=None) -> Dict:
        """
        Processa todas melhorias na fila
        
        Returns:
            Dict com estatísticas do processamento
        """
        melhorias = fila.obter_pendentes()
        
        if not melhorias:
            return {'total': 0, 'sucesso': 0, 'falhas': 0}
        
        print(f"\n{'='*70}")
        print("🔧 AUTO-MELHORIAS DETECTADAS")
        print(f"{'='*70}")
        print(f"\n📋 {len(melhorias)} melhorias na fila\n")
        
        resultados = {'total': len(melhorias), 'sucesso': 0, 'falhas': 0}
        
        for i, melhoria in enumerate(melhorias, 1):
            print(f"\n📝 Melhoria {i}/{len(melhorias)}")
            print(f"   Tipo: {melhoria['tipo']}")
            print(f"   Alvo: {melhoria['alvo']}")
            print(f"   Motivo: {melhoria['motivo']}")
            print(f"   Prioridade: {melhoria['prioridade']}/10")
            
            sucesso = self.aplicar_modificacao(melhoria, memoria)
            
            if sucesso:
                print(f"   ✅ Aplicada com sucesso\n")
                fila.marcar_aplicada(melhoria['id'], {'timestamp': datetime.now().isoformat()})
                resultados['sucesso'] += 1
            else:
                print(f"   ❌ Falhou (rollback automático)\n")
                fila.marcar_falhada(melhoria['id'], "Validação falhou")
                resultados['falhas'] += 1
        
        # Limpar backups antigos
        self._limpar_backups_antigos()
        
        # Resumo
        self._imprimir_resumo(resultados, fila)
        
        return resultados
    
    def _imprimir_resumo(self, resultados: Dict, fila: FilaDeMelhorias):
        """Imprime resumo das modificações"""
        print(f"\n{'='*70}")
        print("🎊 AUTO-MELHORIAS CONCLUÍDAS")
        print(f"{'='*70}\n")
        
        print(f"📊 Resumo:")
        print(f"   ✅ {resultados['sucesso']} melhorias aplicadas")
        print(f"   ❌ {resultados['falhas']} falhas (revertidas)")
        
        if fila.melhorias_aplicadas:
            print(f"\n✅ Melhorias aplicadas:")
            for m in fila.melhorias_aplicadas[-5:]:  # Últimas 5
                print(f"   • {m['motivo'][:60]}")
        
        if fila.melhorias_falhadas:
            print(f"\n⚠️  Melhorias que falharam:")
            for m in fila.melhorias_falhadas[-3:]:  # Últimas 3
                print(f"   • {m['motivo'][:60]}")
        
        # Backups mantidos
        backups = list(Path(self.dir_backups).glob("agente_backup_*.py"))
        print(f"\n💾 Backups mantidos: {len(backups)}")
        
        print(f"\n{'='*70}\n")
    
    # ========================================================================
    # UTILIDADES
    # ========================================================================
    
    def _calcular_hash(self, arquivo: str) -> str:
        """Calcula hash MD5 do arquivo"""
        with open(arquivo, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def _log(self, mensagem: str, nivel: str = 'INFO'):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linha = f"[{timestamp}] {nivel}: {mensagem}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(linha)
    
    def obter_estatisticas(self) -> Dict:
        """Retorna estatísticas do sistema"""
        backups = len(list(Path(self.dir_backups).glob("agente_backup_*.py")))
        
        return {
            **self.stats,
            'backups_mantidos': backups,
            'taxa_sucesso': (self.stats['sucesso'] / self.stats['total_modificacoes'] * 100 
                           if self.stats['total_modificacoes'] > 0 else 0)
        }


# ============================================================================
# INTERFACE DE TESTE
# ============================================================================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  🧬 SISTEMA DE AUTO-EVOLUÇÃO                                ║
║                                                              ║
║  Permite que Luna se auto-modifique com segurança          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Teste básico
    fila = FilaDeMelhorias()
    sistema = SistemaAutoEvolucao()
    
    print("✅ Sistema inicializado")
    print(f"📁 Diretório de backups: {sistema.dir_backups}")
    print(f"📄 Arquivo alvo: {sistema.arquivo_alvo}")
    print(f"🔒 {len(ZONAS_PROTEGIDAS)} zonas protegidas definidas")
    
    print("\n💡 Sistema pronto para uso!")
