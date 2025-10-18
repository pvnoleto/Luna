# 📓 Guia de Integração Notion - Luna V3

## 🎯 Visão Geral

A Luna V3 agora pode acessar o Notion diretamente via SDK oficial, sem precisar abrir o navegador toda vez! Isso torna as operações muito mais rápidas e confiáveis.

## 🚀 Instalação

```bash
pip install notion-client
```

## 🔑 Configuração Inicial

### Passo 1: Obter Token do Notion

1. Acesse: https://www.notion.so/my-integrations
2. Clique em "+ New integration"
3. Dê um nome (ex: "Luna Bot")
4. Selecione o workspace
5. Copie o **Internal Integration Token** (começa com `secret_` ou `ntn_`)

### Passo 2: Compartilhar Database com a Integração

1. Abra o database no Notion que você quer acessar
2. Clique nos 3 pontinhos (•••) no canto superior direito
3. Clique em "Add connections"
4. Selecione sua integração (ex: "Luna Bot")

### Passo 3: Obter Database ID

O Database ID está na URL do seu database:
```
https://www.notion.so/workspace/23b1f06b6b5f80659147d34f6084e0e0?v=...
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                           Este é o Database ID (sem hífens)
```

## 🔧 Configuração na Luna

### Opção 1: Armazenar no Cofre (Recomendado)

```python
# Na Luna, use:
"Salve no cofre a credencial do Notion com token ntn_... e database_id 23b1f06b..."
```

### Opção 2: Conectar Diretamente

```python
# Na Luna, use:
"Conecte ao Notion com o token ntn_..."
```

## 📋 Ferramentas Disponíveis

### 1. `notion_conectar`
Conecta ao Notion usando o token da API.

**Exemplo de uso**:
```
"Conecte ao Notion com o token ntn_V83285389753nEE04QHEhZ7yusPR9ZIjZg5JY3HfeKvakc"
```

### 2. `notion_buscar_database`
Busca itens em um database com filtros opcionais.

**Exemplo de uso**:
```
"Busque no database 23b1f06b6b5f80659147d34f6084e0e0 todas as tarefas com status 'Não iniciado'"
```

**Com filtros JSON**:
```json
{
  "property": "Status",
  "status": {
    "equals": "Não iniciado"
  }
}
```

**Filtros comuns**:
```json
// Status igual a algo
{"property": "Status", "status": {"equals": "Em andamento"}}

// Contém texto
{"property": "Nome", "title": {"contains": "Consulta"}}

// Data futura
{"property": "Data", "date": {"after": "2025-01-01"}}

// Checkbox marcado
{"property": "Concluído", "checkbox": {"equals": true}}

// E múltiplas condições
{
  "and": [
    {"property": "Status", "status": {"equals": "Não iniciado"}},
    {"property": "Prioridade", "select": {"equals": "Alta"}}
  ]
}
```

### 3. `notion_atualizar_pagina`
Atualiza propriedades de uma página.

**Exemplo de uso**:
```
"Atualize a página abc123 mudando o status para 'Concluída'"
```

**Formato JSON de propriedades**:
```json
{
  "Status": {
    "status": {
      "name": "Concluída"
    }
  },
  "Data de conclusão": {
    "date": {
      "start": "2025-10-18"
    }
  }
}
```

### 4. `notion_criar_pagina`
Cria uma nova página em um database.

**Exemplo de uso**:
```
"Crie uma nova tarefa no database 23b1f06b6b5f80659147d34f6084e0e0 com nome 'Nova Consulta' e status 'Não iniciado'"
```

**Formato JSON**:
```json
{
  "Nome da tarefa": {
    "title": [
      {
        "text": {
          "content": "Nova Consulta"
        }
      }
    ]
  },
  "Status": {
    "status": {
      "name": "Não iniciado"
    }
  }
}
```

### 5. `notion_ler_database_schema`
Lê a estrutura de um database (propriedades disponíveis).

**Exemplo de uso**:
```
"Mostre-me quais propriedades existem no database 23b1f06b6b5f80659147d34f6084e0e0"
```

