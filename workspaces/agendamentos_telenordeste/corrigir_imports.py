#!/usr/bin/env python3
"""Script para corrigir as importações do agendador_final_corrigido.py"""

# Ler o arquivo original
with open('agendador_final_corrigido.py', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Definir as importações antigas e novas
old_imports = """import sys
import os
import time
from datetime import datetime, timedelta
import re"""

new_imports = """import sys
import os
import time
from datetime import datetime, timedelta
import re
from playwright.sync_api import sync_playwright, Page
from notion_client import Client"""

# Substituir
new_content = content.replace(old_imports, new_imports)

# Salvar arquivo corrigido
with open('agendador_final_corrigido.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ Arquivo agendador_final_corrigido.py foi corrigido!")
print("✅ Importações adicionadas:")
print("   - from playwright.sync_api import sync_playwright, Page")
print("   - from notion_client import Client")
