import os
from typing import Literal
import orjson
from _functions import update_to_readable, update_to_resources

# TODO: Agregar:
# Yauri (Espinar) (distritos)
# TODO: Por agregar: Región lima para departamentos
equivalencias = {
    'departamentos':{
        'CUZCO': 'Cusco'
    },
    'provincias':{
        'CUZCO': 'Cusco'
    },
    'distritos':{
        'COTABAMBA': 'Cotabambas',
        'SAN JERONIMO DE TUNAN': 'San Jerónimo de Tunán',
        'SAN AGUSTIN' : 'San Agustín de Cajas',
        'CUZCO': 'Cusco'
    }}

distritos = {
    'inei': {
        '070107': 'Mi Perú',
        '080801': 'Yauri',
    },
    'reniec' : {
        '240107': 'Mi Perú',
        '070801': 'Yauri',
    },
    'sunat': {
        "120124": "Pariahuanca",
        "080807": "Suyckutambo",
        "080903": "Huayopata",
        "080905": "Ocobamba",
        '080801': 'Yauri',
        }
}

def update_all(entries: dict, resource_name: Literal["departamentos", "distritos", "equivalencias", "inverted", "macrorregiones", "otros", "provincias"]):
    resources_names = ["departamentos", "distritos", "provincias", "equivalencias", "inverted", "macrorregiones", "otros"]
    if resource_name not in resources_names:
        raise TypeError(f"Entries must have any of following names: {resources_names}")
    update_to_resources(entries, resource_name)
    update_to_readable(entries, resource_name)
    if resource_name in resources_names[:3]:
        from inverted_creation import inverted_creation
        inverted_creation()


if __name__ == "__main__":
    update_all(distritos, "distritos")