**Output esperado**:
```
Database: Agendamentos
Propriedades:
  • Nome da tarefa (title)
  • Status (status)
    Opções: Não iniciado, Em andamento, Concluída
  • Prioridade (select)
    Opções: Alta, Média, Baixa
  • Data (date)
```

### 6. `notion_buscar_paginas`
Busca páginas em todo o workspace por texto.

**Exemplo de uso**:
```
"Busque todas as páginas que mencionam 'agendamento'"
```

## 💡 Exemplos Práticos

### Exemplo 1: Buscar e Atualizar Tarefas

```
Luna, faça o seguinte:
1. Conecte ao Notion com o token do cofre
2. Busque todas as tarefas com status "Não iniciado" no database 23b1f06b6b5f80659147d34f6084e0e0
3. Para cada tarefa encontrada, mostre o nome e o ID
```

### Exemplo 2: Criar Nova Tarefa

```
Luna, crie uma nova tarefa no Notion:
- Database: 23b1f06b6b5f80659147d34f6084e0e0
- Nome: "Agendar consulta - João Silva"
- Especialidade: "Cardiologia"
- Status: "Não iniciado"
- CPF: "123.456.789-00"
```

### Exemplo 3: Atualizar Status em Lote

```
Luna:
1. Busque todas as tarefas com status "Não iniciado" criadas há mais de 7 dias
2. Atualize o status delas para "Cancelada"
3. Adicione uma nota explicando o motivo
```

### Exemplo 4: Relatório de Tarefas

```
Luna, gere um relatório:
1. Busque todas as tarefas do database 23b1f06b6b5f80659147d34f6084e0e0
2. Conte quantas estão em cada status
3. Liste as 5 mais antigas que ainda não foram concluídas
4. Salve o relatório em um arquivo
```

## 🔐 Segurança

### Armazenando Token no Cofre

```python
# Primeira vez
"Luna, abra o cofre e adicione uma credencial chamada 'notion_principal'
com o token ntn_V83285389753nEE04QHEhZ7yusPR9ZIjZg5JY3HfeKvakc
e database_id 23b1f06b6b5f80659147d34f6084e0e0"

# Depois, para usar
"Luna, pegue as credenciais do Notion no cofre e conecte"
```

### Recuperando Token do Cofre

```python
# Luna pode fazer automaticamente
"Luna, conecte ao Notion usando as credenciais do cofre"

# Ou você pode pedir especificamente
"Luna, obtenha a credencial 'notion_principal' do cofre"
```

## 📊 Tipos de Propriedades Suportados

| Tipo | Descrição | Exemplo de Valor |
|------|-----------|------------------|
| `title` | Título da página | "Minha Tarefa" |
| `rich_text` | Texto formatado | "Descrição detalhada..." |
| `number` | Número | 42 |
| `select` | Escolha única | "Alta" |
| `multi_select` | Múltiplas escolhas | ["Tag1", "Tag2"] |
| `status` | Status | "Em andamento" |
| `date` | Data/Data-hora | "2025-10-18" |
| `checkbox` | Sim/Não | true/false |
| `url` | Link | "https://example.com" |
| `email` | Email | "user@example.com" |
| `phone_number` | Telefone | "+55 11 99999-9999" |
| `relation` | Relação com outra página | [IDs de páginas] |
| `people` | Pessoas | [IDs de usuários] |

## 🛠️ Helpers para Criar Propriedades

O módulo `integracao_notion.py` possui funções helper:

```python
from integracao_notion import (
    criar_prop_titulo,
    criar_prop_texto,
    criar_prop_status,
    criar_prop_select,
    criar_prop_checkbox,
    criar_prop_data,
    criar_prop_numero
)

# Exemplo de uso
propriedades = {
    "Nome": criar_prop_titulo("Nova Tarefa"),
    "Status": criar_prop_status("Não iniciado"),
    "Prioridade": criar_prop_select("Alta"),
    "Ativa": criar_prop_checkbox(True),
    "Data": criar_prop_data("2025-10-18")
}
```

