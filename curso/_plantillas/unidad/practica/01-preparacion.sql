-- 01-preparacion.sql
-- Crea el dataset sintético necesario para los ejercicios de esta unidad.
-- Por convención: todo lo necesario para empezar debe correr limpio en un
-- contenedor recién levantado (DB `dp800_lab` vacía).
--
-- Convención:
--   - DROP IF EXISTS al inicio para permitir re-ejecución idempotente.
--   - Comentarios -- PASO N para señalar cada bloque lógico.
--   - Volumen: 50–500 filas realistas por tabla.
--   - Sin uso de datos sensibles (todo sintético).

SET NOCOUNT ON;

-- Crear esquema dedicado para esta unidad (opcional).
IF SCHEMA_ID('demo') IS NULL EXEC('CREATE SCHEMA demo');

-- PASO 1: Definir tablas.
-- ...

-- PASO 2: Cargar dataset sintético.
-- ...

-- PASO 3: Validaciones rápidas.
-- SELECT COUNT(*) AS filas_demo FROM demo.<tabla>;
