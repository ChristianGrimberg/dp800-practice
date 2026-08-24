# AGENTS.md — Routing de agentes y skills

> **Este archivo es el mapa oficial para que cualquier agente IA (opencode, Continue, GitHub Copilot, MCP server, etc.) entienda qué agentes y skills existen en este repositorio, cuándo usarlos y cómo invocarlos.**
>
> Si estás leyendo esto desde opencode o similar, **empezá por acá**. Después leé `.opencode/README.md` para detalles.

## Idioma y convenciones

- **Toda la documentación legible está en español.**
- Nombres de skills/agents usan `kebab-case` en español (ej: `tutor-sql`, `practicar-concepto-sql`).
- Nombres de archivos de configuración técnica (`.yml`, `.json`, `.sql`) en inglés por convención de tooling.
- Mensajes de commit: gitmoji + verbo imperativo español + alcance corto. Ver `CONTRIBUTING.md`.

## Agentes disponibles (5)

| Agente | Cuándo invocarlo | Output esperado |
|---|---|---|
| `arquitecto-dp800` | "Planificar módulo/unidad nuevo", "¿qué sigue?", "descomponeme X en checklist" | Plan + índice + front-matter |
| `tutor-sql` | "Acompañame en el ejercicio", "estoy trabado en X", "revisame este query" | Guía paso a paso sin dar la respuesta |
| `generador-practicas` | "Armame la práctica de X", "generame dataset" | `practica/*.sql` con dataset sintético |
| `revisor-codigo-sql` | "Revisame este SQL antes de commitear", "¿hay安全问题?" | Reporte de sqlfluff + checklist seguridad |
| `documentador` | "Redactá teoría de X", "explicame con analogías" | `teoria/*.md` con analogía + fuentes oficiales |

System prompts completos en `.opencode/agents/<nombre>.md`.

## Skills disponibles (9)

| Skill | Disparador | Entregable |
|---|---|---|
| `planificar-capitulo` | "Planificá la unidad X.Y.Z" | Plan en Markdown con checklist |
| `generar-dataset-sintetico` | "Generame el dataset para X" | `practica/01-preparacion.sql` |
| `practicar-concepto-sql` | "Armame los ejercicios de X" | `practica/02-ejercicio.sql` + `03-solucion.sql` |
| `explicar-concepto` | "Redactá la teoría de X" | `teoria/concepto.md` + `sintaxis.md` + `preguntas-examen.md` |
| `lint-sql` | "Pasame lint" | Reporte en Markdown |
| `abrir-pr-desde-capitulo` | "Abrí el PR de X" | Rama + PR con plantilla + lint |
| `buscar-capitulo-por-concepto` | "Busca unidades sobre X" | Lista con links y snippets |
| `preparar-siguiente-tema` | "Enriqueceme el issue #N" | Comentario enriquecido en el issue |
| `sincronizar-con-curso-oficial` | "Sincronizá con el curso oficial" | Reporte de drift |

Specs completas en `.opencode/skills/<nombre>/SKILL.md`.

## Routing estándar

Cualquier agente o IA que opere en este proyecto debe seguir este orden:

1. **Leer `AGENTS.md`** (este archivo) al inicio.
2. **Leer `.opencode/README.md`** para detalles de uso.
3. **Si la tarea toca código SQL** → invocar primero `revisor-codigo-sql` + `lint-sql` antes de sugerir commit.
4. **Si la tarea toca teoría** → invocar `documentador` + `explicar-concepto` respetando `curso/_plantillas/unidad/teoria/`.
5. **Si la tarea toca estructura** → invocar `arquitecto-dp800` antes de crear archivos sueltos.
6. **Al cerrar un PR mergeado** → no hacer nada (lo maneja el workflow `.github/workflows/siguiente-tema.yml`).
7. **Antes de abrir un PR** → usar el skill `abrir-pr-desde-capitulo`.

## Combinaciones frecuentes

| Quiero... | Combinación |
|---|---|
| Empezar una unidad nueva | `arquitecto-dp800` + `planificar-capitulo` |
| Practicar y luego documentar | `generador-practicas` + `practicar-concepto-sql` → `documentador` + `explicar-concepto` |
| Cerrar una unidad | `revisor-codigo-sql` + `lint-sql` → `abrir-pr-desde-capitulo` |
| Repasar antes del examen | `buscar-capitulo-por-concepto` |
| Enriquecer issue del bot | `preparar-siguiente-tema` |
| Detectar drift del curso oficial | `sincronizar-con-curso-oficial` |

## Convenciones estrictas

- **Commits**: gitmoji + verbo imperativo español + alcance corto. Ver `CONTRIBUTING.md`.
- **Branches**: `feature/<codigo-unidad>-<slug-kebab>` o `feature/<tipo>-<slug>`.
- **PRs**: usar `PULL_REQUEST_TEMPLATE.md`, un PR por unidad (o grupo de unidades de teoría pura).
- **Front-matter**: todos los campos obligatorios, sin省略.
- **main**: protegida, solo merge vía PR con CI verde.

## Fuentes de verdad

- **Estructura del curso**: `curso/_meta/course-hierarchy.json` (espejo del repo privado `ChristianGrimberg/DP-800`).
- **Curso oficial**: cada unidad tiene su `url` en el front-matter apuntando a Microsoft Learn en español.
- **Glosario**: `recursos/glosario.md` (espejo de `001-Curso/Conceptos/` del repo privado).
- **Bibliografía**: `recursos/bibliografia.md`.

## Restricciones globales

- **NO** crear archivos fuera de `curso/<path>/<modulo>/unidades/<codigo>/`.
- **NO** commitear archivos generados manualmente (`.bak`, `.env`, dumps grandes).
- **NO** saltarse el front-matter obligatorio (CI falla).
- **NO** mergear a `main` sin CI verde (regla impuesta por branch protection).
- **NO** commitear secretos. Si se filtra uno, rotar y purgar con `git filter-repo`.

## Cómo abrir el vault en Obsidian

```bash
# Abrir Obsidian → "Open folder as vault" → seleccionar la carpeta del repo.
# La config compartida vive en .obsidian/ (commiteada).
# El workspace.json personal está en .gitignore.
```

Ver `recursos/obsidian.md` para recetas Dataview y configuración de plugins.

## Cómo servir la documentación localmente

```bash
mkdocs serve         # http://localhost:8000
mkdocs build --strict
```

El sitio se publica automáticamente en GitHub Pages con cada merge a `main`.

## Cómo abrir el dev container

```bash
code .  # VS Code detectará .devcontainer/ y preguntará si reabrir.
```

Una vez dentro, los servicios `sql`, `ollama` y `dev` están levantados y el script `post-create.sh` ya corrió.
