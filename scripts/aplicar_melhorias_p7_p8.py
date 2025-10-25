#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Aplicar Melhorias P7/P8 Manualmente

Aplica melhorias de prioridade 7 e 8 de forma controlada,
validando cada aplicação antes de prosseguir.

Uso:
    python scripts/aplicar_melhorias_p7_p8.py [--dry-run] [--max N]

Opções:
    --dry-run: Apenas lista as melhorias sem aplicar
    --max N: Aplica no máximo N melhorias (padrão: todas)
    --continue: Continua de onde parou (pula já processadas)
"""

import json
import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime


class AplicadorMelhorias:
    """Aplica melhorias P7/P8 de forma controlada."""

    def __init__(self, dry_run: bool = False, max_melhorias: int = None):
        self.dry_run = dry_run
        self.max_melhorias = max_melhorias
        self.fila_path = Path("Luna/.melhorias/fila_melhorias.json")
        self.log_path = Path("LOGS_EXECUCAO/aplicacao_p7_p8.log")
        self.resultados_path = Path("LOGS_EXECUCAO/resultados_p7_p8.json")

        # Estatísticas
        self.total_processadas = 0
        self.sucessos = 0
        self.falhas = 0
        self.puladas = 0

        # Criar diretórios
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def carregar_fila(self) -> List[Dict]:
        """Carrega fila de melhorias."""
        if not self.fila_path.exists():
            print(f"❌ Arquivo de fila não encontrado: {self.fila_path}")
            sys.exit(1)

        with open(self.fila_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Buscar em 'pendentes' (novo formato) ou 'melhorias' (formato antigo)
            return data.get('pendentes', data.get('melhorias', []))

    def filtrar_p7_p8(self, melhorias: List[Dict]) -> List[Dict]:
        """Filtra melhorias P7 e P8."""
        filtradas = [
            m for m in melhorias
            if m.get('prioridade', 0) in [7, 8]
        ]

        # Ordenar por prioridade (maior primeiro)
        filtradas.sort(key=lambda m: m.get('prioridade', 0), reverse=True)

        return filtradas

    def carregar_processadas(self) -> set:
        """Carrega IDs de melhorias já processadas."""
        if not self.resultados_path.exists():
            return set()

        with open(self.resultados_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return set(r['id'] for r in data.get('processadas', []))

    def aplicar_melhoria(self, melhoria: Dict) -> Tuple[bool, str]:
        """
        Aplica uma melhoria usando o sistema de auto-evolução.

        Returns:
            (sucesso, mensagem)
        """
        # Criar arquivo temporário com a melhoria
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8')
        try:
            json.dump(melhoria, temp_file, ensure_ascii=False, indent=2)
            temp_file.close()

            # Preparar comando
            cmd = [
                sys.executable,
                "-c",
                f"""
import sys
import json
sys.path.insert(0, '.')
from sistema_auto_evolucao import SistemaAutoEvolucao

# Criar sistema
sistema = SistemaAutoEvolucao()

# Carregar melhoria do arquivo temporário
with open(r'{temp_file.name}', 'r', encoding='utf-8') as f:
    melhoria = json.load(f)

# Aplicar melhoria
resultado = sistema.aplicar_modificacao(melhoria, memoria=None)

# Retornar resultado
if resultado:
    print("SUCESSO")
    sys.exit(0)
else:
    print("FALHA")
    sys.exit(1)
