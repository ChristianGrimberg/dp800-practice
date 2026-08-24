# Referencia rápida de sintaxis

## Firma

```sql
-- Sintaxis canónica
<FUNCION_O_SENTENCIA>(<parametros>)
```

## Variantes

```sql
-- Variante 1
SELECT ...;

-- Variante 2 (con opciones)
SELECT ...;
```

## Ejemplos mínimos

```sql
-- Mínimo 1: <caso simple>
SELECT 1;

-- Mínimo 2: <caso con condición>
SELECT * FROM dbo.<tabla> WHERE <condicion>;
```

## Notas de portabilidad entre SQL Server, Azure SQL y Fabric SQL

- _Diferencias conocidas entre plataformas (si las hay)._
