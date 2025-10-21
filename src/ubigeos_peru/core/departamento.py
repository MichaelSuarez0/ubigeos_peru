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
        on_error: Literal["raise", "ignore", "capitalize"] = "raise",
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
                if not isinstance(item, str):
                    try:
                        str(item)
                    except TypeError:
                        raise TypeError(
                            f"No se permiten otros tipos de datos que no sean str, se insertó {type(item)}"
                        )

                dep_limpio = eliminar_acentos(item).strip().upper()
                try:
                    out.append(mapping[dep_limpio])
                except KeyError:
                    if on_error == "raise":
                        raise KeyError(f"No se ha encontrado el departamento {item}")
                    elif on_error == "capitalize":
                        item = item.capitalize()
                    elif on_error == "ignore":
                        pass
                    else:
                        raise ValueError(
                            'El arg "on_error" debe ser uno de los siguientes: "raise", "ignore", "capitalize"'
                        )
                    out.append(item)

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
                if dep_limpio == "REGION LIMA":
                    return "Lima Región"
                if on_error == "raise":
                    raise KeyError(
                        f"No se ha encontrado el departamento {departamento}"
                    )
                elif on_error == "ignore":
                    resultado = departamento
                elif on_error == "capitalize":
                    resultado = departamento.capitalize()
                else:
                    raise ValueError(
                        'El arg "on_error" debe ser uno de los siguientes: "raise", "ignore", "capitalize"'
                    )

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
        on_error: Literal["raise", "ignore", "capitalize"] = "raise",
    ) -> str | SeriesLike:
        cls._resources.cargar_diccionario("equivalencias")
        mapping = cls._resources._loaded["equivalencias"]

        if is_series_like(ubicacion):
            mapping: dict[str, str] = (
                {k: eliminar_acentos(v).upper() for k, v in mapping.items()}
                if normalize
                else mapping
            )

            out = []
            for item in ubicacion:
                item = eliminar_acentos(item).strip().upper()
                try:
                    resultado = mapping["departamentos"][item]
                except KeyError:
                    try:
                        resultado = mapping["provincias"][item]
                    except KeyError:
                        try:
                            resultado = mapping["distritos"][item]
                        except KeyError:
                            if on_error == "raise":
                                raise KeyError(
                                    f"No se encontró el lugar {item} en la base de datos de departamentos, provincias o distritos"
                                )
                            elif on_error == "ignore":
                                resultado = item
                            elif on_error == "capitalize":
                                resultado = item.capitalize()
                            else:
                                raise ValueError(
                                    'El arg "on_error" debe ser uno de los siguientes: "raise", "ignore", "capitalize"'
                                )

                out.append(resultado)
            return reconstruct_like(ubicacion, out)

        else:
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
                            message="No se encontró el lugar {} en la base de datos de departamentos, provincias o distritos",
                        )

            if not normalize:
                return resultado
            else:
                return eliminar_acentos(resultado).upper()
