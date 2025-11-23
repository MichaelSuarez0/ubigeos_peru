"""
---
script:
  name: "crear_ubigeo_reniec.py"
  description: "Script para obtener los ubigeos de la RENIEC a partir de limpieza de Excel de Identidad Reniec"
  output: "ubigeos_peru/src/ubigeos_peru/databases/ubigeo_reniec_2025.csv"

source:
  name: "Ubigeos Reniec"
  url: ""
  reference: "Obtenida a partir de solicitud de acceso a la información pública. SOLICITUD DE REGISTRO Nº 1931-2025."
  original_name: "UBIGEOS_RENIEC_CCPP_Q20251110.xlsx"
  original_date: "2025-11-11"
  last_visited: "2025-11-11"
  location: "ubigeos_peru/databases/UBIGEOS_RENIEC_CCPP_Q20251110.xlsx"
---
"""

import polars as pl

import ubigeos_peru as ubg
from construction._utils import DATABASES_PATH

reniec_path = DATABASES_PATH / "UBIGEOS_RENIEC_CCPP_Q20251110.xlsx"


def crear_ubigeos_reniec():
    df = pl.read_excel(reniec_path, drop_empty_cols=True, drop_empty_rows=True)
    df = df.drop(["CO_CONTINENTE", "CO_PAIS", "NO_CONTINENTE", "NO_PAIS"])
    df = df.select(
        (
            pl.col("CO_DEPARTAMENTO") + pl.col("CO_PROVINCIA") + pl.col("CO_DISTRITO")
        ).alias("ubigeo"),
        pl.col("NO_DEPARTAMENTO").alias("departamento"),
        pl.col("NO_PROVINCIA").alias("provincia"),
        pl.col("NO_DISTRITO").alias("distrito"),
    )
    df = (
        df.with_columns(pl.col("distrito").str.strip_chars())
        .filter(pl.col("distrito") != "")
        .unique("distrito", maintain_order=True)
    )

    df = df.with_columns(
        ubg.validate_departamento(df["departamento"], on_error="warn").alias(
            "departamento"
        ),
        ubg.validate_provincia(df["provincia"], on_error="warn").alias("provincia"),
        ubg.validate_distrito(df["distrito"], on_error="warn").alias("distrito"),
    )
    # SANTA ROSA DE LORETO -> ANTA
    # ARICA -> TARICA
    df.write_csv(DATABASES_PATH / "ubigeo_reniec_2025.csv", separator=";")
    return df


if __name__ == "__main__":
    print(crear_ubigeos_reniec())
