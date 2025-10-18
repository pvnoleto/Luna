from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://www.telenordeste.com.br/agendamento')
    time.sleep(3)
    
    # Captura HTML
    html = page.content()
    
    # Busca links e botões
    links = page.locator('a').all()
    buttons = page.locator('button').all()
    
    print("=" * 80)
    print("ANÁLISE DA PÁGINA PRINCIPAL DE AGENDAMENTO")
    print("=" * 80)
    
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"  - Total de links: {len(links)}")
    print(f"  - Total de botões: {len(buttons)}")
    
    print(f"\n🔗 LINKS ENCONTRADOS:")
    for i, link in enumerate(links[:20], 1):
        try:
            text = link.text_content().strip()
            href = link.get_attribute('href')
            if text or href:
                print(f"  {i}. Texto: '{text[:50]}' | Href: {href}")
        except:
            pass
    
    print(f"\n🔘 BOTÕES ENCONTRADOS:")
    for i, btn in enumerate(buttons, 1):
        try:
            text = btn.text_content().strip()
            onclick = btn.get_attribute('onclick')
            classes = btn.get_attribute('class')
            print(f"  {i}. Texto: '{text}' | Classes: {classes}")
            if onclick:
                print(f"     OnClick: {onclick}")
        except:
            pass
    
    # Procura especificamente por "Agenda Adulto" e "Agenda Infantil"
    print(f"\n🎯 PROCURANDO AGENDAS ESPECÍFICAS:")
    
    # Busca por texto
    adulto = page.locator('text="Agenda Adulto"').count()
    infantil = page.locator('text="Agenda Infantil"').count()
    
    print(f"  - 'Agenda Adulto' encontrado: {adulto} vez(es)")
    print(f"  - 'Agenda Infantil' encontrado: {infantil} vez(es)")
    
    # Tenta encontrar elementos que contenham essas palavras
    all_elements = page.locator('*').all()
    print(f"\n📝 ELEMENTOS COM 'AGENDA':")
    for elem in all_elements[:100]:
        try:
            text = elem.text_content().strip()
            if 'agenda' in text.lower() and len(text) < 100:
                tag = elem.evaluate('el => el.tagName').lower()
                print(f"  - <{tag}>: {text}")
        except:
            pass
    
    browser.close()
