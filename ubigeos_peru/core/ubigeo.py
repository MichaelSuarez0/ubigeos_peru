import os
from typing import Literal
from ..resources import DEPARTAMENTOS, DISTRITOS, PROVINCIAS, MACRORREGIONES

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
    departamentos: dict = DEPARTAMENTOS
    provincias: dict = PROVINCIAS
    distritos: dict = DISTRITOS
    macrorregiones: dict = MACRORREGIONES
    otros = None

    def _load_database(self):
        pass

    @classmethod
    def _validate_codigo(cls, codigo: str | int) -> str:
        if isinstance(codigo, int):
            codigo = str(codigo)
            
        if isinstance(codigo, str):
            if len(codigo) == 1:
                codigo = codigo.zfill(2)
            elif len(codigo) == 5:
                codigo = codigo.zfill(6)
            elif len(codigo) > 6:
                raise ValueError("No se aceptan ubigeos con más de 6 caracteres")
        else:
            raise ValueError("No se aceptan valores que no sean string o integers")
        
        return codigo
    
    # @classmethod
    # def _normalize_departamento(cls, nombre_departamento: str) -> str:
    #     """Normaliza y valida el nombre del departamento"""
    #     for dpto in cls._DATA.keys():
    #         if eliminar_acentos(nombre_departamento).strip().lower() == eliminar_acentos(dpto).strip().lower():
    #             return dpto
        
    #     raise ValueError(
    #         f"Departamento no encontrado: '{nombre_departamento}'. "
    #         f"Opciones válidas: {list(cls._DATA.keys())}"
    #     )

    @classmethod
    def get_departamento(cls, codigo: str | int, institucion: Literal["inei", "reniec", "sunat"] = "inei", normalize: bool = True):
        codigo = cls._validate_codigo(codigo)
        
        result = cls.departamentos[institucion][codigo[-2:]]

        if normalize:
            return eliminar_acentos(result).upper()
        else:
            return result


    @classmethod
    def get_provincia(cls, codigo: str | int, institucion: Literal["inei", "reniec" "sunat"] = "inei", normalize: bool = True):
        codigo = cls._validate_codigo(codigo)
        if len(codigo) < 4:
            raise ValueError("No se aceptan ubigeos con menos de 4 caracteres para provincias")

        result = cls.provincias[institucion][codigo[-4:]]

        if normalize:
            return eliminar_acentos(result).upper()
        else:
            return result
        

    @classmethod
    def get_distrito(cls, codigo: str | int, institucion: Literal["inei", "reniec", "sunat"] = "inei", normalize: bool = True):
        codigo = cls._validate_codigo(codigo)
        if len(codigo) != 6:
            raise ValueError("No se aceptan ubigeos que no tengan exactamente 6 caracteres para distritos")

        result = cls.distritos[institucion][codigo]

        if normalize:
            return eliminar_acentos(result).upper()
        else:
            return result

    # TODO: Corregir mayúsculas en resources
    @classmethod
    def get_macrorregion(cls, codigo_o_departamento: str | int, institucion: Literal["inei", "minsa", "ceplan"] = "inei", normalize: bool = True):
        if isinstance(codigo_o_departamento, str) and codigo_o_departamento[0] not in list(range(0, 10)):
            departamento = codigo_o_departamento
        
        departamento = eliminar_acentos(departamento).lower().strip()
        
        return eliminar_acentos(cls.macrorregiones[institucion][departamento])

    @classmethod
    def get_ubigeo(cls, lugar: str, level: Literal["departamento", "distrito", "provincia"] = "departamento", institucion: Literal["inei", "reniec", "sunat"] = "inei", normalize: bool = False):
        pass

    @classmethod
    def get_otros(cls, codigo_o_departamento: str | int, key: Literal["capital", "superficie"]):
        pass

    