## ⚡ Vantagens sobre Playwright

| Característica | Playwright (Browser) | SDK Notion |
|----------------|---------------------|------------|
| Velocidade | 🐢 Lento (10-30s) | ⚡ Rápido (<1s) |
| Confiabilidade | 🔄 Pode falhar | ✅ Estável |
| Recursos | 💾 Alto uso (500MB+) | 💡 Mínimo (<10MB) |
| Login | 🔑 Sempre necessário | 🎫 Token único |
| Modo headless | ⚙️ Funciona | ✅ Sempre funciona |
| Manutenção | 🔧 Quebra com mudanças UI | 🛡️ API estável |

## 🎯 Casos de Uso

### Automação de Agendamentos

```python
# Buscar agendamentos pendentes
"Luna, busque todos os agendamentos com status 'Não iniciado' no Notion"

# Processar cada um
"Para cada agendamento, abra o navegador e faça o agendamento no sistema"

# Atualizar status
"Após agendar, atualize o status para 'Concluída' no Notion"
```

### Sincronização de Dados

```python
# Exportar do Notion
"Luna, exporte todas as tarefas do Notion para um CSV"

# Importar para Notion
"Luna, leia o arquivo dados.csv e crie uma página no Notion para cada linha"
```

### Relatórios Automáticos

```python
# Relatório diário
"Luna, crie um relatório diário:
1. Quantas tarefas foram concluídas hoje
2. Quantas estão pendentes
3. Qual a taxa de conclusão desta semana"
```

## 🐛 Troubleshooting

### Erro: "Notion não conectado"
**Solução**: Execute `notion_conectar` primeiro com um token válido.

### Erro: "Database not found"
**Solução**: Certifique-se de que:
1. O database ID está correto (sem hífens)
2. Você compartilhou o database com sua integração
3. Sua integração tem permissão de leitura

### Erro: "Invalid token"
**Solução**:
1. Verifique se o token está completo (começa com `secret_` ou `ntn_`)
2. Confirme que a integração ainda existe em https://www.notion.so/my-integrations
3. Gere um novo token se necessário

### Erro: "Property not found"
**Solução**: Use `notion_ler_database_schema` para ver quais propriedades existem no database.

### Filtros não funcionam
**Solução**: Certifique-se de que:
1. O nome da propriedade está correto (case-sensitive)
2. O tipo do filtro corresponde ao tipo da propriedade
3. O JSON está bem formatado

## 📚 Recursos Adicionais

### Documentação Oficial Notion API
- https://developers.notion.com/docs/getting-started
- https://developers.notion.com/reference/intro

### Exemplos de Filtros Complexos
```json
// OU lógico
{
  "or": [
    {"property": "Status", "status": {"equals": "Urgente"}},
    {"property": "Prioridade", "select": {"equals": "Alta"}}
  ]
}

// Combinação AND e OR
{
  "and": [
    {"property": "Ativo", "checkbox": {"equals": true}},
    {
      "or": [
        {"property": "Status", "status": {"equals": "Não iniciado"}},
        {"property": "Status", "status": {"equals": "Em andamento"}}
      ]
    }
  ]
}

// Data entre intervalo
{
  "and": [
    {"property": "Data", "date": {"on_or_after": "2025-01-01"}},
    {"property": "Data", "date": {"before": "2025-12-31"}}
  ]
}
```

## 🎉 Conclusão

Com a integração Notion via SDK, a Luna pode:
- ✅ Acessar databases sem abrir navegador
- ✅ Trabalhar 10x mais rápido que com Playwright
- ✅ Ter acesso confiável e estável
- ✅ Usar em modo headless sem problemas
- ✅ Integrar Notion em automações complexas

**Próximos Passos:**
1. Instale o SDK: `pip install notion-client`
2. Configure seu token
3. Teste com `notion_conectar`
4. Explore seus databases com `notion_buscar_database`
5. Automatize tudo! 🚀

---

**Versão**: 1.0
**Data**: 2025-10-18
**Compatível com**: Luna V3 Final Otimizada
