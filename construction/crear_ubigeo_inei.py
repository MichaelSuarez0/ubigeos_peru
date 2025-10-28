"""
---
script:
  name: "crear_ubigeo_inei.py"
  description: "Script para transformar el Directorio Nacional de Centros Poblados y extraer la metadata de todos los distritos"
  output:
    - "ubigeos_peru/resources_readable/global.py"
    - "ubigeos_peru/resources_readable/provincias.py"
    - "ubigeos_peru/resources_readable/distritos.py"
    - "ubigeos_peru/src/ubigeos_peru/resources/global.json"
    - "ubigeos_peru/src/ubigeos_peru/resources/provincias.json"
    - "ubigeos_peru/src/ubigeos_peru/resources/distritos.json"
    - "ubigeos_peru/src/ubigeos_peru/databases/ubigeo_inei_2025.csv"

source:
  name: "Directorio Nacional de Gobiernos Regionales, Municipalidades Provinciales, Distritales y de Centros Poblados 2025 (Cuadros en Excel)"
  url: "https://www.gob.pe/institucion/inei/informes-publicaciones/6722617-directorio-nacional-de-gobiernos-regionales-municipalidades-provinciales-distritales-y-de-centros-poblados-2025"
  reference: "1.Directorio-MPyMD-2025"
  date: "2025-05-29"
  location: "ubigeos_peru/databases/municipalidades_2025"
  files:
    - "Amazonas_2025_CC.xls"
    - "Áncash_2025_CC.xls"
    - "Apurímac_2025_CC.xls"
    - "Arequipa_2025_CC.xls"
    - "Ayacucho_2025_CC.xls"
    - "Cajamarca_2025_CC.xls"
    - "Callao_2025_CC.xls"
    - "Cusco_2025_CC.xls"
    - "Huancavelica_2025_CC.xls"
    - "Huánuco_2025_CC.xlsx"
    - "Ica_2025_CC.xls"
    - "Junín_2025_CC.xls"
    - "La Libertad_2025_CC.xls"
    - "Lambayeque_2025_CC.xls"
    - "Lima Metropolitana_2025_CC.xls"
    - "Departamento de Lima_2025_CC.xls"
    - "Loreto_2025_CC.xls"
    - "Madre de Dios_2025_CC.xls"
    - "Moquegua_2025_CC.xls"
    - "Pasco_2025_CC.xls"
    - "Piura_2025_CC.xls"
    - "Puno_2025_CC.xls"
    - "San Martín_2025_CC.xls"
    - "Tacna_2025_CC.xls"
    - "Tumbes_2025_CC.xls"
    - "Ucayali_2025_CC.xls"
  notes:
    - 'población -> Población Total Proyectada al 30/06/2025'
---
"""

from pathlib import Path
from typing import Literal
import polars as pl
import ubigeos_peru as ubg
from _utils import update_to_readable, update_to_resources, DATABASES_PATH, dms_to_dd

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

# Limpiar algunos nombres
corr_distrito = {
    "040302": "Acarí",
    "250307": "Boquerón",
}
corr_provincia = {
    "061306": "Ninabamba",
}


def extraer_datos_de_directorio(
    df: pl.DataFrame, key: Literal["provincias", "distritos"]
) -> pl.DataFrame:
    df.columns = columns

    if key == "provincias":
        longitud = 4
    elif key == "distritos":
        longitud = 6

    # Convertir todas las columnas a string (Utf8)
    df = df.select([pl.col(c).cast(pl.Utf8) for c in df.columns])

    # Limpiar TODAS las columnas string
    df = df.with_columns(
        [
            pl.col(c)
            .cast(pl.Utf8)  # fuerza string
            .str.replace("\n", "")
            .str.replace("\r", "")
            .str.strip_chars()
            .alias(c)
            for c in df.columns
        ]
    )
    df = df.filter(pl.col("Ubigeo") != "Ubigeo")

    # Convertir coordenadas
    df = df.with_columns(
        [
            pl.col("Latitud Sur")
            .map_elements(lambda x: dms_to_dd(x, "S"), return_dtype=pl.Float64)
            .alias("latitud"),
            pl.col("Longitud Oeste")
            .map_elements(lambda x: dms_to_dd(x, "O"), return_dtype=pl.Float64)
            .alias("longitud"),
        ]
    )

    # Filtrar si se piden provincias o distritos
    df = df.with_columns(pl.col("Ubigeo")).filter(
        pl.col("Ubigeo").str.len_chars() == longitud
    )

    df = df.drop(
        [
            "Longitud Oeste",
            "Latitud Sur",
            "Nombre del Alcalde",
            "Dirección",
            "DDN",
            "Teléfonos",
            "Correo Electrónico",
            "Dispositivo Legal de Creación del Distrito",
        ]
    )

    df = df.rename(
        {
            "Población Total Proyectada al 30/06/2025": "Población",
            "Altitud (msnm.)": "altitud",
            "Nombre": "capital_legal",
        }
    )

    df.columns = [col.lower() for col in df.columns]

    return df


