---
origen_url: https://learn.microsoft.com/es-mx/training/modules/design-implement-database-objects/1-introduction/
fecha_consulta: 2026-08-25
---

# Concepto: Introducción al diseño de objetos de base de datos

> **Resumen en una línea**: diseñar objetos de base de datos es plantar los cimientos del sistema;
> cambiar una tabla es como cambiar los cimientos de un edificio, mientras que cambiar una clase de C#
> es como redecorar un departamento.

## Definición

Cuando trabajás como desarrollador de SQL, las decisiones que tomás sobre cómo modelar los **objetos de base de datos** (tablas, índices, restricciones, tipos especializados, particiones) son
mucho
más permanentes que el código de aplicación. Mientras que una clase de C# se puede refactorizar con impacto mínimo o un microservicio se puede reescribir sin tocar el resto del sistema, una tabla
no
se migra así nomás.

Algunos cambios típicos que parecen inofensivos terminan siendo caros:

- Pasar de **almacén de filas** (*rowstore*) a **almacén de columnas** (*columnstore*).
- Activar el seguimiento del historial **temporal** sobre una tabla existente.
- Sustituir una columna **IDENTITY** por un objeto **SEQUENCE**.

Cada uno de estos cambios puede dejar la tabla bloqueada durante horas y tirar abajo sistemas en producción. Por eso, los objetos especializados que vas a ver en este módulo no son
"optimizaciones que
se agregan después": alteran cómo el motor almacena, consulta y valida los datos desde el inicio. Elegir una tabla estándar cuando necesitás auditoría temporal te obliga después a escribir
triggers y
tablas de historial a mano. Elegir `IDENTITY` cuando tu arquitectura pide secuencias distribuidas te obliga a parchear la generación de IDs desde la capa de aplicación.

La conclusión práctica: **comprender estos objetos antes de implementarlos te permite diseñar sistemas que evolucionan sin reescrituras dolorosas**, habilitando después capacidades como
verificación
al estilo *blockchain* (LEDGER), caché de latencia en milisegundos (en memoria) o análisis en tiempo real sobre series de tiempo (Fabric + particiones), cosas que son muy difíciles de agregar
cuando
ya te comprometiste con otra forma de almacenamiento.

## Qué vas a aprender en este módulo

El módulo **1.1** recorre cinco ejes temáticos. Cada uno se desarrolla en profundidad en las unidades 1.1.2 a 1.1.8 y se practica en 1.1.9:

### 1. Diseño e implementación de tablas

Crear tablas con los **tipos de datos**, tamaños y estructuras correctos. Aprenderás a decidir entre **índices rowstore** (transaccionales) y **columnstore** (analíticos) según la carga de
trabajo.
Esto vale tanto para una app transaccional en Azure SQL Database como para una base de análisis operativo en Fabric SQL.

### 2. Tipos de tabla especializados

- **En memoria** (memory-optimized): escenarios de alta concurrencia y latencia baja en SQL Managed Instance.
- **Temporales**: auditoría y viajes en el tiempo en todas las plataformas.
- **Externas**: integración con el Fabric Lakehouse.
- **LEDGER**: integridad al estilo blockchain para aplicaciones de cumplimiento.
- **GRAPH**: modelar relaciones complejas (nodos y aristas).

### 3. Restricciones y validación

Implementar las cinco restricciones que sostienen la integridad de los datos: **PRIMARY KEY**, **FOREIGN KEY**, **UNIQUE**, **CHECK** y **DEFAULT**. Sirven igual para un microservicio, una
aplicación
empresarial o pipelines analíticos.

### 4. Características avanzadas

- Columnas **JSON** para esquemas flexibles en aplicaciones nativas de nube.
- Índices optimizados para el motor de consultas de la plataforma.
- Objetos **SEQUENCE** para generación de IDs distribuidos.

### 5. Estrategias de particiones

Diseñar e implementar particiones de tablas e índices para bases de datos a gran escala. Esencial en tres escenarios:

- **Azure SQL Database Hyperscale** (escala elástica).
- Bases de datos multi-TB en **SQL Managed Instance**.
- Datos de **serie temporal** en bases operativas de **Fabric SQL**.

## Casos de uso reales

### Caso 1 — Banco con auditoría regulatoria

Una fintech necesita reconstruir el estado de una cuenta en cualquier fecha de los últimos siete años para cumplir con el regulador. Si la tabla de saldos se diseñó como una tabla estándar desde
el
primer día, hay que escribir triggers, mantener una tabla espejo y rezar para que no se desincronicen. Si se diseñó como **tabla temporal**, el motor lo hace solo y la consulta es `FOR
SYSTEM_TIME AS
OF <fecha>`.

### Caso 2 — E-commerce con catálogo flexible

