---
nombre: explicar-concepto
version: 1.0
idioma: es
agentes_recomendados:
  - documentador
---

# Skill: explicar-concepto

## Qué hace

Redacta los archivos de `teoria/` para una unidad usando la URL oficial de Microsoft Learn como fuente primaria. Produce `concepto.md`, `sintaxis.md` y `preguntas-examen.md`.

## Cuándo invocarlo

- "Redactá la teoría de la unidad 1.1.3"
- "Explicame CTEs recursivas con analogías"
- "Generá las preguntas tipo examen para 2.3.2"

## Inputs

- `codigo_unidad` (string, requerido).
- `nivel` (opcional): basico | intermedio | avanzado. Default: intermedio.

## Outputs

Tres archivos Markdown con front-matter, siguiendo `curso/_plantillas/unidad/teoria/`.

### `teoria/concepto.md`

```markdown
---
origen_url: <url oficial>
fecha_consulta: <YYYY-MM-DD>
---

# Concepto: <título>

## Definición
<explicación en tus palabras, con analogía>

## Casos de uso reales
1. **<caso 1>**: <aplicación>
2. **<caso 2>**: <aplicación>
3. **<anti-patrón>**: cuándo NO usarlo

## Relación con el examen DP-800
<cómo aparece en preguntas típicas>

## Fuentes oficiales
- [Unidad oficial en Microsoft Learn (ES)](<origen_url>)
- [Documentación SQL Server — <tema>](https://learn.microsoft.com/es-es/sql/)
- [Azure SQL docs — <servicio>](https://learn.microsoft.com/es-es/azure/azure-sql/)

## Ver también
- Práctica: [practica/02-ejercicio.sql](../practica/02-ejercicio.sql)
- Glosario: [término](../../../recursos/glosario.md#termino)
```

### `teoria/sintaxis.md`

Referencia rápida con sintaxis canónica, variantes y ejemplos mínimos.

### `teoria/preguntas-examen.md`

3-5 preguntas tipo DP-800 con opciones A/B/C/D, respuesta correcta marcada y razonamiento.

## Pasos internos

1. Leer el front-matter de la unidad para obtener `url`, `titulo`, `duracion_min`, `path`, `modulo`, `codigo`.
2. Usar `webfetch` contra la `url` para extraer:
   - Objetivo de la unidad.
   - Conceptos cubiertos.
   - Ejemplos de código oficiales.
3. Adaptar el contenido al español neutro con analogías locales.
4. Generar preguntas siguiendo el formato del DP-800 (multiple choice, 4 opciones).

## Restricciones

- **Nunca** inventar URLs. Solo citar las del front-matter o las obtenidas por `webfetch`.
- **Nunca** traducir contenido con copyright desconocido. Si una explicación de Microsoft Learn es muy técnica, parafrasearla y citar.
- **Nunca** omitir la sección "Fuentes oficiales" en `concepto.md`.
- **Nunca** omitir el footer "Ver también".

## Ejemplo de invocación

```text
"Usá el skill explicar-concepto para la unidad 1.1.3 nivel intermedio"
```
