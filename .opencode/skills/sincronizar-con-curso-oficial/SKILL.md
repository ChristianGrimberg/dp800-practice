---
nombre: sincronizar-con-curso-oficial
version: 1.0
idioma: es
agentes_recomendados:
  - arquitecto-dp800
---

# Skill: sincronizar-con-curso-oficial

## Qué hace

Compara el estado actual del repo local con el curso oficial en `ChristianGrimberg/DP-800` y reporta diferencias para que el usuario decida si actualizar.

Diferencias detectadas:

- **Unidades nuevas** en el curso oficial que no existen localmente.
- **Unidades renombradas** (cambio de título o slug).
- **Unidades con duración distinta**.
- **Cambios de URL** en Microsoft Learn.
- **Cambios de `uid`** en Microsoft Learn.

## Cuándo invocarlo

- "Sincronizá con el curso oficial"
- "¿Hay drift respecto al curso oficial?"
- "Comparame el JSON del curso con mi repo"

## Inputs

- `fuente_repo` (opcional, default `ChristianGrimberg/DP-800`).

## Outputs

Reporte en Markdown con tabla de diffs:

```markdown
## 🔄 Reporte de sincronización con ChristianGrimberg/DP-800

### Resumen

- 0 unidades nuevas
- 2 unidades con cambios de título
- 5 unidades con cambio de duración
- 1 unidad con cambio de URL

### Detalle

| Código | Campo | Antes | Ahora |
|---|---|---|---|
| 1.1.4 | duracion_min | 8 | 10 |
| 1.1.4 | titulo | Optimización con índices | Optimización con índices rowstore |
| 2.3.5 | url | https://... | https://... |

### Acción sugerida

- Para actualizar localmente: `bash scripts/sincronizar-curso.sh` (compara JSON).
- Para aplicar cambios al front-matter: revisar y abrir PRs individuales.
```

## Pasos internos

1. Descargar `course-hierarchy.json` del repo privado: `gh api repos/ChristianGrimberg/DP-800/contents/_meta/course-hierarchy.json`.
2. Comparar con `curso/_meta/course-hierarchy.json` local.
3. Recorrer todas las unidades locales y comparar:
   - `titulo` (case-insensitive).
   - `duracion_min`.
   - `url`.
   - `uid`.
4. Detectar unidades en el remoto que no existen localmente.
5. Generar el reporte.

## Restricciones

- **Nunca** modificar archivos automáticamente.
- **Nunca** commitear ni pushear.
- Solo lectura de GitHub vía `gh api`.
- Si no se puede acceder al repo privado, abortar con mensaje claro.

## Ejemplo de invocación

```text
"Usá el skill sincronizar-con-curso-oficial"
```
