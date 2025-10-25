#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Executor Automatizado de Tarefas de Teste - Luna V3

Este script executa automaticamente todas as tarefas de teste definidas
em TAREFAS_TESTE_LUNA.md, executando a Luna para cada uma e coletando
métricas detalhadas.
"""

import subprocess
import json
import time
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import shutil

# Configurações
PYTHON_PATH = r"C:\Users\Pedro Victor\AppData\Local\Programs\Python\Python313\python.exe"
LUNA_SCRIPT = "luna_batch_executor_v2.py"  # Usar versão batch V2 (monkey patching)
LOGS_DIR = "LOGS_EXECUCAO"
TELEMETRIA_API = "luna_telemetria_api.jsonl"
TELEMETRIA_FERRAMENTAS = "luna_telemetria_ferramentas.jsonl"

# Lista de tarefas (extraídas do arquivo TAREFAS_TESTE_LUNA.md)
TAREFAS = [
    {
        "id": 1,
        "nome": "Calculadora de Fibonacci",
        "complexidade": "Simples",
        "iteracoes_esperadas": "2-4",
        "prompt": """Crie um arquivo Python chamado 'fibonacci.py' com uma função que calcula o n-ésimo número da sequência de Fibonacci de forma recursiva e outra de forma iterativa. Inclua uma função main() que testa ambas as implementações com n=10 e imprime os resultados."""
    },
    {
        "id": 2,
        "nome": "Busca de Padrões em Logs",
        "complexidade": "Simples",
        "iteracoes_esperadas": "3-5",
        "prompt": """Analise o arquivo 'auto_modificacoes.log' e me diga:
1. Quantas linhas ele possui?
2. Quantas vezes aparece a palavra "ERRO"?
3. Quantas vezes aparece a palavra "SUCESSO"?
4. Mostre as 3 últimas linhas do arquivo."""
    },
    {
        "id": 3,
        "nome": "Estatísticas de Arquivos Python",
        "complexidade": "Simples",
        "iteracoes_esperadas": "3-5",
        "prompt": """Liste todos os arquivos .py na pasta raiz do projeto (não recursivo) e me informe:
1. Quantos arquivos .py existem?
2. Qual é o maior arquivo (em linhas)?
3. Qual é o menor arquivo (em linhas)?
4. Total de linhas de código Python no projeto (apenas raiz)."""
    },
    {
        "id": 4,
        "nome": "Analisador de Importações",
        "complexidade": "Média",
        "iteracoes_esperadas": "8-12",
        "prompt": """Crie um script Python chamado 'analisador_imports.py' que:
1. Lê o arquivo 'luna_v3_FINAL_OTIMIZADA.py'
2. Extrai todas as linhas de import (import X e from X import Y)
3. Classifica os imports em: biblioteca padrão, terceiros, locais
4. Gera um relatório em 'relatorio_imports.txt' com:
   - Total de imports
   - Imports por categoria
   - Lista alfabética de cada categoria
5. Execute o script e mostre o resultado"""
    },
    {
        "id": 5,
        "nome": "Comparador de Arquivos de Memória",
        "complexidade": "Média",
        "iteracoes_esperadas": "6-10",
        "prompt": """Compare os arquivos 'memoria_agente.json' e 'memoria_agente.json.bak':
1. Qual é maior em tamanho?
2. Carregue ambos como JSON e compare:
   - Quantas chaves tem cada um?
   - Quais chaves existem em um mas não no outro?
   - Se houver chave 'aprendizados', quantos aprendizados tem em cada?
3. Gere um resumo detalhado da comparação"""
    },
    {
        "id": 6,
        "nome": "Organizador de Backups",
        "complexidade": "Média",
        "iteracoes_esperadas": "8-12",
        "prompt": """Organize os arquivos de backup no projeto:
