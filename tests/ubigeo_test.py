from ubigeos_peru import Ubigeo as ubg
#import pytest

class TestGetDepartamento:
    def test_get_departamento_from_string_code(self):
        assert ubg.get_departamento("1") == "Amazonas"
        
    def test_get_departamento_from_complete_code(self):
        assert ubg.get_departamento("010101") == "Amazonas"
        
    def test_get_departamento_from_integer(self):
        assert ubg.get_departamento(10101) == "Amazonas"
        
    def test_get_departamento_normalized(self):
        assert ubg.get_departamento(10101, normalize=True) == "AMAZONAS"


class TestGetMacrorregion:
    def test_get_macrorregion_from_name(self):
        assert ubg.get_macrorregion("Amazonas") == "Oriente"
        
    def test_get_macrorregion_from_uppercase_name(self):
        assert ubg.get_macrorregion("AMAZONAS") == "Oriente"
        
    def test_get_macrorregion_from_code(self):
        assert ubg.get_macrorregion("01") == "Oriente"
        
    def test_get_macrorregion_from_integer(self):
        assert ubg.get_macrorregion(1) == "Oriente"
        
    def test_get_macrorregion_with_institution(self):
        assert ubg.get_macrorregion("Ucayali", institucion="ceplan") == "Nororiente"
        
    def test_get_macrorregion_with_institution_from_integer(self):
        assert ubg.get_macrorregion(25, institucion="ceplan") == "Nororiente"


class TestGetUbigeo:
    def test_get_ubigeo_departamento(self):
        assert ubg.get_ubigeo("Madre de dios", "departamentos") == "17"
        
    def test_get_ubigeo_provincia(self):
        assert ubg.get_ubigeo("Huaral", "provincia") == "1506"
        
    def test_get_ubigeo_distrito(self):
        assert ubg.get_ubigeo("Lince", "distritos") == "150116"


class TestValidateDepartamento:
    def test_validate_departamento_basic(self):
        assert ubg.validate_departamento("HUANUCO") == "Huánuco"
        
    def test_validate_departamento_normalized(self):
        assert ubg.validate_departamento("HUÁNUCO", normalize=True) == 'HUANUCO'
        
    def test_validate_departamento_normalized_lowercase(self):
        assert ubg.validate_departamento("HUÁNUCO", normalize=True).lower() == 'huanuco'


class TestValidateUbicacion:
    def test_validate_ubicacion_basic(self):
        assert ubg.validate_ubicacion("Madre de dios") == "Madre de Dios"


class TestGetMetadato:
    def test_get_metadato_departamento_capital(self):
        assert ubg.get_metadato("La libertad", level="departamentos", key="capital") == "Trujillo"
        
    def test_get_metadato_provincia_capital(self):
        assert ubg.get_metadato("Huarochiri", level="provincias", key="capital") == "Matucana"
        
    def test_get_metadato_departamento_altitud(self):
        assert ubg.get_metadato("Cusco", level="departamento", key="altitud") == "3439"
        
    def test_get_metadato_provincia_altitud(self):
        assert ubg.get_metadato("Huarochiri", level="provincia", key="altitud") == "2395"
        
    def test_get_metadato_distrito_superficie_lince(self):
        assert ubg.get_metadato("Lince", level="distritos", key="superficie") == "3.03"
        
    def test_get_metadato_distrito_superficie_san_isidro(self):
        assert ubg.get_metadato("San Isidro", level="distritos", key="superficie") == "11.1"
        
    def test_get_metadato_distrito_superficie_sjl(self):
        assert ubg.get_metadato("San Juan de Lurigancho", level="distritos", key="superficie") == "131.25"


# Performance: pyinstrument -r html -o import_excel_automation.html -c "import ubigeos_peru"
# # Ejecutar todas las pruebas
# pytest -xvs ubigeo_test.py

# # Ejecutar solo las pruebas de un método específico
# pytest -xvs ubigeo_test.py::TestGetMetadato

# # Ejecutar una prueba específica
# pytest -xvs ubigeo_test.py::TestGetDepartamento::test_get_departamento_from_string_code