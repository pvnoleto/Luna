from playwright.sync_api import sync_playwright
import time
import json
import re

def explorar_site_completo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        print("🔍 Explorando site TeleNordeste (Wix)...")
        page.goto('https://telenordeste.com.br', wait_until='networkidle')
        time.sleep(5)  # Esperar Wix carregar completamente
        
        # Capturar todo o texto visível
        body_text = page.inner_text('body')
        print(f"\n📝 Texto da página capturado ({len(body_text)} caracteres)")
        
        # Salvar texto completo
        with open('texto_pagina.txt', 'w', encoding='utf-8') as f:
            f.write(body_text)
        
        # Buscar palavras-chave
        keywords = ['agendar', 'consulta', 'atendimento', 'marcar', 'teleconsulta', 
                   'login', 'entrar', 'paciente', 'área do paciente', 'acessar']
        
        encontrados = {}
        for keyword in keywords:
            if keyword.lower() in body_text.lower():
                encontrados[keyword] = True
                print(f"  ✓ Palavra-chave encontrada: {keyword}")
        
        # Capturar todos os links
        all_links = page.query_selector_all('a')
        links_info = []
        
        print(f"\n🔗 Analisando {len(all_links)} links...")
        for link in all_links:
            try:
                href = link.get_attribute('href')
                text = link.inner_text().strip()
                if href and text:
                    links_info.append({
                        'text': text,
                        'href': href
                    })
                    # Mostrar links interessantes
                    text_lower = text.lower()
                    if any(kw in text_lower for kw in ['agend', 'consult', 'paciente', 'login', 'entrar', 'acesso']):
                        print(f"  📌 Link relevante: '{text}' -> {href}")
            except:
                pass
        
        # Procurar por iframes
        iframes = page.query_selector_all('iframe')
        print(f"\n🖼️ Encontrados {len(iframes)} iframes")
        
        # Tentar encontrar botões/elementos interativos
        print(f"\n🔘 Buscando botões e elementos interativos...")
        
        # Diferentes seletores que podem conter botões
        selectors = [
            'button',
            '[role="button"]',
            'a[href*="agend"]',
            'a[href*="login"]',
            'a[href*="paciente"]',
            'div[class*="button"]',
            'div[class*="btn"]'
        ]
        
        interactive_elements = []
        for selector in selectors:
            try:
                elements = page.query_selector_all(selector)
                for elem in elements:
                    try:
                        text = elem.inner_text().strip()
                        if text:
                            interactive_elements.append({
                                'selector': selector,
                                'text': text
                            })
                            print(f"  ✓ Elemento: [{selector}] '{text}'")
                    except:
                        pass
            except:
                pass
        
        # Screenshot final
        page.screenshot(path='exploracao_completa.png', full_page=True)
        
        # Compilar resultados
        resultado = {
            'url': page.url,
            'title': page.title(),
            'keywords_encontradas': encontrados,
            'total_links': len(links_info),
            'links': links_info[:50],  # Primeiros 50
            'interactive_elements': interactive_elements,
            'total_iframes': len(iframes)
        }
        
        # Salvar JSON
        with open('exploracao_completa.json', 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Exploração completa!")
        print(f"   - Keywords encontradas: {len(encontrados)}")
        print(f"   - Links totais: {len(links_info)}")
        print(f"   - Elementos interativos: {len(interactive_elements)}")
        
        browser.close()
        return resultado

if __name__ == '__main__':
    resultado = explorar_site_completo()
