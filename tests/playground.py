import pandas as pd

import ubigeos_peru as ubg

# AGREGAR DISTRITOS 26 DE OCTUBRE PIURA
"AÑO,MES,UBIGEO_HECHO,DPTO_HECHO,PROV_HECHO,DIST_HECHO,SEXO,RANGO_EDAD,NACIONALIDAD,CANTIDAD"
desaparecidos = pd.read_csv(
    r"C:\Users\micha\Downloads\DATASET_Personas_Desaparecidas_Enero 2019 a Julio 2025.csv"
)
# print(desaparecidos)
desaparecidos["DPTO_HECHO"] = ubg.validate_departamento(
    desaparecidos["DPTO_HECHO"], on_error="capitalize"
)
desaparecidos["PROV_HECHO"] = ubg.validate_ubicacion(
    desaparecidos["PROV_HECHO"], on_error="capitalize"
)

desaparecidos["LATITUD"] = ubg.get_metadato(
    desaparecidos["DIST_HECHO"], level="distritos", key="latitud"
)
desaparecidos["LONGITUD"] = ubg.get_metadato(
    desaparecidos["DIST_HECHO"], level="distritos", key="longitud"
)

desaparecidos["REGIÓN"] = ubg.get_macrorregion(desaparecidos["DPTO_HECHO"])


desaparecidos = desaparecidos.sort_values(
    by=["AÑO", "UBIGEO_HECHO"], axis=0, ascending=False
)
desaparecidos.to_csv(
    r"C:\Users\micha\Downloads\DATASET_Personas_Desaparecidas_Enero 2019 a Julio 2025_LIMPIO_DIST.csv",
    index=False,
    encoding="utf-8-sig",
)
desaparecidos.to_excel(
    r"C:\Users\micha\Downloads\DATASET_Personas_Desaparecidas_Enero 2019 a Julio 2025_LIMPIO_DIST.xlsx",
    index=False,
)

# print(ubg.get_metadato("Lince", level="distritos", key="latitud"))

# def test_get_macrorregion_from_uppercase_name(self):
#     assert ubg.get_macrorregion("AMAZONAS") == "Oriente"

# def test_get_macrorregion_from_code(self):
#     assert ubg.get_macrorregion("01") == "Oriente"
