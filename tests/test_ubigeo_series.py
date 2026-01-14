import pytest

import ubigeos_peru as ubg


def test_get_departamento_inei(db_enaho_2024):
    # Crear una copia del dataset para comparar
    df_modified = db_enaho_2024.copy()

    # COPIA: Extraer el departamento a partir del código UBIGEO_HECHO.
    # - normalize=True: normaliza el texto de salida (mayúsculas, tildes, etc.)
    # - divide_lima=True: trata Lima (provincia) de forma separada si corresponde

    # ORIGINAL: Solo validar la columna esperada (DPTO_HECHO) para tener
    # ambas columnas en el mismo formato antes de la comparación.
    df_modified["DEPARTAMENTO"] = ubg.get_departamento(df_modified["UBIGEO"])
    deps_modified = df_modified.drop_duplicates(subset="DEPARTAMENTO")[
        "DEPARTAMENTO"
    ].to_list()
    deps_expected = list(ubg.cargar_diccionario("departamentos")["inei"].values())

    for dep_modified, dep_expected in zip(deps_modified, deps_expected):
        assert dep_modified == dep_expected


def test_get_departamento(db_mininter):
    """
    La idea es aplicar la función get_departamento a "UBIGEO_HECHO" para
    obtener la columna "DEPARTAMENTO", y comparar los resultados con la columna
    ya existente "DPTO_HECHO".
    """
    # Crear una copia del dataset para comparar
    db_copia = db_mininter.copy()

    # COPIA: Extraer el departamento a partir del código UBIGEO_HECHO.
    # - normalize=True: normaliza el texto de salida (mayúsculas, tildes, etc.)
    # - divide_lima=True: trata Lima (provincia) de forma separada si corresponde
    db_copia["DEPARTAMENTO"] = ubg.get_departamento(
        db_mininter["UBIGEO_HECHO"], normalize=True, divide_lima=True
    )

    # ORIGINAL: Solo validar la columna esperada (DPTO_HECHO) para tener
    # ambas columnas en el mismo formato antes de la comparación.
    db_mininter["DPTO_HECHO"] = ubg.validate_departamento(
        db_mininter["DPTO_HECHO"], normalize=True, on_error="ignore"
    )

    # Comparar cada departamento calculado con el esperado.
    for dep_clean, dep_expected in zip(
        db_copia["DEPARTAMENTO"], db_mininter["DPTO_HECHO"]
    ):
        # Saltar los casos de Lima, se manejan aparte
        if "LIMA" in dep_expected:
            continue
        assert dep_clean == dep_expected


def test_get_provincia(db_mininter):
    """
    Misma lógica que test_get_departamento, pero con provincias.
    """
    # Crear una copia del dataset para comparar
    db_copia = db_mininter.copy()

    # COPIA: Extraer la provincia a partir del código UBIGEO_HECHO.
    db_copia["PROVINCIA"] = ubg.get_provincia(db_mininter["UBIGEO_HECHO"])

    # ORIGINAL: Solo validar la columna esperada (PROV_HECHO) para tener
    db_mininter["PROV_HECHO"] = ubg.validate_provincia(
        db_mininter["PROV_HECHO"], on_error="raise"
    )

    # Comparar cada provincia calculada con el esperado.
    for clean, expected in zip(db_copia["PROVINCIA"], db_mininter["PROV_HECHO"]):
        # get_ubigeo devuelve "Nasca", siendo el nombre oficial del INEI,
        # Sin embargo, el dataset lo escribe como "Nazca"
        if clean == "Nasca":
            continue
        assert clean == expected


def test_get_distrito(db_mininter):
    # Crear una copia del dataset para comparar
    db_copia = db_mininter.copy()

    # COPIA: Extraer el distrito a partir del código UBIGEO_HECHO.
    db_copia["DISTRITO"] = ubg.get_distrito(
        db_mininter["UBIGEO_HECHO"], on_error="warn"
    )

    # ORIGINAL: Solo validar la columna esperada (DIST_HECHO)
    db_mininter["DIST_HECHO"] = ubg.validate_distrito(
        db_mininter["DIST_HECHO"], fuzzy_match=False, on_error="coerce"
    )

    # Comparar cada distrito calculada con el esperado.
    for clean, expected in zip(
        db_copia["DISTRITO"],
        db_mininter["DIST_HECHO"],
    ):
        ### ============================================
        ### Algunas observaciones en la base de datos:
        ### ============================================
        # 1) 010207 no existe, en el dataset aparece como El Muyo, pero este es un centro poblado, no un distrito.
        # 2) 150144 no existe. En el dataset aparece como Pueblo Libre.
        # 2) El ubigeo de Pueblo Libre es 150121 (incluso lo colocaron bien antes).
        # 3) Aparece 80912 como Kumpirushiato, pero lo correcto es 080915 (el otro pertenece a Villa Virgen).
        # 4) Aparece 10201 como La Peca, pero el correcto es 10206 (el otro pertenece a Bagua).
        # 5) A propósito, 10206 aparece como Bagua, pero lo correcto es La Peca.
        # 6) get_distrito devuelve "Nasca", siendo el nombre oficial del INEI; sin embargo, el dataset lo escribe como "Nazca"
        # 7) 250305 aparece correctamente como A.VON.HUMBOLDT, pero get_distrito devuelve Alexander Von Humboldt.
        # 8) 100607 aparece como Castillo Grande, pero el correcto es 100608 (el otro pertenece a Pucayacu)
        # 9) 160109 no existe (en el INEI al menos, en la Sunat sí le pertenece a Putumayo)
        # 10) 80911 aparece como Megantoni, pero lo correcto es Inkawasi
        # 11) Santa Lucía aparece sin tilde en el dataset
        if (
            expected == "EL MUYO"
            or expected == "Bagua"
            or expected == "La Peca"
            or expected == "Nazca"
            or expected == "Kumpirushiato"
            or clean == "150144"
            or clean == "010207"
            or clean == "Alexander Von Humboldt"
            or clean == "Pucayacu"
            or clean == "160109"
            or clean == "Pueblo Libre"
            or clean == "Inkawasi"
            or expected == "Santa Lucia"
        ):
            continue
        assert clean == expected


if __name__ == "__main__":
    pytest.main([__file__, "-vs"])

# # Ejecutar todas las pruebas
# pytest -xvs test_ubigeo.py

# # Ejecutar solo las pruebas de un método específico
# pytest -xvs test_ubigeo.py::TestGetMetadato

# # Ejecutar una prueba específica
# pytest -xvs test_ubigeo.py::TestGetDepartamento::test_get_departamento_from_string_code
