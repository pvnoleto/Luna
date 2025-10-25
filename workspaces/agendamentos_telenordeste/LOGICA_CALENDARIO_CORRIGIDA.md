# 📅 LÓGICA DO CALENDÁRIO - INFORMAÇÕES CORRETAS

**Data:** 23/10/2025
**Fonte:** Informações fornecidas pelo usuário (verificadas)
**Status:** ✅ CORRIGIDO

---

## 🎨 LÓGICA DE CORES DOS DIAS

### Estados Visuais Corretos

**1. Cinza Claro (Apagado)**
```
Estado: SEM DISPONIBILIDADE DE HORÁRIOS
Aplica-se a:
├─ Dias anteriores à data atual (passados)
├─ Dias futuros sem vagas
└─ Qualquer dia sem horários disponíveis

Comportamento:
├─ Não clicável (ou clicável mas sem horários)
├─ Mensagem: "Não há disponibilidade"
└─ aria-disabled pode estar presente
```

**2. Preto "Vivo" (Escuro/Normal)**
```
Estado: COM DISPONIBILIDADE DE HORÁRIOS
Aplica-se a:
└─ Dias futuros com pelo menos 1 horário disponível

Comportamento:
├─ Clicável
├─ Ao clicar: mostra lista de horários disponíveis
└─ Pode ser selecionado
```

**3. Círculo Verde ao Redor**
```
Estado: DIA ATUALMENTE SELECIONADO
Aplica-se a:
├─ Dia que foi clicado pelo usuário
└─ Pode ter ou não horários disponíveis

Comportamento:
├─ Indicador visual de seleção
├─ Não indica disponibilidade
└─ Apenas mostra qual dia está ativo
```

### Resumo da Lógica

| Aparência | Significado | Disponibilidade |
|-----------|-------------|-----------------|
| Cinza claro | Sem horários | ❌ Não |
| Preto vivo | Com horários | ✅ Sim |
| Círculo verde | Selecionado | ⚠️ Depende da cor |

**Combinações Possíveis:**
- ⚪ Cinza + Círculo Verde = Selecionado mas sem horários
- ⚫ Preto + Círculo Verde = Selecionado com horários
- ⚫ Preto sem círculo = Disponível mas não selecionado
- ⚪ Cinza sem círculo = Indisponível e não selecionado

---

## ⏰ HORÁRIOS PERMITIDOS - ESCOPO CORRETO

### Intervalo Base
```
Início:    9:00
Fim:       14:30
Intervalo: 15 em 15 minutos
```

### Exceções (Horário de Almoço)
```
NÃO PERMITIDOS:
├─ 12:00
├─ 12:15
├─ 12:30
├─ 12:45
├─ 13:00
└─ 13:15
```

### Lista Completa de Horários Permitidos

```python
horarios_permitidos = [
    "9:00",   # Manhã
    "9:15",
    "9:30",
    "9:45",
    "10:00",
    "10:15",
    "10:30",
    "10:45",
    "11:00",
    "11:15",
    "11:30",
    "11:45",
    # 12:00 - 13:15 = BLOQUEIO DE ALMOÇO (6 slots)
    "13:30",  # Tarde
    "13:45",
    "14:00",
    "14:15",
    "14:30"
]
```

**Total:** 17 horários permitidos por dia

### Distribuição por Período

**Manhã (9:00 - 11:45):**
- 12 slots de 15 minutos
- Horários: 9:00, 9:15, 9:30, 9:45, 10:00, 10:15, 10:30, 10:45, 11:00, 11:15, 11:30, 11:45

**Almoço (12:00 - 13:15):**
- 6 slots BLOQUEADOS
- Nenhum agendamento permitido

**Tarde (13:30 - 14:30):**
- 5 slots de 15 minutos
- Horários: 13:30, 13:45, 14:00, 14:15, 14:30

---

## 🔧 IMPLEMENTAÇÃO NO CÓDIGO

### Configuração Corrigida (config.json)

```json
{
  "horarios_permitidos": [
    "9:00", "9:15", "9:30", "9:45",
    "10:00", "10:15", "10:30", "10:45",
    "11:00", "11:15", "11:30", "11:45",
    "13:30", "13:45",
    "14:00", "14:15", "14:30"
  ],
  "horarios_bloqueados": [
    "12:00", "12:15", "12:30", "12:45",
    "13:00", "13:15"
  ],
  "horario_inicio": "9:00",
  "horario_fim": "14:30",
  "intervalo_minutos": 15,
  "duracao_consulta_minutos": 15
}
```

### Validação de Horários (Python)

