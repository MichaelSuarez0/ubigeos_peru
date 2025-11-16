from typing import Literal

from ._utils import (
    SeriesLike,
    assert_error,
    eliminar_acentos,
    fuzzy_validate,
    is_series_like,
    reconstruct_like,
)
from .resource_manager import ResourceManager


class Validations:
    _resources = ResourceManager()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Validations, cls).__new__(cls)
        return cls._instance

    @classmethod
    def _validate_generic(
        cls,
        value: str | SeriesLike,
        entity_type: Literal["departamentos", "provincias", "distritos"],
        normalize: bool = False,
        fuzzy_match: bool = True,
        on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
    ) -> str | SeriesLike:
        """
        Función genérica para validar departamentos, provincias o distritos.

        Parameters
        ----------
        value : str | SeriesLike
            Valor o serie de valores a validar.
        entity_type : {'departamentos', 'provincias', 'distritos'}
            Tipo de entidad a validar.
        normalize : bool, optional
            Si True, normaliza (elimina acentos y convierte a mayúsculas) el resultado.
            Por defecto False.
        fuzzy_match : bool, optional
            Si True, intenta una búsqueda difusa (fuzzy matching) cuando no hay
            coincidencia exacta. Por defecto True.
        on_error : {'raise', 'warn', 'ignore', 'capitalize', 'coerce'}, optional
            Comportamiento ante errores. Por defecto 'raise'.

        Returns
        -------
        str | SeriesLike
            Valor o serie de valores validados. Si `normalize` es True, devuelve
            los valores normalizados.
        """
        cls._resources.cargar_diccionario("equivalencias")
        mapping = cls._resources._loaded["equivalencias"][entity_type]

        # Mensajes de error personalizados
        error_messages = {
            "departamentos": "No se ha encontrado el departamento {}",
            "provincias": "No se ha encontrado la provincia {}",
            "distritos": "No se ha encontrado el distrito {}",
        }
        error_message = error_messages[entity_type]

        # ---------------------- Input: Series-like ----------------------
        if is_series_like(value):
            mapping_processed = (
                {k: eliminar_acentos(v).upper() for k, v in mapping.items()}
                if normalize
                else mapping
            )
            out = []
            fuzzy_matched = set()

            for item in value:
                if not isinstance(item, str) or item.isdigit():
                    raise TypeError(
                        f"No se permiten otros tipos de datos que no sean str, se insertó {type(item)}"
                    )

                item_limpio = eliminar_acentos(item).strip().upper()

                # Intentar búsqueda directa
                try:
                    out.append(mapping_processed[item_limpio])
                    continue
                except KeyError:
                    pass

                # Intentar fuzzy matching
                if fuzzy_match:
                    resultado = fuzzy_validate(
                        item_limpio, list(mapping_processed.keys()), limit=1
                    )
                    if resultado:
                        resultado_limpio = eliminar_acentos(resultado).upper()
                        out.append(mapping_processed[resultado_limpio])
                        fuzzy_matched.add((item_limpio, resultado_limpio))
                        continue

                # Manejo de errores
                resultado = assert_error(
                    on_error,
                    evaluated=item_limpio,
                    message=error_message,
                )
                out.append(resultado)

            # Imprimir fuzzy matches
            if fuzzy_matched:
                print(
                    f"Los siguientes {entity_type} fueron obtenidos con fuzzy match. Validar:"
                )
                for original, matched in fuzzy_matched:
                    print(f"{original} -> {matched}")

            return reconstruct_like(value, out)

        # ------------------------ Input: Singular ------------------------
        else:
            if not isinstance(value, str):
                try:
                    str(value)
                except TypeError:
                    raise TypeError(
                        f"No se permiten otros tipos de datos que no sean str, se insertó {type(value)}"
                    )

            item_limpio = eliminar_acentos(value).strip().upper()
            resultado = None
            
            # Intentar búsqueda directa
            try:
                resultado = mapping[item_limpio]
            except KeyError:
            # Intentar fuzzy matching si no se encontró
                if fuzzy_match:
                    resultado_fuzzy = fuzzy_validate(
                        item_limpio, list(mapping.keys()), limit=1
                    )
                    if resultado_fuzzy:
                        resultado_limpio = eliminar_acentos(resultado_fuzzy).upper()
                        resultado = mapping[resultado_limpio]
            
            # Si no se encontró resultado, manejar error
            if resultado is None:
                resultado = assert_error(
                    on_error,
                    evaluated=item_limpio,
                    message=error_message,
                )
            
            # Aplicar normalización si se requiere
            if resultado and normalize:
                return eliminar_acentos(resultado).strip().upper()
            else:
                return resultado

    @classmethod
    def validate_departamento(
        cls,
        departamento: str | SeriesLike,
        normalize: bool = False,
        fuzzy_match: bool = True,
        on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
    ) -> str | SeriesLike:
        return cls._validate_generic(
            departamento, "departamentos", normalize, fuzzy_match, on_error
        )

    @classmethod
    def validate_provincia(
        cls,
        provincia: str | SeriesLike,
        normalize: bool = False,
        fuzzy_match: bool = True,
        on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
    ) -> str | SeriesLike:
        return cls._validate_generic(
            provincia, "provincias", normalize, fuzzy_match, on_error
        )

    @classmethod
    def validate_distrito(
        cls,
        distrito: str | SeriesLike,
        normalize: bool = False,
        fuzzy_match: bool = True,
        on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
    ) -> str | SeriesLike:
        return cls._validate_generic(
            distrito, "distritos", normalize, fuzzy_match, on_error
        )
