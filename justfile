# Justfile para formateo y limpieza del código

# Usa shell bash en sistemas Windows/WSL/Unix
set shell := ["powershell.exe", "-Command"]

format-all:
    uv run ruff check --fix . --exit-zero
    uv run ruff format .

test:
    uv run pytest
