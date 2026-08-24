FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

ARG DEBIAN_FRONTEND=noninteractive

USER root

# Paquetes base
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    apt-transport-https \
    ca-certificates \
    unixodbc-dev \
    software-properties-common \
    git \
    jq \
    tree \
    ripgrep \
    && rm -rf /var/lib/apt/lists/*

# MSSQL tools (sqlcmd)
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && curl -fsSL https://packages.microsoft.com/config/ubuntu/24.04/prod.list | tee /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends mssql-tools18 \
    && echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> /etc/profile.d/mssql-tools.sh \
    && rm -rf /var/lib/apt/lists/*

# Python pip + herramientas de lint/docs
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --break-system-packages \
    mssql-cli \
    sqlfluff \
    mkdocs-material \
    mkdocs-awesome-pages-plugin \
    mkdocs-include-markdown-plugin \
    pymdown-extensions \
    pyyaml \
    requests

# Crear usuario vscode (lo provee la imagen base, pero validamos)
USER vscode
WORKDIR /workspaces/dp800-practice
