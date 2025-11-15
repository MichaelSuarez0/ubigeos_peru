from .core import (
    Departamento,
    Ubigeo,
    cargar_diccionario,
    get_departamento,
    get_distrito,
    get_macrorregion,
    get_provincia,
    get_ubigeo,
    validate_departamento,
    validate_provincia,
    validate_distrito
)
from .core.resource_manager import ResourceManager

__all__ = [
    "Departamento",
    "Ubigeo",
    "ResourceManager",
    "validate_departamento",
    "validate_provincia",
    "validate_distrito",
    "get_departamento",
    "get_provincia",
    "get_distrito",
    "get_macrorregion",
    "get_ubigeo",
    "get_medatato",
    "cargar_diccionario",
]
