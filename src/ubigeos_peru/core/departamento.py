from typing import Literal
from ._utils import (
    eliminar_acentos,
    is_series_like,
    reconstruct_like,
    assert_error,
    SeriesLike,
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
        nombre_departamento: str | SeriesLike,
        normalize: bool = False,
        on_error: Literal["raise", "ignore", "capitalize"] = "raise",
    ) -> str | SeriesLike:
        cls._resources.cargar_diccionario("equivalencias")
        mapping = cls._resources._loaded["equivalencias"]["departamentos"]

        # ---------------------- Input: Series-like ----------------------
        if is_series_like(nombre_departamento):
            mapping: dict[str, str] = (
                {k: eliminar_acentos(v).upper() for k, v in mapping.items()}
                if normalize
                else mapping
            )
            out = []
            for item in nombre_departamento:
                if not isinstance(item, str):
                    try:
                        str(item)
                    except TypeError:
                        raise TypeError(
                            f"No se permiten otros tipos de datos que no sean str, se insertó {type(item)}"
                        )

                departamento = eliminar_acentos(item).strip().upper()
                try:
                    out.append(mapping[departamento])
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

            return reconstruct_like(nombre_departamento, out)
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
            if not isinstance(nombre_departamento, str):
                try:
                    str(nombre_departamento)
                except TypeError:
                    raise TypeError(
                        f"No se permiten otros tipos de datos que no sean str, se insertó {type(nombre_departamento)}"
                    )

            departamento = eliminar_acentos(nombre_departamento).strip().upper()
            try:
                resultado = mapping[departamento]
            except KeyError:
                if departamento == "REGION LIMA":
                    return "Lima Región"
                if on_error == "raise":
                    raise KeyError(
                        f"No se ha encontrado el departamento {nombre_departamento}"
                    )
                elif on_error == "ignore":
                    resultado = nombre_departamento
                elif on_error == "capitalize":
                    resultado = nombre_departamento.capitalize()
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
        nombre_ubicacion: str | SeriesLike,
        normalize: bool = False,
        on_error: Literal["raise", "ignore", "capitalize"] = "raise",
    ) -> str | SeriesLike:
        cls._resources.cargar_diccionario("equivalencias")
        mapping = cls._resources._loaded["equivalencias"]

        if is_series_like(nombre_ubicacion):
            mapping: dict[str, str] = (
                {k: eliminar_acentos(v).upper() for k, v in mapping.items()}
                if normalize
                else mapping
            )

            out = []
            for item in nombre_ubicacion:
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
            return reconstruct_like(nombre_ubicacion, out)

        else:
            nombre_ubicacion = eliminar_acentos(nombre_ubicacion).strip().upper()
            try:
                resultado = mapping["departamentos"][nombre_ubicacion]
            except KeyError:
                try:
                    resultado = mapping["provincias"][nombre_ubicacion]
                except KeyError:
                    try:
                        resultado = mapping["distritos"][nombre_ubicacion]
                    except KeyError:
                        resultado = assert_error(
                            on_error,
                            nombre_ubicacion,
                            message="No se encontró el lugar {} en la base de datos de departamentos, provincias o distritos",
                        )

            if not normalize:
                return resultado
            else:
                return eliminar_acentos(resultado).upper()
