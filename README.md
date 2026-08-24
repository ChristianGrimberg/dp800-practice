# dp800-practice

[![Curso](https://img.shields.io/badge/curso-DP--800T00--A-blue)](https://learn.microsoft.com/es-mx/training/courses/dp-800t00)
[![Certificación](https://img.shields.io/badge/certificación-SQL%20AI%20Developer%20Associate-indigo)](https://learn.microsoft.com/es-es/credentials/certifications/developing-ai-enabled-database-solutions/)
[![Estado](https://img.shields.io/badge/estado-en%20construcción-yellow)](./docs/mapa-de-aprendizaje.md)
[![Licencia](https://img.shields.io/badge/licencia-MIT-green)](./LICENSE)
[![Sitio](https://img.shields.io/badge/sitio-GitHub%20Pages-blue)](https://christiangrimberg.github.io/dp800-practice/)

Repositorio público de práctica para la certificación **Microsoft Certified: SQL AI Developer Associate (DP-800)**, alineado al curso oficial **DP-800T00-A: Desarrollo de soluciones de base de datos habilitadas para IA** de Microsoft Learn.

## ¿Qué es este repo?

Un espacio donde documento mi avance diario a través del temario oficial del curso DP-800, aprendiendo cada concepto **haciendo**: teoría explicada con casos de uso reales + código SQL ejecutable en un contenedor de desarrollo con Azure SQL Edge y Ollama para prácticas de IA.

> Fuente privada de apuntes: [`ChristianGrimberg/DP-800`](https://github.com/ChristianGrimberg/DP-800) (bóveda de Obsidian).
> Espejo oficial: [Microsoft Learn — DP-800T00](https://learn.microsoft.com/es-mx/training/courses/dp-800t00).

## Características

- 📚 **Estructura espejo del curso oficial** — 3 Paths, 11 Módulos, 108 Unidades.
- 🐳 **Dev container** con Azure SQL Edge + Ollama + VS Code, listo para ejecutar SQL contra una base real.
- 🤖 **5 agentes y 9 skills de opencode** que acompañan el flujo `planificar → practicar → revisar → documentar → PR`.
- 📖 **MkDocs Material + Obsidian** — el mismo repositorio funciona como vault de Obsidian y como sitio navegable publicado en GitHub Pages.
- 🗺️ **Mapa de aprendizaje auto-generado** que indica qué repasar hoy según el sistema de repaso espaciado.
- 🔄 **Bot de "siguiente tema"** — cada merge a `main` abre automáticamente el issue de la próxima unidad.
- 🔒 **`main` protegido** con checks obligatorios (lint SQL + validación de estructura + sincronización de docs).

## Quickstart

```bash
# 1. Clonar
git clone https://github.com/ChristianGrimberg/dp800-practice.git
cd dp800-practice

# 2. Abrir en VS Code con Dev Containers
code .
# Cuando VS Code lo sugiera, "Reabrir en contenedor"

# 3. Una vez dentro del contenedor, validar la conexión
bash scripts/conectar-sql.sh "SELECT @@VERSION"

# 4. Listo para practicar
```

## Estructura del repositorio

```
dp800-practice/
├── curso/                          # espejo del curso DP-800T00-A
│   ├── path-1-diseno-desarrollo/   # Path 1: 4 módulos
│   ├── path-2-seguridad-optimizacion-despliegue/  # Path 2: 4 módulos
│   └── path-3-ia-en-sql/           # Path 3: 3 módulos
├── recursos/                       # glosario, bibliografía, comandos útiles
├── docs/                           # entrada de MkDocs + mapa generado
├── scripts/                        # utilidades (conectar SQL, lint, mapa)
├── .devcontainer/                  # entorno reproducible
├── .github/                        # workflows de CI
├── .opencode/                      # agentes y skills opencode
├── .obsidian/                      # config del vault para Obsidian
└── AGENTS.md                       # routing estándar de agentes/skills
```

## ¿Cómo avanzo?

1. **Abrís un issue** "Practicar Unidad X.Y.Z" (auto-creado por el bot tras cada merge).
2. **Creás una rama**: `feature/<codigo>-<slug>`.
3. **Usás los agentes opencode** para redactar teoría (`/documentador`) y armar la práctica (`/generador-practicas`).
4. **Commiteás** con prefijo gitmoji + verbo en español.
5. **Abrís un PR** contra `main`. CI corre lint + valida estructura.
6. **Merge a `main`** → el bot crea el issue del siguiente tema.

## Documentación navegable

Sitio publicado automáticamente en: <https://christiangrimberg.github.io/dp800-practice/>

Mapa de aprendizaje con estado de avance y repasos: <https://christiangrimberg.github.io/dp800-practice/mapa-de-aprendizaje/>

## Convenciones

- **Commits**: gitmoji + verbo imperativo en español + alcance corto.
  ```
  ✨ agregar práctica de índices columnstore (1.1.4)
  📝 documentar concepto de CTEs recursivas
  ```
- **Branches**: `feature/<codigo-unidad>-<slug-kebab>`.
- **PRs**: uno por unidad (o grupo de unidades de teoría pura).
- **Documentación**: todo en español, salvo configuración técnica.

Ver [`CONTRIBUTING.md`](./CONTRIBUTING.md) para detalles completos.

## Licencia

MIT — ver [`LICENSE`](./LICENSE).
