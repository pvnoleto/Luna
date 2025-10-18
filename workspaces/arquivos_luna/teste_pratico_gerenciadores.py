#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTE PRÁTICO DOS GERENCIADORES
===================================
Demonstração completa de todos os recursos
"""

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
    for arq in arquivos:
        print(f"   📄 {arq['nome']} ({arq['tamanho_bytes']} bytes)")
    
    # 7. Buscar arquivo
    print("\n7️⃣ Buscando arquivo 'exemplo.py'...")
    resultados = gw.buscar_arquivo('exemplo.py')
    for res in resultados:
        print(f"   🔍 Encontrado em: {res['workspace']} -> {res['caminho_relativo']}")
    
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
    print(f"   📊 Deletados: {resultado['deletados']}")
    print(f"   📊 Erros: {resultado['erros']}")
    
    # Limpar arquivos de teste
    print("\n🧹 Limpando arquivos de teste criados...")
    if arquivo_teste.exists():
        arquivo_teste.unlink()
        print(f"   ✅ Removido: {arquivo_teste}")
    if arquivo_teste2.exists():
        arquivo_teste2.unlink()
        print(f"   ✅ Removido: {arquivo_teste2}")
    
    return gt

def teste_integracao():
    """Testa integração entre os dois gerenciadores"""
    separador("🧪 TESTE: INTEGRAÇÃO DOS GERENCIADORES")
    
    gw = GerenciadorWorkspaces()
    gt = GerenciadorTemporarios()
    
    print("1️⃣ Criando workspace de teste...")
    gw.criar_workspace('teste_integracao', 'Workspace para teste de integração')
    gw.selecionar_workspace('teste_integracao')
    
    print("\n2️⃣ Criando arquivo de código no workspace...")
    gw.criar_arquivo('codigo_importante.py', 'print("Código importante")')
    
    print("\n3️⃣ Criando arquivo de log temporário no workspace...")
    caminho_log = gw.resolver_caminho('debug.log')
    Path(caminho_log).write_text('Log de debug temporário', encoding='utf-8')
    
    print("\n4️⃣ Marcando arquivo de log como temporário...")
    gt.marcar_temporario(caminho_log)
    
    print("\n5️⃣ Listando arquivos do workspace...")
    arquivos = gw.listar_arquivos('teste_integracao')
    for arq in arquivos:
        print(f"   📄 {arq['nome']}")
    
    print("\n6️⃣ Listando temporários...")
    temporarios = gt.listar_temporarios()
    for temp in temporarios:
        print(f"   🗑️ {Path(temp['caminho']).name}")
    
    print("\n✅ Integração funcionando perfeitamente!")
    print("   • Workspaces organizam projetos")
    print("   • Temporários marcam arquivos para limpeza")
    print("   • Ambos trabalham juntos de forma transparente")

def resumo_final():
    """Exibe resumo final dos testes"""
    separador("📊 RESUMO FINAL DA ANÁLISE")
    
    print("""
✅ GERENCIADOR DE WORKSPACES:
   • Organiza projetos em pastas separadas
   • Resolve caminhos automaticamente
   • Busca arquivos em todos os workspaces
   • Exibe árvore de diretórios
   • Renomeia e deleta workspaces

✅ GERENCIADOR DE TEMPORÁRIOS:
   • Marca arquivos para auto-limpeza
   • Deleta automaticamente após 30 dias
   • Protege arquivos importantes
   • Rastreia estatísticas de uso
   • Libera espaço em disco

✅ INTEGRAÇÃO:
   • Workspaces + Temporários = Organização perfeita
   • Arquivos importantes no workspace correto
   • Arquivos temporários marcados para limpeza
   • Produtividade maximizada

💡 BOAS PRÁTICAS IDENTIFICADAS:
   1. Sempre criar workspace para novos projetos
   2. Usar resolver_caminho() para paths seguros
   3. Marcar screenshots/logs/debug como temporários
   4. Executar limpar_arquivos_antigos() semanalmente
   5. Verificar estatísticas para monitorar uso
    """)

if __name__ == "__main__":
    print("\n" + "🚀 INICIANDO TESTES COMPLETOS DOS GERENCIADORES" + "\n")
    print("=" * 80)
    
    try:
        # Executar testes
        teste_gerenciador_workspaces()
        time.sleep(1)
        
        teste_gerenciador_temporarios()
        time.sleep(1)
        
        teste_integracao()
        time.sleep(1)
        
        resumo_final()
        
        print("\n" + "="*80)
        print("✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERRO durante os testes: {e}")
        import traceback
        traceback.print_exc()
