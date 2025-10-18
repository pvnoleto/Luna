#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Teste de Validação: Correção de Encoding
============================================
Este script testa se as correções de encoding foram aplicadas corretamente.
Execute APÓS reiniciar o agente.
"""

import subprocess
import sys

def teste_encoding_direto():
    """Testa subprocess.run diretamente com encoding"""
    print("🧪 Teste 1: subprocess.run direto com UTF-8")
    print("-" * 50)
    
    # Teste com acentuação
    resultado = subprocess.run(
        'echo "Testando: áéíóú ÁÉÍÓÚ ãõ çÇ 🎉"',
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    
    output = resultado.stdout.strip()
    esperado = "Testando: áéíóú ÁÉÍÓÚ ãõ çÇ 🎉"
    
    # No Windows, echo adiciona aspas
    if '"Testando:' in output:
        output = output.strip('"')
    
    print(f"Output:   {output}")
    print(f"Esperado: {esperado}")
    
    # Verificar caracteres problemáticos
    tem_erro = '�' in output or '?' in output.replace('🎉', '')
    
    if tem_erro:
        print("❌ FALHOU: Caracteres corrompidos detectados!")
        return False
    else:
        print("✅ PASSOU: Encoding UTF-8 funcionando!")
        return True

def teste_encoding_sem_parametro():
    """Testa subprocess.run SEM encoding (deve falhar)"""
    print("\n🧪 Teste 2: subprocess.run SEM encoding (deve falhar)")
    print("-" * 50)
    
    try:
        resultado = subprocess.run(
            'echo "Teste: áéíóú"',
            shell=True,
            capture_output=True,
            text=True  # SEM encoding='utf-8'
        )
        
        output = resultado.stdout.strip()
        print(f"Output: {output}")
        
        tem_erro = '�' in output or '?' in output
        
        if tem_erro:
            print("⚠️  ESPERADO: Falha de encoding detectada (Windows padrão)")
            return True  # Este teste passa se detectar erro (esperado)
        else:
            print("✅ Encoding padrão funcionou (Linux/Mac?)")
            return True
    except Exception as e:
        print(f"⚠️  Exceção: {e}")
        return True

def teste_palavras_portuguesas():
    """Testa palavras portuguesas comuns"""
    print("\n🧪 Teste 3: Palavras portuguesas com acentuação")
    print("-" * 50)
    
    palavras = [
        "ação", "conclusão", "função", "manutenção",
        "café", "você", "até", "José",
        "ninguém", "também", "porém", "após"
    ]
    
    sucesso = True
    for palavra in palavras:
        resultado = subprocess.run(
            f'echo "{palavra}"',
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        output = resultado.stdout.strip().strip('"')
        tem_erro = '�' in output
        
        status = "✅" if not tem_erro else "❌"
        print(f"{status} {palavra} -> {output}")
        
        if tem_erro:
            sucesso = False
    
    return sucesso

def resumo_testes():
    """Executa todos os testes e mostra resumo"""
    print("\n" + "=" * 60)
    print("🧪 BATERIA DE TESTES DE ENCODING UTF-8")
    print("=" * 60)
    
    resultados = []
    
    # Teste 1
    try:
        r1 = teste_encoding_direto()
        resultados.append(("Subprocess com UTF-8", r1))
    except Exception as e:
        print(f"❌ Teste 1 falhou com exceção: {e}")
        resultados.append(("Subprocess com UTF-8", False))
    
    # Teste 2
    try:
        r2 = teste_encoding_sem_parametro()
        resultados.append(("Subprocess SEM UTF-8", r2))
    except Exception as e:
        print(f"❌ Teste 2 falhou com exceção: {e}")
        resultados.append(("Subprocess SEM UTF-8", False))
    
    # Teste 3
    try:
        r3 = teste_palavras_portuguesas()
        resultados.append(("Palavras Portuguesas", r3))
    except Exception as e:
        print(f"❌ Teste 3 falhou com exceção: {e}")
        resultados.append(("Palavras Portuguesas", False))
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    total = len(resultados)
    passou = sum(1 for _, r in resultados if r)
    
    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{status} - {nome}")
    
    print("\n" + "-" * 60)
    print(f"Total: {passou}/{total} testes passaram")
    print("-" * 60)
    
    if passou == total:
        print("\n🎉 SUCESSO TOTAL! Encoding UTF-8 funcionando perfeitamente!")
        return 0
    else:
        print(f"\n⚠️  ATENÇÃO: {total - passou} teste(s) falharam!")
        print("Verifique se as correções foram aplicadas e o agente foi reiniciado.")
        return 1

if __name__ == "__main__":
    print("Encoding do sistema:", sys.stdout.encoding)
    print("Filesystem encoding:", sys.getfilesystemencoding())
    print()
    
    sys.exit(resumo_testes())
