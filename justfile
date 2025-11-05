# Justfile para formateo y limpieza del código

# Usa shell bash en sistemas Windows/WSL/Unix
set shell := ["powershell.exe", "-Command"]

# Comando principal
update:
    # 🔄 Actualizar hooks de pre-commit
    pre-commit autoupdate


format-all:
    # 🧹 Eliminar imports y variables sin usar
    uv run autoflake --in-place --remove-unused-variables --remove-all-unused-imports \
    --exclude '*/__init__.py' -r .

    # 🧭 Ordenar los imports
    uv run isort . --profile black

    # 🐶 Formatear código con Ruff
    uv run ruff check --fix . --exit-zero
    uv run ruff format .
