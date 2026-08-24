---
nombre: lint-sql
version: 1.0
idioma: es
agentes_recomendados:
  - revisor-codigo-sql
---

# Skill: lint-sql

## Qué hace

Corre `sqlfluff` sobre archivos `.sql` modificados o sobre todo el directorio `practica/` y produce un reporte en Markdown listo para pegar como comentario de PR.

## Cuándo invocarlo

- "Pasame lint sobre mis cambios"
- "Correme sqlfluff y mostrame el reporte"
- "Validá el SQL antes de commitear"

## Inputs

- `paths` (opcional): archivos o directorios a lintar. Default: archivos modificados vs `main`.

## Outputs

Reporte en Markdown:

```markdown
## 🔍 Reporte de sqlfluff

**Archivos analizados**: <N>
**Errores**: <N>
**Warnings**: <N>

### Hallazgos

| Archivo | Línea | Regla | Severidad | Descripción |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

### Comandos sugeridos

```bash
# Fix automático (cuidado: revisar diff antes de commitear)
sqlfluff fix curso/.../practica/ --dialect tsql
```
```

## Pasos internos

1. Identificar paths a lintar (argumento o git diff contra main).
2. Ejecutar `sqlfluff lint --dialect tsql --format json <paths>`.
3. Parsear el JSON y formatear como Markdown.
4. Agregar comandos de fix automático.

## Restricciones

- **Nunca** aplicar fix automático sin pedir confirmación.
- Solo lintar dialecto `tsql`.
- Si no hay sqlfluff instalado, dar instrucciones de instalación.

## Ejemplo de invocación

```text
"Usá el skill lint-sql sobre los archivos modificados"
```
