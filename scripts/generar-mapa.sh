#!/usr/bin/env bash
# generar-mapa.sh — regenera docs/mapa-de-aprendizaje.md desde front-matter.
#
# Recorre todos los README.md bajo curso/**/unidades/*/, extrae los campos
# relevantes del front-matter y reescribe el mapa en español con:
#   - Tabla maestra de unidades (módulo, código, título, estado, PR, próximo repaso).
#   - Sección "Para repasar hoy" (proximo_repaso <= hoy y estado = hecho).
#   - Sección "Pendientes" (estado = por-hacer, ordenado por código).
#   - Sección "Avance por módulo" (% completado).
#   - Sección "Conceptos más frecuentes".
#
# Salida: docs/mapa-de-aprendizaje.md

set -euo pipefail

cd "$(dirname "$0")/.."

OUT="docs/mapa-de-aprendizaje.md"
mkdir -p docs
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

if ! command -v python3 >/dev/null 2>&1; then
  echo "❌ python3 requerido"
  exit 1
fi

python3 <<'PY' | tee "$TMP"
import os, re, sys, json
from collections import Counter, defaultdict
from datetime import date

ROOT = 'curso'
OUT = 'docs/mapa-de-aprendizaje.md'

def parse_fm(text):
    """Devuelve dict con el front-matter; vacío si no hay."""
    m = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    cur_key = None
    cur_list = None
    for line in m.group(1).splitlines():
        if re.match(r'^[a-z_]+:', line) and not line.startswith('  -'):
            if cur_list is not None:
                fm[cur_key] = cur_list
                cur_list = None
            key, _, val = line.partition(':')
            val = val.strip()
            cur_key = key.strip()
            val = val.strip('"').strip("'")
            if val == '':
                cur_list = []
            else:
                fm[cur_key] = val
        elif line.strip().startswith('- ') and cur_list is not None:
            cur_list.append(line.strip()[2:].strip())
    if cur_list is not None:
        fm[cur_key] = cur_list
    return fm

units = []
modules = {}
paths = {}

for dirpath, _, files in os.walk(ROOT):
    # Excluir plantillas para no contaminar el mapa
    if '_plantillas' in dirpath:
        continue
    for f in files:
        if f != 'README.md':
            continue
        path = os.path.join(dirpath, f)
        with open(path) as fh:
            text = fh.read()
        fm = parse_fm(text)
        if fm.get('tipo') != 'Unidad':
            continue
        codigo = fm.get('codigo', '')
        modulo = fm.get('modulo', '')
        path_name = fm.get('path', '')
        unidad = fm.get('unidad', '')
        estado = fm.get('estado', 'por-hacer')
        categoria = fm.get('categoria', '')
        pr = fm.get('pr', '')
        ult = fm.get('ultimo_repaso') or ''
        prox = fm.get('proximo_repaso') or ''
        conceptos = fm.get('conceptos') or []
        if not isinstance(conceptos, list):
            conceptos = []
        dur = fm.get('duracion_min', '')
        url = fm.get('url', '')
        rel = os.path.relpath(path, '.')
        units.append({
            'codigo': codigo, 'modulo': modulo, 'unidad': unidad,
            'estado': estado, 'categoria': categoria, 'pr': pr,
            'ultimo_repaso': ult, 'proximo_repaso': prox,
            'conceptos': conceptos, 'duracion': dur, 'url': url, 'path': rel,
            'path_name': path_name,
        })

units.sort(key=lambda u: u['codigo'])

today = date.today().isoformat()

por_hacer = [u for u in units if u['estado'] == 'por-hacer']
en_curso = [u for u in units if u['estado'] == 'en-curso']
hechas = [u for u in units if u['estado'] == 'hecho']
repasar_hoy = [u for u in hechas if u['proximo_repaso'] and u['proximo_repaso'] <= today]

mod_totals = Counter()
mod_done = Counter()
for u in units:
    mod_totals[u['modulo']] += 1
    if u['estado'] == 'hecho':
        mod_done[u['modulo']] += 1

path_totals = Counter()
path_done = Counter()
for u in units:
    path_totals[u['path_name']] += 1
    if u['estado'] == 'hecho':
        path_done[u['path_name']] += 1

