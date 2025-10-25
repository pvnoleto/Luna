"""
TeleNordeste Automation Bot
Sistema completo de automação para teleconsultas TeleNordeste
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import json
import time
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telenordeste_bot.log'),
        logging.StreamHandler()
    ]
)

class TeleNordesteBot:
    """Bot de automação para TeleNordeste"""
    
    def __init__(self, headless=False):
        self.headless = headless
        self.browser = None
        self.page = None
        self.base_url = "https://www.telenordeste.com.br"
        logging.info("🤖 TeleNordeste Bot inicializado")
    
    def iniciar(self):
        """Inicia o navegador"""
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=self.headless)
            self.page = self.browser.new_page()
            logging.info("✅ Navegador iniciado com sucesso")
            return True
        except Exception as e:
            logging.error(f"❌ Erro ao iniciar navegador: {e}")
            return False
    
    def fechar(self):
        """Fecha o navegador"""
        try:
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            logging.info("🔒 Navegador fechado")
        except Exception as e:
            logging.error(f"❌ Erro ao fechar navegador: {e}")
    
    def acessar_pagina_inicial(self):
        """Acessa a página inicial"""
        try:
            logging.info(f"🌐 Acessando {self.base_url}...")
            self.page.goto(self.base_url, wait_until='networkidle', timeout=30000)
            time.sleep(3)
            logging.info(f"✅ Página carregada: {self.page.title()}")
            return True
        except Exception as e:
            logging.error(f"❌ Erro ao acessar página inicial: {e}")
            return False
    
    def acessar_area_gestor(self):
        """Acessa a área do gestor de saúde"""
        try:
            logging.info("🔐 Acessando área do gestor...")
            
            # Procurar link da área do gestor
            gestor_link = self.page.query_selector('a[href*="paciente"]')
            
            if gestor_link:
                href = gestor_link.get_attribute('href')
                logging.info(f"📌 Link do gestor encontrado: {href}")
                
                # Clicar no link
                gestor_link.click()
                self.page.wait_for_load_state('networkidle')
                time.sleep(3)
                
                # Screenshot
                self.page.screenshot(path=f'area_gestor_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
                logging.info("✅ Área do gestor acessada")
                return True
            else:
                logging.warning("⚠️ Link do gestor não encontrado")
                return False
                
        except Exception as e:
            logging.error(f"❌ Erro ao acessar área do gestor: {e}")
            return False
    
    def acessar_painel_projeto(self):
        """Acessa o painel do projeto (Power BI)"""
        try:
            logging.info("📊 Acessando painel do projeto...")
            
            # Link direto do painel
            painel_url = "https://bit.ly/Painel_TeleNordeste"
            
            # Abrir em nova aba
            new_page = self.browser.new_page()
            new_page.goto(painel_url, wait_until='networkidle', timeout=30000)
            time.sleep(5)
            
            # Screenshot
            new_page.screenshot(path=f'painel_projeto_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png', full_page=True)
            
            logging.info(f"✅ Painel acessado: {new_page.title()}")
            
            # Extrair URL real (após redirecionamento do bit.ly)
            url_real = new_page.url
            logging.info(f"🔗 URL real do painel: {url_real}")
            
            return new_page, url_real
            
        except Exception as e:
            logging.error(f"❌ Erro ao acessar painel: {e}")
            return None, None
    
    def extrair_informacoes_pagina(self):
        """Extrai todas as informações da página atual"""
        try:
            logging.info("📝 Extraindo informações da página...")
            
            info = {
                'timestamp': datetime.now().isoformat(),
                'url': self.page.url,
                'title': self.page.title(),
                'texto_completo': self.page.inner_text('body'),
                'links': []
            }
            
            # Extrair links
            links = self.page.query_selector_all('a')
            for link in links:
                try:
                    href = link.get_attribute('href')
                    text = link.inner_text().strip()
                    if href and text:
                        info['links'].append({'text': text, 'href': href})
                except:
                    pass
            
            logging.info(f"✅ Informações extraídas: {len(info['links'])} links encontrados")
            return info
            
        except Exception as e:
            logging.error(f"❌ Erro ao extrair informações: {e}")
            return None
    
    def salvar_dados(self, dados, nome_arquivo):
        """Salva dados em JSON"""
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            logging.info(f"💾 Dados salvos em: {nome_arquivo}")
            return True
        except Exception as e:
            logging.error(f"❌ Erro ao salvar dados: {e}")
            return False
    
    def monitorar_site(self, intervalo_segundos=300):
        """Monitora o site em intervalos regulares"""
        logging.info(f"👀 Iniciando monitoramento (intervalo: {intervalo_segundos}s)")
        
        try:
            while True:
                # Acessar página
                self.acessar_pagina_inicial()
                
                # Extrair informações
                info = self.extrair_informacoes_pagina()
                
                # Salvar com timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.salvar_dados(info, f'monitoramento_{timestamp}.json')
                
                # Screenshot
                self.page.screenshot(path=f'monitor_{timestamp}.png', full_page=True)
                
                logging.info(f"⏰ Próxima verificação em {intervalo_segundos}s")
                time.sleep(intervalo_segundos)
                
        except KeyboardInterrupt:
            logging.info("⏹️ Monitoramento interrompido pelo usuário")
        except Exception as e:
            logging.error(f"❌ Erro no monitoramento: {e}")
    
    def executar_fluxo_completo(self):
        """Executa fluxo completo de automação"""
        logging.info("🚀 Iniciando fluxo completo de automação")
        
        try:
            # 1. Acessar página inicial
            if not self.acessar_pagina_inicial():
                return False
            
            # 2. Extrair informações iniciais
            info_inicial = self.extrair_informacoes_pagina()
            self.salvar_dados(info_inicial, 'dados_pagina_inicial.json')
            
            # 3. Screenshot inicial
            self.page.screenshot(path='01_pagina_inicial.png', full_page=True)
            
            # 4. Acessar área do gestor
            self.acessar_area_gestor()
            info_gestor = self.extrair_informacoes_pagina()
            self.salvar_dados(info_gestor, 'dados_area_gestor.json')
            
            # 5. Voltar à página inicial
            self.page.goto(self.base_url)
            time.sleep(2)
            
            # 6. Acessar painel do projeto
            painel_page, painel_url = self.acessar_painel_projeto()
            
            if painel_page:
                # Extrair informações do painel
                info_painel = {
                    'timestamp': datetime.now().isoformat(),
                    'url': painel_url,
                    'title': painel_page.title(),
                    'texto': painel_page.inner_text('body')
                }
                self.salvar_dados(info_painel, 'dados_painel_projeto.json')
                painel_page.close()
            
            logging.info("✅ Fluxo completo executado com sucesso!")
            return True
            
        except Exception as e:
            logging.error(f"❌ Erro no fluxo completo: {e}")
            return False


def main():
    """Função principal"""
    print("=" * 70)
    print("🤖 TELENORDESTE AUTOMATION BOT")
    print("=" * 70)
    print()
    print("Opções:")
    print("1. Executar fluxo completo")
    print("2. Monitorar site continuamente")
    print("3. Apenas acessar e explorar")
    print()
    
    opcao = input("Escolha uma opção (1-3): ").strip()
    
    bot = TeleNordesteBot(headless=False)
    
    try:
        if not bot.iniciar():
            print("❌ Erro ao iniciar bot")
            return
        
        if opcao == "1":
            bot.executar_fluxo_completo()
        elif opcao == "2":
            intervalo = int(input("Intervalo de monitoramento (segundos, padrão 300): ") or "300")
            bot.monitorar_site(intervalo)
        elif opcao == "3":
            bot.acessar_pagina_inicial()
            info = bot.extrair_informacoes_pagina()
            bot.salvar_dados(info, 'exploracao.json')
            print("\n✅ Exploração concluída! Dados salvos em exploracao.json")
            input("\nPressione ENTER para fechar...")
        else:
            print("❌ Opção inválida")
        
    finally:
        bot.fechar()


if __name__ == "__main__":
    main()
