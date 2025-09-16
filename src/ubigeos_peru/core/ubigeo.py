from typing import Literal
from .departamento import Departamento
from ._utils import SeriesLike, eliminar_acentos, is_series_like, reconstruct_like
from .resource_manager import ResourceManager


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
        ubigeo: str | int | SeriesLike | SeriesLike,
        institucion: Literal["inei", "reniec", "sunat"] = "inei",
        with_lima_metro: bool = False,
        with_lima_region: bool = False,
        normalize: bool = False,
    ) -> str | SeriesLike:
        
        cls._resources._load_resource_if_needed("departamentos")
        mapping: dict[str, str] = cls._resources._loaded["departamentos"][institucion]

        # ---------------------- Input: Series-like ----------------------
        if is_series_like(ubigeo) and not isinstance(ubigeo, (str, bytes)):
            mapping: dict[str, str] = (
                {k: eliminar_acentos(v).upper() for k, v in mapping.items()}
                if normalize else mapping
            )
            # Fast-path: sin reglas de Lima -> solo tomar dept key y mapear
            if not (with_lima_metro or with_lima_region):
                out = []
                for u in ubigeo:
                    code = cls._validate_codigo(u)
                    dept_key = code[:2]
                    try:
                        out.append(mapping[dept_key])
                        out.append(mapping[dept_key])
                    except KeyError:
                        raise KeyError(f"El código de ubigeo {code} no se encontró en la base de datos")
                return reconstruct_like(ubigeo, out)
        else:
        # ------------------------ Input: Singular ------------------------
            code = cls._validate_codigo(ubigeo)
            try:
                dept = mapping[code[:2]]
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
        ubigeo: str | int | SeriesLike,
        institucion: Literal["inei", "reniec", "sunat"] = "inei",
        normalize: bool = False,
    ) -> str | SeriesLike:
        
        cls._resources._load_resource_if_needed('provincias')
        mapping: dict[str, str] = cls._resources._loaded["provincias"][institucion]
        
         # ---------------------- Input: Series-like ----------------------
        if is_series_like(ubigeo) and not isinstance(ubigeo, (str, bytes)):
            mapping: dict[str, str] = (
                {k: eliminar_acentos(v).upper() for k, v in mapping.items()}
                if normalize else mapping
            )
            
            out = []
            for u in ubigeo:
                code = cls._validate_codigo(u)
                dept_key = code[:4]
                try:
                    out.append(mapping[dept_key])
                except KeyError:
                    raise KeyError(f"El código de ubigeo {code} no se encontró en la base de datos")
            return reconstruct_like(ubigeo, out)
        else:
        # ------------------------ Input: Singular ------------------------
            ubigeo = cls._validate_codigo(ubigeo)
            if len(ubigeo) < 4:
                raise ValueError(
                    "No se aceptan ubigeos con menos de 3 o 4 caracteres para provincias"
                )

            try:
                result = mapping[ubigeo[:4]]
            except KeyError:
                raise KeyError(f"El código de ubigeo {ubigeo} no se encontró en la base de datos")

            if normalize:
                return eliminar_acentos(result).upper()
            else:
                return result

    # TODO: Implementar "on_error"
    @classmethod
    def get_distrito(
        cls,
        ubigeo: str | int | SeriesLike,
        institucion: Literal["inei", "reniec", "sunat"] = "inei",
        normalize: bool = False,
    ) -> str | SeriesLike:
                
        cls._resources._load_resource_if_needed('distritos')
        mapping: dict[str, str] = cls._resources._loaded["distritos"][institucion]

        # ---------------------- Input: Series-like ----------------------
        if is_series_like(ubigeo) and not isinstance(ubigeo, (str, bytes)):
            mapping: dict[str, str] = (
                {k: eliminar_acentos(v).upper() for k, v in mapping.items()}
                if normalize else mapping
            )
            
            out = []
            for u in ubigeo:
                code = cls._validate_codigo(u)
                dept_key = code[:6]
                try:
                    out.append(mapping[dept_key])
                except KeyError:
                    raise KeyError(f"El código de ubigeo {code} no se encontró en la base de datos")
            return reconstruct_like(ubigeo, out)
        
        else:
        # ------------------------ Input: Singular ------------------------
            ubigeo = cls._validate_codigo(ubigeo)
            if len(ubigeo) not in (5, 6):
                raise ValueError(
                    "No se aceptan ubigeos que no tengan 5 o 6 caracteres para distritos"
                )

            result = cls._resources._loaded["distritos"][institucion][ubigeo]

            return eliminar_acentos(result).upper() if normalize else result


    @classmethod
    def get_macrorregion(
        cls,
        departamento_o_ubigeo: str | int | SeriesLike,
        institucion: Literal["inei", "minsa", "ceplan"] = "inei",
        normalize: bool = False,
    )-> str | SeriesLike:
        
        cls._resources._load_resource_if_needed("macrorregiones")
        mapping = cls._resources._loaded["macrorregiones"][institucion]

        # ---------------------- Input: Series-like ----------------------
        if is_series_like(departamento_o_ubigeo):
            mapping: dict[str, str] = (
                {k: eliminar_acentos(v).upper() for k, v in mapping.items()}
                if normalize else mapping
            )
            out = []
            for item in departamento_o_ubigeo:
                if isinstance(item, str):
                    if not item[0].isdigit():
                        # Se asume que es el input es un string con el nombre del departamento
                        departamento = Departamento.validate_departamento(item, normalize=False)
                    else:
                    # Se asume que es el input es un string con el código de ubigeo
                        departamento = cls.get_departamento(item, normalize=False)
                    
                elif isinstance(item, int):
                    # Se asume que es el input es el código en formato string
                    departamento = cls.get_departamento(item, normalize=False)
                else:
                    raise TypeError("Solo se acepta el nombre del departamento o su código de ubigeo")
                # if eliminar_acentos(departamento.lower()) in ("region lima", "lima metropolitana"):
                #     departamento = "Lima"
                out.append(mapping[departamento])
            return reconstruct_like(departamento_o_ubigeo, out)
        
        else:
        # ------------------------ Input: Singular ------------------------
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

        resultado = mapping[departamento]
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
        nombre_ubicacion: str | SeriesLike,
        level: Literal["departamentos", "distritos", "provincias"] = "departamentos",
        institucion: Literal["inei", "reniec", "sunat"] = "inei",
    )-> str | SeriesLike:
        
        level = cls._validate_level(level)
        cls._resources._load_resource_if_needed("inverted")
        mapping = cls._resources._loaded["inverted"][level][institucion]

        # ---------------------- Input: Series-like ----------------------
        if isinstance(nombre_ubicacion, SeriesLike):
            out = []
            for item in nombre_ubicacion:
                if not isinstance(item, str):
                    try:
                        item = str(item)
                    except TypeError:
                        raise TypeError("El lugar debe ser un str, no se aceptan números u otros tipos de datos")
                    
                ubicacion_normalized = eliminar_acentos(item).upper().strip()
                try:
                    lugar_clean = Departamento.validate_ubicacion(ubicacion_normalized)
                    out.append(mapping[lugar_clean])
                except KeyError:
                    raise KeyError(f"El lugar '{item}' no se encontró en la base de datos de '{level}'")
            return reconstruct_like(nombre_ubicacion, out)
        
        else:
        # ------------------------ Input: Singular ------------------------
            if not isinstance(nombre_ubicacion, str):
                try:
                    nombre_ubicacion = str(nombre_ubicacion)
                except TypeError:
                    raise TypeError("El lugar debe ser un str, no se aceptan números u otros tipos de datos")
        mapping = cls._resources._loaded["inverted"][level][institucion]

        # ---------------------- Input: Series-like ----------------------
        if isinstance(nombre_ubicacion, SeriesLike):
            out = []
            for item in nombre_ubicacion:
                if not isinstance(item, str):
                    try:
                        item = str(item)
                    except TypeError:
                        raise TypeError("El lugar debe ser un str, no se aceptan números u otros tipos de datos")
                    
                ubicacion_normalized = eliminar_acentos(item).upper().strip()
                try:
                    lugar_clean = Departamento.validate_ubicacion(ubicacion_normalized)
                    out.append(mapping[lugar_clean])
                except KeyError:
                    raise KeyError(f"El lugar '{item}' no se encontró en la base de datos de '{level}'")
            return reconstruct_like(nombre_ubicacion, out)
        
        else:
        # ------------------------ Input: Singular ------------------------
            if not isinstance(nombre_ubicacion, str):
                try:
                    nombre_ubicacion = str(nombre_ubicacion)
                except TypeError:
                    raise TypeError("El lugar debe ser un str, no se aceptan números u otros tipos de datos")
            ubicacion_normalized = eliminar_acentos(nombre_ubicacion).upper().strip()
            try:
                lugar_clean = Departamento.validate_ubicacion(ubicacion_normalized)
                ubicacion_limpia = eliminar_acentos(cls._resources._loaded["inverted"][level][institucion][lugar_clean]) 
            except KeyError:
                return ""
                #raise KeyError(f"El lugar '{ubicacion_normalized}' no se encontró en la base de datos de '{level}'")
            else:
                return ubicacion_limpia

   
                return ubicacion_limpia

   
    @classmethod
    def get_metadato(
        cls, 
        codigo_o_ubicacion: str | int | SeriesLike,
        level: Literal["departamentos", "provincias", "distritos"],
        key: Literal["altitud", "capital", "latitud", "longitud", "superficie"] = "capital",
    )-> str | SeriesLike:
    
        level = cls._validate_level(level)
        cls._resources._load_resource_if_needed("otros")
        mapping = cls._resources._loaded["otros"][level]

        if not isinstance(key, str):
            raise TypeError('Solo se aceptan "altitud", "capital", "latitud", "longitud", "superficie" como valores para solicitar')
        
        if key not in ["altitud", "capital", "latitud", "longitud", "superficie"]:
            raise ValueError('Solo se aceptan "altitud", "capital", "latitud", "longitud", "superficie" como valores para solicitar')

        # ---------------------- Input: Series-like ----------------------
        if isinstance(codigo_o_ubicacion, SeriesLike):
            out = []
            for item in codigo_o_ubicacion:
                if isinstance(item, str):
                    if not item[0].isdigit():
                        # Se asume que el input es un string con el nombre del departamento
                        ubicacion = Departamento.validate_ubicacion(item, normalize=False, on_error="ignore")
                    else:
                    # Se asume que el input es un string con el código de ubigeo
                        ubicacion = cls.get_ubigeo(item, level)
                elif isinstance(item, int):
                    # Se asume que el input es es un int con l código
                    if level == "departamentos":
                        ubicacion = cls.get_departamento(item)
                    elif level == "provincias":
                        ubicacion = cls.get_provincia(item)
                    elif level == "distritos":
                        ubicacion = cls.get_distrito(item)
                    #ubicacion = cls.get_ubigeo(codigo_o_ubicacion, level)
                else:
                    raise TypeError("Solo se acepta el nombre de la ubicacion o su código de ubigeo")
                            
                #ubicacion_normalized = eliminar_acentos(item).upper().strip()
                try:
                    ubicacion_normalized = eliminar_acentos(ubicacion).upper()
                    out.append(mapping[ubicacion_normalized][key])
                except KeyError:
                    out.append("")
                    #raise KeyError(f"El lugar '{ubicacion_normalized}' no se encontró en la base de datos de '{level}'")
            return reconstruct_like(codigo_o_ubicacion, out)
        
        else: 
            # ------------------------ Input: Singular ------------------------
            if isinstance(codigo_o_ubicacion, str):
                if not codigo_o_ubicacion[0].isdigit():
                    # Se asume que el input es un string con el nombre del departamento
                    ubicacion = Departamento.validate_ubicacion(codigo_o_ubicacion, normalize=False)
                else:
                # Se asume que el input es un string con el código de ubigeo
                    ubicacion = cls.get_ubigeo(codigo_o_ubicacion, level)
            elif isinstance(codigo_o_ubicacion, int):
                # Se asume que el input es un int con el código
                if level == "departamentos":
                    ubicacion = cls.get_departamento(codigo_o_ubicacion)
                elif level == "provincias":
                    ubicacion = cls.get_provincia(codigo_o_ubicacion)
                elif level == "distritos":
                    ubicacion = cls.get_distrito(codigo_o_ubicacion)
                #ubicacion = cls.get_ubigeo(codigo_o_ubicacion, level)
            else:
                raise TypeError("Solo se acepta el nombre de la ubicacion o su código de ubigeo")

        ubicacion = eliminar_acentos(ubicacion).upper()
        return mapping[ubicacion][key]
        