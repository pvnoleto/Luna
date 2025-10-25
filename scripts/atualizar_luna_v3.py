#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para atualizar luna_v3_TIER2.py com feedback visual e recuperação de erros"""

import re

# Ler o arquivo original
with open("C:\\Users\\Pedro Victor\\OneDrive\\Área de Trabalho\\Documentos\\Projetos Automações e Digitais\\Luna\\luna_v3_TIER2.py", "r", encoding="utf-8") as f:
    conteudo = f.read()

# =============================================================================
# 1. ADICIONAR FUNÇÕES DE FEEDBACK VISUAL após a configuração do sys
# =============================================================================

funcoes_feedback = '''

# ============================================================================
# FUNÇÕES DE FEEDBACK VISUAL EM TEMPO REAL
# ============================================================================

def print_realtime(msg):
    """Print com flush imediato para feedback em tempo real"""
    print(msg, flush=True)


def input_seguro(prompt: str = "\\n💬 O que você quer? (ou 'sair'): ") -> str:
    """
    Input melhorado que lida corretamente com paste (Ctrl+V)
    Mostra o que foi colado e pede confirmação se for texto grande
    
    DICA: Para textos MUITO grandes, digite 'multi' para modo multiline
    """
    print(prompt, end='', flush=True)
    
    # Coletar input
    comando = input().strip()
    
    # Modo multiline especial
    if comando.lower() == 'multi':
        print("\\n📝 MODO MULTILINE ATIVADO", flush=True)
        print("   Cole seu texto (pode ser múltiplas linhas)")
        print("   Digite 'FIM' numa linha sozinha quando terminar\\n", flush=True)
        
        linhas = []
        while True:
            try:
                linha = input()
                if linha.strip() == 'FIM':
                    break
                linhas.append(linha)
            except EOFError:
                break
        
        comando = '\\n'.join(linhas).strip()
        
        if not comando:
            print_realtime("⚠️  Nenhum texto fornecido")
            return input_seguro()
        
        print_realtime(f"\\n✅ Texto recebido ({len(comando)} caracteres)")
    
    # Se for vazio, retornar
    if not comando:
        return comando
    
    # Se for comando de saída, retornar direto
    if comando.lower() in ['sair', 'exit', 'quit']:
        return comando
    
    # Se for texto curto, retornar direto
    if len(comando) <= 150:
        return comando
    
    # Para textos longos (provavelmente colados), mostrar preview e confirmar
    print_realtime(f"\\n📋 Comando recebido ({len(comando)} caracteres)")
    print_realtime("─" * 70)
    
    # Mostrar preview inteligente
    if len(comando) > 400:
        # Texto muito longo: primeiros 200 chars + últimos 100
        preview = comando[:200] + "\\n\\n[... " + str(len(comando) - 300) + " caracteres ...]\\n\\n" + comando[-100:]
        print_realtime(preview)
    else:
        # Texto médio: mostrar tudo
        print_realtime(comando)
    
    print_realtime("─" * 70)
    
    # Pedir confirmação
    print_realtime("\\n✓ Este comando está correto?")
    print_realtime("   [Enter] = Sim, executar")
    print_realtime("   [e]     = Não, editar")
    print_realtime("   [c]     = Cancelar")
    
    confirma = input("\\nEscolha: ").strip().lower()
    
    if confirma == 'e':
        print_realtime("\\n✏️  Digite o comando correto (ou 'multi' para modo multiline):")
        return input_seguro("")
    elif confirma == 'c':
        print_realtime("❌ Comando cancelado")
        return ""
    
    # Enter ou qualquer outra coisa = confirmar
    return comando

'''

# Encontrar onde inserir (após sys.stderr.reconfigure)
padrao_insercao = r"(sys\.stderr\.reconfigure\(line_buffering=True\).*?\n\n)"
conteudo = re.sub(padrao_insercao, r"\1" + funcoes_feedback, conteudo, count=1)

# =============================================================================
# 2. ADICIONAR MÉTODOS DE RECUPERAÇÃO DE ERROS NO AGENTE
# =============================================================================

