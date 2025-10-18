#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 CLAUDE AGENTE COMPLETO - VERSÃO FINAL
==========================================

TODAS AS CAPACIDADES INTEGRADAS:
✅ Auto-evolução (cria ferramentas)
✅ Computer Use (navega web + screenshots)
✅ Credenciais seguras (AES-256)
✅ Memória permanente (aprende sempre)
✅ Login automático
✅ Autonomia total

Este é o agente mais avançado possível!
"""

import anthropic
from anthropic import BadRequestError
import os
import subprocess
import json
from dotenv import load_dotenv
from datetime import datetime
import getpass

# Importar sistema de auto-evolução
try:
    from sistema_auto_evolucao import FilaDeMelhorias, SistemaAutoEvolucao
    AUTO_EVOLUCAO_DISPONIVEL = True
except:
    AUTO_EVOLUCAO_DISPONIVEL = False
    print("⚠️  sistema_auto_evolucao.py não encontrado - auto-evolução desabilitada")

# Importar gerenciador de temporários
try:
    from gerenciador_temp import GerenciadorTemporarios
    GERENCIADOR_TEMP_DISPONIVEL = True
except:
    GERENCIADOR_TEMP_DISPONIVEL = False
    print("⚠️  gerenciador_temp.py não encontrado - gerenciamento de temporários desabilitado")

# Importar gerenciador de workspaces
try:
    from gerenciador_workspaces import GerenciadorWorkspaces
    GERENCIADOR_WORKSPACES_DISPONIVEL = True
except:
    GERENCIADOR_WORKSPACES_DISPONIVEL = False
    print("⚠️  gerenciador_workspaces.py não encontrado - gerenciamento de workspaces desabilitado")

# Importar gerenciador de workspaces
try:
    from gerenciador_workspaces import GerenciadorWorkspaces
    GERENCIADOR_WORKSPACES_DISPONIVEL = True
except:
    GERENCIADOR_WORKSPACES_DISPONIVEL = False
    print("⚠️  gerenciador_workspaces.py não encontrado - gerenciamento de workspaces desabilitado")

# Importar sistemas
try:
    from cofre_credenciais import Cofre
    COFRE_DISPONIVEL = True
except:
    COFRE_DISPONIVEL = False
    print("⚠️  cofre_credenciais.py não encontrado - funcionalidades de credenciais desabilitadas")

try:
    from memoria_permanente import MemoriaPermanente
    MEMORIA_DISPONIVEL = True
except:
    MEMORIA_DISPONIVEL = False
    print("⚠️  memoria_permanente.py não encontrado - memória permanente desabilitada")

# Carregar configuração
load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))


# ============================================================================
# SISTEMA DE FERRAMENTAS COMPLETO
# ============================================================================

class SistemaFerramentasCompleto:
    """Sistema de ferramentas com TODAS as capacidades"""
    
    def __init__(self, master_password: str = None, usar_memoria: bool = True):
        self.ferramentas_codigo = {}
        self.ferramentas_descricao = []
        self.historico = []
        self.browser = None
        self.page = None
        
        # Auto-evolução
        self.auto_evolucao_disponivel = AUTO_EVOLUCAO_DISPONIVEL
        self.fila_melhorias = FilaDeMelhorias() if AUTO_EVOLUCAO_DISPONIVEL else None
        self.sistema_evolucao = SistemaAutoEvolucao() if AUTO_EVOLUCAO_DISPONIVEL else None
        
        # Gerenciador de temporários
        self.gerenciador_temp_disponivel = GERENCIADOR_TEMP_DISPONIVEL
        self.gerenciador_temp = GerenciadorTemporarios() if GERENCIADOR_TEMP_DISPONIVEL else None
        
        # Gerenciador de workspaces
        self.gerenciador_workspaces_disponivel = GERENCIADOR_WORKSPACES_DISPONIVEL
        self.gerenciador_workspaces = GerenciadorWorkspaces() if GERENCIADOR_WORKSPACES_DISPONIVEL else None
        
        # Gerenciador de workspaces
        self.gerenciador_workspaces_disponivel = GERENCIADOR_WORKSPACES_DISPONIVEL
        self.gerenciador_workspaces = GerenciadorWorkspaces() if GERENCIADOR_WORKSPACES_DISPONIVEL else None
        
        # Cofre de credenciais
        self.cofre = None
        self.cofre_disponivel = False
        if COFRE_DISPONIVEL and master_password:
            try:
                self.cofre = Cofre()
                self.cofre.inicializar(master_password)
                self.cofre_disponivel = True
            except Exception as e:
                print(f"⚠️  Cofre não disponível: {e}")
        
        # Memória permanente
        self.memoria = None
        self.memoria_disponivel = False
        if MEMORIA_DISPONIVEL and usar_memoria:
            try:
                self.memoria = MemoriaPermanente()
                self.memoria_disponivel = True
            except Exception as e:
                print(f"⚠️  Memória não disponível: {e}")
        
        # Carregar ferramentas
        self._carregar_ferramentas_base()
    
    def _carregar_ferramentas_base(self):
        """Todas as ferramentas base"""
        
        # BASH
        self.adicionar_ferramenta(
            "bash_avancado",
            '''def bash_avancado(comando: str, timeout: int = 60) -> str:
    import subprocess, os
    print(f"    💻 Bash: {comando[:100]}...")
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, 
                                 text=True, timeout=timeout, cwd=os.getcwd())
        saida = f"STDOUT:\\n{resultado.stdout}\\nSTDERR:\\n{resultado.stderr}\\nCODE: {resultado.returncode}"
        print(f"    ✅ Código {resultado.returncode}")
        return saida[:3000]
    except Exception as e:
        return f"Erro: {e}"''',
            "Executa comandos bash/terminal",
            {"comando": {"type": "string"}, "timeout": {"type": "integer"}}
        )
        
        # ARQUIVOS
        self.adicionar_ferramenta(
            "criar_arquivo",
            '''def criar_arquivo(caminho: str, conteudo: str) -> str:
    from pathlib import Path
    print(f"    📝 Criando: {caminho}")
    try:
        Path(caminho).parent.mkdir(parents=True, exist_ok=True)
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        print(f"    ✅ Criado")
        return f"Arquivo '{caminho}' criado"
    except Exception as e:
        return f"Erro: {e}"''',
            "Cria arquivo",
            {"caminho": {"type": "string"}, "conteudo": {"type": "string"}}
        )
        
        self.adicionar_ferramenta(
            "ler_arquivo",
            '''def ler_arquivo(caminho: str) -> str:
    print(f"    📖 Lendo: {caminho}")
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        print(f"    ✅ Lido")
        return conteudo[:5000]
    except Exception as e:
        return f"Erro: {e}"''',
            "Lê arquivo",
            {"caminho": {"type": "string"}}
        )
        
        # GERENCIAMENTO DE TEMPORÁRIOS
        if self.gerenciador_temp_disponivel:
            self.adicionar_ferramenta(
                "marcar_temporario",
                '''def marcar_temporario(caminho: str, forcar: bool = False) -> str:
    print(f"    🗑️ Marcando temporário: {caminho}")
    try:
        global _gerenciador_temp
        sucesso = _gerenciador_temp.marcar_temporario(caminho, forcar)
        if sucesso:
            print(f"    ✅ Marcado (delete em 30 dias)")
            return f"Arquivo '{caminho}' marcado como temporário. Será deletado em 30 dias se não for usado."
        else:
            return f"Arquivo '{caminho}' não pode ser marcado (protegido ou não é temporário)"
    except Exception as e:
        return f"Erro: {e}"''',
                "Marca arquivo como temporário para auto-limpeza em 30 dias. Útil para arquivos de teste, debug, screenshots temporários.",
                {"caminho": {"type": "string"}, "forcar": {"type": "boolean", "description": "Force marcar mesmo se não parecer temporário"}}
            )
            
            self.adicionar_ferramenta(
                "listar_temporarios",
                '''def listar_temporarios() -> str:
    print(f"    📋 Listando temporários...")
    try:
        global _gerenciador_temp
        temporarios = _gerenciador_temp.listar_temporarios()
        
        if not temporarios:
            return "Nenhum arquivo temporário no momento"
        
        resultado = f"Total: {len(temporarios)} arquivo(s) temporário(s)\\n\\n"
        for arq in temporarios[:20]:  # Máximo 20
            resultado += f"• {arq['nome']} ({arq['tamanho_mb']:.2f} MB)\\n"
            resultado += f"  Delete em: {arq['dias_restantes']} dias\\n"
            resultado += f"  Motivo: {arq['motivo']}\\n\\n"
        
        if len(temporarios) > 20:
            resultado += f"... e mais {len(temporarios) - 20} arquivo(s)"
        
        print(f"    ✅ {len(temporarios)} temporário(s)")
        return resultado
    except Exception as e:
        return f"Erro: {e}"''',
                "Lista todos arquivos temporários e quando serão deletados",
                {}
            )
            
            self.adicionar_ferramenta(
                "status_temporarios",
                '''def status_temporarios() -> str:
    print(f"    📊 Status temporários...")
    try:
        global _gerenciador_temp
        stats = _gerenciador_temp.obter_estatisticas()
        
        resultado = "📊 STATUS DO GERENCIADOR DE TEMPORÁRIOS\\n\\n"
        resultado += f"📁 Arquivos temporários: {stats['arquivos_temporarios_atuais']}\\n"
        resultado += f"🛡️ Arquivos protegidos: {stats['arquivos_protegidos']}\\n"
        resultado += f"🗑️ Total deletados: {stats['total_deletados']}\\n"
        resultado += f"✅ Total resgatados: {stats['total_resgatados']}\\n"
        resultado += f"📈 Taxa de resgate: {stats['taxa_resgate_percent']:.1f}%\\n"
        resultado += f"💾 Espaço liberado: {stats['espaco_liberado_mb']:.2f} MB"
        
        print(f"    ✅ Status obtido")
        return resultado
    except Exception as e:
        return f"Erro: {e}"''',
                "Mostra estatísticas do gerenciador de temporários (total, deletados, resgatados, etc)",
                {}
            )
        
        # GERENCIAMENTO DE WORKSPACES
        if self.gerenciador_workspaces_disponivel:
            self.adicionar_ferramenta(
                "criar_workspace",
                '''def criar_workspace(nome: str, descricao: str = "") -> str:
    print(f"    📁 Criando workspace: {nome}")
    try:
        global _gerenciador_workspaces
        path = _gerenciador_workspaces.criar_workspace(nome, descricao)
        return f"Workspace '{nome}' criado em: workspaces/{nome}/"
    except Exception as e:
        return f"Erro: {e}"''',
                "Cria novo workspace (projeto) em Luna/workspaces/nome/. Use para organizar projetos separados.",
                {"nome": {"type": "string", "description": "Nome do workspace (letras, números, - e _)"}, 
                 "descricao": {"type": "string", "description": "Descrição do projeto (opcional)"}}
            )
            
            self.adicionar_ferramenta(
                "listar_workspaces",
                '''def listar_workspaces() -> str:
    print(f"    📋 Listando workspaces...")
    try:
        global _gerenciador_workspaces
        workspaces = _gerenciador_workspaces.listar_workspaces()
        
        if not workspaces:
            return "Nenhum workspace criado ainda. Use criar_workspace('nome') para criar."
        
        resultado = f"Total: {len(workspaces)} workspace(s)\\n\\n"
        for ws in workspaces:
            marcador = "→ " if ws['atual'] else "  "
            resultado += f"{marcador}{ws['nome']}"
            if ws['descricao']:
                resultado += f" - {ws['descricao']}"
            resultado += f"\\n   📁 {ws['path_relativo']}\\n"
            resultado += f"   📄 {ws['arquivos']} arquivo(s) • {ws['tamanho_mb']:.2f} MB\\n\\n"
        
        print(f"    ✅ {len(workspaces)} workspace(s)")
        return resultado
    except Exception as e:
        return f"Erro: {e}"''',
                "Lista todos workspaces criados com suas informações",
                {}
            )
            
            self.adicionar_ferramenta(
                "selecionar_workspace",
                '''def selecionar_workspace(nome: str) -> str:
    print(f"    📍 Selecionando: {nome}")
    try:
        global _gerenciador_workspaces
        path = _gerenciador_workspaces.selecionar_workspace(nome)
        return f"Workspace '{nome}' selecionado! Arquivos serão criados em: {path}"
    except Exception as e:
        return f"Erro: {e}"''',
                "Seleciona workspace como atual. Novos arquivos serão criados nele.",
                {"nome": {"type": "string", "description": "Nome do workspace"}}
            )
            
            self.adicionar_ferramenta(
                "resolver_caminho",
                '''def resolver_caminho(caminho: str) -> str:
    print(f"    🔍 Resolvendo caminho...")
    try:
        global _gerenciador_workspaces
        path_completo = _gerenciador_workspaces.resolver_caminho(caminho)
        return f"Caminho completo: {path_completo}"
    except Exception as e:
        return f"Erro: {e}"''',
                "Resolve caminho relativo ao workspace atual para caminho absoluto",
                {"caminho": {"type": "string", "description": "Caminho relativo (ex: api.py)"}}
            )
        
        # PLAYWRIGHT
        self.adicionar_ferramenta(
            "instalar_playwright",
            '''def instalar_playwright() -> str:
    import subprocess
    print("    📦 Instalando Playwright...")
    try:
        subprocess.run("pip install playwright", shell=True, timeout=120)
        subprocess.run("playwright install chromium", shell=True, timeout=300)
        print("    ✅ Instalado")
        return "Playwright instalado!"
    except Exception as e:
        return f"Erro: {e}"''',
            "Instala Playwright",
            {}
        )
        
        self.adicionar_ferramenta(
            "iniciar_navegador",
            '''def iniciar_navegador(headless: bool = True) -> str:
    print("    🌐 Iniciando navegador...")
    try:
        from playwright.sync_api import sync_playwright
        global _playwright_instance, _browser, _page
        _playwright_instance = sync_playwright().start()
        _browser = _playwright_instance.chromium.launch(headless=headless)
        _page = _browser.new_page()
        print("    ✅ Iniciado")
        return "Navegador iniciado!"
    except Exception as e:
        return f"Erro: {e}"''',
            "Inicia navegador Playwright",
            {"headless": {"type": "boolean"}}
        )
        
        self.adicionar_ferramenta(
            "navegar_url",
            '''def navegar_url(url: str) -> str:
    print(f"    🔗 Navegando: {url}")
    try:
        global _page
        _page.goto(url, timeout=30000)
        titulo = _page.title()
        print(f"    ✅ {titulo}")
        return f"Navegado para '{url}'"
    except Exception as e:
        return f"Erro: {e}"''',
            "Navega para URL",
            {"url": {"type": "string"}}
        )
        
        self.adicionar_ferramenta(
            "tirar_screenshot",
            '''def tirar_screenshot(caminho: str = "screenshot.png") -> str:
    print(f"    📸 Screenshot: {caminho}")
    try:
        global _page
        _page.screenshot(path=caminho)
        print("    ✅ Salvo")
        return f"Screenshot: {caminho}"
    except Exception as e:
        return f"Erro: {e}"''',
            "Tira screenshot",
            {"caminho": {"type": "string"}}
        )
        
        self.adicionar_ferramenta(
            "clicar_elemento",
            '''def clicar_elemento(seletor: str) -> str:
    print(f"    🖱️ Clicando: {seletor}")
    try:
        global _page
        _page.click(seletor, timeout=5000)
        print("    ✅ Clicado")
        return f"Clicado em '{seletor}'"
    except Exception as e:
        return f"Erro: {e}"''',
            "Clica em elemento",
            {"seletor": {"type": "string"}}
        )
        
        self.adicionar_ferramenta(
            "preencher_campo",
            '''def preencher_campo(seletor: str, valor: str) -> str:
    print(f"    ⌨️ Preenchendo: {seletor}")
    try:
        global _page
        _page.fill(seletor, valor, timeout=5000)
        print("    ✅ Preenchido")
        return "Campo preenchido"
    except Exception as e:
        return f"Erro: {e}"''',
            "Preenche campo",
            {"seletor": {"type": "string"}, "valor": {"type": "string"}}
        )
        
        self.adicionar_ferramenta(
            "fechar_navegador",
            '''def fechar_navegador() -> str:
    print("    🔚 Fechando...")
    try:
        global _browser, _page, _playwright_instance
        if _page: _page.close()
        if _browser: _browser.close()
        if _playwright_instance: _playwright_instance.stop()
        _page = _browser = _playwright_instance = None
        print("    ✅ Fechado")
        return "Navegador fechado"
    except Exception as e:
        return f"Erro: {e}"''',
            "Fecha navegador",
            {}
        )
        
        # CREDENCIAIS
        if self.cofre_disponivel:
            self.adicionar_ferramenta(
                "obter_credencial",
                '''def obter_credencial(servico: str) -> str:
    print(f"    🔑 Obtendo: {servico}")
    try:
        global _cofre
        import json
        cred = _cofre.obter_credencial(servico)
        print(f"    ✅ Obtida para: {cred['usuario']}")
        return json.dumps(cred)
    except Exception as e:
        return f"Erro: {e}"''',
                "Obtém credencial do cofre. NUNCA mostre senhas!",
                {"servico": {"type": "string"}}
            )
            
            self.adicionar_ferramenta(
                "login_automatico",
                '''def login_automatico(servico: str, url_login: str = None) -> str:
    print(f"    🔐 Login: {servico}")
    try:
        global _cofre, _page
        cred = _cofre.obter_credencial(servico)
        usuario = cred['usuario']
        senha = cred['senha']
        extras = cred.get('extras', {})
        
        url = url_login or extras.get('url_login')
        if not url:
            return "Erro: URL não fornecida"
        
        sel_user = extras.get('seletor_usuario', 'input[type="email"]')
        sel_pass = extras.get('seletor_senha', 'input[type="password"]')
        sel_btn = extras.get('seletor_botao', 'button[type="submit"]')
        
        _page.goto(url, timeout=30000)
        _page.fill(sel_user, usuario, timeout=10000)
        _page.fill(sel_pass, senha, timeout=10000)
        _page.click(sel_btn, timeout=10000)
        _page.wait_for_load_state('networkidle', timeout=15000)
        
        print("    ✅ Login OK")
        return f"Login em '{servico}' realizado!"
    except Exception as e:
        return f"Erro: {e}"''',
                "Faz login automático usando credenciais do cofre",
                {"servico": {"type": "string"}, "url_login": {"type": "string"}}
            )
        
        # MEMÓRIA
        if self.memoria_disponivel:
            self.adicionar_ferramenta(
                "salvar_aprendizado",
                '''def salvar_aprendizado(categoria: str, conteudo: str, tags: str = "") -> str:
    print(f"    🧠 Salvando aprendizado: {categoria}")
    try:
        global _memoria
        tags_list = [t.strip() for t in tags.split(",")] if tags else []
        _memoria.adicionar_aprendizado(categoria, conteudo, tags=tags_list)
        print("    ✅ Aprendizado salvo")
        return f"Aprendizado salvo em '{categoria}'"
    except Exception as e:
        return f"Erro: {e}"''',
                "Salva aprendizado na memória permanente. Use para guardar insights, soluções, preferências.",
                {"categoria": {"type": "string", "description": "tecnica/preferencia/bug/solucao"}, 
                 "conteudo": {"type": "string"}, 
                 "tags": {"type": "string", "description": "tags separadas por vírgula"}}
            )
            
            self.adicionar_ferramenta(
                "buscar_aprendizados",
                '''def buscar_aprendizados(query: str = "", categoria: str = "") -> str:
    print(f"    🔍 Buscando: {query or 'todos'}")
    try:
        global _memoria
        resultados = _memoria.buscar_aprendizados(
            query=query if query else None,
            categoria=categoria if categoria else None,
            limite=5
        )
        
        if not resultados:
            return "Nenhum aprendizado encontrado"
        
        texto = f"Encontrados {len(resultados)} aprendizados:\\n"
        for r in resultados:
            texto += f"- [{r['categoria']}] {r['conteudo']}\\n"
        
        print(f"    ✅ {len(resultados)} encontrados")
        return texto
    except Exception as e:
        return f"Erro: {e}"''',
                "Busca aprendizados salvos. Use antes de tarefas para ver se já aprendeu algo relevante.",
                {"query": {"type": "string", "description": "texto para buscar (opcional)"}, 
                 "categoria": {"type": "string", "description": "categoria para filtrar (opcional)"}}
            )
            
            self.adicionar_ferramenta(
                "salvar_preferencia",
                '''def salvar_preferencia(chave: str, valor: str) -> str:
    print(f"    ⚙️ Preferência: {chave}")
    try:
        global _memoria
        _memoria.salvar_preferencia(chave, valor)
        print("    ✅ Salva")
        return f"Preferência '{chave}' salva"
    except Exception as e:
        return f"Erro: {e}"''',
                "Salva preferência do usuário para uso futuro",
                {"chave": {"type": "string"}, "valor": {"type": "string"}}
            )
        
        # AUTO-EVOLUÇÃO
        if self.auto_evolucao_disponivel:
            self.adicionar_ferramenta(
                "anotar_melhoria",
                '''def anotar_melhoria(tipo: str, alvo: str, motivo: str, codigo_sugerido: str, prioridade: int = 5) -> str:
    print(f"    💡 Anotando melhoria...")
    try:
        global _fila_melhorias
        melhoria_id = _fila_melhorias.adicionar(tipo, alvo, motivo, codigo_sugerido, prioridade)
        return f"Melhoria anotada (ID: {melhoria_id})! Será aplicada após conclusão da tarefa atual."
    except Exception as e:
        return f"Erro: {e}"''',
                "Anota melhoria para aplicar DEPOIS da tarefa atual (não interrompe execução). Use quando detectar: otimizações, bugs, novas features.",
                {
                    "tipo": {"type": "string", "enum": ["otimizacao", "bug_fix", "nova_feature", "refatoracao"], "description": "Tipo de melhoria"},
                    "alvo": {"type": "string", "description": "Função/classe/módulo a modificar"},
                    "motivo": {"type": "string", "description": "Por que fazer essa melhoria"},
                    "codigo_sugerido": {"type": "string", "description": "Código completo modificado"},
                    "prioridade": {"type": "integer", "description": "Prioridade 1-10 (padrão: 5)"}
                }
            )
        
        # META-FERRAMENTAS
        self.adicionar_ferramenta(
            "criar_ferramenta",
            '''def criar_ferramenta(nome: str, codigo_python: str, descricao: str, parametros_json: str) -> str:
    import json
    print(f"    🧬 Criando: {nome}")
    try:
        global _nova_ferramenta_info
        _nova_ferramenta_info = {
            'nome': nome,
            'codigo': codigo_python,
            'descricao': descricao,
            'parametros': json.loads(parametros_json)
        }
        print("    ✅ Criada")
        return f"Ferramenta '{nome}' criada!"
    except Exception as e:
        return f"Erro: {e}"''',
            "Cria nova ferramenta dinamicamente",
            {"nome": {"type": "string"}, "codigo_python": {"type": "string"}, 
             "descricao": {"type": "string"}, "parametros_json": {"type": "string"}}
        )
        
        self.adicionar_ferramenta(
            "alterar_limite_iteracoes",
            '''def alterar_limite_iteracoes(novo_limite: int) -> str:
    print(f"    ⚙️ Alterando limite de iterações...")
    try:
        global _novo_limite_iteracoes
        if novo_limite < 10:
            return "Erro: Limite mínimo é 10 iterações"
        if novo_limite > 200:
            return "Erro: Limite máximo é 200 iterações (para evitar custos excessivos)"
        
        _novo_limite_iteracoes = novo_limite
        print(f"    ✅ Limite alterado para {novo_limite}")
        return f"Limite de iterações alterado para {novo_limite}. Isso terá efeito IMEDIATAMENTE nesta execução!"
    except Exception as e:
        return f"Erro: {e}"''',
            "Altera o limite máximo de iterações dinamicamente (efeito imediato na execução atual)",
            {"novo_limite": {"type": "integer", "description": "Novo limite (mínimo 10, máximo 200)"}}
        )
        
        self.adicionar_ferramenta(
            "instalar_biblioteca",
            '''def instalar_biblioteca(nome_pacote: str) -> str:
    import subprocess
    print(f"    📦 Instalando: {nome_pacote}")
    try:
        resultado = subprocess.run(f"pip install {nome_pacote}", shell=True, 
                                 capture_output=True, text=True, timeout=120)
        if resultado.returncode == 0:
            print("    ✅ Instalado")
            return f"'{nome_pacote}' instalado!"
        return f"Erro: {resultado.stderr[:500]}"
    except Exception as e:
        return f"Erro: {e}"''',
            "Instala biblioteca Python via pip",
            {"nome_pacote": {"type": "string"}}
        )
    
    def adicionar_ferramenta(self, nome: str, codigo: str, descricao: str, parametros: dict):
        """Adiciona ferramenta ao sistema"""
        self.ferramentas_codigo[nome] = codigo
        
        # Garantir que os parâmetros estão no formato correto do JSON Schema draft 2020-12
        properties = {}
        for param_name, param_def in parametros.items():
            if isinstance(param_def, dict):
                # Já está no formato correto
                properties[param_name] = param_def
            else:
                # Converter para formato correto
                properties[param_name] = {"type": "string"}
        
        tool_desc = {
            "name": nome,
            "description": descricao,
            "input_schema": {
                "type": "object",
                "properties": properties,
                "required": list(parametros.keys()) if parametros else []
            }
        }
        
        self.ferramentas_descricao = [t for t in self.ferramentas_descricao if t["name"] != nome]
        self.ferramentas_descricao.append(tool_desc)
        
        # Registrar na memória
        if self.memoria_disponivel and nome not in ["salvar_aprendizado", "buscar_aprendizados", "salvar_preferencia"]:
            self.memoria.registrar_ferramenta_criada(nome, descricao, codigo)
    
    def executar(self, nome: str, parametros: dict) -> str:
        """Executa ferramenta"""
        if nome not in self.ferramentas_codigo:
            return f"❌ Ferramenta '{nome}' não existe"
        
        try:
            namespace = {
                '_nova_ferramenta_info': None,
                '_novo_limite_iteracoes': None,
                '_fila_melhorias': self.fila_melhorias,
                '_gerenciador_temp': self.gerenciador_temp,
                '_gerenciador_workspaces': self.gerenciador_workspaces,
                '_playwright_instance': None,
                '_browser': self.browser,
                '_page': self.page,
                '_cofre': self.cofre,
                '_memoria': self.memoria,
                '__builtins__': __builtins__,
                'os': __import__('os')
            }
            
            exec(self.ferramentas_codigo[nome], namespace)
            
            func = None
            for key, value in namespace.items():
                if callable(value) and key == nome:
                    func = value
                    break
            
            if not func:
                return f"❌ Função não encontrada"
            
            resultado = func(**parametros)
            
            # Atualizar estado
            if '_browser' in namespace:
                self.browser = namespace['_browser']
            if '_page' in namespace:
                self.page = namespace['_page']
            
            # Nova ferramenta?
            if nome == "criar_ferramenta" and namespace['_nova_ferramenta_info']:
                info = namespace['_nova_ferramenta_info']
                self.adicionar_ferramenta(
                    info['nome'], info['codigo'], info['descricao'], info['parametros']
                )
            
            # Retornar também o novo limite se foi alterado
            novo_limite = namespace.get('_novo_limite_iteracoes')
            if novo_limite:
                return (str(resultado), novo_limite)
            
            return str(resultado)
            
        except Exception as e:
            import traceback
            return f"Erro: {traceback.format_exc()[:1000]}"
    
    def obter_descricoes(self) -> list:
        return self.ferramentas_descricao


# ============================================================================
# AGENTE COMPLETO FINAL
# ============================================================================

class AgenteCompletoFinal:
    """Agente com TODAS as capacidades"""
    
    def __init__(self, api_key: str, master_password: str = None, usar_memoria: bool = True):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.sistema_ferramentas = SistemaFerramentasCompleto(master_password, usar_memoria)
        self.historico_conversa = []
        self.max_iteracoes_atual = 40  # Configuração padrão que pode ser alterada dinamicamente
    
    def executar_tarefa(self, tarefa: str, max_iteracoes: int = None):
        """Executa tarefa com todas capacidades"""
        
        # Usar max_iteracoes fornecido ou o padrão atual
        if max_iteracoes is None:
            max_iteracoes = self.max_iteracoes_atual
        else:
            self.max_iteracoes_atual = max_iteracoes
        
        # Limpeza automática de arquivos temporários antigos
        if self.sistema_ferramentas.gerenciador_temp_disponivel:
            self.sistema_ferramentas.gerenciador_temp.limpar_arquivos_antigos(exibir_resumo=True)
        
        # Buscar aprendizados relevantes
        contexto_aprendizados = ""
        if self.sistema_ferramentas.memoria_disponivel:
            contexto_aprendizados = self.sistema_ferramentas.memoria.obter_contexto_recente(3)
        
        prompt_sistema = f"""Você é o AGENTE AI MAIS AVANÇADO possível.

