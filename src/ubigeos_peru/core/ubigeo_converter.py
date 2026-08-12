from typing import Literal

import narwhals as nw
from narwhals.typing import IntoSeriesT

from ._utils import (
    assert_error,
    eliminar_acentos,
)
from .resource_manager import ResourceManager
from .validations import Validations

Levels = Literal["departamentos", "provincias", "distritos"]


class UbigeoConverter:
    _instance = None
    _resources = ResourceManager()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UbigeoConverter, cls).__new__(cls)
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
    def _validate_level(cls, level: Levels) -> Levels:
        if isinstance(level, str) and not level.endswith("s"):
            level += "s"

        if level not in ["departamentos", "distritos", "provincias"]:
            raise ValueError(
                'Solo se aceptan "departamentos", "distritos", "provincias" como argumentos para el nivel (level)'
            )

        return level

    # ------------------------------------------------------------------
    # GET DEPARTAMENTO - SERIES
    # ------------------------------------------------------------------

    @staticmethod
    @nw.narwhalify(
        series_only=True,
        eager_only=True,
    )
    def _get_departamento_series(
        ubigeo: nw.Series,
        mapping: dict[str, str],
        provincias: dict[str, str] | None,
        normalize: bool,
        divide_lima: bool,
    ) -> nw.Series:
        resultado = []

        for value in ubigeo:
            code = UbigeoConverter._validate_codigo(value)

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
                        "Para distinguir Lima Metropolitana "
                        "y Lima Región, el ubigeo debe tener "
                        "al menos 3 dígitos"
                    )

                if provincias is None:
                    raise RuntimeError("No se cargó el diccionario de provincias")

                prov = provincias[code[:4]]

                dept = "Lima Metropolitana" if prov == "Lima" else "Lima Región"

            if normalize:
                dept = eliminar_acentos(dept).upper()

            resultado.append(dept)

        return nw.new_series(
            name=ubigeo.name,
            values=resultado,
            backend=ubigeo.implementation,
        )

    # ------------------------------------------------------------------
    # GET DEPARTAMENTO
    # ------------------------------------------------------------------

    @classmethod
    def get_departamento(
        cls,
        ubigeo: str | int | IntoSeriesT,
        institucion: Literal[
            "inei",
            "reniec",
            "sunat",
        ] = "inei",
        divide_lima: bool = False,
        normalize: bool = False,
    ) -> str | IntoSeriesT:

        cls._resources.cargar_diccionario("departamentos")

        if divide_lima:
            cls._resources.cargar_diccionario("provincias")

        mapping = cls._resources._loaded["departamentos"][institucion]

        if isinstance(ubigeo, (str, int)):
            code = cls._validate_codigo(ubigeo)

            try:
                dept = mapping[code[:2]]
            except KeyError:
                raise KeyError(
                    f"El código de ubigeo {code} no se encontró en la base de datos"
                )

            if divide_lima and dept == "Lima":
                if len(code) < 4:
                    raise ValueError(
                        "Para distinguir Lima Metropolitana "
                        "y Lima Región, el ubigeo debe tener "
                        "al menos 3 dígitos"
                    )

                prov = cls._resources._loaded["provincias"][institucion][code[:4]]

                dept = "Lima Metropolitana" if prov == "Lima" else "Lima Región"

            return eliminar_acentos(dept).upper() if normalize else dept

        mapping_series = (
            {k: eliminar_acentos(v).upper() for k, v in mapping.items()}
            if normalize
            else mapping
        )

        provincias = (
            cls._resources._loaded["provincias"][institucion] if divide_lima else None
        )

        return cls._get_departamento_series(
            ubigeo,
            mapping_series,
            provincias,
            normalize,
            divide_lima,
        )

    # ------------------------------------------------------------------
    # GET PROVINCIA - SERIES
    # ------------------------------------------------------------------

    @staticmethod
    @nw.narwhalify(
        series_only=True,
        eager_only=True,
    )
    def _get_provincia_series(
        ubigeo: nw.Series,
        mapping: dict[str, str],
        institucion: str,
        on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"],
    ) -> nw.Series:
        resultado = []

        for value in ubigeo:
            code = UbigeoConverter._validate_codigo(value)

            if len(code) < 4:
                raise ValueError(
                    "No se aceptan ubigeos con menos de 3 o 4 caracteres para provincias"
                )

            prov_key = code[:4]

            try:
                prov = mapping[prov_key]
            except KeyError:
                prov = assert_error(
                    on_error,
                    evaluated=prov_key,
                    institucion=institucion,
                    message="El código de ubigeo {} no se encontró en la base de datos de provincias de {}",
                )

            resultado.append(prov)

        return nw.new_series(
            name=ubigeo.name,
            values=resultado,
            backend=ubigeo.implementation,
        )

    # ------------------------------------------------------------------
    # GET PROVINCIA
    # ------------------------------------------------------------------

    @classmethod
    def get_provincia(
        cls,
        ubigeo: str | int | IntoSeriesT,
        institucion: Literal["inei", "reniec", "sunat"] = "inei",
        on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
        normalize: bool = False,
    ) -> str | IntoSeriesT:
        cls._resources.cargar_diccionario("provincias")

        mapping = cls._resources._loaded["provincias"][institucion]

        if isinstance(ubigeo, (str, int)):
            code = cls._validate_codigo(ubigeo)
            if len(code) < 4:
                raise ValueError(
                    "No se aceptan ubigeos con menos de 3 o 4 caracteres para provincias"
                )

            try:
                result = mapping[code[:4]]
            except KeyError:
                raise KeyError(
                    f"El código de ubigeo {ubigeo} no se encontró en la base de datos de provincias de {institucion.upper()}"
                )

            return eliminar_acentos(result).upper() if normalize else result

        mapping_series = (
            {k: eliminar_acentos(v).upper() for k, v in mapping.items()}
            if normalize
            else mapping
        )

        return cls._get_provincia_series(ubigeo, mapping_series, institucion, on_error)

    # ------------------------------------------------------------------
    # GET DISTRITO - SERIES
    # ------------------------------------------------------------------

    @staticmethod
    @nw.narwhalify(
        series_only=True,
        eager_only=True,
    )
    def _get_distrito_series(
        ubigeo: nw.Series,
        mapping: dict[str, str],
        institucion: str,
        on_error: Literal["raise", "warn", "coerce", "ignore", "capitalize"],
    ) -> nw.Series:
        resultado = []

        for value in ubigeo:
            code = UbigeoConverter._validate_codigo(value)

            if len(code) not in (5, 6):
                raise ValueError(
                    "No se aceptan ubigeos que no tengan 5 o 6 caracteres para distritos"
                )

            dist_key = code[:6]

            try:
                dist = mapping[dist_key]
            except KeyError:
                dist = assert_error(
                    on_error,
                    evaluated=dist_key,
                    institucion=institucion,
                    message="El código de ubigeo {} no se encontró en la base de datos de distritos de {}",
                )

            resultado.append(dist)

        return nw.new_series(
            name=ubigeo.name,
            values=resultado,
            backend=ubigeo.implementation,
        )

    # ------------------------------------------------------------------
    # GET DISTRITO
    # ------------------------------------------------------------------

    @classmethod
    def get_distrito(
        cls,
        ubigeo: str | int | IntoSeriesT,
        institucion: Literal["inei", "reniec", "sunat"] = "inei",
        on_error: Literal["raise", "warn", "coerce", "ignore", "capitalize"] = "raise",
        normalize: bool = False,
    ) -> str | IntoSeriesT:
        cls._resources.cargar_diccionario("distritos")

        mapping = cls._resources._loaded["distritos"][institucion]

        if isinstance(ubigeo, (str, int)):
            code = cls._validate_codigo(ubigeo)
            if len(code) not in (5, 6):
                raise ValueError(
                    "No se aceptan ubigeos que no tengan 5 o 6 caracteres para distritos"
                )
            try:
                result = mapping[code]
            except KeyError:
                raise KeyError(
                    f"El código de ubigeo {code} no se encontró en la base de datos de distritos de {institucion.upper()}"
                )

            return eliminar_acentos(result).upper() if normalize else result

        mapping_series = (
            {k: eliminar_acentos(v).upper() for k, v in mapping.items()}
            if normalize
            else mapping
        )

        return cls._get_distrito_series(ubigeo, mapping_series, institucion, on_error)

    # ------------------------------------------------------------------
    # GET MACRORREGION - SERIES
    # ------------------------------------------------------------------

    @staticmethod
    @nw.narwhalify(
        series_only=True,
        eager_only=True,
    )
    def _get_macrorregion_series(
        departamento_o_ubigeo: nw.Series,
        mapping: dict[str, str],
        institucion: Literal["inei", "minsa", "ceplan"],
    ) -> nw.Series:
        resultado = []

        for item in departamento_o_ubigeo:
            if isinstance(item, str):
                if not item[0].isdigit():
                    departamento = Validations.validate_departamento(
                        item, normalize=False
                    )
                else:
                    departamento = UbigeoConverter.get_departamento(
                        item, institucion=institucion, normalize=False
                    )
            elif isinstance(item, int):
                departamento = UbigeoConverter.get_departamento(
                    item, institucion=institucion, normalize=False
                )
            else:
                raise TypeError(
                    "Solo se acepta el nombre del departamento o su código de ubigeo"
                )

            try:
                resultado.append(mapping[departamento])
            except KeyError:
                raise KeyError(
                    f"El departamento '{departamento}' no se encontró en la base de datos de macrorregiones de {institucion.upper()}"
                )

        return nw.new_series(
            name=departamento_o_ubigeo.name,
            values=resultado,
            backend=departamento_o_ubigeo.implementation,
        )

    # ------------------------------------------------------------------
    # GET MACRORREGION
    # ------------------------------------------------------------------

    @classmethod
    def get_macrorregion(
        cls,
        departamento_o_ubigeo: str | int | IntoSeriesT,
        institucion: Literal["inei", "minsa", "ceplan"] = "inei",
        normalize: bool = False,
    ) -> str | IntoSeriesT:
        cls._resources.cargar_diccionario("macrorregiones")
        mapping = cls._resources._loaded["macrorregiones"][institucion]

        if isinstance(departamento_o_ubigeo, (str, int)):
            if isinstance(departamento_o_ubigeo, str):
                if not departamento_o_ubigeo[0].isdigit():
                    departamento = Validations.validate_departamento(
                        departamento_o_ubigeo, normalize=False
                    )
                else:
                    departamento = cls.get_departamento(
                        departamento_o_ubigeo, institucion=institucion, normalize=False
                    )
            else:
                departamento = cls.get_departamento(
                    departamento_o_ubigeo, institucion=institucion, normalize=False
                )

            try:
                resultado = mapping[departamento]
            except KeyError:
                raise KeyError(
                    f"El departamento '{departamento}' no se encontró en la base de datos de macrorregiones de {institucion.upper()}"
                )

            return eliminar_acentos(resultado).upper() if normalize else resultado

        mapping_series = (
            {k: eliminar_acentos(v).upper() for k, v in mapping.items()}
            if normalize
            else mapping
        )

        return cls._get_macrorregion_series(
            departamento_o_ubigeo, mapping_series, institucion
        )

    # ------------------------------------------------------------------
    # GET UBIGEO - SERIES
    # ------------------------------------------------------------------

    @staticmethod
    @nw.narwhalify(
        series_only=True,
        eager_only=True,
    )
    def _get_ubigeo_series(
        ubicacion: nw.Series,
        mapping: dict[str, str],
        institucion: str,
        level: Levels,
    ) -> nw.Series:
        resultado = []

        for item in ubicacion:
            try:
                item_normalized = eliminar_acentos(str(item)).upper().strip()
            except TypeError:
                raise TypeError(
                    "El lugar debe ser un str, no se aceptan números u otros tipos de datos"
                )

            if level == "provincias":
                lugar_clean = Validations.validate_provincia(item_normalized)
            elif level == "distritos":
                lugar_clean = Validations.validate_distrito(item_normalized)
            else:
                lugar_clean = Validations.validate_departamento(item_normalized)

            try:
                resultado.append(mapping[lugar_clean])
            except KeyError:
                raise KeyError(
                    f"El lugar '{item}' no se encontró en la base de datos de '{level}' de de {institucion.upper()}"
                )

        return nw.new_series(
            name=ubicacion.name,
            values=resultado,
            backend=ubicacion.implementation,
        )

    # ------------------------------------------------------------------
    # GET UBIGEO
    # ------------------------------------------------------------------

    @classmethod
    def get_ubigeo(
        cls,
        ubicacion: str | IntoSeriesT,
        level: Levels,
        institucion: Literal["inei", "reniec", "sunat"] = "inei",
    ) -> str | IntoSeriesT:
        level = cls._validate_level(level)
        cls._resources.cargar_diccionario("inverted")
        mapping = cls._resources._loaded["inverted"][level][institucion]

        if isinstance(ubicacion, str):
            try:
                ubicacion_normalized = eliminar_acentos(ubicacion).upper().strip()
            except TypeError:
                raise TypeError(
                    "El lugar debe ser un str, no se aceptan números u otros tipos de datos"
                )

            try:
                return mapping[ubicacion_normalized]
            except KeyError:
                raise KeyError(
                    f"El lugar '{ubicacion}' no se encontró en la base de datos de '{level}' de {institucion.upper()}"
                )

        return cls._get_ubigeo_series(ubicacion, mapping, institucion, level)

    # ------------------------------------------------------------------
    # GET METADATO - SERIES
    # ------------------------------------------------------------------

    @staticmethod
    @nw.narwhalify(
        series_only=True,
        eager_only=True,
    )
    def _get_metadato_series(
        codigo_o_ubicacion: nw.Series,
        mapping: dict[str, dict[str, str]],
        level: Levels,
        key: Literal["altitud", "capital", "latitud", "longitud", "superficie"],
        institucion: Literal["inei", "reniec", "sunat"],
    ) -> nw.Series:
        resultado = []

        for item in codigo_o_ubicacion:
            if isinstance(item, str):
                if not item[0].isdigit():
                    if level == "departamentos":
                        ubicacion = Validations.validate_departamento(
                            item, normalize=False, on_error="ignore"
                        )
                    elif level == "provincias":
                        ubicacion = Validations.validate_provincia(
                            item, normalize=False, on_error="ignore"
                        )
                    else:
                        ubicacion = Validations.validate_distrito(
                            item, normalize=False, on_error="ignore"
                        )
                else:
                    ubicacion = UbigeoConverter.get_ubigeo(item, level, institucion)
            elif isinstance(item, int):
                if level == "departamentos":
                    ubicacion = UbigeoConverter.get_departamento(
                        item, institucion=institucion
                    )
                elif level == "provincias":
                    ubicacion = UbigeoConverter.get_provincia(
                        item, institucion=institucion
                    )
                else:
                    ubicacion = UbigeoConverter.get_distrito(
                        item, institucion=institucion
                    )
            else:
                raise TypeError(
                    "Solo se acepta el nombre de la ubicacion o su código de ubigeo"
                )

            ubicacion_normalized = eliminar_acentos(ubicacion).upper()

            try:
                resultado.append(mapping[ubicacion_normalized][key])
            except KeyError:
                resultado.append("")

        return nw.new_series(
            name=codigo_o_ubicacion.name,
            values=resultado,
            backend=codigo_o_ubicacion.implementation,
        )

    # ------------------------------------------------------------------
    # GET METADATO
    # ------------------------------------------------------------------

    @classmethod
    def get_metadato(
        cls,
        codigo_o_ubicacion: str | int | IntoSeriesT,
        level: Levels,
        key: Literal[
            "altitud", "capital", "latitud", "longitud", "superficie"
        ] = "capital",
        institucion: Literal["inei", "reniec", "sunat"] = "inei",
    ) -> str | IntoSeriesT:
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

        if isinstance(codigo_o_ubicacion, (str, int)):
            if isinstance(codigo_o_ubicacion, str):
                if not codigo_o_ubicacion[0].isdigit():
                    if level == "departamentos":
                        ubicacion = Validations.validate_departamento(
                            codigo_o_ubicacion, normalize=False, on_error="ignore"
                        )
                    elif level == "provincias":
                        ubicacion = Validations.validate_provincia(
                            codigo_o_ubicacion, normalize=False, on_error="ignore"
                        )
                    else:
                        ubicacion = Validations.validate_distrito(
                            codigo_o_ubicacion, normalize=False, on_error="ignore"
                        )
                else:
                    ubicacion = cls.get_ubigeo(codigo_o_ubicacion, level, institucion)
            else:
                if level == "departamentos":
                    ubicacion = cls.get_departamento(
                        codigo_o_ubicacion, institucion=institucion
                    )
                elif level == "provincias":
                    ubicacion = cls.get_provincia(
                        codigo_o_ubicacion, institucion=institucion
                    )
                else:
                    ubicacion = cls.get_distrito(
                        codigo_o_ubicacion, institucion=institucion
                    )

            ubicacion = eliminar_acentos(ubicacion).upper()

            try:
                return mapping[ubicacion][key]
            except KeyError:
                return ""

        return cls._get_metadato_series(
            codigo_o_ubicacion, mapping, level, key, institucion
        )
