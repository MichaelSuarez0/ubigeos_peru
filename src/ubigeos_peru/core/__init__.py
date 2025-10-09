"""
Interfaz pública de ubigeos_peru.core

Permite usar la librería con un import compacto:

>>> import ubigeos_peru as ubg
>>> ubg.get_departamento("150101")
'Lima'

Antes:
>>> from ubigeos_peru import Ubigeo as ubg
>>> ubg.get_departamento("150101")
'Lima'

"""

from __future__ import annotations
from typing import Iterable, TypeAlias, Literal, Any, TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd
    import polars as pl

from .ubigeo import Ubigeo
from .departamento import Departamento
from .resource_manager import ResourceManager
from ._utils import SeriesLike

# ------------------------------------------------------------------
# Envuelve los métodos de clase de Ubigeo en funciones top-level
# ------------------------------------------------------------------

# @overload
# def get_departamento(
#     ubigeo: list[str] | list[int],
#     institucion: Literal["inei", "reniec", "sunat"] = "inei",
#     with_lima_metro: bool = False,
#     with_lima_region: bool = False,
#     normalize: bool = False,
# ) -> list[str]: ...

# @overload
# def get_departamento(
#     ubigeo: tuple[str, ...] | tuple[int, ...],
#     institucion: Literal["inei", "reniec", "sunat"] = "inei",
#     with_lima_metro: bool = False,
#     with_lima_region: bool = False,
#     normalize: bool = False,
# ) -> tuple[str, ...]: ...

# Contenedores soportados: pandas.Series, polars.Series, list, tuple

# TODO: Mergear con SeriesLike de _utils

def get_departamento(
    ubigeo: str | int | SeriesLike,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    with_lima_metro: bool = False,
    with_lima_region: bool = False,
    normalize: bool = False,
) -> str | SeriesLike:
    """
    Obtiene el nombre de un departamento a partir de su código de ubigeo.

    Parameters
    ----------
    ubigeo : str or int
        Código de ubigeo.
    institucion : {"inei", "reniec", "sunat"}, optional
        Institución a utilizar como fuente de datos de ubigeo (por defecto "inei").
    with_lima_metro : bool, optional
        Si se cambia a True, se diferencia Lima de Lima Metropolitana (el ubigeo debe incluir el código de provincia).
    with_lima_region : bool, optional
        Si se cambia a True, se diferencia Lima de Lima Región (el ubigeo debe incluir el código de provincia).
    normalize : bool, optional
        Si se cambia a True, retorna el nombre en mayúsculas y sin acentos (ex. JUNIN), por defecto False.

    Returns
    -------
    str
        Nombre del departamento, normalizado si normalize=True.

    Raises
    ------
    ValueError
        Si el código supera los 6 caracteres o no es str/int.
    ValueError
        Si el código no contiene el código de provincia (más de 2 caracteres) y se señala with_lima_metro o with_lima_region.
    KeyError
        Si el código no existe en la base de datos.

    Notes
    -----
    - El subcódigo para departamento se toma de los últimos 2 caracteres del código validado.
    - Para códigos de longitud impar (1, 3 o 5), se asume que falta un cero inicial y se añadirá.
    - El input puede ser int o str

    Examples
    --------
    
    Consultas rápidas individuales (sin importar el formato de entrada)

    >>> ubg.get_departamento("010101")
    "Amazonas"
    >>> ubg.get_departamento(10101)
    "Amazonas"
    >>> ubg.get_departamento(10101, normalize=True)
    "AMAZONAS"
    
    **Integración con Pandas**

    Ejemplo con un DataFrame de prueba

    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     "UBIGEO": [10101, 50101, 110101, 150101, 210101],
    ...     "P1144": [1, 1, 0, 1, 0]
    ... })
    >>> df
            UBIGEO  P1144
    0      10101     1
    1      50101     1
    2     110101     0
    3     150101     1
    4     210101	 0

    Añadimos una columna para obtener los departamentos

    >>> df["DPTO"] = ubg.get_departamento(df["UBIGEO"])
    >>> df
            UBIGEO  P1144   DPTO
    0      10101     1     Amazonas
    1      50101     1     Ayacucho
    2     110101     0     Ica
    3     150101     1     Lima
    4     210101     0     Puno

    Podemos personalizar el output con parámetros adicionales

    >>> df["DPTO"] = ubg.get_departamento(df["UBIGEO"], normalize=True)
    >>> df
            UBIGEO  P1144    DPTO
    0      10101     1     AMAZONAS
    1      50101     1     AYACUCHO
    2     110101     0     ICA
    3     150101     1     LIMA
    4     210101     0     PUNO

    La función acepta como input Series de Pandas, pero también acepta valores individuales.
    En ese sentido, los siguientes son válidos:

    >>> df["DPTO"] = df["UBIGEO"].apply(get_departamento)
    >>> df["DPTO"] = df["UBIGEO"].apply(
    ...     lambda x: get_departamento(x, normalize = True)
    ...     )
    >>> df
            UBIGEO  P1144    DPTO
    0      10101     1     AMAZONAS
    1      50101     1     AYACUCHO
    2     110101     0     ICA
    3     150101     1     LIMA
    4     210101     0     PUNO

    Sin embargo, estos métodos son más lentos y menos intuitivo, por lo que se recomienda pasar la Serie.
    """
    return Ubigeo.get_departamento(
        ubigeo, institucion, with_lima_metro, with_lima_region, normalize
    )


