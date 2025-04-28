from ubigeos_peru import Ubigeo as ubg

assert ubg.get_departamento("1") == "AMAZONAS"
assert ubg.get_departamento(10101) == "AMAZONAS"

assert ubg.normalize_departamento("HUANUCO", upper= False) == "Huánuco"

assert ubg.get_macrorregion("AMAZONAS") == "Oriente"
assert ubg.get_macrorregion("Amazonas") == "Oriente"
assert ubg.get_macrorregion("01") == "Oriente"
assert ubg.get_macrorregion(1) == "Oriente"

assert ubg.get_ubigeo("Lince", "distritos") == "150116"
assert ubg.get_ubigeo("Huaral", "provincia") == "1506"

# pyinstrument -r html -o import_excel_automation.html -c "import ubigeos_peru"