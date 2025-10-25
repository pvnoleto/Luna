@echo off
REM Script de instalação - TeleNordeste Integration
echo ============================================================
echo  TeleNordeste Integration - Instalador
echo ============================================================
echo.

echo [1/3] Verificando Python...
python --version
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.8+ de: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo [2/3] Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo ERRO: Falha ao instalar dependencias!
    pause
    exit /b 1
)

echo.
echo [3/3] Verificando instalacao...
python -c "import requests; import google.auth; print('OK')" > nul 2>&1
if errorlevel 1 (
    echo ERRO: Dependencias nao instaladas corretamente!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  Instalacao concluida com sucesso!
echo ============================================================
echo.
echo Proximos passos:
echo  1. Configure suas credenciais (Notion e Google)
echo  2. Execute: python main.py
echo.
pause