def get_provincia(
    ubigeo: str | int | SeriesLike,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    normalize: bool = False,
) -> str | SeriesLike:
    """
    Obtiene el nombre de una provincia a partir de su código de ubigeo.

    Parameters
    ----------
    ubigeo : str or int
        Código de ubigeo (recomendado 4 o 6 caracteres).
    institucion : {"inei", "reniec", "sunat"}, optional
        Institución a utilizar como fuente de datos de ubigeo (por defecto "inei").
    normalize : bool, optional
        Si se cambia a True, retorna el nombre en mayúsculas y sin acentos (ex. JUNIN), por defecto False.

    Returns
    -------
    str
        Nombre de la provincia, normalizado si normalize=True.

    Raises
    ------
    TypeError
        Si el código no es str/int
    ValueError
        Si el código tiene menos de 4 caracteres o supera los 6 caracteres.
    KeyError
        Si el código no existe en la base de datos.

    Notes
    -----
    - Para códigos de longitud impar (3 o 5), se asume que falta un cero inicial y se añadirá.
    - El subcódigo para provincia se toma de los últimos 4 caracteres del código validado.
    - El input puede ser str o int

    Examples
    --------
    >>> # Ejemplos básicos de obtención de provincias
    >>> ubg.get_provincia("101")
    "Chachapoyas"
    >>> ubg.get_provincia(1506)
    "Huaral"
    >>> ubg.get_provincia(101, normalize=True)
    "CHACHAPOYAS"
    >>> Para ver ejemplos de integración con pandas, visitar el docstring de get_departamento()
    """
    return Ubigeo.get_provincia(ubigeo, institucion, normalize)


def get_distrito(
    ubigeo: str | int | SeriesLike,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    normalize: bool = False,
) -> str | SeriesLike:
    """
    Obtiene el nombre de un distrito a partir de su código de ubigeo.

    Parameters
    ----------
    ubigeo : str or int
        Código de ubigeo (5 o 6 caracteres).
    institucion : {"inei", "reniec", "sunat"}, optional
        Institución a utilizar como fuente de datos de ubigeo (por defecto "inei").
    normalize : bool, optional
        Si se cambia a True, retorna el nombre en mayúsculas y sin acentos (ex. JUNIN), por defecto False.

    Returns
    -------
    str
        Nombre del distrito, normalizado si normalize=True.

    Raises
    ------
    ValueError
        Si el código no tiene 5 o 6 caracteres o no es str/int.
    KeyError
        Si el código no existe en la base de datos.

    Notes
    -----
    - El subcódigo para provincia se toma de los últimos 4 caracteres del código validado.
    - Para códigos de longitud impar (3 o 5), se asume que falta un cero inicial y se añadirá.
    - El input puede ser str o int

    Examples
    --------
    >>> # Ejemplos básicos de obtención de distritos
    >>> ubg.get_distrito("50110")
    "San Juan Bautista"
    >>> ubg.get_distrito(150110)
    "Comas"
    >>> Para ver ejemplos de integración con pandas, visitar el docstring de get_departamento()
    """
    return Ubigeo.get_distrito(ubigeo, institucion, normalize)


