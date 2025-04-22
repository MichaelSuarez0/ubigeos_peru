import os
import json
from re import A
import pandas as pd
from icecream import ic
from typing import Literal
from ..resources import Departamentos, Provincias, Distritos

script_dir = os.path.dirname(__file__)
databases = os.path.join(script_dir, "..", "databases", "otros")

departamentos_path = os.path.join(databases, "ubigeo_peru_2016_departamentos.csv")
provincias_path = os.path.join(databases, "ubigeo_peru_2016_provincias.csv")
distritos_path = os.path.join(databases, "ubigeo_peru_2016_distritos.csv")

import unicodedata

def eliminar_acentos(texto: str)-> str:
    # Normaliza el texto en la forma NFKD (descompone los caracteres acentuados)
    texto_normalizado = unicodedata.normalize('NFKD', texto)
    # Filtra solo los caracteres que no son signos diacríticos
    texto_sin_acentos = ''.join(c for c in texto_normalizado if not unicodedata.combining(c))
    return texto_sin_acentos


# TODO: Guardar los datos de ubigeos en dataclasses y ponerlas en Ubigeo como dependencias con lazy loading
# TODO: Los métodos, por ejemplo departamento, deberían aceptar o dos caracteres o seis 
# TODO: También colocar métodos para exportar las bases de datos
class Ubigeo:
    departamentos = None
    provincias = None
    distritos = None
    otros = None


    def _load_database(self):
        pass

    @classmethod
    def get_departamento(cls, codigo: str | int, institucion: Literal["inei", "reniec", "sunat"] = "inei", quitar_acentos: bool = False):
        pass

    @classmethod
    def get_provincia(cls, codigo: str | int, institucion: Literal["inei", "reniec" "sunat"] = "inei", quitar_acentos: bool = False):
        pass

    @classmethod
    def get_distrito(cls, codigo: str | int, institucion: Literal["inei", "reniec", "sunat"] = "inei", quitar_acentos: bool = False):
        pass

    @classmethod
    def get_macrorregion(cls, codigo_o_departamento: str | int, institucion: Literal["inei", "reniec", "sunat"] = "inei", quitar_acentos: bool = False):
        pass

    @classmethod
    def get_ubigeo(cls, ubicacion: str, level: Literal["departamento", "distrito", "provincia"] = "departamento", institucion: Literal["inei", "reniec", "sunat"] = "inei", quitar_acentos: bool = False):
        pass

    @classmethod
    def get_otros(cls, codigo_o_departamento: str | int, key: Literal["capital", "superficie"]):
        pass

        
    @classmethod
    def normalize_departamento(cls, nombre_departamento: str) -> str:
        """Normaliza y valida el nombre del departamento"""
        for dpto in cls._DATA.keys():
            if eliminar_acentos(nombre_departamento).strip().lower() == eliminar_acentos(dpto).strip().lower():
                return dpto
        
        raise ValueError(
            f"Departamento no encontrado: '{nombre_departamento}'. "
            f"Opciones válidas: {list(cls._DATA.keys())}"
        )




Ubigeo.get_distrito("0102", institucion="")