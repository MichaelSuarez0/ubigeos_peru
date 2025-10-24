from pathlib import Path

import numpy as np
import pandas as pd

import ubigeos_peru as ubg
from _utils import DATABASES_PATH

centros_poblados = Path(DATABASES_PATH / "municipalidades_centros_poblados_2025")

OUTPUT_DIR = centros_poblados.parent


def get_headers(df: pd.DataFrame):
    df_headers = df.iloc[:3, :].copy()
    df_headers.ffill(axis=0, limit=1, inplace=True)
    df_headers = list(df_headers.iloc[-1, :])
    df_headers[-3] = "Viviendas particulares"
    df_headers[-6] = "Población Censada"
    df_headers[2] = "Región natural (según piso altitudinal)"
    return df_headers


def clean_directorio():
    excels = {}
    n = 0
    for excel in centros_poblados.iterdir():
        df = pd.read_excel(excel)

        # Obtener metadata
        departamento = df.columns[0].replace("DEPARTAMENTO DE ", "").strip()
        departamento = ubg.validate_departamento(departamento, on_error="capitalize")
        headers = get_headers(df)
        df.columns = headers

        # Quedarse con el cuerpo
        df_clean = df.loc[df.iloc[:, 0].str.len() == 4, :]
        df_clean.reset_index(drop=True, inplace=True)
        df_clean = df_clean.drop(index=0).copy()
        df_clean.iloc[:, 3:] = df_clean.iloc[:, 3:].apply(
            pd.to_numeric, errors="coerce"
        )
        df_final = df_clean.replace("-", np.nan)

        # Crear col "Departamento" y mover a la segunda posición
        df_final["Departamento"] = departamento
        col_temp = df_final.pop("Departamento")
        df_final.insert(1, "Departamento", col_temp)
        excels[departamento] = df_final

        print(f"Ya va {n}")
        n += 1

    directorio_cp = pd.concat(
        [df.reset_index(drop=True) for df in excels.values()],
        axis=0,
        ignore_index=True,
        sort=False,
    )
    directorio_cp.to_csv(
        OUTPUT_DIR / "directorio_centros_poblados.csv", index=False, sep=";", encoding="utf-8-sig"
    )


if __name__ == "__main__":
    clean_directorio()
