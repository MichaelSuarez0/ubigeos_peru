import os
from typing import Literal
import unicodedata
from ..resources import DEPARTAMENTOS, DISTRITOS, PROVINCIAS, MACRORREGIONES, EQUIVALENCIAS

script_dir = os.path.dirname(__file__)
databases = os.path.join(script_dir, "..", "databases", "otros")


def eliminar_acentos(texto: str)-> str:
    texto_normalizado = unicodedata.normalize('NFKD', texto)
    texto_sin_acentos = ''.join(c for c in texto_normalizado if not unicodedata.combining(c))
    return texto_sin_acentos


# TODO: Guardar los datos de ubigeos en dataclasses y ponerlas en Ubigeo como dependencias con lazy loading
# TODO: También colocar métodos para exportar las bases de datos
class Ubigeo:
    _departamentos: dict = DEPARTAMENTOS
    _provincias: dict = PROVINCIAS
    _distritos: dict = DISTRITOS
    _macrorregiones: dict = MACRORREGIONES
    _equivalencias: dict = EQUIVALENCIAS
    _otros = None

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
    
    @classmethod
    def normalize_departamento(cls, nombre_departamento: str) -> str:
        """"""
        nombre_departamento = eliminar_acentos(nombre_departamento).strip().upper()
        try:
            departamento = cls._equivalencias["departamentos"][nombre_departamento]
        except KeyError:
            raise ValueError(f"No se ha encontrado el departamento {nombre_departamento}")
        
        return departamento
    
    @classmethod
    def normalize_ubicacion(cls, nombre_ubicacion: str, ignore_errors: bool = False) -> str:
        """"""
        nombre_ubicacion = eliminar_acentos(nombre_ubicacion).strip().upper()
        try:
            resultado = cls._equivalencias["departamentos"][nombre_ubicacion]
        except KeyError:
            try:
                resultado = cls._equivalencias["provincias"][nombre_ubicacion]
            except KeyError:
                try:
                    resultado = cls._equivalencias["distritos"][nombre_ubicacion]
                except KeyError:
                    if not ignore_errors:
                        raise ValueError(f"No se encontró el lugar {nombre_ubicacion} en la base de datos de departamentos, provincias o distritos")
                    else:
                        resultado = nombre_ubicacion
                    
        return resultado

    @classmethod
    def get_departamento(cls, codigo: str | int, institucion: Literal["inei", "reniec", "sunat"] = "inei", normalize: bool = True):
        codigo = cls._validate_codigo(codigo)
        
        result = cls._departamentos[institucion][codigo[-2:]]

        if normalize:
            return eliminar_acentos(result).upper()
        else:
            return result


    @classmethod
    def get_provincia(cls, codigo: str | int, institucion: Literal["inei", "reniec" "sunat"] = "inei", normalize: bool = True):
        codigo = cls._validate_codigo(codigo)
        if len(codigo) < 4:
            raise ValueError("No se aceptan ubigeos con menos de 4 caracteres para provincias")

        result = cls._provincias[institucion][codigo[-4:]]

        if normalize:
            return eliminar_acentos(result).upper()
        else:
            return result
        

    @classmethod
    def get_distrito(cls, codigo: str | int, institucion: Literal["inei", "reniec", "sunat"] = "inei", normalize: bool = True):
        codigo = cls._validate_codigo(codigo)
        if len(codigo) != 6:
            raise ValueError("No se aceptan ubigeos que no tengan exactamente 6 caracteres para distritos")

        result = cls._distritos[institucion][codigo]

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
        
        return eliminar_acentos(cls._macrorregiones[institucion][departamento])

    @classmethod
    def get_ubigeo(cls, lugar: str, level: Literal["departamento", "distrito", "provincia"] = "departamento", institucion: Literal["inei", "reniec", "sunat"] = "inei", normalize: bool = False):
        pass

    @classmethod
    def get_otros(cls, codigo_o_departamento: str | int, key: Literal["capital", "superficie"]):
        pass

    