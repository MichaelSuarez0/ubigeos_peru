from functools import lru_cache
import unicodedata
from typing import Any, Literal, Protocol, Sequence, TypeVar, runtime_checkable

@lru_cache(maxsize=128)
def eliminar_acentos(texto: str) -> str:
    texto_normalizado = unicodedata.normalize("NFKD", texto)
    texto_sin_acentos = "".join(
        c for c in texto_normalizado if not unicodedata.combining(c)
    )
    return texto_sin_acentos

@runtime_checkable
class SeriesLike(Protocol):
    def map(self, mapper: Any) -> "SeriesLike": ...

S = TypeVar("S", bound=SeriesLike)

#@lru_cache(maxsize=128)
def is_series_like(obj: Any) -> bool:
    # Duck typing: iterable pero que NO sea str ni bytes ni dict
    if isinstance(obj, (str, bytes, dict)):
        return False
    try:
        iter(obj)
        return True
    except TypeError:
        return False

def reconstruct_like(proto: Any, data: Sequence) -> Any:
    """
    Intenta reconstruir el mismo tipo de contenedor que 'proto' con 'data'.
    Si falla, devuelve list(data). No requiere pandas.
    """
    try:
        # Caso común: list -> list(data), tuple -> tuple(data), numpy -> np.array(data), pd.Series -> Series(data)
        return proto.__class__(data)
    except Exception:
        return list(data)

def assert_error(on_error: Literal["raise", "ignore", "capitalize"], evaluated: str, message: str):
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
