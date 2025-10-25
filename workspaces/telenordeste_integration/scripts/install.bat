@echo off
echo ========================================
echo  TeleNordeste Integration - Instalacao
echo ========================================
echo.

echo [1/3] Instalando dependencias Python...
pip install -r requirements.txt

echo.
echo [2/3] Criando estrutura de diretorios...
if not exist "config" mkdir config
if not exist "logs" mkdir logs

echo.
echo [3/3] Copiando arquivo de exemplo...
if not exist ".env" (
    copy .env.example .env
    echo Arquivo .env criado! Configure as variaveis antes de usar.
) else (
    echo Arquivo .env ja existe.
)

echo.
echo ========================================
echo  Instalacao concluida!
echo ========================================
echo.
echo Proximos passos:
echo 1. Configure o arquivo .env
echo 2. Coloque credentials.json em config/
echo 3. Execute: python src/main.py sync
echo.
pause
