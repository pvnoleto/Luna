from playwright.sync_api import sync_playwright
import time

def criar_repositorio_github():
    with sync_playwright() as p:
        # Iniciar navegador
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Ir para página de login do GitHub
        print("Navegando para GitHub...")
        page.goto("https://github.com/login")
        time.sleep(2)
        
        # Fazer login
        print("Fazendo login...")
        page.fill("#login_field", "pvnoleto@gmail.com")
        page.fill("#password", "quize180994")
        page.click("input[type='submit'][value='Sign in']")
        time.sleep(5)
        
        # Ir para página de criação de repositório
        print("Navegando para criar novo repositorio...")
        page.goto("https://github.com/new")
        time.sleep(3)
        
        # Preencher informações do repositório usando seletores mais robustos
        print("Preenchendo informacoes do repositorio...")
        
        # Nome do repositório - buscar por placeholder
        page.locator('input[name="repository[name]"]').fill("Luna")
        time.sleep(1)
        
        # Descrição
        page.locator('input[name="repository[description]"]').fill("Luna AI Agent - Sistema avancado com memoria permanente e auto-evolucao")
        time.sleep(1)
        
        # Criar repositório
        print("Criando repositorio...")
        page.locator('button:has-text("Create repository")').click()
        time.sleep(5)
        
        # Obter URL do repositório
        url_atual = page.url
        print(f"\nRepositorio criado com sucesso!")
        print(f"URL: {url_atual}")
        
        # Salvar uma screenshot
        page.screenshot(path="repo_criado.png")
        
        time.sleep(3)
        browser.close()
        
        return url_atual

if __name__ == "__main__":
    criar_repositorio_github()
