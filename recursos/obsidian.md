# Guía de uso de Obsidian en este repositorio

Este repositorio funciona como **vault de Obsidian** sin necesidad de clonar aparte. La misma carpeta que navegás en GitHub se abre en Obsidian y se sincroniza vía git.

## Abrir el vault

1. En Obsidian: **Open folder as vault** → seleccionar la carpeta clonada del repo.
2. La primera vez, Obsidian detecta `.obsidian/` y carga la configuración compartida.

## Navegación recomendada

- **Grafo** (`Ctrl/Cmd + G`): visualiza las relaciones entre unidades por backlink. Útil para detectar temas conexos.
- **Backlinks** (panel derecho de cualquier nota): muestra qué unidades referencian a la actual.
- **Outline** (panel derecho): usa los `##` y `###` para navegar dentro de una unidad larga.
- **Tag Pane** (panel izquierdo): filtra por `módulo/path-X`, `leccion`, `hecho`, etc.

## Consultas Dataview útiles

Abrir cualquier nota y pegar estas consultas como bloques `dataview`:

### Listar unidades pendientes

```dataview
TABLE
  modulo as "Módulo",
  categoria as "Tipo",
  duracion_min as "Min"
FROM "curso"
WHERE tipo = "Unidad" AND estado = "por-hacer"
SORT codigo ASC
```

### Unidades para repasar hoy

```dataview
LIST
FROM "curso"
WHERE tipo = "Unidad" AND proximo_repaso <= date(today) AND estado = "hecho"
SORT proximo_repaso ASC
```

### Avance por módulo

```dataview
TABLE
  length(filter(rows, (r) => r.estado = "hecho")) as "Hechas",
  length(rows) as "Total",
  round(length(filter(rows, (r) => r.estado = "hecho")) * 100.0 / length(rows)) + "%" as "Progreso"
FROM "curso"
WHERE tipo = "Unidad"
GROUP BY modulo
```

### Conceptos más usados

```dataview
LIST conceptos
FROM "curso"
WHERE tipo = "Unidad"
FLATTEN conceptos
GROUP BY conceptos
SORT length(rows) DESC
LIMIT 20
```

## Plugins de comunidad recomendados

Instalar desde **Settings → Community plugins → Browse**:

| Plugin | Uso en este repo |
|---|---|
| **Dataview** | Consultas sobre front-matter (arriba) |
| **Templater** | Automatizar creación de unidades nuevas |
| **Calendar** | Vista de calendario para planificar práctica diaria |
| **Mind Map** | Mapas mentales a partir de headings |
| **Excalidraw** | Diagramas de arquitectura SQL |
| **Charts** | Gráficos a partir de tablas Dataview |

## Templates disponibles

- `.obsidian/templates/unidad.md` → replica el front-matter completo para una unidad nueva.
- `.obsidian/templates/nota-rapida.md` → nota personal sin front-matter estricto.

En Templater: configurar la carpeta de templates como `.obsidian/templates/`.

## Wikilinks vs links relativos

- **Dentro del mismo módulo**: preferir wikilinks `[[1.1.3-creacion-tablas-eficaces]]`. Obsidian los autocompleta.
- **Entre módulos o hacia `recursos/`**: usar links relativos `.md` para que funcionen también en GitHub.
- **A Microsoft Learn**: siempre link directo a la URL.

## Sincronización git ↔ Obsidian

Trabajo recomendado:

1. En Obsidian, editar las notas.
2. Git pull/push desde terminal o desde el plugin **Obsidian Git** (instalar desde community plugins).
3. El dev container mantiene `.obsidian/workspace.json` fuera del repo, así que cada máquina puede tener su layout propio.

## Limitaciones

- Dataview **no se renderiza en GitHub ni en el sitio MkDocs**. Para verlo hay que abrir Obsidian localmente.
- El grafo grande (108 unidades) puede ser lento; usar el filtro de búsqueda para enfocarlo.
- `workspace.json` está en `.gitignore` por diseño: cada máquina tiene su estado de paneles.
