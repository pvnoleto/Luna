#!/bin/bash

echo "========================================"
echo " TeleNordeste Integration - Instalação"
echo "========================================"
echo ""

echo "[1/3] Instalando dependências Python..."
pip install -r requirements.txt

echo ""
echo "[2/3] Criando estrutura de diretórios..."
mkdir -p config logs

echo ""
echo "[3/3] Copiando arquivo de exemplo..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Arquivo .env criado! Configure as variáveis antes de usar."
else
    echo "Arquivo .env já existe."
fi

echo ""
echo "========================================"
echo " Instalação concluída!"
echo "========================================"
echo ""
echo "Próximos passos:"
echo "1. Configure o arquivo .env"
echo "2. Coloque credentials.json em config/"
echo "3. Execute: python src/main.py sync"
echo ""
