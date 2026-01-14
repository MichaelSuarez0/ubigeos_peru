from __future__ import annotations
from pathlib import Path
import pandas as pd
import ubigeos_peru as ubg

# ============================================================
# 0. CONFIGURACIÓN GENERAL / CONSTANTES
# ============================================================
SCRIPT_DIR = Path(__file__).parent

INPUT_FILE = SCRIPT_DIR / "tu_base_de_datos.xlsx"
OUTPUT_FILE = INPUT_FILE.with_name(f"{INPUT_FILE.stem}_clean.csv")

CSV_ENCODING = "utf-8" 
CSV_SEPARATOR = ";"          

# ============================================================
# 1. FUNCIONES PRINCIPALES
# ============================================================
def get_dep_prov_dist(df: pd.DataFrame, columna_ubigeo: str) -> pd.DataFrame:
    """
    Obtiene el departamento, provincia y distrito de una base de datos
    a partir de la columna que contiene el ubigeo.
    """
    df["DEPARTAMENTO"] = ubg.get_departamento(df[columna_ubigeo], institucion="inei", divide_lima=True)
    df["PROVINCIA"] = ubg.get_provincia(df[columna_ubigeo], on_error="warn", institucion="inei")
    df["DISTRITO"] = ubg.get_distrito(df[columna_ubigeo], on_error="warn", institucion="inei")
    
    return df

def get_ubigeos(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica transformaciones o validaciones al DataFrame."""
    df["UBIGEO"] = ubg.get_ubigeo(df["DISTRITO"], level="distritos", institucion="inei", on_error="coerce")
    return df


def main() -> None:
    """Ejecuta el flujo principal del script."""
    df = pd.read_excel(INPUT_FILE)
    df = get_dep_prov_dist(df, columna_ubigeo="UBIGEO")
    df.to_csv(OUTPUT_FILE, index=False, sep=CSV_SEPARATOR, encoding=CSV_ENCODING)
    print(f"✅ Archivo exportado correctamente en: {OUTPUT_FILE}")

# ============================================================
# 2. EJECUCIÓN DIRECTA
# ============================================================
if __name__ == "__main__":
    main()
