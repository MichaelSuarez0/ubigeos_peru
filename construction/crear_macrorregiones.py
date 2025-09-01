
import os
import pandas as pd
from collections import defaultdict
from _utils import DATABASES_PATH, write_to_resources, write_to_readable

all_path = os.path.join(DATABASES_PATH, "ubigeo_provincia.csv")


def preprocess_dataframe(df: pd.DataFrame) -> dict:
    base_list = ["departamento", "macroregion_inei", "macroregion_minsa", "capital"]
    df = df[base_list].drop_duplicates(subset= f"departamento").dropna()

    final_dict = defaultdict(dict)
    for row in df.itertuples(index=False):
        final_dict["inei"][row[0]] = str(row[1]).strip().capitalize()
        final_dict["minsa"][row[0]] = str(row[2]).replace("MACROREGION ", "").strip().capitalize()


    final_dict = {
        inst: {
            code: desc
            for code, desc in mapping.items()
            if pd.notnull(desc)   # o bien: desc == desc
        }
        for inst, mapping in final_dict.items()
    }
    return dict(final_dict)


def modify_macrorregiones(df: pd.DataFrame)-> dict:
    macrorregiones = preprocess_dataframe(df)
    for values in macrorregiones.values():
        for dep, macrorregion in values.items():
            if macrorregion == "Lima metropolitana":
                values[dep] = "Lima Metropolitana"
            elif macrorregion == "Lima y callao":
                values[dep] = "Lima y Callao"
            else:
                pass
    return macrorregiones

def add_ceplan_macrorregiones(macrorregiones: dict):
    macrorregiones.update({'ceplan':{
        "Amazonas": "Norte",
        "Áncash": "Centro",
        "Apurímac": "Sur",
        "Arequipa": "Sur",
        "Ayacucho": "Sur",
        "Cajamarca": "Norte",
        "Cusco": "Sur",
        "Huancavelica": "Sur",
        "Huánuco": "Centro",
        "Ica": "Sur",
        "Junín": "Centro",
        "La Libertad": "Norte",
        "Lambayeque": "Norte",
        "Lima Región": "Centro",
        "Lima Metropolitana": "Centro",
        "Loreto": "Nororiente",
        "Madre de Dios": "Sur",
        "Moquegua": "Sur",
        "Pasco": "Centro",
        "Piura": "Norte",
        "Puno": "Sur",
        "San Martín": "Norte",
        "Tacna": "Sur",
        "Tumbes": "Norte",
        "Ucayali": "Nororiente",
    }})


def macrorregiones_creation():
    df = pd.read_csv(all_path, encoding='utf-8', dtype=str)
    macrorregiones = preprocess_dataframe(df)
    macrorregiones = modify_macrorregiones(macrorregiones)
    macrorregiones = add_ceplan_macrorregiones(macrorregiones)
    write_to_resources(macrorregiones, "macrorregiones")
    write_to_readable(macrorregiones, "macrorregiones")

if __name__ == "__main__":
    macrorregiones_creation()
               
# Then they get pretty formatted with terminal command black ubigeos_peru/ubigeos_peru/resources/distritos.py


