import json
from pathlib import Path
from cryptography.fernet import Fernet
import os

cofre_dir = Path.home() / ".luna_secrets"
cofre_dir.mkdir(exist_ok=True)

key_file = cofre_dir / ".key"
vault_file = cofre_dir / "vault.enc"

# Carregar ou criar chave
if key_file.exists():
    with open(key_file, 'rb') as f:
        key = f.read()
else:
    key = Fernet.generate_key()
    with open(key_file, 'wb') as f:
        f.write(key)
    os.chmod(str(key_file), 0o600)

cipher = Fernet(key)

# Carregar vault existente ou criar novo
if vault_file.exists():
    with open(vault_file, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = cipher.decrypt(encrypted_data)
    vault = json.loads(decrypted_data)
else:
    vault = {}

# Adicionar credenciais Netflix
vault['netflix'] = {
    'usuario': 'pvnoleto@hotmail.com',
    'senha': 'quize180994',
    'descricao': 'Credenciais Netflix do usuario'
}

# Salvar vault criptografado
vault_json = json.dumps(vault, indent=2)
encrypted_vault = cipher.encrypt(vault_json.encode())
with open(vault_file, 'wb') as f:
    f.write(encrypted_vault)
os.chmod(str(vault_file), 0o600)

print("Credenciais Netflix salvas com seguranca no cofre!")
print(f"Localizacao: {vault_file}")
print(f"Servico: netflix")
print(f"Usuario: pvnoleto@hotmail.com")
print(f"Senha: {'*' * 12} [criptografada]")
