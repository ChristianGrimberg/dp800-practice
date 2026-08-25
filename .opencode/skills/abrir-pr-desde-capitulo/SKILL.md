---
nombre: abrir-pr-desde-capitulo
version: 2.0
idioma: es
agentes_recomendados:
  - arquitecto-dp800
---

# Skill: abrir-pr-desde-capitulo

## Qué hace

Automatiza la apertura de un PR para una unidad del curso, respetando
las convenciones de flujo del repo (ver `CONTRIBUTING.md`):

1. Verifica que el front-matter esté completo.
2. Crea la rama `feature/<codigo>-<slug>` desde `origin/main` actualizado.
3. Hace commit con mensaje gitmoji + español.
4. Pushea.
5. Abre el PR con `gh pr create` aplicando las reglas obligatorias:
   - `--base main` (merge siempre hacia `main`).
   - `--draft` (siempre en Draft, esperando aprobación humana).
   - `--assignee ChristianGrimberg`.
   - `--label` con los labels `módulo:*` y `categoria:*` copiados del issue,
     más un label de tipología (`enhancement`/`bug`/`documentation`).
   - `--body` con la plantilla + cláusula `Closes #<issue>` cuando aplique.
6. Ejecuta el skill `lint-sql` y pega el reporte como comentario.
7. Verifica el PR resultante (`gh pr view`) y confirma que el cuerpo
   renderiza bien y que está en Draft.

## Cuándo invocarlo

- "Abrí el PR de la unidad 1.1.3"
- "Subí los cambios y abrime un PR"

## Inputs

| Parámetro | Tipo | Requerido | Descripción |
|---|---|---|---|
| `codigo_unidad` | string | sí | Código X.Y.Z |
| `slug` | string | sí | Slug de la carpeta de la unidad |
| `issue_numero` | int | recomendado | Issue que este PR cierra. Si se omite, se debe agregar `Closes #N` manualmente en el body antes de pasar el PR a listo. |
| `labels_extra` | CSV | opcional | Labels adicionales a sumar a los derivados del issue. |
| `mensaje_commit` | string | opcional | Si no se da, se genera uno a partir del front-matter. |

## Outputs

- Rama `feature/<codigo>-<slug>` pusheada.
- PR abierto en Draft en `https://github.com/ChristianGrimberg/dp800-practice/pulls`.
- Comentario de lint pegado al PR.
- Reporte de verificación post-creación.

## Convenciones aplicadas (ley del repo)

Estas reglas vienen de `CONTRIBUTING.md` y son obligatorias en todo PR abierto
por el skill. Saltarse alguna es un error.

| Regla | Cómo se aplica |
|---|---|
| PR siempre hacia `main` | `--base main` |
| PR siempre en Draft | `--draft` |
| PR asignado al owner | `--assignee ChristianGrimberg` |
| PR con `Closes #N` cuando venga de un issue | Se inyecta en el body antes de `gh pr create` |
| Rama basada en `origin/main` actualizado | `git fetch origin main && git checkout -b feature/<codigo>-<slug> origin/main` |
| Labels de módulo + categoría copiados del issue | Derivados con `gh issue view <n> --json labels` |
| Label de tipología | `enhancement` por defecto; `bug`/`documentation`/`chore` según correspondan |

## Pasos internos

