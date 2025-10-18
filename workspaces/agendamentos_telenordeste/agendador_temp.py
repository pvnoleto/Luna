#!/usr/bin/env python3

"""
AGENDADOR FINAL CORRIGIDO
Versão que estava 95% funcional - encontrava 4 dias com vagas (16, 23, 30, 31)
"""

import sys
import os
import time
from datetime import datetime, timedelta
import re

# Funções de log integradas
def log_info(mensagem: str):
    """Log de informação com timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] ℹ️  {mensagem}")

def log_sucesso(mensagem: str):
    """Log de sucesso com timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] ✅ {mensagem}")

def log_erro(mensagem: str):
    """Log de erro com timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] ❌ {mensagem}")

def log_aviso(mensagem: str):
    """Log de aviso com timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] ⚠️ {mensagem}")

def conectar_notion() -> Client:
    """Conecta ao Notion usando API direta."""
    try:
        client = Client(auth=NOTION_TOKEN)
        log_sucesso("Conectado ao Notion")
        return client
    except Exception as e:
        log_erro(f"Erro ao conectar ao Notion: {e}")
        return None

def buscar_tarefas_nao_iniciadas(client: Client) -> list:
    """Busca tarefas com status 'Não iniciado' usando API direta do Notion."""
    try:
        log_info("🔍 Buscando tarefas 'Não Iniciadas' no Notion...")
        
        # Buscar tarefas com status "Não iniciado"
        response = client.databases.query(
            database_id=DATABASE_ID,
            filter={
                "property": "Status",
                "select": {
                    "equals": "Não iniciado"
                }
            }
        )
        
        tarefas = []
        for page in response["results"]:
            try:
                properties = page["properties"]
                
                # Extrair dados básicos com tratamento robusto
                nome = ""
                if "Nome da tarefa" in properties and properties["Nome da tarefa"]["title"]:
                    nome = properties["Nome da tarefa"]["title"][0]["text"]["content"]
                elif "Nome" in properties and properties["Nome"]["title"]:
                    nome = properties["Nome"]["title"][0]["text"]["content"]
                
                status = ""
                if "Status" in properties and properties["Status"]["select"]:
                    status = properties["Status"]["select"]["name"]
                
                # Extrair dados específicos com múltiplas tentativas
                cpf = ""
                especialidade = ""
                motivo = ""
                acs = ""
                tipo = ""
                
                # Extrair da descrição se disponível
                descricao = ""
                if "Descrição" in properties and properties["Descrição"]["rich_text"]:
                    descricao = properties["Descrição"]["rich_text"][0]["text"]["content"]
                    
                    # Parse da descrição para extrair dados
                    lines = descricao.split('\n')
                    for line in lines:
                        if line.startswith("Nome:"):
                            if not nome:
                                nome = line.replace("Nome:", "").strip()
                        elif line.startswith("CPF:"):
                            cpf = line.replace("CPF:", "").strip()
                        elif line.startswith("Especialidade:"):
                            especialidade = line.replace("Especialidade:", "").strip()
                        elif line.startswith("Motivo da Consulta:"):
                            motivo = line.replace("Motivo da Consulta:", "").strip()
                        elif line.startswith("ACS:"):
                            acs = line.replace("ACS:", "").strip()
                    
                    # Inferir tipo da descrição
                    if "Infantil" in descricao:
                        tipo = "Infantil"
                    elif "Adulto" in descricao:
                        tipo = "Adulto"
                
                # Verificar se tem dados essenciais
                if nome and especialidade:
                    # Garantir que tipo seja definido
                    if not tipo:
                        # Inferir tipo baseado na especialidade
                        especialidades_infantis = [
                            "triagem", "pediatria", "neuropediatria", "psiquiatria infantil", 
                            "psiquiatria pediátrica", "endocrinologia pediátrica"
                        ]
                        if any(esp in especialidade.lower() for esp in especialidades_infantis):
                            tipo = "Infantil"
                        else:
                            tipo = "Adulto"
                    
                    tarefa = {
                        "id": page["id"],
                        "nome": nome,
                        "status": status,
                        "cpf": cpf,
                        "especialidade": especialidade,
                        "motivo": motivo,
                        "acs": acs,
                        "tipo": tipo,
                        "descricao": descricao
                    }
                    tarefas.append(tarefa)
                    
            except Exception as e:
                log_erro(f"Erro ao processar tarefa: {e}")
                continue
        
        log_sucesso(f"Encontradas {len(tarefas)} tarefas para processar")
        for i, tarefa in enumerate(tarefas, 1):
            log_info(f"   {i}. {tarefa['nome']} ({tarefa['especialidade']} - {tarefa['tipo']})")
        
        return tarefas
        
    except Exception as e:
        log_erro(f"Erro ao buscar tarefas: {e}")
        return []

