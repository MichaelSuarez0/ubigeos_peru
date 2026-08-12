from typing import Any, Literal, overload

from narwhals.typing import IntoSeriesT

from ._utils import SeriesLike

# ----------------------------------------------------------------------
# VALIDADORES Y GETTERS UBIGEOS
# ----------------------------------------------------------------------

@overload
def get_departamento(
    ubigeo: str,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    divide_lima: bool = False,
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str: ...
@overload
def get_departamento(
    ubigeo: int,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    divide_lima: bool = False,
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str: ...
@overload
def get_departamento(
    ubigeo: IntoSeriesT,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    divide_lima: bool = False,
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> IntoSeriesT: ...
def get_departamento(
    ubigeo: str | int | SeriesLike,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    divide_lima: bool = False,
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str | SeriesLike: ...
@overload
def get_provincia(
    ubigeo: str,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str: ...
@overload
def get_provincia(
    ubigeo: int,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str: ...
@overload
def get_provincia(
    ubigeo: IntoSeriesT,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> IntoSeriesT: ...
def get_provincia(
    ubigeo: str | int | SeriesLike,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str | SeriesLike: ...
@overload
def get_distrito(
    ubigeo: str,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str: ...
@overload
def get_distrito(
    ubigeo: int,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str: ...
@overload
def get_distrito(
    ubigeo: IntoSeriesT,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> IntoSeriesT: ...
def get_distrito(
    ubigeo: str | int | SeriesLike,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str | SeriesLike: ...
@overload
def get_macrorregion(
    departamento_o_ubigeo: str,
    institucion: Literal["inei", "minsa", "ceplan"] = "inei",
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str: ...
@overload
def get_macrorregion(
    departamento_o_ubigeo: int,
    institucion: Literal["inei", "minsa", "ceplan"] = "inei",
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str: ...
@overload
def get_macrorregion(
    departamento_o_ubigeo: IntoSeriesT,
    institucion: Literal["inei", "minsa", "ceplan"] = "inei",
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> IntoSeriesT: ...
def get_macrorregion(
    departamento_o_ubigeo: str | int | SeriesLike,
    institucion: Literal["inei", "minsa", "ceplan"] = "inei",
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str | SeriesLike: ...
@overload
def get_ubigeo(
    ubicacion: str,
    level: Literal["departamentos", "distritos", "provincias"] = "departamentos",
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str: ...
@overload
def get_ubigeo(
    ubicacion: IntoSeriesT,
    level: Literal["departamentos", "distritos", "provincias"] = "departamentos",
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> IntoSeriesT: ...
def get_ubigeo(
    ubicacion: str | SeriesLike,
    level: Literal["departamentos", "distritos", "provincias"] = "departamentos",
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str | SeriesLike: ...
@overload
def validate_departamento(
    departamento: str,
    normalize: bool = False,
    fuzzy_match: bool = True,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str: ...
@overload
def validate_departamento(
    departamento: IntoSeriesT,
    normalize: bool = False,
    fuzzy_match: bool = True,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> IntoSeriesT: ...
def validate_departamento(
    departamento: str | SeriesLike,
    normalize: bool = False,
    fuzzy_match: bool = True,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str | SeriesLike: ...
@overload
def validate_provincia(
    provincia: str,
    normalize: bool = False,
    fuzzy_match: bool = True,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str: ...
@overload
def validate_provincia(
    provincia: IntoSeriesT,
    normalize: bool = False,
    fuzzy_match: bool = True,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> IntoSeriesT: ...
def validate_provincia(
    provincia: str | SeriesLike,
    normalize: bool = False,
    fuzzy_match: bool = True,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str | SeriesLike: ...
@overload
def validate_distrito(
    distrito: str,
    normalize: bool = False,
    fuzzy_match: bool = True,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str: ...
@overload
def validate_distrito(
    distrito: IntoSeriesT,
    normalize: bool = False,
    fuzzy_match: bool = True,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> IntoSeriesT: ...
def validate_distrito(
    distrito: str | SeriesLike,
    normalize: bool = False,
    fuzzy_match: bool = True,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str | SeriesLike: ...
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
) -> dict[str, Any]: ...
