#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 SISTEMA DE GESTÃO SEGURA DE CREDENCIAIS
===========================================

Gerencia credenciais de forma criptografada para automação web.

Características:
- Criptografia AES-256
- Master password
- Armazenamento local seguro
- Fácil integração com Playwright
- Suporte a múltiplas contas
"""

import json
import os
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import getpass


class Cofre:
    """
    Cofre de senhas criptografado com AES-256
    """
    
    def __init__(self, arquivo_cofre: str = "cofre.enc"):
        self.arquivo_cofre = arquivo_cofre
        self.credenciais = {}
        self.cipher = None
        self.master_password = None
    
    def _gerar_chave(self, password: str, salt: bytes) -> bytes:
        """Gera chave de criptografia a partir da master password"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def _criar_cipher(self, password: str, salt: bytes):
        """Cria cipher para criptografia/descriptografia"""
        key = self._gerar_chave(password, salt)
        self.cipher = Fernet(key)
    
    def inicializar(self, master_password: str = None):
        """
        Inicializa cofre (cria novo ou abre existente)
        """
        print("\n🔐 COFRE DE CREDENCIAIS")
        print("=" * 50)
        
        if os.path.exists(self.arquivo_cofre):
            # Cofre existe, pedir master password
            if not master_password:
                master_password = getpass.getpass("🔑 Master Password: ")
            
            try:
                self._abrir_cofre(master_password)
                print("✅ Cofre aberto com sucesso!")
                print(f"📊 {len(self.credenciais)} credenciais carregadas")
            except Exception as e:
                print(f"❌ Erro ao abrir cofre: Master password incorreta ou arquivo corrompido")
                raise ValueError("Master password incorreta")
        else:
            # Criar novo cofre
            print("\n🆕 Criando novo cofre...")
            if not master_password:
                master_password = getpass.getpass("🔑 Crie uma Master Password: ")
                confirmar = getpass.getpass("🔑 Confirme a Master Password: ")
                
                if master_password != confirmar:
                    raise ValueError("❌ Senhas não coincidem!")
            
            self._criar_cofre(master_password)
            print("✅ Cofre criado com sucesso!")
        
        self.master_password = master_password
        print("=" * 50 + "\n")
    
    def _criar_cofre(self, master_password: str):
        """Cria novo cofre vazio"""
        # Gerar salt aleatório
        salt = os.urandom(16)
        
        # Criar cipher
        self._criar_cipher(master_password, salt)
        
        # Dados iniciais vazios
        self.credenciais = {}
        
        # Salvar
        self._salvar_cofre(salt)
    
    def _abrir_cofre(self, master_password: str):
        """Abre cofre existente"""
        with open(self.arquivo_cofre, 'rb') as f:
            # Ler salt (primeiros 16 bytes)
            salt = f.read(16)
            # Ler dados criptografados
            dados_criptografados = f.read()
        
        # Criar cipher com salt
        self._criar_cipher(master_password, salt)
        
        # Descriptografar
        try:
            dados_json = self.cipher.decrypt(dados_criptografados)
            self.credenciais = json.loads(dados_json.decode())
        except Exception as e:
            raise ValueError("Falha na descriptografia")
    
    def _salvar_cofre(self, salt: bytes = None):
        """Salva cofre no disco"""
        if salt is None:
            # Ler salt existente
            with open(self.arquivo_cofre, 'rb') as f:
                salt = f.read(16)
        
        # Serializar credenciais
        dados_json = json.dumps(self.credenciais, indent=2).encode()
        
        # Criptografar
        dados_criptografados = self.cipher.encrypt(dados_json)
        
        # Salvar: salt + dados
        with open(self.arquivo_cofre, 'wb') as f:
            f.write(salt)
            f.write(dados_criptografados)
    
    def adicionar_credencial(self, servico: str, usuario: str, senha: str, extras: dict = None):
        """
        Adiciona credencial ao cofre
        
        Args:
            servico: Nome do serviço (ex: "notion", "gmail")
            usuario: Nome de usuário ou email
            senha: Senha
            extras: Dados adicionais (ex: {"url": "...", "2fa_secret": "..."})
        """
        print(f"\n➕ Adicionando credencial: {servico}")
        
        credencial = {
            "usuario": usuario,
            "senha": senha,
            "extras": extras or {}
        }
        
        self.credenciais[servico] = credencial
        self._salvar_cofre()
        
        print(f"✅ Credencial '{servico}' salva com segurança!")
    
    def obter_credencial(self, servico: str) -> dict:
        """
        Obtém credencial do cofre
        
        Returns:
            {"usuario": "...", "senha": "...", "extras": {...}}
        """
        if servico not in self.credenciais:
            raise KeyError(f"❌ Credencial '{servico}' não encontrada no cofre")
        
        return self.credenciais[servico]
    
    def listar_credenciais(self) -> list:
        """Lista todos os serviços com credenciais"""
        return list(self.credenciais.keys())
    
    def remover_credencial(self, servico: str):
        """Remove credencial do cofre"""
        if servico in self.credenciais:
            del self.credenciais[servico]
            self._salvar_cofre()
            print(f"✅ Credencial '{servico}' removida")
        else:
            print(f"⚠️  Credencial '{servico}' não existe")
    
    def atualizar_credencial(self, servico: str, usuario: str = None, senha: str = None, extras: dict = None):
        """Atualiza credencial existente"""
        if servico not in self.credenciais:
            raise KeyError(f"❌ Credencial '{servico}' não encontrada")
        
        if usuario:
            self.credenciais[servico]["usuario"] = usuario
        if senha:
            self.credenciais[servico]["senha"] = senha
        if extras:
            self.credenciais[servico]["extras"].update(extras)
        
        self._salvar_cofre()
        print(f"✅ Credencial '{servico}' atualizada!")
    
    def exportar_backup(self, arquivo: str, master_password_backup: str = None):
        """
        Exporta backup do cofre (ainda criptografado)
        """
        import shutil
        
        if not master_password_backup:
            master_password_backup = getpass.getpass("🔑 Master Password para backup: ")
        
        if master_password_backup != self.master_password:
            raise ValueError("❌ Master password incorreta!")
        
        shutil.copy2(self.arquivo_cofre, arquivo)
        print(f"✅ Backup criado: {arquivo}")
    
    def mostrar_resumo(self):
        """Mostra resumo do cofre (sem senhas)"""
        print("\n" + "=" * 50)
        print("📊 RESUMO DO COFRE")
        print("=" * 50)
        
        if not self.credenciais:
            print("⚠️  Cofre vazio")
        else:
            print(f"Total de credenciais: {len(self.credenciais)}\n")
            for servico, cred in self.credenciais.items():
                print(f"🔑 {servico}")
                print(f"   └─ Usuário: {cred['usuario']}")
                print(f"   └─ Senha: {'*' * len(cred['senha'])}")
                if cred['extras']:
                    print(f"   └─ Extras: {list(cred['extras'].keys())}")
        
        print("=" * 50 + "\n")