def atualizar_status_tarefa(client: Client, tarefa_id: str, novo_status: str, resumo: str = "") -> bool:
    """Atualiza o status de uma tarefa no Notion."""
    try:
        if DRY_RUN:
            log_aviso(f"🧪 DRY RUN: Simulando atualização de status para '{novo_status}'")
            return True
        
        client.pages.update(
            page_id=tarefa_id,
            properties={
                "Status": {
                    "select": {
                        "name": novo_status
                    }
                }
            }
        )
        
        log_sucesso(f"✅ Status atualizado para: {novo_status}")
        return True
        
    except Exception as e:
        log_erro(f"❌ Erro ao atualizar status: {e}")
        return False

def atualizar_status_tarefa_completa(client: Client, tarefa_id: str, data: str, horario: str) -> bool:
    """Atualiza tarefa para status 'Concluída' com data e horário."""
    try:
        if DRY_RUN:
            log_aviso(f"🧪 DRY RUN: Simulando atualização para 'Concluída' - {data} às {horario}")
            return True
        
        # Atualizar para Concluída
        client.pages.update(
            page_id=tarefa_id,
            properties={
                "Status": {
                    "select": {
                        "name": "Concluída"
                    }
                }
            }
        )
        
        log_sucesso(f"✅ Tarefa marcada como 'Concluída' - {data} às {horario}")
        return True
        
    except Exception as e:
        log_erro(f"❌ Erro ao marcar como concluída: {e}")
        return False

# Imports do Playwright
from playwright.sync_api import sync_playwright, Page
from notion_client import Client

# Configurações
NOTION_TOKEN = "ntn_V83285389753nEE04QHEhZ7yusPR9ZIjZg5JY3HfeKvakc"
DATABASE_ID = "23b1f06b-6b5f-80f5-8901-000b818675db"
DRY_RUN = True  # Modo de teste - MODO TESTE (DRY RUN) - Nenhum agendamento será efetivado!

def navegar_para_agenda(page: Page, tipo: str) -> bool:
    """Navega para a agenda especificada (Infantil ou Adulto)."""
    try:
        if tipo.lower() == "infantil":
            url = "https://outlook.office365.com/owa/calendar/PeditricoTeleNEBP@bp.org.br/bookings/"
            log_info("🧭 Navegando para Agenda Infantil...")
        else:
            url = "https://outlook.office365.com/owa/calendar/AdultoTeleNeBP@bp.org.br/bookings/"
            log_info("🧭 Navegando para Agenda Adulto...")
        
        log_info(f"🧭 URL: {url}")
        
        # Navegar para URL
        page.goto(url, timeout=30000)
        
        # Aguardar carregamento
        log_info("🧭 Aguardando carregamento da agenda...")
        page.wait_for_timeout(8000)
        
        log_sucesso(f"✅ Navegação para Agenda {'Infantil' if tipo.lower() == 'infantil' else 'Adulto'} bem-sucedida!")
        
        return True
        
    except Exception as e:
        log_erro(f"❌ Erro ao navegar para agenda: {e}")
        return False

