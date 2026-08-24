#!/usr/bin/env python3
"""Valida que la estructura del curso y el front-matter cumplan la convención."""
import os
import re
import sys
from pathlib import Path

ROOT = Path('curso')

CATEGORIES_REQUIRING_PRACTICA = {'leccion', 'lab'}
CATEGORIES_NOT_REQUIRING_PRACTICA = {'introduccion', 'quiz', 'resumen'}

REQUIRED_FIELDS_UNIDAD = {
    'tipo', 'curso', 'codigo_curso', 'path', 'modulo', 'unidad', 'codigo', 'slug',
    'categoria', 'url', 'uid', 'duracion_min', 'fecha_actualizacion', 'estado',
    'fecha_inicio', 'fecha_fin', 'ultimo_repaso', 'proximo_repaso', 'pr',
    'conceptos', 'nivel', 'prerequisitos', 'esfuerzo',
}

REQUIRED_FIELDS_MODULO = {
    'tipo', 'curso', 'codigo_curso', 'path', 'modulo', 'codigo', 'slug',
    'uid', 'url', 'duracion_min', 'fecha_actualizacion', 'estado',
}

VALID_CATEGORIES = CATEGORIES_REQUIRING_PRACTICA | CATEGORIES_NOT_REQUIRING_PRACTICA
VALID_ESTADOS = {'por-hacer', 'por-empezar', 'en-curso', 'hecho', 'completado'}
VALID_NIVELES = {'basico', 'intermedio', 'avanzado'}
VALID_ESFUERZOS = {'corto', 'medio', 'largo'}


def parse_fm(text):
    m = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
    if not m:
        return {}, False
    fm = {}
    cur_key = None
    cur_list = None
    for line in m.group(1).splitlines():
        if re.match(r'^[a-z_]+:', line) and not line.startswith('  -'):
            if cur_list is not None:
                fm[cur_key] = cur_list
                cur_list = None
            key, _, val = line.partition(':')
            val = val.strip().strip('"').strip("'")
            cur_key = key.strip()
            if val == '':
                cur_list = []
            else:
                fm[cur_key] = val
        elif line.strip().startswith('- ') and cur_list is not None:
            cur_list.append(line.strip()[2:].strip())
    if cur_list is not None:
        fm[cur_key] = cur_list
    return fm, True


def check_unidad(path: Path, errors: list):
    text = path.read_text(encoding='utf-8', errors='ignore')
    fm, has_fm = parse_fm(text)
    rel = path.relative_to('.')

    if not has_fm:
        errors.append(f"{rel}: sin front-matter")
        return

    if fm.get('tipo') != 'Unidad':
        return

    missing = REQUIRED_FIELDS_UNIDAD - set(fm.keys())
    if missing:
        errors.append(f"{rel}: faltan campos obligatorios: {sorted(missing)}")

    cat = fm.get('categoria', '')
    if cat not in VALID_CATEGORIES:
        errors.append(f"{rel}: categoria '{cat}' no válida ({sorted(VALID_CATEGORIES)})")

    if fm.get('estado') not in VALID_ESTADOS:
        errors.append(f"{rel}: estado '{fm.get('estado')}' no válido ({sorted(VALID_ESTADOS)})")

    if fm.get('nivel') not in VALID_NIVELES:
        errors.append(f"{rel}: nivel '{fm.get('nivel')}' no válido ({sorted(VALID_NIVELES)})")

    if fm.get('esfuerzo') not in VALID_ESFUERZOS:
        errors.append(f"{rel}: esfuerzo '{fm.get('esfuerzo')}' no válido ({sorted(VALID_ESFUERZOS)})")

    if fm.get('codigo_curso') != 'DP-800T00':
        errors.append(f"{rel}: codigo_curso debe ser 'DP-800T00'")

    # Validar presencia/ausencia de practica/ solo si la unidad está empezada
    # (estado en-curso o hecho). En estado por-hacer/por-empezar, las carpetas
    # aún no existen por diseño.
    unidad_dir = path.parent
    practica_dir = unidad_dir / 'practica'
    teoria_dir = unidad_dir / 'teoria'

    estado = fm.get('estado', 'por-hacer')
    requiere_estructura = estado in ('en-curso', 'hecho')

    if requiere_estructura:
        if cat in CATEGORIES_REQUIRING_PRACTICA and not practica_dir.exists():
            errors.append(f"{rel}: categoria='{cat}' y estado='{estado}' requiere carpeta practica/")
        elif cat in CATEGORIES_NOT_REQUIRING_PRACTICA and practica_dir.exists():
            errors.append(f"{rel}: categoria='{cat}' NO debe tener carpeta practica/")
        if not teoria_dir.exists():
            errors.append(f"{rel}: falta carpeta teoria/")

        # Si hay practica/, validar archivos esperados
        if practica_dir.exists():
            for f in ['01-preparacion.sql', '02-ejercicio.sql', '03-solucion.sql']:
                if not (practica_dir / f).exists():
                    errors.append(f"{rel}/practica/: falta {f}")


def check_modulo(path: Path, errors: list):
    text = path.read_text(encoding='utf-8', errors='ignore')
    fm, has_fm = parse_fm(text)
    rel = path.relative_to('.')

    if not has_fm:
        errors.append(f"{rel}: sin front-matter")
        return

    if fm.get('tipo') not in ('Indice-de-Modulo', 'Modulo'):
        return

    missing = REQUIRED_FIELDS_MODULO - set(fm.keys())
    if missing:
        errors.append(f"{rel}: faltan campos obligatorios: {sorted(missing)}")


def main():
    errors = []
    count_unidades = 0
    count_modulos = 0

    for path in ROOT.rglob('README.md'):
        rel = str(path.relative_to('.'))
        if '_plantillas' in rel or '_meta' in rel:
            continue

        text = path.read_text(encoding='utf-8', errors='ignore')
        fm, _ = parse_fm(text)
        tipo = fm.get('tipo', '')

        if tipo == 'Unidad':
            count_unidades += 1
            check_unidad(path, errors)
        elif tipo in ('Indice-de-Modulo', 'Modulo'):
            count_modulos += 1
            check_modulo(path, errors)

    print(f"Unidades revisadas: {count_unidades}")
    print(f"Módulos revisados: {count_modulos}")

    if errors:
        print(f"\n❌ {len(errors)} errores encontrados:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("\n✅ Estructura y front-matter válidos.")


if __name__ == '__main__':
    main()