def merge_directories_to_dict(
    path: Path, key: Literal["provincia", "distrito"]
) -> dict:
    final_dict = {}

    for path in path.iterdir():
        df = pl.read_excel(path)
        df = extraer_datos_de_directorio(df, key=f"{key}s")
        df = df.rename({"provincia y distrito": key})
        llaves = df.to_dicts()

        for fila in llaves:
            ubigeo = fila.pop("ubigeo")
            final_dict[ubigeo] = fila

    return final_dict


def _merge_directories(path: Path, key: Literal["provincia", "distrito"]) -> list:
    final_list = []

    for path in path.iterdir():
        df = pl.read_excel(path)
        df = extraer_datos_de_directorio(df, key=f"{key}s")
        df = df.rename({"provincia y distrito": key})
        llaves = df.to_dicts()

        final_list.append(llaves)

    return final_list


def crear_provincias_inei():
    provincias_dir = DATABASES_PATH / "municipalidades_2025"
    provincias = {}
    final_dict = {}

    provincias = merge_directories_to_dict(provincias_dir, key="provincia")
    provincias_completas = {
        ubigeo: metadata["provincia"] for ubigeo, metadata in provincias.items()
    }

    # Limpiar algunos nombres
    provincias_completas["0701"] = "Callao"
    provincias_completas["1501"] = "Lima"
    provincias_completas["0508"] = "Páucar del Sara Sara"
    provincias_completas["1005"] = "Huamalíes"

    final_dict["inei"] = provincias_completas
    update_to_readable(final_dict, variable_name="provincias")
    update_to_resources(final_dict, variable_name="provincias")
    return final_dict


def crear_distritos_inei():
    distritos_dir = DATABASES_PATH / "municipalidades_2025"
    final_dict = {}

    distritos = merge_directories_to_dict(distritos_dir, key="distrito")
    distritos_completos = {
        ubigeo: metadata["distrito"] for ubigeo, metadata in distritos.items()
    }

    # Limpiar algunos nombres
    distritos_completos["040302"] = "Acarí"
    distritos_completos["061306"] = "Ninabamba"
    distritos_completos["250307"] = "Boquerón"

    final_dict["inei"] = distritos_completos
    update_to_readable(final_dict, variable_name="distritos")
    update_to_resources(final_dict, variable_name="distritos")
    return final_dict


def crear_global_db():
    provincias_dir = DATABASES_PATH / "municipalidades_2025"

    final_dict = merge_directories_to_dict(provincias_dir, key="distrito")

    # Limpiar algunos nombres
    # distritos["040302"]["distrito"] = "Acarí"
    # distritos["250307"]["distrito"] = "Boquerón"
    # distritos["061306"]["provincia"] = "Ninabamba"

    # final_dict["inei"] = distritos
    update_to_readable(final_dict, variable_name="global")
    update_to_resources(final_dict, variable_name="global")
    return final_dict


def crear_ubigeo_inei():
    provincias_dir = DATABASES_PATH / "municipalidades_2025"

    final_list = _merge_directories(provincias_dir, key="distrito")

    # Limpiar algunos nombres
    # distritos["040302"]["distrito"] = "Acarí"
    # distritos["250307"]["distrito"] = "Boquerón"
    # distritos["061306"]["provincia"] = "Ninabamba"

    # final_list["inei"] = distritos
    # update_to_readable(final_list, variable_name="full")
    flat_list = [item for sublist in final_list for item in sublist]

    # convertimos a DataFrame
    df = pl.DataFrame(flat_list)
    df = df.with_columns(
        pl.col("altitud").cast(pl.Float32),
        pl.col("población").cast(pl.Int32),
        pl.col("ubigeo")
        .map_elements(ubg.get_departamento, return_dtype=pl.Utf8)
        .alias("departamento"),
        pl.col("ubigeo")
        .map_elements(ubg.get_provincia, return_dtype=pl.Utf8)
        .alias("provincia"),
    )
    df = df.sort("ubigeo")

    # reordenar columnas
    df = df.select(
        ["departamento", "provincia", "distrito"]
        + [c for c in df.columns if c not in ["departamento", "provincia", "distrito"]]
    )

    # limpiar algunos nombres
    df = df.with_columns(
        pl.when(pl.col("ubigeo") == "040302").then(pl.lit("Acarí"))
        .when(pl.col("ubigeo") == "250307").then(pl.lit("Boquerón"))
        .when(pl.col("ubigeo") == "061306").then(pl.lit("Ninabamba"))
        .when(pl.col("ubigeo") == "060414").then(pl.lit("Pion"))
        .otherwise(pl.col("distrito"))
        .alias("distrito")
    )

    df = df.with_columns(
        pl.when(pl.col("ubigeo") == "061306").then(pl.lit("Ninabamba"))
        .otherwise(pl.col("provincia"))
        .alias("provincia")
    )

    # escribir
    df = df.to_pandas()
    df["ubigeo"] = df["ubigeo"].astype(str)
    df.to_csv(DATABASES_PATH / "ubigeo_inei_2025.csv", encoding="utf-8-sig", index=False, sep=";")

    return df


if __name__ == "__main__":
    crear_ubigeo_inei()
