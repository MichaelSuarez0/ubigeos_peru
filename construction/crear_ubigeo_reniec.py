"""
---
script:
  name: "crear_ubigeo_reniec.py"
  description: "Script para obtener los ubigeos de la RENIEC a partir de limpieza de Excel de Identidad Reniec"
  output: "ubigeos_peru/src/ubigeos_peru/databases/ubigeo_reniec_2024.csv"

source:
  name: "Ubigeo de DNI de Perú (RENIEC)"
  url: "https://identidad.reniec.gob.pe/documents/d/guest/c02-9-2024-ii"
  reference: ""
  original_name: "C02.9.2024.II.xlsx"
  original_date: " 2024-06-30
  last_visited: "2025-11-11"
  location: "ubigeos_peru/databases/C02.9.2024.II.xlsx"
  files: ""
---
"""

import polars as pl
from _utils import DATABASES_PATH
import ubigeos_peru as ubg

reniec_path = DATABASES_PATH / "geodir-ubigeo-reniec.csv"


def crear_ubigeos_reniec():
    df = pl.read_csv(reniec_path, separator=";", schema_overrides={"Ubigeo": pl.Utf8})

    df = df.with_columns(pl.col("X").alias("Longitud"), pl.col("Y").alias("Latitud"))

    df = df.with_columns(
        [
            ubg.validate_departamento(df["Departamento"]).alias("Departamento"),
            ubg.validate_ubicacion(df["Provincia"], on_error="warn").alias("Provincia"),
            ubg.validate_ubicacion(df["Distrito"], on_error="warn").alias("Distrito"),
        ]
    )

    df = df.with_columns(
        pl.when(pl.col("Provincia") == "CARLOS FERMIN FITZCA")
        .then(pl.lit("Carlos Fermín Fitzcarrald"))
        .otherwise(pl.col("Provincia"))
        .alias("Provincia")
    )

    # Reordenar columnas
    df = df.select(
        [
            "Ubigeo",
            "Departamento",
            "Provincia",
            "Distrito",
            "Poblacion",
            "Superficie",
            "Longitud",
            "Latitud",
        ]
    )

    df = df.rename(
        {
            "Ubigeo": "ubigeo",
            "Departamento": "departamento",
            "Provincia": "provincia",
            "Distrito": "distrito",
            "Poblacion": "poblacion",
            "Superficie": "superficie",
            "Longitud": "longitud",
            "Latitud": "latitud",
        }
    )

    df.write_csv(DATABASES_PATH / "ubigeo_reniec_2019.csv", separator=";")


if __name__ == "__main__":
    crear_ubigeos_reniec()
