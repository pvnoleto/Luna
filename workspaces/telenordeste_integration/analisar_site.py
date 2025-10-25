from playwright.sync_api import sync_playwright
import time
import json

def analisar_site():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        print("🔍 Analisando estrutura do site TeleNordeste...")
        page.goto('https://telenordeste.com.br', wait_until='networkidle')
        time.sleep(3)
        
        # Capturar informações da página
        info = {
            'url': page.url,
            'title': page.title(),
            'buttons': [],
            'links': [],
            'forms': []
        }
        
        # Buscar botões e links relacionados a agendamento
        keywords = ['agendar', 'consulta', 'atendimento', 'marcar', 'teleconsulta', 'login', 'entrar', 'paciente']
        
        print("\n📋 Buscando elementos de agendamento...")
        
        # Procurar por links
        links = page.query_selector_all('a')
        for link in links:
            try:
                text = link.inner_text().lower()
                href = link.get_attribute('href')
                for keyword in keywords:
                    if keyword in text:
                        info['links'].append({'text': text, 'href': href})
                        print(f"  ✓ Link encontrado: {text} -> {href}")
                        break
            except:
                pass
        
        # Procurar por botões
        buttons = page.query_selector_all('button')
        for button in buttons:
            try:
                text = button.inner_text().lower()
                for keyword in keywords:
                    if keyword in text:
                        info['buttons'].append({'text': text})
                        print(f"  ✓ Botão encontrado: {text}")
                        break
            except:
                pass
        
        # Salvar HTML da página
        html_content = page.content()
        with open('pagina_inicial.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n📄 HTML salvo em: pagina_inicial.html")
        
        # Screenshot
        page.screenshot(path='analise_site.png', full_page=True)
        print(f"📸 Screenshot completo salvo: analise_site.png")
        
        # Salvar análise
        with open('analise_estrutura.json', 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Análise completa salva em: analise_estrutura.json")
        
        browser.close()
        return info

if __name__ == '__main__':
    resultado = analisar_site()
    print(f"\n🎯 Análise concluída!")
    print(f"   - {len(resultado['links'])} links relevantes encontrados")
    print(f"   - {len(resultado['buttons'])} botões relevantes encontrados")
