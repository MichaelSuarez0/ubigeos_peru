from ubigeos_peru.resources import DEPARTAMENTOS, PROVINCIAS, DISTRITOS, EQUIVALENCIAS, MACRORREGIONES
from _functions import DATABASES_PATH, RESOURCES_PATH, RESOURCES_READABLE_PATH
from _functions import write_to_json, write_to_readable
from ubigeos_peru import Ubigeo as ubg


def clean_dict(constant: dict)-> dict:
    for inst, details in constant.items():
        for codigo, ubicacion in details.items():
            constant[inst][codigo] = ubg.validate_ubicacion(ubicacion, ignore_errors=True)
    
    return constant
        
    
def cleaning():
    deps = clean_dict(DEPARTAMENTOS)
    provs = clean_dict(PROVINCIAS)
    dist = clean_dict(DISTRITOS)
    write_to_json(deps, "departamentos")
    write_to_json(provs, "provincias")
    write_to_json(dist, "distritos")
    write_to_readable(deps, "departamentos")
    write_to_readable(provs, "provincias")
    write_to_readable(dist, "distritos")


if __name__ == "__main__":
    cleaning()
