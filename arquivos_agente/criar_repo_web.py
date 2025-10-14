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
        time.sleep(3)
        
        # Ir para página de criação de repositório
        print("Navegando para criar novo repositorio...")
        page.goto("https://github.com/new")
        time.sleep(2)
        
        # Preencher informações do repositório
        print("Preenchendo informacoes do repositorio...")
        page.fill("#\\:r0\\:", "Luna")  # Nome do repositório
        time.sleep(1)
        
        # Descrição
        page.fill("#\\:r1\\:", "Luna AI Agent - Sistema avancado com memoria permanente, cofre de credenciais, auto-evolucao e capacidades de Computer Use")
        time.sleep(1)
        
        # Manter público (já é o padrão)
        
        # Criar repositório
        print("Criando repositorio...")
        page.click("button[type='submit']:has-text('Create repository')")
        time.sleep(3)
        
        # Obter URL do repositório
        url_atual = page.url
        print(f"\nRepositorio criado com sucesso!")
        print(f"URL: {url_atual}")
        
        time.sleep(2)
        browser.close()
        
        return url_atual

if __name__ == "__main__":
    criar_repositorio_github()