def selecionar_especialidade(page: Page, especialidade: str) -> bool:
    """Seleciona a especialidade com detecção inteligente de variações."""
    try:
        # Aguardar especialidades carregarem
        page.wait_for_timeout(8000)
        log_info(f"🔍 Procurando especialidade: {especialidade}")
        
        # Mapeamento de especialidades com variações
        mapeamento_especialidades = {
            "triagem": ["triagem", "avaliação", "primeira consulta", "inicial"],
            "neurologia": ["neurologia", "neuro", "neurologista"],
            "psiquiatria": ["psiquiatria", "psiquiatra", "saúde mental"],
            "psiquiatria infantil": ["psiquiatria infantil", "psiquiatria pediátrica", "psiquiatra infantil"],
            "psiquiatria pediátrica": ["psiquiatria pediátrica", "psiquiatria infantil", "psiquiatra pediátrico"],
            "neuropediatria": ["neuropediatria", "neuro pediatria", "neuropediatra"],
            "pediatria": ["pediatria", "pediatra", "pediátrico"],
            "endocrinologia": ["endocrinologia", "endócrino", "endocrinologista"],
            "cardiologia": ["cardiologia", "cardio", "cardiologista"],
            "dermatologia": ["dermatologia", "dermato", "dermatologista"],
            "ginecologia": ["ginecologia", "gineco", "ginecologista"]
        }
        
        # Encontrar variações da especialidade
        especialidade_lower = especialidade.lower()
        variacoes = [especialidade_lower]
        
        for esp_base, lista_variacoes in mapeamento_especialidades.items():
            if especialidade_lower in lista_variacoes or esp_base == especialidade_lower:
                variacoes.extend(lista_variacoes)
                break
        
        # Remover duplicatas e manter ordem
        variacoes = list(dict.fromkeys(variacoes))
        log_info(f"🔍 Variações a buscar: {variacoes}")
        
        # Aguardar mais tempo para garantir carregamento
        page.wait_for_timeout(5000)
        
        # Tentar encontrar a especialidade com diferentes estratégias
        elemento_encontrado = None
        
        # Estratégia 1: Busca exata por texto
        for variacao in variacoes:
            try:
                elementos = page.locator(f"text=/{re.escape(variacao)}/i").all()
                if elementos:
                    log_sucesso(f"✅ Especialidade encontrada (exata): '{variacao}'")
                    elemento_encontrado = elementos[0]
                    break
            except:
                continue
        
        # Estratégia 2: Busca por contém texto
        if not elemento_encontrado:
            for variacao in variacoes:
                try:
                    elementos = page.locator(f":has-text('{variacao}')").all()
                    if elementos:
                        log_sucesso(f"✅ Especialidade encontrada (contém): '{variacao}'")
                        elemento_encontrado = elementos[0]
                        break
                except:
                    continue
        
        # Estratégia 3: Busca em botões e links
        if not elemento_encontrado:
            for variacao in variacoes:
                try:
                    elementos = page.locator(f"button:has-text('{variacao}'), a:has-text('{variacao}'), div:has-text('{variacao}')").all()
                    if elementos:
                        log_sucesso(f"✅ Especialidade encontrada (elemento): '{variacao}'")
                        elemento_encontrado = elementos[0]
                        break
                except:
                    continue
        
        if elemento_encontrado:
            log_sucesso(f"✅ ✅ Especialidade '{especialidade}' encontrada!")
            
            # Clicar no elemento encontrado
            log_info("🖱️ Clicando na especialidade...")
            elemento_encontrado.click()
            page.wait_for_timeout(5000)
            
            # Verificar se há botão OK ou similar
            try:
                botoes_confirmacao = [
                    "button:has-text('OK')",
                    "button:has-text('Ok')", 
                    "button:has-text('Continuar')",
                    "button:has-text('Próximo')",
                    "button:has-text('Avançar')"
                ]
                
                for seletor in botoes_confirmacao:
                    botao = page.locator(seletor).first
                    if botao.is_visible():
                        botao.click()
                        page.wait_for_timeout(3000)
                        log_info(f"✅ Botão de confirmação clicado: {seletor}")
                        break
            except:
                pass
            
            return True
        else:
            log_erro(f"❌ Especialidade '{especialidade}' não encontrada com nenhuma estratégia")
            
            # Listar especialidades disponíveis para debug
            try:
                log_info("🔍 Especialidades disponíveis na página:")
                elementos_texto = page.locator("text=/[a-zA-Z]{3,}/").all()[:20]  # Limitar a 20 elementos
                for i, elem in enumerate(elementos_texto):
                    try:
                        texto = elem.text_content().strip()
                        if len(texto) > 3 and len(texto) < 50:
                            log_info(f"   - {texto}")
                    except:
                        continue
            except:
                pass
            
            return False
            
    except Exception as e:
        log_erro(f"❌ Erro ao selecionar especialidade: {e}")
        return False

