---
nombre: generar-dataset-sintetico
version: 1.0
idioma: es
agentes_recomendados:
  - generador-practicas
---

# Skill: generar-dataset-sintetico

## Qué hace

Genera `practica/01-preparacion.sql` con un dataset sintético realista para una unidad específica. Típicamente 2-5 tablas relacionadas, 50-500 filas totales, datos variados que permitan ejercitar los conceptos de la unidad.

## Cuándo invocarlo

- "Generame el dataset para practicar índices columnstore"
- "Armá el 01-preparacion.sql para la unidad 2.3.2"

## Inputs

- `codigo_unidad` o `tema` (string).
- `volumen` (opcional): bajo (~50), medio (~200), alto (~500). Default: medio.

## Outputs

Un archivo `practica/01-preparacion.sql` con:

1. Cabecera con comentario de origen.
2. `SET NOCOUNT ON;`.
3. `DROP ... IF EXISTS` para todas las tablas (idempotencia).
4. `CREATE TABLE` con tipos de datos apropiados al tema.
5. `INSERT` con datos variados:
   - Casos típicos.
   - Casos borde (NULLs, valores extremos).
   - Datos suficientes para que las consultas devuelvan resultados interesantes.
6. Validaciones `SELECT COUNT(*)` al final.

## Convenciones de estilo

- Nombres de objetos en `snake_case`.
- Esquema dedicado: `demo` o `<unidad_slug>`.
- Comentarios `-- PASO N` separando bloques lógicos.
- Datos plausibles (nombres, fechas, montos) pero **nunca reales**.

## Plantilla base

```sql
-- 01-preparacion.sql
-- Dataset sintético para la unidad X.Y.Z — <título>
-- Generado por el skill `generar-dataset-sintetico`.
--
-- Volumen: ~<N> filas en <M> tablas.
-- Re-ejecutable: incluye DROP IF EXISTS al inicio.

SET NOCOUNT ON;

-- Esquema dedicado
IF SCHEMA_ID('demo') IS NULL EXEC('CREATE SCHEMA demo');

-- PASO 1: tablas
IF OBJECT_ID('demo.<tabla_1>', 'U') IS NOT NULL DROP TABLE demo.<tabla_1>;
CREATE TABLE demo.<tabla_1> (
    id INT IDENTITY(1,1) PRIMARY KEY,
    -- ...
);

-- PASO 2: carga
INSERT INTO demo.<tabla_1> (<cols>) VALUES
    (...),
    (...);

-- PASO 3: validaciones
SELECT '<tabla_1>' AS tabla, COUNT(*) AS filas FROM demo.<tabla_1>;
```

## Restricciones

- **Nunca** incluir datos sensibles o personales reales.
- **Nunca** usar passwords hardcoded.
- Tablas y columnas deben ser autocontenidas (sin depender de objetos fuera de este archivo).
- Compatible con Azure SQL Edge como target principal.

## Ejemplo de invocación

```text
"Usá el skill generar-dataset-sintetico para la unidad 1.1.3 con volumen medio"
```
