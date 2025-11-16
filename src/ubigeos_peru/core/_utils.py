import unicodedata
import warnings
from functools import lru_cache
from typing import (
    Any,
    Iterator,
    Literal,
    Optional,
    Protocol,
    TypeGuard,
    runtime_checkable,
)

from rapidfuzz import fuzz, process, utils


@lru_cache(maxsize=128)
def eliminar_acentos(texto: str) -> str:
    texto_normalizado = unicodedata.normalize("NFKD", texto)
    texto_sin_acentos = "".join(
        c for c in texto_normalizado if not unicodedata.combining(c)
    )
    return texto_sin_acentos


@runtime_checkable
class SeriesLike(Protocol):
    # def apply(self, *args: Any, **kwargs: Any) -> Any: ...
    def __iter__(self) -> Iterator[Any]: ...


# class Expr(Protocol):
#     #def apply(self, *args: Any, **kwargs: Any) -> Any: ...
#     def alias(self, name: str, *args: Any, **kwargs: Any) -> "Expr": ...

# SeriesLike = Series | Expr


# @lru_cache(maxsize=128) # No funciona con Series
def is_series_like(obj: Any) -> TypeGuard[SeriesLike]:
    """
    Determina si el objeto es una estructura tipo serie (pandas, polars o iterable),
    sin requerir dependencias externas.

    Detecta dinámicamente:
      - pandas.Series
      - polars.Series
      - polars.Expr
      - cualquier iterable (listas, arrays, etc.)
    Excluye tipos escalares (str, int, bytes, dict).

    Returns
    -------
    bool
        True si el objeto se comporta como una serie o expresión; False en caso contrario.
    """
    if isinstance(obj, (str, int, bytes, dict)):
        return False

    # Introspección segura
    module = getattr(type(obj), "__module__", "")
    name = getattr(type(obj), "__name__", "")

    # pandas.Series
    if "pandas" in module and name == "Series":
        return True

    # polars.Series o polars.Expr
    if "polars" in module and name in ("Series", "Expr"):
        return True

    # Genérico iterable (listas, tuplas, arrays, etc.)
    if hasattr(obj, "__iter__"):
        return True

    return False


def reconstruct_like(proto: Any, data: list[str]) -> Any:
    """
    Intenta reconstruir el mismo tipo de contenedor que 'proto' con 'data'.
    Si falla, devuelve list(data). No requiere pandas.
    """
    return proto.__class__(data)
    # except Exception:
    #     return list(data)


def assert_error(
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"],
    evaluated: str,
    message: str,
) -> Optional[str]:
    """
    Maneja errores en la transformación de ubigeos.

    Parameters
    ----------
    on_error : {'raise', 'warn', 'ignore', 'capitalize', 'coerce'}
        - 'raise': Lanza KeyError
        - 'warn': Emite warning y retorna None
        - 'coerce': Retorna None
        - 'ignore': Retorna el valor sin cambios
        - 'capitalize': Capitaliza el valor
    evaluated : str
        El valor (ubigeo) a procesar
    message : str
        Mensaje de error (puede usar .format())

    Returns
    -------
    str or None
        Valor procesado según la estrategia
    """
    if on_error == "raise":
        raise KeyError(message.format(evaluated))
    elif on_error == "warn":
        warnings.warn(message.format(evaluated), UserWarning, stacklevel=2)
        return evaluated
    elif on_error == "coerce":
        return None
    elif on_error == "ignore":
        return evaluated
    elif on_error == "capitalize":
        return evaluated.capitalize()
    else:
        raise ValueError(
            'El arg "on_error" debe ser uno de: "raise", "warn", "ignore", "capitalize", "coerce"'
        )


def fuzzy_validate(ubicacion: str, options: list[str], limit: int = 1):
    result = process.extractOne(
        ubicacion, options, scorer=fuzz.WRatio, processor=utils.default_process
    )
    if result[1] >= 80:
        return result[0]
    else:
        return None