1. Liste todos os arquivos que contêm 'backup' no nome (recursivo)
2. Verifique se existe a pasta '.backups' (crie se não existir)
3. Crie um script bash 'organizar_backups.sh' que:
   - Encontra todos arquivos *backup* fora de .backups
   - Move-os para .backups mantendo uma estrutura de pastas por data
   - Gera log de operações
4. NÃO execute o script, apenas crie-o para revisão"""
    },
    {
        "id": 7,
        "nome": "Sistema de Validação de Configuração",
        "complexidade": "Complexa",
        "iteracoes_esperadas": "15-25",
        "prompt": """Crie um sistema completo de validação de configuração com 3 arquivos:

1. 'validador_config.py': Classe ValidationConfig com métodos:
   - validar_estrutura_json(arquivo) -> bool
   - validar_campos_obrigatorios(json_data, campos) -> list[erros]
   - validar_tipos(json_data, schema) -> list[erros]
   - gerar_relatorio(resultados) -> str

2. 'schemas.py': Dicionário com schemas de validação para:
   - workspace_config.json
   - memoria_agente.json

3. 'test_validador.py': Script que:
   - Testa o validador com arquivos reais do projeto
   - Gera relatório de conformidade
   - Sugere correções se houver problemas

Execute apenas o test_validador.py e mostre os resultados."""
    },
    {
        "id": 8,
        "nome": "Refatoração de Código Duplicado",
        "complexidade": "Complexa",
        "iteracoes_esperadas": "20-30",
        "prompt": """Analise o arquivo 'gerenciador_workspaces.py' e:
1. Identifique padrões de código que se repetem (duplicação)
2. Sugira refatorações para eliminar duplicação:
   - Extrair funções auxiliares
   - Criar métodos genéricos
   - Melhorar reutilização
