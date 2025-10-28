from pathlib import Path
from typing import Literal

import polars as pl
from _utils import DATABASES_PATH, update_to_readable, update_to_resources

columns = [
    "Ubigeo",
    "Provincia y Distrito",
    "Dispositivo Legal de Creación del Distrito",
    "Nombre",
    "Categoría",
    "Altitud (msnm.)",
    "Longitud Oeste",
    "Latitud Sur",
    "Población Total Proyectada al 30/06/2025",
    "Nombre del Alcalde",
    "Dirección",
    "DDN",
    "Teléfonos",
    "Correo Electrónico",
]

DB_INEI = DATABASES_PATH / "ubigeo_inei_2025.csv"
DB_RENIEC = DATABASES_PATH / "ubigeo_reniec_2019.csv"

def crear_provincias(institucion: Literal["inei", "reniec"]):
    provincias = {}
    final_dict = {}

    if institucion == "inei":
        DB = DB_INEI
    elif institucion == "reniec":
        DB = DB_RENIEC

    df = pl.read_csv(
        DB,
        separator=";",
        schema_overrides={"ubigeo": pl.Utf8}
    )

    unique = set()
    for row in df.iter_rows(named=True):
        ubigeo = row["ubigeo"][:4]
        if ubigeo not in unique:
            unique.add(ubigeo)
            provincias[ubigeo] = row["provincia"]

    final_dict[institucion] = provincias
    update_to_readable(final_dict, variable_name="provincias")
    update_to_resources(final_dict, variable_name="provincias")
    return final_dict

def crear_distritos(institucion: Literal["inei", "reniec"]):
    provincias = {}
    final_dict = {}

    if institucion == "inei":
        DB = DB_INEI
    elif institucion == "reniec":
        DB = DB_RENIEC

    df = pl.read_csv(
        DB,
        separator=";",
        schema_overrides={"ubigeo": pl.Utf8}
    )

    unique = set()
    for row in df.iter_rows(named=True):
        ubigeo = row["ubigeo"]
        if ubigeo not in unique:
            unique.add(ubigeo)
            provincias[ubigeo] = row["distrito"]

    final_dict[institucion] = provincias
    update_to_readable(final_dict, variable_name="distritos")
    update_to_resources(final_dict, variable_name="distritos")
    return final_dict


if __name__ == "__main__":
    # crear_provincias(institucion="inei")
    # crear_provincias(institucion="reniec")
    crear_distritos(institucion="inei")
    crear_distritos(institucion="reniec")
    # crear_distritos_inei()
