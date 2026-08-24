#!/usr/bin/env bash
# conectar-sql.sh — wrapper para invocar sqlcmd o mssql-cli.
#
# Uso:
#   bash scripts/conectar-sql.sh                           # abre mssql-cli interactivo
#   bash scripts/conectar-sql.sh "SELECT @@VERSION"        # ejecuta query y sale
#   bash scripts/conectar-sql.sh archivo.sql               # ejecuta archivo
set -euo pipefail

# Detectar entorno: dentro del container usa service name "sql", fuera usa localhost.
if [ -n "${MSSQL_HOST:-}" ]; then
  HOST="$MSSQL_HOST"
  PORT="${MSSQL_PORT:-1433}"
else
  HOST="localhost"
  PORT="1433"
fi

USER="${MSSQL_USER:-sa}"
PASSWORD="${MSSQL_PASSWORD:-${MSSQL_SA_PASSWORD:-}}"
DB="${MSSQL_DATABASE:-dp800_lab}"

if [ -z "$PASSWORD" ] && [ -f .env ]; then
  PASSWORD="$(grep '^MSSQL_SA_PASSWORD=' .env | cut -d= -f2-)"
fi

if [ -z "$PASSWORD" ]; then
  echo "❌ MSSQL_PASSWORD (o MSSQL_SA_PASSWORD) no definido."
  echo "   Definilo en .env (ver .devcontainer/.env.example) o como variable de entorno."
  exit 1
fi

SQLCMD="/opt/mssql-tools18/bin/sqlcmd"
if ! command -v "$SQLCMD" >/dev/null 2>&1; then
  SQLCMD="sqlcmd"
fi
MSSQL_CLI="mssql-cli"

args=(-C -S "${HOST},${PORT}" -U "$USER" -P "$PASSWORD" -d "$DB")

if [ $# -eq 0 ]; then
  exec "$MSSQL_CLI" "${args[@]}"
elif [ -f "$1" ]; then
  exec "$SQLCMD" "${args[@]}" -i "$1"
else
  exec "$SQLCMD" "${args[@]}" -Q "$1"
fi
