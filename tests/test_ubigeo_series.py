import pytest

import ubigeos_peru as ubg


def test_get_departamento(db_mininter):
    # Crear una copia del dataset para comparar
    dataset_limpio = db_mininter.copy()

    # COPIA: Extraer el departamento a partir del código UBIGEO_HECHO.
    # - normalize=True: normaliza el texto de salida (mayúsculas, tildes, etc.)
    # - divide_lima=True: trata Lima (provincia) de forma separada si corresponde
    dataset_limpio["DEPARTAMENTO"] = ubg.get_departamento(
        db_mininter["UBIGEO_HECHO"], normalize=True, divide_lima=True
    )

    # ORIGINAL: Solo validar la columna esperada (DPTO_HECHO) para tener
    # ambas columnas en el mismo formato antes de la comparación.
    db_mininter["DPTO_HECHO"] = ubg.validate_departamento(
        db_mininter["DPTO_HECHO"], normalize=True, on_error="ignore")

    # Comparar cada departamento calculado con el esperado.
    for dep_clean, dep_expected in zip(
        dataset_limpio["DEPARTAMENTO"], db_mininter["DPTO_HECHO"]
    ):
        # Saltar los casos de Lima, se manejan aparte
        if "LIMA" in dep_expected:
            continue
        assert dep_clean == dep_expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# # Ejecutar todas las pruebas
# pytest -xvs test_ubigeo.py

# # Ejecutar solo las pruebas de un método específico
# pytest -xvs test_ubigeo.py::TestGetMetadato

# # Ejecutar una prueba específica
# pytest -xvs test_ubigeo.py::TestGetDepartamento::test_get_departamento_from_string_code
