import shutil  
from datetime import datetime  
  
ARQUIVO = r"luna_v3_FINAL_OTIMIZADA.py"  
timestamp = datetime.now().strftime("%%Y%%m%%d_%%H%%M%%S")  
backup = f"backups_auto_evolucao/luna_backup_{timestamp}.py"  
shutil.copy2(ARQUIVO, backup)  
print(f"Backup: {backup}")  
  
with open(ARQUIVO, "r", encoding="utf-8") as f:  
    content = f.read()  
  
old = "self.sistema_evolucao = SistemaAutoEvolucao() if AUTO_EVOLUCAO_DISPONIVEL else None"  
new = "self.sistema_evolucao = SistemaAutoEvolucao(arquivo_alvo=__file__, dir_backups=\"backups_auto_evolucao\") if AUTO_EVOLUCAO_DISPONIVEL else None"  
  
if old in content:  
    content = content.replace(old, new)  
    with open(ARQUIVO, "w", encoding="utf-8") as f:  
        f.write(content)  
    print("Corrigido!")  
else:  
    print("Nao encontrado")  
