#!/usr/bin/env python3
"""Script para fazer scroll na página"""

import time
from playwright.sync_api import sync_playwright

def scroll_and_capture():
    with sync_playwright() as p:
        # Conectar ao navegador já aberto
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0]
        
        # Scroll suave para baixo
        page.evaluate("window.scrollBy(0, 300)")
        time.sleep(1)
        
        # Capturar screenshot
        page.screenshot(path="analise_cardiologia_03_scroll1.png")
        print("Screenshot 1 capturado")
        
        # Mais scroll
        page.evaluate("window.scrollBy(0, 300)")
        time.sleep(1)
        
        # Capturar screenshot
        page.screenshot(path="analise_cardiologia_04_scroll2.png")
        print("Screenshot 2 capturado")
        
        # Scroll para ver o calendário completo
        page.evaluate("window.scrollBy(0, 400)")
        time.sleep(1)
        
        # Capturar screenshot final
        page.screenshot(path="analise_cardiologia_05_calendario_completo.png")
        print("Screenshot final capturado")

if __name__ == "__main__":
    scroll_and_capture()