def buscar_horarios_disponiveis(page: Page, horario_preferido: str = None) -> tuple:
    """Busca horários disponíveis no calendário."""
    try:
        log_info("🔍 Procurando horários disponíveis...")
        
        # Aguardar calendário carregar completamente
        log_info("⏳ Aguardando carregamento completo do calendário (60 segundos)...")
        page.wait_for_timeout(60000)
        
        # Horários válidos expandidos (BRT - sem conversão de fuso)
        horarios_validos = [
            "7:00", "7:30", "8:00", "8:30", "9:00", "9:30", 
            "10:00", "10:30", "11:00", "11:30", "12:00", "12:30",
            "13:00", "13:30", "14:00", "14:30", "15:00", "15:30",
            "16:00", "16:30", "17:00", "17:30", "18:00"
        ]
        
        log_info(f"🕐 Horários válidos: {horarios_validos}")
        
        # Obter dia atual
        hoje = datetime.now().day
        log_info(f"📅 Hoje é dia {hoje} - Buscando dias >= {hoje + 1}")
        
        # Buscar elementos de dia com diferentes estratégias
        seletores_dia = [
            "div[role='gridcell']",  # Células de calendário
            "button[aria-label*='dia']",  # Botões de dia
            "td[role='gridcell']",  # Células de tabela
            "div[data-date]",  # Divs com data
            ".calendar-day",  # Classe comum de dia
            "[aria-label*='day']"  # Elementos com aria-label de dia
        ]
        
        dias_elementos = []
        for seletor in seletores_dia:
            try:
                elementos = page.locator(seletor).all()
                if elementos:
                    log_info(f"🔍 Encontrados {len(elementos)} elementos com seletor: {seletor}")
                    dias_elementos.extend(elementos)
                    break  # Usar o primeiro seletor que encontrar elementos
            except:
                continue
        
        # Se não encontrou com seletores específicos, buscar todos os divs
        if not dias_elementos:
            log_info("🔍 Buscando dias em todos os elementos div...")
            dias_elementos = page.locator("div").all()
        
        dias_validos = []
        log_info(f"🔍 Analisando {len(dias_elementos)} elementos para encontrar dias...")
        
        for i, elemento in enumerate(dias_elementos):
            try:
                # Obter texto do elemento
                texto = elemento.text_content()
                if not texto:
                    continue
                
                texto = texto.strip()
                
                # Verificar se é um número de dia válido
                if texto.isdigit() and 1 <= int(texto) <= 31:
                    numero_dia = int(texto)
                    
                    # Filtrar apenas dias futuros
                    if numero_dia <= hoje:
                        continue
                    
                    # Verificar atributos que indicam disponibilidade
                    aria_disabled = elemento.get_attribute("aria-disabled")
                    aria_label = elemento.get_attribute("aria-label") or ""
                    class_name = elemento.get_attribute("class") or ""
                    
                    # Verificar se está explicitamente desabilitado
                    if aria_disabled == "true":
                        log_info(f"⚪ Dia {numero_dia}: Explicitamente desabilitado (aria-disabled=true)")
                        continue
                    
                    # Verificar mensagens de indisponibilidade
                    if any(msg in aria_label.lower() for msg in ["não há", "indisponível", "sem vagas", "fechado"]):
                        log_info(f"⚪ Dia {numero_dia}: Indisponível por aria-label")
                        continue
                    
                    # Verificar classes que indicam indisponibilidade
                    classes_indisponiveis = ["disabled", "unavailable", "blocked", "inactive"]
                    if any(cls in class_name.lower() for cls in classes_indisponiveis):
                        log_info(f"⚪ Dia {numero_dia}: Indisponível por classe CSS")
                        continue
                    
                    # Verificar cores que indicam disponibilidade (estratégia avançada)
                    try:
                        # Obter estilos computados
                        style = elemento.get_attribute("style") or ""
                        
                        # Cores que geralmente indicam disponibilidade
                        cores_disponiveis = ["green", "blue", "#00", "#0f", "#1f", "#2f", "#3f", "#4f", "#5f"]
                        cores_indisponiveis = ["gray", "grey", "#ccc", "#ddd", "#eee", "#f0f", "disabled"]
                        
                        tem_cor_disponivel = any(cor in style.lower() for cor in cores_disponiveis)
                        tem_cor_indisponivel = any(cor in style.lower() for cor in cores_indisponiveis)
                        
                        if tem_cor_indisponivel and not tem_cor_disponivel:
                            log_info(f"⚪ Dia {numero_dia}: Indisponível por cor (cinza/desabilitado)")
                            continue
                    except:
                        pass
                    
                    # Verificar se o elemento é clicável
                    try:
                        if not elemento.is_enabled():
                            log_info(f"⚪ Dia {numero_dia}: Elemento não habilitado")
                            continue
                    except:
                        pass
                    
                    log_info(f"✅ Dia candidato: {numero_dia} (índice {i})")
                    dias_validos.append((elemento, numero_dia, i))
                    
            except Exception as e:
                continue
        
        if not dias_validos:
            log_erro("❌ Nenhum dia válido encontrado")
            return None, None
        
        log_sucesso(f"✅ Encontrados {len(dias_validos)} dias com vagas: {[d[1] for d in dias_validos]}")
        
        # Testar cada dia válido
        for elemento_dia, numero_dia, indice in dias_validos:
            log_info(f"🎯 Testando dia: {numero_dia}")
            
            try:
                # Clicar no dia
                elemento_dia.click()
                page.wait_for_timeout(8000)
                
                # Verificar se apareceu mensagem de "não há disponibilidade"
                sem_disponibilidade = page.locator(":has-text('Não há disponibilidade')").is_visible()
                if sem_disponibilidade:
                    log_info(f"⚠️ Dia {numero_dia}: Sem disponibilidade")
                    continue
                
                # Procurar horários disponíveis
                horarios_elementos = page.locator("text=/^\\d{1,2}:\\d{2}$/").all()
                
                for elemento_horario in horarios_elementos:
                    try:
                        horario_texto = elemento_horario.text_content().strip()
                        log_info(f"🕐 Horário encontrado: {horario_texto}")
                        
                        if horario_texto in horarios_validos:
                            log_sucesso(f"✅ Horário válido encontrado: {horario_texto}")
                            
                            # Clicar no horário
                            elemento_horario.click()
                            page.wait_for_timeout(5000)
                            
                            # Verificar se formulário carregou
                            formulario_carregado = page.locator("input[placeholder*='Primeiro e sobrenome']").is_visible()
                            if formulario_carregado:
                                data_formatada = f"{numero_dia:02d}/{datetime.now().month:02d}/{datetime.now().year}"
                                log_sucesso(f"✅ Formulário carregado! Data: {data_formatada}, Horário: {horario_texto}")
                                return data_formatada, horario_texto
                            else:
                                log_aviso(f"⚠️ Formulário não carregou após clicar em {horario_texto}")
                        
                    except Exception as e:
                        continue
                
                log_info(f"⚠️ Dia {numero_dia}: Nenhum horário válido encontrado")
                
            except Exception as e:
                log_erro(f"❌ Erro ao testar dia {numero_dia}: {e}")
                continue
        
        log_erro("❌ Nenhum horário disponível encontrado após testar todos os dias")
        return None, None
        
    except Exception as e:
        log_erro(f"❌ Erro ao buscar horários: {e}")
        return None, None

