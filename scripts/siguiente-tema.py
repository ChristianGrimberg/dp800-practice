#!/usr/bin/env python3
"""
siguiente-tema.py — detecta qué unidad se practicó en el último merge a main
y emite variables de entorno con los datos de la siguiente unidad sugerida.

Uso local:
    python3 scripts/siguiente-tema.py \
        --merged-pr 5 \
        --curso-json curso/_meta/course-hierarchy.json

Uso en workflow:
    python3 scripts/siguiente-tema.py \
        --merged-pr "${{ github.event.pull_request.number }}" \
        --curso-json curso/_meta/course-hierarchy.json \
        --emit-env >> $GITHUB_ENV

Salida:
    - Stdout: variables de entorno en formato KEY=value si --emit-env.
    - Las variables escalares se emiten como ``KEY=valor``.
    - Las variables multi-línea (p.ej. ``SIGUIENTE_CUERPO``) se emiten con
      sintaxis heredoc de GitHub Actions (``KEY<<DELIM\\ncontenido\\nDELIM``)
      para preservar saltos de línea reales.
    - Variables emitidas:
        SIGUIENTE_CODIGO    (ej: 1.1.4)
        SIGUIENTE_TITULO    (ej: Optimización con índices)
        SIGUIENTE_PATH_DIR  (ruta relativa a la unidad)
        SIGUIENTE_URL       (URL oficial en Microsoft Learn)
        SIGUIENTE_DURACION  (minutos)
        SIGUIENTE_CATEGORIA (introduccion | leccion | lab | quiz | resumen)
        SIGUIENTE_LABELS    (CSV: modulo:1.1,categoria:leccion,...)
        SIGUIENTE_CUERPO    (Markdown del cuerpo del issue, multi-línea)
"""
import argparse
import json
import os
import re
import subprocess
import sys


def run(cmd, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)


