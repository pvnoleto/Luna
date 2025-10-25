# Dockerfile for Luna V3 - Advanced AI Agent System
# Based on Python 3.13 with Playwright support

FROM python:3.13-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONUTF8=1 \
    PYTHONIOENCODING=utf-8 \
    DEBIAN_FRONTEND=noninteractive \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Set working directory
WORKDIR /app

# Install system dependencies required for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install Playwright and browsers
RUN pip install --no-cache-dir playwright && \
    playwright install chromium && \
    playwright install-deps chromium

# Copy Luna application files
COPY luna_v3_FINAL_OTIMIZADA.py .
COPY memoria_permanente.py .
COPY cofre_credenciais.py .
COPY gerenciador_workspaces.py .
COPY integracao_notion.py .
COPY integracao_google.py .
COPY sistema_auto_evolucao.py .
COPY gerenciador_temp.py .
COPY telemetria_manager.py .

# Create necessary directories
RUN mkdir -p /app/workspaces \
    /app/Luna/planos \
    /app/Luna/.stats \
    /app/.backups \
    /app/backups_auto_evolucao \
    /app/LOGS_EXECUCAO

# Create volumes for persistence
VOLUME ["/app/workspaces", "/app/Luna", "/app/.backups", "/app/backups_auto_evolucao"]

# Copy entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Set entrypoint
ENTRYPOINT ["docker-entrypoint.sh"]

# Default command (can be overridden)
CMD ["python", "luna_v3_FINAL_OTIMIZADA.py"]
