#!/usr/bin/env bash
# sincronizar-curso.sh — compara el course-hierarchy.json del repo privado con el local.
set -euo pipefail
cd "$(dirname "$0")/.."

LOCAL="curso/_meta/course-hierarchy.json"
REMOTE_PATH="_meta/course-hierarchy.json"

echo "🔄 Sincronizando curso oficial..."
TMP=$(mktemp)
trap 'rm -f "$TMP"' EXIT

gh api "repos/ChristianGrimberg/DP-800/contents/${REMOTE_PATH}" --jq '.content' | base64 -d > "$TMP"

if diff -q "$LOCAL" "$TMP" >/dev/null 2>&1; then
  echo "✅ Sin diferencias."
  exit 0
fi

echo "⚠️  Hay diferencias entre el curso oficial y el espejo local."
echo "   Local: $LOCAL"
echo "   Remoto: $REMOTE_PATH"
diff -u "$LOCAL" "$TMP" | head -40 || true
echo ""
echo "Para sincronizar: cp $TMP $LOCAL"
