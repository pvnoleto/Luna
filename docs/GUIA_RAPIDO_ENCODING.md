# 🚀 Guia Rápido: Encoding no Windows

## ⚡ TL;DR

```python
# ❌ ERRADO (quebra no Windows)
subprocess.run(cmd, text=True)

# ✅ CORRETO
import sys
if sys.platform == 'win32':
    enc = 'cp850'
else:
    enc = 'utf-8'
subprocess.run(cmd, text=True, encoding=enc, errors='replace')
```

## 🎯 Problema

Windows `cmd.exe` retorna **CP850**, não UTF-8!
- `áéíóú` vira `�����`
- `UnicodeDecodeError` ao usar UTF-8

## ✅ Solução

### Método 1: Encoding Específico (Simples)
```python
import sys

enc = 'cp850' if sys.platform == 'win32' else 'utf-8'
subprocess.run(cmd, encoding=enc, errors='replace')
```

### Método 2: Fallback Múltiplo (Robusto)
```python
if sys.platform == 'win32':
    for enc in ['cp850', 'cp1252', 'utf-8']:
        try:
            resultado = subprocess.run(cmd, encoding=enc, errors='replace')
            break
        except UnicodeDecodeError:
            continue
else:
    resultado = subprocess.run(cmd, encoding='utf-8', errors='replace')
```

## 📋 Checklist

- [ ] `import sys` no topo
- [ ] Verificar `sys.platform == 'win32'`
- [ ] Usar `encoding='cp850'` no Windows
- [ ] Sempre incluir `errors='replace'`
- [ ] Testar com: `echo "áéíóú"`

## 🔗 Referências

- Relatório completo: `CORRECAO_ENCODING_RELATORIO.md`
- README: `README_CORRECAO_ENCODING.md`
- Testes: `teste_encoding_validacao.py`

---
**Lembre-se:** Windows ≠ UTF-8! 🪟≠🌍
