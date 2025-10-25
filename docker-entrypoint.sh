#!/bin/bash
# Docker entrypoint script for Luna V3
set -e

echo "=========================================="
echo "   Luna V3 - AI Agent System"
echo "=========================================="
echo ""

# Check for required environment variables
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  WARNING: ANTHROPIC_API_KEY is not set!"
    echo "   Please set it in your .env file or pass it as an environment variable."
    echo "   Example: docker run -e ANTHROPIC_API_KEY=sk-ant-... luna-v3"
    echo ""
fi

# Initialize files if they don't exist
if [ ! -f /app/memoria_agente.json ]; then
    echo "📝 Creating memoria_agente.json..."
    echo '{"aprendizados": [], "preferencias": {}, "historico_tarefas": []}' > /app/memoria_agente.json
fi

if [ ! -f /app/workspace_config.json ]; then
    echo "📁 Creating workspace_config.json..."
    echo '{"workspaces": {}, "workspace_atual": null}' > /app/workspace_config.json
fi

# Create directories if they don't exist
mkdir -p /app/workspaces
mkdir -p /app/Luna/planos
mkdir -p /app/Luna/.stats
mkdir -p /app/.backups
mkdir -p /app/backups_auto_evolucao

# Set proper permissions
chmod -R 755 /app/workspaces
chmod 644 /app/memoria_agente.json 2>/dev/null || true
chmod 644 /app/workspace_config.json 2>/dev/null || true

echo "✅ Luna V3 environment initialized"
echo ""
echo "Starting Luna..."
echo "=========================================="
echo ""

# Execute the command passed to docker run
exec "$@"
