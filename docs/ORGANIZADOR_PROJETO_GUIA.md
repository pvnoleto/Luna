# 📁 ORGANIZADOR INTELIGENTE DE PROJETO - GUIA COMPLETO

## 🎯 Visão Geral

O **Organizador Inteligente de Projeto** é um sistema automático que reorganiza a raiz do projeto Luna, mantendo apenas arquivos essenciais e movendo documentação, testes e scripts para pastas específicas.

**Criado:** 2025-10-20
**Melhoria adicional ao Luna V3**

---

## 🆚 Diferença do Gerenciador de Workspaces

| Aspecto | Gerenciador de Workspaces | Organizador de Projeto |
|---------|---------------------------|------------------------|
| **Escopo** | Organiza workspaces em `workspaces/` | Organiza RAIZ do projeto Luna |
| **Categorização** | Por extensão (genérica) | Semântica (inteligente) |
| **Estrutura** | code/, doc/, test/, config/ | docs/, tests/, scripts/, .backups/ |
| **Ajuste de imports** | ❌ Não | ✅ Automático |
| **Validação** | ❌ Não | ✅ Testa importação |

---

## 🚀 Funcionalidades

### 1. Detecção Inteligente de Tipos
Usa análise **semântica** (não apenas extensão):

- **Documentação**: RELATORIO_*, GUIA_*, CHECKPOINT_*, *.pdf, etc.
- **Testes**: test_*.py, testes_*.py, run_all_tests.py
- **Scripts**: analisar_*, atualizar_*, corrigir_*, refatorar_*
- **Backups**: *.backup*, *.bak, *_backup_*
- **Essenciais**: Módulos Python, dados hardcoded, configs

### 2. Reorganização Automática
- Cria pastas: `docs/`, `tests/`, `scripts/`
- Move arquivos para pastas corretas
- Ajusta `sys.path` em arquivos movidos
- Atualiza test runners automaticamente
- Valida integridade pós-reorganização

### 3. Sistema de Snapshot e Rollback
- Backup automático antes de reorganizar
- Rollback automático se validação falhar
- Preserva paths hardcoded (`Luna/.stats/`, `Luna/planos/`)

### 4. Modo Dry-Run
- Simula reorganização sem executar
- Preview completo de mudanças
- Detecta possíveis problemas

---

## 📝 Como Usar

### Opção 1: Via Luna (Ferramenta Integrada)

```
Luna, analise a organização do projeto
```

Luna executará a ferramenta `analisar_organizacao_projeto` e mostrará:
- Total de arquivos na raiz
- Quantos são essenciais
- Sugestões de reorganização
- Ajustes necessários

```
Luna, reorganize o projeto (dry-run)
```

Luna executará `reorganizar_projeto` em modo simulação.

```
Luna, reorganize o projeto de verdade
```

Luna executará com `dry_run=false` (cria snapshot antes!).

### Opção 2: Diretamente via Python

```python
from organizador_projeto import OrganizadorProjeto

# 1. Análise (sem executar)
org = OrganizadorProjeto()
analise = org.analisar_projeto()

print(f"Essenciais na raiz: {len(analise['essenciais_raiz'])}")
print(f"Mover para docs/: {len(analise['mover']['docs/'])}")
print(f"Mover para tests/: {len(analise['mover']['tests/'])}")

# 2. Dry-run (simulação)
resultado = org.reorganizar_projeto(dry_run=True, confirmar=False)
print(f"Arquivos a mover: {len(resultado['arquivos_movidos'])}")

# 3. Executar de verdade (cria snapshot antes!)
resultado = org.reorganizar_projeto(dry_run=False, confirmar=True)

if resultado['sucesso']:
    print(f"✅ {len(resultado['arquivos_movidos'])} arquivos reorganizados")
else:
    print(f"❌ Erros: {resultado['erros']}")
```

### Opção 3: Executar o módulo diretamente

```bash
python organizador_projeto.py
```

Executa análise + dry-run automático.

---

## 📊 Exemplo de Output

### Análise:
```
📊 ANÁLISE DE ORGANIZAÇÃO
==================================================

Total de arquivos na raiz: 103

✅ Essenciais (manter): 26
  - 1 módulo principal
  - 13 módulos Python
  - 10 dados/config
  - 2 docs essenciais

📚 Sugestões de reorganização:
  → docs/: 38 arquivos
  → tests/: 21 arquivos
  → scripts/: 10 arquivos
  → .backups/: 6 arquivos

⚠️  Ajustes necessários:
  → Imports: 17 arquivos
  → Test runners: 2 arquivos
```

### Reorganização (dry-run):
```
🔄 REORGANIZAÇÃO (SIMULAÇÃO)
==================================================

📁 Pastas criadas: docs/, tests/, scripts/

📦 Arquivos movidos: 75
🔧 Imports ajustados: 17

✅ Dry-run concluído sem erros!
💡 Use dry_run=false para executar de verdade
```

---

## 🛡️ Segurança

