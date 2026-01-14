from typing import TYPE_CHECKING, Any, Literal, overload

if TYPE_CHECKING:
    import pandas as pd
    import polars as pl

from ._utils import SeriesLike

# ----------------------------------------------------------------------
# VALIDADORES Y GETTERS UBIGEOS
# ----------------------------------------------------------------------

@overload
def get_departamento(
    ubigeo: str | int | SeriesLike,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    divide_lima: bool = False,
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str | SeriesLike: ...
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
    ubigeo: pd.Series,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    divide_lima: bool = False,
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> pd.Series: ...
@overload
def get_departamento(
    ubigeo: pl.Series,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    divide_lima: bool = False,
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> pl.Series: ...
def get_departamento(
    ubigeo: str | SeriesLike,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    divide_lima: bool = False,
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str | SeriesLike: ...
@overload
def get_provincia(
    ubigeo: str | int | SeriesLike,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
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
    ubigeo: pd.Series,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> pd.Series: ...
@overload
def get_provincia(
    ubigeo: pl.Series,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> pl.Series: ...
def get_provincia(
    ubigeo: str | SeriesLike,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str | SeriesLike: ...
@overload
def get_distrito(
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
    ubigeo: pd.Series,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> pd.Series: ...
@overload
def get_distrito(
    ubigeo: pl.Series,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> pl.Series: ...
def get_distrito(
    ubigeo: str | SeriesLike,
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str | SeriesLike: ...
@overload
def get_macrorregion(
    departamento_o_ubigeo: str | SeriesLike,
    institucion: Literal["inei", "minsa", "ceplan"] = "inei",
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
    departamento_o_ubigeo: pd.Series,
    institucion: Literal["inei", "minsa", "ceplan"] = "inei",
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> pd.Series: ...
@overload
def get_macrorregion(
    departamento_o_ubigeo: pl.Series,
    institucion: Literal["inei", "minsa", "ceplan"] = "inei",
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> pl.Series: ...
def get_macrorregion(
    departamento_o_ubigeo: str | SeriesLike,
    institucion: Literal["inei", "minsa", "ceplan"] = "inei",
    normalize: bool = False,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str | SeriesLike: ...
@overload
def get_ubigeo(
    ubicacion: str | SeriesLike,
    level: Literal["departamentos", "distritos", "provincias"] = "departamentos",
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
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
    ubicacion: pd.Series,
    level: Literal["departamentos", "distritos", "provincias"] = "departamentos",
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> pd.Series: ...
@overload
def get_ubigeo(
    ubicacion: pl.Series,
    level: Literal["departamentos", "distritos", "provincias"] = "departamentos",
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> pl.Series: ...
def get_ubigeo(
    ubicacion: str | SeriesLike,
    level: Literal["departamentos", "distritos", "provincias"] = "departamentos",
    institucion: Literal["inei", "reniec", "sunat"] = "inei",
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str | SeriesLike: ...

# @overload
# def get_metadato(
#     codigo_ubigeo: str | SeriesLike,
#     campo: Literal["departamento", "provincia", "distrito", "macrorregion"],
#     on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
# ) -> str | SeriesLike: ...
# @overload
# def get_metadato(
#     codigo_ubigeo: str,
#     campo: Literal["departamento", "provincia", "distrito", "macrorregion"],
#     on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
# ) -> str: ...
# @overload
# def get_metadato(
#     codigo_ubigeo: pd.Series,
#     campo: Literal["departamento", "provincia", "distrito", "macrorregion"],
#     on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
# ) -> pd.Series: ...
# @overload
# def get_metadato(
#     codigo_ubigeo: pl.Series,
#     campo: Literal["departamento", "provincia", "distrito", "macrorregion"],
#     on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
# ) -> pl.Series: ...
# def get_metadato(
#     codigo_ubigeo: str | SeriesLike,
#     campo: Literal["departamento", "provincia", "distrito", "macrorregion"],
#     on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
# ) -> str | SeriesLike: ...


@overload
def validate_departamento(
    departamento: str,
    normalize: bool = False,
    fuzzy_match: bool = True,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str: ...

@overload
def validate_departamento(
    departamento: pd.Series,
    normalize: bool = False,
    fuzzy_match: bool = True,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> pd.Series: ...

@overload
def validate_departamento(
    departamento: pl.Series,
    normalize: bool = False,
    fuzzy_match: bool = True,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> pl.Series: ...

def validate_departamento(
    departamento: str | SeriesLike,
    normalize: bool = False,
    fuzzy_match: bool = True,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str | SeriesLike: ...

# ==================== validate_provincia ====================
@overload
def validate_provincia(
    provincia: str,
    normalize: bool = False,
    fuzzy_match: bool = True,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str: ...

@overload
def validate_provincia(
    provincia: pd.Series,
    normalize: bool = False,
    fuzzy_match: bool = True,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> pd.Series: ...

@overload
def validate_provincia(
    provincia: pl.Series,
    normalize: bool = False,
    fuzzy_match: bool = True,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> pl.Series: ...

def validate_provincia(
    provincia: str | SeriesLike,
    normalize: bool = False,
    fuzzy_match: bool = True,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str | SeriesLike: ...

# ==================== validate_distrito ====================
@overload
def validate_distrito(
    distrito: str,
    normalize: bool = False,
    fuzzy_match: bool = True,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str: ...

@overload
def validate_distrito(
    distrito: pd.Series,
    normalize: bool = False,
    fuzzy_match: bool = True,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> pd.Series: ...

@overload
def validate_distrito(
    distrito: pl.Series,
    normalize: bool = False,
    fuzzy_match: bool = True,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> pl.Series: ...

def validate_distrito(
    distrito: str | SeriesLike,
    normalize: bool = False,
    fuzzy_match: bool = True,
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
) -> str | SeriesLike: ...

# ==================== cargar_diccionario ====================
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

