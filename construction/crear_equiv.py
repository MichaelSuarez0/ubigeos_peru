import orjson
from _utils import (
    RESOURCES_PATH,
    eliminar_acentos,
    write_to_readable,
    write_to_resources,
)


def crear_equivalencias():
    niveles = ["departamentos", "provincias", "distritos"]
    equivalencias_full = {}
    for nivel in niveles:
        with open(RESOURCES_PATH / f"{nivel}.json", mode="rb") as f:
            existing_dict = orjson.loads(f.read())

        values = existing_dict["inei"].values()
        equivalencias = {eliminar_acentos(v).upper(): v for v in values}
        equivalencias = dict(sorted(equivalencias.items(), key=lambda x: x[0]))
        equivalencias_full[nivel] = equivalencias

    # Añadir
    # Departamentos
    equivalencias_full["departamentos"]["CUZCO"] = "Cusco"
    equivalencias_full["departamentos"]["LIMA METROPOLITANA"] = "Lima Metropolitana"
    equivalencias_full["departamentos"]["LIMA REGION"] = "Lima Región"
    equivalencias_full["departamentos"]["REGION LIMA"] = "Lima Región"

    # Provincias
    equivalencias_full["provincias"]["CUZCO"] = "Cusco"
    equivalencias_full["provincias"]["NAZCA"] = "Nazca"
    equivalencias_full["provincias"]["NASCA"] = "Nasca"
    equivalencias_full["provincias"]["ANTONIO RAIMONDI"] = "Antonio Raymondi"

    # Distritos
    equivalencias_full["distritos"]["CUZCO"] = "Cusco"
    equivalencias_full["distritos"]["26 DE OCTUBRE"] = "Veintiséis de Octubre"
    equivalencias_full["distritos"]["27 DE NOVIEMBRE"] = "Veintisiete de Noviembre"
    equivalencias_full["distritos"]["ANDRES AVELINO CACERES"] = (
        "Andrés Avelino Cáceres Dorregaray"
    )
    equivalencias_full["distritos"]["ANCO_HUALLO"] = "Anco-Huallo"
    equivalencias_full["distritos"]["ANCO HUALLO"] = "Anco-Huallo"
    equivalencias_full["distritos"]["ANCOHUALLO"] = "Anco-Huallo"
    equivalencias_full["distritos"]["LURIGANCHO - CHOSICA"] = "Lurigancho"
    equivalencias_full["distritos"]["RAYMONDI"] = "Raimondi"
    equivalencias_full["distritos"]["PALMAPAMPA"] = "Samugari"
    equivalencias_full["distritos"]["MILPUCC"] = "Milpuc"
    equivalencias_full["distritos"]["SAN FRANCISCO DE YESO"] = "San Francisco del Yeso"
    equivalencias_full["distritos"]["SAN FRANCISCO DEL YESO"] = "San Francisco del Yeso"
    equivalencias_full["distritos"]["HUAYLLO"] = "Ihuayllo"
    equivalencias_full["distritos"]["HUAILLATI"] = "Huayllati"
    equivalencias_full["distritos"]["MARISCAL GAMARRA"] = "Mariscal Gamarra"
    equivalencias_full["distritos"]["SANTA RITA DE SIHUAS"] = "Santa Rita de Siguas"
    equivalencias_full["distritos"]["SAN FRANCISCO DE RAVACAYCO"] = "San Francisco de Rivacayco"
    equivalencias_full["distritos"]["PION"] = "Pion"
    equivalencias_full["distritos"]["HUALLAY-GRANDE"] = "Huallay Grande"
    equivalencias_full["distritos"]["QUITO ARMA"] = "Quito-Arma"
    equivalencias_full["distritos"]["TOMAY-KICHWA"] = "Tomay Kichwa"
    equivalencias_full["distritos"]["SAN JUAN DE YSCOS"] = "San Juan de Iscos"
    equivalencias_full["distritos"]["HUAY HUAY"] = "Huay-Huay"
    equivalencias_full["distritos"]["CASTA"] = "San Pedro de Casta"
    equivalencias_full["distritos"]["SAN JOSE DE LOS CHORRILLOS"] = "San José de los Chorrillos"
    equivalencias_full["distritos"]["HUAYA"] = "Hualla"
    equivalencias_full["distritos"]["DANIEL ALOMIAS ROBLES"] = "Daniel Alomia Robles"
    equivalencias_full["distritos"]["AYAUCA"] = "ALLAUCA"
    equivalencias_full["distritos"]["CARMEN DE LA LEGUA"] = "CARMEN DE LA LEGUA REYNOSO"


    # Sortear subniveles por última vez
    for nivel, dicc in equivalencias_full.items():
        equivalencias_full[nivel] = dict(sorted(dicc.items(), key=lambda x: x[0]))

    write_to_resources(equivalencias_full, "equivalencias")
    write_to_readable(equivalencias_full, "equivalencias")
    return equivalencias_full


if __name__ == "__main__":
    crear_equivalencias()
