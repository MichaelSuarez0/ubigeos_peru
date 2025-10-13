from typing import overload, Literal, TYPE_CHECKING
if TYPE_CHECKING:
    import pandas as pd
    import polars as pl

from ._utils import SeriesLike


@overload
def validate_departamento(
    nombre_departamento: str | SeriesLike,
    normalize: bool = False,
    on_error: Literal["raise", "ignore", "capitalize"] = "raise",
) -> str | SeriesLike: ...

@overload
def validate_departamento(
    nombre_departamento: str,
    normalize: bool = False,
    on_error: Literal["raise", "ignore", "capitalize"] = "raise",
) -> str: ...

@overload
def validate_departamento(
    nombre_departamento: pd.Series,
    normalize: bool = False,
    on_error: Literal["raise", "ignore", "capitalize"] = "raise",
) -> pd.Series: ...

@overload
def validate_departamento(
    nombre_departamento: pl.Series,
    normalize: bool = False,
    on_error: Literal["raise", "ignore", "capitalize"] = "raise",
) -> pl.Series: ...

def validate_departamento(
    nombre_departamento: str | SeriesLike,
    normalize: bool = False,
    on_error: Literal["raise", "ignore", "capitalize"] = "raise",
) -> str | SeriesLike: ...

