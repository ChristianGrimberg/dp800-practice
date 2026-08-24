---
tipo: Glosario
fecha_actualizacion: '2026-08-24'
fuente: 'ChristianGrimberg/DP-800 -> 001-Curso/Conceptos'
---

# Glosario del curso DP-800

Glosario con **42 conceptos** del curso oficial, espejado desde el repo privado `ChristianGrimberg/DP-800` y mantenido en sincronización.

Cada entrada tiene una definición breve extraída del material oficial.

---

## Índice alfabético

- [Almacén de consultas](#almacén-de-consultas)
- [Auditoría](#auditoría)
- [Azure SQL Database](#azure-sql-database)
- [Azure SQL Managed Instance](#azure-sql-managed-instance)
- [Bloqueos e interbloqueos](#bloqueos-e-interbloqueos)
- [Búsqueda de texto completo](#búsqueda-de-texto-completo)
- [Búsqueda de vectores](#búsqueda-de-vectores)
- [Búsqueda híbrida](#búsqueda-híbrida)
- [CICD](#cicd)
- [Cifrado de datos](#cifrado-de-datos)
- [CTE (Expresión de tabla común)](#cte-expresión-de-tabla-común)
- [Data API Builder](#data-api-builder)
- [Deriva de esquema](#deriva-de-esquema)
- [Desencadenadores](#desencadenadores)
- [DMV (Vistas de administración dinámica)](#dmv-vistas-de-administración-dinámica)
- [Enmascaramiento dinámico de datos (DDM)](#enmascaramiento-dinámico-de-datos-ddm)
- [Fabric Copilot](#fabric-copilot)
- [Funciones con valores de tabla](#funciones-con-valores-de-tabla)
- [Funciones de ventana](#funciones-de-ventana)
- [Funciones escalares](#funciones-escalares)
- [GitHub Copilot](#github-copilot)
- [IA Generativa](#ia-generativa)
- [Incrustaciones (Embeddings)](#incrustaciones-embeddings)
- [JSON en SQL](#json-en-sql)
- [MCP (Model Context Protocol)](#mcp-model-context-protocol)
- [Modelos externos](#modelos-externos)
- [Niveles de aislamiento](#niveles-de-aislamiento)
- [Particionamiento](#particionamiento)
- [Permisos a nivel de objeto](#permisos-a-nivel-de-objeto)
- [Planes de ejecución](#planes-de-ejecución)
- [Procedimientos almacenados](#procedimientos-almacenados)
- [Proyectos de SQL Database](#proyectos-de-sql-database)
- [RAG (Generación aumentada de recuperación)](#rag-generación-aumentada-de-recuperación)
- [Restricciones](#restricciones)
- [Seguridad a nivel de fila (RLS)](#seguridad-a-nivel-de-fila-rls)
- [SQL Database en Microsoft Fabric](#sql-database-en-microsoft-fabric)
- [SQL Server en Azure VMs](#sql-server-en-azure-vms)
- [T-SQL](#t-sql)
- [Tablas temporales](#tablas-temporales)
- [Vistas](#vistas)
- [Índice de Conceptos](#índice-de-conceptos)
- [Índices](#índices)

---

## Definiciones

### Almacén de consultas

> El modo de captura predeterminado, **Automático**, es la opción adecuada para la mayoría de las cargas de trabajo. Filtra las consultas poco frecuentes y las consultas con un consumo de recursos insignificante, lo que mantiene el uso de almacenamiento administrable. Empareje esta configuración con **la limpieza basada en tamaño establecida en Automático**, por lo que la base de datos quita autom...

---

### Auditoría

> SQL Server Audit requiere crear un objeto de auditoría de servidor que defina dónde escribir registros de auditoría y, a continuación, crear especificaciones de auditoría que definan qué capturar.

---

### Azure SQL Database

> ¿Qué pasaría si los lectores no tuvieran que esperar a los escritores? Esta cuestión es la que aborda el aislamiento de control de versiones de fila. En lugar de bloquear detrás de los bloqueos, el motor de la base de datos mantiene las versiones anteriores de las filas en un **almacén de versiones**. Cuando una transacción necesita leer los datos que modifica otra transacción, lee desde el alma...

---

### Azure SQL Managed Instance

> Las bases de datos SQL admiten varios métodos de autenticación. La autenticación de SQL usa un nombre de usuario y una contraseña almacenados en la base de datos. Es sencillo, pero arriesgado si las credenciales se ponen en peligro. La autenticación de Microsoft Entra amplía la integración de identidades a escenarios en la nube, trabajando con Azure SQL Database, Azure SQL Managed Instance, SQL ...

---

### Bloqueos e interbloqueos

> En Azure SQL Database, el enfoque es diferente. Puede crear una sesión de eventos extendidos personalizada que capture el evento `sqlserver.database_xml_deadlock_report` y lo consulte mediante las VMD `sys.dm_xe_database_sessions` y `sys.dm_xe_database_session_targets` con ámbito de base de datos. En el ejemplo siguiente se crea una sesión de captura de interbloqueos y se consulta su búfer circu...

---

### Búsqueda de texto completo

> La búsqueda de texto completo se destaca cuando los usuarios buscan con palabras y frases específicas. Usa índices de texto completo para habilitar búsquedas lingüísticas rápidas y proporciona predicados como `CONTAINS` y `FREETEXT` para consultar esos índices. Los diferentes patrones de consulta (término, frase, prefijo, inflexión y proximidad) abordan diferentes necesidades de búsqueda. Cuando...

---

### Búsqueda de vectores

> Preparar SQL para la búsqueda de vectores significa tomar tres decisiones: qué tipo de datos y dimensiones usar, qué métrica de distancia coincide con el modelo de inserción y si la búsqueda exacta o aproximada se ajusta al tamaño del conjunto de datos. La búsqueda exacta con `VECTOR_DISTANCE` funciona bien para conjuntos de datos más pequeños o consultas filtradas, mientras que la búsqueda apro...

---

### Búsqueda híbrida

> La búsqueda híbrida combina la búsqueda de texto completo y vectorial para controlar consultas centradas en palabras clave y centradas en conceptos. La fusión de clasificación recíproca combina los resultados clasificados sin necesidad de normalización de puntuación, tratando ambas fuentes de forma justa. Puede ajustar el tamaño del conjunto de resultados, la constante RRF y los pesos de origen ...

---

### CICD

> El proyecto de base de datos SQL indica que la `Customers` tabla tiene 12 columnas. La producción tiene 13. Alguien agregó una `LoyaltyTier` columna directamente a través de SQL Server Management Studio (SSMS) el jueves pasado durante un incidente. La siguiente implementación quitará silenciosamente esa columna porque el proyecto no sabe que existe. Este tipo de situación se conoce como desfase ...

---

### Cifrado de datos

> ![Diagrama que compara tres capas de cifrado: TDE en el nivel de archivo de base de datos, cifrado de nivel de columna en columnas específicas y Always Encrypted con claves de cifrado que se mantienen fuera de la base de datos en el nivel de aplicación cliente.](https://raw.githubusercontent.com/MicrosoftDocs/learn/25affc3c56f9c1deba8f7793c83f7aa376751620/learn-pr/wwl-data-ai/implement-data-secu...

---

### CTE (Expresión de tabla común)

> Una expresión de tabla común se define mediante la `WITH` cláusula , seguida del nombre de CTE, una lista de columnas opcional y una consulta que define el conjunto de resultados. A continuación, se puede hacer referencia a la CTE en la instrucción `SELECT`, `INSERT`, `UPDATE` o `DELETE` posterior.

---

### Data API Builder

> [Data API Builder (DAB)](https://learn.microsoft.com/es-es/azure/data-api-builder/overview?azure-portal=true) es un motor multiplataforma de código abierto que crea puntos de conexión REST y GraphQL modernos para la base de datos sin necesidad de escribir código personalizado. Con un único archivo de configuración, puede exponer los objetos de base de datos a través de API seguras y escalables q...

---

### Deriva de esquema

> Concepto transversal que aparece en 3 unidades del curso. Ver las unidades listadas abajo para entender su aplicación práctica.

---

### Desencadenadores

> LOS desencadenadores **INSTEAD OF** reemplazan la instrucción de modificación de datos original. El código de desencadenador se ejecuta en lugar de la operación `INSERT`, `UPDATE` o `DELETE`. Utilice desencadenadores INSTEAD OF para modificar vistas que normalmente no aceptarían modificaciones directas o para implementar lógica de negocios compleja:

---

### DMV (Vistas de administración dinámica)

> SELECT
    d.value('(/event/@timestamp)[1]', 'datetime2') AS deadlock_time,
    d.query('/event/data[@name=''xml_report'']/value/deadlock') AS deadlock_xml
FROM (
    SELECT CAST(target_data AS XML) AS rb
    FROM sys.dm_xe_database_sessions AS s
    INNER JOIN sys.dm_xe_database_session_targets AS t
        ON CAST(t.event_session_address AS BINARY(8)) = CAST(s.address AS BINARY(8))
    WHERE s...

---

### Enmascaramiento dinámico de datos (DDM)

> [El enmascaramiento dinámico de datos](https://learn.microsoft.com/es-es/sql/relational-databases/security/dynamic-data-masking?Azure-portal=true) proporciona una manera de limitar la exposición de datos confidenciales sin cambiar el código de la aplicación ni los datos subyacentes. Cuando los usuarios consultan columnas enmascaradas, SQL Server devuelve valores ofuscados en función de las regla...

---

### Fabric Copilot

> Al usar herramientas asistidas por IA para el desarrollo de bases de datos, está trabajando con sistemas que aplican [principios de inteligencia artificial responsables](https://learn.microsoft.com/es-es/azure/machine-learning/concept-responsible-ai?azure-portal=true). Tanto GitHub Copilot como Fabric Copilot están diseñados con medidas de seguridad para ayudar a garantizar que el código generad...

---

### Funciones con valores de tabla

> Las vistas solo pueden modificar datos cuando los cambios afectan a una sola tabla base. Las funciones insertadas con valores de tabla se benefician del almacenamiento en caché del plan porque el optimizador las expande directamente al plan de consulta. Las TVF de varias instrucciones y las funciones escalares se tratan como "cajas negras": el optimizador no puede ver dentro de ellas, lo que a m...

---

### Funciones de ventana

> Las funciones analíticas permiten acceder a los datos de otras filas sin usar autocombinaciones ni subconsultas. Estas funciones son útiles para el análisis de series temporales, la detección de tendencias y la comparación de valores actuales con valores históricos o futuros. A diferencia de las funciones de ventana de agregado que calculan resúmenes, las funciones analíticas recuperan valores e...

---

### Funciones escalares

> Una función escalar acepta cero o más parámetros y devuelve un único valor de un tipo de datos especificado. A diferencia de los procedimientos almacenados, las funciones escalares se pueden incrustar directamente en expresiones SQL siempre que se use una columna o variable.

---

### GitHub Copilot

> Al usar herramientas asistidas por IA para el desarrollo de bases de datos, está trabajando con sistemas que aplican [principios de inteligencia artificial responsables](https://learn.microsoft.com/es-es/azure/machine-learning/concept-responsible-ai?azure-portal=true). Tanto GitHub Copilot como Fabric Copilot están diseñados con medidas de seguridad para ayudar a garantizar que el código generad...

---

### IA Generativa

> En este ejercicio, implementará una solución completa de generación aumentada de recuperación (RAG) mediante Azure SQL Database. Puede recuperar los datos pertinentes de la base de datos, formatearlos como contexto JSON, construir un mensaje aumentado, llamar a un punto de conexión del modelo de lenguaje grande (LLM) y extraer la respuesta.

---

### Incrustaciones (Embeddings)

> La generación de incrustaciones con `AI_GENERATE_EMBEDDINGS` es solo el primer paso. A medida que cambian los datos de origen, los vectores almacenados pueden salir de la sincronización, por lo que necesita una estrategia de mantenimiento. Las opciones van desde desencadenadores y Change Tracking para actualizaciones estrechamente acopladas a captura de datos modificados, streaming de eventos mo...

---

### JSON en SQL

> En este ejemplo se crea una tabla con una `JSON` columna que almacena las opciones de configuración del usuario. Las `INSERT` instrucciones agregan documentos JSON como literales de cadena. Para leer valores específicos, `JSON_VALUE` extrae valores escalares como el tema y el lenguaje, mientras `JSON_QUERY` que devuelve todo el objeto JSON. El `.modify()` método (actualmente en versión prelimina...

---

### MCP (Model Context Protocol)

> Las soluciones de base de datos modernas exponen datos a través de varios puntos de conexión de API, lo que permite a las aplicaciones acceder a la información sin escribir consultas SQL tradicionales. Los puntos de conexión de GraphQL, REST y Model Context Protocol (MCP) presentan consideraciones de seguridad únicas. La protección correcta de estos puntos de conexión protege los datos al tiempo...

---

### Modelos externos

> El `@credential` parámetro hace referencia a una credencial con ámbito de base de datos que contiene los detalles de autenticación. Estas credenciales se configuran al crear un modelo externo mediante una identidad administrada o una clave de API. La misma credencial funciona tanto para las llamadas de modelo externo como para las llamadas directas al punto de conexión REST con `sp_invoke_extern...

---

### Niveles de aislamiento

> **Read Committed Snapshot Isolation** cambia el comportamiento de READ COMMITTED en el nivel de base de datos. Con el Aislamiento de instantánea de lectura confirmada (RCSI) habilitado, cada operación de lectura ve una instantánea de los datos tal como existían al principio de esa *instrucción*. Los escritores siguen bloqueando las filas que modifican, pero los lectores nunca bloquean detrás de ...

---

### Particionamiento

> En este ejemplo se crean particiones trimestrales para una tabla *Orders* . La función de partición define cuatro valores de límite (enero, abril, julio, octubre) que crean cinco particiones: una para los datos anteriores a 2024 y cuatro para cada trimestre de 2024. El esquema de partición asigna todas las particiones al grupo de archivos PRIMARY. La tabla *Orders* usa la columna *OrderDate* com...

---

### Permisos a nivel de objeto

> Tres instrucciones controlan permisos: [`GRANT`](https://learn.microsoft.com/es-es/sql/t-sql/statements/grant-transact-sql?Azure-portal=true) concede permisos específicos a los usuarios, [`REVOKE`](https://learn.microsoft.com/es-es/sql/t-sql/statements/revoke-transact-sql?Azure-portal=true) quita los permisos concedidos previamente y [`DENY`](https://learn.microsoft.com/es-es/sql/t-sql/statement...

---

### Planes de ejecución

> - **Plan de ejecución estimado**: generado sin ejecutar la consulta. Muestra los operadores planificados y los recuentos de filas estimados en función de las estadísticas. Use planes estimados para el análisis rápido sin afectar a la base de datos.
- **Plan de ejecución real**: capturado durante la ejecución de la consulta. Incluye el plan estimado más recuentos de filas reales, tiempos de ejecu...

---

### Procedimientos almacenados

> La creación de un procedimiento almacenado comienza con la instrucción [`CREATE PROCEDURE`](https://learn.microsoft.com/es-es/sql/t-sql/statements/create-procedure-transact-sql?azure-portal=true) seguida de tu lógica T-SQL. Especifique el nombre del procedimiento mediante un identificador calificado por esquemas, lo que mejora la claridad y el rendimiento.

---

### Proyectos de SQL Database

> El peligro no es el desfase en sí. Es lo que sucede a continuación. La canalización implementa `.dacpac`, SqlPackage calcula la diferencia y todos los objetos sobre los que el proyecto no tiene conocimiento se quitan. La detección del desfase antes de que se ejecute la implementación es fundamental.

---

### RAG (Generación aumentada de recuperación)

> La creación de aplicaciones inteligentes con Azure SQL Database implica más que almacenar y consultar datos relacionales. Los desarrolladores deben integrar modelos de INTELIGENCIA ARTIFICIAL, generar incrustaciones a partir de texto y realizar búsquedas vectoriales para habilitar características como la búsqueda semántica y la generación aumentada de recuperación (RAG). Azure SQL Database y Fab...

---

### Restricciones

> Ha implementado tipos de tabla especializados, incluidas tablas temporales para el seguimiento automático de cambios, tablas del libro contabilidad para escenarios de cumplimiento a prueba de alteraciones, tablas de grafos para el modelado de relaciones y tablas optimizadas para memoria para cargas de trabajo OLTP de alto rendimiento. Ha aprendido a aplicar la integridad de los datos a través de...

---

### Seguridad a nivel de fila (RLS)

> [Row-Level Security (RLS)](https://learn.microsoft.com/es-es/sql/relational-databases/security/row-level-security?Azure-portal=true) permite controlar el acceso a las filas de una tabla de base de datos en función de las características del usuario que ejecuta una consulta. A diferencia de los permisos de nivel de tabla que conceden o deniegan el acceso a tablas completas, RLS filtra las filas d...

---

### SQL Database en Microsoft Fabric

> Concepto transversal que aparece en 3 unidades del curso. Ver las unidades listadas abajo para entender su aplicación práctica.

---

### SQL Server en Azure VMs

> [SQL Server en Azure Virtual Machines](https://learn.microsoft.com/es-es/azure/azure-sql/virtual-machines/windows/sql-server-on-azure-vm-iaas-what-is-overview?azure-portal=true) proporciona implementación de infraestructura como servicio (IaaS) donde se controla la instancia de SQL Server, la configuración del motor de base de datos y el sistema operativo Windows o Linux subyacentes. Esta opción...

---

### T-SQL

> Después de crear tablas particionadas, debe administrarlas a lo largo del tiempo. Entre las operaciones comunes se incluyen la consulta de metadatos de partición, la adición de nuevas particiones a medida que crecen los datos y la eliminación de particiones antiguas durante el archivado. Estas operaciones usan la función [`$PARTITION`](https://learn.microsoft.com/es-es/sql/t-sql/functions/partit...

---

### Tablas temporales

> Puede crear una tabla temporal mediante la `SYSTEM_VERSIONING = ON` opción . Las tablas temporales requieren dos columnas adicionales `DATETIME2` para realizar un seguimiento del período de validez de cada versión de fila y una `PERIOD FOR SYSTEM_TIME` cláusula para definir qué columnas realizan un seguimiento de estas marcas de tiempo. Este es un ejemplo:

---

### Vistas

> [*Un índice no clúster*](https://learn.microsoft.com/es-es/sql/relational-databases/indexes/clustered-and-nonclustered-indexes-described?azure-portal=true#nonclustered) tiene una estructura independiente de las filas de datos. Un índice no clúster contiene los valores de clave de índice no clúster y cada entrada de valor de clave tiene un puntero a la fila de datos que contiene el valor clave. S...

---

### Índice de Conceptos

> Notas de concepto que aparecen en múltiples unidades del curso. Sirven como punto de entrada para entender temas recurrentes y se vinculan a todas las unidades donde se mencionan.

---

### Índices

> Un índice de almacén de columnas no agrupado (NCCI) crea una copia de columnas independiente de las columnas seleccionadas junto con la tabla de almacén de filas existente, lo que permite que la misma tabla sirva de forma eficaz las cargas de trabajo transaccionales y analíticas. La tabla conserva su índice de almacén de filas agrupado original para búsquedas y actualizaciones rápidas de una sol...

---

