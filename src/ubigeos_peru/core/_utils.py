import unicodedata
import warnings
from functools import lru_cache
from typing import Literal, Optional

from rapidfuzz import fuzz, process, utils


@lru_cache(maxsize=128)
def eliminar_acentos(texto: str) -> str:
    texto_normalizado = unicodedata.normalize("NFKD", texto)
    texto_sin_acentos = "".join(
        c for c in texto_normalizado if not unicodedata.combining(c)
    )
    return texto_sin_acentos


def assert_error(
    on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"],
    evaluated: str,
    institucion: str,
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
        raise KeyError(message.format(evaluated, institucion))
    elif on_error == "warn":
        warnings.warn(message.format(evaluated, institucion), UserWarning, stacklevel=2)
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
