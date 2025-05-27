from collections import defaultdict
import os
from typing import Literal
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
    'otros': "otros.json",
    'inverted': "inverted.json",
}

def eliminar_acentos(texto: str) -> str:
    texto_normalizado = unicodedata.normalize("NFKD", texto)
    texto_sin_acentos = "".join(
        c for c in texto_normalizado if not unicodedata.combining(c)
    )
    return texto_sin_acentos


# TODO: También colocar métodos para exportar las bases de datos
class Ubigeo:
    _instance = None
    _resources_loaded = {
        'departamentos': False,
        'provincias': False,
        'distritos': False,
        'macrorregiones': False,
        'equivalencias': False,
        'otros': False,
        'inverted': False
    }
    
    _DEPARTAMENTOS = None
    _PROVINCIAS = None
    _DISTRITOS = None
    _MACRORREGIONES = None
    _EQUIVALENCIAS = None
    _OTROS = None
    _INVERTED = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Ubigeo, cls).__new__(cls)
        return cls._instance

    @classmethod
    def _load_resource(cls, resource_name: str) -> None:
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
            elif len(codigo) == 3:
                codigo = codigo.zfill(4)
            elif len(codigo) == 5:
                codigo = codigo.zfill(6)
            elif len(codigo) > 6:
                raise ValueError("No se aceptan ubigeos con más de 6 caracteres")
        else:
            raise TypeError("No se aceptan valores que no sean str o int")

        return codigo

    @classmethod
    def _validate_level(cls, level: str) -> str:
        if not isinstance(level, str):
            raise TypeError('Solo se aceptan "departamentos", "distritos", "provincias" como argumentos para el nivel (level)')
        
        if isinstance(level, str) and not level.endswith("s"):
            level += "s"
        
        if level not in ["departamentos", "distritos", "provincias"]:
            raise ValueError('Solo se aceptan "departamentos", "distritos", "provincias" como argumentos para el nivel (level)')
        
        return level

    @classmethod
    def get_departamento(
        cls,
        ubigeo: str | int,
        institucion: Literal["inei", "reniec", "sunat"] = "inei",
        normalize: bool = False,
    ) -> str:
        """
        Obtiene el nombre de un departamento a partir de su código de ubigeo.

        Parameters
        ----------
        ubigeo : str or int
            Código de ubigeo.
        institucion : {"inei", "reniec", "sunat"}, optional
            Institución a utilizar como fuente de datos de ubigeo (por defecto "inei").
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
        KeyError
            Si el código no existe en la base de datos.

        Notes
        -----
        - El subcódigo para departamento se toma de los últimos 2 caracteres del código validado.
        - Para códigos de longitud impar (1, 3 o 5), se asume que falta un cero inicial y se añadirá.
        - El input puede ser int o str

        Examples
        --------
        >>> # Estandarización básica de nombres
        >>> ubg.get_departamento("010101") 
        "Amazonas"
        >>> ubg.get_departamento(10101)
        "Amazonas"
        >>> ubg.get_departamento(10101, normalize=True)
        "amazonas" 
        >>>
        >>> # Integración con Pandas
        >>> # Ejemplo básico con DataFrame
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
        >>> df["DEPT"] = df["UBIGEO"].apply(ubg.get_departamento)
        >>> df
              UBIGEO  P1144    DEPT
        0      10101     1     Amazonas
        1      50101     1     Ayacucho
        2     110101     0     Ica
        3     150101     1     Lima
        4     210101	 0     Puno
        >>> # Ejemplo con normalize (formato por defecto en la ENAHO)
        >>> df["DEPT"] = df["UBIGEO"].apply(lambda x: get_departamento(x, normalize = True))
        >>> df
              UBIGEO  P1144    DEPT
        0      10101     1     AMAZONAS
        1      50101     1     AYACUCHO
        2     110101     0     ICA
        3     150101     1     LIMA
        4     210101	 0     PUNO
        """
        cls._load_resource_if_needed('departamentos')
        ubigeo = cls._validate_codigo(ubigeo)
        try:
            result = cls._DEPARTAMENTOS[institucion][ubigeo[:2]]
        except KeyError:
            raise KeyError(
                f"El código de ubigeo {ubigeo} no se encontró en la base de datos"
            )

        if normalize:
            return eliminar_acentos(result).upper()
        else:
            return result

    @classmethod
    def get_provincia(
        cls,
        ubigeo: str | int,
        institucion: Literal["inei", "reniec", "sunat"] = "inei",
        normalize: bool = False,
    ) -> str:
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
        cls._load_resource_if_needed('provincias')
        ubigeo = cls._validate_codigo(ubigeo)
        
        if len(ubigeo) < 4:
            raise ValueError(
                "No se aceptan ubigeos con menos de 3 o 4 caracteres para provincias"
            )

        result = cls._PROVINCIAS[institucion][ubigeo[:4]]

        if normalize:
            return eliminar_acentos(result).upper()
        else:
            return result

    @classmethod
    def get_distrito(
        cls,
        ubigeo: str | int,
        institucion: Literal["inei", "reniec", "sunat"] = "inei",
        normalize: bool = False,
    ) -> str:
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
        cls._load_resource_if_needed('distritos')
        ubigeo = cls._validate_codigo(ubigeo)
        
        if len(ubigeo) not in (5, 6):
            raise ValueError(
                "No se aceptan ubigeos que no tengan 5 o 6 caracteres para distritos"
            )

        result = cls._DISTRITOS[institucion][ubigeo]

        if normalize:
            return eliminar_acentos(result).upper()
        else:
            return result


    @classmethod
    def get_macrorregion(
        cls,
        departamento_o_ubigeo: str | int,
        institucion: Literal["inei", "minsa", "ceplan"] = "inei",
        normalize: bool = False,
    )-> str:
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
        cls._load_resource_if_needed("macrorregiones")
        
        if isinstance(departamento_o_ubigeo, str):
            if not departamento_o_ubigeo[0].isdigit():
                # Se asume que es el input es un string con el nombre del departamento
                departamento = cls.validate_departamento(departamento_o_ubigeo, normalize=False)
            else:
            # Se asume que es el input es un string con el código de ubigeo
                departamento = cls.get_departamento(departamento_o_ubigeo, normalize=False)
            
        elif isinstance(departamento_o_ubigeo, int):
            # Se asume que es el input es el código en formato string
            departamento = cls.get_departamento(departamento_o_ubigeo, normalize=False)
        else:
            raise TypeError("Solo se acepta el nombre del departamento o su código de ubigeo")

        resultado = cls._MACRORREGIONES[institucion][departamento]
        if not normalize:
            return resultado
        else:
            return eliminar_acentos(resultado).upper()

    # @classmethod
    # def get_macrorregion_map(
    #     cls,
    #     institucion: Literal["inei", "minsa", "ceplan"] = "inei",
    # )-> dict:
    #     """Devuelve un diccionario con las macrorregiones como keys y los nombres de los departamentos como valores"""
    #     cls._load_resource_if_needed("macrorregiones")
        
    #     diccionario = cls._MACRORREGIONES[institucion]
    #     resultado = defaultdict(list)
    #     for dep, macrorregion in diccionario.items():
    #         resultado[macrorregion].append(dep)
        
    #     return list(resultado)

    @classmethod
    def get_ubigeo(
        cls,
        nombre_ubicacion: str,
        level: Literal["departamentos", "distritos", "provincias"] = "departamentos",
        institucion: Literal["inei", "reniec", "sunat"] = "inei",
    )-> str:
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
            - 4 siguientes: provincia
            - 2 últimos: distrito

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
        cls._load_resource_if_needed("inverted")
        
        level = cls._validate_level(level)
        
        if not isinstance(nombre_ubicacion, str):
            try:
                nombre_ubicacion = str(nombre_ubicacion)
            except TypeError:
                raise TypeError("El lugar debe ser un str, no se aceptan números u otros tipos de datos")
        if isinstance(nombre_ubicacion, str):
            ubicacion_normalized = eliminar_acentos(nombre_ubicacion).upper().strip()
            try:
                lugar_clean = cls.validate_ubicacion(ubicacion_normalized)
                result = eliminar_acentos(cls._INVERTED[level][institucion][lugar_clean]) 
            except KeyError:
                raise KeyError(f"El lugar '{nombre_ubicacion}' no se encontró en la base de datos de '{level}'")
            else:
                return result

        departamento = eliminar_acentos(departamento).lower().strip()

        return eliminar_acentos(cls._MACRORREGIONES[institucion][departamento])

    
    @classmethod
    def validate_departamento(cls, nombre_departamento: str, normalize: bool = False, ignore_errors: bool = False) -> str:
        """
        Valida el nombre de un departamento escrito con gramática variable y devuelve el nombre oficial.

        Parameters
        ----------
        nombre_departamento : str
            Nombre del departamento que se busca validar y normalizar
        normalize : bool, optional
            Si se cambia a True, retorna el nombre en mayúsculas y sin acentos (ex. JUNIN), por defecto False.
        ignore_errors : bool, optional
            Si es True, ignora los nombres que no coinciden con nombres de departamentos sin generar error, 
            útil si se aplica para conjuntos de datos que no solo contienen departamentos, por defecto `False`.

        Returns
        -------
        str
            Nombre oficial del departamento.

        Raises
        ------
        TypeError
            Si `nombre_departamento` no es un str
        KeyError
            Si `nombre_departamento` no coincide con ningún nombre en la base de datos e ignore_errors = `False`
            
        Notes
        --------
        - La búsqueda es **case-insensitive** y se normalizan automáticamente los caracteres como acentos.

        Examples
        --------
        >>> # Validación simple de nombres
        >>> validate_departamento("HUÁNUCO")
        'Huánuco'
        >>>

        >>> validate_departamento("HUÁNUCO", normalize = True)
        'HUANUCO'
        >>>

        >>> validate_departamento("HUÁNUCO", normalize = True).lower()
        'huanuco'
        >>>
        
        >>> # Integración con Pandas: ejemplo básico con DataFrame
        >>> import pandas as pd
        >>> df = pd.DataFrame({
        ...     "DEPARTAMENTO": [AMAZONAS, ÁNCASH, APURÍMAC, CUSCO, HUÁNUCO],
        ...     "P1144": [1, 1, 0, 1, 0]
        ... })
        >>> df
            DEPARTAMENTO  P1144
        0     AMAZONAS      1
        1       ÁNCASH      1
        2     APURÍMAC      0
        3        CUSCO      1
        4      HUÁNUCO      0
        >>> df["DEPARTAMENTO"] = df["DEPARTAMENTO"].apply(ubg.validate_departamento)
        >>> df
            DEPARTAMENTO  P1144
        0     Amazonas      1
        1       Áncash      1
        2     Apurímac      0
        3        Cusco      1
        4      Huánuco      0
        >>> # Agregar argumentos
        >>> df["DEPARTAMENTO"] = df["DEPARTAMENTO"].apply(lambda x: ubg.validate_departamento(x, normalize = True))
        >>> df
            DEPARTAMENTO  P1144
        0     AMAZONAS      1
        1       ANCASH      1
        2     APURIMAC      0
        3        CUSCO      1
        4      HUANUCO      0
        """
        cls._load_resource_if_needed('equivalencias')
        
        # if cls._EQUIVALENCIAS is None:
        #     raise RuntimeError("No se pudieron cargar las equivalencias")
        if not isinstance(nombre_departamento, str):
            try:
                str(nombre_departamento)
            except TypeError:
                raise TypeError(f"No se permiten otros tipos de datos que no sean str, se insertó {type(nombre_departamento)}")

        departamento = eliminar_acentos(nombre_departamento).strip().upper()
        try:
            resultado = cls._EQUIVALENCIAS["departamentos"][departamento]
        except KeyError:
            if ignore_errors:
               resultado = nombre_departamento
            else: 
                raise KeyError(
                    f"No se ha encontrado el departamento {nombre_departamento}"
                )
        
        if not normalize:
            return resultado
        else:
            return eliminar_acentos(resultado).strip().upper()

    @classmethod
    def validate_ubicacion(
        cls, 
        nombre_ubicacion: str,
        normalize: bool = False,
        ignore_errors: bool = False
    ) -> str:
        """
        Valida el nombre de una ubicación (departamento, provincia o distrito) escrita con gramática variable y devuelve el nombre oficial.

        Parameters
        ----------
        nombre_ubicacion : str
            Nombre de la ubicación que se busca validar y normalizar
        normalize : bool, optional
            Si se cambia a True, retorna el nombre en mayúsculas y sin acentos (ex. JUNIN), por defecto False.
        ignore_errors : bool, optional
            Si es True, ignora los nombres que no coinciden con nombres de departamentos sin generar error, 
            útil si se aplica para conjuntos de datos que no solo contienen departamentos, por defecto `False`.

        Returns
        -------
        str
            Nombre oficial del ubicación.

        Raises
        ------
        TypeError
            Si `nombre_ubicacion` no es un str
        KeyError
            Si `nombre_ubicacion` no coincide con ningún nombre en la base de datos e ignore_errors = `False`
     
        Notes
        --------
        - La búsqueda es **case-insensitive** y se normalizan automáticamente los caracteres como acentos.

        Examples
        --------
        >>> # Validación simple de nombres
        >>> validate_ubicacion("HUÁNUCO")
        'Huánuco'
        >>>

        >>> validate_ubicacion("HUÁNUCO", normalize = True)
        'HUANUCO'
        >>>

        >>> validate_ubicacion("HUÁNUCO", normalize = True).lower()
        'huanuco'
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
        >>> # Agregar argumentos de normalización
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
        cls._load_resource_if_needed("equivalencias")
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
                        raise KeyError(
                            f"No se encontró el lugar {nombre_ubicacion} en la base de datos de departamentos, provincias o distritos"
                        )
                    else:
                        resultado = nombre_ubicacion

        if not normalize:
            return resultado
        else:
            return eliminar_acentos(resultado).upper()

    @classmethod
    def get_metadato(
        cls, 
        codigo_o_ubicacion: str | int,
        level: Literal["departamentos", "provincias", "distritos"],
        key: Literal["altitud", "capital", "latitud", "longitud", "superficie"] = "capital"
    )-> str:
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
        cls._load_resource_if_needed("otros")
        level = cls._validate_level(level)
        
        if not isinstance(key, str):
            raise TypeError('Solo se aceptan "altitud", "capital", "latitud", "longitud", "superficie" como valores para solicitar')
        
        if key not in ["altitud", "capital", "latitud", "longitud", "superficie"]:
            raise ValueError('Solo se aceptan "altitud", "capital", "latitud", "longitud", "superficie" como valores para solicitar')
        
        if isinstance(codigo_o_ubicacion, str):
            if not codigo_o_ubicacion[0].isdigit():
                # Se asume que es el input es un string con el nombre del departamento
                ubicacion = cls.validate_ubicacion(codigo_o_ubicacion, normalize=False)
            else:
            # Se asume que es el input es un string con el código de ubigeo
                ubicacion = cls.get_ubigeo(codigo_o_ubicacion, level)
        elif isinstance(codigo_o_ubicacion, int):
            # Se asume que es el input es el código en formato string
            ubicacion = cls.get_ubigeo(codigo_o_ubicacion, level)
        else:
            raise TypeError("Solo se acepta el nombre de la ubicacion o su código de ubigeo")

        ubicacion = eliminar_acentos(ubicacion).upper()
        return cls._OTROS[level][ubicacion][key]
        