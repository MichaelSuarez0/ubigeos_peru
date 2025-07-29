import ubigeos_peru as ubg
import pytest

class TestGetDepartamento:
    def test_get_departamento_from_string_code(self):
        assert ubg.get_departamento("1") == "Amazonas"
        
    def test_get_departamento_from_complete_code(self):
        assert ubg.get_departamento("010101") == "Amazonas"
        
    def test_get_departamento_from_integer(self):
        assert ubg.get_departamento(10101) == "Amazonas"
        
    def test_get_departamento_normalized(self):
        assert ubg.get_departamento(10101, normalize=True) == "AMAZONAS"

class TestGetProvincia:
    def test_get_provincia_from_string_code(self):
        assert ubg.get_provincia("101") == "Chachapoyas"
        
    def test_get_provincia_from_integer(self):
        assert ubg.get_provincia(1506) == "Huaral"
        
    def test_get_provincia_normalized(self):
        assert ubg.get_provincia("101", normalize=True) == "CHACHAPOYAS"

class TestGetDistrito:
    def test_get_distrito_from_string_code(self):
        assert ubg.get_distrito("50110") == "San Juan Bautista"
        
    def test_get_distrito_from_integer(self):
        assert ubg.get_distrito(150110) == "Comas"
        
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

class TestGetMacrorregionMap:
    pass

class TestGetUbigeo:
    def test_get_ubigeo_departamento(self):
        assert ubg.get_ubigeo("Madre de dios", "departamentos") == "17"
        
    def test_get_ubigeo_provincia(self):
        assert ubg.get_ubigeo("Huaral", "provincia") == "1506"
        
    def test_get_ubigeo_distrito(self):
        assert ubg.get_ubigeo("Lince", "distritos") == "150116"
    
    def test_get_ubigeo_distrito_badly_written(self):
        assert ubg.get_ubigeo("Mi peru", "distritos") == "070107"

    def test_get_ubigeo_distrito_from_diff_institution(self):
        assert ubg.get_ubigeo("Mi peru", "distritos", "reniec") == "240107"


class TestValidateDepartamento:
    def test_validate_departamento_basic(self):
        assert ubg.validate_departamento("HUANUCO") == "Huánuco"
        
    def test_validate_departamento_normalized(self):
        assert ubg.validate_departamento("HUÁNUCO", normalize=True) == 'HUANUCO'
        
    def test_validate_departamento_normalized_lowercase(self):
        assert ubg.validate_departamento("HUÁNUCO", normalize=True).lower() == 'huanuco'

    def test_validate_departamento_on_error_capitalize(self):
        assert ubg.validate_departamento("ARICA", on_error="capitalize") == "Arica"
        assert ubg.validate_departamento("otra region", on_error="capitalize") == "Otra region"

    def test_validate_departamento_on_error_ignore(self):
        # Asegurar que 'ignore' funcione con normalize
        assert ubg.validate_departamento("ARICA", on_error="ignore") == "ARICA"
        assert ubg.validate_departamento("OtraRegion", normalize=True, on_error="ignore") == "OTRAREGION"
    

class TestValidateUbicacion:
    def test_validate_ubicacion_space(self):
        assert ubg.validate_ubicacion("Madre de dios") == "Madre de Dios"
    
    def test_validate_ubicacion_space_sp_char(self):
        assert ubg.validate_ubicacion("SAN MARTIN") == "San Martín"


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

class TestWrongInputs:
    """Tests para inputs incorrectos en get_departamento"""
    
    def test_get_departamento_invalid_type_none(self):
        with pytest.raises(TypeError):
            ubg.get_departamento(None)
    
    def test_get_departamento_invalid_type_list(self):
        with pytest.raises(TypeError):
            ubg.get_departamento([1, 2, 3])
    
    def test_get_departamento_invalid_type_dict(self):
        with pytest.raises(TypeError):
            ubg.get_departamento({"codigo": "01"})
    
    def test_get_departamento_invalid_type_float(self):
        with pytest.raises(TypeError):
            ubg.get_departamento(1.5)
    
    def test_get_departamento_too_long_code(self):
        with pytest.raises(ValueError):
            ubg.get_departamento("1234567")
    
    def test_get_departamento_nonexistent_code(self):
        with pytest.raises(KeyError):
            ubg.get_departamento("99")
    
    def test_get_departamento_invalid_institution(self):
        with pytest.raises(KeyError):
            ubg.get_departamento("01", institucion="invalid")
    

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# # Ejecutar todas las pruebas
# pytest -xvs test_ubigeo.py

# # Ejecutar solo las pruebas de un método específico
# pytest -xvs test_ubigeo.py::TestGetMetadato

# # Ejecutar una prueba específica
# pytest -xvs test_ubigeo.py::TestGetDepartamento::test_get_departamento_from_string_code