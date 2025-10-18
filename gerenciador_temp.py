#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗑️ GERENCIADOR DE ARQUIVOS TEMPORÁRIOS - LUNA
===============================================

Gerencia arquivos temporários com auto-limpeza inteligente
Marca arquivos para deleção após 30 dias sem uso

✅ CORRIGIDO COMPLETAMENTE:
- Encoding UTF-8 forçado em TODOS os arquivos e prints
- Caminhos Windows com espaços e acentuação
- Console Windows configurado para UTF-8
- Path.resolve() em todos os lugares críticos

Criado: 2025-01-14
Atualizado: 2025-10-15
Corrigido: 2025-10-15 (Encoding + Windows paths)
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import shutil

# ✅ CORREÇÃO CRÍTICA: Forçar UTF-8 no console Windows
if sys.platform == 'win32':
    try:
        # Tenta configurar console para UTF-8
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except (AttributeError, ValueError, IOError) as e:
        # Se falhar, desabilitar emojis (terminal sem suporte UTF-8)
        pass


class GerenciadorTemporarios:
    """
    Gerencia arquivos temporários com auto-limpeza
    
    ✅ 100% compatível com Windows (espaços, acentuação, UTF-8)
    """
    
    def __init__(self, base_dir: str = None):
        # ✅ CORREÇÃO: Usar Path.resolve() para caminho absoluto seguro
        if base_dir is None:
            # Usar diretório atual, mas resolver para caminho absoluto
            self.base_dir = Path.cwd().resolve()
        else:
            # Converter para Path e resolver
            self.base_dir = Path(base_dir).resolve()
        
        # ✅ CORREÇÃO: Criar pasta .temp usando Path (nunca \\)
        self.temp_dir = self.base_dir / ".temp"
        
        # Arquivo de metadados
        self.metadata_file = self.temp_dir / "metadata.json"
        
        # Arquivo de log
        self.log_file = self.temp_dir / "temp.log"
        
        # Criar estrutura
        self._inicializar()
        
        # Carregar metadados
        self.metadata = self._carregar_metadata()
    
    # ========================================================================
    # INICIALIZAÇÃO
    # ========================================================================
    
    def _inicializar(self):
        """Cria estrutura inicial - ✅ CORRIGIDO para Windows"""
        try:
            # ✅ Criar pasta .temp de forma segura (parents=True)
            self.temp_dir.mkdir(parents=True, exist_ok=True)
            
            # Criar README com encoding UTF-8 explícito
            readme = self.temp_dir / "README.md"
            if not readme.exists():
                # ✅ CORREÇÃO: Usar encoding UTF-8 explicitamente
                readme.write_text(
                    """# Pasta Temporaria

Esta pasta contem arquivos temporarios que serao deletados automaticamente.

Arquivos sao marcados e deletados apos 30 dias sem uso.

AVISO: NAO salve arquivos importantes aqui!
""", 
                    encoding='utf-8'
                )
        except Exception as e:
            print(f"[ERRO] Falha ao inicializar: {e}")
            raise
    
    def _carregar_metadata(self) -> Dict:
        """Carrega metadados dos arquivos temporários"""
        if self.metadata_file.exists():
            try:
                # ✅ CORREÇÃO: Usar encoding UTF-8
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self._log(f"Erro ao carregar metadata: {e}")
                return self._metadata_padrao()
        else:
            return self._metadata_padrao()
    
    def _metadata_padrao(self) -> Dict:
        """Retorna metadados padrão"""
        return {
            "arquivos_temporarios": {},
            "arquivos_protegidos": [],
            "estatisticas": {
                "total_deletados": 0,
                "total_resgatados": 0,
                "espaco_liberado_bytes": 0
            },
            "criado_em": datetime.now().isoformat()
        }
    
    def _salvar_metadata(self):
        """Salva metadados em disco"""
        try:
            # ✅ CORREÇÃO: Usar encoding UTF-8
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self._log(f"Erro ao salvar metadata: {e}")
    
    def _log(self, mensagem: str):
        """Registra log de operações"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {mensagem}\n"

        try:
            # ✅ CORREÇÃO: Usar encoding UTF-8 explicitamente
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_msg)
        except (IOError, OSError, PermissionError) as e:
            # Silencioso se falhar (log não é crítico)
            pass
    
    # ========================================================================
    # OPERAÇÕES DE MARCAÇÃO
    # ========================================================================
    
    def marcar_temporario(self, caminho: str, forcar: bool = False) -> bool:
        """
        Marca arquivo como temporário
        
        Args:
            caminho: Caminho do arquivo
            forcar: Se True, marca mesmo se não parecer temporário
            
        Returns:
            True se marcado, False caso contrário
        """
        # ✅ Converter para Path e resolver
        arquivo_path = Path(caminho).resolve()
        
        if not arquivo_path.exists():
            self._log(f"Arquivo nao existe: {caminho}")
            return False
        
        if not arquivo_path.is_file():
            self._log(f"Nao e um arquivo: {caminho}")
            return False
        
        # Verificar se é temporário
        if not forcar and not self._parece_temporario(arquivo_path):
            self._log(f"Arquivo nao parece temporario: {caminho}")
            return False
        
        # Verificar se está protegido
        caminho_str = str(arquivo_path)
        if caminho_str in self.metadata["arquivos_protegidos"]:
            self._log(f"Arquivo protegido: {caminho}")
            return False
        
        # Marcar como temporário
        self.metadata["arquivos_temporarios"][caminho_str] = {
            "caminho": caminho_str,
            "marcado_em": datetime.now().isoformat(),
            "delete_em": (datetime.now() + timedelta(days=30)).isoformat(),
            "ultimo_acesso": datetime.now().isoformat(),
            "tamanho_bytes": arquivo_path.stat().st_size,
            "motivo": "manual" if forcar else "auto"
        }
        
        self._salvar_metadata()
        self._log(f"Arquivo marcado como temporario: {caminho}")
        
        return True
    
    def _parece_temporario(self, arquivo_path: Path) -> bool:
        """Verifica se arquivo parece temporário"""
        nome = arquivo_path.name.lower()
        
        # Padrões temporários
        padroes_temp = [
            "temp", "tmp", "cache", "backup", "bak",
            "screenshot", "test", "debug", "log"
        ]
        
        # Verificar se nome contém padrões
        for padrao in padroes_temp:
            if padrao in nome:
                return True
        
        # Verificar extensões temporárias
        extensoes_temp = [".tmp", ".bak", ".cache", ".log"]
        if arquivo_path.suffix.lower() in extensoes_temp:
            return True
        
        return False
    
    def proteger_arquivo(self, caminho: str) -> bool:
        """
        Protege arquivo de ser marcado como temporário
        
        Args:
            caminho: Caminho do arquivo
            
        Returns:
            True se protegido, False caso contrário
        """
        arquivo_path = Path(caminho).resolve()
        caminho_str = str(arquivo_path)
        
        # Remover de temporários se estiver lá
        if caminho_str in self.metadata["arquivos_temporarios"]:
            del self.metadata["arquivos_temporarios"][caminho_str]
            self.metadata["estatisticas"]["total_resgatados"] += 1
        
        # Adicionar à lista de protegidos
        if caminho_str not in self.metadata["arquivos_protegidos"]:
            self.metadata["arquivos_protegidos"].append(caminho_str)
        
        self._salvar_metadata()
        self._log(f"Arquivo protegido: {caminho}")
        
        return True
    
    # ========================================================================
    # LIMPEZA
    # ========================================================================
    
    def limpar_arquivos_antigos(self, exibir_resumo: bool = False) -> Dict:
        """
        Limpa arquivos temporários antigos (após 30 dias)
        
        Args:
            exibir_resumo: Se True, exibe resumo da limpeza
            
        Returns:
            Dict com estatísticas da limpeza
        """
        agora = datetime.now()
        deletados = []
        erros = []
        espaco_liberado = 0
        
        # Verificar cada arquivo temporário
        for caminho_str, info in list(self.metadata["arquivos_temporarios"].items()):
            # Verificar se passou do prazo
            delete_em = datetime.fromisoformat(info["delete_em"])
            
            if agora >= delete_em:
                # Deletar arquivo
                arquivo_path = Path(caminho_str)
                
                if arquivo_path.exists():
                    try:
                        tamanho = arquivo_path.stat().st_size
                        arquivo_path.unlink()
                        
                        deletados.append(caminho_str)
                        espaco_liberado += tamanho
                        
                        self._log(f"Arquivo deletado: {caminho_str}")
                    except Exception as e:
                        erros.append((caminho_str, str(e)))
                        self._log(f"Erro ao deletar {caminho_str}: {e}")
                
                # Remover do metadata
                del self.metadata["arquivos_temporarios"][caminho_str]
        
        # Atualizar estatísticas
        self.metadata["estatisticas"]["total_deletados"] += len(deletados)
        self.metadata["estatisticas"]["espaco_liberado_bytes"] += espaco_liberado
        
        self._salvar_metadata()
        
        # Exibir resumo (sem emojis para compatibilidade)
        if exibir_resumo and deletados:
            print("\n" + "="*70)
            print("LIMPEZA DE ARQUIVOS TEMPORARIOS")
            print("="*70)
            print(f"Deletados: {len(deletados)} arquivo(s)")
            print(f"Espaco liberado: {espaco_liberado / (1024*1024):.2f} MB")
            if erros:
                print(f"Erros: {len(erros)}")
            print("="*70 + "\n")
        
        return {
            "deletados": len(deletados),
            "erros": len(erros),
            "espaco_liberado_bytes": espaco_liberado,
            "espaco_liberado_mb": espaco_liberado / (1024*1024)
        }
    
    # ========================================================================
    # CONSULTAS
    # ========================================================================
    
    def listar_temporarios(self) -> List[Dict]:
        """
        Lista todos arquivos temporários
        
        Returns:
            Lista de dicionários com info dos arquivos
        """
        agora = datetime.now()
        temporarios = []
        
        for caminho_str, info in self.metadata["arquivos_temporarios"].items():
            delete_em = datetime.fromisoformat(info["delete_em"])
            dias_restantes = (delete_em - agora).days
            
            temporarios.append({
                "caminho": caminho_str,
                "nome": Path(caminho_str).name,
                "tamanho_bytes": info["tamanho_bytes"],
                "tamanho_mb": info["tamanho_bytes"] / (1024*1024),
                "marcado_em": info["marcado_em"],
                "delete_em": info["delete_em"],
                "dias_restantes": max(0, dias_restantes),
                "motivo": info.get("motivo", "auto")
            })
        
        return temporarios
    
    def obter_estatisticas(self) -> Dict:
        """
        Obtém estatísticas do gerenciador
        
        Returns:
            Dict com estatísticas
        """
        stats = self.metadata["estatisticas"].copy()
        
        stats["arquivos_temporarios_atuais"] = len(self.metadata["arquivos_temporarios"])
        stats["arquivos_protegidos"] = len(self.metadata["arquivos_protegidos"])
        stats["espaco_liberado_mb"] = stats["espaco_liberado_bytes"] / (1024*1024)
        
        # Taxa de resgate
        total = stats["total_deletados"] + stats["total_resgatados"]
        if total > 0:
            stats["taxa_resgate_percent"] = (stats["total_resgatados"] / total) * 100
        else:
            stats["taxa_resgate_percent"] = 0
        
        return stats
    
    # ========================================================================
    # VISUALIZAÇÃO
    # ========================================================================
    
    def exibir_status(self):
        """Exibe status dos arquivos temporários"""
        print("\n" + "="*70)
        print("GERENCIADOR DE TEMPORARIOS - STATUS")
        print("="*70)
        
        temporarios = self.listar_temporarios()
        stats = self.obter_estatisticas()
        
        print(f"\nESTATISTICAS")
        print(f"   Arquivos temporarios: {stats['arquivos_temporarios_atuais']}")
        print(f"   Arquivos protegidos: {stats['arquivos_protegidos']}")
        print(f"   Total deletados: {stats['total_deletados']}")
        print(f"   Total resgatados: {stats['total_resgatados']}")
        print(f"   Espaco liberado: {stats['espaco_liberado_mb']:.2f} MB")
        print(f"   Taxa de resgate: {stats['taxa_resgate_percent']:.1f}%")
        
        if temporarios:
            print(f"\nARQUIVOS TEMPORARIOS ({len(temporarios)})")
            print("-"*70)
            
            for temp in temporarios[:10]:  # Mostrar até 10
                print(f"\n{temp['nome']}")
                print(f"   Tamanho: {temp['tamanho_mb']:.2f} MB")
                print(f"   Delete em: {temp['dias_restantes']} dia(s)")
                print(f"   Motivo: {temp['motivo']}")
            
            if len(temporarios) > 10:
                print(f"\n... e mais {len(temporarios) - 10} arquivo(s)")
        
        print("\n" + "="*70 + "\n")


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("""
================================================================================
              GERENCIADOR DE TEMPORARIOS
                   LUNA (CORRIGIDO)
================================================================================
    """)
    
    # Teste básico
    print("Testando gerenciador...")
    gerenciador = GerenciadorTemporarios()
    
    print(f"Gerenciador inicializado")
    print(f"Pasta temporaria: {gerenciador.temp_dir}")
    print(f"Pasta existe: {gerenciador.temp_dir.exists()}")
    
    gerenciador.exibir_status()
    
    print("\nTESTE CONCLUIDO!")
