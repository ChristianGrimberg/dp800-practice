---
nombre: preparar-siguiente-tema
version: 1.0
idioma: es
agentes_recomendados:
  - arquitecto-dp800
  - documentador
---

# Skill: preparar-siguiente-tema

## Qué hace

Toma un issue ya creado por el workflow `siguiente-tema.yml` (con metadata básica: código, título, URL de MS Learn) y lo enriquece con:

1. Resumen extraído de Microsoft Learn vía `webfetch`.
2. Borrador de `teoria/concepto.md` con analogía y casos de uso.
3. Sugerencia de `practica/01-preparacion.sql` (esquema de tablas, no SQL final).
4. Casos de uso reales sugeridos (mínimo 2).
5. Preguntas tipo examen sugeridas (mínimo 3).
6. Lista de prerrequisitos chequeables con checkboxes.

Luego actualiza el issue con todo esto como un comentario nuevo (no modifica el original para mantener el historial).

## Cuándo invocarlo

- "Usá el skill preparar-siguiente-tema sobre el issue #42"
- "Enriqueceme el último issue de práctica"

## Inputs

- `numero_issue` (int, requerido).

## Outputs

Un comentario nuevo en el issue con todas las secciones mencionadas, listo para que el usuario lo revise y use como base para crear la rama y los archivos.

## Pasos internos

1. Obtener el issue: `gh issue view <n> --json title,body,labels`.
2. Extraer el código de unidad del título (formato `📚 Practicar Unidad X.Y.Z — <título>`).
3. Leer el front-matter de la unidad objetivo para conocer `url`, `duracion_min`, `prerequisitos`.
4. `webfetch` contra `url` para extraer:
   - Resumen ejecutivo.
   - Temas cubiertos.
5. Generar el comentario enriquecido con todas las secciones.
6. Postear el comentario con `gh issue comment <n> --body-file /tmp/comentario.md`.

## Restricciones

- **No crear archivos nuevos** en el repo. Solo postear al issue.
- **No abrir PR** ni crear rama.
- **No commitear**.
- Si la `webfetch` falla, generar el contenido solo a partir del front-matter local y avisar.

## Plantilla del comentario

```markdown
## 📚 Preparación para la Unidad X.Y.Z — <título>

### Resumen extraído de Microsoft Learn

<resumen>

### Prerrequisitos

- [ ] Unidad X.Y.Z-1 (si aplica)
- [ ] Concepto: ...

### Esquema sugerido para practica/01-preparacion.sql

- Tabla `demo.<X>` con columnas ...
- Tabla `demo.<Y>` con relación ...
- Volumen: ~<N> filas

### Casos de uso sugeridos

1. ...
2. ...

### Preguntas tipo examen sugeridas

1. ...
2. ...
3. ...

### Próximos pasos

- [ ] Invocar al agente `arquitecto-dp800` con el skill `planificar-capitulo`
- [ ] Crear rama `feature/<codigo>-<slug>`
- [ ] Seguir el checklist del README de la unidad
```

## Ejemplo de invocación

```text
"Usá el skill preparar-siguiente-tema sobre el issue #42"
```