concept_count = Counter()
for u in units:
    for c in u['conceptos']:
        concept_count[c] += 1

lines = []
lines.append('---')
lines.append('title: Mapa de aprendizaje')
lines.append('fecha_generacion: ' + today)
lines.append('generado_por: scripts/generar-mapa.sh')
lines.append('---')
lines.append('')
lines.append('# Mapa de aprendizaje — DP-800 practice')
lines.append('')
lines.append(f'_Última regeneración: {today} · Total unidades: {len(units)}_')
lines.append('')
lines.append('> Este mapa se regenera automáticamente en CI cada vez que cambia un front-matter de unidad. Para repasar eficientemente, empezá por la sección "Para repasar hoy".')
lines.append('')
lines.append('## Resumen global')
lines.append('')
lines.append('| Estado | Cantidad | % |')
lines.append('|---|---|---|')
for estado, lista in [('por-hacer', por_hacer), ('en-curso', en_curso), ('hecho', hechas)]:
    pct = (len(lista) * 100 // len(units)) if units else 0
    lines.append(f'| {estado} | {len(lista)} | {pct}% |')
lines.append('')

lines.append('## Para repasar hoy')
lines.append('')
if repasar_hoy:
    lines.append('| Código | Unidad | Último repaso | Próximo |')
    lines.append('|---|---|---|---|')
    for u in sorted(repasar_hoy, key=lambda x: x['proximo_repaso']):
        lines.append(f"| {u['codigo']} | [{u['unidad']}]({u['path']}) | {u['ultimo_repaso']} | {u['proximo_repaso']} |")
else:
    lines.append('_Nada pendiente de repaso._')
lines.append('')

lines.append('## Pendientes')
lines.append('')
if por_hacer:
    lines.append('| Código | Módulo | Unidad | Categoría | Duración |')
    lines.append('|---|---|---|---|---|')
    for u in por_hacer:
        lines.append(f"| {u['codigo']} | {u['modulo']} | [{u['unidad']}]({u['path']}) | {u['categoria']} | {u['duracion']} min |")
else:
    lines.append('_Todo completado._')
lines.append('')

lines.append('## En curso')
lines.append('')
if en_curso:
    lines.append('| Código | Módulo | Unidad | PR |')
    lines.append('|---|---|---|---|')
    for u in en_curso:
        lines.append(f"| {u['codigo']} | {u['modulo']} | [{u['unidad']}]({u['path']}) | {u['pr'] or '-'} |")
else:
    lines.append('_Ninguna unidad en curso._')
lines.append('')

lines.append('## Avance por path')
lines.append('')
lines.append('| Path | Hechas | Total | % |')
lines.append('|---|---|---|---|')
for p in sorted(path_totals):
    tot = path_totals[p]
    done = path_done[p]
    pct = (done * 100 // tot) if tot else 0
    lines.append(f'| {p} | {done} | {tot} | {pct}% |')
lines.append('')

lines.append('## Avance por módulo')
lines.append('')
lines.append('| Módulo | Hechas | Total | % |')
lines.append('|---|---|---|---|')
for m in sorted(mod_totals):
    tot = mod_totals[m]
    done = mod_done[m]
    pct = (done * 100 // tot) if tot else 0
    lines.append(f'| {m} | {done} | {tot} | {pct}% |')
lines.append('')

lines.append('## Conceptos más frecuentes')
lines.append('')
if concept_count:
    lines.append('| Concepto | Apariciones |')
    lines.append('|---|---|')
    for c, n in concept_count.most_common(20):
        lines.append(f'| {c} | {n} |')
else:
    lines.append('_Aún no hay conceptos registrados en unidades._')
lines.append('')

lines.append('## Tabla maestra')
lines.append('')
lines.append('| Código | Módulo | Unidad | Estado | PR | Próximo repaso |')
lines.append('|---|---|---|---|---|---|')
for u in units:
    lines.append(f"| {u['codigo']} | {u['modulo']} | [{u['unidad']}]({u['path']}) | {u['estado']} | {u['pr'] or '-'} | {u['proximo_repaso'] or '-'} |")
lines.append('')

sys.stdout.write('\n'.join(lines))
PY

mv "$TMP" "$OUT"
echo "✅ Mapa regenerado: $OUT"
