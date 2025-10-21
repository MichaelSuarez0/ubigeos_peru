from collections import defaultdict

import orjson
from _utils import RESOURCES_PATH, write_to_readable, write_to_resources, eliminar_acentos


def read_dict(level: str):
    with open(RESOURCES_PATH / f"{level}.json", mode="r", encoding="utf-8") as f:
        dictio = orjson.loads(f.read())

    return dictio


def join_dicts(dictionaries: list[dict], names: list[str]) -> dict:
    result = defaultdict(dict)
    for d, name in zip(dictionaries, names):
        result[name] = d

    return dict(result)


def invert_dict(final_dict: dict):
    final_dict = {
        level: {
            inst: {eliminar_acentos(lugar.upper()): code for code, lugar in mappings.items()}
            for inst, mappings in institutions.items()
        }
        for level, institutions in final_dict.items()
    }
    return final_dict


def crear_inverted():
    names = ["departamentos", "provincias", "distritos"]
    departamentos = read_dict(names[0])
    provincias = read_dict(names[1])
    distritos = read_dict(names[2])

    final_dict = join_dicts([departamentos, provincias, distritos], names)
    final_dict = invert_dict(final_dict)

    write_to_resources(final_dict, "inverted")
    write_to_readable(final_dict, "inverted")


if __name__ == "__main__":
    crear_inverted()
