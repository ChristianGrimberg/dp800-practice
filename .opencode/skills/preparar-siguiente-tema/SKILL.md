---
nombre: preparar-siguiente-tema
version: 2.0
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
7. **Verificación post-enriquecimiento** (obligatoria): leer de vuelta el
   issue y el comentario, confirmar que el Markdown renderiza bien
   (saltos de línea reales, sin `\n` literales) y que el comentario
   contiene las 6 secciones. Si algo no se renderiza bien, regenerar el
   contenido y volver a postear; nunca dejar el issue con texto roto.

## Verificación post-enriquecimiento

```bash
# 1. El cuerpo del issue no debe contener \\n literales
ISSUE_BODY=$(gh issue view "$ISSUE_ISSUE" --json body --jq '.body')
if echo "$ISSUE_BODY" | grep -q '\\n'; then
  echo "FAIL: el cuerpo del issue #$ISSUE_ISSUE tiene \\n literales."
  exit 1
fi

# 2. El último comentario sí debe tener saltos de línea reales y secciones esperadas
LAST_COMMENT=$(gh issue view "$ISSUE_ISSUE" --comments --json comments \
  --jq '.comments | last | .body')
if echo "$LAST_COMMENT" | grep -q '\\n'; then
  echo "FAIL: el comentario de enriquecimiento tiene \\n literales."
  exit 1
fi
for sec in 'Resumen extraído' Prerrequisitos 'Esquema sugerido' \
           'Casos de uso' 'Preguntas tipo examen'; do
  echo "$LAST_COMMENT" | grep -q "$sec" || {
    echo "FAIL: falta la sección '$sec' en el comentario."
    exit 1;
  }
done
echo "OK: issue #$ISSUE_ISSUE enriquecido correctamente."
```

## Restricciones

- **No crear archivos nuevos** en el repo. Solo postear al issue.
- **No abrir PR** ni crear rama.
- **No commitear**.
- Si la `webfetch` falla, generar el contenido solo a partir del front-matter local y avisar.
- **Nunca dar por terminado el skill sin haber ejecutado la verificación
  post-enriquecimiento.** Si la verificación falla, regenerar y volver a
  postear. El issue debe quedar legible en Markdown.

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
