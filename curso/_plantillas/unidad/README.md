---
tipo: Unidad
curso: 'Curso DP-800T00-A: Desarrollo de soluciones de base de datos habilitadas para IA'
codigo_curso: DP-800T00
path: 'Path X — <título del path>'
modulo: 'Módulo X.Y — <título del módulo>'
unidad: 'Unidad X.Y.Z — <título de la unidad>'
codigo: X.Y.Z
slug: unidad-plantilla
categoria: leccion
url: <URL oficial en Microsoft Learn>
uid: learn.wwl.<modulo>.<unidad>
duracion_min: 0
fecha_actualizacion: '2026-08-24'
estado: por-hacer
fecha_inicio: null
fecha_fin: null
ultimo_repaso: null
proximo_repaso: null
pr: null
conceptos: []
nivel: basico
prerequisitos: []
esfuerzo: corto
---

# Unidad X.Y.Z — <Título>

**Fuente oficial**: [Unidad en Microsoft Learn (ES)](<url oficial>)

**Duración estimada**: X minutos · **Categoría**: lección

## Objetivo

> _Completar al abordar la unidad._

## Checklist de la unidad

- [ ] Leer la unidad oficial en Microsoft Learn
- [ ] Anotar conceptos clave en `conceptos:` del front-matter
- [ ] Redactar `teoria/concepto.md` con analogía y casos de uso
- [ ] Crear `practica/01-preparacion.sql` con dataset sintético
- [ ] Armar `practica/02-ejercicio.sql` con enunciados progresivos
- [ ] Completar `practica/03-solucion.sql` con soluciones comentadas
- [ ] Responder `teoria/preguntas-examen.md`
- [ ] Actualizar `estado: hecho` y `fecha_fin` en este front-matter
- [ ] Abrir PR

## Estructura de archivos de esta unidad

```
.
├── README.md                  # este archivo
├── practica/                  # solo si categoria ∈ {leccion, lab}
│   ├── 01-preparacion.sql
│   ├── 02-ejercicio.sql
│   ├── 03-solucion.sql
│   └── notas.md
└── teoria/                    # siempre presente
    ├── concepto.md
    ├── sintaxis.md
    └── preguntas-examen.md
```

## Convención de presencia de `practica/`

| Categoría | `practica/` | `teoria/` |
|---|---|---|
| `introduccion` | ❌ | ✅ (resumen corto) |
| `leccion` | ✅ | ✅ |
| `lab` | ✅ (es el ejercicio) | ✅ (resumen + reflexión) |
| `quiz` | ❌ | ✅ (con respuestas razonadas) |
| `resumen` | ❌ | ✅ (cheatsheet) |
