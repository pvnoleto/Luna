#!/usr/bin/env python3
"""
ANÁLISE DA DINÂMICA DO CALENDÁRIO - CARDIOLOGIA
Observação do comportamento de dias e horários disponíveis
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time
from datetime import datetime

def analisar_calendario():
    """Analisa a dinâmica do calendário"""
    
    print("=" * 70)
    print("🔍 ANÁLISE DA DINÂMICA DO CALENDÁRIO - CARDIOLOGIA")
    print("=" * 70)
    
    with sync_playwright() as p:
        try:
            # Tentar conectar ao navegador existente
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            page = context.pages[0]
            print("✅ Conectado ao navegador existente\n")
        except:
            # Se não conseguir, iniciar novo
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto("https://outlook.office365.com/owa/calendar/AdultoTeleNeBP@bp.org.br/bookings/")
            print("✅ Navegador iniciado\n")
            time.sleep(3)
            
            # Clicar em Cardiologia
            try:
                page.click("text=Cardiologia", timeout=5000)
                print("✅ Cardiologia selecionada\n")
                time.sleep(2)
            except:
                print("⚠️ Cardiologia pode já estar selecionada\n")
        
        print("📊 OBSERVAÇÕES DO CALENDÁRIO:")
        print("-" * 70)
        
        # 1. Aguardar calendário carregar
        print("\n1️⃣ Aguardando calendário carregar...")
        time.sleep(2)
        
        # 2. Capturar screenshot inicial
        page.screenshot(path="calendario_01_visao_inicial.png")
        print("   ✅ Screenshot inicial capturado")
        
        # 3. Tentar identificar estrutura do calendário
        print("\n2️⃣ Analisando estrutura do calendário...")
        
        try:
            # Buscar dias do calendário
            dias_buttons = page.locator('[class*="CalendarDay"]').all()
            print(f"   📅 Elementos de dias encontrados: {len(dias_buttons)}")
            
            # Buscar botões de data
            date_buttons = page.locator('button[name*="date"], button[aria-label*="2025"]').all()
            print(f"   📅 Botões de data encontrados: {len(date_buttons)}")
            
        except Exception as e:
            print(f"   ⚠️ Erro ao buscar elementos: {e}")
        
        # 4. Scroll para visualizar todo o calendário
        print("\n3️⃣ Fazendo scroll para visualizar calendário completo...")
        page.evaluate("window.scrollBy(0, 300)")
        time.sleep(1)
        page.screenshot(path="calendario_02_pos_scroll.png")
        print("   ✅ Screenshot pós-scroll capturado")
        
        # 5. Tentar clicar em um dia (se visível)
        print("\n4️⃣ Tentando interagir com dias do calendário...")
        try:
            # Procurar por dias clicáveis
            clickable_days = page.locator('[role="button"][class*="day"], button[aria-label*="Janeiro"]').all()
            print(f"   🖱️ Dias clicáveis encontrados: {len(clickable_days)}")
            
            if len(clickable_days) > 0:
                # Clicar no primeiro dia disponível
                clickable_days[10].click() # Tentar um dia no meio do mês
                time.sleep(1)
                page.screenshot(path="calendario_03_dia_selecionado.png")
                print("   ✅ Dia clicado - screenshot capturado")
                print("   🟢 Observar: círculo verde deve aparecer no dia selecionado")
        except Exception as e:
            print(f"   ⚠️ Não foi possível clicar em dia: {e}")
        
        # 6. Screenshot final da página completa
        print("\n5️⃣ Capturando página completa...")
        page.screenshot(path="calendario_04_pagina_completa.png", full_page=True)
        print("   ✅ Screenshot de página completa capturado")
        
        # 7. Tentar extrair informações de estilo dos dias
        print("\n6️⃣ Analisando estilos dos dias...")
        try:
            # Script para extrair informações de cores
            info_cores = page.evaluate("""
            () => {
                const days = document.querySelectorAll('[class*="CalendarDay"], [role="button"][class*="day"]');
                let info = {
                    total: days.length,
                    com_horarios: 0,
                    sem_horarios: 0,
                    selecionado: 0
                };
                
                days.forEach(day => {
                    const style = window.getComputedStyle(day);
                    const color = style.color;
                    const bgColor = style.backgroundColor;
                    const opacity = style.opacity;
                    
                    // Lógica para determinar estado
                    if (parseFloat(opacity) < 0.5) {
                        info.sem_horarios++;
                    } else if (day.classList.contains('selected') || bgColor.includes('green')) {
                        info.selecionado++;
                    } else {
                        info.com_horarios++;
                    }
                });
                
                return info;
            }
            """)
            
            print(f"   📊 Total de dias: {info_cores.get('total', 0)}")
            print(f"   ⚫ Dias com horários (cor mais preta): {info_cores.get('com_horarios', 0)}")
            print(f"   ⚪ Dias sem horários (cor apagada): {info_cores.get('sem_horarios', 0)}")
            print(f"   🟢 Dias selecionados (círculo verde): {info_cores.get('selecionado', 0)}")
            
        except Exception as e:
            print(f"   ⚠️ Não foi possível extrair informações de cores: {e}")
        
        # 8. Scroll para ver formulário completo
        print("\n7️⃣ Visualizando formulário completo...")
        page.evaluate("window.scrollBy(0, 500)")
        time.sleep(1)
        page.screenshot(path="calendario_05_formulario.png")
        print("   ✅ Screenshot do formulário capturado")
        
        print("\n" + "=" * 70)
        print("✅ ANÁLISE CONCLUÍDA!")
        print("=" * 70)
        print("\n📁 Screenshots salvos:")
        print("   1. calendario_01_visao_inicial.png")
        print("   2. calendario_02_pos_scroll.png")
        print("   3. calendario_03_dia_selecionado.png")
        print("   4. calendario_04_pagina_completa.png")
        print("   5. calendario_05_formulario.png")
        
        print("\n📝 OBSERVAÇÕES IMPORTANTES:")
        print("   ⚫ Dias com HORÁRIOS DISPONÍVEIS: coloração mais PRETA/ESCURA")
        print("   ⚪ Dias SEM horários: tom mais APAGADO/CINZA")
        print("   🟢 Dia SELECIONADO: círculo VERDE aparece sobre o dia")
        print("=" * 70)
        
        # Manter navegador aberto
        input("\n⏸️ Pressione ENTER para fechar o navegador...")

if __name__ == "__main__":
    analisar_calendario()
