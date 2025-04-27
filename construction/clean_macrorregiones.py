from collections import defaultdict
from _functions import DATABASES_PATH, RESOURCES_PATH, RESOURCES_READABLE_PATH, write_to_readable, write_to_json
from ubigeos_peru.resources import MACRORREGIONES
from ubigeos_peru import Ubigeo as ubg


def clean_macrorregiones(macrorregiones: dict)-> dict:
    clean_dict = defaultdict(dict)
    for inst, details in macrorregiones.items():
        for dep, macrorregion in details.items():
            clean_dict[inst][ubg.normalize_departamento(dep, upper=False)] = macrorregion

    return dict(clean_dict)


if __name__ == "__main__":
    macro_clean = clean_macrorregiones(MACRORREGIONES)
    write_to_json(macro_clean, "macrorregiones")
    write_to_readable(macro_clean, "macrorregiones")
    


