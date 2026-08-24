#!/usr/bin/env bash
# lint-sql.sh — corre sqlfluff sobre toda la carpeta practica/ del curso.
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v sqlfluff >/dev/null 2>&1; then
  echo "❌ sqlfluff no instalado. Instalá con: pip install sqlfluff"
  exit 1
fi

TARGET="${1:-curso/path-1-diseno-y-desarrollo-de-soluciones-de-base-de-datos}"

echo "🔍 Ejecutando sqlfluff sobre: $TARGET"
exec sqlfluff lint "$TARGET" --dialect tsql
