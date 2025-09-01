
import os
import pandas as pd
from collections import defaultdict
from _utils import DATABASES_PATH, write_to_readable, write_to_resources

all_path = os.path.join(DATABASES_PATH, "equivalencia-ubigeos-oti-concytec.csv")


# Departamento
def convert_to_dict(df: pd.DataFrame, level: str) -> dict:
    base_list = ["cod_{}_inei", "cod_{}_reniec", "cod_{}_sunat", "desc_{}_inei", "desc_{}_reniec", "desc_{}_sunat"]
    df = df[[name.format(level).strip() for name in base_list]].drop_duplicates(subset= f"cod_{level}_inei")
    df = df.drop_duplicates(subset= f"cod_{level}_inei").dropna()

    final_dict = defaultdict(dict)
    for row in df.itertuples(index=False):
        final_dict["inei"][row[0]] = row[3]
        final_dict["reniec"][row[1]] = row[4]
        final_dict["sunat"][row[2]] = row[5]


    final_dict = {
        inst: {
            code: desc
            for code, desc in mapping.items()
            if pd.notnull(desc)   # o bien: desc == desc
        }
        for inst, mapping in final_dict.items()
    }
    return dict(final_dict)


def ubigeos_creation():
    df = pd.read_csv(all_path, encoding='latin8', dtype=str)    
    departamentos = convert_to_dict(df, level= "dep")
    provincias = convert_to_dict(df, level="prov")
    distritos = convert_to_dict(df, level="ubigeo")   
    write_to_resources(departamentos, "departamentos")
    write_to_resources(provincias, "provincias")
    write_to_resources(distritos, "distritos")
    
    write_to_readable(departamentos, "departamentos")
    write_to_readable(provincias, "provincias")
    write_to_readable(distritos, "distritos")

if __name__ == "__main__":
    ubigeos_creation()
