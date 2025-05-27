from collections import defaultdict
import os
from pprint import PrettyPrinter
import unicodedata
import orjson
from typing import Literal
import json
import importlib.util
import sys

script_dir = os.path.dirname(__file__)
DATABASES_PATH = os.path.join(script_dir, "..", "databases")
RESOURCES_PATH = os.path.join(script_dir, "..", "ubigeos_peru", "resources")
RESOURCES_READABLE_PATH = os.path.join(script_dir, "..", "resources_readable")


def eliminar_acentos(texto: str)-> str:
    texto_normalizado = unicodedata.normalize('NFKD', texto)
    texto_sin_acentos = ''.join(c for c in texto_normalizado if not unicodedata.combining(c))
    return texto_sin_acentos

def write_to_resources(final_dict: dict, variable_name: Literal["departamentos", "distritos", "equivalencias", "inverted", "macrorregiones", "otros", "provincias"])-> None:
    out_path = os.path.join(RESOURCES_PATH, f"{variable_name}.json")
    with open(out_path, mode = "wb") as f:
        f.write(orjson.dumps(final_dict))
        
def write_to_readable(final_dict: dict, variable_name: Literal["departamentos", "distritos", "equivalencias", "inverted", "macrorregiones", "otros", "provincias"])-> None:
    out_path = os.path.join(RESOURCES_READABLE_PATH, f"{variable_name}.py")
    with open(out_path, mode="w", encoding="utf-8") as f:
        f.write(f"{variable_name.upper()} = ")
        pp = PrettyPrinter(stream=f, width=200, compact=True)
        pp.pprint(final_dict)

def update_to_resources(final_dict: dict, variable_name: Literal["departamentos", "distritos", "equivalencias", "inverted", "macrorregiones", "otros", "provincias"])-> None:
    out_path = os.path.join(RESOURCES_PATH, f"{variable_name}.json")

    if os.path.exists(out_path):        
        with open(out_path, mode = "rb") as f:
            final_dict = {**orjson.loads(f.read()), **final_dict}
    
    with open(out_path, mode= "wb") as f:
        f.write(orjson.dumps(final_dict))
            
def update_to_readable(final_dict: dict, variable_name: Literal["departamentos", "distritos", "equivalencias", "inverted", "macrorregiones", "otros", "provincias"])-> None:
    out_path = os.path.join(RESOURCES_READABLE_PATH, f"{variable_name}.py")
    
    # Configuramos para importar el módulo desde la ruta específica
    module_name = f"resources_readable.{variable_name}"
    spec = importlib.util.spec_from_file_location(module_name, out_path)
    
    existing_data = {}
    if os.path.exists(out_path):
        try:
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            existing_data = getattr(module, variable_name.upper(), {})
        except Exception as e:
            print(f"Error importing existing data: {e}")
            existing_data = {}
    
    # Combinar diccionarios
    merged_dict = {**existing_data, **final_dict}
    
    # Escribir el archivo actualizado
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"{variable_name.upper()} = ")
        pp = PrettyPrinter(stream=f, width=200, compact=True)
        pp.pprint(merged_dict)


# Note: when writing to readable format, remember to use this commdand in the terminal to pretty print:
# black ubigeos_peru/resources_readable/{file}.py