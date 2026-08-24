---
nombre: practicar-concepto-sql
version: 1.0
idioma: es
agentes_recomendados:
  - generador-practicas
---

# Skill: practicar-concepto-sql

## Qué hace

Genera `practica/02-ejercicio.sql` y `practica/03-solucion.sql` con 3 a 5 ejercicios progresivos para una unidad específica. Los ejercicios crecen en dificultad y combinan los conceptos de la unidad.

## Cuándo invocarlo

- "Armame los ejercicios de la unidad 1.1.3"
- "Generá 02-ejercicio.sql y 03-solucion.sql para índices columnstore"

## Inputs

- `codigo_unidad` o `concepto` (string).
- `cantidad_ejercicios` (opcional): 3-5. Default: 4.

## Outputs

### `practica/02-ejercicio.sql`

```sql
-- 02-ejercicio.sql
-- Ejercicios progresivos para la unidad X.Y.Z — <título>
-- Generado por el skill `practicar-concepto-sql`.

USE dp800_lab;
SET NOCOUNT ON;

-- EJERCICIO 1: <título corto>
-- Objetivo: <qué se prueba>
-- Resultado esperado: <qué debería devolver>

/*
-- Escribí tu SQL acá.
SELECT 1;
*/


-- EJERCICIO 2: <título corto>
-- ...

-- EJERCICIO 3: <combinando 1 y 2>
-- ...

-- EJERCICIO 4: <caso más complejo / optimizable>
-- ...
```

### `practica/03-solucion.sql`

```sql
-- 03-solucion.sql
-- Soluciones comentadas para los ejercicios de 02-ejercicio.sql.

USE dp800_lab;
SET NOCOUNT ON;

-- EJERCICIO 1
-- POR QUÉ: <decisión de diseño>
SELECT ... ;


-- EJERCICIO 2
-- POR QUÉ: ...
SELECT ... ;
```

## Convenciones

- Cada ejercicio es **autocontenido** (no depende de variables de sesión ni de outputs anteriores).
- Numeración correlativa, títulos claros.
- El SQL del usuario en `02-ejercicio.sql` queda como comentario entre `/* */`.
- Las soluciones en `03-solucion.sql` incluyen `-- POR QUÉ:` para decisiones no triviales.
- Si hay más de una forma válida, mostrar la principal y mencionar la variante en un comentario.

## Restricciones

- Las soluciones deben correr limpias en Azure SQL Edge.
- No incluir ejercicios que requieran dependencias externas (Azure, Fabric) sin avisar.
- No incluir secretos, ni siquiera como ejemplo.

## Ejemplo de invocación

```text
"Usá el skill practicar-concepto-sql para la unidad 1.1.3 con 4 ejercicios"
```
