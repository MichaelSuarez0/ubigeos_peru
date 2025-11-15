from typing import Literal

from ._utils import (
    SeriesLike,
    assert_error,
    eliminar_acentos,
    is_series_like,
    reconstruct_like,
    fuzzy_validate
)
from .resource_manager import ResourceManager



class Departamento:
    _resources = ResourceManager()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Departamento, cls).__new__(cls)
        return cls._instance

    # TODO: REGIÓN LIMA DEBE SER LIMA REGIÓN
    # TODO: EN LA DB DE MACRORREGIONES FALTA LIMA METROPOLITANA: LIMA METROPOLITANA
    @classmethod
    def validate_departamento(
        cls,
        departamento: str | SeriesLike,
        normalize: bool = False,
        fuzzy_match: bool = True,
        on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
    ) -> str | SeriesLike:
        cls._resources.cargar_diccionario("equivalencias")
        mapping = cls._resources._loaded["equivalencias"]["departamentos"]

        # ---------------------- Input: Series-like ----------------------
        if is_series_like(departamento):
            mapping: dict[str, str] = (
                {k: eliminar_acentos(v).upper() for k, v in mapping.items()}
                if normalize
                else mapping
            )
            out = []
            for item in departamento:
                if not isinstance(item, str) or item.isdigit():
                    raise TypeError(
                        f"No se permiten otros tipos de datos que no sean str, se insertó {type(item)}"
                    )

                dep_limpio = eliminar_acentos(item).strip().upper()
                try:
                    out.append(mapping[dep_limpio])
                except KeyError:
                    if fuzzy_match:
                        resultado = fuzzy_validate(
                            dep_limpio,
                            list(mapping.keys()),
                            limit=1
                        )
                        out.append(resultado)
                        continue
                    resultado = assert_error(
                        on_error,
                        evaluated=dep_limpio,
                        message="No se ha encontrado del departamento {}",
                    )
                    out.append(resultado)

            return reconstruct_like(departamento, out)
        else:
            # ------------------------ Input: Singular ------------------------
            if not isinstance(departamento, str):
                try:
                    str(departamento)
                except TypeError:
                    raise TypeError(
                        f"No se permiten otros tipos de datos que no sean str, se insertó {type(departamento)}"
                    )

            dep_limpio = eliminar_acentos(departamento).strip().upper()
            try:
                resultado = mapping[dep_limpio]
            except KeyError:
                resultado = assert_error(
                    on_error,
                    evaluated=dep_limpio,
                    message="No se ha encontrado del departamento {}",
                )
                return resultado

            if not normalize:
                return resultado
            else:
                return eliminar_acentos(resultado).strip().upper()

    @classmethod
    def validate_provincia(
        cls,
        provincia: str | SeriesLike,
        normalize: bool = False,
        fuzzy_match: bool = True,
        on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
    ) -> str | SeriesLike:
        cls._resources.cargar_diccionario("equivalencias")
        mapping = cls._resources._loaded["equivalencias"]["provincias"]

        # ---------------------- Input: Series-like ----------------------
        if is_series_like(provincia):
            mapping: dict[str, str] = (
                {k: eliminar_acentos(v).upper() for k, v in mapping.items()}
                if normalize
                else mapping
            )
            out = []
            for item in provincia:
                if not isinstance(item, str) or item.isdigit():
                    raise TypeError(
                        f"No se permiten otros tipos de datos que no sean str, se insertó {type(item)}"
                    )

                prov_limpio = eliminar_acentos(item).strip().upper()
                try:
                    out.append(mapping[prov_limpio])
                except KeyError:
                    if fuzzy_match:
                        resultado = fuzzy_validate(
                            prov_limpio,
                            list(mapping.keys()),
                            limit=1
                        )
                        out.append(resultado)
                        continue
                    resultado = assert_error(
                        on_error,
                        evaluated=prov_limpio,
                        message="No se ha encontrado la provincia {}",
                    )
                    out.append(resultado)

            return reconstruct_like(provincia, out)
        else:
            # ------------------------ Input: Singular ------------------------
            if not isinstance(provincia, str):
                try:
                    str(provincia)
                except TypeError:
                    raise TypeError(
                        f"No se permiten otros tipos de datos que no sean str, se insertó {type(provincia)}"
                    )

            prov_limpio = eliminar_acentos(provincia).strip().upper()
            try:
                resultado = mapping[prov_limpio]
            except KeyError:
                resultado = assert_error(
                    on_error,
                    evaluated=prov_limpio,
                    message="No se ha encontrado la provincia {}",
                )
                return resultado

            if not normalize:
                return resultado
            else:
                return eliminar_acentos(resultado).strip().upper()

    @classmethod
    def validate_distrito(
        cls,
        distrito: str | SeriesLike,
        normalize: bool = False,
        fuzzy_match: bool = True,
        on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
    ) -> str | SeriesLike:
        cls._resources.cargar_diccionario("equivalencias")
        mapping = cls._resources._loaded["equivalencias"]["distritos"]

        # ---------------------- Input: Series-like ----------------------
        if is_series_like(distrito):
            mapping: dict[str, str] = (
                {k: eliminar_acentos(v).upper() for k, v in mapping.items()}
                if normalize
                else mapping
            )
            out = []
            for item in distrito:
                if not isinstance(item, str) or item.isdigit():
                    raise TypeError(
                        f"No se permiten otros tipos de datos que no sean str, se insertó {type(item)}"
                    )

                dist_limpio = eliminar_acentos(item).strip().upper()
                try:
                    out.append(mapping[dist_limpio])
                except KeyError:
                    if fuzzy_match:
                        resultado = fuzzy_validate(
                            dist_limpio,
                            list(mapping.keys()),
                            limit=1
                        )
                        out.append(resultado)
                        continue
                    resultado = assert_error(
                        on_error,
                        evaluated=dist_limpio,
                        message="No se ha encontrado el distrito {}",
                    )
                    out.append(resultado)

            return reconstruct_like(distrito, out)
        else:
            # ------------------------ Input: Singular ------------------------
            if not isinstance(distrito, str):
                try:
                    str(distrito)
                except TypeError:
                    raise TypeError(
                        f"No se permiten otros tipos de datos que no sean str, se insertó {type(distrito)}"
                    )

            dist_limpio = eliminar_acentos(distrito).strip().upper()
            try:
                resultado = mapping[dist_limpio]
            except KeyError:
                resultado = assert_error(
                    on_error,
                    evaluated=dist_limpio,
                    message="No se ha encontrado el distrito {}",
                )
                return resultado

            if not normalize:
                return resultado
            else:
                return eliminar_acentos(resultado).strip().upper()
