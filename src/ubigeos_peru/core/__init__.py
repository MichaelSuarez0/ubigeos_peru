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

from typing import Any, Literal

from ._utils import SeriesLike
from .departamento import Departamento
from .resource_manager import ResourceManager
from .ubigeo import Ubigeo

# ------------------------------------------------------------------
# Envuelve los métodos de clase de Ubigeo en funciones top-level
# ------------------------------------------------------------------

# TODO: Mergear con SeriesLike de _utils


def get_departamento(
    ubigeo: str | int | SeriesLike,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    divide_lima: bool = False,
    normalize: bool = False,
) -> str | SeriesLike:
    """
     Obtiene el nombre de un departamento a partir de su código de ubigeo.

     Parameters
     ----------
     ubigeo : str, int, SeriesLike
         Código de ubigeo o columna de un DataFrame con códigos de ubigeo.
     institucion : {"inei", "reniec", "sunat"}, default "inei"
         Institución a utilizar como fuente de datos de ubigeo.
     divide_lima : bool, default False
         Si es True, se diferencia Lima Región y Lima Metropolitana (el ubigeo debe incluir el código de provincia, mínimo 3 caracteres).
     normalize : bool, default False
         Si es True, retorna el nombre en mayúsculas y sin acentos (ex. JUNIN).

     Returns
     -------
     str | SeriesLike
         Nombre del departamento o columna de un DataFrame con nombres de departamentos, normalizados si normalize=True.

     Raises
     ------
     TypeError
         Si el código no es str/int/SeriesLike
     ValueError
         Si el código no contiene el código de provincia (más de 2 caracteres) y se señala with_lima_metro o with_lima_region.
     KeyError
         Si el código no existe en la base de datos.

     Notes
     -----
     - El subcódigo para departamento se toma de los primeros 2 caracteres del código validado.
     - Para códigos de longitud impar (1, 3 o 5), se asume que falta un cero inicial y se añadirá.
     - El input puede ser int o str, o una columna de un DataFrame. Se recomienda este último para mayor eficiencia y legibilidad.

     Examples
     --------

     Consultas rápidas individuales (sin importar el formato de entrada)

     >>> import ubigeos_peru as ubg
     >>> ubg.get_departamento("010101")
     "Amazonas"
     >>> ubg.get_departamento(10101)
     "Amazonas"
     >>> ubg.get_departamento(22)
     "San Martín"
     >>> ubg.get_departamento("22", normalize=True)
     "SAN MARTIN"

     **Integración con Pandas: insertar una columna (Serie) de departamentos**

    Ejemplo con un DataFrame de prueba

    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     "UBIGEO": [10101, 50101, 150101, 170101, 220101],
    ...     "P1144": [1, 1, 0, 1, 0]
    ... })
    >>> df
       UBIGEO  P1144
    0   10101      1
    1   50101      1
    2  150101      0
    3  170101      1
    4  220101      0

    Simplemente pasamos una columna (Serie) como argumento. 
    Lo guardamos en una columna de nuestro DataFramepara obtener los departamentos

    >>> df["DPTO"] = ubg.get_departamento(df["UBIGEO"])
    >>> df
       UBIGEO  P1144           DPTO
    0   10101      1       Amazonas
    1   50101      1       Ayacucho
    2  150101      0           Lima
    3  170101      1  Madre de Dios
    4  220101      0     San Martín

     Podemos personalizar el output con parámetros adicionales

     >>> df["DPTO"] = ubg.get_departamento(df["UBIGEO"], normalize=True)
     >>> df
       UBIGEO  P1144           DPTO
    0   10101      1       AMAZONAS
    1   50101      1       AYACUCHO
    2  150101      0           LIMA
    3  170101      1  MADRE DE DIOS
    4  220101      0     SAN MARTIN
    
     La función acepta como input Series de Pandas, pero también acepta valores individuales.
     En ese sentido, los siguientes son válidos, pero no recomendados, ya que son más lentos 
     y menos intuitivos que pasar la Serie.

     >>> df["DPTO"] = df["UBIGEO"].apply(get_departamento)
     >>> df["DPTO"] = df["UBIGEO"].apply(
     ...     lambda x: get_departamento(x, normalize = True)
     ...     )
     >>> df
       UBIGEO  P1144           DPTO
    0   10101      1       AMAZONAS
    1   50101      1       AYACUCHO
    2  150101      0           LIMA
    3  170101      1  MADRE DE DIOS
    4  220101      0     SAN MARTIN
    
    """
    return Ubigeo.get_departamento(ubigeo, institucion, divide_lima, normalize)