# ============================================================================
# INTERFACE DE LINHA DE COMANDO
# ============================================================================

def menu_principal():
    """Interface de gerenciamento do cofre"""
    
    cofre = Cofre()
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  🔐 COFRE DE CREDENCIAIS                                    ║
║                                                              ║
║  Gerenciamento seguro de senhas com criptografia AES-256   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Inicializar cofre
    try:
        cofre.inicializar()
    except Exception as e:
        print(f"\n❌ Erro ao inicializar cofre: {e}")
        return
    
    # Menu interativo
    while True:
        print("\n" + "=" * 50)
        print("MENU PRINCIPAL")
        print("=" * 50)
        print("1. ➕ Adicionar credencial")
        print("2. 👁️  Ver credencial")
        print("3. 📋 Listar todas")
        print("4. ✏️  Atualizar credencial")
        print("5. 🗑️  Remover credencial")
        print("6. 💾 Exportar backup")
        print("7. 📊 Mostrar resumo")
        print("0. 🚪 Sair")
        print("=" * 50)
        
        escolha = input("\nEscolha: ").strip()
        
        try:
            if escolha == "1":
                # Adicionar
                print("\n➕ ADICIONAR CREDENCIAL")
                servico = input("Nome do serviço (ex: notion, gmail): ").strip()
                usuario = input("Usuário/Email: ").strip()
                senha = getpass.getpass("Senha: ")
                
                # Extras opcionais
                adicionar_extras = input("Adicionar dados extras? (s/n): ").strip().lower()
                extras = {}
                if adicionar_extras == 's':
                    url = input("URL (opcional): ").strip()
                    if url:
                        extras["url"] = url
                    notas = input("Notas (opcional): ").strip()
                    if notas:
                        extras["notas"] = notas
                
                cofre.adicionar_credencial(servico, usuario, senha, extras)
            
            elif escolha == "2":
                # Ver
                print("\n👁️  VER CREDENCIAL")
                servico = input("Nome do serviço: ").strip()
                cred = cofre.obter_credencial(servico)
                
                print("\n" + "=" * 50)
                print(f"Serviço: {servico}")
                print(f"Usuário: {cred['usuario']}")
                print(f"Senha: {cred['senha']}")
                if cred['extras']:
                    print("Extras:")
                    for k, v in cred['extras'].items():
                        print(f"  - {k}: {v}")
                print("=" * 50)
            
            elif escolha == "3":
                # Listar
                print("\n📋 CREDENCIAIS NO COFRE:")
                servicos = cofre.listar_credenciais()
                if servicos:
                    for i, s in enumerate(servicos, 1):
                        print(f"  {i}. {s}")
                else:
                    print("  ⚠️  Nenhuma credencial")
            
            elif escolha == "4":
                # Atualizar
                print("\n✏️  ATUALIZAR CREDENCIAL")
                servico = input("Nome do serviço: ").strip()
                
                usuario = input("Novo usuário (Enter para manter): ").strip()
                senha = getpass.getpass("Nova senha (Enter para manter): ")
                
                cofre.atualizar_credencial(
                    servico,
                    usuario=usuario if usuario else None,
                    senha=senha if senha else None
                )
            
            elif escolha == "5":
                # Remover
                print("\n🗑️  REMOVER CREDENCIAL")
                servico = input("Nome do serviço: ").strip()
                confirmar = input(f"Confirma remoção de '{servico}'? (s/n): ").strip().lower()
                if confirmar == 's':
                    cofre.remover_credencial(servico)
            
            elif escolha == "6":
                # Backup
                print("\n💾 EXPORTAR BACKUP")
                arquivo = input("Nome do arquivo (ex: backup_cofre.enc): ").strip()
                cofre.exportar_backup(arquivo)
            
            elif escolha == "7":
                # Resumo
                cofre.mostrar_resumo()
            
            elif escolha == "0":
                print("\n👋 Até logo!")
                break
            
            else:
                print("❌ Opção inválida")
        
        except KeyboardInterrupt:
            print("\n\n👋 Até logo!")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")


# ============================================================================
# UTILITÁRIO: Adicionar credenciais rapidamente
# ============================================================================

def adicionar_rapido(servico: str, usuario: str, senha: str, master_password: str, extras: dict = None):
    """
    Adiciona credencial rapidamente (útil para scripts)
    """
    cofre = Cofre()
    cofre.inicializar(master_password)
    cofre.adicionar_credencial(servico, usuario, senha, extras)
    print(f"✅ Credencial '{servico}' adicionada!")


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "add":
        # Modo rápido: python cofre_credenciais.py add
        print("Modo rápido de adição")
        master = getpass.getpass("Master Password: ")
        servico = input("Serviço: ")
        usuario = input("Usuário: ")
        senha = getpass.getpass("Senha: ")
        
        adicionar_rapido(servico, usuario, senha, master)
    else:
        # Modo interativo
        menu_principal()
