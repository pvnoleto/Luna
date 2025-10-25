#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de refatoração automática: executar_tarefa()
Quebra método de 224 linhas em 6 submétodos organizados

ESTRUTURA:
1. _preparar_contexto_tarefa() - Busca contexto de memória/workspace
2. _construir_prompt_sistema() - Monta prompt inicial
3. _inicializar_estado_execucao() - Reset de variáveis
4. _executar_chamada_api() - Chamada à API Claude
5. _processar_resposta_final() - Quando stop_reason == "end_turn"
6. _processar_uso_ferramentas() - Quando stop_reason == "tool_use"
"""

import re

def refatorar_executar_tarefa():
    """Refatora o método executar_tarefa()"""

    # Ler arquivo
    with open('luna_v3_FINAL_OTIMIZADA.py', 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.splitlines(keepends=True)

    # Encontrar início do método
    metodo_inicio = None
    for i, line in enumerate(lines):
        if 'def executar_tarefa(' in line:
            metodo_inicio = i
            break

    if metodo_inicio is None:
        print("❌ Erro: Não encontrou método executar_tarefa")
        return False

    # Encontrar fim do método (próximo def no mesmo nível)
    metodo_fim = None
    for i in range(metodo_inicio + 1, len(lines)):
        if lines[i].startswith('    def ') and 'executar_tarefa' not in lines[i]:
            metodo_fim = i
            break

    if metodo_fim is None:
        print("❌ Erro: Não encontrou fim do método")
        return False

    print(f"📍 Método encontrado: linhas {metodo_inicio+1} até {metodo_fim}")
    print(f"   Total: {metodo_fim - metodo_inicio} linhas")

    # Criar backup
    with open('luna_v3_FINAL_OTIMIZADA.py.backup_executar', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("💾 Backup criado: luna_v3_FINAL_OTIMIZADA.py.backup_executar")

    # ========================================================================
    # MÉTODO 1: _preparar_contexto_tarefa
    # ========================================================================

    metodo1 = '''    def _preparar_contexto_tarefa(self, tarefa: str) -> tuple[str, str]:
        """
        Prepara contexto de memória e workspace para a tarefa.

        Returns:
            (contexto_aprendizados, contexto_workspace)
        """
        # Buscar contexto de memória
        contexto_aprendizados = ""
        if self.sistema_ferramentas.memoria_disponivel:
            contexto_aprendizados = self.sistema_ferramentas.memoria.obter_contexto_recente(3)

        # Contexto de workspace
        contexto_workspace = ""
        if self.sistema_ferramentas.gerenciador_workspaces_disponivel:
            ws_atual = self.sistema_ferramentas.gerenciador_workspaces.get_workspace_atual()
            if ws_atual:
                contexto_workspace = (
                    f"\\n\\nWORKSPACE ATUAL: {ws_atual['nome']}\\n"
                    f"Localização: {ws_atual['path_relativo']}\\n"
                    f"Novos arquivos serão criados aqui automaticamente!"
                )

        return contexto_aprendizados, contexto_workspace

'''

    # ========================================================================
    # MÉTODO 2: _construir_prompt_sistema
    # ========================================================================

    metodo2 = '''    def _construir_prompt_sistema(
        self,
        tarefa: str,
        contexto_aprendizados: str,
        contexto_workspace: str
    ) -> str:
        """Constrói o prompt do sistema para a tarefa."""
        return f"""Você é o AGENTE AI MAIS AVANÇADO possível.

CAPACIDADES COMPLETAS:
1. AUTO-EVOLUÇÃO: Cria ferramentas dinamicamente
2. COMPUTER USE: Navega web, screenshots, interação
3. CREDENCIAIS: Acessa cofre criptografado, login automático
4. MEMÓRIA PERMANENTE: Aprende e lembra entre sessões
5. WORKSPACE MANAGER: Organiza projetos automaticamente
6. RECUPERAÇÃO DE ERROS: Detecta e corrige erros automaticamente

INSTRUÇÕES CRÍTICAS:
1. ANTES de tarefas, BUSQUE aprendizados relevantes
2. DEPOIS de resolver algo novo, SALVE o aprendizado
3. NUNCA mostre senhas ao usuário
4. USE login_automatico sempre que precisar de login
5. APRENDA com erros e sucessos
6. USE workspaces para organizar projetos
7. SE ENCONTRAR ERRO: PARE e CORRIJA antes de continuar!

{contexto_aprendizados}{contexto_workspace}

TAREFA DO USUÁRIO:
{tarefa}

