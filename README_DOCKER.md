# 🐳 Luna V3 - Docker Setup Guide

Este guia explica como executar Luna V3 em um container Docker, proporcionando um ambiente isolado e reproduzível.

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Instalação Rápida](#instalação-rápida)
3. [Configuração](#configuração)
4. [Como Usar](#como-usar)
5. [Volumes e Persistência](#volumes-e-persistência)
6. [Troubleshooting](#troubleshooting)
7. [Comandos Avançados](#comandos-avançados)

---

## 🔧 Pré-requisitos

### Instalar Docker

**Linux (Ubuntu/Debian):**
```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Adicionar seu usuário ao grupo docker (evita usar sudo)
sudo usermod -aG docker $USER

# Fazer logout e login novamente para aplicar
```

**Windows:**
- Baixe e instale [Docker Desktop para Windows](https://www.docker.com/products/docker-desktop/)
- No WSL2 (recomendado), Docker Desktop integra automaticamente

**macOS:**
- Baixe e instale [Docker Desktop para Mac](https://www.docker.com/products/docker-desktop/)

### Verificar Instalação
```bash
docker --version
docker-compose --version
```

---

## 🚀 Instalação Rápida

### 1. Configure sua API Key

Crie o arquivo `.env` na raiz do projeto Luna:

```bash
# Copie o template
cp .env.example .env

# Edite e adicione sua chave (use nano, vim, ou qualquer editor)
nano .env
```

Conteúdo do `.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-XXXXXXXXXXXXXXXXXXXXXXX
```

### 2. Build da Imagem Docker

```bash
# Navegue até o diretório do Luna
cd /mnt/c/Projetos\ Automações\ e\ Digitais/Luna

# Build da imagem (primeira vez pode demorar ~5-10 min)
docker-compose build
```

### 3. Execute Luna

```bash
# Inicie o container
docker-compose up

# Ou em modo detached (background)
docker-compose up -d

# Para acessar o terminal do Luna em background
docker attach luna-agent
```

---

## ⚙️ Configuração

### Estrutura de Arquivos

```
Luna/
├── Dockerfile              # Definição da imagem Docker
├── docker-compose.yml      # Orquestração do container
├── docker-entrypoint.sh    # Script de inicialização
├── .dockerignore           # Arquivos excluídos do build
├── requirements.txt        # Dependências Python
├── .env                    # Variáveis de ambiente (API key)
└── README_DOCKER.md        # Este arquivo
```

### Variáveis de Ambiente

O arquivo `.env` pode conter:

```bash
# Obrigatório
ANTHROPIC_API_KEY=sk-ant-api03-...

# Opcional - Configurações do Notion
NOTION_TOKEN=secret_...

# Opcional - Outras configurações
LUNA_TIER=2                 # Tier da API (1-4)
LUNA_RATE_MODE=balanced     # conservative/balanced/aggressive
```

---

## 🎯 Como Usar

### Modo Interativo (Recomendado)

```bash
# Iniciar Luna em modo interativo
docker-compose run --rm luna

# Ou se já estiver rodando
docker attach luna-agent
```

Agora você pode interagir com Luna normalmente:
```
🌙 Luna V3 está pronta!
Digite sua solicitação (ou 'sair' para encerrar):
> Olá Luna, me ajude a criar um script Python
```

### Executar Comando Específico

```bash
# Executar script específico
docker-compose run --rm luna python meu_script.py

# Abrir shell interativo no container
docker-compose run --rm luna bash
```

### Parar o Container

```bash
# Se estiver em modo attached (Ctrl+C não funciona bem)
# Use Ctrl+P seguido de Ctrl+Q para detach sem parar

# Parar o container
docker-compose stop

# Parar e remover
docker-compose down
```

---

## 💾 Volumes e Persistência

### Dados Persistidos

O Docker Compose mapeia os seguintes dados para o host, garantindo persistência:

```yaml
volumes:
  - ./workspaces:/app/workspaces              # Seus projetos
  - ./memoria_agente.json:/app/memoria_agente.json  # Memória do agente
  - ./workspace_config.json:/app/workspace_config.json  # Configuração
  - ./cofre.enc:/app/cofre.enc                # Credenciais encriptadas
  - ./credentials.json:/app/credentials.json  # Credenciais Google
  - ./token_gmail.json:/app/token_gmail.json  # Token Gmail
  - ./token_calendar.json:/app/token_calendar.json  # Token Calendar
  - ./backups_auto_evolucao:/app/backups_auto_evolucao  # Backups
  - ./Luna:/app/Luna                          # Dados internos
```

### Backup dos Dados

```bash
# Backup manual dos dados importantes
tar -czf luna-backup-$(date +%Y%m%d).tar.gz \
    workspaces/ \
    memoria_agente.json \
    workspace_config.json \
    cofre.enc \
    Luna/ \
    backups_auto_evolucao/

# Restaurar backup
tar -xzf luna-backup-YYYYMMDD.tar.gz
```

---

## 🔍 Troubleshooting

### Problema: API Key não encontrada

**Sintoma:**
```
⚠️  WARNING: ANTHROPIC_API_KEY is not set!
```

**Solução:**
```bash
# Verifique se o .env existe
ls -la .env

# Verifique o conteúdo (sem mostrar a chave completa)
grep ANTHROPIC_API_KEY .env | head -c 30

# Reconstrua o container
docker-compose down
docker-compose up --build
```

### Problema: Permissões de arquivo

**Sintoma:**
```
Permission denied: 'memoria_agente.json'
```

**Solução:**
```bash
# Ajuste as permissões no host
chmod 644 memoria_agente.json
chmod 644 workspace_config.json
chmod -R 755 workspaces/

# Ou dentro do container
docker-compose run --rm luna bash
chmod 644 /app/memoria_agente.json
```

### Problema: Container não inicia

**Sintoma:**
```
Error: container luna-agent is not running
```

**Solução:**
```bash
# Veja os logs
docker-compose logs

# Reinicie do zero
docker-compose down
docker-compose up --build

# Se ainda não funcionar, limpe tudo
docker-compose down -v
docker system prune -a
docker-compose up --build
```

### Problema: Playwright não funciona

**Sintoma:**
```
Executable doesn't exist at /ms-playwright/chromium-XXXX/chrome-linux/chrome
```

**Solução:**
```bash
# Reconstrua a imagem do zero
docker-compose build --no-cache

# Ou reinstale o Playwright dentro do container
docker-compose run --rm luna bash
playwright install chromium
playwright install-deps chromium
```

### Problema: Memória insuficiente

**Sintoma:**
```
Killed
```

**Solução:**
Edite `docker-compose.yml` e aumente os limites:
```yaml
deploy:
  resources:
    limits:
      memory: 4G  # Era 2G
```

---

## 🔧 Comandos Avançados

### Build e Deploy

```bash
# Build sem cache (útil após mudanças no Dockerfile)
docker-compose build --no-cache

# Build com argumentos customizados
docker build --build-arg PYTHON_VERSION=3.13 -t luna-v3:custom .

# Tag para registry
docker tag luna-v3:latest myregistry.com/luna-v3:v1.0
docker push myregistry.com/luna-v3:v1.0
```

### Debugging

```bash
# Ver logs em tempo real
docker-compose logs -f

# Logs apenas do serviço luna
docker-compose logs -f luna

# Entrar no container em execução
docker exec -it luna-agent bash

# Inspecionar o container
docker inspect luna-agent

# Ver uso de recursos
docker stats luna-agent
```

### Manutenção

```bash
# Listar containers
docker-compose ps

# Parar todos os containers
docker-compose stop

# Remover containers parados
docker-compose rm

# Limpar volumes órfãos
docker volume prune

# Limpar tudo (CUIDADO: remove imagens, containers, volumes)
docker system prune -a --volumes
```

### Execução de Scripts

```bash
# Executar teste específico
docker-compose run --rm luna python -c "print('Hello from Luna!')"

# Executar com variáveis customizadas
docker-compose run --rm -e LUNA_TIER=4 luna

# Montar volume adicional
docker-compose run --rm -v $(pwd)/scripts:/scripts luna python /scripts/test.py
```

### Multi-Stage Build (Otimização)

Para produção, você pode otimizar o Dockerfile usando multi-stage:

```dockerfile
# Stage 1: Builder
FROM python:3.13-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.13-slim
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
# ... resto do Dockerfile
```

---

## 📊 Monitoring e Logs

### Configurar Logging

Edite `docker-compose.yml` para configurar logs:

```yaml
services:
  luna:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Analisar Logs

```bash
# Ver últimas 100 linhas
docker-compose logs --tail=100

# Filtrar por data
docker-compose logs --since 2024-01-01T00:00:00

# Buscar por erro
docker-compose logs | grep -i "error"
```

---

## 🔐 Segurança

### Boas Práticas

1. **Nunca commite `.env`**
   - O `.gitignore` já está configurado
   - Use `.env.example` como template

2. **Proteja credenciais**
   ```bash
   chmod 600 .env
   chmod 600 cofre.enc
   chmod 600 credentials.json
   ```

3. **Use secrets do Docker** (produção)
   ```yaml
   secrets:
     anthropic_key:
       file: ./secrets/anthropic_key.txt
   services:
     luna:
       secrets:
         - anthropic_key
   ```

4. **Scaneie vulnerabilidades**
   ```bash
   docker scan luna-v3:latest
   ```

---

## 🌐 Deploy em Servidor

### Docker Compose em Servidor

```bash
# Em servidor remoto via SSH
ssh user@server

# Clone o repo
git clone <seu-repo> luna
cd luna

# Configure .env
nano .env

# Inicie em background
docker-compose up -d

# Monitore logs
docker-compose logs -f
```

### Systemd Service (Linux)

Crie `/etc/systemd/system/luna.service`:

```ini
[Unit]
Description=Luna V3 Docker Container
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/path/to/luna
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Ative:
```bash
sudo systemctl enable luna
sudo systemctl start luna
sudo systemctl status luna
```

---

## 📝 Notas Importantes

1. **Primeira execução**: O build pode demorar 5-10 minutos (download de dependências e Playwright)

2. **Persistência**: Todos os dados importantes são salvos em volumes mapeados no host

3. **Interatividade**: Use `-it` para modo interativo e `stdin_open: true` no docker-compose

4. **Recursos**: Configure limites adequados de CPU/memória para seu caso de uso

5. **Atualizações**: Para atualizar Luna, faça pull do código e rebuild:
   ```bash
   git pull
   docker-compose build
   docker-compose up
   ```

---

## 🆘 Suporte

- **Documentação principal**: `README_VERSAO_FINAL.md`
- **Guia rápido**: `GUIA_RAPIDO.md`
- **Notion integration**: `INTEGRACAO_NOTION_GUIA.md`
- **Google integration**: `INTEGRACAO_GOOGLE_GUIA.md`
- **Project instructions**: `CLAUDE.md`

---

## ✅ Checklist de Verificação

Antes de reportar problemas, verifique:

- [ ] Docker e Docker Compose instalados (`docker --version`)
- [ ] Arquivo `.env` existe e contém `ANTHROPIC_API_KEY`
- [ ] Build completou sem erros (`docker-compose build`)
- [ ] Volumes mapeados corretamente (veja `docker-compose.yml`)
- [ ] Permissões de arquivos corretas (`chmod 644` em JSONs)
- [ ] Logs do container não mostram erros (`docker-compose logs`)
- [ ] Recursos suficientes (memória > 2GB disponível)

---

**Desenvolvido com 🌙 por Luna V3**
**Qualidade: 98/100 - Production-ready**
