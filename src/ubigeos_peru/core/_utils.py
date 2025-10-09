from functools import lru_cache
import unicodedata
from typing import Any, Callable, Iterable, Iterator, Literal, Protocol, Self, Sequence, TypeGuard, TypeVar, Union, overload, runtime_checkable

@lru_cache(maxsize=128)
def eliminar_acentos(texto: str) -> str:
    texto_normalizado = unicodedata.normalize("NFKD", texto)
    texto_sin_acentos = "".join(
        c for c in texto_normalizado if not unicodedata.combining(c)
    )
    return texto_sin_acentos

_T = TypeVar('_T')

@runtime_checkable
class SeriesLike(Protocol):
    def map(self, *args: Any, **kwargs: Any) -> Any: ...
    def __iter__(self) -> Iterator[Any]: ...

    
S = TypeVar("S")

#@lru_cache(maxsize=128)
def is_series_like(obj: Any) -> TypeGuard[SeriesLike]:
    return not isinstance(obj, (str, int, bytes, dict)) and hasattr(obj, "__iter__")

def reconstruct_like(proto: Any, data: list[str]) -> Any:
    """
    Intenta reconstruir el mismo tipo de contenedor que 'proto' con 'data'.
    Si falla, devuelve list(data). No requiere pandas.
    """
    return proto.__class__(data)
    # except Exception:
    #     return list(data)

def assert_error(on_error: Literal["raise", "warn", "capitalize", "ignore"], evaluated: str, message: str):
    if on_error == "raise":
        raise KeyError(message.format(evaluated))
    elif on_error == "ignore":
        return evaluated
    elif on_error == "capitalize":
        return evaluated.capitalize()
    else:
        raise ValueError(
            'El arg "on_error" debe ser uno de los siguientes: "raise", "ignore", "capitalize"'
        )
