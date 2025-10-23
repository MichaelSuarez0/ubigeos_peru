from typing import Literal

from ._utils import (
    SeriesLike,
    eliminar_acentos,
    is_series_like,
    reconstruct_like,
    assert_error,
)
from .departamento import Departamento
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
        if not isinstance(codigo, (str, int)):
            raise TypeError("No se aceptan valores que no sean str o int")

        codigo = str(codigo)
        length = len(codigo)

        if not codigo.isdigit():
            raise ValueError("El código debe contener solo dígitos")

        if length > 6:
            raise ValueError("No se aceptan ubigeos con más de 6 caracteres")

        if length in (1, 3, 5):
            codigo = codigo.zfill(length + 1)

        return codigo

    @classmethod
    def _validate_level(cls, level: str) -> str:
        if not isinstance(level, str):
            raise TypeError(
                'Solo se aceptan "departamentos", "distritos", "provincias" como argumentos para el nivel (level)'
            )

        if isinstance(level, str) and not level.endswith("s"):
            level += "s"

        if level not in ["departamentos", "distritos", "provincias"]:
            raise ValueError(
                'Solo se aceptan "departamentos", "distritos", "provincias" como argumentos para el nivel (level)'
            )

        return level

    @classmethod
    def get_departamento(
        cls,
        ubigeo: str | int | SeriesLike,
        institucion: Literal["inei", "reniec", "sunat"] = "inei",
        divide_lima: bool = False,
        normalize: bool = False,
    ) -> str | SeriesLike:
        cls._resources.cargar_diccionario("departamentos")

        if divide_lima:
            cls._resources.cargar_diccionario("provincias")

        # ---------------------- Input: Series-like ----------------------
        if is_series_like(ubigeo):
            # Ya no hay necesidad de normalizar el departamento dentro del for loop
            mapping: dict[str, str] = (
                {
                    k: eliminar_acentos(v).upper()
                    for k, v in cls._resources._loaded["departamentos"][
                        institucion
                    ].items()
                }
                if normalize
                else cls._resources._loaded["departamentos"][institucion]
            )

            series = []
            for u in ubigeo:
                code = cls._validate_codigo(u)
                dept_key = code[:2]
                try:
                    dept = mapping[dept_key]
                except KeyError:
                    raise KeyError(
                        f"El código de ubigeo {code} no se encontró en la base de datos"
                    )

                if divide_lima and dept == "Lima":
                    if len(code) < 4:
                        raise ValueError(
                            "Para distinguir Lima Metropolitana y Lima Región, el ubigeo debe tener al menos 3 dígitos"
                        )
                    prov = cls._resources._loaded["provincias"][institucion][code[:4]]
                    dept = "Lima Metropolitana" if prov == "Lima" else "Lima Región"
                    dept = dept if not normalize else eliminar_acentos(dept).upper()

                series.append(dept)
            return reconstruct_like(ubigeo, series)

        else:
            # ------------------------ Input: Singular ------------------------
            code = cls._validate_codigo(ubigeo)
            try:
                dept = cls._resources._loaded["departamentos"][institucion][code[:2]]
            except KeyError:
                raise KeyError(
                    f"El código de ubigeo {code} no se encontró en la base de datos"
                )

            if divide_lima and dept == "Lima":
                if len(code) < 4:
                    raise ValueError(
                        "Para distinguir Lima Metropolitana y Lima Región, el ubigeo debe tener al menos 3 dígitos"
                    )
                prov = cls._resources._loaded["provincias"][institucion][code[:4]]
                dept = "Lima Metropolitana" if prov == "Lima" else "Lima Región"

            return dept if not normalize else eliminar_acentos(dept).upper()

    @classmethod
    def get_provincia(
        cls,
        ubigeo: str | int | SeriesLike,
        institucion: Literal["inei", "reniec", "sunat"] = "inei",
        on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
        normalize: bool = False,
    ) -> str | SeriesLike:
        cls._resources.cargar_diccionario("provincias")

        # ---------------------- Input: Series-like ----------------------
        if is_series_like(ubigeo):
            # Ya no hay necesidad de normalizar el departamento dentro del for loop
            mapping: dict[str, str] = (
                {
                    k: eliminar_acentos(v).upper()
                    for k, v in cls._resources._loaded["provincias"][
                        institucion
                    ].items()
                }
                if normalize
                else cls._resources._loaded["provincias"][institucion]
            )

            series = []
            for u in ubigeo:
                code = cls._validate_codigo(u)
                dept_key = code[:4]
                try:
                    series.append(mapping[dept_key])
                except KeyError:
                    resultado = assert_error(
                        on_error,
                        evaluated=dept_key,
                        message="El código de ubigeo {} no se encontró en la base de datos de provincias",
                    )
                    series.append(resultado)
            return reconstruct_like(ubigeo, series)
        else:
            # ------------------------ Input: Singular ------------------------
            code = cls._validate_codigo(ubigeo)
            if len(code) < 4:
                raise ValueError(
                    "No se aceptan ubigeos con menos de 3 o 4 caracteres para provincias"
                )

            try:
                result = cls._resources._loaded["provincias"][institucion][code[:4]]
            except KeyError:
                raise KeyError(
                    f"El código de ubigeo {ubigeo} no se encontró en la base de datos de provincias"
                )

            return eliminar_acentos(result).upper() if normalize else result

    
    @classmethod
    def get_distrito(
        cls,
        ubigeo: str | int | SeriesLike,
        institucion: Literal["inei", "reniec", "sunat"] = "inei",
        on_error: Literal["raise", "warn", "coerce", "ignore", "capitalize"] = "raise",
        normalize: bool = False,
    ) -> str | SeriesLike:
        cls._resources.cargar_diccionario("distritos")

        # ---------------------- Input: Series-like ----------------------
        if is_series_like(ubigeo) and not isinstance(ubigeo, (str, bytes)):
            mapping: dict[str, str] = (
                {
                    k: eliminar_acentos(v).upper()
                    for k, v in cls._resources._loaded["distritos"][institucion].items()
                }
                if normalize
                else cls._resources._loaded["distritos"][institucion]
            )

            series = []
            for u in ubigeo:
                code = cls._validate_codigo(u)
                dept_key = code[:6]
                try:
                    series.append(mapping[dept_key])
                except KeyError:
                    resultado = assert_error(
                        on_error,
                        evaluated=dept_key,
                        message="El código de ubigeo {} no se encontró en la base de datos de distritos",
                    )
                    series.append(resultado)
            return reconstruct_like(ubigeo, series)

        else:
            # ------------------------ Input: Singular ------------------------
            code = cls._validate_codigo(ubigeo)
            if len(code) not in (5, 6):
                raise ValueError(
                    "No se aceptan ubigeos que no tengan 5 o 6 caracteres para distritos"
                )
            try:
                result = cls._resources._loaded["distritos"][institucion][code]
            except KeyError:
                raise KeyError(
                    f"El código de ubigeo {code} no se encontró en la base de datos de distritos"
                )

            result = cls._resources._loaded["distritos"][institucion][code]

            return eliminar_acentos(result).upper() if normalize else result

    @classmethod
    def get_macrorregion(
        cls,
        departamento_o_ubigeo: str | int | SeriesLike,
        institucion: Literal["inei", "minsa", "ceplan"] = "inei",
        normalize: bool = False,
    ) -> str | SeriesLike:
        cls._resources.cargar_diccionario("macrorregiones")
        mapping = cls._resources._loaded["macrorregiones"][institucion]

        # ---------------------- Input: Series-like ----------------------
        if is_series_like(departamento_o_ubigeo):
            mapping: dict[str, str] = (
                {k: eliminar_acentos(v).upper() for k, v in mapping.items()}
                if normalize
                else mapping
            )
            series = []
            for item in departamento_o_ubigeo:
                if isinstance(item, str):
                    if not item[0].isdigit():
                        # Se asume que es el input es un string con el nombre del departamento
                        departamento = Departamento.validate_departamento(
                            item, normalize=False
                        )
                    else:
                        # Se asume que es el input es un string con el código de ubigeo
                        departamento = cls.get_departamento(item, normalize=False)

                elif isinstance(item, int):
                    # Se asume que es el input es el código en formato string
                    departamento = cls.get_departamento(item, normalize=False)
                else:
                    raise TypeError(
                        "Solo se acepta el nombre del departamento o su código de ubigeo"
                    )
                # if eliminar_acentos(departamento.lower()) in ("region lima", "lima metropolitana"):
                #     departamento = "Lima"
                series.append(mapping[departamento])
            return reconstruct_like(departamento_o_ubigeo, series)

        else:
            # ------------------------ Input: Singular ------------------------
            if isinstance(departamento_o_ubigeo, str):
                if not departamento_o_ubigeo[0].isdigit():
                    # Se asume que es el input es un string con el nombre del departamento
                    departamento = Departamento.validate_departamento(
                        departamento_o_ubigeo, normalize=False
                    )
                else:
                    # Se asume que es el input es un string con el código de ubigeo
                    departamento = cls.get_departamento(
                        departamento_o_ubigeo, normalize=False
                    )

            elif isinstance(departamento_o_ubigeo, int):
                # Se asume que es el input es el código en formato string
                departamento = cls.get_departamento(
                    departamento_o_ubigeo, normalize=False
                )
            else:
                raise TypeError(
                    "Solo se acepta el nombre del departamento o su código de ubigeo"
                )

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
    #     cls._resources.cargar_diccionario("macrorregiones")

    #     diccionario = cls._MACRORREGIONES[institucion]
    #     resultado = defaultdict(list)
    #     for dep, macrorregion in diccionario.items():
    #         resultado[macrorregion].append(dep)

    #     return list(resultado)

    @classmethod
    def get_ubigeo(
        cls,
        ubicacion: str | SeriesLike,
        level: Literal["departamentos", "distritos", "provincias"] = "departamentos",
        institucion: Literal["inei", "reniec", "sunat"] = "inei",
    ) -> str | SeriesLike:
        level = cls._validate_level(level)
        cls._resources.cargar_diccionario("inverted")
        mapping = cls._resources._loaded["inverted"][level][institucion]

        # ---------------------- Input: Series-like ----------------------
        if is_series_like(ubicacion):
            out = []
            for item in ubicacion:
                try:
                    ubicacion_normalized = (
                        eliminar_acentos(str(ubicacion)).upper().strip()
                    )
                except TypeError:
                    raise TypeError(
                        "El lugar debe ser un str, no se aceptan números u otros tipos de datos"
                    )

                try:
                    lugar_clean = Departamento.validate_ubicacion(ubicacion_normalized)
                    out.append(mapping[lugar_clean])
                except KeyError:
                    raise KeyError(
                        f"El lugar '{item}' no se encontró en la base de datos de '{level}'"
                    )
            return reconstruct_like(ubicacion, out)

        else:
            # ------------------------ Input: Singular ------------------------

            try:
                ubicacion = eliminar_acentos(str(ubicacion)).upper().strip()
            except TypeError:
                raise TypeError(
                    "El lugar debe ser un str, no se aceptan números u otros tipos de datos"
                )
            return cls._resources._loaded["inverted"][level][institucion][ubicacion]

    @classmethod
    def get_metadato(
        cls,
        codigo_o_ubicacion: str | int | SeriesLike,
        level: Literal["departamentos", "provincias", "distritos"],
        key: Literal[
            "altitud", "capital", "latitud", "longitud", "superficie"
        ] = "capital",
    ) -> str | SeriesLike:
        level = cls._validate_level(level)
        cls._resources.cargar_diccionario("otros")
        mapping = cls._resources._loaded["otros"][level]

        if not isinstance(key, str):
            raise TypeError(
                'Solo se aceptan "altitud", "capital", "latitud", "longitud", "superficie" como valores para solicitar'
            )

        if key not in ["altitud", "capital", "latitud", "longitud", "superficie"]:
            raise ValueError(
                'Solo se aceptan "altitud", "capital", "latitud", "longitud", "superficie" como valores para solicitar'
            )

        # ---------------------- Input: Series-like ----------------------
        if isinstance(codigo_o_ubicacion, SeriesLike):
            out = []
            for item in codigo_o_ubicacion:
                if isinstance(item, str):
                    if not item[0].isdigit():
                        # Se asume que el input es un string con el nombre del departamento
                        ubicacion = Departamento.validate_ubicacion(
                            item, normalize=False, on_error="ignore"
                        )
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
                    # ubicacion = cls.get_ubigeo(codigo_o_ubicacion, level)
                else:
                    raise TypeError(
                        "Solo se acepta el nombre de la ubicacion o su código de ubigeo"
                    )

                # ubicacion_normalized = eliminar_acentos(item).upper().strip()
                try:
                    ubicacion_normalized = eliminar_acentos(ubicacion).upper()
                    out.append(mapping[ubicacion_normalized][key])
                except KeyError:
                    out.append("")
                    # raise KeyError(f"El lugar '{ubicacion_normalized}' no se encontró en la base de datos de '{level}'")
            return reconstruct_like(codigo_o_ubicacion, out)

        else:
            # ------------------------ Input: Singular ------------------------
            if isinstance(codigo_o_ubicacion, str):
                if not codigo_o_ubicacion[0].isdigit():
                    # Se asume que el input es un string con el nombre del departamento
                    ubicacion = Departamento.validate_ubicacion(
                        codigo_o_ubicacion, normalize=False
                    )
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
                # ubicacion = cls.get_ubigeo(codigo_o_ubicacion, level)
            else:
                raise TypeError(
                    "Solo se acepta el nombre de la ubicacion o su código de ubigeo"
                )

        ubicacion = eliminar_acentos(ubicacion).upper()
        return mapping[ubicacion][key]