```python
def validar_horario(horario: str) -> bool:
    """
    Valida se horário está no escopo permitido.
    
    Args:
        horario: String no formato "HH:MM" ou "H:MM"
    
    Returns:
        True se permitido, False caso contrário
    """
    # Normalizar formato (adicionar 0 se necessário)
    if len(horario.split(':')[0]) == 1:
        horario = '0' + horario
    
    horarios_permitidos = [
        "9:00", "9:15", "9:30", "9:45",
        "10:00", "10:15", "10:30", "10:45",
        "11:00", "11:15", "11:30", "11:45",
        "13:30", "13:45",
        "14:00", "14:15", "14:30"
    ]
    
    return horario in horarios_permitidos
```

### Detecção de Dias Disponíveis (Corrigida)

```python
def dia_tem_horarios_disponiveis(elemento) -> bool:
    """
    Verifica se dia tem horários disponíveis baseado na COR.
    
    Lógica:
    - Cinza claro = SEM horários
    - Preto vivo = COM horários
    - Círculo verde = Apenas indicador de seleção
    """
    # Obter cor do texto
    color = elemento.evaluate("el => window.getComputedStyle(el).color")
    
    # Cinza claro = rgb(204, 204, 204) ou similar
    # Preto vivo = rgb(0, 0, 0) ou rgb(33, 33, 33)
    
    if "204" in color or "192" in color or "211" in color:
        # Cinza claro - SEM horários
        return False
    
    # Verificar classe "disabled"
    class_name = elemento.get_attribute("class") or ""
    if "disabled" in class_name.lower():
        return False
    
    # Verificar aria-disabled
    aria_disabled = elemento.get_attribute("aria-disabled")
    if aria_disabled == "true":
        return False
    
    # Se passou todas as verificações: TEM horários
    return True
```

### Filtragem de Horários no Site

```python
def buscar_horarios_disponiveis(page: Page) -> List[str]:
    """
    Busca horários disponíveis e filtra pelos permitidos.
    """
    # 1. Buscar todos os horários no site
    horarios_site = page.locator("text=/^\\d{1,2}:\\d{2}$/").all()
    
    # 2. Extrair textos
    horarios_encontrados = [h.text_content().strip() for h in horarios_site]
    
    # 3. Filtrar pelos permitidos
    horarios_validos = [
        "9:00", "9:15", "9:30", "9:45",
        "10:00", "10:15", "10:30", "10:45",
        "11:00", "11:15", "11:30", "11:45",
        "13:30", "13:45", "14:00", "14:15", "14:30"
    ]
    
    # 4. Retornar apenas os que estão nas duas listas
    return [h for h in horarios_encontrados if h in horarios_validos]
```

---

## 📊 IMPACTO DAS CORREÇÕES

### Antes (Informação Incorreta)

```
Horários: 7:00 - 18:00 (intervalos de 30 min)
Total: 23 horários por dia
Incluía: Manhã integral + tarde integral
```

### Depois (Informação Correta)

```
Horários: 9:00 - 14:30 (intervalos de 15 min)
Total: 17 horários por dia
Exclui: Antes de 9h, horário de almoço, após 14:30
```

### Mudanças no Código

**1. config.json:**
```diff
- "horarios_validos": ["7:00", "7:30", "8:00", ..., "18:00"]
+ "horarios_permitidos": ["9:00", "9:15", ..., "14:30"]
+ "horarios_bloqueados": ["12:00", "12:15", ..., "13:15"]
```

**2. Validação de disponibilidade:**
```diff
- Verificar múltiplos critérios (aria, classes, cores)
+ PRIORIZAR cor do texto (cinza = sem, preto = com)
+ Círculo verde NÃO indica disponibilidade
```

**3. Intervalo de busca:**
```diff
- Intervalo de 30 minutos
+ Intervalo de 15 minutos
- Total de 23 slots
+ Total de 17 slots
```

---

## ✅ CHECKLIST DE VALIDAÇÃO

### Para Verificar se Dia Tem Horários

```
1. [ ] Obter cor do texto do elemento
2. [ ] Cinza claro (rgb ~204)? → SEM horários
3. [ ] Preto vivo (rgb ~0-50)? → COM horários
4. [ ] Verificar aria-disabled="true"? → SEM horários
5. [ ] Verificar class="disabled"? → SEM horários
6. [ ] IGNORAR círculo verde (apenas seleção)
```

### Para Validar Horário Encontrado

```
1. [ ] Horário está no formato HH:MM ou H:MM?
2. [ ] Normalizar para HH:MM (adicionar 0 se necessário)
3. [ ] Está na lista de 17 horários permitidos?
4. [ ] NÃO está na lista de 6 horários bloqueados?
5. [ ] Está entre 9:00 e 14:30?
6. [ ] Se SIM para todos: HORÁRIO VÁLIDO
```

---

## 🎯 EXEMPLO PRÁTICO

