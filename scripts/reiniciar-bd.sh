#!/usr/bin/env bash
# reiniciar-bd.sh — baja los servicios y limpia volúmenes del SQL.
set -euo pipefail

cd "$(dirname "$0")/.."

echo "🛑 Bajando servicios..."
docker compose -f .devcontainer/docker-compose.yml down

read -rp "¿Borrar también los volúmenes (DATOS SE PIERDEN)? [y/N] " resp
case "$resp" in
  [yY]*)
    docker compose -f .devcontainer/docker-compose.yml down -v
    echo "✅ Volúmenes borrados."
    ;;
  *)
    echo "ℹ️  Volúmenes conservados."
    ;;
esac

echo "🚀 Levantando de nuevo..."
docker compose -f .devcontainer/docker-compose.yml up -d