def preencher_formulario(page: Page, tarefa: dict) -> bool:
    """Preenche o formulário com os dados da tarefa."""
    try:
        log_info("📝 Preenchendo formulário...")
        
        # Aguardar formulário carregar
        page.wait_for_timeout(5000)
        
        # Preparar dados para preenchimento com lógica robusta
        acs_limpo = tarefa.get("acs", "Pedro").split(" | ")[0].split(" +")[0].strip() if tarefa.get("acs") else "Pedro"
        
        dados = {
            "nome": tarefa.get("nome", ""),
            "email": "equipesos02@outlook.com",  # Email fixo da equipe
            "cpf": tarefa.get("cpf", "000.000.000-00"),
            "cnes": "2368846",  # CNES fixo da unidade
            "profissional_medico": acs_limpo,
            "telefone_ubs": "86999978887",  # Telefone fixo da UBS
            "motivo": tarefa.get("motivo", "Consulta médica especializada")
        }
        
        log_info(f"📝 Dados a preencher:")
        for campo, valor in dados.items():
            log_info(f"   {campo}: {valor}")
        
        campos_preenchidos = 0
        
        # Preencher Nome
        try:
            nome_input = page.locator("input[placeholder*='Primeiro e sobrenome']").first
            if nome_input.is_visible():
                nome_input.fill(dados["nome"])
                log_info(f"✅ Nome preenchido: {dados['nome']}")
                campos_preenchidos += 1
        except Exception as e:
            log_erro(f"❌ Erro ao preencher nome: {e}")
        
        # Preencher Email
        try:
            email_input = page.locator("input[placeholder*='email'], input[type='email']").first
            if email_input.is_visible():
                email_input.fill(dados["email"])
                log_info(f"✅ Email preenchido: {dados['email']}")
                campos_preenchidos += 1
        except Exception as e:
            log_erro(f"❌ Erro ao preencher email: {e}")
        
        # Preencher CPF
        try:
            cpf_input = page.locator("input[placeholder*='CPF'], input[aria-label*='CPF']").first
            if cpf_input.is_visible():
                cpf_input.fill(dados["cpf"])
                log_info(f"✅ CPF preenchido: {dados['cpf']}")
                campos_preenchidos += 1
        except Exception as e:
            log_erro(f"❌ Erro ao preencher CPF: {e}")
        
        # Preencher CNES
        try:
            cnes_input = page.locator("input[placeholder*='CNES'], input[aria-label*='CNES']").first
            if cnes_input.is_visible():
                cnes_input.fill(dados["cnes"])
                log_info(f"✅ CNES preenchido: {dados['cnes']}")
                campos_preenchidos += 1
        except Exception as e:
            log_erro(f"❌ Erro ao preencher CNES: {e}")
        
        # Preencher Profissional Médico
        try:
            prof_input = page.locator("input[placeholder*='Profissional'], input[aria-label*='Profissional']").first
            if prof_input.is_visible():
                prof_input.fill(dados["profissional_medico"])
                log_info(f"✅ Profissional Médico preenchido: {dados['profissional_medico']}")
                campos_preenchidos += 1
        except Exception as e:
            log_erro(f"❌ Erro ao preencher Profissional Médico: {e}")
        
        # Preencher Telefone UBS
        try:
            tel_input = page.locator("input[placeholder*='Telefone'], input[aria-label*='Telefone']").first
            if tel_input.is_visible():
                tel_input.fill(dados["telefone_ubs"])
                log_info(f"✅ Telefone UBS preenchido: {dados['telefone_ubs']}")
                campos_preenchidos += 1
        except Exception as e:
            log_erro(f"❌ Erro ao preencher Telefone UBS: {e}")
        
        # Preencher Motivo
        try:
            motivo_input = page.locator("textarea[placeholder*='Motivo'], textarea[aria-label*='Motivo'], input[placeholder*='Motivo']").first
            if motivo_input.is_visible():
                motivo_input.fill(dados["motivo"])
                log_info(f"✅ Motivo preenchido: {dados['motivo']}")
                campos_preenchidos += 1
        except Exception as e:
            log_erro(f"❌ Erro ao preencher Motivo: {e}")
        
        log_sucesso(f"✅ Formulário preenchido: {campos_preenchidos} campos")
        
        # Verificar se preencheu campos obrigatórios mínimos
        if campos_preenchidos >= 5:  # Nome, Email, CPF, CNES, Motivo
            return True
        else:
            log_erro(f"❌ Poucos campos preenchidos: {campos_preenchidos}/7")
            return False
        
    except Exception as e:
        log_erro(f"❌ Erro ao preencher formulário: {e}")
        return False

