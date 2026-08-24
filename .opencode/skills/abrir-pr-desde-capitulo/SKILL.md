---
nombre: abrir-pr-desde-capitulo
version: 1.0
idioma: es
agentes_recomendados:
  - arquitecto-dp800
---

# Skill: abrir-pr-desde-capitulo

## Qué hace

Automatiza la apertura de un PR para una unidad del curso, siguiendo la convención del repo:

1. Verifica que el front-matter esté completo.
2. Crea la rama `feature/<codigo>-<slug>`.
3. Hace commit con mensaje gitmoji + español.
4. Pushea.
5. Abre PR usando `gh pr create --fill` con la plantilla del repo.
6. Ejecuta el skill `lint-sql` y pega el reporte como comentario.

## Cuándo invocarlo

- "Abrí el PR de la unidad 1.1.3"
- "Subí los cambios y abrime un PR"

## Inputs

- `codigo_unidad` (string, requerido).
- `mensaje_commit` (opcional): si no se da, se genera uno a partir del front-matter.

## Outputs

- Rama `feature/<codigo>-<slug>` pusheada.
- PR abierto en `https://github.com/ChristianGrimberg/dp800-practice/pulls`.
- Comentario de lint pegado al PR.

## Pasos internos

```bash
# 1. Validar front-matter (básicamente no nulo)
# 2. Crear rama
git checkout -b feature/<codigo>-<slug>

# 3. Commit
git add .
git commit -m "<gitmoji> <verbo español> <alcance>"

# 4. Push
git push -u origin feature/<codigo>-<slug>

# 5. PR
gh pr create \
  --base main \
  --head feature/<codigo>-<slug> \
  --title "<gitmoji> Practicar Unidad X.Y.Z — <título>" \
  --body-file .github/PULL_REQUEST_TEMPLATE.md \
  --fill

# 6. Lint
bash scripts/lint-sql.sh <path-de-practica> | tee /tmp/lint.md
gh pr comment <pr_number> --body-file /tmp/lint.md
```

## Restricciones

- **Nunca** pushear a `main` directamente.
- **Nunca** abrir PR sin haber commiteado algo (rama vacía falla).
- Si el front-matter no tiene los campos obligatorios, abortar y avisar.
- Si el lint falla con errores críticos, avisar antes de abrir el PR.

## Ejemplo de invocación

```text
"Usá el skill abrir-pr-desde-capitulo para la unidad 1.1.3"
```
