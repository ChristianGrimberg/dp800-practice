#!/usr/bin/env bash
# post-create.sh — se ejecuta una vez cuando se construye el dev container.
set -euo pipefail

echo "==[ dp800-practice :: post-create ]=="

MSSQL_HOST="${MSSQL_HOST:-sql}"
MSSQL_PORT="${MSSQL_PORT:-1433}"
MSSQL_USER="${MSSQL_USER:-sa}"
MSSQL_PASSWORD="${MSSQL_PASSWORD:?MSSQL_PASSWORD requerido}"
OLLAMA_HOST="${OLLAMA_HOST:-ollama}"
OLLAMA_PORT="${OLLAMA_PORT:-11434}"

SQLCMD="/opt/mssql-tools18/bin/sqlcmd"

echo "[1/4] Esperando SQL Server en ${MSSQL_HOST}:${MSSQL_PORT}..."
for i in {1..60}; do
  if "$SQLCMD" -C -S "${MSSQL_HOST},${MSSQL_PORT}" -U "$MSSQL_USER" -P "$MSSQL_PASSWORD" -Q "SELECT 1" > /dev/null 2>&1; then
    echo "    SQL listo tras ${i} intento(s)."
    break
  fi
  sleep 2
done

echo "[2/4] Creando base dp800_lab si no existe..."
"$SQLCMD" -C -S "${MSSQL_HOST},${MSSQL_PORT}" -U "$MSSQL_USER" -P "$MSSQL_PASSWORD" -Q "
IF DB_ID('dp800_lab') IS NULL
  CREATE DATABASE dp800_lab;
" > /dev/null 2>&1 || echo "    (la base ya existe o reintentá manualmente)"

echo "[3/4] Esperando Ollama en ${OLLAMA_HOST}:${OLLAMA_PORT}..."
for i in {1..30}; do
  if curl -fsS "http://${OLLAMA_HOST}:${OLLAMA_PORT}/api/tags" > /dev/null 2>&1; then
    echo "    Ollama listo."
    break
  fi
  sleep 2
done

echo "[4/4] Descargando modelos (nomic-embed-text, llama3.2:3b)..."
docker exec dp800-ollama ollama pull nomic-embed-text 2>&1 | tail -3 || echo "    modelo nomic-embed-text ya estaba"
docker exec dp800-ollama ollama pull llama3.2:3b 2>&1 | tail -3 || echo "    modelo llama3.2:3b ya estaba"

cat <<EOF

========================================
🎉 Contenedor listo.

📚 Documentación:    https://christiangrimberg.github.io/dp800-practice/
🗺️  Mapa:            https://christiangrimberg.github.io/dp800-practice/mapa-de-aprendizaje/
🛢️  SQL:             ${MSSQL_HOST}:${MSSQL_PORT} (usuario: ${MSSQL_USER}, BD: dp800_lab)
🤖 Ollama:           ${OLLAMA_HOST}:${OLLAMA_PORT}

Para conectarte:
  bash scripts/conectar-sql.sh "SELECT @@VERSION"

Para servir la documentación localmente:
  mkdocs serve
========================================
EOF