def get_files_in_pr(pr_number):
    """Devuelve la lista de archivos tocados en el PR mergeado."""
    r = subprocess.run(
        ["gh", "pr", "view", str(pr_number), "--json", "files"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        return []
    try:
        return [f["path"] for f in json.loads(r.stdout)["files"]]
    except Exception:
        return []


def get_latest_commit_files(base="main"):
    """Devuelve archivos del último commit en la rama dada."""
    r = run(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"])
    if r.returncode == 0:
        return [l.strip() for l in r.stdout.splitlines() if l.strip()]
    return []


def parse_fm(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    cur_key = None
    cur_list = None
    for line in m.group(1).splitlines():
        if re.match(r"^[a-z_]+:", line) and not line.startswith("  -"):
            if cur_list is not None:
                fm[cur_key] = cur_list
                cur_list = None
            key, _, val = line.partition(":")
            val = val.strip().strip('"').strip("'")
            cur_key = key.strip()
            if val == "":
                cur_list = []
            else:
                fm[cur_key] = val
        elif line.strip().startswith("- ") and cur_list is not None:
            cur_list.append(line.strip()[2:].strip())
    if cur_list is not None:
        fm[cur_key] = cur_list
    return fm


def find_modified_unit(files):
    """Devuelve el codigo de la unidad modificada, si hay una."""
    for f in files:
        m = re.search(r"/unidades/(\d+\.\d+\.\d+)-", f)
        if m:
            return m.group(1)
    return None


def load_units(course_json):
    with open(course_json) as f:
        data = json.load(f)
    units = []
    for path in data["paths"]:
        for mod in path["modules"]:
            for u in mod["units"]:
                units.append({
                    "code": u["uid"].rsplit(".", 1)[-1],  # ej: 3-design-implement-tables
                    "title": u["title"],
                    "url": u["url"],
                    "duration": u["duration_min"],
                    "category": u["category"],
                    "module_code": mod["uid"].rsplit(".", 1)[-1],
                    "module_title": mod["title"],
                    "module_url": mod["url"],
                    "module_index": path["modules"].index(mod),
                    "path_title": path["title"],
                    "path_index": data["paths"].index(path),
                    "position_in_module": mod["units"].index(u),
                    "total_in_module": len(mod["units"]),
                })
    return data["paths"], units


def find_unit_by_code(paths, code):
    """code puede ser 1.1.3 o 3-design-implement-tables; devolvemos dict con unit+mod+path."""
    for path in paths:
        for mod in path["modules"]:
            for unit in mod["units"]:
                if code in (str(mod["modules"].index(mod) + 1) if False else "",):
                    pass
    # Match más simple: el code del front-matter es 1.1.3 pero en el JSON los units
    # están indexados por posición. Reconstruimos el codigo:
    for path_idx, path in enumerate(paths, start=1):
        for mod_idx, mod in enumerate(path["modules"], start=1):
            for unit_idx, unit in enumerate(mod["units"], start=1):
                code_str = f"{path_idx}.{mod_idx}.{unit_idx}"
                if code_str == code:
                    return {
                        "codigo": code_str,
                        "path_idx": path_idx,
                        "mod_idx": mod_idx,
                        "unit_idx": unit_idx,
                        "unit": unit,
                        "mod": mod,
                        "path": path,
                    }
    return None


def next_unit(paths, current):
    """Devuelve la siguiente unidad lógica."""
    cur = find_unit_by_code(paths, current)
    if not cur:
        return None
    path = cur["path"]
    mod = cur["mod"]
    units = mod["units"]
    # ¿Hay otra unidad en el mismo módulo?
    if cur["unit_idx"] < len(units):
        next_u = units[cur["unit_idx"]]
        return {
            "codigo": current,
            "path_idx": cur["path_idx"],
            "mod_idx": cur["mod_idx"],
            "unit_idx": cur["unit_idx"] + 1,
            "unit": next_u,
            "mod": mod,
            "path": path,
        }
    # Si no, saltar al siguiente módulo
    for mod_idx, m in enumerate(path["modules"], start=1):
        if mod_idx > cur["mod_idx"]:
            if m["units"]:
                return {
                    "codigo": current,
                    "path_idx": cur["path_idx"],
                    "mod_idx": mod_idx,
                    "unit_idx": 1,
                    "unit": m["units"][0],
                    "mod": m,
                    "path": path,
                }
    # No hay más unidades (raro)
    return None


def make_issue_body(next_data, prev_codigo, prev_url):
    u = next_data["unit"]
    m = next_data["mod"]
    p = next_data["path"]
    code = f"{next_data['path_idx']}.{next_data['mod_idx']}.{next_data['unit_idx']}"
    return f"""## 📚 Practicar Unidad {code} — {u['title']}

**Path**: {p['title']}
**Módulo**: {m['title']}
**Duración estimada**: {u['duration_min']} minutos
**Categoría**: `{u['category']}`
**Fuente oficial**: [Unidad en Microsoft Learn (ES)]({u['url']})

### Unidad anterior practicada
- Código: `{prev_codigo}`
- Link: [PR mergeado]({prev_url})

### Checklist sugerido

- [ ] Abrir `curso/<ruta-path>/modulo-<...>/unidades/<codigo>-<slug>/`
- [ ] Marcar `estado: en-curso` y `fecha_inicio` en el front-matter
- [ ] Invocar al agente `documentador` con skill `explicar-concepto` para redactar `teoria/concepto.md`
- [ ] Si categoría es `leccion` o `lab`: invocar `generador-practicas` para armar `practica/01-preparacion.sql`
- [ ] Lint SQL: `bash scripts/lint-sql.sh`
- [ ] Abrir PR siguiendo `PULL_REQUEST_TEMPLATE.md`
- [ ] Al mergear, el workflow `siguiente-tema.yml` abrirá el siguiente issue automáticamente

### Tiempo estimado

~{u['duration_min']} minutos de práctica + redacción.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--merged-pr", required=True, help="Número de PR mergeado")
    ap.add_argument("--curso-json", required=True, help="Ruta al course-hierarchy.json")
    ap.add_argument("--emit-env", action="store_true", help="Imprimir en formato env")
    args = ap.parse_args()

    files = get_files_in_pr(args.merged_pr)
    if not files:
        files = get_latest_commit_files()
    codigo = find_modified_unit(files)
    if not codigo:
        print("⚠️  No se detectó unidad modificada en el PR/commit.", file=sys.stderr)
        sys.exit(0)

    with open(args.curso_json) as f:
        data = json.load(f)
    paths = data["paths"]

    nxt = next_unit(paths, codigo)
    if not nxt:
        print(f"⚠️  No hay siguiente unidad después de {codigo}.", file=sys.stderr)
        sys.exit(0)

    prev_url = f"https://github.com/ChristianGrimberg/dp800-practice/pull/{args.merged_pr}"
    body = make_issue_body(nxt, codigo, prev_url)

    code_str = f"{nxt['path_idx']}.{nxt['mod_idx']}.{nxt['unit_idx']}"
    labels = f"módulo:{nxt['mod_idx']},categoria:{nxt['unit']['category']},prioridad:media"

    if args.emit_env:
        def env_scalar(k, v):
            """Variable de una sola línea (KEY=valor)."""
            return f"{k}={v}"

        def env_multiline(k, v):
            """Variable multi-línea con sintaxis heredoc de GitHub Actions.

            GitHub Actions interpreta ``KEY<<DELIM\\ncontenido\\nDELIM``
            y asigna a ``KEY`` el contenido entre delimitadores sin escape,
            preservando saltos de línea reales. Esto evita que el cuerpo del
            issue aparezca con ``\\n`` literales (bug observado en #8).
            """
            delim = "_GH_ENV_EOF_"
            return f"{k}<<{delim}\n{v}\n{delim}"

        print(env_scalar("SIGUIENTE_CODIGO", code_str))
        print(env_scalar("SIGUIENTE_TITULO", nxt["unit"]["title"]))
        print(env_scalar("SIGUIENTE_URL", nxt["unit"]["url"]))
        print(env_scalar("SIGUIENTE_DURACION", str(nxt["unit"]["duration_min"])))
        print(env_scalar("SIGUIENTE_CATEGORIA", nxt["unit"]["category"]))
        print(env_scalar("SIGUIENTE_LABELS", labels))
        print(env_multiline("SIGUIENTE_CUERPO", body))
    else:
        out = {
            "codigo": code_str,
            "titulo": nxt["unit"]["title"],
            "url": nxt["unit"]["url"],
            "duracion": nxt["unit"]["duration_min"],
            "categoria": nxt["unit"]["category"],
            "labels": labels,
            "cuerpo": body,
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
