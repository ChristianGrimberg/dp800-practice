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

### Reglas obligatorias al abrir un PR

Estas reglas son ley. Ningún PR puede saltarse alguna.

| Regla | Cómo |
|---|---|
| **Base siempre `main`** | `gh pr create --base main` |
| **Rama fresca basada en `origin/main`** | `git fetch origin main && git checkout -b feature/<...> origin/main` |
| **PR siempre en Draft** | `gh pr create --draft`. El humano lo pasa a listo cuando lo apruebe. |
| **Asignado al owner** | `gh pr create --assignee ChristianGrimberg` |
| **Labels coherentes** | Labels `módulo:*` y `categoria:*` derivados del issue asociado, más un label de tipología (`enhancement`, `bug`, `documentation`, `chore`). |
| **Cierra su issue** | Si el PR trata contenido de un issue, incluir `Closes #N` en el campo del template. Para fix/docs/infra/bot, completar con `N/A`. |
| **Verificación post-creación** | El agente que abre el PR debe verificar con `gh pr view <n> --json isDraft,assignees,labels,body` que todo está como espera. Si el body contiene `\n` literales, regenerarlo antes de pasarlo a listo. |

El skill `abrir-pr-desde-capitulo` aplica todas estas reglas en orden.

## Convención de issues

- Usar `.github/ISSUE_TEMPLATE/nueva-practica.yml` para unidades nuevas.
- El bot crea automáticamente issues con título `📚 Practicar Unidad X.Y.Z — <título>`.

### Verificación post-creación

El agente que crea o enriquece un issue es **responsable** de su legibilidad:

1. Después de crear el issue, leerlo de vuelta: `gh issue view <n> --json body`.
2. Verificar que el cuerpo renderiza bien en Markdown (headers, listas, saltos de línea reales).
3. **Nunca** dejar un issue con `\n` literales en el cuerpo (caso bug #8).
4. Si la verificación falla, regenerar el contenido con `gh issue edit <n> --body-file ...` y volver a verificar.

Los workflows automatizados (ej. `siguiente-tema.yml`) emiten los cuerpos multi-línea con sintaxis heredoc para preservar los saltos de línea reales; si se observa un issue automático con cuerpo roto, es bug en el script `scripts/siguiente-tema.py`.

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
