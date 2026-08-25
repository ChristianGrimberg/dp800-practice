---
tipo: Unidad
curso: 'Curso DP-800T00-A: Desarrollo de soluciones de base de datos habilitadas para IA'
codigo_curso: DP-800T00
path: "Path 1 — Diseño y desarrollo de soluciones de base de datos"
modulo: 'Módulo 1.1 — Diseño e implementación de objetos de base de datos con SQL'
unidad: 'Unidad 1.1.1 — Introducción'
codigo: 1.1.1
slug: 1.1.1-introduccion
categoria: introduccion
url: https://learn.microsoft.com/es-mx/training/modules/design-implement-database-objects/1-introduction/
uid: learn.wwl.design-implement-database-objects.1-introduction
duracion_min: 3
fecha_actualizacion: '2026-08-25'
estado: hecho
fecha_inicio: '2026-08-25'
fecha_fin: '2026-08-25'
ultimo_repaso: '2026-08-25'
proximo_repaso: '2026-09-25'
pr: 7
conceptos:
  - objetos de base de datos
  - rowstore vs columnstore
  - tablas en memoria
  - tablas temporales
  - tablas externas
  - tablas LEDGER
  - tablas GRAPH
  - restricciones (PK, FK, UNIQUE, CHECK, DEFAULT)
  - columnas JSON
  - objetos SEQUENCE
  - particionamiento de tablas e índices
  - Azure SQL Database
  - Azure SQL Managed Instance
  - SQL Database en Microsoft Fabric
nivel: intermedio
prerequisitos: []
esfuerzo: corto
---

# Unidad 1.1.1 — Introducción

**Fuente oficial**: [Unidad en Microsoft Learn (ES)](https://learn.microsoft.com/es-mx/training/modules/design-implement-database-objects/1-introduction/)

**Duración estimada**: 3 minutos · **Categoría**: introduccion

> **Resumen**: las decisiones de diseño de objetos de base de datos son mucho más permanentes que el
> código de aplicación — elegir mal el tipo de tabla hoy puede bloquear producción mañana. Esta unidad
> presenta los cinco ejes temáticos del módulo y las plataformas donde correrán.

## Objetivo

Al terminar esta unidad vas a poder **explicar por qué las decisiones de diseño de objetos de base de
datos son más permanentes que el código de aplicación**, identificar las cinco familias de objetos
especializados que vas a usar durante el módulo y ubicar en qué plataforma corre cada uno (SQL Server /
Azure SQL DB / Azure SQL MI / SQL DB en Fabric).

## Checklist de la unidad

- [x] Leer la unidad oficial en Microsoft Learn
- [x] Anotar conceptos clave en `conceptos:` del front-matter
- [x] Redactar `teoria/concepto.md` con analogía y casos de uso
- [x] Crear `teoria/sintaxis.md` (placeholder — no introduce sintaxis nueva)
- [x] Crear `teoria/preguntas-examen.md` con 5 preguntas razonadas
- [x] Actualizar `estado: hecho` y `fecha_fin` en este front-matter
- [x] Abrir PR #7

> _Esta unidad no requiere `practica/` por ser `categoria: introduccion`. El laboratorio práctico
> integrado aparece en la unidad **1.1.9 — Ejercicio: Creación y mantenimiento de objetos de base de
> datos**._

## Estructura de archivos de esta unidad

```
.
├── README.md                  # este archivo (front-matter + checklist)
└── teoria/
    ├── concepto.md            # definición + analogía + casos de uso + fuentes
    ├── sintaxis.md            # placeholder: no hay sintaxis nueva
    └── preguntas-examen.md    # 5 preguntas tipo DP-800
```

## Resumen de la unidad

Esta unidad es la puerta de entrada conceptual al módulo **1.1**. Su única pretensión es que, antes de
escribir tu primer `CREATE TABLE` o `CREATE INDEX`, entiendas que **la elección del tipo de objeto es
una decisión arquitectónica**, no un detalle de implementación. En las próximas unidades vas a ver la
sintaxis concreta para cada objeto, pero el "por qué" se sostiene en estas tres ideas:

1. **Lo que diseñás hoy migra con dolor mañana.** Pasar de rowstore a columnstore, agregar historial
   temporal o cambiar `IDENTITY` por `SEQUENCE` no son "optimizaciones que se agregan después": son
   migraciones que pueden dejar tablas bloqueadas durante horas.

2. **Los objetos especializados cambian el motor, no solo el rendimiento.** Tablas en memoria, temporales,
   externas, LEDGER y GRAPH no son "extras": alteran cómo el motor almacena, consulta y valida los
   datos desde el inicio.

3. **Cada plataforma tiene su superset.** SQL Server, Azure SQL DB, Managed Instance y Fabric SQL
   comparten la base, pero cada una expone un subconjunto distinto de objetos avanzados. La elección
   correcta depende de la plataforma donde vas a correr.

Las próximas unidades (1.1.2 a 1.1.8) bajan a sintaxis concreta siguiendo los cinco ejes temáticos
presentados acá: tablas → tipos especializados → restricciones → JSON/Sequence → particiones.

## Próxima unidad

> **1.1.2 — Descripción de las opciones de la plataforma basada en SQL Server** _(se calcula
> automáticamente al hacer merge a `main` vía workflow `siguiente-tema.yml`)_