def get_macrorregion(
    departamento_o_ubigeo: str | int | SeriesLike,
    institucion: Literal["inei", "minsa", "ceplan"] = "inei",
    normalize: bool = False,
) -> str | SeriesLike:
    """
    Obtiene el nombre de una macrorregión a partir de su código o nombre de departamento.

    Parameters
    ----------
    departamento_o_ubigeo : str or int
        Código de ubigeo (recomendado 2 o 6 caracteres) o nombre del departamento.
    institucion : {"inei", "reniec", "sunat"}, optional
        Institución a utilizar como fuente de datos de ubigeo (por defecto "inei").
    normalize : bool, optional
        Si se cambia a True, retorna el nombre en mayúsculas y sin acentos (ex. JUNIN), por defecto False.

    Returns
    -------
    str
        Nombre de la macrorregión, normalizado si normalize=True.

    Raises
    ------
    TypeError
        Si `codigo_o_departamento` no es str o int.
    KeyError
        Si `codigo_o_departamento` no existe en la base de datos de macrorregiones.

    Notes
    -----
    - Si se proporciona un nombre de departamento, este será convertido a minúsculas, normalizado y usado para la búsqueda.
    - Se recomienda usar strings de 2 o 6 caracteres para códigos de ubigeo.
    """
    return Ubigeo.get_macrorregion(departamento_o_ubigeo, institucion, normalize)


def get_ubigeo(
    nombre_ubicacion: str | SeriesLike,
    level: Literal["departamentos", "distritos", "provincias"] = "departamentos",
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
) -> str | SeriesLike:
    """
    Obtiene el ubigeo de cierta ubicación (departamentos, distritos o provincias) a partir de su nombre.

    Parameters
    ----------
    nombre_ubicacion : str
        Nombre de la ubicación geográfica
    level : {"departamentos", "distritos", "provincias"}, optional
        Nivel administrativo de la ubicación (por defecto "departamentos").
    institucion : {"inei", "reniec", "sunat"}, optional
        Institución a utilizar como fuente de datos de ubigeo (por defecto "inei").

    Returns
    -------
    str
        Código de ubigeo correspondiente a la ubicación.

    Raises
    ------
    TypeError
        Si `level` o `institucion` no es un str.
    ValueError
        Si `level` o `institucion` no son opciones válidas.
    KeyError
        Si el nombre no existe en la base de datos de la institución especificada.

    Notes
    -----
    - La búsqueda es **case-insensitive** y se normalizan automáticamente los caracteres como acentos.
    - Los códigos retornados siguen el formato estándar de 6 dígitos:
        - 2 primeros: departamento
        - 4 primeros: provincia
        - 6 primeros: distrito

    Examples
    --------
    >>> # Obtener ubigeo de un departamento
    >>> get_ubigeo("loreto", level="departamentos")
    '16'

    >>> # Obtener ubigeo de una provincia (requiere formato específico)
    >>> get_ubigeo("Maynas", level="provincias", institucion="reniec")
    '1601'

    >>> # Obtener ubigeo completo de un distrito
    >>> get_ubigeo("Miraflores", level="distritos")
    '150125'

    >>> # Búsqueda con nombre inexistente (genera KeyError)
    >>> get_ubigeo("Ciudad Inexistente", level="departamentos")
    Traceback (most recent call last):
        ...
    KeyError: 'Nombre no encontrado: "ciudad inexistente"'
    """
    return Ubigeo.get_ubigeo(nombre_ubicacion, level, institucion)


