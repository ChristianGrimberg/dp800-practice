#!/usr/bin/env bash
# sincronizar-curso.sh — compara el course-hierarchy.json del repo privado con el local.
set -euo pipefail
cd "$(dirname "$0")/.."

LOCAL="curso/_meta/course-hierarchy.json"
REMOTE_PATH="_meta/course-hierarchy.json"

echo "🔄 Sincronizando curso oficial..."
TMP=$(mktemp)
trap 'rm -f "$TMP"' EXIT

if ! gh api "repos/ChristianGrimberg/DP-800/contents/${REMOTE_PATH}" --jq '.content' | base64 -d > "$TMP"; then
  echo "❌ No se pudo descargar el curso privado. Revisá la autenticación y el acceso." >&2
  exit 2
fi

# Una respuesta vacía o inválida no representa drift.
if ! python3 - "$LOCAL" "$TMP" <<'PYJSON'
import json
import sys

for filename in sys.argv[1:]:
    with open(filename, encoding='utf-8') as source:
        data = json.load(source)
    if not isinstance(data, dict) or not data.get('course') or not data.get('paths'):
        raise ValueError(f'Jerarquía de curso inválida: {filename}')
PYJSON
then
  echo "❌ No se puede comparar: la jerarquía está vacía o es inválida." >&2
  exit 2
fi

if diff -q "$LOCAL" "$TMP" >/dev/null 2>&1; then
  echo "✅ Sin diferencias."
  exit 0
fi

echo "⚠️  Hay diferencias entre el curso oficial y el espejo local."
echo "   Local: $LOCAL"
echo "   Remoto: $REMOTE_PATH"
diff -u "$LOCAL" "$TMP" | head -40 || true
echo ""
echo "Revisá los cambios y actualizá $LOCAL mediante un PR."
# 0: sin diferencias; 1: drift confirmado; 2: error de descarga/validación.
exit 1
