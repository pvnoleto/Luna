#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 SISTEMA DE MEMÓRIA PERMANENTE
==================================

Implementa aprendizado contínuo para o agente:
- Salva aprendizados entre sessões
- Base de conhecimento crescente
- Contexto histórico
- Preferências do usuário

Arquitetura:
- memoria.json: Base de conhecimento
- Busca semântica (opcional: embeddings)
- Categorização automática
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import hashlib


class MemoriaPermanente:
    """
    Sistema de memória persistente para o agente
    """
    
    def __init__(self, arquivo_memoria: str = "memoria_agente.json"):
        self.arquivo_memoria = arquivo_memoria
        self.memoria = {
            "aprendizados": [],
            "preferencias_usuario": {},
            "historico_tarefas": [],
            "ferramentas_criadas": [],
            "contexto": {},
            "estatisticas": {
                "total_tarefas": 0,
                "total_aprendizados": 0,
                "ferramentas_criadas": 0,
                "primeira_sessao": None,
                "ultima_sessao": None
            }
        }
        self._carregar_memoria()
    
    def _carregar_memoria(self):
        """Carrega memória do disco"""
        if os.path.exists(self.arquivo_memoria):
            try:
                with open(self.arquivo_memoria, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    self.memoria.update(dados)
                print(f"🧠 Memória carregada: {len(self.memoria['aprendizados'])} aprendizados")
            except Exception as e:
                print(f"⚠️  Erro ao carregar memória: {e}")
                print("   Iniciando memória vazia")
        else:
            print("🆕 Criando nova memória")
            self.memoria["estatisticas"]["primeira_sessao"] = datetime.now().isoformat()
            self._salvar_memoria()
    
    def _salvar_memoria(self):
        """Salva memória no disco"""
        try:
            # Atualizar timestamp
            self.memoria["estatisticas"]["ultima_sessao"] = datetime.now().isoformat()
            
            # Salvar com backup
            if os.path.exists(self.arquivo_memoria):
                backup = f"{self.arquivo_memoria}.bak"
                os.replace(self.arquivo_memoria, backup)
            
            with open(self.arquivo_memoria, 'w', encoding='utf-8') as f:
                json.dump(self.memoria, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            print(f"❌ Erro ao salvar memória: {e}")
    
    def adicionar_aprendizado(self, categoria: str, conteudo: str, 
                             contexto: Optional[str] = None, tags: List[str] = None):
        """
        Adiciona novo aprendizado
        
        Args:
            categoria: Tipo (ex: "tecnica", "preferencia", "bug", "solucao")
            conteudo: O que foi aprendido
            contexto: Contexto adicional
            tags: Tags para busca
        """
        aprendizado = {
            "id": self._gerar_id(conteudo),
            "timestamp": datetime.now().isoformat(),
            "categoria": categoria,
            "conteudo": conteudo,
            "contexto": contexto or "",
            "tags": tags or [],
            "relevancia": 1.0,
            "uso_count": 0
        }
        
        # Evitar duplicatas
        if not any(a["id"] == aprendizado["id"] for a in self.memoria["aprendizados"]):
            self.memoria["aprendizados"].append(aprendizado)
            self.memoria["estatisticas"]["total_aprendizados"] += 1
            self._salvar_memoria()
            print(f"✅ Aprendizado salvo: {categoria}")
            return True
        return False
    
    def buscar_aprendizados(self, query: str = None, categoria: str = None, 
                           tags: List[str] = None, limite: int = 10) -> List[Dict]:
        """
        Busca aprendizados relevantes
        
        Args:
            query: Texto para buscar
            categoria: Filtrar por categoria
            tags: Filtrar por tags
            limite: Máximo de resultados
        """
        resultados = self.memoria["aprendizados"]
        
        # Filtrar por categoria
        if categoria:
            resultados = [a for a in resultados if a["categoria"] == categoria]
        
        # Filtrar por tags
        if tags:
            resultados = [a for a in resultados if any(t in a["tags"] for t in tags)]
        
        # Busca textual simples
        if query:
            query_lower = query.lower()
            resultados = [
                a for a in resultados 
                if query_lower in a["conteudo"].lower() or 
                   query_lower in a["contexto"].lower()
            ]
        
        # Ordenar por relevância e uso
        resultados.sort(key=lambda x: (x["relevancia"], x["uso_count"]), reverse=True)
        
        # Incrementar uso dos retornados
        for r in resultados[:limite]:
            r["uso_count"] += 1
        
        self._salvar_memoria()
        return resultados[:limite]
    
    def registrar_tarefa(self, tarefa: str, resultado: str, 
                        ferramentas_usadas: List[str] = None, 
                        sucesso: bool = True):
        """Registra tarefa executada"""
        registro = {
            "timestamp": datetime.now().isoformat(),
            "tarefa": tarefa,
            "resultado": resultado[:500],  # Limitar tamanho
            "ferramentas_usadas": ferramentas_usadas or [],
            "sucesso": sucesso
        }
        
        self.memoria["historico_tarefas"].append(registro)
        self.memoria["estatisticas"]["total_tarefas"] += 1
        
        # Manter apenas últimas 100 tarefas
        if len(self.memoria["historico_tarefas"]) > 100:
            self.memoria["historico_tarefas"] = self.memoria["historico_tarefas"][-100:]
        
        self._salvar_memoria()
    
    def registrar_ferramenta_criada(self, nome: str, descricao: str, codigo: str):
        """Registra ferramenta criada pelo agente"""
        ferramenta = {
            "timestamp": datetime.now().isoformat(),
            "nome": nome,
            "descricao": descricao,
            "codigo_hash": hashlib.md5(codigo.encode()).hexdigest(),
            "uso_count": 0
        }
        
        self.memoria["ferramentas_criadas"].append(ferramenta)
        self.memoria["estatisticas"]["ferramentas_criadas"] += 1
        self._salvar_memoria()
    
    def salvar_preferencia(self, chave: str, valor):
        """Salva preferência do usuário"""
        self.memoria["preferencias_usuario"][chave] = {
            "valor": valor,
            "timestamp": datetime.now().isoformat()
        }
        self._salvar_memoria()
        print(f"✅ Preferência salva: {chave}")
    
    def obter_preferencia(self, chave: str, padrao=None):
        """Obtém preferência do usuário"""
        pref = self.memoria["preferencias_usuario"].get(chave)
        return pref["valor"] if pref else padrao
    
    def obter_contexto_recente(self, limite: int = 5) -> str:
        """Obtém contexto das últimas tarefas"""
        tarefas = self.memoria["historico_tarefas"][-limite:]
        
        if not tarefas:
            return "Primeira interação com o usuário."
        
        contexto = "Histórico recente:\n"
        for t in tarefas:
            contexto += f"- {t['tarefa'][:100]} → {'✅' if t['sucesso'] else '❌'}\n"
        
        return contexto
    
    def obter_estatisticas(self) -> Dict:
        """Retorna estatísticas da memória"""
        stats = self.memoria["estatisticas"].copy()
        
        # Calcular adicionais
        stats["aprendizados_unicos"] = len(self.memoria["aprendizados"])
        stats["categorias"] = len(set(a["categoria"] for a in self.memoria["aprendizados"]))
        
        if stats["primeira_sessao"]:
            primeira = datetime.fromisoformat(stats["primeira_sessao"])
            dias = (datetime.now() - primeira).days
            stats["dias_uso"] = dias
        
        return stats
    
    def exportar_relatorio(self, arquivo: str = "relatorio_memoria.md"):
        """Exporta relatório de memória em Markdown"""
        stats = self.obter_estatisticas()
        
        relatorio = f"""# 🧠 RELATÓRIO DE MEMÓRIA DO AGENTE

Data: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## 📊 ESTATÍSTICAS

- **Total de tarefas executadas:** {stats['total_tarefas']}
- **Total de aprendizados:** {stats['total_aprendizados']}
- **Ferramentas criadas:** {stats['ferramentas_criadas']}
- **Dias de uso:** {stats.get('dias_uso', 0)}
- **Primeira sessão:** {stats['primeira_sessao']}
- **Última sessão:** {stats['ultima_sessao']}

## 🎯 APRENDIZADOS POR CATEGORIA

"""
        # Agrupar por categoria
        categorias = {}
        for a in self.memoria["aprendizados"]:
            cat = a["categoria"]
            if cat not in categorias:
                categorias[cat] = []
            categorias[cat].append(a)
        
        for cat, aprendizados in sorted(categorias.items()):
            relatorio += f"\n### {cat.upper()} ({len(aprendizados)} aprendizados)\n\n"
            for a in sorted(aprendizados, key=lambda x: x["uso_count"], reverse=True)[:10]:
                relatorio += f"- **[Uso: {a['uso_count']}x]** {a['conteudo']}\n"
        
        relatorio += f"\n## 🛠️ FERRAMENTAS CRIADAS\n\n"
        for f in self.memoria["ferramentas_criadas"][-20:]:
            relatorio += f"- **{f['nome']}**: {f['descricao']} (Uso: {f['uso_count']}x)\n"
        
        relatorio += f"\n## 📋 ÚLTIMAS TAREFAS\n\n"
        for t in self.memoria["historico_tarefas"][-10:]:
            emoji = "✅" if t["sucesso"] else "❌"
            relatorio += f"- {emoji} {t['tarefa'][:100]}\n"
        
        relatorio += f"\n## ⚙️ PREFERÊNCIAS DO USUÁRIO\n\n"
        for chave, pref in self.memoria["preferencias_usuario"].items():
            relatorio += f"- **{chave}**: {pref['valor']}\n"
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write(relatorio)
        
        print(f"✅ Relatório exportado: {arquivo}")
        return arquivo
    
    def limpar_memoria(self, confirmar: bool = False):
        """Limpa toda a memória (CUIDADO!)"""
        if not confirmar:
            print("⚠️  Use confirmar=True para limpar a memória")
            return False
        
        # Backup antes de limpar
        backup = f"memoria_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.exportar_backup(backup)
        
        self.memoria = {
            "aprendizados": [],
            "preferencias_usuario": {},
            "historico_tarefas": [],
            "ferramentas_criadas": [],
            "contexto": {},
            "estatisticas": {
                "total_tarefas": 0,
                "total_aprendizados": 0,
                "ferramentas_criadas": 0,
                "primeira_sessao": datetime.now().isoformat(),
                "ultima_sessao": None
            }
        }
        
        self._salvar_memoria()
        print(f"✅ Memória limpa. Backup salvo em: {backup}")
        return True
    
    def exportar_backup(self, arquivo: str):
        """Exporta backup completo"""
        import shutil
        shutil.copy2(self.arquivo_memoria, arquivo)
        print(f"✅ Backup criado: {arquivo}")
    
    def _gerar_id(self, texto: str) -> str:
        """Gera ID único para aprendizado"""
        return hashlib.md5(texto.encode()).hexdigest()[:16]
    
    def mostrar_resumo(self):
        """Mostra resumo da memória"""
        stats = self.obter_estatisticas()
        
        print("\n" + "="*70)
        print("🧠 MEMÓRIA DO AGENTE")
        print("="*70)
        print(f"📊 Tarefas executadas: {stats['total_tarefas']}")
        print(f"🎯 Aprendizados: {stats['total_aprendizados']}")
        print(f"🛠️  Ferramentas criadas: {stats['ferramentas_criadas']}")
        print(f"📅 Dias de uso: {stats.get('dias_uso', 0)}")
        
        if self.memoria["aprendizados"]:
            print(f"\n🏆 Top 5 Aprendizados Mais Usados:")
            top = sorted(self.memoria["aprendizados"], 
                        key=lambda x: x["uso_count"], reverse=True)[:5]
            for i, a in enumerate(top, 1):
                print(f"  {i}. [{a['uso_count']}x] {a['conteudo'][:60]}...")
        
        print("="*70 + "\n")


# ============================================================================
# INTERFACE DE TESTE
# ============================================================================

def menu_memoria():
    """Interface de teste da memória"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  🧠 SISTEMA DE MEMÓRIA PERMANENTE                           ║
║                                                              ║
║  Gerenciamento de aprendizado contínuo do agente           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    memoria = MemoriaPermanente()
    
    while True:
        print("\n" + "="*70)
        print("MENU DE MEMÓRIA")
        print("="*70)
        print("1. ➕ Adicionar aprendizado")
        print("2. 🔍 Buscar aprendizados")
        print("3. 📊 Mostrar estatísticas")
        print("4. 📋 Exportar relatório")
        print("5. ⚙️  Salvar preferência")
        print("6. 💾 Exportar backup")
        print("7. 🗑️  Limpar memória (backup automático)")
        print("0. 🚪 Sair")
        print("="*70)
        
        escolha = input("\nEscolha: ").strip()
        
        try:
            if escolha == "1":
                print("\n➕ ADICIONAR APRENDIZADO")
                categoria = input("Categoria (tecnica/preferencia/bug/solucao): ").strip()
                conteudo = input("Conteúdo: ").strip()
                contexto = input("Contexto (opcional): ").strip()
                tags_str = input("Tags (separadas por vírgula): ").strip()
                tags = [t.strip() for t in tags_str.split(",")] if tags_str else []
                
                memoria.adicionar_aprendizado(categoria, conteudo, contexto, tags)
            
            elif escolha == "2":
                print("\n🔍 BUSCAR APRENDIZADOS")
                query = input("Buscar por (Enter para todos): ").strip()
                categoria = input("Categoria (Enter para todas): ").strip()
                
                resultados = memoria.buscar_aprendizados(
                    query=query if query else None,
                    categoria=categoria if categoria else None
                )
                
                print(f"\n📋 {len(resultados)} resultados:")
                for i, r in enumerate(resultados, 1):
                    print(f"\n{i}. [{r['categoria']}] (Uso: {r['uso_count']}x)")
                    print(f"   {r['conteudo']}")
                    if r['contexto']:
                        print(f"   💬 {r['contexto']}")
            
            elif escolha == "3":
                memoria.mostrar_resumo()
            
            elif escolha == "4":
                arquivo = input("Nome do arquivo (Enter=padrão): ").strip()
                memoria.exportar_relatorio(arquivo if arquivo else "relatorio_memoria.md")
            
            elif escolha == "5":
                chave = input("Chave: ").strip()
                valor = input("Valor: ").strip()
                memoria.salvar_preferencia(chave, valor)
            
            elif escolha == "6":
                arquivo = input("Nome do backup: ").strip()
                if not arquivo:
                    arquivo = f"memoria_backup_{datetime.now().strftime('%Y%m%d')}.json"
                memoria.exportar_backup(arquivo)
            
            elif escolha == "7":
                confirmar = input("⚠️  CONFIRMA LIMPEZA DA MEMÓRIA? (sim/não): ").strip()
                if confirmar.lower() == "sim":
                    memoria.limpar_memoria(confirmar=True)
            
            elif escolha == "0":
                print("\n👋 Até logo!")
                break
            
            else:
                print("❌ Opção inválida")
        
        except KeyboardInterrupt:
            print("\n\n👋 Saindo...")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")


if __name__ == "__main__":
    menu_memoria()
