from typing import Literal
import polars as pl
from pathlib import Path
from natsort import natsorted
from _utils import update_to_readable, update_to_resources, DATABASES_PATH


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

# Helper functions
def extraer_datos_de_directorio(df: pl.DataFrame, key: Literal["provincias", "distritos"]) -> dict:
    df.columns = columns
    if key == "provincias":
        longitud = 4
    elif key == "distritos":
        longitud = 6
    df = df.with_columns(pl.col("Ubigeo").cast(pl.Utf8)).filter(
        pl.col("Ubigeo").str.len_chars() == longitud
    )
    llaves = df.select(["Ubigeo", "Provincia y Distrito"]).to_dicts()
    dict_final = {
        llave["Ubigeo"]
        .strip(): llave["Provincia y Distrito"]
        .replace("\n", "")
        .replace("\r", "")
        .strip()
        for llave in llaves
    }
    return dict_final


def crear_provincias_db():
    provincias_dir = DATABASES_PATH / "municipalidades_2025"
    provincias = {}
    final_dict = {}

    for path in provincias_dir.iterdir():
        df = pl.read_excel(path)
        provs = extraer_datos_de_directorio(df, key="provincias")
        provincias.update(provs)

    # Limpiar algunos nombres
    provincias["0701"] = "Callao"
    provincias["1501"] = "Lima"
    provincias["0508"] = "Páucar del Sara Sara"
    provincias["1005"] = "Huamalíes"

    final_dict["inei"] = provincias
    update_to_readable(final_dict, variable_name="provincias")
    update_to_resources(final_dict, variable_name="provincias")
    return final_dict


def crear_distritos_db():
    provincias_dir = DATABASES_PATH / "municipalidades_2025"
    distritos_dict = {}
    final_dict = {}

    for path in provincias_dir.iterdir():
        df = pl.read_excel(path)
        distritos = extraer_datos_de_directorio(df, key="distritos")
        distritos_dict.update(distritos)

    # Limpiar algunos nombres
    distritos_dict.pop("Ubigeo")
    distritos_dict["040302"] = "Acarí"
    distritos_dict["061306"] = "Ninabamba"
    distritos_dict["250307"] = "Boquerón"

    final_dict["inei"] = distritos_dict
    update_to_readable(final_dict, variable_name="distritos")
    update_to_resources(final_dict, variable_name="distritos")
    return final_dict


if __name__ == "__main__":
    from pprint import pprint

    crear_provincias_db()
    crear_distritos_db()
