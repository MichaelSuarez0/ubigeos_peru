from typing import Literal

import narwhals as nw
from narwhals.typing import IntoSeriesT

from ._utils import (
    assert_error,
    eliminar_acentos,
    fuzzy_validate,
)
from .resource_manager import ResourceManager


class Validations:
    _resources = ResourceManager()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Validations, cls).__new__(cls)
        return cls._instance

    # ------------------------------------------------------------------
    # VALIDATE GENERIC - SERIES
    # ------------------------------------------------------------------

    @staticmethod
    @nw.narwhalify(
        series_only=True,
        eager_only=True,
    )
    def _validate_generic_series(
        value: nw.Series,
        mapping: dict[str, str],
        error_message: str,
        fuzzy_match: bool,
        institucion: str,
        on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"],
    ) -> nw.Series:
        resultado = []
        fuzzy_matched = set()

        for item in value:
            if not isinstance(item, str) or item.isdigit():
                raise TypeError(
                    f"No se permiten otros tipos de datos que no sean str, se insertó {type(item)}"
                )

            item_limpio = eliminar_acentos(item).strip().upper()

            # Intentar búsqueda directa
            try:
                resultado.append(mapping[item_limpio])
                continue
            except KeyError:
                pass

            # Intentar fuzzy matching
            if fuzzy_match:
                match = fuzzy_validate(item_limpio, list(mapping.keys()), limit=1)
                if match:
                    match_limpio = eliminar_acentos(match).upper()
                    resultado.append(mapping[match_limpio])
                    fuzzy_matched.add((item_limpio, match_limpio))
                    continue

            # Manejo de errores
            valor_error = assert_error(
                on_error,
                evaluated=item_limpio,
                message=error_message,
                institucion=institucion,
            )
            resultado.append(valor_error)

        # Imprimir fuzzy matches
        if fuzzy_matched:
            print("Los siguientes valores fueron obtenidos con fuzzy match. Validar:")
            for original, matched in fuzzy_matched:
                print(f"{original} -> {matched}")

        return nw.new_series(
            name=value.name,
            values=resultado,
            backend=value.implementation,
        )

    # ------------------------------------------------------------------
    # VALIDATE GENERIC
    # ------------------------------------------------------------------

    @classmethod
    def _validate_generic(
        cls,
        value: str | IntoSeriesT,
        entity_type: Literal["departamentos", "provincias", "distritos"],
        institucion: str,
        normalize: bool = False,
        fuzzy_match: bool = True,
        on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
    ) -> str | IntoSeriesT:
        """
        Función genérica para validar departamentos, provincias o distritos.

        Parameters
        ----------
        value : str | IntoSeriesT
            Valor o serie de valores a validar.
        entity_type : {'departamentos', 'provincias', 'distritos'}
            Tipo de entidad a validar.
        institucion : str
            Institución de referencia, usada en el mensaje de error.
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
        str | IntoSeriesT
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

        # ------------------------ Input: Singular ------------------------
        if isinstance(value, str):
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
                    institucion=institucion,
                )

            # Aplicar normalización si se requiere
            if resultado and normalize:
                return eliminar_acentos(resultado).strip().upper()
            else:
                return resultado

        # ---------------------- Input: Series-like ----------------------
        mapping_series = (
            {k: eliminar_acentos(v).upper() for k, v in mapping.items()}
            if normalize
            else mapping
        )

        return cls._validate_generic_series(
            value,
            mapping=mapping_series,
            error_message=error_message,
            fuzzy_match=fuzzy_match,
            institucion=institucion,
            on_error=on_error,
        )

    @classmethod
    def validate_departamento(
        cls,
        departamento: str | IntoSeriesT,
        institucion: str = "inei",
        normalize: bool = False,
        fuzzy_match: bool = True,
        on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
    ) -> str | IntoSeriesT:
        return cls._validate_generic(
            value=departamento,
            entity_type="departamentos",
            institucion=institucion,
            normalize=normalize,
            fuzzy_match=fuzzy_match,
            on_error=on_error,
        )

    @classmethod
    def validate_provincia(
        cls,
        provincia: str | IntoSeriesT,
        institucion: str = "inei",
        normalize: bool = False,
        fuzzy_match: bool = True,
        on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
    ) -> str | IntoSeriesT:
        return cls._validate_generic(
            value=provincia,
            entity_type="provincias",
            institucion=institucion,
            normalize=normalize,
            fuzzy_match=fuzzy_match,
            on_error=on_error,
        )

    @classmethod
    def validate_distrito(
        cls,
        distrito: str | IntoSeriesT,
        institucion: str = "inei",
        normalize: bool = False,
        fuzzy_match: bool = True,
        on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
    ) -> str | IntoSeriesT:
        return cls._validate_generic(
            value=distrito,
            entity_type="distritos",
            institucion=institucion,
            normalize=normalize,
            fuzzy_match=fuzzy_match,
            on_error=on_error,
        )