CAPACIDADES COMPLETAS:
1. AUTO-EVOLUÇÃO: Cria ferramentas dinamicamente
2. COMPUTER USE: Navega web, screenshots, interação
3. CREDENCIAIS: Acessa cofre criptografado, login automático
4. MEMÓRIA PERMANENTE: Aprende e lembra entre sessões

FERRAMENTAS ESPECIAIS:
- Memória: salvar_aprendizado, buscar_aprendizados, salvar_preferencia
- Credenciais: obter_credencial, login_automatico
- Web: navegar_url, tirar_screenshot, clicar_elemento, preencher_campo
- Meta: criar_ferramenta, instalar_biblioteca

INSTRUÇÕES CRÍTICAS:
1. ANTES de tarefas, BUSQUE aprendizados relevantes
2. DEPOIS de resolver algo novo, SALVE o aprendizado
3. NUNCA mostre senhas ao usuário
4. USE login_automatico sempre que precisar de login
5. APRENDA com erros e sucessos

{contexto_aprendizados}

TAREFA DO USUÁRIO:
{tarefa}

Comece BUSCANDO aprendizados relevantes, depois execute a tarefa!"""
        
        self.historico_conversa = [{"role": "user", "content": prompt_sistema}]
        
        print("\n" + "="*70)
        print(f"👤 TAREFA: {tarefa}")
        print("="*70)
        
        # Status
        status = []
        if self.sistema_ferramentas.cofre_disponivel:
            status.append("✅ Cofre")
        if self.sistema_ferramentas.memoria_disponivel:
            stats = self.sistema_ferramentas.memoria.obter_estatisticas()
            status.append(f"✅ Memória ({stats['total_aprendizados']} aprendizados)")
        status.append(f"🚀 {len(self.sistema_ferramentas.ferramentas_descricao)} ferramentas")
        status.append(f"⚙️ Limite: {max_iteracoes} iterações")
        
        print(" | ".join(status))
        print("-" * 70)
        
        for iteracao in range(1, max_iteracoes + 1):
            print(f"\n🔄 Iteração {iteracao}")
            print("-" * 70)
            
            try:
                response = self.client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=4096,
                    tools=self.sistema_ferramentas.obter_descricoes(),
                    messages=self.historico_conversa
                )
            except BadRequestError as e:
                error_msg = str(e)
                if "JSON schema is invalid" in error_msg:
                    print(f"\n❌ Erro de schema JSON na ferramenta")
                    print(f"   Removendo última ferramenta criada...")
                    
                    # Remover última ferramenta adicionada
                    if len(self.sistema_ferramentas.ferramentas_descricao) > 16:
                        ultima = self.sistema_ferramentas.ferramentas_descricao.pop()
                        print(f"   Ferramenta '{ultima['name']}' removida")
                        print(f"   Tentando novamente...")
                        continue
                    else:
                        print(f"   Não foi possível identificar a ferramenta problemática")
                        break
                else:
                    print(f"\n❌ Erro de requisição: {e}")
                    break
            except Exception as e:
                print(f"\n❌ Erro API: {e}")
                break
            
            if response.stop_reason == "end_turn":
                resposta_final = ""
                for block in response.content:
                    if hasattr(block, "text"):
                        resposta_final += block.text
                
                # Registrar na memória
                if self.sistema_ferramentas.memoria_disponivel:
                    ferramentas_usadas = [h["name"] for h in self.historico_conversa 
                                        if isinstance(h.get("content"), list)
                                        for item in h["content"]
                                        if isinstance(item, dict) and item.get("type") == "tool_use"]
                    
                    self.sistema_ferramentas.memoria.registrar_tarefa(
                        tarefa, resposta_final[:500], ferramentas_usadas, True
                    )
                
                print("\n" + "="*70)
                print("✅ CONCLUÍDO!")
                print("="*70)
                print(resposta_final)
                print("="*70 + "\n")
                
                # 🆕 PROCESSAR AUTO-MELHORIAS
                if self.sistema_ferramentas.auto_evolucao_disponivel:
                    self.processar_auto_melhorias()
                
                return resposta_final
            
            if response.stop_reason == "tool_use":
                self.historico_conversa.append({"role": "assistant", "content": response.content})
                
                tool_results = []
                for block in response.content:
                    if hasattr(block, "text"):
                        texto = block.text[:200] + "..." if len(block.text) > 200 else block.text
                        print(f"  💭 {texto}")
                    
                    if block.type == "tool_use":
                        nome = block.name
                        params = block.input
                        
                        # Ocultar senhas
                        params_display = params.copy()
                        if 'senha' in params_display:
                            params_display['senha'] = '***'
                        
                        print(f"\n  🔧 {nome}")
                        
                        resultado = self.sistema_ferramentas.executar(nome, params)
                        
                        # Verificar se foi alterado o limite de iterações
                        if isinstance(resultado, tuple):
                            resultado_str, novo_limite = resultado
                            if novo_limite:
                                max_iteracoes = novo_limite
                                self.max_iteracoes_atual = novo_limite
                                print(f"  ⚙️ Limite atualizado para {novo_limite} iterações (efeito imediato!)")
                            resultado = resultado_str
                        
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": resultado
                        })
                
                self.historico_conversa.append({"role": "user", "content": tool_results})
        
        print("\n⚠️  Limite atingido")
        return None
    
    def processar_auto_melhorias(self):
        """Processa melhorias anotadas após conclusão da tarefa"""
        
        if not self.sistema_ferramentas.fila_melhorias:
            return
        
        melhorias_pendentes = self.sistema_ferramentas.fila_melhorias.obter_pendentes()
        
        if not melhorias_pendentes:
            return
        
        # Processar melhorias usando o sistema de evolução
        resultados = self.sistema_ferramentas.sistema_evolucao.processar_fila(
            self.sistema_ferramentas.fila_melhorias,
            self.sistema_ferramentas.memoria if self.sistema_ferramentas.memoria_disponivel else None
        )
        
        # Limpar fila após processamento
        self.sistema_ferramentas.fila_melhorias.limpar()


# ============================================================================
# INTERFACE
# ============================================================================

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  🚀 CLAUDE AGENTE COMPLETO - VERSÃO FINAL                   ║
║                                                              ║
║  ✅ Auto-evolução (cria ferramentas)                        ║
║  ✅ Computer Use (navega web + screenshots)                 ║
║  ✅ Credenciais seguras (AES-256)                           ║
║  ✅ Memória permanente (aprende sempre)                     ║
║  ✅ Login automático                                        ║
║  🧬 Auto-modificação (evolui continuamente)                 ║
║  ✅ Autonomia TOTAL                                         ║
║                                                              ║
║  O agente mais avançado E inteligente possível! 🌟          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ Configure ANTHROPIC_API_KEY no .env")
        return
    
    # Opções
    # Memória permanente sempre ativada
    usar_memoria = MEMORIA_DISPONIVEL
    if usar_memoria:
        print("\n🧠 Sistema de memória permanente: ✅ ATIVADO")
    
    # Cofre de credenciais - perguntar apenas se disponível
    usar_cofre = COFRE_DISPONIVEL
    if usar_cofre:
        print("\n🔐 Sistema de credenciais disponível")
        usar = input("   Usar cofre de credenciais? (s/n): ").strip().lower()
        if usar != 's':
            usar_cofre = False
            master_password = None
        else:
            master_password = getpass.getpass("   🔑 Master Password: ")
    else:
        master_password = None
    
    try:
        agente = AgenteCompletoFinal(api_key, master_password if usar_cofre else None, usar_memoria)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        return
    
    while True:
        print("\n" + "-"*70)
        comando = input("\n👤 O que você quer? (ou 'sair'): ").strip()
        
        if comando.lower() in ['sair', 'exit', 'quit', '']:
            print("\n👋 Até logo!")
            if agente.sistema_ferramentas.browser:
                agente.sistema_ferramentas.executar('fechar_navegador', {})
            
            # Mostrar estatísticas finais
            if agente.sistema_ferramentas.memoria_disponivel:
                agente.sistema_ferramentas.memoria.mostrar_resumo()
            
            break
        
        agente.executar_tarefa(comando)
        input("\n⏸️  Pressione ENTER...")


if __name__ == "__main__":
    main()