def get_provincia(
    ubigeo: str | int | SeriesLike,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    on_error: Literal["raise", "warn", "coerce", "ignore", "capitalize"] = "raise",
    normalize: bool = False,
) -> str | SeriesLike:
    """
    Obtiene el nombre de una provincia a partir de su código de ubigeo.

    Parameters
    ----------
    ubigeo : str, int, SeriesLike
        Código de ubigeo o columna de un DataFrame con códigos de ubigeo (entre 3 y 6 caracteres).
    institucion : {"inei", "reniec", "sunat"}, default "inei"
        Institución a utilizar como fuente de datos de ubigeo.
    normalize : bool, optional
        Si se cambia a True, retorna el nombre en mayúsculas y sin acentos (ex. JUNIN), por defecto False.

    Returns
    -------
    str | SeriesLike
        Nombre de la provincia o columna de un DataFrame con nombres de provincias, normalizados si normalize=True.

    Raises
    ------
    TypeError
        Si el código no es str/int/SeriesLike
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
    
    **Integración con Pandas: insertar una columna (Serie) de provincias**
    
    Ejemplo con un DataFrame de prueba
    
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     "UBIGEO": [0805, 1508, 1703, 2101, 2109],
    ...     "P1144": [0, 1, 0, 0, 1]
    ... })
    >>> df["PROVINCIA"] = ubg.get_provincia(df["UBIGEO"])
    >>> df
       UBIGEO  P1144    PROVINCIA
    0    0805      1     Tayacaja
    1    1508      0   Huarochirí
    2    1703      0    Tahuamanu
    3    2101      1     Azángaro
    4    2109      0    San Román
    
    Podemos personalizar el output con parámetros adicionales
    
    >>> df["PROVINCIA"] = ubg.get_provincia(df["UBIGEO"], normalize=True)
       UBIGEO  P1144     PROVINCIA
    0    0805      1      TAYACAJA
    1    1508      0    HUAROCHIRI
    2    1703      0     TAHUAMANU
    3    2101      1      AZANGARO
    4    2109      0     SAN ROMAN
    
    La función acepta como input Series de Pandas, pero también acepta valores individuales.
    En ese sentido, los siguientes son válidos, pero no recomendados, ya que son más lentos
    y menos intuitivos que pasar la Serie directamente.
    
    >>> df["PROVINCIA"] = df["UBIGEO"].apply(get_provincia)
    >>> df["PROVINCIA"] = df["UBIGEO"].apply(
    ...     lambda x: get_provincia(x, normalize=True)
    ... )
    >>> print(df)
       UBIGEO  P1144     PROVINCIA
    0    0805      1      TAYACAJA
    1    1508      0    HUAROCHIRI
    2    1703      0     TAHUAMANU
    3    2101      1      AZANGARO
    4    2109      0     SAN ROMAN
    
    Accediendo a la Serie resultante directamente
    
    >>> provincias = ubg.get_provincia(df["UBIGEO"])
    >>> print(provincias)
    0     San Román
    1      Azángaro
    2     Tahuamanu
    3    Huarochirí
    4      Tayacaja
    Name: PROVINCIA, dtype: object

    """
    return Ubigeo.get_provincia(ubigeo, institucion, on_error, normalize)


def get_distrito(
    ubigeo: str | int | SeriesLike,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    on_error: Literal["raise", "warn", "coerce", "ignore", "capitalize"] = "raise",
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
    Ejemplos básicos de obtención de distritos
    
    >>> import ubigeos_peru as ubg
    >>> ubg.get_distrito("010516")
    'San Cristóbal'
    >>> ubg.get_distrito(150140)
    'Santiago de Surco'
    >>> ubg.get_distrito(200701, normalize=True)
    'PARINAS'
    
    **Integración con Pandas: insertar una columna (Serie) de distritos**
    
    Ejemplo con un DataFrame de prueba
    
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     "UBIGEO": [10516, 40118, 90111, 150140, 200701],
    ...     "P1144": [1, 0, 1, 0, 1]
    ... })
    >>> print(df)
       UBIGEO  P1144
    0   10516      1
    1   40118      0
    2   90111      1
    3  150140      0
    4  200701      1
    
    Añadimos una columna para obtener los distritos
    
    >>> df["DISTRITO"] = ubg.get_distrito(df["UBIGEO"])
    >>> print(df)
       UBIGEO  P1144             DISTRITO
    0   10516      1        San Cristóbal
    1   40118      0   San Juan de Siguas
    2   90111      1     Mariscal Cáceres
    3  150140      0    Santiago de Surco
    4  200701      1              Pariñas
    
    Podemos personalizar el output con parámetros adicionales
    
    >>> df["DISTRITO"] = ubg.get_distrito(df["UBIGEO"], normalize=True)
    >>> print(df)
       UBIGEO  P1144            DISTRITO
    0   10516      1       SAN CRISTOBAL
    1   40118      0  SAN JUAN DE SIGUAS
    2   90111      1    MARISCAL CACERES
    3  150140      0   SANTIAGO DE SURCO
    4  200701      1             PARINAS
    
    La función acepta como input Series de Pandas, pero también acepta valores individuales.
    En ese sentido, los siguientes son válidos, pero no recomendados, ya que son más lentos
    y menos intuitivos que pasar la Serie directamente.
    
    >>> df["DISTRITO"] = df["UBIGEO"].apply(get_distrito)
    >>> df["DISTRITO"] = df["UBIGEO"].apply(
    ...     lambda x: get_distrito(x, normalize=True)
    ... )
    >>> print(df)
       UBIGEO  P1144            DISTRITO
    0   10516      1       SAN CRISTOBAL
    1   40118      0  SAN JUAN DE SIGUAS
    2   90111      1    MARISCAL CACERES
    3  150140      0   SANTIAGO DE SURCO
    4  200701      1             PARINAS
    """
    return Ubigeo.get_distrito(ubigeo, institucion, on_error, normalize)


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
    ubicacion: str | SeriesLike,
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
    return Ubigeo.get_ubigeo(ubicacion, level, institucion)


def validate_departamento(
    departamento: str | SeriesLike,
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str | SeriesLike:
    """
    Valida el nombre de un departamento escrito con gramática variable y devuelve el nombre oficial.

    Parameters
    ----------
    nombre_departamento : str | SeriesLike
        Nombre o Serie de nombres de departamentos que se buscan validar y normalizar
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

    >>> validate_departamento("HUÁNUCO")
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
    return Departamento.validate_departamento(departamento, normalize, on_error)


def validate_ubicacion(
    ubicacion: str | SeriesLike,
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
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
    return Departamento.validate_ubicacion(ubicacion, normalize, on_error)


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
    "cargar_diccionario",
]

if __name__ == "__main__":
    import doctest

    doctest.testmod()
