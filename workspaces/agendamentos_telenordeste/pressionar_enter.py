from playwright.sync_api import sync_playwright
import time

# Script para pressionar Enter no campo de senha do Notion
with sync_playwright() as p:
    # Conectar ao navegador existente (não criar novo)
    # Como já temos um navegador aberto, vamos usar pyautogui
    pass

# Alternativa: usar pyautogui
try:
    import pyautogui
    time.sleep(1)
    pyautogui.press('enter')
    print("Enter pressionado com sucesso!")
except Exception as e:
    print(f"Erro: {e}")
