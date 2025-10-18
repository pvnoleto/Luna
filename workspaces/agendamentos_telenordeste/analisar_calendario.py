#!/usr/bin/env python3
"""Análise do calendário de cardiologia"""

from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    # Conectar ao navegador já aberto via CDP
    try:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        print("📍 Conectado à página atual")
        
        # Aguardar calendário carregar
        time.sleep(2)
        
        # Scroll para ver calendário
        page.evaluate("window.scrollTo(0, 500)")
        time.sleep(1)
        
        # Screenshot do calendário
        page.screenshot(path="analise_cardiologia_03_calendario.png", full_page=False)
        print("✅ Screenshot 3 - Calendário capturado")
        
        # Scroll mais
        page.evaluate("window.scrollTo(0, 800)")
        time.sleep(1)
        
        page.screenshot(path="analise_cardiologia_04_calendario_detalhes.png", full_page=False)
        print("✅ Screenshot 4 - Detalhes do calendário")
        
        # Screenshot página completa
        page.screenshot(path="analise_cardiologia_05_pagina_completa.png", full_page=True)
        print("✅ Screenshot 5 - Página completa capturada")
        
        # Tentar identificar dias disponíveis
        print("\n🔍 Analisando estrutura do calendário...")
        
        # Buscar elementos do calendário
        dias = page.locator('[role="button"]').all()
        print(f"   Total de elementos clicáveis encontrados: {len(dias)}")
        
        # Buscar dias específicos
        dias_calendario = page.locator('.ms-CalendarDay-button').all()
        print(f"   Dias do calendário encontrados: {len(dias_calendario)}")
        
        print("\n✅ Análise concluída!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
