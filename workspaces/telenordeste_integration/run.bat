@echo off
REM Script de execução - TeleNordeste Integration

echo.
echo ============================================================
echo  TeleNordeste Integration
echo  Iniciando...
echo ============================================================
echo.

python main.py

if errorlevel 1 (
    echo.
    echo ============================================================
    echo  ERRO ao executar!
    echo ============================================================
    pause
)
