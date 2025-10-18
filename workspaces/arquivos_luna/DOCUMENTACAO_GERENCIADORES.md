# Documentação dos Gerenciadores Luna

## 🗑️ GerenciadorTemporarios

Gerencia arquivos temporários com auto-limpeza após 30 dias.

### Métodos Principais:

- **`marcar_temporario()`**: Marca arquivo como temporário (será deletado em 30 dias)
- **`proteger_arquivo()`**: Remove arquivo da lista de temporários e o protege
- **`listar_temporarios()`**: Lista todos os arquivos temporários marcados
- **`limpar_arquivos_antigos()`**: Deleta arquivos temporários antigos (>30 dias)
- **`obter_estatisticas()`**: Retorna estatísticas de uso
- **`exibir_status()`**: Exibe status formatado no console

## 📁 GerenciadorWorkspaces

Organiza projetos em pastas separadas dentro de `Luna/workspaces/`.

### Métodos Principais:

- **`criar_workspace()`**: Cria novo workspace (projeto)
- **`selecionar_workspace()`**: Define workspace ativo
- **`listar_workspaces()`**: Lista todos os workspaces criados
- **`deletar_workspace()`**: Remove workspace e seus arquivos
- **`renomear_workspace()`**: Renomeia workspace existente
- **`resolver_caminho()`**: Converte caminho relativo para absoluto no workspace atual
- **`criar_arquivo()`**: Cria arquivo no workspace atual
- **`buscar_arquivo()`**: Busca arquivo por nome em todos os workspaces
- **`listar_arquivos()`**: Lista arquivos de um workspace
- **`exibir_arvore()`**: Mostra árvore de diretórios
- **`get_workspace_atual()`**: Retorna nome do workspace ativo
- **`get_caminho_workspace()`**: Retorna caminho completo de um workspace

## 💡 Boas Práticas

### Gerenciador de Temporários:
1. Marque screenshots, logs de debug e arquivos de teste como temporários
2. Use `proteger_arquivo()` para arquivos importantes erroneamente marcados
3. Execute `limpar_arquivos_antigos()` periodicamente
4. Verifique `obter_estatisticas()` para monitorar espaço liberado

### Gerenciador de Workspaces:
1. Crie workspace separado para cada projeto
2. Use `resolver_caminho()` para garantir caminhos corretos
3. Sempre selecione workspace antes de criar arquivos
4. Use `buscar_arquivo()` quando não souber a localização exata
5. Execute `exibir_arvore()` para visualizar estrutura

## 🎯 Fluxo de Trabalho Recomendado

```python
# 1. Criar workspace para novo projeto
gw = GerenciadorWorkspaces()
gw.criar_workspace('meu_projeto', 'Descrição do projeto')
gw.selecionar_workspace('meu_projeto')

# 2. Criar arquivos no workspace
caminho = gw.resolver_caminho('codigo.py')
gw.criar_arquivo('codigo.py', 'print("Hello")')

# 3. Marcar arquivos temporários de teste
gt = GerenciadorTemporarios()
gt.marcar_temporario('test_screenshot.png')
gt.marcar_temporario('debug.log')

# 4. Limpar periodicamente
gt.limpar_arquivos_antigos(exibir_resumo=True)
```
