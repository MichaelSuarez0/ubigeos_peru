"""
---
script:
  name: "crear_ubigeo_reniec.py"
  description: "Script para obtener los ubigeos de la RENIEC a partir de webscraping de la página Relación de Ubigeos"
  output:
    - "ubigeos_peru/resources_readable/global.py"
    - "ubigeos_peru/resources_readable/provincias.py"
    - "ubigeos_peru/resources_readable/distritos.py"
    - "ubigeos_peru/src/ubigeos_peru/resources/global.json"
    - "ubigeos_peru/src/ubigeos_peru/resources/provincias.json"
    - "ubigeos_peru/src/ubigeos_peru/resources/distritos.json"
    - "ubigeos_peru/src/ubigeos_peru/databases/ubigeo_reniec_2025.csv"

source:
  name: "RELACIÓN DE UBIGEOS"
  url: "https://www.reniec.gob.pe/Adherentes/jsp/ListaUbigeos.jsp"
  reference: ""
  date: "2025-10-23"
  location: ""
  files: ""
  notes:
    - 'población -> Población Total Proyectada al 30/06/2025'
---
"""

import json
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import pandas as pd
import duckdb

import ubigeos_peru as ubg
from ubigeos_peru.core._utils import eliminar_acentos

from _utils import DATABASES_PATH


def _clean_ubigeo_reniec(df: pd.DataFrame):
    try:
        df = df.drop(columns=["N°"])
    except KeyError:
        print("['N°'] not found in axis")

    df["COD_DEP"]  = df["COD_DEP"].astype(str).str.zfill(2)
    df["COD_PROV"] = df["COD_PROV"].astype(str).str.zfill(2)
    df["COD_DIST"] = df["COD_DIST"].astype(str).str.zfill(2)

    df["Ubigeo"] = df["COD_DEP"] + df["COD_PROV"] + df["COD_DIST"]
    cols = ["Ubigeo"] + [c for c in df.columns if c != "Ubigeo"]

    df = df[cols]
    df["Distrito"] = df["Distrito"].str.replace(
        "Weblogic Bridge MessageFailure of Web Server bridge:No backend server available for connection: timed out after 10 seconds or idempotent set to OFF or method not idempotent.",
        "",
        regex=True,
    )
    df["Distrito"] = df["Distrito"].replace(
        {"SAN ISI": "SAN ISIDRO"},
        regex=False
    )

    df["Departamento"] = ubg.validate_departamento(df["Departamento"])
    df["Provincia"] = ubg.validate_ubicacion(df["Provincia"], on_error="raise")
    df["Distrito"] = ubg.validate_ubicacion(df["Distrito"], on_error="warn")


    return df

def _write_ubigeo_reniec(df: pd.DataFrame):
    df.to_csv(
        DATABASES_PATH / "ubigeo_reniec_2025.csv", encoding="utf-8-sig", index=False
    )
    print("Se creó ubigeo_reniec_2025.csv")

def _leer_ubigeo_reniec():
    df = pd.read_csv(DATABASES_PATH / "ubigeo_reniec_2025.csv", encoding="utf-8-sig")
    return df


def crear_ubigeo_reniec():
    URL = "https://www.reniec.gob.pe/Adherentes/ubigeos"
    HEADERS = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.reniec.gob.pe/Adherentes/jsp/ListaUbigeos.jsp",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    UBIGEOS_PATH = DATABASES_PATH / "ubigeo_inei_2025.csv"
    CACHE_PATH = Path(__file__).parent / ".cache" / "reniec_cache.json"
    CACHE_PATH.parent.mkdir(exist_ok=True)

    if CACHE_PATH.exists():
        cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    else:
        cache = {}

    conn = duckdb.connect() 
    query = "SELECT DISTINCT provincia FROM read_csv_auto(?) WHERE departamento = '{}'"

    departamentos = list(ubg.cargar_diccionario("departamentos")["inei"].values())
    departamentos = [eliminar_acentos(dep).upper() for dep in departamentos]
    departamentos.remove("CALLAO")

    all_rows = []
    for dep in departamentos:     
        print(f"Obteniendo para {dep}")
        query_provincia = query.format(ubg.validate_departamento(dep))
        print(query_provincia)

        result = conn.execute(query_provincia, [str(UBIGEOS_PATH)]).fetchdf()
        provincias = [eliminar_acentos(provincia).upper() for provincia in result["provincia"].to_list()]
        correcciones = {
            "ANTONIO RAYMONDI": "ANTONIO RAIMONDI",
            "MARANON": "MARAÑON",
            "NASCA": "NAZCA",
            "FERRENAFE": "FERREÑAFE",
            "CANETE": "CAÑETE",
            "DATEM DEL MARANON": "DATEM DEL MARAÑON",
        }

        provincias = [correcciones.get(p, p) for p in provincias]
        for prov in provincias:
            
            if prov in ("NINABAMBA", "PUTUMAYO"):
                continue

            if prov in cache:
                html = cache[prov]
                print(f"Obteniendo para {dep} de {prov} (cached)")
                
            else:
                print(f"Obteniendo para {dep} de {prov} (request)")
                payload = {
                    "cmbSeleccionado": "4",
                    "noDepartamento": dep,
                    "noProvincia" : prov
                }

                resp = requests.post(URL, data=payload, headers=HEADERS)
                resp.raise_for_status()
                html = resp.text
            
                cache[prov] = html
                CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


            soup = BeautifulSoup(html, "html.parser")
            table = soup.find("table")

            rows = []
            for tr in table.find_all("tr"):
                cols = [td.get_text(strip=True) for td in tr.find_all("td")]
                if cols:
                    rows.append(cols)

            all_rows.extend(rows)

    df = pd.DataFrame(all_rows, columns=[
        "N°", "COD_DEP", "COD_PROV", "COD_DIST",
        "Departamento", "Provincia", "Distrito"
    ])

    df = _clean_ubigeo_reniec(df)

    _write_ubigeo_reniec(df)



if __name__ == "__main__":
    df = _leer_ubigeo_reniec()
    df = _clean_ubigeo_reniec(df)
    _write_ubigeo_reniec(df)