def validate_departamento(
    nombre_departamento: str | SeriesLike,
    normalize: bool = False,
    on_error: Literal["raise", "ignore", "capitalize"] = "raise",
) -> str | SeriesLike:
    """
    Valida el nombre de un departamento escrito con gramática variable y devuelve el nombre oficial.

    Parameters
    ----------
    nombre_departamento : str
        Nombre del departamento que se busca validar y normalizar
    normalize : bool, optional
        Si se cambia a True, retorna el nombre en mayúsculas y sin acentos (ex. JUNIN), por defecto False.
    on_error : {"raise", "ignore", "capitalize"}, opcional
        Para manejar casos en que el nombre no coincide con ningún departamento válido, útil para evaluar datos mixtos (no solo departamentos)
        - `raise`: Lanza una excepción (valor por defecto).
        - `ignore`: Omite el nombre sin generar error.
        - `capitalize`: Devuelve el nombre capitalizado (primera letra en mayúscula).

    Returns
    -------
    str
        Nombre oficial del departamento.

    Raises
    ------
    TypeError
        Si `nombre_departamento` no es un str
    KeyError
        Si `nombre_departamento` no coincide con ningún nombre en la base de datos y on_error = `raise`

    Notes
    --------
    - La búsqueda es **case-insensitive** y se normalizan automáticamente los caracteres como acentos.

    Examples
    --------

    Validaciones rápidas individuales (sin importar el formato de entrada)

    >>> validate_departamento(`HUÁNUCO")
    'Huánuco'
    >>>

    >>> validate_departamento("HUÁNUCO", normalize=True)
    'HUANUCO'
    >>>

    **Integración con Pandas** 
    
    Creamos un DataFrame de prueba

    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     "DEPARTAMENTO": [AMAZONAS, ÁNCASH, APURÍMAC, CUSCO, HUÁNUCO],
    ...     "P1144": [1, 1, 0, 1, 0]
    ... })
    >>> df
        DEPARTAMENTO  P1144
    0     AMAZONAS      1
    1       ANCASH      1
    2     APURÍMAC      0
    3        CUSCO      1
    4      HUANUCO      0

    Sobreescribimos la columna con los nombres oficiales debidamente validados

    >>> df["DEPARTAMENTO"] = ubg.validate_departamento(df["DEPARTAMENTO"])
    >>> df
        DEPARTAMENTO  P1144
    0     Amazonas      1
    1       Áncash      1
    2     Apurímac      0
    3        Cusco      1
    4      Huánuco      0

    Agregar argumentos

    >>> df["DEPARTAMENTO"] = ubg.validate_departamento(df["DEPARTAMENTO"], normalize=True)
    >>> df
        DEPARTAMENTO  P1144
    0     AMAZONAS      1
    1       ANCASH      1
    2     APURIMAC      0
    3        CUSCO      1
    4      HUANUCO      0
    """
    return Departamento.validate_departamento(nombre_departamento, normalize, on_error)


