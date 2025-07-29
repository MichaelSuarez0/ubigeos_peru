

from typing import Literal
from .utils import eliminar_acentos
from .resource_manager import ResourceManager

class Departamento:
    _resources = ResourceManager()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Departamento, cls).__new__(cls)
        return cls._instance

    @classmethod
    def validate_departamento(
        cls, 
        nombre_departamento: str, 
        normalize: bool = False, 
        on_error: Literal["raise", "ignore", "capitalize"] = "raise"
    ) -> str:
        """
        Valida el nombre de un departamento escrito con gramática variable y devuelve el nombre oficial.

        Parameters
        ----------
        nombre_departamento : str
            Nombre del departamento que se busca validar y normalizar
        normalize : bool, optional
            Si se cambia a True, retorna el nombre en mayúsculas y sin acentos (ex. JUNIN), por defecto False.
        on_error : {"raise", "ignore", "capitalize"}, optional
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
        >>> # Validación simple de nombres
        >>> validate_departamento(`HUÁNUCO")
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
        cls._resources._load_resource_if_needed('equivalencias')
        
        # if cls._EQUIVALENCIAS is None:
        #     raise RuntimeError("No se pudieron cargar las equivalencias")
        if not isinstance(nombre_departamento, str):
            try:
                str(nombre_departamento)
            except TypeError:
                raise TypeError(f"No se permiten otros tipos de datos que no sean str, se insertó {type(nombre_departamento)}")

        departamento = eliminar_acentos(nombre_departamento).strip().upper()
        try:
            resultado = cls._resources._EQUIVALENCIAS["departamentos"][departamento]
        except KeyError:
            if on_error == "raise":
                raise KeyError(f"No se ha encontrado el departamento {nombre_departamento}")
            elif on_error == "ignore":
               resultado = nombre_departamento
            elif on_error == "capitalize":
                resultado = nombre_departamento.capitalize()
            else:
                raise ValueError('El arg "on_error" debe ser uno de los siguientes: "raise", "ignore", "capitalize"')
        
        if not normalize:
            return resultado
        else:
            return eliminar_acentos(resultado).strip().upper()

    @classmethod
    def validate_ubicacion(
        cls, 
        nombre_ubicacion: str,
        normalize: bool = False,
        on_error: Literal["raise", "ignore", "capitalize"] = "raise"
    ) -> str:
        """
        Valida el nombre de una ubicación (departamento, provincia o distrito) escrita con gramática variable y devuelve el nombre oficial.

        Parameters
        ----------
        nombre_ubicacion : str
            Nombre de la ubicación que se busca validar y normalizar
        normalize : bool, optional
            Si se cambia a True, retorna el nombre en mayúsculas y sin acentos (ex. JUNIN), por defecto False.
         on_error : {"raise", "ignore", "capitalize"}, optional
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
        cls._resources._load_resource_if_needed("equivalencias")
        nombre_ubicacion = eliminar_acentos(nombre_ubicacion).strip().upper()
        try:
            resultado = cls._resources._EQUIVALENCIAS["departamentos"][nombre_ubicacion]
        except KeyError:
            try:
                resultado = cls._resources._EQUIVALENCIAS["provincias"][nombre_ubicacion]
            except KeyError:
                try:
                    resultado = cls._resources._EQUIVALENCIAS["distritos"][nombre_ubicacion]
                except KeyError:
                    if on_error == "raise":
                        raise KeyError(
                            f"No se encontró el lugar {nombre_ubicacion} en la base de datos de departamentos, provincias o distritos"
                        )
                    elif on_error == "ignore":
                        resultado = nombre_ubicacion
                    elif on_error == "capitalize":
                        resultado = nombre_ubicacion.capitalize()
                    else:
                        raise ValueError('El arg "on_error" debe ser uno de los siguientes: "raise", "ignore", "capitalize"')
                
        if not normalize:
            return resultado
        else:
            return eliminar_acentos(resultado).upper()