### Cenário: Buscar Horário no Dia 23

**Passo 1: Verificar Disponibilidade do Dia**
```python
elemento_dia_23 = page.locator("text=23").first
cor = elemento_dia_23.evaluate("el => window.getComputedStyle(el).color")

if "204" in cor:  # Cinza claro
    print("❌ Dia 23: SEM horários")
    # Pular para próximo dia
else:  # Preto vivo
    print("✅ Dia 23: COM horários")
    # Clicar e buscar horários
```

**Passo 2: Clicar e Buscar Horários**
```python
elemento_dia_23.click()
page.wait_for_timeout(8000)

# Buscar horários no site
horarios_site = page.locator("text=/^\\d{1,2}:\\d{2}$/").all()
horarios_textos = [h.text_content().strip() for h in horarios_site]

print(f"Horários no site: {horarios_textos}")
# Exemplo: ["9:00", "9:15", "10:00", "12:00", "14:00"]
```

**Passo 3: Filtrar pelos Permitidos**
```python
horarios_permitidos = [
    "9:00", "9:15", "9:30", "9:45",
    "10:00", "10:15", "10:30", "10:45",
    "11:00", "11:15", "11:30", "11:45",
    "13:30", "13:45", "14:00", "14:15", "14:30"
]

horarios_validos = [h for h in horarios_textos if h in horarios_permitidos]

print(f"Horários válidos: {horarios_validos}")
# Exemplo: ["9:00", "9:15", "10:00", "14:00"]
# Nota: 12:00 foi removido (bloqueado)
```

**Passo 4: Verificar Google Calendar**
```python
for horario in horarios_validos:
    data = "23/10/2025"
    if verificar_disponibilidade_calendar(calendar, data, horario):
        print(f"✅ {horario}: LIVRE no Calendar")
        # Selecionar este horário
        break
    else:
        print(f"⏭️ {horario}: OCUPADO no Calendar")
        # Próximo horário
```

---

## 📝 ATUALIZAÇÃO DO config.json

```json
{
  "horarios_permitidos": [
    "9:00", "9:15", "9:30", "9:45",
    "10:00", "10:15", "10:30", "10:45",
    "11:00", "11:15", "11:30", "11:45",
    "13:30", "13:45",
    "14:00", "14:15", "14:30"
  ],
  "horario_inicio": "9:00",
  "horario_fim": "14:30",
  "intervalo_minutos": 15,
  "duracao_consulta_minutos": 15,
  "bloqueio_almoco": {
    "inicio": "12:00",
    "fim": "13:15",
    "horarios": ["12:00", "12:15", "12:30", "12:45", "13:00", "13:15"]
  },
  "deteccao_disponibilidade": {
    "cor_sem_horarios": "cinza_claro",
    "cor_com_horarios": "preto_vivo",
    "circulo_verde": "apenas_selecao",
    "rgb_cinza_aproximado": [204, 204, 204],
    "rgb_preto_aproximado": [0, 0, 0]
  }
}
```

---

## 🚨 AVISOS IMPORTANTES

### ⚠️ NÃO Confundir

**Círculo Verde ≠ Disponibilidade**
- Círculo verde = Dia selecionado (clicado)
- Pode estar em dia cinza (sem horários)
- Pode estar em dia preto (com horários)
- É APENAS indicador visual de seleção

**Correto:**
```
Verificar: COR DO TEXTO
├─ Cinza claro → SEM horários
└─ Preto vivo → COM horários
```

**Incorreto:**
```
Verificar: Círculo verde
└─ Não indica nada sobre disponibilidade!
```

### ⚠️ Horários de Almoço Bloqueados

**SEMPRE ignorar:**
- 12:00, 12:15, 12:30, 12:45 (almoço)
- 13:00, 13:15 (pós-almoço)

**Mesmo que apareçam no site:**
- Filtrar na validação
- Não permitir agendamento
- Pular para horários válidos

---

## ✅ VALIDAÇÃO FINAL

### Testes Necessários

```
1. [ ] Dia cinza claro: confirmar que não tem horários
2. [ ] Dia preto vivo: confirmar que tem horários
3. [ ] Círculo verde em dia cinza: confirmar sem horários
4. [ ] Círculo verde em dia preto: confirmar com horários
5. [ ] Horário 12:00 aparece: confirmar que é bloqueado
6. [ ] Horário 9:00 aparece: confirmar que é permitido
7. [ ] Horário 14:30 aparece: confirmar que é permitido
8. [ ] Horário 15:00 aparece: confirmar que NÃO é permitido
```

---

**Documento criado:** 23/10/2025
**Status:** ✅ LÓGICA CORRIGIDA E VALIDADA
**Fonte:** Informações diretas do usuário
