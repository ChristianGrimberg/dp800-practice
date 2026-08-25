# Preguntas tipo examen DP-800 — Unidad 1.1.1

> 5 preguntas de opción múltiple estilo DP-800, basadas en el contenido de esta unidad introductoria. Sirven para fijar el "por qué" antes de pasar a la sintaxis de las próximas unidades.

---

## Pregunta 1 — Permanencia del diseño

**Enunciado**: Tu equipo mantiene una clase `Pedido` en C# y una tabla `Pedido` en SQL Server. El negocio pide cambiar la lógica de cálculo de impuestos. ¿Cuál de las siguientes afirmaciones
describe mejor la diferencia en costo de cambio entre el código y la tabla?

**Opciones**:

- A) El cambio en la tabla es más barato porque solo se modifica el `CREATE TABLE`.
- B) El cambio en el código de C# y en la tabla cuestan exactamente lo mismo.
- C) El cambio en el código de C# suele ser más barato porque podés refactorizar la clase sin migrar
  datos, mientras que un cambio en la tabla (por ejemplo, pasar de rowstore a columnstore) puede requerir
  migración y dejar la tabla bloqueada.
- D) El cambio en la tabla es imposible una vez creada.

**Respuesta correcta**: **C**

**Razonamiento**: La unidad enfatiza que las decisiones de diseño de objetos de base de datos son más permanentes que el código de aplicación. Cambiar una clase C# es comparable a redecorar un
departamento; cambiar una tabla es comparable a cambiar los cimientos de un edificio. La opción A confunde "barato" con "simple": modificar el DDL no significa que sea barato en producción. La
opción B ignora el costo de migración. La opción D es falsa — la tabla puede cambiarse, pero el costo es alto.

**Fuentes**:

- [Unidad 1.1.1 oficial (ES)](https://learn.microsoft.com/es-mx/training/modules/design-implement-database-objects/1-introduction/)

---

## Pregunta 2 — Tablas temporales y plataforma

**Enunciado**: ¿En cuál de las siguientes plataformas **NO** están soportadas las tablas temporales con historial gestionado por el motor (system-versioned temporal tables)?

**Opciones**:

- A) SQL Server 2016 o superior.
- B) Azure SQL Database.
- C) Azure SQL Managed Instance.
- D) En ninguna de las tres anteriores: las tres plataformas las soportan.

**Respuesta correcta**: **D**

**Razonamiento**: La unidad introduce las tablas temporales como un tipo especializado aplicable "en todas las plataformas" (SQL Server, Azure SQL DB, Managed Instance y SQL Database en Fabric).
La trampa del examen suele ser asumir que una característica está restringida cuando en realidad fue portada. Las system-versioned temporal tables están disponibles en SQL Server desde 2016, en
Azure SQL DB y en Managed Instance; en Fabric SQL se accede vía el warehouse con mecanismos equivalentes. Por eso, la respuesta correcta es "ninguna de las anteriores".

**Fuentes**:

- [Unidad 1.1.1 oficial (ES)](https://learn.microsoft.com/es-mx/training/modules/design-implement-database-objects/1-introduction/)
- [Documentación de tablas temporales](https://learn.microsoft.com/es-es/sql/relational-databases/tables/temporal-tables)

---

## Pregunta 3 — Tablas LEDGER

**Enunciado**: Una empresa farmacéutica necesita demostrar que los registros de producción de un lote no fueron modificados después de su certificación, ni siquiera por un DBA con acceso total al
servidor. ¿Qué tipo de tabla especializada es la más apropiada?

**Opciones**:

- A) Tabla **temporal** con `SYSTEM_VERSIONING = ON`.
- B) Tabla **memory-optimized** con `DURABILITY = SCHEMA_AND_DATA`.
- C) Tabla **LEDGER** con `LEDGER = ON`.
- D) Tabla **external** apuntando a un archivo inmutable en OneLake.

**Respuesta correcta**: **C**

**Razonamiento**: Las tablas LEDGER están diseñadas específicamente para ese caso de uso: integridad al estilo blockchain donde ni siquiera un administrador puede alterar los datos sin dejar
evidencia criptográfica. La opción A (temporal) te da historial pero no te protege contra modificaciones maliciosas. La opción B (memory-optimized) optimiza latencia, no integridad. La opción D
(external) puede ayudar como capa de inmutabilidad física, pero requiere toda una pipeline adicional y no es el mecanismo nativo de SQL Server.

**Fuentes**:

