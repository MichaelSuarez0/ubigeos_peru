from typing import Literal
from .utils import eliminar_acentos
from .resource_manager import ResourceManager


class Departamento:
    _resources = ResourceManager()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Departamento, cls).__new__(cls)
        return cls._instance

    @classmethod
    def validate_departamento(
        cls,
        nombre_departamento: str,
        normalize: bool = False,
        on_error: Literal["raise", "ignore", "capitalize"] = "raise",
    ) -> str:
        
        cls._resources._load_resource_if_needed("equivalencias")

        # if cls._EQUIVALENCIAS is None:
        #     raise RuntimeError("No se pudieron cargar las equivalencias")
        if not isinstance(nombre_departamento, str):
            try:
                str(nombre_departamento)
            except TypeError:
                raise TypeError(
                    f"No se permiten otros tipos de datos que no sean str, se insertó {type(nombre_departamento)}"
                )

        departamento = eliminar_acentos(nombre_departamento).strip().upper()
        try:
            resultado = cls._resources._EQUIVALENCIAS["departamentos"][departamento]
        except KeyError:
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

    @classmethod
    def validate_ubicacion(
        cls,
        nombre_ubicacion: str,
        normalize: bool = False,
        on_error: Literal["raise", "ignore", "capitalize"] = "raise",
    ) -> str:
        
        cls._resources._load_resource_if_needed("equivalencias")
        nombre_ubicacion = eliminar_acentos(nombre_ubicacion).strip().upper()
        try:
            resultado = cls._resources._EQUIVALENCIAS["departamentos"][nombre_ubicacion]
        except KeyError:
            try:
                resultado = cls._resources._EQUIVALENCIAS["provincias"][
                    nombre_ubicacion
                ]
            except KeyError:
                try:
                    resultado = cls._resources._EQUIVALENCIAS["distritos"][
                        nombre_ubicacion
                    ]
                except KeyError:
                    if on_error == "raise":
                        raise KeyError(
                            f"No se encontró el lugar {nombre_ubicacion} en la base de datos de departamentos, provincias o distritos"
                        )
                    elif on_error == "ignore":
                        resultado = nombre_ubicacion
                    elif on_error == "capitalize":
                        resultado = nombre_ubicacion.capitalize()
                    else:
                        raise ValueError(
                            'El arg "on_error" debe ser uno de los siguientes: "raise", "ignore", "capitalize"'
                        )

        if not normalize:
            return resultado
        else:
            return eliminar_acentos(resultado).upper()
