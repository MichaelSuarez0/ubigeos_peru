from .core import (
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
from .core.validations import Validations
from .core.ubigeo_converter import UbigeoConverter

__all__ = [
    "Validations",
    "UbigeoConverter",
    "ResourceManager",
    "validate_departamento",
    "validate_provincia",
    "validate_distrito",
    "get_departamento",
    "get_provincia",
    "get_distrito",
    "get_macrorregion",
    "get_ubigeo",
    # "get_medatato",
    "cargar_diccionario",
]

__version__ = "0.2.2"
__version_info__ = (0, 2, 2)
__author__ = "Michael Suárez"
__email__ = "michael-salvador@hotmail.com"