# Adicionar métodos detect_erro e criar_prompt_recuperacao ANTES do método executar_tarefa
metodos_recuperacao = '''
    
    def detectar_erro(self, resultado: str) -> tuple:
        """Detecta se há erro no resultado de uma ferramenta"""
        # Detectar padrões de erro
        padrao_erro = resultado.startswith("ERRO:") or "ERRO:" in resultado[:100]
        
        if padrao_erro:
            # Extrair informação do erro
            linhas = resultado.split("\\n")
            erro_principal = linhas[0] if linhas else resultado[:200]
            
            return True, erro_principal
        
        return False, None
    
    def criar_prompt_recuperacao(self, erro: str, tarefa_original: str):
        """Cria prompt focado em recuperar do erro"""
        return f"""🔧 MODO DE RECUPERAÇÃO DE ERRO ATIVADO

ERRO DETECTADO:
{erro}

INSTRUÇÕES DE RECUPERAÇÃO:
1. ANALISE o erro cuidadosamente
2. IDENTIFIQUE a causa raiz (arquivo não existe? permissão negada? sintaxe? dependência faltando?)
3. CORRIJA o problema (criar arquivo, instalar pacote, ajustar código, etc.)
4. VALIDE que a correção funcionou
5. SÓ DEPOIS volte à tarefa original

TAREFA ORIGINAL (retomar após correção):
{tarefa_original}

FOCO TOTAL: Resolver o erro acima antes de continuar!"""

'''

# Procurar a classe AgenteComTier2Completo e adicionar os métodos antes de executar_tarefa
padrao_classe = r"(class AgenteComTier2Completo:.*?def _executar_requisicao_simples)"
conteudo = re.sub(padrao_classe, r"\1" + metodos_recuperacao + "\n    def _executar_requisicao_simples", conteudo, count=1, flags=re.DOTALL)

# =============================================================================
# 3. ADICIONAR LÓGICA DE RECUPERAÇÃO NO LOOP DE ITERAÇÕES
# =============================================================================

# Adicionar lógica após tool_results
logica_recuperacao = '''
                
                # ✅ SISTEMA DE RECUPERAÇÃO DE ERROS
                # Detectar erros nos resultados das ferramentas
                erro_detectado = False
                ultimo_erro = None
                
                for i, resultado in enumerate(tool_results):
                    resultado_texto = resultado.get('content', '')
                    tem_erro, erro_info = self.detectar_erro(resultado_texto)
                    
                    if tem_erro:
                        erro_detectado = True
                        ultimo_erro = erro_info
                        print_realtime(f"  ⚠️  ERRO DETECTADO na ferramenta {tool_uses[i].name}: {erro_info[:80]}")
                        self.erros_recentes.append({
                            'ferramenta': tool_uses[i].name,
                            'erro': erro_info,
                            'iteracao': iteracao
                        })
                
                # Entrar em modo recuperação se erro detectado
                if erro_detectado and not self.modo_recuperacao:
                    print_realtime(f"\\n🚨 ENTRANDO EM MODO DE RECUPERAÇÃO DE ERRO")
                    self.modo_recuperacao = True
                    self.tentativas_recuperacao = 1
                    
                    # Adicionar prompt de recuperação
                    prompt_recuperacao = self.criar_prompt_recuperacao(ultimo_erro, tarefa)
                    self.historico_conversa.append({
                        "role": "user",
                        "content": prompt_recuperacao
                    })
                    
                    continue  # Ir para próxima iteração para tentar recuperar
                
                elif erro_detectado and self.modo_recuperacao:
                    self.tentativas_recuperacao += 1
                    if self.tentativas_recuperacao >= 3:  # max 3 tentativas
                        print_realtime(f"\\n⚠️  Muitas tentativas de recuperação ({self.tentativas_recuperacao})")
                        print_realtime(f"   Continuando com a tarefa mesmo com erro...")
                        self.modo_recuperacao = False
                        self.tentativas_recuperacao = 0
'''

# Inserir após tool_results append
padrao_tool_results = r"(self\.historico_conversa\.append\({\s*\"role\": \"user\",\s*\"content\": tool_results\s*}\))"
conteudo = re.sub(padrao_tool_results, r"\1" + logica_recuperacao, conteudo, count=1, flags=re.DOTALL)

# =============================================================================
# 4. ADICIONAR VARIÁVEIS DE ESTADO PARA RECUPERAÇÃO NO __init__
# =============================================================================

# Adicionar após as existentes
variaveis_recuperacao = '''
        self.tentativas_recuperacao = 0
        self.max_tentativas_recuperacao = 3
'''

