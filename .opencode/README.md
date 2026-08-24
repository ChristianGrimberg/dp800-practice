# .opencode — Sistema de agentes y skills de dp800-practice

Este directorio define los **agentes** (`.opencode/agents/`) y **skills** (`.opencode/skills/`) que opencode puede invocar para acompañar el estudio del curso DP-800.

> ⚠️ **Importante**: leer [`AGENTS.md`](../../AGENTS.md) en la raíz del repo antes de usar cualquier agente o skill. Ahí está el routing estándar y las convenciones.

## Agentes

Los agentes definen **personalidades y capacidades**. Cada uno tiene un system prompt en español que determina cómo responde.

| Archivo | Agente | Cuándo se invoca |
|---|---|---|
| `agents/arquitecto-dp800.md` | arquitecto-dp800 | Planificar módulos/unidades nuevas |
| `agents/tutor-sql.md` | tutor-sql | Acompañar práctica activa (pair-programming) |
| `agents/generador-practicas.md` | generador-practicas | Crear `practica/*.sql` con dataset sintético |
| `agents/revisor-codigo-sql.md` | revisor-codigo-sql | Revisar SQL antes de commitear |
| `agents/documentador.md` | documentador | Redactar `teoria/*.md` con fuentes oficiales |

## Skills

Las skills definen **flujos concretos y entregables**. Cada una tiene un `SKILL.md` con inputs/outputs y restricciones.

| Skill | Disparador típico | Entregable |
|---|---|---|
| `skills/planificar-capitulo/` | "Planificá la unidad X.Y.Z" | Plan en Markdown con checklist |
| `skills/generar-dataset-sintetico/` | "Generame el dataset para X" | `practica/01-preparacion.sql` |
| `skills/practicar-concepto-sql/` | "Armame los ejercicios de X" | `practica/02-ejercicio.sql` + `03-solucion.sql` |
| `skills/explicar-concepto/` | "Redactá la teoría de X" | `teoria/concepto.md` + `sintaxis.md` + `preguntas-examen.md` |
| `skills/lint-sql/` | "Pasame lint" | Reporte en Markdown |
| `skills/abrir-pr-desde-capitulo/` | "Abrí el PR de X" | Rama + PR con plantilla + lint |
| `skills/buscar-capitulo-por-concepto/` | "¿Qué unidades hablan de X?" | Lista de unidades + snippets |
| `skills/preparar-siguiente-tema/` | "Enriqueceme el issue #N" | Comentario en el issue |
| `skills/sincronizar-con-curso-oficial/` | "Sincronizá con el curso oficial" | Reporte de drift |

## Cómo se invocan desde opencode

### Ejemplos en español

```text
"Usá el agente arquitecto-dp800 junto con el skill planificar-capitulo para
 armar el capítulo 'índices columnstore' en M1."

"Generá la práctica de la unidad 1.1.3 con el agente generador-practicas."

"Buscame todas las unidades que mencionan 'CTEs' con el skill buscar-capitulo-por-concepto."

"Pasame lint sobre los archivos modificados con el skill lint-sql."
```

### Combinaciones frecuentes

| Quiero... | Agente + Skill |
|---|---|
| Empezar una unidad nueva | `arquitecto-dp800` + `planificar-capitulo` |
| Practicar y luego documentar | `generador-practicas` + `practicar-concepto-sql` → `documentador` + `explicar-concepto` |
| Cerrar una unidad | `revisor-codigo-sql` + `lint-sql` → `abrir-pr-desde-capitulo` |
| Repasar antes del examen | `buscar-capitulo-por-concepto` |
| Enriquecer issue sugerido por el bot | `preparar-siguiente-tema` |
| Detectar drift del curso oficial | `sincronizar-con-curso-oficial` |

## Convención de nombres

- **Agentes**: `kebab-case` en español. Ej: `arquitecto-dp800`, `tutor-sql`.
- **Skills**: `kebab-case` en español. Ej: `planificar-capitulo`, `lint-sql`.
- Cada skill vive en una carpeta con `SKILL.md` (obligatorio) y opcionalmente `examples/` y `scripts/`.

## Idioma

- Toda la documentación, system prompts, descripciones y outputs son en **español**.
- Nombres de archivos de config técnica (`.yml`, `.json`, `.sql`) en inglés por convención.

## Restricciones globales

1. Ningún agente modifica archivos sin pedir confirmación.
2. Ningún agente hace commit/push sin invocar explícitamente `abrir-pr-desde-capitulo`.
3. Ningún agente crea archivos fuera de `curso/<path>/<modulo>/unidades/<codigo>/`.
4. Todos los outputs respetan `CONTRIBUTING.md`.