- [Unidad 1.1.1 oficial (ES)](https://learn.microsoft.com/es-mx/training/modules/design-implement-database-objects/1-introduction/)
- [Azure SQL Database — tablas ledger](https://learn.microsoft.com/es-es/azure/azure-sql/database/ledger-atabase)

---

## Pregunta 4 — `IDENTITY` vs `SEQUENCE`

**Enunciado**: Estás diseñando un sistema de pedidos que se va a desplegar en 8 sucursales, cada una con su propia base de datos local, y todas deben consolidar IDs únicos a nivel global sin
colisiones. ¿Qué mecanismo de generación de IDs es el más apropiado?

**Opciones**:

- A) Una columna `IDENTITY(1,1)` por sucursal con rangos disjuntos preasignados manualmente.
- B) Una columna `UNIQUEIDENTIFIER` con `DEFAULT NEWID()`.
- C) Un objeto `SEQUENCE` compartido entre sucursales vía linked server.
- D) Un objeto `SEQUENCE` por sucursal con rangos disjuntos, o un servicio externo de IDs distribuidos, según la latencia tolerable.

**Respuesta correcta**: **D**

**Razonamiento**: El anti-patrón típico es caer en la opción A: usar `IDENTITY` por sucursal con rangos "manualmente" preasignados funciona, pero es frágil — cuando una sucursal consume más
rápido de lo previsto y otra no, hay que renegociar rangos, lo cual reintroducir el problema original. La opción B (`NEWID`) es correcta funcionalmente pero genera IDs aleatorios de 16 bytes y
consume más índice. La opción C (`SEQUENCE` compartido por linked server) introduce latencia de red en cada INSERT. La opción D reconoce que `SEQUENCE` es la herramienta correcta para generar
rangos disjuntos sin acoplamiento por red y, si la latencia es inaceptable, se delega a un servicio externo (Snowflake-style IDs). Esta es la respuesta más alineada con la unidad.

**Fuentes**:

- [Unidad 1.1.1 oficial (ES)](https://learn.microsoft.com/es-mx/training/modules/design-implement-database-objects/1-introduction/)
- [CREATE SEQUENCE (Transact-SQL)](https://learn.microsoft.com/es-es/sql/t-sql/statements/create-sequence-transact-sql)

---

## Pregunta 5 — Particionamiento y escala

**Enunciado**: Tenés una tabla de hechos de ventas con 8 TB de datos históricos en Azure SQL Database. El equipo de analítica reporta que las consultas sobre los últimos 30 días tardan más de 40
segundos porque escanean toda la tabla. ¿Qué estrategia de objetos ofrece la mejora más directa **sin** cambiar la plataforma?

**Opciones**:

- A) Convertir toda la tabla a **columnstore index** clustered.
- B) Implementar **particionamiento por fecha** sobre la tabla y los índices aligned.
- C) Crear un índice rowstore non-clustered sobre la columna de fecha.
- D) Mover la tabla a una **tabla externa** en Fabric OneLake.

**Respuesta correcta**: **B**

**Razonamiento**: La unidad menciona explícitamente que las estrategias de partición son esenciales para "bases de datos a gran escala" y "datos de serie temporal en bases operativas de Fabric".
Cuando una consulta pide un rango de fechas, una tabla particionada por fecha permite al motor **saltar particiones enteras** (partition elimination), reduciendo drásticamente la I/O. La opción A
(columnstore) ayuda en consultas analíticas con muchas agregaciones, pero no es la solución más directa para "filtrar por rango de fecha". La opción C (índice non-clustered sobre fecha) ayuda
pero no al nivel de las particiones cuando hay 8 TB. La opción D (tabla externa) cambia la plataforma, lo cual la unidad descarta explícitamente como condición del enunciado.

**Fuentes**:

- [Unidad 1.1.1 oficial (ES)](https://learn.microsoft.com/es-mx/training/modules/design-implement-database-objects/1-introduction/)
- [Tablas e índices particionados](https://learn.microsoft.com/es-es/sql/relational-databases/partitions/partitioned-tables-and-indexes)

---

## Cómo usar estas preguntas

1. Leé la pregunta, tapá la respuesta y razoná en voz alta **por qué** cada opción incorrecta es incorrecta.
2. Si fallaste una, volvé a la sección correspondiente de `teoria/concepto.md`.
3. Las 5 preguntas cubren los 5 ejes temáticos del módulo (diseño, tipos especializados, restricciones,
   características avanzadas, particiones). Cuando llegues a la unidad específica (1.1.5, 1.1.6, etc.) vas a
   volver a ver el mismo concepto con más profundidad.