# Inserir após self.erros_recentes = []
padrao_erros = r"(self\.erros_recentes = \[\])"
conteudo = re.sub(padrao_erros, r"\1" + variaveis_recuperacao, conteudo, count=1)

# =============================================================================
# 5. SUBSTITUIR input() POR input_seguro() NO MAIN
# =============================================================================

conteudo = conteudo.replace(
    'comando = input("\\n💬 O que você quer? (ou \'sair\'): ").strip()',
    'comando = input_seguro()'
)

# =============================================================================
# 6. ADICIONAR VERIFICAÇÃO DE RECUPERAÇÃO NO END_TURN
# =============================================================================

codigo_verificacao_end_turn = '''
                
                # Verificar se estava em modo recuperação
                if self.modo_recuperacao:
                    print_realtime("\\n✅ Erro resolvido! Voltando à tarefa principal...")
                    self.modo_recuperacao = False
                    self.tentativas_recuperacao = 0
                    continue  # Continuar com a tarefa
'''

# Inserir após o break do end_turn
padrao_end_turn = r"(print\(f\"\\n\{'='\*70\}\"\\s*print\(f\"✅ TAREFA CONCLUÍDA EM \{iteracao\} ITERAÇÕES!\"\))"
conteudo = re.sub(padrao_end_turn, codigo_verificacao_end_turn + r"\1", conteudo, count=1, flags=re.DOTALL)

# =============================================================================
# 7. ADICIONAR RECUPERAÇÃO NO SISTEMA DE PLANEJAMENTO
# =============================================================================

# Adicionar verificação de erro na execução das ondas
codigo_recuperacao_onda = '''
                
                # ✅ VERIFICAR SE RESULTADO TEM ERRO
                tem_erro, erro_info = self.agente.detectar_erro(str(resultado_exec.get('output', '')))
                
                if tem_erro:
                    print_realtime(f"   ⚠️  ERRO DETECTADO: {erro_info[:80]}")
                    
                    # Tentar recuperar
                    print_realtime(f"   🔧 Tentando recuperar...")
                    prompt_recuperacao = self.agente.criar_prompt_recuperacao(erro_info, st.descricao)
                    resultado_recuperacao = self.agente._executar_com_iteracoes(prompt_recuperacao, max_iteracoes=5)
                    
                    if resultado_recuperacao.get('concluido', False):
                        print_realtime(f"   ✅ Recuperação bem-sucedida! Retentando subtarefa...")
                        # Retentar subtarefa
                        resultado_exec = self.agente._executar_com_iteracoes(prompt, max_iteracoes=10)
'''

# Inserir no método _executar_onda_sequencial, após resultado_exec
padrao_resultado_exec = r"(resultado_exec = self\.agente\._executar_com_iteracoes\(prompt, max_iteracoes=10\))"
conteudo = re.sub(padrao_resultado_exec, r"\1" + codigo_recuperacao_onda, conteudo, count=1)

# Fazer o mesmo para o ProcessadorParalelo
conteudo = re.sub(
    r"(class ProcessadorParalelo:.*?resultado_exec = self\.agente\._executar_com_iteracoes\(prompt, max_iteracoes=10\))",
    r"\1" + codigo_recuperacao_onda,
    conteudo,
    count=1,
    flags=re.DOTALL
)

# =============================================================================
# SALVAR ARQUIVO ATUALIZADO
# =============================================================================

with open("C:\\Users\\Pedro Victor\\OneDrive\\Área de Trabalho\\Documentos\\Projetos Automações e Digitais\\Luna\\luna_v3_TIER2.py", "w", encoding="utf-8") as f:
    f.write(conteudo)

print("✅ Arquivo atualizado com sucesso!")
print("   ✨ Funções de feedback visual adicionadas")
print("   ✨ Sistema de recuperação de erros implementado")
print("   ✨ Recuperação integrada ao sistema de planejamento")
print("\\n📋 Alterações realizadas:")
print("   1. print_realtime() e input_seguro() adicionadas")
print("   2. detectar_erro() e criar_prompt_recuperacao() no agente")
print("   3. Lógica de recuperação no loop de iterações")
print("   4. Recuperação no sistema de planejamento avançado")
print("   5. Recuperação no processador paralelo")
