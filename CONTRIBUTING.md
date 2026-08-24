# Convenciones de contribución

## Idioma

- **Toda la documentación legible** (README, comentarios, commits, issues, PRs, teoria/) está en **español**.
- Nombres de archivos de configuración técnica (`.yml`, `.json`, `.sql`, `.sh`, `.py`) en inglés por convención.
- Mensajes de commit: gitmoji + verbo en imperativo en español + alcance corto.

## Estructura del repositorio

```
dp800-practice/
├── curso/                          # espejo del curso DP-800T00-A
│   ├── _meta/                      # course-hierarchy.json (espejo del repo privado)
│   ├── _plantillas/unidad/         # plantilla para crear nuevas unidades
│   ├── path-1-.../                 # 4 módulos
│   ├── path-2-.../                 # 4 módulos
│   └── path-3-.../                 # 3 módulos
├── recursos/                       # glosario, bibliografía, comandos
├── docs/                           # entrada de MkDocs + mapa generado
├── scripts/                        # utilidades
├── .devcontainer/                  # entorno reproducible
├── .github/                        # workflows de CI
├── .opencode/                      # agentes y skills
├── .obsidian/                      # config del vault
└── AGENTS.md                       # routing estándar
```

## Front-matter obligatorio por unidad

Cada `README.md` de unidad debe tener **todos** los campos siguientes (el workflow `validar-estructura.yml` falla el PR si falta alguno):

```yaml
---
tipo: Unidad
curso: 'Curso DP-800T00-A: ...'
codigo_curso: DP-800T00
path: 'Path X — ...'
modulo: 'Módulo X.Y — ...'
unidad: 'Unidad X.Y.Z — ...'
codigo: X.Y.Z
slug: <carpeta>
categoria: introduccion | leccion | lab | quiz | resumen
url: <URL oficial en Microsoft Learn>
uid: learn.wwl.<modulo>.<unidad>
duracion_min: <numero>
fecha_actualizacion: 'YYYY-MM-DD'
estado: por-hacer | en-curso | hecho
fecha_inicio: null | 'YYYY-MM-DD'
fecha_fin: null | 'YYYY-MM-DD'
ultimo_repaso: null | 'YYYY-MM-DD'
proximo_repaso: null | 'YYYY-MM-DD'
pr: null | <numero>
conceptos: [t1, t2, ...]
nivel: basico | intermedio | avanzado
prerequisitos: [<slug-de-unidades-previas>]
esfuerzo: corto | medio | largo
---
```

## Presencia de `practica/` según categoría

| Categoría | `practica/` | `teoria/` |
|---|---|---|
| `introduccion` | ❌ | ✅ |
| `leccion` | ✅ | ✅ |
| `lab` | ✅ (es el ejercicio) | ✅ |
| `quiz` | ❌ | ✅ (con respuestas) |
| `resumen` | ❌ | ✅ (cheatsheet) |

## Convención de commits

Prefijo gitmoji + verbo en imperativo español + alcance corto.

```bash
✨ agregar práctica de índices columnstore (1.1.4)
📝 documentar concepto de CTEs recursivas
🐛 corregir orden de variables en docker-compose
🔧 configurar protección de rama main
📦 agregar skill generar-dataset-sintetico
🗃️ agregar script de creación de base dp800_lab
♻️ refactorizar script generar-mapa para soportar módulos grandes
🧪 agregar tests para validar-estructura
🚧 trabajo en progreso sobre 1.1.5 (no mergeable aún)
📚 publicar sitio en GitHub Pages
```

Gitmoji permitidos: `✨ 📝 🐛 🔧 📦 🗃️ 🚀 ♻️ 🎨 ✅ 🔒 📚 ⚡ 🧪 🔥 🚧 🐳 🤖 👷 🔍`.

El bot de GitHub Actions puede usar prefijos que no respeten esta convención (ej. `🤖 regenerar mapa`); están permitidos para commits automatizados.

## Convención de branches

```
feature/<codigo-unidad>-<slug-kebab>
```

Ejemplos:

```
feature/1.1.3-creacion-tablas
feature/1.1.9-lab-creacion-mantenimiento
feature/3.2.5-busqueda-vectorial
```

Para cambios transversales (no asociados a una unidad):

```
feature/<tipo>-<slug>
```

Ejemplos:

```
feature/docs-agregar-seccion-preguntas-frecuentes
fix/ci-sql-lint-falla-con-unicode
chore/actualizar-dependencias-mkdocs
```

## Convención de PRs

- **Un PR por unidad** (o grupo de unidades de teoría pura).
- Usar la plantilla `.github/PULL_REQUEST_TEMPLATE.md`.
- Cada commit del PR debe tener prefijo gitmoji + español.
- El PR debe pasar CI verde (lint SQL + validar estructura + build docs).
- Merge con **squash** para mantener `main` limpio.

## Convención de issues

- Usar `.github/ISSUE_TEMPLATE/nueva-practica.yml` para unidades nuevas.
- El bot crea automáticamente issues con título `📚 Practicar Unidad X.Y.Z — <título>`.

## Ramas protegidas

`main` está protegida con:

- ✅ PR obligatorio.
- ✅ CI verde (lint SQL + validar estructura + publicar docs).
- ❌ Aprobación manual (auto-merge con checks).
- ❌ Force-push.
- ❌ Borrado de la rama.

## Datos sensibles

- **Nunca** commitear `.env`, claves, contraseñas.
- Las contraseñas de SQL Server en dev container se generan por `.env` (ignorado).
- Si encontrás un secreto en el repo, rotar inmediatamente y purgar con `git filter-repo`.

## Agentes y skills

Ver `AGENTS.md` para el routing estándar. Resumen rápido:

- **Planificar** una unidad nueva → agente `arquitecto-dp800` + skill `planificar-capitulo`.
- **Redactar teoría** → agente `documentador` + skill `explicar-concepto`.
- **Generar práctica** → agente `generador-practicas` + skills `generar-dataset-sintetico` + `practicar-concepto-sql`.
- **Antes de commitear SQL** → agente `revisor-codigo-sql` + skill `lint-sql`.
- **Buscar tema por concepto** → skill `buscar-capitulo-por-concepto`.
- **Enriquecer issue sugerido por el bot** → skill `preparar-siguiente-tema`.