"""
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(Path.cwd())
            )
        finally:
            # Remover arquivo temporário
            try:
                Path(temp_file.name).unlink()
            except:
                pass

        try:

            sucesso = result.returncode == 0
            mensagem = result.stdout.strip() if sucesso else result.stderr.strip()

            return sucesso, mensagem

        except subprocess.TimeoutExpired:
            return False, "Timeout (>60s)"
        except Exception as e:
            return False, str(e)

    def validar_sintaxe(self, arquivo: str = "luna_v3_FINAL_OTIMIZADA.py") -> bool:
        """Valida sintaxe do arquivo após modificação."""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", arquivo],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False

    def salvar_resultado(self, melhoria: Dict, sucesso: bool, mensagem: str):
        """Salva resultado da aplicação."""
        # Carregar resultados existentes
        if self.resultados_path.exists():
            with open(self.resultados_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {
                'inicio': datetime.now().isoformat(),
                'processadas': [],
                'estatisticas': {}
            }

        # Adicionar resultado
        data['processadas'].append({
            'id': melhoria.get('id', 'unknown'),
            'tipo': melhoria.get('tipo'),
            'prioridade': melhoria.get('prioridade'),
            'alvo': melhoria.get('alvo'),
            'sucesso': sucesso,
            'mensagem': mensagem,
            'timestamp': datetime.now().isoformat()
        })

        # Atualizar estatísticas
        data['estatisticas'] = {
            'total': len(data['processadas']),
            'sucessos': sum(1 for r in data['processadas'] if r['sucesso']),
            'falhas': sum(1 for r in data['processadas'] if not r['sucesso']),
            'taxa_sucesso': round(
                sum(1 for r in data['processadas'] if r['sucesso']) /
                len(data['processadas']) * 100,
                2
            ) if data['processadas'] else 0
        }

        # Salvar
        with open(self.resultados_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def log(self, mensagem: str):
        """Registra mensagem no log."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linha = f"[{timestamp}] {mensagem}\n"

        # Console
        print(mensagem)

        # Arquivo
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(linha)

    def executar(self):
        """Executa processamento das melhorias."""
        self.log("="*80)
        self.log("APLICACAO MANUAL DE MELHORIAS P7/P8")
        self.log("="*80)

        # Carregar fila
        self.log("[*] Carregando fila de melhorias...")
        melhorias = self.carregar_fila()
        self.log(f"   Total na fila: {len(melhorias)}")

        # Filtrar P7/P8
        melhorias_p7_p8 = self.filtrar_p7_p8(melhorias)
        self.log(f"   Melhorias P7/P8: {len(melhorias_p7_p8)}")

        # Carregar já processadas (se --continue)
        processadas = self.carregar_processadas()
        if processadas:
            self.log(f"   Ja processadas anteriormente: {len(processadas)}")

        # Aplicar limite
        if self.max_melhorias:
            melhorias_p7_p8 = melhorias_p7_p8[:self.max_melhorias]
            self.log(f"   Limitado a: {self.max_melhorias} melhorias")

        self.log("")

        # Modo dry-run
        if self.dry_run:
            self.log("[DRY-RUN] MODO DRY-RUN - Apenas listando melhorias:")
            for i, m in enumerate(melhorias_p7_p8, 1):
                self.log(f"   {i}. P{m['prioridade']} - {m['tipo']} - {m['alvo']}")
            return

        # Processar melhorias
        self.log(f"[>>] Processando {len(melhorias_p7_p8)} melhorias...")
        self.log("")

        for i, melhoria in enumerate(melhorias_p7_p8, 1):
            melhoria_id = melhoria.get('id', f"melhoria_{i}")

            # Pular se já processada
            if melhoria_id in processadas:
                self.log(f"[SKIP] [{i}/{len(melhorias_p7_p8)}] Pulando (ja processada): {melhoria_id}")
                self.puladas += 1
                continue

            self.log("-"*80)
            self.log(f"[{i}/{len(melhorias_p7_p8)}] Processando melhoria:")
            self.log(f"   ID: {melhoria_id}")
            self.log(f"   Tipo: {melhoria['tipo']}")
            self.log(f"   Prioridade: P{melhoria['prioridade']}")
            self.log(f"   Alvo: {melhoria['alvo']}")

            # Aplicar
            sucesso, mensagem = self.aplicar_melhoria(melhoria)

            if sucesso:
                # Validar sintaxe
                if self.validar_sintaxe():
                    self.log(f"[OK] SUCESSO: {mensagem}")
                    self.log(f"   Sintaxe: OK")
                    self.sucessos += 1
                else:
                    self.log(f"[ERRO] FALHA: Sintaxe invalida apos aplicacao")
                    sucesso = False
                    mensagem = "Sintaxe invalida"
                    self.falhas += 1
            else:
                self.log(f"[ERRO] FALHA: {mensagem}")
                self.falhas += 1

            # Salvar resultado
            self.salvar_resultado(melhoria, sucesso, mensagem)
            self.total_processadas += 1

            # Exibir progresso
            taxa_sucesso = (self.sucessos / self.total_processadas * 100) if self.total_processadas > 0 else 0
            self.log(f"   Progresso: {self.total_processadas}/{len(melhorias_p7_p8)} | Taxa sucesso: {taxa_sucesso:.1f}%")
            self.log("")

        # Relatório final
        self.log("="*80)
        self.log("RELATORIO FINAL")
        self.log("="*80)
        self.log(f"Total processadas: {self.total_processadas}")
        self.log(f"Sucessos: {self.sucessos}")
        self.log(f"Falhas: {self.falhas}")
        self.log(f"Puladas: {self.puladas}")

        if self.total_processadas > 0:
            taxa = (self.sucessos / self.total_processadas * 100)
            self.log(f"Taxa de sucesso: {taxa:.1f}%")

            if taxa >= 80:
                self.log("")
                self.log("[SUCCESS] TAXA DE SUCESSO OTIMA (>= 80%)")
                self.log("[OK] Sistema pronto para auto-aplicacao completa!")
            elif taxa >= 60:
                self.log("")
                self.log("[WARNING] TAXA DE SUCESSO MODERADA (60-80%)")
                self.log("[!] Revisar falhas antes de ativar auto-aplicacao")
            else:
                self.log("")
                self.log("[ERROR] TAXA DE SUCESSO BAIXA (< 60%)")
                self.log("[X] NAO ativar auto-aplicacao - investigar problemas")

        self.log("")
        self.log(f"[*] Resultados salvos em: {self.resultados_path}")
        self.log(f"[*] Log completo em: {self.log_path}")
        self.log("="*80)


def main():
    """Função principal."""
    import argparse

    parser = argparse.ArgumentParser(description="Aplicar melhorias P7/P8 manualmente")
    parser.add_argument("--dry-run", action="store_true", help="Apenas listar melhorias")
    parser.add_argument("--max", type=int, help="Número máximo de melhorias a processar")
    parser.add_argument("--continue", dest="continuar", action="store_true", help="Continuar de onde parou")

    args = parser.parse_args()

    # Criar aplicador
    aplicador = AplicadorMelhorias(
        dry_run=args.dry_run,
        max_melhorias=args.max
    )

    # Executar
    try:
        aplicador.executar()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompido pelo usuário")
        print(f"Progresso salvo em: {aplicador.resultados_path}")
        print("Use --continue para continuar de onde parou")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
