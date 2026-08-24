---
nombre: planificar-capitulo
version: 1.0
idioma: es
agentes_recomendados:
  - arquitecto-dp800
---

# Skill: planificar-capitulo

## Qué hace

Dado un código de unidad (ej. `1.1.3`) o un título libre, genera un plan completo en Markdown para abordarla. Incluye objetivo, prerrequisitos, checklist paso a paso, tiempo estimado y conceptos clave.

## Cuándo invocarlo

- "Planificá la unidad 1.1.4"
- "Necesito un plan para CTEs recursivas"
- "Decime cómo abordar la unidad 3.2.5"

## Inputs

- `codigo_unidad` (opcional): código X.Y.Z del curso oficial.
- `titulo` (opcional): título libre si no hay código.

## Outputs

Markdown con la siguiente estructura:

```markdown
# Plan: Unidad X.Y.Z — <título>

**Path**: ...
**Módulo**: ...
**Duración estimada**: ... min
**Fuente**: [Microsoft Learn](url)

## Objetivo
<una frase medible>

## Prerrequisitos
- [ ] Unidad X.Y.Z-1 ...
- [ ] Conceptos: ...

## Checklist
- [ ] Leer la unidad oficial
- [ ] Redactar teoria/concepto.md (usar agente documentador)
- [ ] Generar dataset sintético (usar agente generador-practicas)
- [ ] Armar 02-ejercicio.sql
- [ ] Resolver y completar 03-solucion.sql
- [ ] Responder preguntas-examen.md
- [ ] Actualizar front-matter
- [ ] Abrir PR (usar skill abrir-pr-desde-capitulo)

## Conceptos clave a cubrir
- ...

## Riesgos
- ...
```

## Pasos internos

1. Leer `curso/_meta/course-hierarchy.json` para encontrar la unidad.
2. Si la unidad tiene `prerrequisitos` en su front-matter local, incluirlos.
3. Consultar unidades vecinas para asegurar coherencia.

## Restricciones

- Solo produce el plan como texto. **No crea archivos** a menos que el usuario lo pida explícitamente.
- Siempre incluir link a la unidad oficial en MS Learn.

## Ejemplo de invocación

```text
"Usá el skill planificar-capitulo para la unidad 1.1.3"
```
