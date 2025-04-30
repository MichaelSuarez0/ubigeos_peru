from ubigeos_peru import Ubigeo as ubg

assert ubg.get_departamento("1") == "Amazonas"
assert ubg.get_departamento(10101) == "Amazonas"
assert ubg.get_departamento(10101, no_sp_chars=True) == "amazonas"

assert ubg.get_macrorregion("AMAZONAS") == "Oriente"
assert ubg.get_macrorregion("Amazonas") == "Oriente"
assert ubg.get_macrorregion("01") == "Oriente"
assert ubg.get_macrorregion(1) == "Oriente"

assert ubg.get_ubigeo("Madre de dios", "departamentos") == "17"
assert ubg.get_ubigeo("Huaral", "provincia") == "1506"
assert ubg.get_ubigeo("Lince", "distritos") == "150116"

assert ubg.normalize_ubicacion("Madre de dios") == "Madre de Dios"
assert ubg.validate_departamento("HUANUCO", no_sp_chars= False) == "Huánuco"


# import pandas as pd
# df = pd.DataFrame({
#     "UBIGEO": [10101, 50101, 110101, 150101, 210101],
#     "P1144": [1, 1, 0, 1, 0]
# })

# # Aplicar la función para obtener el departamento
# df["DEPTO"] = df["UBIGEO"].apply(ubg.get_departamento)

# print(df)
# pyinstrument -r html -o import_excel_automation.html -c "import ubigeos_peru"