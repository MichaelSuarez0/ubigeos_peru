import os
import pandas as pd
from collections import defaultdict
from _utils import DATABASES_PATH, write_to_readable, write_to_resources

all_path = os.path.join(DATABASES_PATH, "ubigeo_{}.csv")

def preprocess_dataframe(df: pd.DataFrame, level: str) -> dict:
    base_list = [level, "capital", "superficie", "altitude", "latitude", "longitude"]
    df = df[base_list].drop_duplicates().dropna()

    final_dict = defaultdict(dict)
    for row in df.itertuples(index=False):
        final_dict[level][row[0]] = {
            base_list[1]: str(row[1]).strip(),
            base_list[2]: str(row[2]).strip(),
            "altitud": str(row[3]).strip(),
            "latitud": str(row[4]).strip(),
            "longitud": str(row[5]).strip(),
        }    
    return dict(final_dict)
    
def join_dicts(*dictionaries: dict)-> dict:
    result = {}
    for d in dictionaries:
        result.update(d)
    return result

    
def global_creation():
    names = ["departamento", "provincia", "distrito"]
    df1 = pd.read_csv(all_path.format(names[0]), encoding='utf-8', dtype=str)
    df2 = pd.read_csv(all_path.format(names[1]), encoding='utf-8', dtype=str)
    df3 = pd.read_csv(all_path.format(names[2]), encoding='utf-8', dtype=str)
    
    departamentos = preprocess_dataframe(df1, f"{names[0]}s")
    provincias = preprocess_dataframe(df2, f"{names[1]}s")
    distritos = preprocess_dataframe(df3, f"{names[2]}s")
    final_dict = join_dicts(departamentos, provincias, distritos)
    
    write_to_resources(final_dict, "global")
    write_to_readable(final_dict, "global")


if __name__ == "__main__":
    global_creation()