#!/usr/bin/env python3
"""Build glossary from the private DP-800 vault concepts."""
import os, json, re, base64, subprocess

def gh(p):
    return subprocess.run(['gh', 'api', p, '--jq', '.content'],
                          capture_output=True, text=True).stdout.strip()

def gh_tree():
    return subprocess.run(
        ['gh', 'api',
         'repos/ChristianGrimberg/DP-800/git/trees/main?recursive=1',
         '--jq', '.tree | map(select(.path | startswith("001-Curso/Conceptos/"))) | map(.path) | .[]'],
        capture_output=True, text=True).stdout.splitlines()

paths = [p.strip() for p in gh_tree() if p.strip()]
print(f"Encontrados {len(paths)} conceptos")

entries = []
for p in paths:
    name = p.split('/')[-1].replace('.md', '')
    content_b64 = gh(f'repos/ChristianGrimberg/DP-800/contents/{p}')
    try:
        text = base64.b64decode(content_b64).decode('utf-8', errors='ignore')
    except Exception:
        text = ''
    text = re.sub(r'^---.*?---\s*', '', text, count=1, flags=re.DOTALL)
    paragraphs = [pp for pp in text.split('\n\n') if pp.strip() and not pp.startswith('#') and not pp.startswith('!')]
    definition = paragraphs[0].strip() if paragraphs else '_Sin definición._'
    if len(definition) > 400:
        definition = definition[:400] + '...'
    entries.append((name, definition))

entries.sort(key=lambda x: x[0].lower())

with open('recursos/glosario.md', 'w') as f:
    f.write("---\ntipo: Glosario\nfecha_actualizacion: '2026-08-24'\nfuente: 'ChristianGrimberg/DP-800 -> 001-Curso/Conceptos'\n---\n\n")
    f.write("# Glosario del curso DP-800\n\n")
    f.write(f"Glosario con **{len(entries)} conceptos** del curso oficial, espejado desde el repo privado `ChristianGrimberg/DP-800` y mantenido en sincronización.\n\n")
    f.write("Cada entrada tiene una definición breve extraída del material oficial.\n\n")
    f.write("---\n\n")
    f.write("## Índice alfabético\n\n")
    for name, _ in entries:
        slug = name.lower().replace(' ', '-').replace('(', '').replace(')', '').replace('---', '-')
        f.write(f"- [{name}](#{slug})\n")
    f.write("\n---\n\n## Definiciones\n\n")
    for name, definition in entries:
        slug = name.lower().replace(' ', '-').replace('(', '').replace(')', '').replace('---', '-')
        f.write(f"### {name}\n\n{definition}\n\n---\n\n")

print(f"Glosario generado con {len(entries)} entradas")
