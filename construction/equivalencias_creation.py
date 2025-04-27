import os
import pandas as pd
import unicodedata
from collections import defaultdict
from _functions import DATABASES_PATH, RESOURCES_PATH, RESOURCES_READABLE_PATH
from _functions import write_to_json, write_to_readable

base = "ubigeo_peru_2016_{}.csv"


def eliminar_acentos(texto: str)-> str:
    texto_normalizado = unicodedata.normalize('NFKD', texto)
    texto_sin_acentos = ''.join(c for c in texto_normalizado if not unicodedata.combining(c))
    return texto_sin_acentos

def crear_diccionario(df: pd.DataFrame)-> dict:
    final_dict = defaultdict(dict)
    for nombre in list(df["name"]):
        final_dict[eliminar_acentos(nombre).upper().strip()] = nombre.strip()
    
    return dict(final_dict)


def equivalencias_creation():
    departamentos = pd.read_csv(os.path.join(DATABASES_PATH, base.format("departamentos")), encoding='utf-8', dtype=str)
    provincias = pd.read_csv(os.path.join(DATABASES_PATH, base.format("provincias")), encoding='utf-8', dtype=str)
    distritos = pd.read_csv(os.path.join(DATABASES_PATH, base.format("distritos")), encoding='utf-8', dtype=str)

    dep_dict = crear_diccionario(departamentos)
    prov_dict = crear_diccionario(provincias)
    dist_dict = crear_diccionario(distritos)

    equivalencias = defaultdict(dict)
    equivalencias["departamentos"] = dep_dict
    equivalencias["provincias"] = prov_dict
    equivalencias["distritos"] = dist_dict
    equivalencias = dict(equivalencias)

    write_to_json(equivalencias, "equivalencias")
    write_to_readable(equivalencias, "equivalencias")
        

if __name__ == "__main__":
    equivalencias_creation()