#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTE PRÁTICO DOS GERENCIADORES - VERSÃO CORRIGIDA
======================================================
Demonstração completa de todos os recursos

✅ CORREÇÃO APLICADA:
- Linha 60: listar_arquivos() retorna List[Path], não List[Dict]
- Alterado de arq['nome'] para arq.name
- Alterado de arq['tamanho_bytes'] para arq.stat().st_size
"""

import sys
import os

# Adicionar diretório pai ao path para importar os gerenciadores
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gerenciador_temp import GerenciadorTemporarios
from gerenciador_workspaces import GerenciadorWorkspaces
from pathlib import Path
import time

def separador(titulo):
    """Imprime separador visual"""
    print("\n" + "="*80)
    print(f"  {titulo}")
    print("="*80 + "\n")

def teste_gerenciador_workspaces():
    """Testa todas as funcionalidades do gerenciador de workspaces"""
    separador("🧪 TESTE: GERENCIADOR DE WORKSPACES")
    
    gw = GerenciadorWorkspaces()
    
    # 1. Criar workspace
    print("1️⃣ Criando novo workspace 'demo_analise'...")
    resultado = gw.criar_workspace('demo_analise', 'Workspace de demonstração da análise')
    print(f"   ✅ Criado: {resultado}")
    
    # 2. Listar workspaces
    print("\n2️⃣ Listando workspaces existentes...")
    workspaces = gw.listar_workspaces()
    for ws in workspaces:
        print(f"   📁 {ws['nome']}: {ws.get('descricao', 'Sem descrição')}")
    
    # 3. Selecionar workspace
    print("\n3️⃣ Selecionando workspace 'demo_analise'...")
    gw.selecionar_workspace('demo_analise')
    atual = gw.get_workspace_atual()
    print(f"   ✅ Workspace atual: {atual}")
    
    # 4. Criar arquivo no workspace
    print("\n4️⃣ Criando arquivo no workspace...")
    gw.criar_arquivo('exemplo.py', '''#!/usr/bin/env python3
# Exemplo de código no workspace
print("Hello from workspace!")
''')
    print(f"   ✅ Arquivo criado")
    
    # 5. Resolver caminho
    print("\n5️⃣ Resolvendo caminho relativo...")
    caminho = gw.resolver_caminho('exemplo.py')
    print(f"   📍 Caminho completo: {caminho}")
    
    # 6. Listar arquivos
    print("\n6️⃣ Listando arquivos do workspace...")
    arquivos = gw.listar_arquivos('demo_analise')
    # ✅ CORREÇÃO: arquivos é List[Path], não List[Dict]
    for arq in arquivos:
        try:
            tamanho = arq.stat().st_size
            print(f"   📄 {arq.name} ({tamanho} bytes)")
        except Exception as e:
            print(f"   📄 {arq.name} (erro ao obter tamanho: {e})")
    
    # 7. Buscar arquivo
    print("\n7️⃣ Buscando arquivo 'exemplo.py'...")
    resultado = gw.buscar_arquivo('exemplo.py')
    if resultado:
        print(f"   🔍 Encontrado: {resultado}")
        print(f"   🔍 Caminho relativo: {resultado.relative_to(gw.workspaces_dir)}")
    else:
        print(f"   ❌ Não encontrado")
    
    # 8. Exibir árvore
    print("\n8️⃣ Exibindo árvore de diretórios...")
    gw.exibir_arvore('demo_analise')
    
    # 9. Status
    print("\n9️⃣ Exibindo status geral...")
    gw.exibir_status()
    
    return gw

def teste_gerenciador_temporarios():
    """Testa todas as funcionalidades do gerenciador de temporários"""
    separador("🧪 TESTE: GERENCIADOR DE TEMPORÁRIOS")
    
    gt = GerenciadorTemporarios()
    
    # 1. Criar arquivo de teste
    print("1️⃣ Criando arquivo de teste temporário...")
    arquivo_teste = Path('test_temp_demo.txt')
    arquivo_teste.write_text('Este é um arquivo de teste temporário', encoding='utf-8')
    print(f"   ✅ Criado: {arquivo_teste}")
    
    # 2. Marcar como temporário
    print("\n2️⃣ Marcando arquivo como temporário...")
    resultado = gt.marcar_temporario(str(arquivo_teste))
    print(f"   ✅ Marcado: {resultado}")
    
    # 3. Listar temporários
    print("\n3️⃣ Listando arquivos temporários...")
    temporarios = gt.listar_temporarios()
    for temp in temporarios:
        print(f"   🗑️ {temp['caminho']}")
        print(f"      Marcado em: {temp['marcado_em']}")
        print(f"      Deletar em: {temp['delete_em']}")
        print(f"      Tamanho: {temp['tamanho_bytes']} bytes")
    
    # 4. Obter estatísticas
    print("\n4️⃣ Obtendo estatísticas...")
    stats = gt.obter_estatisticas()
    print(f"   📊 Total temporários: {stats['total_temporarios']}")
    print(f"   📊 Total protegidos: {stats['total_protegidos']}")
    print(f"   📊 Total deletados: {stats['total_deletados']}")
    print(f"   📊 Total resgatados: {stats['total_resgatados']}")
    print(f"   📊 Espaço liberado: {stats['espaco_liberado_mb']:.2f} MB")
    
    # 5. Proteger arquivo (simular resgate)
    print("\n5️⃣ Protegendo arquivo (removendo da lista de temporários)...")
    resultado = gt.proteger_arquivo(str(arquivo_teste))
    print(f"   ✅ Protegido: {resultado}")
    
    # 6. Verificar se foi removido
    print("\n6️⃣ Verificando lista de temporários após proteção...")
    temporarios = gt.listar_temporarios()
    print(f"   📊 Total temporários agora: {len(temporarios)}")
    
    # 7. Criar novo arquivo e marcar novamente
    print("\n7️⃣ Criando novo arquivo temporário para demonstração...")
    arquivo_teste2 = Path('test_temp_demo2.log')
    arquivo_teste2.write_text('Log temporário de teste', encoding='utf-8')
    gt.marcar_temporario(str(arquivo_teste2), forcar=True)
    print(f"   ✅ Criado e marcado: {arquivo_teste2}")
    
    # 8. Status
    print("\n8️⃣ Exibindo status geral...")
    gt.exibir_status()
    
    # 9. Limpar (não vai deletar ainda pois não completou 30 dias)
    print("\n9️⃣ Tentando limpar arquivos antigos...")
    resultado = gt.limpar_arquivos_antigos(exibir_resumo=True)
    print(f"   📊 Resultado da limpeza: {resultado}")
    
    # Limpar arquivo de teste
    if arquivo_teste.exists():
        arquivo_teste.unlink()
        print(f"\n🧹 Arquivo de teste {arquivo_teste} removido")
    
    return gt

def teste_integracao():
    """Testa integração entre os dois gerenciadores"""
    separador("🧪 TESTE: INTEGRAÇÃO ENTRE GERENCIADORES")
    
    print("1️⃣ Inicializando gerenciadores...")
    gw = GerenciadorWorkspaces()
    gt = GerenciadorTemporarios()
    
    print("\n2️⃣ Criando workspace de testes...")
    gw.criar_workspace('teste_integracao', 'Teste de integração')
    gw.selecionar_workspace('teste_integracao')
    
    print("\n3️⃣ Criando arquivo temporário no workspace...")
    gw.criar_arquivo('temp_log.txt', 'Log temporário de testes')
    caminho = gw.resolver_caminho('temp_log.txt')
    
    print("\n4️⃣ Marcando arquivo do workspace como temporário...")
    resultado = gt.marcar_temporario(str(caminho), forcar=True)
    print(f"   ✅ Arquivo marcado: {resultado}")
    
    print("\n5️⃣ Verificando arquivo na lista de temporários...")
    temporarios = gt.listar_temporarios()
    encontrado = any(str(caminho) in temp['caminho'] for temp in temporarios)
    print(f"   {'✅' if encontrado else '❌'} Arquivo {'encontrado' if encontrado else 'não encontrado'} na lista")
    
    print("\n6️⃣ Protegendo arquivo (decisão de manter)...")
    gt.proteger_arquivo(str(caminho))
    
    print("\n✅ Integração testada com sucesso!")

def main():
    """Execução principal dos testes"""
    print("\n🚀 INICIANDO TESTES COMPLETOS DOS GERENCIADORES")
    print("="*80)
    
    try:
        # Teste 1: Gerenciador de Workspaces
        teste_gerenciador_workspaces()
        
        # Teste 2: Gerenciador de Temporários
        teste_gerenciador_temporarios()
        
        # Teste 3: Integração
        teste_integracao()
        
        print("\n" + "="*80)
        print("✅ TODOS OS TESTES COMPLETADOS COM SUCESSO!")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERRO durante os testes: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
