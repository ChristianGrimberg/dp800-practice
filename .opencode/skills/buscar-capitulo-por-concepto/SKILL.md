---
nombre: buscar-capitulo-por-concepto
version: 1.0
idioma: es
agentes_recomendados:
  - documentador
  - tutor-sql
---

# Skill: buscar-capitulo-por-concepto

## Qué hace

Busca dentro del repositorio todas las unidades que mencionan un concepto dado (ya sea en el campo `conceptos:` del front-matter, en el texto de `teoria/concepto.md`, o en el glosario). Devuelve links directos y snippets relevantes para repaso rápido.

## Cuándo invocarlo

- "¿Qué unidades hablan de índices columnstore?"
- "Encontrame todas las menciones a CTEs"
- "Repaso de Always Encrypted: ¿qué unidades lo cubren?"

## Inputs

- `concepto` (string, requerido).
- `incluir_practica` (opcional, default true): buscar también dentro de archivos `.sql`.

## Outputs

Markdown con:

1. **Coincidencias en front-matter** (más confiable).
2. **Coincidencias en teoria/** (snippets).
3. **Coincidencias en glosario** (definición rápida).
4. **Coincidencias en practica/** (si se pidió).

```markdown
## 🔎 Búsqueda: "índices columnstore"

### En front-matter de unidades

| Código | Unidad | Campo | Valor |
|---|---|---|---|
| 1.1.4 | Optimización con índices | `conceptos` | [índice columnstore, ...] |
| 1.1.5 | Tipos de tabla especializados | `conceptos` | [índice columnstore, ...] |

### En teoria/

- **1.1.4/teoria/concepto.md** L23: "...los índices columnstore almacenan los datos por columna en lugar de por fila..."

### En glosario

- [Índices](../../../recursos/glosario.md#indices): _definición breve..._

### Sugerencia de repaso

```dataview
LIST unidad
FROM "curso"
WHERE contains(conceptos, "índices columnstore")
SORT codigo ASC
```
```

## Pasos internos

1. Buscar en `curso/**/unidades/*/README.md` el campo `conceptos:` del front-matter usando `ripgrep` con multiline.
2. Buscar el término en `curso/**/unidades/*/teoria/*.md`.
3. Buscar en `recursos/glosario.md`.
4. Si `incluir_practica=true`, buscar en `curso/**/unidades/*/practica/*.sql`.
5. Formatear y devolver.

## Restricciones

- Búsqueda insensible a mayúsculas/minúsculas y acentos.
- Si no hay coincidencias, sugerir términos cercanos usando fuzzy matching.
- Solo buscar dentro del repo local (no salir a internet).

## Ejemplo de invocación

```text
"Usá el skill buscar-capitulo-por-concepto para 'índices columnstore'"
```
