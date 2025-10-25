#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 SISTEMA DE ROLLBACK INTELIGENTE - Luna V3 (Versão Compacta)

Rollback automático se auto-melhorias quebrarem testes.

Criado: 2025-10-20
Melhoria 1.4 - Nível 1
"""

import sys, os
if sys.platform == 'win32':
    os.environ['PYTHONUTF8'] = '1'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except: pass

from pathlib import Path
from datetime import datetime
import json


class RollbackManager:
    """Gerencia snapshots e rollback de código."""

    def __init__(self, backup_dir: str = ".rollback_backups"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        self.current_snapshot = None

    def create_snapshot(self, codigo: str, identificador: str = "default") -> str:
        """
        Cria snapshot do código.

        Args:
            codigo: Código atual
            identificador: Nome do snapshot

        Returns:
            Path do snapshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"snapshot_{identificador}_{timestamp}.py"
        snapshot_path = self.backup_dir / filename

        # Salvar código
        snapshot_path.write_text(codigo, encoding='utf-8')

        # Salvar metadata
        meta = {
            'timestamp': timestamp,
            'identificador': identificador,
            'size': len(codigo),
            'lines': len(codigo.split('\n'))
        }

        meta_path = snapshot_path.with_suffix('.json')
        meta_path.write_text(json.dumps(meta, indent=2), encoding='utf-8')

        self.current_snapshot = snapshot_path
        return str(snapshot_path)

    def rollback(self) -> str:
        """
        Restaura último snapshot.

        Returns:
            Código restaurado
        """
        if not self.current_snapshot or not self.current_snapshot.exists():
            raise FileNotFoundError("Nenhum snapshot disponível")

        codigo = self.current_snapshot.read_text(encoding='utf-8')
        print(f"🔄 Rollback executado: {self.current_snapshot.name}")

        return codigo

    def validate_code(self, codigo: str) -> bool:
        """
        Valida código modificado.

        Args:
            codigo: Código a validar

        Returns:
            True se válido
        """
        try:
            import ast
            ast.parse(codigo)
            return True
        except SyntaxError:
            return False

    def apply_with_rollback(self, codigo_original: str, codigo_novo: str, run_tests: callable = None) -> tuple:
        """
        Aplica mudança com rollback automático.

        Args:
            codigo_original: Código antes da mudança
            codigo_novo: Código modificado
            run_tests: Função para executar testes (opcional)

        Returns:
            (sucesso: bool, codigo_final: str, mensagem: str)
        """
        # 1. Criar snapshot
        snapshot = self.create_snapshot(codigo_original, "pre_apply")
        print(f"📸 Snapshot criado: {Path(snapshot).name}")

        # 2. Validar sintaxe
        if not self.validate_code(codigo_novo):
            print("❌ Código novo tem erro de sintaxe")
            codigo_restaurado = self.rollback()
            return False, codigo_restaurado, "Erro de sintaxe - rollback executado"

        # 3. Executar testes (se fornecido)
        if run_tests:
            try:
                if not run_tests(codigo_novo):
                    print("❌ Testes falharam")
                    codigo_restaurado = self.rollback()
                    return False, codigo_restaurado, "Testes falharam - rollback executado"
            except Exception as e:
                print(f"❌ Erro ao executar testes: {e}")
                codigo_restaurado = self.rollback()
                return False, codigo_restaurado, f"Erro nos testes - rollback executado"

        # 4. Tudo OK
        print("✅ Validação OK - mudança aplicada")
        return True, codigo_novo, "Mudança aplicada com sucesso"

    def list_snapshots(self) -> list:
        """Lista snapshots disponíveis."""
        return sorted(self.backup_dir.glob("snapshot_*.py"))

    def cleanup_old_snapshots(self, keep_last: int = 10):
        """Remove snapshots antigos."""
        snapshots = self.list_snapshots()
        if len(snapshots) > keep_last:
            for old in snapshots[:-keep_last]:
                old.unlink()
                old.with_suffix('.json').unlink(missing_ok=True)


# Teste
if __name__ == "__main__":
    print("🔄 Testando Rollback Manager\n")

    manager = RollbackManager()

    # Código original
    codigo_original = "def teste(): pass"

    # Código novo válido
    codigo_novo_ok = "def teste():\n    return 42"

    # Código novo com erro
    codigo_novo_erro = "def teste(\n    pass"  # Sintaxe errada

    # Teste 1: Aplicar código válido
    print("📊 TESTE 1: Código válido")
    sucesso, codigo, msg = manager.apply_with_rollback(codigo_original, codigo_novo_ok)
    print(f"   Resultado: {'✅ OK' if sucesso else '❌ FALHOU'}")
    print(f"   Mensagem: {msg}\n")

    # Teste 2: Aplicar código com erro (deve fazer rollback)
    print("📊 TESTE 2: Código com erro de sintaxe")
    sucesso, codigo, msg = manager.apply_with_rollback(codigo_original, codigo_novo_erro)
    print(f"   Resultado: {'✅ OK (rollback)' if not sucesso else '❌ FALHOU (não detectou erro)'}")
    print(f"   Mensagem: {msg}\n")

    # Teste 3: Listar snapshots
    snapshots = manager.list_snapshots()
    print(f"📊 TESTE 3: Snapshots criados: {len(snapshots)}")
    for s in snapshots:
        print(f"   - {s.name}")

    print("\n✅ Melhoria 1.4: FUNCIONAL")
