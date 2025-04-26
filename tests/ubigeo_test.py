from ubigeos_peru import Ubigeo as ubg

assert ubg.get_departamento("1") == "AMAZONAS"
assert ubg.get_departamento(10101) == "AMAZONAS"

assert ubg.normalize_departamento("HUANUCO", upper= False) == "Huánuco"

# pyinstrument -r html -o import_excel_automation.html -c "import ubigeos_peru"