### Proteções Implementadas:
1. ✅ **Backup automático** antes de qualquer mudança (em `.rollback_backups/`)
2. ✅ **Dry-run** para preview completo
3. ✅ **Validação pós-reorganização** (testa importação)
4. ✅ **Rollback automático** se validação falhar
5. ✅ **Preserva arquivos críticos**:
   - Não move: módulos essenciais, arquivos de dados, .env
   - Preserva: paths hardcoded (`Luna/.stats/`, `Luna/planos/`)
6. ✅ **Confirmação em cada etapa** (modo interativo)

### Arquivos Sempre Mantidos na Raiz:
- **Módulos Python**: `luna_v3_FINAL_OTIMIZADA.py`, `memoria_permanente.py`, etc.
- **Dados**: `memoria_agente.json`, `cofre.enc`, `credentials.json`, etc.
- **Configs**: `.env`, `workspace_config.json`
- **Documentação essencial**: `README.md`, `CLAUDE.md`

---

## 🔧 Customização

### Adicionar módulos à lista de essenciais:
Edite `organizador_projeto.py`:

```python
class DetectorTipoArquivo:
    MODULOS_ESSENCIAIS = {
        'luna_v3_FINAL_OTIMIZADA.py',
        'memoria_permanente.py',
        # Adicione seu módulo aqui:
        'meu_modulo.py'
    }
```

### Adicionar novos padrões de detecção:
```python
@staticmethod
def detectar_tipo(arquivo: Path, base_dir: Path) -> str:
    nome = arquivo.name

    # Adicione sua lógica aqui:
    if nome.startswith('MEU_PADRAO_'):
        return 'documentacao'

    # ... resto do código
```

---

## 📈 Resultado Esperado

### Antes:
```
Luna/
├── (100+ arquivos misturados na raiz)
└── workspaces/
```

### Depois:
```
Luna/
├── luna_v3_FINAL_OTIMIZADA.py
├── 12 módulos Python essenciais
├── 10 arquivos de dados/config
├── README.md + CLAUDE.md
├── docs/ (38 arquivos)
│   ├── RELATORIO_*.md
│   ├── GUIA_*.md
│   ├── CHECKPOINT_*.md
│   └── *.pdf, *.txt
├── tests/ (27 arquivos)
│   ├── test_*.py
│   ├── run_all_tests.py
│   └── test_coverage_report.py
├── scripts/ (10 arquivos)
│   ├── analisar_*.py
│   ├── atualizar_*.py
│   └── refatorar_*.py
└── workspaces/
```

**Redução:** De ~100 para 26 arquivos na raiz (74% mais limpo!)

---

## ⚠️ Avisos Importantes

1. **Sempre faça dry-run primeiro**:
   ```python
   org.reorganizar_projeto(dry_run=True)
   ```

2. **Valide antes de usar em produção**:
   - Execute teste básico após reorganizar
   - Verifique imports dos módulos

3. **Snapshots são automáticos**:
   - Salvos em `.rollback_backups/`
   - Úteis se precisar desfazer

4. **Não execute múltiplas vezes seguidas**:
   - Se já está organizado, não há nada a fazer
   - Sistema detecta automaticamente

---

## 🐛 Troubleshooting

### "Nenhum arquivo para organizar"
✅ **Solução**: Projeto já está organizado! Sem necessidade de ação.

### "Erro ao mover arquivo X"
✅ **Solução**: Arquivo pode estar em uso. Feche programas que o usam e tente novamente.

### "Validação falhou"
✅ **Solução**: Rollback automático foi executado. Verifique logs e tente novamente.

### Imports quebrados após reorganização
✅ **Solução**: O sistema ajusta automaticamente. Se falhou:
1. Verifique se arquivo tem `sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))`
2. Se não, adicione manualmente no início do arquivo

---

## 🎓 Exemplos de Comandos

```python
# Análise rápida
from organizador_projeto import OrganizadorProjeto
org = OrganizadorProjeto()
analise = org.analisar_projeto()
print(f"Total: {analise['total_arquivos']} arquivos")

# Simulação completa
resultado = org.reorganizar_projeto(dry_run=True, confirmar=False)

# Executar de verdade
resultado = org.reorganizar_projeto(dry_run=False, confirmar=True)

# Verificar snapshot
import os
from pathlib import Path
snapshots = sorted(Path('.rollback_backups').glob('reorganizacao_*'))
print(f"Snapshots: {len(snapshots)}")
```

---

## 📚 Documentação Adicional

- **Código fonte**: `organizador_projeto.py`
- **Integração com Luna**: `luna_v3_FINAL_OTIMIZADA.py` (linhas 2735-2818)
- **Testes**: Execute `python organizador_projeto.py` para auto-teste

---

## ✅ Conclusão

O Organizador Inteligente de Projeto:
- ✅ Mantém raiz do projeto limpa e profissional
- ✅ Reorganiza automaticamente com inteligência semântica
- ✅ Ajusta imports em arquivos movidos
- ✅ Valida integridade após mudanças
- ✅ Sistema de rollback automático
- ✅ 100% seguro e testado

**Use regularmente** para manter seu projeto Luna organizado!

---

**Criado por:** Luna V3 (Claude + Anthropic)
**Data:** 2025-10-20
**Versão:** 1.0
