import os
from pathlib import Path
import re
import sys
import unicodedata
from natsort import natsorted
import orjson
from typing import Literal, Optional
import importlib.util

import black
import pprint

SCRIPT_DIR = Path(__file__).parent
RESOURCES_PATH = SCRIPT_DIR.parent / "src" / "ubigeos_peru" / "resources"
RESOURCES_READABLE_PATH = SCRIPT_DIR.parent / "resources_readable"
DATABASES_PATH = SCRIPT_DIR.parent / "databases"


def eliminar_acentos(texto: str) -> str:
    texto_normalizado = unicodedata.normalize("NFKD", texto)
    texto_sin_acentos = "".join(
        c for c in texto_normalizado if not unicodedata.combining(c)
    )
    return texto_sin_acentos


# Helper functions
def dms_to_dd(coord: str, hemisphere: str) -> Optional[float]:
    """
    Convierte coordenadas en grados, minutos, segundos (DMS) a decimal (DD).
    Ejemplo: "74º13'31\"" con hemisferio "O" -> -74.225278

    Retorna None si la conversión falla.
    """
    if not coord or not isinstance(coord, str) or coord.strip() == "":
        return None

    try:
        # Normalizar símbolos y quitar comillas
        clean = (
            coord.replace("º", " ")
                 .replace("°", " ")
                 .replace("ʹ", " ")
                 .replace("'", " ")
                 .replace("′", " ")
                 .replace('"', " ")
                 .replace("″", " ")
                 .replace(",", ".")
        )
        
        # Separar en partes y limpiar espacios
        parts = [p.strip() for p in re.split(r"\s+", clean.strip()) if p.strip()]

        deg = float(parts[0])
        minutes = float(parts[1])
        seconds = float(parts[2])

        dd = deg + minutes / 60 + seconds / 3600

        # Aplicar signo según hemisferio
        if hemisphere.upper() in ["S", "O", "W"]:
            dd = -dd

        return round(dd, 8)  # Redondear a 8 decimales para precisión    except Exception as e:
        print(f"Error convirtiendo coordenada '{coord}': {e}")
        return None

def write_to_resources(
    final_dict: dict,
    variable_name: Literal[
        "departamentos",
        "distritos",
        "equivalencias",
        "inverted",
        "macrorregiones",
        "otros",
        "provincias",
    ],
) -> None:
    output_path = RESOURCES_PATH / f"{variable_name}.json"
    with open(output_path, mode="wb") as f:
        f.write(orjson.dumps(final_dict))


def write_to_readable(
    final_dict: dict,
    variable_name: Literal[
        "departamentos",
        "distritos",
        "equivalencias",
        "inverted",
        "macrorregiones",
        "otros",
        "provincias",
    ],
) -> None:
    output_path = RESOURCES_READABLE_PATH / f"{variable_name}.py"

    # Formateamos con Black
    code = f"{variable_name.upper()} = {repr(final_dict)}"
    formatted_code = black.format_str(code, mode=black.FileMode())

    with open(output_path, mode="w", encoding="utf-8") as f:
        f.write(formatted_code)


def deep_merge_dicts(existing_dict: dict, new_dict: dict) -> dict:
    result = existing_dict.copy()

    for key, value in new_dict.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # Solo entra aquí si la clave ya existe en result
            result[key] = deep_merge_dicts(result[key], value)
        else:
            # Entra aquí si la clave no existe o si no son ambos diccionarios
            result[key] = value

    return result


def update_to_resources(
    final_dict: dict,
    variable_name: Literal[
        "departamentos",
        "distritos",
        "equivalencias",
        "inverted",
        "macrorregiones",
        "otros",
        "provincias",
        "global"
    ],
) -> None:
    output_path = RESOURCES_PATH / f"{variable_name}.json"

    if os.path.exists(output_path):
        with open(output_path, mode="rb") as f:
            existing_data = orjson.loads(f.read())

        merged_dicts = deep_merge_dicts(existing_data, final_dict)
    else:
        merged_dicts = {}
    # for subdict, values in merged_dicts.items():
    #     merged_dicts[subdict] = dict(
    #         natsorted(values.items(), key=lambda x: int(x[0]))
    #     )

    with open(output_path, mode="wb") as f:
        f.write(orjson.dumps(merged_dicts))
        
    print(f"[INFO] Se actualizó {variable_name} en resources")


def update_to_readable(
    final_dict: dict,
    variable_name: Literal[
        "departamentos",
        "distritos",
        "equivalencias",
        "inverted",
        "macrorregiones",
        "otros",
        "provincias",
        "global"
    ],
) -> None:
    output_path = RESOURCES_READABLE_PATH / f"{variable_name}.py"

    # Configuramos para importar el módulo desde la ruta específica
    # Esto se lo dejé a Claude
    module_name = f"resources_readable.{variable_name}"
    spec = importlib.util.spec_from_file_location(module_name, output_path)

    existing_data = {}
    if os.path.exists(output_path):
        try:
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            existing_data = getattr(module, variable_name.upper(), {})
        except Exception as e:
            print(f"Error importing existing data: {e}")
            existing_data = {}

    # Combinar diccionarios
    merged_dicts = deep_merge_dicts(existing_data, final_dict)
    for institucion, values in merged_dicts.items():
        merged_dicts[institucion] = dict(
            natsorted(values.items(), key=lambda x: x[0])
        )

    # Formatear con black
    code_str = f"{variable_name.upper()} = {pprint.pformat(merged_dicts)}"
    formatted_code = black.format_str(code_str, mode=black.FileMode())

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(formatted_code)
    print(f"[INFO] Se actualizó {variable_name} en resources_readable")


# Note: when writing to readable format, remember to use this commdand in the terminal to pretty print:
# black ubigeos_peru/resources_readable/{file}.py