Un marketplace agrega cada semana atributos nuevos a los productos (color, talla, voltaje, certificación). Si la tabla `Producto` se modeló con columnas fijas, cada cambio es una migración
dolorosa.
Si se modeló con una **columna JSON** + un índice sobre las claves más consultadas, agregar un atributo es cambiar una línea de INSERT sin DDL.

### Caso 3 — IoT con series de tiempo en Fabric

Una planta industrial-ingiere 50.000 lecturas por segundo de sensores. Si la tabla de mediciones no está particionada por fecha, una consulta del último mes escanea toda la tabla. Si está
particionada
por día y la consulta pide un rango, el motor salta particiones enteras y devuelve en milisegundos.

### Anti-patrón — Elegir `IDENTITY` por defecto para todo

`IDENTITY` funciona bien para una sola base de datos. Pero cuando tenés **múltiples shards** o un patrón de **merge replication**, `IDENTITY` te obliga a pedir rangos disjuntos a mano y se vuelve
una
fuente de bugs. La elección correcta en ese caso es un objeto `SEQUENCE` global o un servicio de IDs distribuido.

## Por qué esto importa en el examen DP-800

Las preguntas del examen casi nunca preguntan "¿qué hace una tabla?" — eso lo sabés. Lo que preguntan es **escenarios de decisión**:

- "Tenés auditoría regulatoria y 50 TB de datos históricos. ¿Qué combinación de objetos usás?" (Tabla temporal + particiones + Ledger, probablemente).
- "Necesitás generar IDs únicos entre 12 sucursales. ¿IDENTITY, SEQUENCE o GUID?" (SEQUENCE o GUID con `NEWSEQUENTIALID`, depende del matiz).
- "Tu consulta analítica es lenta en una tabla transaccional. ¿Índice columnstore o partición?" (Columnstore si la cardinalidad lo permite; partición si el problema es el volumen).

Por eso, este módulo no se trata de memorizar tipos: se trata de **reconocer en qué escenario cada objeto es la herramienta correcta**.

## Plataformas objetivo

Todo el contenido del módulo aplica a las cuatro plataformas que la certificación cubre:

| Plataforma | Caso típico |
|---|---|
| **SQL Server** (on-premises o VMs) | Apps tradicionales, ERP, sistemas legacy. |
| **Azure SQL Database** | SaaS nuevo, escala elástica con Hyperscale, serverless. |
| **Azure SQL Managed Instance** | Migración lift-and-shift desde SQL Server, alta compatibilidad. |
| **SQL Database en Microsoft Fabric** | Data warehouse + análisis operacional sobre OneLake. |

Cada plataforma tiene matices: por ejemplo, las **tablas en memoria** están disponibles en Managed Instance y SQL Server, pero **no** en Azure SQL Database sin servidor. Esos detalles se cubren
en las
unidades específicas (1.1.5, 1.1.7).

## Relación con el examen DP-800

Esta unidad en sí no es "pregunta de examen" — es contexto. Pero las siguientes del módulo sí caen típicamente en preguntas tipo:

- "Elegir el tipo de tabla apropiado" → dominio *Design and implement database objects* (20-25% del examen).
- "Decidir entre tipos de restricciones" → mismo dominio.
- "Particionar una tabla" → dominio *Optimize database performance* (15-20%).
- "Diseñar esquema para IA / RAG" → cruza con Path 3 (este módulo es la base).

## Fuentes oficiales

- [Unidad oficial en Microsoft Learn (ES)](https://learn.microsoft.com/es-mx/training/modules/design-implement-database-objects/1-introduction/)
- [Documentación de SQL Server — Diseñar tablas](https://learn.microsoft.com/es-es/sql/relational-databases/tables/tables)
- [Azure SQL — Tipos de tablas especializadas](https://learn.microsoft.com/es-es/azure/azure-sql/)
- [SQL Database en Microsoft Fabric — overview](https://learn.microsoft.com/es-es/fabric/database/sql/overview)
- [Data Exposed (video)](https://learn.microsoft.com/shows/data-exposed/) — buscar "database object design"

## Ver también

- Próxima unidad: [Unidad 1.1.2 — Descripción de las opciones de la plataforma basada en SQL Server](../../1.1.2-descripcion-de-las-opciones-de-la-plataforma-basada-en-sql-server/README.md)
- Glosario:
  [**objetos de base de datos**](../../../../../_extras/glosario.md#restricciones),
  [**rowstore vs columnstore**](../../../../../_extras/glosario.md#índices),
  [**tablas temporales**](../../../../../_extras/glosario.md#tablas-temporales),
  [**particionamiento**](../../../../../_extras/glosario.md#particionamiento),
  [**SQL Database en Microsoft Fabric**](../../../../../_extras/glosario.md#sql-database-en-microsoft-fabric)
- Aparece en: Path 1 → Módulo 1.1 → Unidad 1.1.1