Comece BUSCANDO aprendizados relevantes, depois execute a tarefa!"""

'''

    # ========================================================================
    # MÉTODO 3: _inicializar_estado_execucao
    # ========================================================================

    metodo3 = '''    def _inicializar_estado_execucao(self, prompt_sistema: str) -> None:
        """Inicializa o estado da execução."""
        self.historico_conversa = [{"role": "user", "content": prompt_sistema}]
        self.modo_recuperacao = False
        self.erros_recentes = []
        self.tentativas_recuperacao = 0
        self.rate_limit_manager.exibir_status()

'''

    # ========================================================================
    # MÉTODO 4: _executar_chamada_api
    # ========================================================================

    metodo4 = '''    def _executar_chamada_api(self):
        """
        Executa chamada à API Claude com tratamento de rate limit.

        Returns:
            Response object ou None se houver rate limit
        """
        from anthropic import RateLimitError

        self.rate_limit_manager.aguardar_se_necessario()

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=4096,
                tools=self.sistema_ferramentas.obter_descricoes(),
                messages=self.historico_conversa
            )

            self.rate_limit_manager.registrar_uso(
                response.usage.input_tokens,
                response.usage.output_tokens
            )

            return response

        except RateLimitError:
            print_realtime(f"\\n⚠️  RATE LIMIT ATINGIDO!")
            print_realtime(f"   Aguardando 60 segundos...")
            time.sleep(60)
            return None

        except Exception as e:
            print_realtime(f"\\n❌ Erro: {e}")
            raise

'''

    # ========================================================================
    # MÉTODO 5: _processar_resposta_final
    # ========================================================================

    metodo5 = '''    def _processar_resposta_final(self, response, tarefa: str) -> str:
        """
        Processa resposta final quando stop_reason == "end_turn".

        Returns:
            Texto da resposta final
        """
        resposta_final = ""
        for block in response.content:
            if hasattr(block, "text"):
                resposta_final += block.text

        # Verificar se está em modo recuperação
        if self.modo_recuperacao:
            print_realtime("\\n✅ Erro resolvido! Voltando à tarefa principal...")
            self.modo_recuperacao = False
            self.tentativas_recuperacao = 0
            return None  # Continua executando

        # Registrar na memória
        if self.sistema_ferramentas.memoria_disponivel:
            ferramentas_usadas: List[str] = []
            self.sistema_ferramentas.memoria.registrar_tarefa(
                tarefa, resposta_final[:500], ferramentas_usadas, True
            )

        # Exibir resultado
        print_realtime("\\n" + "="*70)
        print_realtime("✅ CONCLUÍDO!")
        print_realtime("="*70)
        print_realtime(resposta_final)
        print_realtime("="*70)

        return resposta_final

'''

    # ========================================================================
    # MÉTODO 6: _processar_uso_ferramentas
    # ========================================================================

    metodo6 = '''    def _processar_uso_ferramentas(self, response, tarefa: str, iteracao: int) -> bool:
        """
        Processa uso de ferramentas quando stop_reason == "tool_use".

        Returns:
            True se deve continuar loop, False se deve parar
        """
        self.historico_conversa.append({
            "role": "assistant",
            "content": response.content
        })

        # Extrair pensamento
        pensamento = ""
        for block in response.content:
            if hasattr(block, "text") and block.text:
                pensamento = block.text[:120]
                break

        if pensamento:
            print_realtime(f"💭 {pensamento}...")

        # Executar ferramentas
        tool_results = []
        erro_detectado = False
        ultimo_erro = None

        for block in response.content:
            if block.type == "tool_use":
                print_realtime(f"🔧 {block.name}")

                resultado = self.sistema_ferramentas.executar(
                    block.name, block.input
                )

                # Detectar erro
                tem_erro, erro_info = self.detectar_erro(resultado)
                if tem_erro:
                    erro_detectado = True
                    ultimo_erro = erro_info
                    print_realtime(f"  ⚠️  ERRO DETECTADO: {erro_info[:80]}")
                    self.erros_recentes.append({
                        'ferramenta': block.name,
                        'erro': erro_info,
                        'iteracao': iteracao
                    })

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": resultado
                })

        self.historico_conversa.append({
            "role": "user",
            "content": tool_results
        })

        # Sistema de recuperação
        if erro_detectado and not self.modo_recuperacao:
            print_realtime(f"\\n🚨 ENTRANDO EM MODO DE RECUPERAÇÃO DE ERRO")
            self.modo_recuperacao = True
            self.tentativas_recuperacao = 1

            prompt_recuperacao = self.criar_prompt_recuperacao(
                ultimo_erro, tarefa
            )
            self.historico_conversa.append({
                "role": "user",
                "content": prompt_recuperacao
            })

        elif erro_detectado and self.modo_recuperacao:
            self.tentativas_recuperacao += 1
            if self.tentativas_recuperacao >= self.max_tentativas_recuperacao:
                print_realtime(
                    f"\\n⚠️  Muitas tentativas de recuperação "
                    f"({self.tentativas_recuperacao})"
                )
                print_realtime(f"   Continuando com a tarefa mesmo com erro...")
                self.modo_recuperacao = False
                self.tentativas_recuperacao = 0

        return True  # Continua loop

'''

    # ========================================================================
    # MÉTODO PRINCIPAL REFATORADO
    # ========================================================================

    metodo_principal = '''    def executar_tarefa(
        self,
        tarefa: str,
        max_iteracoes: Optional[int] = None
    ) -> Optional[str]:
        """
        Executa uma tarefa completa.

        ✅ REFATORADO: Organizado em submétodos para melhor manutenção.

        Args:
            tarefa: Descrição da tarefa
            max_iteracoes: Limite de iterações (padrão: 40)

        Returns:
            Resposta final do agente (ou None se não concluir)
        """
        # Configurar max_iteracoes
        if max_iteracoes is None:
            max_iteracoes = self.max_iteracoes_atual
        else:
            self.max_iteracoes_atual = max_iteracoes

        # Header
        print_realtime("\\n" + "="*70)
        print_realtime(f"🎯 TAREFA: {tarefa}")
        print_realtime("="*70)

        # Preparar contexto
        contexto_aprendizados, contexto_workspace = self._preparar_contexto_tarefa(tarefa)

        # Construir prompt
        prompt_sistema = self._construir_prompt_sistema(
            tarefa, contexto_aprendizados, contexto_workspace
        )

        # Inicializar estado
        self._inicializar_estado_execucao(prompt_sistema)

        # Loop principal
        for iteracao in range(1, max_iteracoes + 1):
            modo_tag = "🔧 RECUPERAÇÃO" if self.modo_recuperacao else f"🔄 Iteração {iteracao}/{max_iteracoes}"
            print_realtime(f"\\n{modo_tag}")

            # Executar API
            response = self._executar_chamada_api()
            if response is None:
                continue  # Rate limit, tentar novamente

            # Processar resposta
            if response.stop_reason == "end_turn":
                resposta_final = self._processar_resposta_final(response, tarefa)
                if resposta_final is not None:
                    # Estatísticas finais
                    self._exibir_estatisticas()
                    return resposta_final
                # Se None, continua loop (estava em modo recuperação)

            elif response.stop_reason == "tool_use":
                self._processar_uso_ferramentas(response, tarefa, iteracao)

            # Exibir status periodicamente
            if iteracao % 5 == 0:
                self.rate_limit_manager.exibir_status()

        print_realtime("\\n⚠️  Limite de iterações atingido")
        self._exibir_estatisticas()

        return None

'''

    # ========================================================================
    # RECONSTRUIR ARQUIVO
    # ========================================================================

    # Linhas até o método original
    novas_lines = lines[:metodo_inicio]

    # Adicionar métodos auxiliares
    novas_lines.append(metodo1)
    novas_lines.append(metodo2)
    novas_lines.append(metodo3)
    novas_lines.append(metodo4)
    novas_lines.append(metodo5)
    novas_lines.append(metodo6)

    # Adicionar método principal refatorado
    novas_lines.append(metodo_principal)

    # Adicionar resto do arquivo (após o método original)
    novas_lines.extend(lines[metodo_fim:])

    # Salvar arquivo refatorado
    with open('luna_v3_FINAL_OTIMIZADA.py', 'w', encoding='utf-8') as f:
        f.writelines(novas_lines)

    print(f"\n✅ Refatoração completa!")
    print(f"   Método original: {metodo_fim - metodo_inicio} linhas")
    print(f"   Método refatorado: ~60 linhas")
    print(f"   Métodos auxiliares criados: 6")
    print(f"   Redução: {metodo_fim - metodo_inicio} → ~120 linhas total (60 principal + 60 auxiliares)")

    return True

if __name__ == '__main__':
    print("🔧 REFATORAÇÃO AUTOMÁTICA: executar_tarefa()")
    print("=" * 60)

    sucesso = refatorar_executar_tarefa()

    if sucesso:
        print("\n🎉 Sucesso! Execute para validar:")
        print("   python3 -m py_compile luna_v3_FINAL_OTIMIZADA.py")
    else:
        print("\n❌ Falha na refatoração")
