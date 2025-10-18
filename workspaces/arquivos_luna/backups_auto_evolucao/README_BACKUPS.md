# 🗂️ Sistema de Backups - Luna Auto-Evolução

## 📋 Estrutura de Backups

### 1. **Backups do Sistema de Auto-Evolução**
**Localização:** `backups_auto_evolucao/`

Contém backups automáticos criados pelo sistema de auto-evolução quando modificações são feitas no código:

#### Tipos de arquivos:
- **`agente_backup_*.py`** - Backups do agente principal antes de modificações
- **`luna_completo_workspaces_CORRIGIDO.backup_*.py`** - Backups de correções aplicadas
- **`patch_*.py`** - Scripts de correção/patch aplicados
- **`teste_*.py`** - Testes de validação relacionados às modificações

#### Arquivos atuais:
```
backups_auto_evolucao/
├── luna_completo_workspaces_CORRIGIDO.backup_20251015_150523.py
├── luna_completo_workspaces_CORRIGIDO.backup_v2_20251015_150703.py
├── luna_completo_workspaces_CORRIGIDO.backup_v3_FINAL_20251015_151043.py
├── patch_encoding_fix.py
├── patch_encoding_fix_v2.py
├── patch_encoding_fix_v3_FINAL.py
└── teste_encoding_validacao.py
```

### 2. **Backups da Memória Permanente**
**Localização:** `backups_auto_evolucao/backups_memoria/` (estrutura criada)

Para backups futuros da memória permanente exportados manualmente:
- **`memoria_backup_*.json`** - Exportações manuais da memória
- **`memoria_agente.json.bak`** - Backup automático (mantido na raiz por segurança)

---

## 🔧 Como o Sistema Funciona

### Sistema de Auto-Evolução (`sistema_auto_evolucao.py`)

**Configuração padrão:**
```python
dir_backups = "backups_auto_evolucao"
```

**Processo de backup:**
1. Antes de qualquer modificação, cria backup com timestamp
2. Formato: `agente_backup_YYYYMMDD_HHMMSS.py`
3. Salva metadata com motivo da modificação
4. Valida código (sintaxe + imports + execução)
5. Se falhar, faz rollback automático do backup

**Características:**
- ✅ Backup automático antes de modificações
- ✅ Validação completa do código
- ✅ Rollback automático em caso de erro
- ✅ Limpeza inteligente de backups antigos (mantém últimos 10)
- ✅ Zonas protegidas (código crítico não é modificado)
- ✅ Memória de erros (não repete modificações que falharam)

### Sistema de Memória Permanente (`memoria_permanente.py`)

**Backup automático:**
- Arquivo: `memoria_agente.json.bak`
- Criado automaticamente antes de salvar nova versão
- Mantido na raiz para acesso rápido em caso de corrupção

**Backup manual:**
- Função: `exportar_backup(arquivo)`
- Permite exportar toda memória com nome customizado
- Útil antes de operações críticas ou para versionamento

---

## 📝 Regras de Organização

### ✅ O QUE MOVER para `backups_auto_evolucao/`:
- Todos arquivos `*.backup_*.py`
- Scripts `patch_*.py` de correções
- Scripts `teste_*.py` relacionados a correções
- Backups de códigos do agente principal
- Arquivos temporários de validação

### ❌ O QUE NÃO MOVER (manter na raiz):
- `memoria_agente.json.bak` - backup automático da memória (acesso rápido)
- Arquivos principais: `agente_completo_final.py`, `luna_completo*.py`
- Módulos do sistema: `gerenciador_*.py`, `sistema_auto_evolucao.py`
- Configurações: `.env`, `cofre.enc`

---

## 🎯 Boas Práticas

1. **Nunca apague backups automaticamente** - São seu seguro contra erros
2. **Mantenha estrutura organizada** - Um tipo de backup por pasta
3. **Documente modificações importantes** - Use arquivos `.meta` ou `.md`
4. **Teste antes de aplicar** - Sempre valide modificações
5. **Mantenha backup da memória** - É seu cérebro, proteja-o

---

## 🔄 Rotina de Manutenção

### Automática (pelo sistema):
- ✅ Limpeza de backups antigos (mantém últimos 10)
- ✅ Backup antes de cada modificação
- ✅ Validação após cada mudança

### Manual (quando necessário):
- Revisar backups mensalmente
- Exportar backup completo da memória antes de updates grandes
- Documentar modificações importantes

---

## 📊 Status Atual

**Data:** 2025-10-15  
**Backups organizados:** ✅ Todos na pasta correta  
**Sistema funcionando:** ✅ Configurado e operacional  
**Documentação:** ✅ Completa e atualizada

---

**Última atualização:** 15/10/2025 15:30  
**Responsável:** Luna (Sistema de Auto-Evolução)