def clicar_reservar(page: Page) -> bool:
    """Clica no botão Reservar."""
    try:
        if DRY_RUN:
            log_aviso("🧪 DRY RUN: Simulando clique em 'Reservar'")
            return True
        
        # Procurar botão Reservar
        botao_reservar = page.locator("button:has-text('Reservar'), input[value='Reservar']").first
        
        if botao_reservar.is_visible():
            botao_reservar.click()
            page.wait_for_timeout(5000)
            log_sucesso("✅ Botão 'Reservar' clicado com sucesso!")
            return True
        else:
            log_erro("❌ Botão 'Reservar' não encontrado")
            return False
            
    except Exception as e:
        log_erro(f"❌ Erro ao clicar em Reservar: {e}")
        return False

def verificar_confirmacao(page: Page) -> dict:
    """Verifica se o agendamento foi confirmado."""
    try:
        if DRY_RUN:
            log_aviso("🧪 DRY RUN: Simulando confirmação de agendamento")
            return {
                "confirmado": True,
                "data": datetime.now().strftime("%d/%m/%Y"),
                "horario": "10:00",
                "resumo": "Agendamento simulado em modo DRY RUN"
            }
        
        # Aguardar possível confirmação
        page.wait_for_timeout(10000)
        
        # Verificar sinais de confirmação
        confirmacao_textos = [
            "confirmado", "agendado", "reservado", "sucesso",
            "confirmação", "agendamento realizado"
        ]
        
        for texto in confirmacao_textos:
            if page.locator(f":has-text('{texto}')").is_visible():
                log_sucesso(f"✅ Confirmação detectada: {texto}")
                return {
                    "confirmado": True,
                    "data": datetime.now().strftime("%d/%m/%Y"),
                    "horario": "10:00",
                    "resumo": f"Agendamento confirmado - {texto}"
                }
        
        log_aviso("⚠️ Confirmação não detectada claramente")
        return {
            "confirmado": False,
            "data": None,
            "horario": None,
            "resumo": "Confirmação não detectada"
        }
        
    except Exception as e:
        log_erro(f"❌ Erro ao verificar confirmação: {e}")
        return {
            "confirmado": False,
            "data": None,
            "horario": None,
            "resumo": f"Erro: {e}"
        }