```bash
# 0. Validar inputs y existencia del issue (si se proveyó)
ISSUE_NUMERO="${input.issue_numero}"
# (si ISSUE_NUMERO está vacío, el skill debe avisar al usuario que agregue
#  Closes #N manualmente en el PR antes de pasarlo a listo)

# 1. Validar front-matter (básicamente no nulo)
#    python3 scripts/validar-estructura.py

# 2. Garantizar que la rama nace de origin/main actualizado
git fetch origin main
git checkout -b "feature/<codigo>-<slug>" origin/main

# 3. Commit
git add .
git commit -m "<gitmoji> <verbo español> <alcance>"

# 4. Push
git push -u origin "feature/<codigo>-<slug>"

# 5. Derivar labels desde el issue (si ISSUE_NUMERO está presente)
ISSUE_LABELS=$(gh issue view "$ISSUE_NUMERO" --json labels \
  --jq '.labels[].name' \
  | grep -E '^(módulo:|categoria:)' | tr '\n' ',' | sed 's/,$//')
TIPO_LABEL=$(gh issue view "$ISSUE_NUMERO" --json labels --jq '.labels[].name' \
  | grep -E '^(enhancement|bug|documentation)$' | head -1)
[ -z "$TIPO_LABEL" ] && TIPO_LABEL="enhancement"
LABELS="${ISSUE_LABELS:+${ISSUE_LABELS},}${TIPO_LABEL}${EXTRA_LABELS:+,$EXTRA_LABELS}"

# 6. Preparar body con Closes #N
if [ -n "$ISSUE_NUMERO" ]; then
  CLOSES_LINE="Closes #${ISSUE_NUMERO}"
else
  CLOSES_LINE="N/A (PR de infra/fix, sin issue asociado)"
fi
# Se completa en el template reemplazando el placeholder

# 7. Abrir PR
gh pr create \
  --base main \
  --head "feature/<codigo>-<slug>" \
  --title "<gitmoji> Practicar Unidad X.Y.Z — <título>" \
  --body-file .github/PULL_REQUEST_TEMPLATE.md \
  --draft \
  --assignee ChristianGrimberg \
  --label "$LABELS"

# 8. Reemplazar el placeholder de Closes en el body (vía gh pr edit)
gh pr edit <pr_number> --body "$(cat .github/PULL_REQUEST_TEMPLATE.md | \
  sed "s|_ej. Closes #8_  |  | N/A**|$CLOSES_LINE|")"

# 9. Lint
bash scripts/lint-sql.sh <path-de-practica> | tee /tmp/lint.md
gh pr comment <pr_number> --body-file /tmp/lint.md

# 10. Verificación post-creación
gh pr view <pr_number> --json isDraft,assignees,labels,title,body \
  | jq '{isDraft, assignees: [.assignees[].login], labels: [.labels[].name]}'
#   Esperado:
#   { "isDraft": true,
#     "assignees": ["ChristianGrimberg"],
#     "labels":   ["módulo:1.1", "categoria:leccion", "enhancement"] (o similar) }

# 11. Confirmación visual del body
gh issue view <pr_number> --json body --jq '.body' \
  | grep -q '\\n' && {
      echo "WARN: el body contiene '\\n' literal, regenerar antes de mergear.";
      exit 1;
  }
```

## Restricciones

- **Nunca** pushear a `main` directamente.
- **Nunca** abrir PR sin haber commiteado algo (rama vacía falla).
- **Nunca** abrir PR sin la bandera `--draft`. El PR debe esperar la
  aprobación humana antes de salir de Draft.
- **Nunca** abrir PR sin assignee (siempre `ChristianGrimberg`).
- **Nunca** omitir `Closes #N` en PRs de contenido (los que cierran un
  issue de práctica/teoría).
- Si el front-matter no tiene los campos obligatorios, abortar y avisar.
- Si el lint falla con errores críticos, avisar antes de abrir el PR.
- Si el body del PR contiene `\\n` literales al verificar post-creación,
  el skill debe fallar y pedir regeneración del body antes de marcar el
  PR como listo.

## Ejemplo de invocación

```text
"Usá el skill abrir-pr-desde-capitulo para la unidad 1.1.3,
 issue asociado #8, branch feature/1.1.3-creacion-tablas"
```

## Post-condición esperada

El PR resultante debe cumplir **todas** estas condiciones al verificarlo
con `gh pr view <n> --json ...`:

```json
{
  "isDraft": true,
  "assignees": ["ChristianGrimberg"],
  "labels":   ["módulo:1.1", "categoria:leccion", "enhancement"],
  "title":    "✨ Practicar Unidad 1.1.3 — Creación de tablas",
  "body":     "...incluye 'Closes #8'..."
}
```

Si alguna falla, el skill debe reportar el problema al usuario y **no**
marcar el PR como listo para revisión.
