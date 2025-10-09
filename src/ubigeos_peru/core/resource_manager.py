from pathlib import Path
from typing import Any, Literal
import orjson

# Configuración de recursos
RESOURCE_DIR = Path(__file__).parent.parent / "resources"

ResourceName = Literal[
    "departamentos",
    "provincias",
    "distritos",
    "macrorregiones",
    "equivalencias",
    "otros",
    "inverted",
]

_RESOURCE_FILES: dict[ResourceName, str] = {
    "departamentos": "departamentos.json",
    "provincias": "provincias.json",
    "distritos": "distritos.json",
    "macrorregiones": "macrorregiones.json",
    "equivalencias": "equivalencias.json",
    "otros": "otros.json",
    "inverted": "inverted.json",
}


class ResourceManager:
    _loaded: dict[str, dict[str, Any]] = {}

    @classmethod
    def cargar_diccionario(
        cls,
        resource_name: ResourceName
    ) -> dict[str, Any]:
        """
        Carga un recurso JSON desde el directorio de recursos con lazy loading

        Args:
            resource_name: Nombre clave del recurso (debe estar en _RESOURCE_FILES)

        Returns:
            Diccionario con los datos del JSON

        Raises:
            FileNotFoundError: Si el recurso no existe
            json.JSONDecodeError: Si el archivo no es JSON válido
        """
        if resource_name not in cls._loaded:
            file_path = RESOURCE_DIR / _RESOURCE_FILES[resource_name]
            try:
                with open(file_path, "rb") as f:
                    resource_data = orjson.loads(f.read())
                    cls._loaded[resource_name] = resource_data
            except FileNotFoundError as e:
                raise FileNotFoundError(f"Recurso no encontrado: {file_path}") from e
        else:
            resource_data = cls._loaded[resource_name]
        return resource_data
