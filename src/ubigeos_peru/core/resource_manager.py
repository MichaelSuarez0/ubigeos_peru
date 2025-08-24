from pathlib import Path
import orjson

# Configuración de recursos
BASE_DIR = Path(__file__).parent.resolve()
RESOURCE_DIR = BASE_DIR.parent / 'resources'
_RESOURCE_FILES = {
    'departamentos': "departamentos.json",
    'provincias': "provincias.json",
    'distritos': "distritos.json",
    'macrorregiones': "macrorregiones.json",
    'equivalencias': "equivalencias.json",
    'otros': "otros.json",
    'inverted': "inverted.json",
}


class ResourceManager:
    _resources_loaded = {
        'departamentos': False,
        'provincias': False,
        'distritos': False,
        'macrorregiones': False,
        'equivalencias': False,
        'otros': False,
        'inverted': False
    }
 

    @classmethod
    def _load_resource(cls, resource_name: str) -> dict[str, str]:
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
        file_path = RESOURCE_DIR / _RESOURCE_FILES[resource_name]
        try:
            with open(file_path, 'rb') as f:
                return orjson.loads(f.read())
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Recurso no encontrado: {file_path}") from e
        
        
    @classmethod
    def _load_resource_if_needed(cls, resource_name: str) -> None:
        """Carga un recurso si aún no ha sido cargado"""
        if not cls._resources_loaded.get(resource_name, False):
            resource_data = cls._load_resource(resource_name)
            cls._resources_loaded[resource_name] = resource_data

