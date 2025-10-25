from typing import Literal

from ._utils import (
    SeriesLike,
    assert_error,
    eliminar_acentos,
    is_series_like,
    reconstruct_like,
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
                    resultado = assert_error(
                        on_error,
                        evaluated=dep_limpio,
                        message="No se ha encontrado del departamento {}",
                    )
                    out.append(resultado)

            return reconstruct_like(departamento, out)
        # # ---------------------- Input: Expr-like ----------------------
        # module = getattr(type(nombre_departamento), "__module__", "")
        # name = getattr(type(nombre_departamento), "__name__", "")
        # if "polars" in module and name == "Expr":
        #     # Lazy-safe: aplicar por batches
        #     return nombre_departamento.map_batches(
        #         lambda s: cls.validate_departamento(s, normalize=normalize, on_error=on_error)
        #     )
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
                # if dep_limpio == "REGION LIMA":
                #     return "Lima Región"
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

    # TODO: Unhasable type Series when passing series
    @classmethod
    def validate_ubicacion(
        cls,
        ubicacion: str | SeriesLike,
        normalize: bool = False,
        on_error: Literal["raise", "warn", "ignore", "capitalize", "coerce"] = "raise",
    ) -> str | SeriesLike:
        cls._resources.cargar_diccionario("equivalencias")
        mapping = cls._resources._loaded["equivalencias"]

        if is_series_like(ubicacion):
            # Normalizar cada sub-diccionario si es necesario
            if normalize:
                mapping_norm = {
                    "departamentos": {k: eliminar_acentos(v).upper() for k, v in mapping["departamentos"].items()},
                    "provincias": {k: eliminar_acentos(v).upper() for k, v in mapping["provincias"].items()},
                    "distritos": {k: eliminar_acentos(v).upper() for k, v in mapping["distritos"].items()}
                }
            else:
                mapping_norm = mapping

            out = []
            for item in ubicacion:
                if not isinstance(item, str) or item.isdigit():
                    raise TypeError(
                    f"No se permiten otros tipos de datos que no sean str, se insertó {type(item)}"
                )

                item = eliminar_acentos(item).strip().upper()
                try:
                    resultado = mapping_norm["departamentos"][item]
                except KeyError:
                    try:
                        resultado = mapping_norm["provincias"][item]
                    except KeyError:
                        try:
                            resultado = mapping_norm["distritos"][item]
                        except KeyError:
                            resultado = assert_error(
                                on_error,
                                evaluated=item,
                                message="No se encontró el lugar {} en la base de datos de provincias o distritos",
                            )

                out.append(resultado)

            return reconstruct_like(ubicacion, out)

        else:
            if not isinstance(ubicacion, str) or ubicacion.isdigit():
                raise TypeError(
                    f"No se permiten otros tipos de datos que no sean str, se insertó {type(ubicacion)}"
                )
            ubicacion = eliminar_acentos(ubicacion).strip().upper()
            try:
                resultado = mapping["departamentos"][ubicacion]
            except KeyError:
                try:
                    resultado = mapping["provincias"][ubicacion]
                except KeyError:
                    try:
                        resultado = mapping["distritos"][ubicacion]
                    except KeyError:
                        resultado = assert_error(
                            on_error,
                            ubicacion,
                            message="No se encontró el lugar {} en la base de datos de provincias o distritos",
                        )
                        return resultado

            if not normalize:
                return resultado
            else:
                return eliminar_acentos(resultado).upper()
