# Referencia rápida de sintaxis — Unidad 1.1.1

> **Nota**: esta unidad es introductoria al módulo 1.1 y **no introduce sintaxis nueva**. Su objetivo es
> sentar el contexto conceptual para que las decisiones de las próximas unidades tengan fundamento.
>
> La referencia rápida de sintaxis aparecerá en cada lección específica:
>
> - **Unidad 1.1.2** — `CREATE TABLE` básico y tipos de datos.
> - **Unidad 1.1.3** — `CREATE TABLE` eficaz + constraints inline.
> - **Unidad 1.1.4** — `CREATE INDEX` (rowstore y columnstore).
> - **Unidad 1.1.5** — Tipos de tabla especializados (memory-optimized, temporal, external, ledger, graph).
> - **Unidad 1.1.6** — Restricciones (PK, FK, UNIQUE, CHECK, DEFAULT).
> - **Unidad 1.1.7** — Columnas e índices JSON.
> - **Unidad 1.1.8** — `PARTITION FUNCTION` / `PARTITION SCHEME`.

## Mapa conceptual de los objetos que verás

```text
┌─ Objetos de base de datos (este módulo) ────────────────────────────┐
│                                                                     │
│  ┌─ Tablas ───────────────────────────────────────────────────────┐  │
│  │  • Estándar (rowstore)            → 1.1.2, 1.1.3               │  │
│  │  • Columnstore                    → 1.1.4                      │  │
│  │  • Especializadas:                → 1.1.5                      │  │
│  │      ◦ Memory-optimized                                         │  │
│  │      ◦ Temporal (con historial)                                 │  │
│  │      ◦ External (lee de Fabric/ADLS)                            │  │
│  │      ◦ Ledger (blockchain-like)                                 │  │
│  │      ◦ Graph (nodos + aristas)                                  │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─ Restricciones ──────────────── 1.1.6 ────────────────────────┐  │
│  │  PRIMARY KEY · FOREIGN KEY · UNIQUE · CHECK · DEFAULT           │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─ JSON + índices JSON ─────────── 1.1.7 ────────────────────────┐  │
│  │  NVARCHAR(MAX) + JSON_VALUE / JSON_QUERY / ISJSON              │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─ Particiones ─────────────────── 1.1.8 ────────────────────────┐  │
│  │  PARTITION FUNCTION · PARTITION SCHEME · $PARTITION            │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─ Práctica integrada ─────────── 1.1.9 ────────────────────────┐  │
│  │  Lab: crear y mantener objetos de base de datos                │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Convención de unidades que sí tienen sintaxis

Cuando una unidad sí enseña una sentencia, el archivo `teoria/sintaxis.md` sigue siempre esta estructura:

1. **Firma** — la sintaxis canónica, en bloque `sql`.
2. **Variantes** — las opciones más usadas.
3. **Ejemplos mínimos** — uno o dos queries autocontenidos.
4. **Notas de portabilidad** — diferencias entre SQL Server, Azure SQL DB, Managed Instance y Fabric.

Por ahora, este archivo sirve únicamente como índice del módulo.

## Notas de portabilidad entre SQL Server, Azure SQL y Fabric SQL

No hay sentencia para portar todavía. Lo que sí vale la pena anotar desde el inicio:

- **Funcionalidades comunes a las 4 plataformas**: tablas estándar, restricciones, JSON, índices rowstore.
- **Solo SQL Server + Managed Instance**: memory-optimized tables, native compilation.
- **Solo Azure SQL Database**: tier Hyperscale con partitioning elástico.
- **Solo Fabric SQL**: tablas externas sobre OneLake, integración nativa con Lakehouse.

Estos matices se retomarán cuando llegues a la unidad específica.