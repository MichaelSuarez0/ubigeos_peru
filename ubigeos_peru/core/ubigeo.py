import os
from typing import Literal, Any
import unicodedata
import orjson

# Configuración de recursos
BASE_DIR = os.path.dirname(__file__)
RESOURCE_DIR = os.path.join(BASE_DIR, '..', 'resources')
_RESOURCE_FILES = {
    'departamentos': "departamentos.json",
    'provincias': "provincias.json",
    'distritos': "distritos.json",
    'macrorregiones': "macrorregiones.json",
    'equivalencias': "equivalencias.json",
}

def eliminar_acentos(texto: str) -> str:
    texto_normalizado = unicodedata.normalize("NFKD", texto)
    texto_sin_acentos = "".join(
        c for c in texto_normalizado if not unicodedata.combining(c)
    )
    return texto_sin_acentos


# TODO: Guardar los datos de ubigeos en dataclasses y ponerlas en Ubigeo como dependencias con lazy loading
# TODO: También colocar métodos para exportar las bases de datos
class Ubigeo:
    _instance = None
    _resources_loaded = {
        'departamentos': False,
        'provincias': False,
        'distritos': False,
        'macrorregiones': False,
        'equivalencias': False,
        'global': False
    }
    
    _DEPARTAMENTOS = None
    _PROVINCIAS = None
    _DISTRITOS = None
    _MACRORREGIONES = None
    _EQUIVALENCIAS = None
    _GLOBAL = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Ubigeo, cls).__new__(cls)
        return cls._instance

    @classmethod
    def _load_resource(cls, resource_name: str) -> None:
        """
        Carga un recurso JSON desde el directorio de recursos con cache.
        
        Args:
            resource_name: Nombre clave del recurso (debe estar en _RESOURCE_FILES)
        
        Returns:
            Diccionario con los datos del JSON
        
        Raises:
            FileNotFoundError: Si el recurso no existe
            json.JSONDecodeError: Si el archivo no es JSON válido
        """
        file_path = os.path.join(RESOURCE_DIR, _RESOURCE_FILES[resource_name])
        try:
            with open(file_path, 'rb') as f:
                resource_data = orjson.loads(f.read())
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Recurso no encontrado: {file_path}") from e
        
        setattr(cls, f"_{resource_name.upper()}", resource_data)
        
    @classmethod
    def _load_resource_if_needed(cls, resource_name: str) -> None:
        """Carga un recurso si aún no ha sido cargado"""
        if not cls._resources_loaded.get(resource_name.lower(), False):
            cls._load_resource(resource_name)
            cls._resources_loaded[resource_name.lower()] = True


    @classmethod
    def _validate_codigo(cls, codigo: str | int) -> str:
        if isinstance(codigo, int):
            codigo = str(codigo)

        if isinstance(codigo, str):
            if len(codigo) == 1:
                codigo = codigo.zfill(2)
            elif len(codigo) == 5:
                codigo = codigo.zfill(6)
            elif len(codigo) > 6:
                raise ValueError("No se aceptan ubigeos con más de 6 caracteres")
        else:
            raise ValueError("No se aceptan valores que no sean string o integers")

        return codigo

    @classmethod
    def normalize_departamento(cls, nombre_departamento: str, upper: bool = True) -> str:
        """"""
        cls._load_resource_if_needed('equivalencias')
        
        # if cls._EQUIVALENCIAS is None:
        #     raise RuntimeError("No se pudieron cargar las equivalencias")
        
        nombre_departamento = eliminar_acentos(nombre_departamento).strip().upper()
        try:
            departamento = cls._EQUIVALENCIAS["departamentos"][nombre_departamento]
        except KeyError:
            raise ValueError(
                f"No se ha encontrado el departamento {nombre_departamento}"
            )
        
        if not upper:
            return departamento
        else:
            return eliminar_acentos(departamento).strip().upper()

    @classmethod
    def normalize_ubicacion(
        cls, 
        nombre_ubicacion: str, 
        ignore_errors: bool = False
    ) -> str:
        """"""
        nombre_ubicacion = eliminar_acentos(nombre_ubicacion).strip().upper()
        try:
            resultado = cls._EQUIVALENCIAS["departamentos"][nombre_ubicacion]
        except KeyError:
            try:
                resultado = cls._EQUIVALENCIAS["provincias"][nombre_ubicacion]
            except KeyError:
                try:
                    resultado = cls._EQUIVALENCIAS["distritos"][nombre_ubicacion]
                except KeyError:
                    if not ignore_errors:
                        raise ValueError(
                            f"No se encontró el lugar {nombre_ubicacion} en la base de datos de departamentos, provincias o distritos"
                        )
                    else:
                        resultado = nombre_ubicacion

        return resultado

    @classmethod
    def get_departamento(
        cls,
        codigo: str | int,
        institucion: Literal["inei", "reniec", "sunat"] = "inei",
        normalize: bool = True,
    ) -> str:
        """
        Obtiene el nombre de un departamento a partir de su código de ubigeo.

        Parameters
        ----------
        codigo : str or int
            Código de ubigeo (recomendado 2 o 6 caracteres).
        institucion : str, optional
            Institución a utilizar como fuente de datos.
            Opciones: 'inei', 'reniec', 'sunat', por defecto 'inei'
        normalize : bool, optional
            Si se cambia a False, retorna nombre oficial con gramática correcta (ex. Junín), por defecto True.

        Returns
        -------
        str
            Nombre del departamento, normalizado si normalize=True.

        Raises
        ------
        ValueError
            Si el código supera los 6 caracteres o no es str/int.
        KeyError
            Si el código no existe en la base de datos.

        Notes
        -----
        - Para códigos de longitud impar (1, 3 o 5), se asume que falta un cero inicial y se añadirá.
        - El subcódigo para departamento se toma de los últimos 2 caracteres del código validado.
        - Se recomienda utilizar strings de 2 o 6 caracteres.
        """
        cls._load_resource_if_needed('departamentos')
        codigo = cls._validate_codigo(codigo)

        try:
            result = cls._DEPARTAMENTOS[institucion][codigo[-2:]]
        except KeyError:
            raise KeyError(
                f"El código de ubigeo {codigo} no se encontró en la base de datos"
            )

        if normalize:
            return eliminar_acentos(result).upper()
        else:
            return result

    @classmethod
    def get_provincia(
        cls,
        codigo: str | int,
        institucion: Literal["inei", "reniec", "sunat"] = "inei",
        normalize: bool = True,
    ) -> str:
        """
        Obtiene el nombre de una provincia a partir de su código de ubigeo.

        Parameters
        ----------
        codigo : str or int
            Código de ubigeo (recomendado 4 o 6 caracteres).
        institucion : str, optional
            Institución como fuente de datos. Opciones: 'inei', 'reniec', 'sunat' (por defecto 'inei').
        normalize : bool, optional
            Si se cambia a False, retorna nombre oficial con gramática correcta (ex. Junín), por defecto True.

        Returns
        -------
        str
            Nombre de la provincia, normalizado si normalize=True.

        Raises
        ------
        ValueError
            Si el código tiene menos de 4 caracteres o supera los 6 caracteres, o no es str/int.
        KeyError
            Si el código no existe en la base de datos.

        Notes
        -----
        - Para códigos de longitud impar (3 o 5), se asume que falta un cero inicial y se añadirá.
        - El subcódigo para provincia se toma de los últimos 4 caracteres del código validado.
        - Se recomienda utilizar strings de 4 o 6 caracteres.
        """
        cls._load_resource_if_needed('provincia')
        codigo = cls._validate_codigo(codigo)
        
        if len(codigo) < 4:
            raise ValueError(
                "No se aceptan ubigeos con menos de 4 caracteres para provincias"
            )

        result = cls._PROVINCIAS[institucion][codigo[-4:]]

        if normalize:
            return eliminar_acentos(result).upper()
        else:
            return result

    @classmethod
    def get_distrito(
        cls,
        codigo: str | int,
        institucion: Literal["inei", "reniec", "sunat"] = "inei",
        normalize: bool = True,
    ) -> str:
        """
        Obtiene el nombre de un distrito a partir de su código de ubigeo.

        Parameters
        ----------
        codigo : str or int
            Código de ubigeo (6 caracteres).
        institucion : str, optional
            Institución a utilizar como fuente de datos.
            Opciones: 'inei', 'reniec', 'sunat', por defecto 'inei'
        normalize : bool, optional
            Si se cambia a False, retorna nombre oficial con gramática correcta (ex. Junín), por defecto True.

        Returns
        -------
        str
            Nombre del distrito, normalizado si normalize=True.

        Raises
        ------
        ValueError
            Si el código no tiene 6 caracteres o no es str/int.
        KeyError
            Si el código no existe en la base de datos.

        Notes
        -----
        -
        """
        cls._load_resource_if_needed('distrito')
        codigo = cls._validate_codigo(codigo)
        
        if len(codigo) != 6:
            raise ValueError(
                "No se aceptan ubigeos que no tengan exactamente 6 caracteres para distritos"
            )

        result = cls._DISTRITOS[institucion][codigo]

        if normalize:
            return eliminar_acentos(result).upper()
        else:
            return result


    @classmethod
    def get_macrorregion(
        cls,
        codigo_o_departamento: str | int,
        institucion: Literal["inei", "minsa", "ceplan"] = "inei",
        normalize: bool = True,
    )-> str:
        """
        Obtiene el nombre de una macrorregión a partir de su código o nombre de departamento.

        Parameters
        ----------
        codigo_o_departamento : str or int
            Código de ubigeo (recomendado 2 o 6 caracteres) o nombre del departamento.
        institucion : str, optional
            Institución como fuente de datos. Opciones: 'inei', 'minsa', 'ceplan' (por defecto 'inei').
        normalize : bool, optional
            Si se cambia a False, retorna nombre oficial con gramática correcta (ex. Junín), por defecto True.

        Returns
        -------
        str
            Nombre de la macrorregión, normalizado si normalize=True.

        Raises
        ------
        ValueError
            Si el código o el nombre del departamento no es válido o no se encuentra en la base de datos.
        KeyError
            Si el código o el nombre del departamento no existe en la base de datos de macrorregiones.

        Notes
        -----
        - Si se proporciona un nombre de departamento, este será convertido a minúsculas, normalizado y usado para la búsqueda.
        - Se recomienda usar strings de 2 o 6 caracteres para códigos de ubigeo.
        """
        if isinstance(codigo_o_departamento, str) and codigo_o_departamento[0] not in list(range(0, 10)):
            departamento = codigo_o_departamento

        departamento = eliminar_acentos(departamento).lower().strip()

        return eliminar_acentos(cls._MACRORREGIONES[institucion][departamento])


    @classmethod
    def get_ubigeo(
        cls,
        lugar: str,
        level: Literal["departamento", "distrito", "provincia"] = "departamento",
        institucion: Literal["inei", "reniec", "sunat"] = "inei",
        normalize: bool = False,
    ):
        pass

    @classmethod
    def get_otros(
        cls, codigo_o_departamento: str | int, key: Literal["capital", "superficie"]
    ):
        pass
