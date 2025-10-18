#!/usr/bin/env python3
"""
Script para fazer scroll e análise do calendário
Usa a sessão do Playwright já aberta
"""

import sys
import os

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar as ferramentas do Luna
from playwright.sync_api import sync_playwright
import time

def main():
    # Este script será executado no contexto que tem acesso ao navegador
    print("🔍 Iniciando análise do calendário...")
    
    # Simular scroll (será executado via eval na página)
    scroll_script = """
    // Scroll suave para baixo
    window.scrollBy({top: 400, behavior: 'smooth'});
    """
    
    print("✅ Script preparado")
    print("\nINSTRUÇÕES:")
    print("1. O calendário está carregado")
    print("2. Scroll manual ou via ferramenta para ver os dias")
    print("3. Observar cores dos dias:")
    print("   - Dias DISPONÍVEIS: coloração mais preta/escura")
    print("   - Dias SEM VAGAS: tom mais apagado/cinza")
    print("   - Dia SELECIONADO: círculo verde")
    
if __name__ == "__main__":
    main()