def validate_ubicacion(
    nombre_ubicacion: str | SeriesLike,
    normalize: bool = False,
    on_error: Literal["raise", "ignore", "capitalize"] = "raise",
) -> str | SeriesLike:
    """
    Valida el nombre de una ubicación (departamento, provincia o distrito) escrita con gramática variable y devuelve el nombre oficial.

    Parameters
    ----------
    nombre_ubicacion : str
        Nombre de la ubicación que se busca validar y normalizar.
    normalize : bool, optional
        Si se cambia a True, retorna el nombre en mayúsculas y sin acentos (ex. JUNIN), por defecto False.
    on_error : {"raise", "ignore", "capitalize"}, opcional
        Para manejar casos en que el nombre no coincide con ningún departamento, provincia o distrito; útil para evaluar datos mixtos.
        - `raise`: Lanza una excepción (valor por defecto).
        - `ignore`: Omite el nombre sin generar error.
        - `capitalize`: Devuelve el nombre capitalizado (primera letra en mayúscula).

    Returns
    -------
    str
        Nombre oficial del ubicación.

    Raises
    ------
    TypeError
        Si `nombre_ubicacion` no es un str
    KeyError
        Si `nombre_ubicacion` no coincide con ningún nombre en la base de datos y on_error = `raise`

    Notes
    --------
    - La búsqueda es **case-insensitive** y se normalizan automáticamente los caracteres como acentos.

    Examples
    --------
    >>> # Validación simple de nombres
    >>> validate_ubicacion("HUANUCO")
    'Huánuco'
    >>>

    >>> validate_ubicacion("HUÁNUCO", normalize = True)
    'HUANUCO'
    >>>

    >>> validate_ubicacion("NACIONAL", on_error = "capitalize")
    'Nacional'
    >>>

    >>> # Integración con Pandas: ejemplo básico con DataFrame
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    >>>     "Provincia": ["HUAROCHIRÍ", "HUARAZ", "LA MAR", "MARAÑÓN", "URUBAMBA"]
    >>>     "Distrito": ["ANTIOQUÍA", "HUARAZ", "TAMBO", "CHOLÓN", "CHINCHERO"]
    >>> })
    >>> df
        Provincia    Distrito
    0 HUAROCHIRÍ   ANTIOQUÍA
    1     HUARAZ      HUARAZ
    2     LA MAR       TAMBO
    3    MARAÑÓN      CHOLÓN
    4   URUBAMBA   CHINCHERO
    >>> df["Provincia"] = df["Provincia"].apply(ubg.validate_ubicacion)
    >>> df["Distrito"] = df["Distrito"].apply(ubg.validate_ubicacion)
    >>> df
            Provincia    Distrito
    0   Huarochirí   Antioquia
    1       Huaraz      Huaraz
    2       La Mar       Tambo
    3      Marañón      Cholón
    4     Urubamba   Chinchero
    >>> # Agregar argumentos adicionales
    >>> df["Provincia"] = df["Provincia"].apply(lambda x: ubg.validate_ubicacion(x, normalize=True))
    >>> df["Distrito"] = df["Distrito"].apply(lambda x: ubg.validate_ubicacion(x, normalize=True))
    >>> df
        Provincia    Distrito
    0 HUAROCHIRI   ANTIOQUIA
    1     HUARAZ      HUARAZ
    2     LA MAR       TAMBO
    3    MARANON      CHOLON
    4   URUBAMBA   CHINCHERO
    """
    return Departamento.validate_ubicacion(nombre_ubicacion, normalize, on_error)


def get_metadato(
    codigo_o_ubicacion: str | int | SeriesLike,
    level: Literal["departamentos", "provincias", "distritos"],
    key: Literal["altitud", "capital", "latitud", "longitud", "superficie"] = "capital",
) -> str | SeriesLike:
    """
    Consultar otros datos (como capital o superficie) de la ubicación a partir de su código de ubigeo o nombre.

    Parameters
    ----------
    codigo_o_ubicacion : str or int
        Código de ubigeo o nombre de la ubicación.
    level : {"departamentos", "distritos", "provincias"}, optional
        Nivel administrativo de la ubicación (por defecto "departamentos").
    key : {"altitud", "capital", "latitud", "longitud", "superficie"}, optional
        Metadato que se desea obtener (por defecto "capital").

    Returns
    -------
    str
        Metadato en formato string

    Raises
    ------
    TypeError
        Si `codigo_o_ubicacion` no es str o int.
    KeyError
        Si el código o el nombre del departamento no existe en la base de datos respectiva.

    Notes
    -----
    - Si se proporciona un nombre de departamento, este será convertido a minúsculas, normalizado y usado para la búsqueda.
    - Se recomienda usar strings de 2 o 6 caracteres para códigos de ubigeo.
    """
    return Ubigeo.get_metadato(codigo_o_ubicacion, level, key)

def cargar_diccionario(
    resource_name: Literal[
        "departamentos",
        "provincias",
        "distritos",
        "macrorregiones",
        "equivalencias",
        "otros",
        "inverted",
    ],
    ) -> dict[str, Any]:
    return ResourceManager.cargar_diccionario(resource_name)

# ------------------------------------------------------------------
# Lo que se exporta al hacer `from ubigeos_peru.core import *`
# ------------------------------------------------------------------
__all__ = [
    "get_departamento",
    "get_provincia",
    "get_distrito",
    "get_macrorregion",
    "get_ubigeo",
    "get_metadato",
    "validate_departamento",
    "validate_ubicacion",
    "cargar_diccionario"
]
