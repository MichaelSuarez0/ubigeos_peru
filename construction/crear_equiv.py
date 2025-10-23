import orjson
from _utils import (
    RESOURCES_PATH,
    eliminar_acentos,
    write_to_readable,
    write_to_resources,
)


def crear_equivalencias():
    niveles = ["departamentos", "provincias", "distritos"]
    equivalencias_completo = {}
    for nivel in niveles:
        with open(RESOURCES_PATH / f"{nivel}.json", mode="rb") as f:
            existing_dict = orjson.loads(f.read())

        values = existing_dict["inei"].values()
        equivalencias = {eliminar_acentos(v).upper(): v for v in values}
        equivalencias = dict(sorted(equivalencias.items(), key=lambda x: x[0]))
        equivalencias_completo[nivel] = equivalencias

    # Añadir
    # Departamentos
    equivalencias_completo["departamentos"]["CUZCO"] = "Cusco"
    equivalencias_completo["departamentos"]["LIMA METROPOLITANA"] = "Lima Metropolitana"
    equivalencias_completo["departamentos"]["LIMA REGION"] = "Lima Región"
    equivalencias_completo["departamentos"]["REGION LIMA"] = "Lima Región"

    # Provincias
    equivalencias_completo["provincias"]["CUZCO"] = "Cusco"
    equivalencias_completo["provincias"]["NAZCA"] = "Nazca"
    equivalencias_completo["provincias"]["NASCA"] = "Nasca"

    # Distritos
    equivalencias_completo["distritos"]["CUZCO"] = "Cusco"
    equivalencias_completo["distritos"]["26 DE OCTUBRE"] = "Veintiséis de Octubre"
    equivalencias_completo["distritos"]["27 DE NOVIEMBRE"] = "Veintisiete de Noviembre"
    equivalencias_completo["distritos"]["ANDRES AVELINO CACERES"] = "Andrés Avelino Cáceres Dorregaray"
    equivalencias_completo["distritos"]["ANCO_HUALLO"] = "Anco-Huallo"
    equivalencias_completo["distritos"]["ANCOHUALLO"] = "Anco-Huallo"


    # Sortear subniveles por última vez
    for nivel, dicc in equivalencias_completo.items():
        equivalencias_completo[nivel] = dict(sorted(dicc.items(), key=lambda x: x[0]))

    write_to_resources(equivalencias_completo, "equivalencias")
    write_to_readable(equivalencias_completo, "equivalencias")
    return equivalencias_completo


if __name__ == "__main__":
    crear_equivalencias()