3. Crie um arquivo 'gerenciador_workspaces_refatorado.py' com:
   - Código refatorado
   - Mesma funcionalidade
   - Mais limpo e DRY (Don't Repeat Yourself)
4. Crie 'REFATORACAO_REPORT.md' documentando:
   - O que foi mudado e por quê
   - Benefícios da refatoração
   - Riscos e testes recomendados"""
    },
    {
        "id": 9,
        "nome": "Dashboard de Métricas do Projeto",
        "complexidade": "Complexa",
        "iteracoes_esperadas": "25-35",
        "prompt": """Crie um dashboard de métricas do projeto Luna:

1. 'metricas_projeto.py': Script que coleta:
   - Estatísticas de código (.py files):
     * Total de linhas, arquivos, classes, funções
     * Complexidade média (McCabe se possível, ou aproximação)
     * Top 5 arquivos maiores
   - Estatísticas de sistema:
     * Tamanho de memoria_agente.json
     * Número de aprendizados armazenados
     * Número de workspaces
   - Estatísticas de telemetria:
     * Total de eventos em arquivos .jsonl
     * Taxa de cache hit média
     * Ferramentas mais usadas

2. 'dashboard_visualizacao.py': Gera visualização em texto:
   - Tabelas formatadas
   - Gráficos ASCII se possível
   - Comparações

3. Execute e gere 'METRICAS_PROJETO.txt' com relatório completo

Seja criativo na visualização!"""
    },
    {
        "id": 10,
        "nome": "Teste de Recuperação de Erros",
        "complexidade": "Média (com erro intencional)",
        "iteracoes_esperadas": "8-15",
        "prompt": """Execute o seguinte comando Python que contém um erro proposital:
python -c "print(variavel_inexistente)"

Quando o erro ocorrer, você deve:
1. Identificar o problema
2. Corrigir criando um script válido
3. Executar a versão corrigida
4. Confirmar que funcionou"""
    },
    {
        "id": 11,
        "nome": "Integração com APIs Externas (Simulada)",
        "complexidade": "Média-Alta",
        "iteracoes_esperadas": "12-18",
        "prompt": """Crie um sistema de integração com API (simulada):

1. 'api_client.py': Classe APIClient com:
   - Métodos: get(), post(), put(), delete()
   - Tratamento de erros (timeouts, 404, 500)
   - Retry logic (3 tentativas)
   - Rate limiting básico
   - Logging de todas operações

2. 'test_api_client.py': Testes usando httpbin.org:
   - GET /get (sucesso)
   - POST /post (com payload JSON)
   - GET /status/404 (erro 404)
   - GET /delay/10 (timeout)

3. Execute os testes e mostre resultado de cada operação

ATENÇÃO: httpbin.org é um serviço de teste real, use com moderação."""
    },
    {
        "id": 12,
        "nome": "Análise e Auto-Melhoria",
        "complexidade": "Complexa",
        "iteracoes_esperadas": "20-30",
        "prompt": """Analise o arquivo 'telemetria_manager.py' e:

1. Faça análise de código:
   - Identifique possíveis melhorias de performance
   - Identifique possíveis bugs ou edge cases não tratados
   - Identifique oportunidades de otimização
   - Verifique type hints e docstrings

2. Classifique cada melhoria por:
   - Prioridade (Alta/Média/Baixa)
   - Impacto (Alto/Médio/Baixo)
   - Esforço (Horas estimadas)

3. Crie 'MELHORIAS_TELEMETRIA.md' com:
   - Lista priorizada de melhorias
   - Código de exemplo para top 3 melhorias
   - Justificativa técnica para cada uma

4. SE o sistema de auto-evolução sugerir aplicar alguma melhoria, PERGUNTE ao usuário antes de aplicar (não aplique automaticamente)

NÃO modifique o arquivo original sem autorização."""
    }
]


class ExecutorTarefas:
    """Executa tarefas de teste na Luna e coleta métricas"""

    def __init__(self):
        self.logs_dir = Path(LOGS_DIR)
        self.logs_dir.mkdir(exist_ok=True)
        self.resultados = []

    def executar_tarefa(self, tarefa: Dict[str, Any]) -> Dict[str, Any]:
        """Executa uma tarefa na Luna e coleta métricas"""

        task_id = tarefa["id"]
        task_nome = tarefa["nome"]

        print(f"\n{'='*80}")
        print(f">> INICIANDO TAREFA {task_id}: {task_nome}")
        print(f"   Complexidade: {tarefa['complexidade']}")
        print(f"   Iteracoes esperadas: {tarefa['iteracoes_esperadas']}")
        print(f"{'='*80}\n")

        # Preparar ambiente
        timestamp_inicio = datetime.now()
        log_file = self.logs_dir / f"tarefa_{task_id:02d}_{task_nome.replace(' ', '_').lower()}.log"
        telemetria_backup_dir = self.logs_dir / f"tarefa_{task_id:02d}_telemetria"
        telemetria_backup_dir.mkdir(exist_ok=True)

        # Backup telemetria anterior (se existir)
        self._backup_telemetria_anterior(telemetria_backup_dir)

        # Limpar arquivos de telemetria para esta execução
        self._limpar_telemetria()

        # Executar Luna com a tarefa
        try:
            # Escrever prompt em arquivo temporário
            prompt_file = self.logs_dir / f"tarefa_{task_id:02d}_prompt.txt"
            prompt_file.write_text(tarefa["prompt"], encoding='utf-8')

            print(f"   Prompt salvo em: {prompt_file}")
            print(f"   Executando Luna...\n")

            # Comando para executar Luna em batch mode
            # Passar prompt como argumento
            cmd = [
                PYTHON_PATH,
                LUNA_SCRIPT,
                tarefa["prompt"],  # Primeiro argumento: prompt
                "--tier", "2",
                "--rate-mode", "2"
            ]

            # Executar com timeout de 10 minutos por tarefa
            inicio_exec = time.time()

            with open(log_file, 'w', encoding='utf-8') as log:
                processo = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding='utf-8',
                    env={**os.environ, 'PYTHONUTF8': '1', 'PYTHONIOENCODING': 'utf-8'}
                )

                try:
                    stdout, _ = processo.communicate(timeout=600)  # 10 min timeout
                    log.write(stdout)
                    print(stdout)
                    returncode = processo.returncode

                except subprocess.TimeoutExpired:
                    processo.kill()
                    stdout, _ = processo.communicate()
                    log.write(stdout)
                    log.write("\n\n[!] EXECUCAO INTERROMPIDA POR TIMEOUT (10 minutos)\n")
                    print("\n[!] TIMEOUT - Execucao interrompida apos 10 minutos")
                    returncode = -1

            tempo_execucao = time.time() - inicio_exec

            # Coletar telemetria
            metricas = self._coletar_metricas_telemetria(telemetria_backup_dir)

            # Montar resultado
            resultado = {
                "tarefa_id": task_id,
                "nome": task_nome,
                "complexidade": tarefa["complexidade"],
                "iteracoes_esperadas": tarefa["iteracoes_esperadas"],
                "timestamp_inicio": timestamp_inicio.isoformat(),
                "timestamp_fim": datetime.now().isoformat(),
                "tempo_execucao_segundos": round(tempo_execucao, 2),
                "returncode": returncode,
                "log_file": str(log_file),
                "telemetria_dir": str(telemetria_backup_dir),
                "metricas": metricas,
                "sucesso": returncode == 0
            }

            self.resultados.append(resultado)

            print(f"\n[OK] Tarefa {task_id} concluida!")
            print(f"   Tempo: {tempo_execucao:.1f}s")
            print(f"   Iteracoes: {metricas.get('total_iteracoes', 'N/A')}")
            print(f"   Log salvo em: {log_file}")

            return resultado

        except Exception as e:
            print(f"\n[ERRO] Falha ao executar tarefa {task_id}: {e}")
            import traceback
            traceback.print_exc()

            resultado = {
                "tarefa_id": task_id,
                "nome": task_nome,
                "erro": str(e),
                "sucesso": False
            }
            self.resultados.append(resultado)
            return resultado

    def _backup_telemetria_anterior(self, backup_dir: Path):
        """Faz backup dos arquivos de telemetria existentes"""
        if Path(TELEMETRIA_API).exists():
            shutil.copy2(TELEMETRIA_API, backup_dir / "telemetria_api_antes.jsonl")
        if Path(TELEMETRIA_FERRAMENTAS).exists():
            shutil.copy2(TELEMETRIA_FERRAMENTAS, backup_dir / "telemetria_ferramentas_antes.jsonl")

    def _limpar_telemetria(self):
        """Limpa arquivos de telemetria para nova execução"""
        # Não vamos deletar, vamos mover para backup
        # Assim conseguimos comparar o antes/depois
        pass

    def _coletar_metricas_telemetria(self, backup_dir: Path) -> Dict[str, Any]:
        """Coleta métricas dos arquivos de telemetria"""

        metricas = {
            "total_iteracoes": 0,
            "tokens_input": 0,
            "tokens_output": 0,
            "cache_creation": 0,
            "cache_read": 0,
            "cache_hit_rate": 0.0,
            "ferramentas_usadas": [],
            "erros_detectados": 0,
            "recuperacoes": 0
        }

        try:
            # Ler telemetria de API
            if Path(TELEMETRIA_API).exists():
                # Backup após execução
                shutil.copy2(TELEMETRIA_API, backup_dir / "telemetria_api_depois.jsonl")

                with open(TELEMETRIA_API, 'r', encoding='utf-8') as f:
                    eventos_api = [json.loads(line) for line in f if line.strip()]

                metricas["total_iteracoes"] = len(eventos_api)

                for evento in eventos_api:
                    usage = evento.get("usage", {})
                    metricas["tokens_input"] += usage.get("input_tokens", 0)
                    metricas["tokens_output"] += usage.get("output_tokens", 0)
                    metricas["cache_creation"] += usage.get("cache_creation_input_tokens", 0)
                    metricas["cache_read"] += usage.get("cache_read_input_tokens", 0)

                # Calcular cache hit rate
                total_input = metricas["tokens_input"]
                if total_input > 0:
                    metricas["cache_hit_rate"] = round(
                        (metricas["cache_read"] / total_input) * 100, 2
                    )

            # Ler telemetria de ferramentas
            if Path(TELEMETRIA_FERRAMENTAS).exists():
                shutil.copy2(TELEMETRIA_FERRAMENTAS, backup_dir / "telemetria_ferramentas_depois.jsonl")

                with open(TELEMETRIA_FERRAMENTAS, 'r', encoding='utf-8') as f:
                    eventos_ferramentas = [json.loads(line) for line in f if line.strip()]

                ferramentas = set()
                for evento in eventos_ferramentas:
                    nome_ferramenta = evento.get("nome_ferramenta")
                    if nome_ferramenta:
                        ferramentas.add(nome_ferramenta)

                    # Detectar erros
                    resultado = evento.get("resultado", "")
                    if "ERRO" in resultado or "Error" in resultado or "Exception" in resultado:
                        metricas["erros_detectados"] += 1

                metricas["ferramentas_usadas"] = sorted(list(ferramentas))

        except Exception as e:
            print(f"[!] Erro ao coletar metricas de telemetria: {e}")

        return metricas

    def gerar_relatorio_final(self):
        """Gera relatório consolidado de todas as tarefas"""

        relatorio_file = self.logs_dir / "RELATORIO_EXECUCAO.json"

        with open(relatorio_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp_execucao": datetime.now().isoformat(),
                "total_tarefas": len(self.resultados),
                "tarefas_sucesso": sum(1 for r in self.resultados if r.get("sucesso")),
                "tarefas_falha": sum(1 for r in self.resultados if not r.get("sucesso")),
                "resultados": self.resultados
            }, f, indent=2, ensure_ascii=False)

        print(f"\n{'='*80}")
        print(f"RELATORIO FINAL")
        print(f"{'='*80}")
        print(f"Total de tarefas: {len(self.resultados)}")
        print(f"Sucesso: {sum(1 for r in self.resultados if r.get('sucesso'))}")
        print(f"Falha: {sum(1 for r in self.resultados if not r.get('sucesso'))}")
        print(f"\nRelatorio detalhado salvo em: {relatorio_file}")
        print(f"{'='*80}\n")


def main():
    """Função principal"""

    # Forçar UTF-8 no stdout
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

    print("""
================================================================================

         EXECUTOR AUTOMATIZADO DE TAREFAS DE TESTE - LUNA V3

================================================================================

Este script ira executar automaticamente 12 tarefas de teste na Luna V3
e coletar metricas detalhadas de cada execucao.

Tarefas a executar:
  - 3 Simples (2-5 iteracoes esperadas)
  - 3 Medias (5-15 iteracoes esperadas)
  - 3 Complexas (15-40 iteracoes esperadas)
  - 3 Feature-especificas (testes de recovery, auto-evolucao, etc.)

Tempo estimado total: 1.5 - 2.5 horas

INICIANDO AUTOMATICAMENTE EM 3 SEGUNDOS...
""")

    time.sleep(3)

    executor = ExecutorTarefas()

    print("\n>> Iniciando execucao das tarefas...\n")

    for i, tarefa in enumerate(TAREFAS, 1):
        print(f"\n\n>> Progresso: {i}/{len(TAREFAS)} tarefas")
        executor.executar_tarefa(tarefa)

        # Pequena pausa entre tarefas
        if i < len(TAREFAS):
            print("\n   Pausa de 5 segundos antes da proxima tarefa...")
            time.sleep(5)

    # Gerar relatório final
    executor.gerar_relatorio_final()

    print("\n[OK] TODAS AS TAREFAS CONCLUIDAS!\n")
    print("Todos os logs e telemetria estao disponiveis em: LOGS_EXECUCAO/\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Execucao interrompida pelo usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[ERRO CRITICO] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
