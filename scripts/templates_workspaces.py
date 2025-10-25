#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📋 TEMPLATES DE WORKSPACES - SISTEMA LUNA V3
===========================================

Define templates predefinidos para diferentes tipos de projetos.
🆕 FASE 2.2: Sistema de templates de workspace

Autor: Sistema Luna V3
Data: 2025-10-19
"""

from typing import Dict, List
from pathlib import Path


class TemplatesWorkspace:
    """
    Gerencia templates predefinidos para workspaces

    Templates disponíveis:
    - automacao_web: Automação com Playwright/Selenium
    - bot: Bot com comandos e handlers
    - analise_dados: Análise de dados com Pandas/NumPy
    - webapp: Aplicação web (Flask/Django)
    - api: API REST
    - estudo: Material de estudos organizado
    """

    TEMPLATES = {
        "automacao_web": {
            "nome": "Automação Web",
            "descricao": "Projeto de automação web com Playwright",
            "tipo": "automação",
            "tags": ["automação", "web", "scraping"],
            "tech_stack": ["Python", "Playwright"],
            "estrutura": {
                "src/": "Código fonte principal",
                "tests/": "Testes automatizados",
                "data/": "Dados de entrada/saída",
                "logs/": "Arquivos de log",
                "screenshots/": "Capturas de tela",
                "config/": "Arquivos de configuração"
            },
            "arquivos": {
                "src/main.py": '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script principal de automação
"""

from playwright.sync_api import sync_playwright

def main():
    """Função principal"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Seu código aqui
        page.goto("https://example.com")

        browser.close()

if __name__ == "__main__":
    main()
''',
                "README.md": "# Projeto de Automação Web\\n\\nDescrição do projeto.\\n",
                ".gitignore": "*.pyc\\n__pycache__/\\n*.log\\nscreenshots/\\ndata/*.csv\\n",
                "requirements.txt": "playwright\\npython-dotenv\\n"
            }
        },

        "bot": {
            "nome": "Bot",
            "descricao": "Projeto de bot com handlers e comandos",
            "tipo": "bot",
            "tags": ["bot", "automação", "comandos"],
            "tech_stack": ["Python"],
            "estrutura": {
                "bot/": "Código do bot",
                "bot/handlers/": "Handlers de comandos",
                "bot/utils/": "Utilitários",
                "tests/": "Testes",
                "logs/": "Logs de execução"
            },
            "arquivos": {
                "bot/main.py": '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot principal
"""

def main():
    """Inicia o bot"""
    print("Bot iniciado!")
    # Seu código aqui

if __name__ == "__main__":
    main()
''',
                "README.md": "# Bot\\n\\nDescrição do bot.\\n",
                ".gitignore": "*.pyc\\n__pycache__/\\n*.log\\n.env\\n"
            }
        },

        "analise_dados": {
            "nome": "Análise de Dados",
            "descricao": "Projeto de análise de dados com Pandas",
            "tipo": "análise",
            "tags": ["dados", "análise", "visualização"],
            "tech_stack": ["Python", "Pandas", "NumPy"],
            "estrutura": {
                "notebooks/": "Jupyter notebooks",
                "data/raw/": "Dados brutos",
                "data/processed/": "Dados processados",
                "scripts/": "Scripts de processamento",
                "reports/": "Relatórios gerados",
                "visualizations/": "Gráficos e visualizações"
            },
            "arquivos": {
                "notebooks/exploracao.ipynb": "",  # Notebook vazio
                "scripts/processar_dados.py": '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de processamento de dados
"""

import pandas as pd

def processar_dados(arquivo_entrada):
    """Processa dados do arquivo"""
    df = pd.read_csv(arquivo_entrada)
    # Seu código aqui
    return df

if __name__ == "__main__":
    processar_dados("data/raw/dados.csv")
''',
                "README.md": "# Análise de Dados\\n\\nDescrição da análise.\\n",
                "requirements.txt": "pandas\\nnumpy\\nmatplotlib\\njupyter\\n"
            }
        },

        "webapp": {
            "nome": "Web App",
            "descricao": "Aplicação web com Flask",
            "tipo": "webapp",
            "tags": ["web", "flask", "api"],
            "tech_stack": ["Python", "Flask", "HTML"],
            "estrutura": {
                "app/": "Código da aplicação",
                "app/templates/": "Templates HTML",
                "app/static/": "CSS, JS, imagens",
                "app/routes/": "Rotas da aplicação",
                "tests/": "Testes",
                "config/": "Configurações"
            },
            "arquivos": {
                "app/__init__.py": "",
                "app/main.py": '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicação Flask
"""

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True)
''',
                "README.md": "# Web App\\n\\nAplicação web com Flask.\\n",
                "requirements.txt": "flask\\n"
            }
        },

        "estudo": {
            "nome": "Estudo",
            "descricao": "Material de estudos organizado",
            "tipo": "estudo",
            "tags": ["estudo", "aprendizado", "notas"],
            "tech_stack": ["Markdown"],
            "estrutura": {
                "notas/": "Anotações e resumos",
                "exercicios/": "Exercícios práticos",
                "projetos/": "Projetos de prática",
                "recursos/": "PDFs, vídeos, links"
            },
            "arquivos": {
                "README.md": "# Material de Estudo\\n\\n## Tópicos\\n\\n## Recursos\\n\\n## Progresso\\n",
                "notas/introducao.md": "# Introdução\\n\\nNotas de estudo.\\n"
            }
        }
    }

    @classmethod
    def listar_templates(cls) -> List[Dict]:
        """
        Lista todos os templates disponíveis

        Returns:
            Lista de dicionários com info dos templates
        """
        return [
            {
                "id": template_id,
                "nome": info["nome"],
                "descricao": info["descricao"],
                "tipo": info["tipo"],
                "tags": info["tags"]
            }
            for template_id, info in cls.TEMPLATES.items()
        ]

    @classmethod
    def obter_template(cls, template_id: str) -> Dict:
        """
        Obtém template específico

        Args:
            template_id: ID do template

        Returns:
            Dicionário com info completa do template
        """
        return cls.TEMPLATES.get(template_id, {})

    @classmethod
    def aplicar_template(cls, workspace_path: Path, template_id: str) -> bool:
        """
        Aplica template ao workspace

        Args:
            workspace_path: Caminho do workspace
            template_id: ID do template

        Returns:
            True se sucesso, False caso contrário
        """
        template = cls.obter_template(template_id)
        if not template:
            return False

        try:
            # Criar estrutura de pastas
            for pasta, descricao in template.get("estrutura", {}).items():
                pasta_path = workspace_path / pasta
                pasta_path.mkdir(parents=True, exist_ok=True)

                # Criar README na pasta explicando
                readme = pasta_path / ".info.txt"
                readme.write_text(descricao, encoding='utf-8')

            # Criar arquivos predefinidos
            for arquivo, conteudo in template.get("arquivos", {}).items():
                arquivo_path = workspace_path / arquivo
                arquivo_path.parent.mkdir(parents=True, exist_ok=True)

                # Não sobrescrever se já existe
                if not arquivo_path.exists():
                    arquivo_path.write_text(conteudo, encoding='utf-8')

            return True

        except Exception as e:
            print(f"Erro ao aplicar template: {e}")
            return False


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("📋 Templates Disponíveis:")
    print("=" * 70)

    for template in TemplatesWorkspace.listar_templates():
        print(f"\n🏷️  {template['id']}: {template['nome']}")
        print(f"   Descrição: {template['descricao']}")
        print(f"   Tipo: {template['tipo']}")
        print(f"   Tags: {', '.join(template['tags'])}")
