# Cheatsheet de comandos útiles

## Conexión a SQL

```bash
# Conectar con sqlcmd (interactivo)
sqlcmd -C -S sql -U sa -P "<password>" -d dp800_lab

# Ejecutar query one-shot
sqlcmd -C -S sql -U sa -P "<password>" -Q "SELECT @@VERSION"

# Ejecutar archivo SQL
sqlcmd -C -S sql -U sa -P "<password>" -i ./script.sql

# Conectar con mssql-cli (mejor UX)
mssql-cli -S sql -U sa -P "<password>" -d dp800_lab

# Wrapper del repo (lee .env automáticamente)
bash scripts/conectar-sql.sh "SELECT @@VERSION"
bash scripts/conectar-sql.sh                # abre mssql-cli interactivo
```

## Contenedor de desarrollo

```bash
# Levantar
docker compose -f .devcontainer/docker-compose.yml up -d

# Ver logs
docker compose -f .devcontainer/docker-compose.yml logs -f sql
docker compose -f .devcontainer/docker-compose.yml logs -f ollama

# Reiniciar SQL (limpia volúmenes)
bash scripts/reiniciar-bd.sh

# Bajar todo
docker compose -f .devcontainer/docker-compose.yml down

# Bajar y limpiar volúmenes (CUIDADO: borra datos)
docker compose -f .devcontainer/docker-compose.yml down -v
```

## Ollama (modelos para IA)

```bash
# Listar modelos instalados
docker exec ollama ollama list

# Descargar modelo nuevo
docker exec ollama ollama pull llama3.2:3b

# Probar embedding
curl -X POST http://localhost:11434/api/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model":"nomic-embed-text","prompt":"hola mundo"}'

# Probar generación
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"llama3.2:3b","prompt":"Hola, quién eres?","stream":false}'
```

## Lint SQL

```bash
# Local
sqlfluff lint curso/ --dialect tsql

# Solo práctica
sqlfluff lint curso/ --dialect tsql --paths curso/path-1-diseno-y-desarrollo-de-soluciones-de-base-de-datos/modulo-1.1-*/unidades/*/practica/

# Fix automático (usar con cuidado)
sqlfluff fix curso/ --dialect tsql

# Via wrapper
bash scripts/lint-sql.sh
```

## MkDocs (sitio de documentación)

```bash
# Servir local con hot-reload
mkdocs serve

# Build estricto (falla si hay warnings)
mkdocs build --strict

# Build normal
mkdocs build
```

## Git

```bash
# Crear rama para nueva unidad
git checkout -b feature/1.1.3-creacion-tablas

# Estado
git status

# Commit con convención
git add .
git commit -m "✨ agregar práctica de creación de tablas (1.1.3)"

# Push y abrir PR
git push -u origin feature/1.1.3-creacion-tablas
gh pr create --fill --base main
```

## GitHub CLI

```bash
# Ver issues
gh issue list --label modulo --state open

# Crear issue desde plantilla
gh issue create --template nueva-practica.yml

# Ver PR actual
gh pr view --web

# Ver estado de CI
gh pr checks
```

## Generar mapa de aprendizaje

```bash
# Local
bash scripts/generar-mapa.sh

# El output se escribe en docs/mapa-de-aprendizaje.md
# El workflow .github/workflows/generar-mapa.yml lo corre en CI
```
