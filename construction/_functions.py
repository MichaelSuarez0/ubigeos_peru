from collections import defaultdict
import os
from pprint import PrettyPrinter
import unicodedata
import orjson

script_dir = os.path.dirname(__file__)
DATABASES_PATH = os.path.join(script_dir, "..", "databases")
RESOURCES_PATH = os.path.join(script_dir, "..", "ubigeos_peru", "resources")
RESOURCES_READABLE_PATH = os.path.join(script_dir, "..", "resources_readable")


def eliminar_acentos(texto: str)-> str:
    texto_normalizado = unicodedata.normalize('NFKD', texto)
    texto_sin_acentos = ''.join(c for c in texto_normalizado if not unicodedata.combining(c))
    return texto_sin_acentos


def write_to_resources(final_dict: dict, variable_name: str)-> None:
    out_path = os.path.join(RESOURCES_PATH, f"{variable_name}.json")
    with open(out_path, mode = "wb") as f:
        f.write(orjson.dumps(final_dict))
        
def write_to_readable(final_dict: dict, variable_name: str)-> None:
    out_path = os.path.join(RESOURCES_READABLE_PATH, f"{variable_name}.py")
    with open(out_path, mode="w", encoding="utf-8") as f:
        f.write(f"{variable_name.upper()} = ")
        pp = PrettyPrinter(stream=f, width=200, compact=True)
        pp.pprint(final_dict)

# Note: when writing to readable format, remember to use in the terminal afterwards:
# black ubigeos_peru/resources_readable/{file}.py