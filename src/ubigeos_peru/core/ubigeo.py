from typing import Any, Literal, Protocol, Sequence, TypeVar, runtime_checkable
from .departamento import Departamento
from .utils import eliminar_acentos
from .resource_manager import ResourceManager

@runtime_checkable
class SeriesLike(Protocol):
    def map(self, mapper: Any) -> "SeriesLike": ...

S = TypeVar("S", bound=SeriesLike)

def _is_series_like(obj: Any) -> bool:
    # Duck typing: algo que se pueda iterar (lista, numpy array, pd.Series, etc.)
    try:
        iter(obj)
        return True
    except TypeError:
        return False

def _reconstruct_like(proto: Any, data: Sequence) -> Any:
    """
    Intenta reconstruir el mismo tipo de contenedor que 'proto' con 'data'.
    Si falla, devuelve list(data). No requiere pandas.
    """
    try:
        # Caso común: list -> list(data), tuple -> tuple(data), numpy -> np.array(data), pd.Series -> Series(data)
        return proto.__class__(data)
    except Exception:
        return list(data)

class Ubigeo:
    _instance = None
    _resources = ResourceManager()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Ubigeo, cls).__new__(cls)
        return cls._instance

    @classmethod
    def _validate_codigo(cls, codigo: str | int) -> str:
        if isinstance(codigo, int):
            codigo = str(codigo)

        if isinstance(codigo, str):
            if not codigo.isdigit():
                raise ValueError("El código debe contener solo dígitos")
            
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
        ubigeo: str | int | SeriesLike,
        institucion: Literal["inei", "reniec", "sunat"] = "inei",
        with_lima_metro: bool = False,
        with_lima_region: bool = False,
        normalize: bool = False,
    ) -> str:
        
        cls._resources._load_resource_if_needed("departamentos")
        mapping: dict[str, str] = cls._resources._loaded["departamentos"][institucion]

        # === Serie-like ===
        if _is_series_like(ubigeo) and not isinstance(ubigeo, (str, bytes)):
            mapping: dict[str, str] = (
                {k: eliminar_acentos(v).upper() for k, v in mapping.items()}
                if normalize else mapping
            )
            # Fast-path: sin reglas de Lima -> solo tomar dept key y mapear
            if not (with_lima_metro or with_lima_region):
                out = []
                append = out.append
                for u in ubigeo:
                    code = cls._validate_codigo(u)
                    dept_key = code[:2]
                    try:
                        append(mapping[dept_key])
                    except KeyError:
                        raise KeyError(f"El código de ubigeo {code} no se encontró en la base de datos")
                return _reconstruct_like(ubigeo, out)
        else:

        # def _single(u: str | int) -> str:
            code = cls._validate_codigo(ubigeo)
            try:
                dept = mapping[code[:2]]
            except KeyError:
                raise KeyError(f"El código de ubigeo {code} no se encontró en la base de datos")

            if with_lima_metro or with_lima_region:
                try:
                    prov = cls.get_provincia(code, institucion=institucion, normalize=False)
                except KeyError:
                    raise ValueError(
                        "Para diferenciar Lima de Lima Metropolitana o Lima Región, "
                        "el ubigeo debe incluir el código de la provincia"
                    )

                if with_lima_metro and dept == "Lima" and prov == "Lima":
                    dept = "Lima Metropolitana"
                elif with_lima_region and dept == "Lima" and prov != "Lima":
                    dept = "Lima Región"

            return eliminar_acentos(dept).upper() if normalize else dept
        
        # Fast-path: Series-like con .map(dict) cuando NO hay reglas de Lima
        # if isinstance(ubigeo, SeriesLike):
        #     if not (with_lima_metro or with_lima_region) and not normalize:
        #         # usar directamente el dict (más rápido)
        #         return ubigeo.map(mapping)
        #     # si hay reglas de Lima o normalize, caemos a map(callable)

        # Escalar
        #return _single(ubigeo)

    @classmethod
    def get_provincia(
        cls,
        ubigeo: str | int,
        institucion: Literal["inei", "reniec", "sunat"] = "inei",
        normalize: bool = False,
    ) -> str:
        
        ubigeo = cls._validate_codigo(ubigeo)
        cls._resources._load_resource_if_needed('provincias')
        
        if len(ubigeo) < 4:
            raise ValueError(
                "No se aceptan ubigeos con menos de 3 o 4 caracteres para provincias"
            )

        result = cls._resources._loaded["provincias"][institucion][ubigeo[:4]]

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

        ubigeo = cls._validate_codigo(ubigeo)
        cls._resources._load_resource_if_needed('distritos')
        
        if len(ubigeo) not in (5, 6):
            raise ValueError(
                "No se aceptan ubigeos que no tengan 5 o 6 caracteres para distritos"
            )

        result = cls._resources._loaded["distritos"][institucion][ubigeo]

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
        
        cls._resources._load_resource_if_needed("macrorregiones")
        
        if isinstance(departamento_o_ubigeo, str):
            if not departamento_o_ubigeo[0].isdigit():
                # Se asume que es el input es un string con el nombre del departamento
                departamento = Departamento.validate_departamento(departamento_o_ubigeo, normalize=False)
            else:
            # Se asume que es el input es un string con el código de ubigeo
                departamento = cls.get_departamento(departamento_o_ubigeo, normalize=False)
            
        elif isinstance(departamento_o_ubigeo, int):
            # Se asume que es el input es el código en formato string
            departamento = cls.get_departamento(departamento_o_ubigeo, normalize=False)
        else:
            raise TypeError("Solo se acepta el nombre del departamento o su código de ubigeo")

        resultado = cls._resources._loaded["macrorregiones"][institucion][departamento]
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
    #     cls._resources._load_resource_if_needed("macrorregiones")
        
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
        
        level = cls._validate_level(level)
        cls._resources._load_resource_if_needed("inverted")
        
        if not isinstance(nombre_ubicacion, str):
            try:
                nombre_ubicacion = str(nombre_ubicacion)
            except TypeError:
                raise TypeError("El lugar debe ser un str, no se aceptan números u otros tipos de datos")
        if isinstance(nombre_ubicacion, str):
            ubicacion_normalized = eliminar_acentos(nombre_ubicacion).upper().strip()
            try:
                lugar_clean = Departamento.validate_ubicacion(ubicacion_normalized)
                result = eliminar_acentos(cls._resources._loaded["inverted"][level][institucion][lugar_clean]) 
            except KeyError:
                raise KeyError(f"El lugar '{nombre_ubicacion}' no se encontró en la base de datos de '{level}'")
            else:
                return result

        departamento = eliminar_acentos(departamento).lower().strip()

        return eliminar_acentos(cls._resources._loaded["macrorregiones"][institucion][departamento])

    
    # @classmethod
    # def validate_departamento(
    #     cls, 
    #     nombre_departamento: str, 
    #     normalize: bool = False, 
    #     on_error: Literal["raise", "ignore", "capitalize"] = "raise"
    # ) -> str:
        
    #     # if cls._EQUIVALENCIAS is None:
    #     #     raise RuntimeError("No se pudieron cargar las equivalencias")
    #     if not isinstance(nombre_departamento, str):
    #         try:
    #             str(nombre_departamento)
    #         except TypeError:
    #             raise TypeError(f"No se permiten otros tipos de datos que no sean str, se insertó {type(nombre_departamento)}")
        
    #     cls._resources._load_resource_if_needed('equivalencias')

    #     departamento = eliminar_acentos(nombre_departamento).strip().upper()
    #     try:
    #         resultado = cls._resources._EQUIVALENCIAS["departamentos"][departamento]
    #     except KeyError:
    #         if on_error == "raise":
    #             raise KeyError(f"No se ha encontrado el departamento {nombre_departamento}")
    #         elif on_error == "ignore":
    #            resultado = nombre_departamento
    #         elif on_error == "capitalize":
    #             resultado = nombre_departamento.capitalize()
    #         else:
    #             raise ValueError('El arg "on_error" debe ser uno de los siguientes: "raise", "ignore", "capitalize"')
        
    #     if not normalize:
    #         return resultado
    #     else:
    #         return eliminar_acentos(resultado).strip().upper()

    # @classmethod
    # def validate_ubicacion(
    #     cls, 
    #     nombre_ubicacion: str,
    #     normalize: bool = False,
    #     on_error: Literal["raise", "ignore", "capitalize"] = "raise"
    # ) -> str:
    #     """
    #     Valida el nombre de una ubicación (departamento, provincia o distrito) escrita con gramática variable y devuelve el nombre oficial.

    #     Parameters
    #     ----------
    #     nombre_ubicacion : str
    #         Nombre de la ubicación que se busca validar y normalizar.
    #     normalize : bool, optional
    #         Si se cambia a True, retorna el nombre en mayúsculas y sin acentos (ex. JUNIN), por defecto False.
    #     on_error : {"raise", "ignore", "capitalize"}, optional
    #         Para manejar casos en que el nombre no coincide con ningún departamento, provincia o distrito; útil para evaluar datos mixtos.
    #         - `raise`: Lanza una excepción (valor por defecto).
    #         - `ignore`: Omite el nombre sin generar error.
    #         - `capitalize`: Devuelve el nombre capitalizado (primera letra en mayúscula).

    #     Returns
    #     -------
    #     str
    #         Nombre oficial del ubicación.

    #     Raises
    #     ------
    #     TypeError
    #         Si `nombre_ubicacion` no es un str
    #     KeyError
    #         Si `nombre_ubicacion` no coincide con ningún nombre en la base de datos y on_error = `raise`
     
    #     Notes
    #     --------
    #     - La búsqueda es **case-insensitive** y se normalizan automáticamente los caracteres como acentos.

    #     Examples
    #     --------
    #     >>> # Validación simple de nombres
    #     >>> validate_ubicacion("HUANUCO")
    #     'Huánuco'
    #     >>>

    #     >>> validate_ubicacion("HUÁNUCO", normalize = True)
    #     'HUANUCO'
    #     >>>

    #     >>> validate_ubicacion("NACIONAL", on_error = "capitalize")
    #     'Nacional'
    #     >>>
        
    #     >>> # Integración con Pandas: ejemplo básico con DataFrame
    #     >>> import pandas as pd
    #     >>> df = pd.DataFrame({
    #     >>>     "Provincia": ["HUAROCHIRÍ", "HUARAZ", "LA MAR", "MARAÑÓN", "URUBAMBA"]
    #     >>>     "Distrito": ["ANTIOQUÍA", "HUARAZ", "TAMBO", "CHOLÓN", "CHINCHERO"]
    #     >>> })
    #     >>> df
    #        Provincia    Distrito
    #     0 HUAROCHIRÍ   ANTIOQUÍA
    #     1     HUARAZ      HUARAZ
    #     2     LA MAR       TAMBO
    #     3    MARAÑÓN      CHOLÓN
    #     4   URUBAMBA   CHINCHERO
    #     >>> df["Provincia"] = df["Provincia"].apply(ubg.validate_ubicacion)
    #     >>> df["Distrito"] = df["Distrito"].apply(ubg.validate_ubicacion)
    #     >>> df
    #          Provincia    Distrito
    #     0   Huarochirí   Antioquia
    #     1       Huaraz      Huaraz
    #     2       La Mar       Tambo
    #     3      Marañón      Cholón
    #     4     Urubamba   Chinchero
    #     >>> # Agregar argumentos adicionales
    #     >>> df["Provincia"] = df["Provincia"].apply(lambda x: ubg.validate_ubicacion(x, normalize=True))
    #     >>> df["Distrito"] = df["Distrito"].apply(lambda x: ubg.validate_ubicacion(x, normalize=True))
    #     >>> df
    #        Provincia    Distrito
    #     0 HUAROCHIRI   ANTIOQUIA
    #     1     HUARAZ      HUARAZ
    #     2     LA MAR       TAMBO
    #     3    MARANON      CHOLON
    #     4   URUBAMBA   CHINCHERO
    #     """
    #     nombre_ubicacion = eliminar_acentos(nombre_ubicacion).strip().upper()
    #     cls._resources._load_resource_if_needed("equivalencias")
    #     try:
    #         resultado = cls._resources._EQUIVALENCIAS["departamentos"][nombre_ubicacion]
    #     except KeyError:
    #         try:
    #             resultado = cls._resources._EQUIVALENCIAS["provincias"][nombre_ubicacion]
    #         except KeyError:
    #             try:
    #                 resultado = cls._resources._EQUIVALENCIAS["distritos"][nombre_ubicacion]
    #             except KeyError:
    #                 if on_error == "raise":
    #                     raise KeyError(
    #                         f"No se encontró el lugar {nombre_ubicacion} en la base de datos de departamentos, provincias o distritos"
    #                     )
    #                 elif on_error == "ignore":
    #                     resultado = nombre_ubicacion
    #                 elif on_error == "capitalize":
    #                     resultado = nombre_ubicacion.capitalize()
    #                 else:
    #                     raise ValueError('El arg "on_error" debe ser uno de los siguientes: "raise", "ignore", "capitalize"')
                
    #     if not normalize:
    #         return resultado
    #     else:
    #         return eliminar_acentos(resultado).upper()

    @classmethod
    def get_metadato(
        cls, 
        codigo_o_ubicacion: str | int,
        level: Literal["departamentos", "provincias", "distritos"],
        key: Literal["altitud", "capital", "latitud", "longitud", "superficie"] = "capital"
    )-> str:
    
        level = cls._validate_level(level)
        cls._resources._load_resource_if_needed("otros")
        
        if not isinstance(key, str):
            raise TypeError('Solo se aceptan "altitud", "capital", "latitud", "longitud", "superficie" como valores para solicitar')
        
        if key not in ["altitud", "capital", "latitud", "longitud", "superficie"]:
            raise ValueError('Solo se aceptan "altitud", "capital", "latitud", "longitud", "superficie" como valores para solicitar')
        
        if isinstance(codigo_o_ubicacion, str):
            if not codigo_o_ubicacion[0].isdigit():
                # Se asume que es el input es un string con el nombre del departamento
                ubicacion = Departamento.validate_ubicacion(codigo_o_ubicacion, normalize=False)
            else:
            # Se asume que es el input es un string con el código de ubigeo
                ubicacion = cls.get_ubigeo(codigo_o_ubicacion, level)
        elif isinstance(codigo_o_ubicacion, int):
            # Se asume que es el input es el código en formato string
            ubicacion = cls.get_ubigeo(codigo_o_ubicacion, level)
        else:
            raise TypeError("Solo se acepta el nombre de la ubicacion o su código de ubigeo")

        ubicacion = eliminar_acentos(ubicacion).upper()
        return cls._resources._loaded["otros"][level][ubicacion][key]
        