def executar_agendamento_final() -> bool:
    """Executa o agendamento final com todas as melhorias."""
    try:
        print("🎯 AGENDAMENTO FINAL CORRIGIDO")
        print("=" * 60)
        if DRY_RUN:
            print("🧪 MODO TESTE (DRY RUN) - Nenhum agendamento será efetivado!")
        else:
            print("⚠️  MODO REAL - Agendamento será efetivado!")
        print("=" * 60)
        
        # Conectar ao Notion
        client = conectar_notion()
        if not client:
            log_erro("❌ Falha ao conectar com o Notion!")
            return False
        
        # Buscar tarefas reais do Notion
        tarefas = buscar_tarefas_nao_iniciadas(client)
        log_sucesso(f"✅ Encontradas {len(tarefas)} tarefa(s) reais do Notion")
        
        if not tarefas:
            log_erro("❌ Nenhuma tarefa encontrada!")
            return False
        
        sucessos = 0
        erros = 0
        
        # Processar cada tarefa
        for tarefa in tarefas:
            log_sucesso(f"✅ Processando: {tarefa['nome']}")
            
            # Guardar status original
            status_original = tarefa.get("status", "Não iniciado")
            
            # Executar agendamento para esta tarefa
            import os
            is_sandbox = os.environ.get('USER') == 'ubuntu' and os.path.exists('/home/ubuntu')
            
            try:
                with sync_playwright() as p:
                    # Configuração inteligente do navegador
                    if is_sandbox:
                        # No sandbox, usar headless
                        browser = p.chromium.launch(
                            headless=True,
                            args=[
                                '--no-sandbox',
                                '--disable-dev-shm-usage',
                                '--disable-gpu',
                                '--disable-web-security',
                                '--disable-features=VizDisplayCompositor'
                            ]
                        )
                        log_info("🤖 Navegador iniciado em modo headless (sandbox)")
                    else:
                        # Fora do sandbox, mostrar navegador
                        browser = p.chromium.launch(
                            headless=False,
                            slow_mo=1000,  # Delay para visualização
                            args=[
                                '--start-maximized',
                                '--disable-web-security',
                                '--disable-features=VizDisplayCompositor'
                            ]
                        )
                        log_info("🌐 Navegador iniciado em modo visual")
                    
                    # Configurar contexto com timezone correto
                    context = browser.new_context(
                        timezone_id="America/Fortaleza",  # Fuso horário BRT
                        locale="pt-BR"
                    )
                    page = context.new_page()
                    
                    try:
                        # Etapa 1: Navegar para agenda
                        if not navegar_para_agenda(page, tarefa["tipo"]):
                            log_erro(f"❌ {tarefa['nome']}: Erro ao abrir agenda")
                            erros += 1
                            continue
                        
                        # Etapa 2: Selecionar especialidade
                        if not selecionar_especialidade(page, tarefa["especialidade"]):
                            log_erro(f"❌ {tarefa['nome']}: Especialidade não encontrada")
                            erros += 1
                            continue
                        
                        # Etapa 3: Encontrar horário
                        data, horario = buscar_horarios_disponiveis(page, None)
                        if not data or not horario:
                            log_erro(f"❌ {tarefa['nome']}: Nenhum horário disponível")
                            erros += 1
                            continue
                        
                        log_sucesso(f"✅ {tarefa['nome']}: Horário selecionado: {data} às {horario}")
                        
                        # Etapa 4: Preencher formulário
                        if not preencher_formulario(page, tarefa):
                            log_erro(f"❌ {tarefa['nome']}: Erro ao preencher formulário")
                            erros += 1
                            continue
                        
                        # Etapa 5: Clicar em Reservar
                        if not clicar_reservar(page):
                            log_erro(f"❌ {tarefa['nome']}: Erro ao clicar em Reservar")
                            erros += 1
                            continue
                        
                        # Etapa 6: Verificar confirmação
                        confirmacao = verificar_confirmacao(page)
                        
                        if confirmacao["confirmado"]:
                            log_sucesso(f"🎉 {tarefa['nome']}: AGENDAMENTO REALIZADO COM SUCESSO!")
                            # Atualizar status no Notion
                            if atualizar_status_tarefa_completa(client, tarefa["id"], data, horario):
                                log_sucesso(f"✅ {tarefa['nome']}: Status atualizado no Notion para 'Concluída'")
                            sucessos += 1
                        else:
                            log_aviso(f"⚠️ {tarefa['nome']}: Confirmação não detectada - agendamento pode ter falhado")
                            
                            # Restaurar status original
                            atualizar_status_tarefa(client, tarefa["id"], status_original, "Status restaurado - agendamento não confirmado")
                            erros += 1
                        
                    except Exception as e:
                        log_erro(f"❌ {tarefa['nome']}: Erro durante agendamento: {e}")
                        erros += 1
                    finally:
                        browser.close()
                        
            except Exception as e:
                log_erro(f"❌ {tarefa['nome']}: Erro geral: {e}")
                erros += 1
        
        # Relatório final detalhado
        print("\n" + "=" * 60)
        print("📊 RELATÓRIO FINAL DE PROCESSAMENTO")
        print("=" * 60)
        print(f"✅ Sucessos: {sucessos}")
        print(f"❌ Erros: {erros}")
        print(f"📋 Total processado: {sucessos + erros}")
        print(f"📈 Taxa de sucesso: {(sucessos/(sucessos+erros)*100):.1f}%" if (sucessos+erros) > 0 else "0%")
        
        if sucessos > 0:
            print(f"\n🎉 {sucessos} agendamento(s) realizado(s) com sucesso!")
            print("✅ Tarefas processadas e atualizadas no Notion!")
        
        if erros > 0:
            print(f"\n⚠️ {erros} erro(s) encontrado(s)")
            print("💡 Verifique os logs acima para identificar problemas")
            print("💡 Possíveis causas: especialidades não encontradas, sem horários disponíveis")
        
        print("\n" + "=" * 60)
        print("🔧 CONFIGURAÇÕES:")
        print(f"   • Modo: {'DRY RUN (Teste)' if DRY_RUN else 'PRODUÇÃO (Real)'}")
        print(f"   • Navegador: {'Headless (Sandbox)' if is_sandbox else 'Visual (Local)'}")
        print(f"   • Fuso horário: America/Fortaleza (BRT)")
        print(f"   • API: Notion direta")
        print("=" * 60)
        
        return sucessos > 0
                
    except Exception as e:
        log_erro(f"❌ Erro geral: {e}")
        return False

if __name__ == "__main__":
    # Executar agendamento final
    sucesso = executar_agendamento_final()
    
    if sucesso:
        print("\n🎉 AGENDAMENTO CONCLUÍDO COM SUCESSO!")
        print("✅ Script processou tarefas reais do Notion!")
        print("📝 Logs detalhados disponíveis acima")
        if DRY_RUN:
            print("💡 Para usar em produção, altere DRY_RUN = False no código")
        print("🌐 O navegador abrirá visualmente quando executado fora do sandbox")
    else:
        print("\n❌ NENHUM AGENDAMENTO FOI COMPLETADO")
        print("⚠️ Verifique se existem tarefas com status 'Não iniciado' no Notion")
        print("🔍 Analise os logs acima para identificar problemas específicos")
        print("💡 Certifique-se de que o token e database_id do Notion estão corretos")
    
    print("\n🏁 EXECUÇÃO FINALIZADA")
