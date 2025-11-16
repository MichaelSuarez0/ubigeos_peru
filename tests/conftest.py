"""
Configuración global para pytest
"""

from pathlib import Path

# import inei_tools as inei
import pandas as pd
import pytest

DBS_DIR = Path(__file__).parent.resolve() / "test_dbs"


@pytest.fixture
def fuzzy_match_test_cases():
    """
    Proporciona casos de prueba para pruebas de coincidencia difusa.
    """
    return {
        "departamentos": {
            "CUZCO": "Cusco",
            "LIMA METROPOLITANA": "Lima Metropolitana",
            "LIMA REGION": "Lima Región",
            "REGION LIMA": "Lima Región",
        },
        "provincias": {
            "CUZCO": "Cusco",
            "NAZCA": "Nazca",
            "NASCA": "Nasca",
            "ANTONIO RAIMONDI": "Antonio Raymondi",
        },
        "distritos": {
            "CUZCO": "Cusco",
            "26 DE OCTUBRE": "Veintiséis de Octubre",
            "27 DE NOVIEMBRE": "Veintisiete de Noviembre",
            "ANDRES AVELINO CACERES": "Andrés Avelino Cáceres Dorregaray",
            "ANCO_HUALLO": "Anco-Huallo",
            "ANCO HUALLO": "Anco-Huallo",
            "ANCOHUALLO": "Anco-Huallo",
            "LURIGANCHO - CHOSICA": "Lurigancho",
            "RAYMONDI": "Raimondi",
            "PALMAPAMPA": "Samugari",
            "MILPUCC": "Milpuc",
            "SAN FRANCISCO DE YESO": "San Francisco del Yeso",
            "HUAYLLO": "Ihuayllo",
            "HUAILLATI": "Huayllati",
            "MARISCAL GAMARRA": "Mariscal Gamarra",
            "SANTA RITA DE SIHUAS": "Santa Rita de Siguas",
            "SAN FRANCISCO DE RAVACAYCO": "San Francisco de Rivacayco",
            "PION": "Pion",
            "HUALLAY-GRANDE": "Huallay Grande",
            "QUITO ARMA": "Quito-Arma",
            "TOMAY-KICHWA": "Tomay Kichwa",
            "SAN JUAN DE YSCOS": "San Juan de Iscos",
            "HUAY HUAY": "Huay-Huay",
            "CASTA": "San Pedro de Casta",
            "SAN JOSE DE LOS CHORRILLOS": "San José de los Chorrillos",
            "HUAYA": "Hualla",
            "DANIEL ALOMIAS ROBLES": "Daniel Alomia Robles",
            "AYAUCA": "ALLAUCA",
            "CARMEN DE LA LEGUA": "Carmen de la Legua Reynoso",
        },
    }


@pytest.fixture
def db_mininter():
    """
    Lee un dataset de ejemplo del Mininter para pruebas
    Fuente: https://datosabiertos.gob.pe/dataset/personas-desaparecidas/resource/f49ae77f-8822-45ea-aa16-911d677e303d
    """

    df = pd.read_csv(
        DBS_DIR / "mininter_personas_desaparecidas.csv",
        sep=",",
        usecols=[
            "AÑO",
            "MES",
            "UBIGEO_HECHO",
            "DPTO_HECHO",
            "PROV_HECHO",
            "DIST_HECHO",
        ],
        encoding="utf-8-sig",
    )
    return df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)


@pytest.fixture
def db_minam():
    """
    Lee un dataset de ejemplo del MINAM para pruebas
    Fuente: https://datosabiertos.gob.pe/dataset/valorizaci%C3%B3n-de-residuos-s%C3%B3lidos-nivel-distrital-ministerio-del-ambiente-minam
    Nota: Esta data tiene fallas, pues en algún punto la columna "DEPARTAMENTO" y "REG_NAT" están mezcladas.
    """

    df = pd.read_csv(
        DBS_DIR / "minam_valorizacion_residuos.csv",
        sep=";",
        usecols=["UBIGEO", "REG_NAT", "DEPARTAMENTO", "PROVINCIA", "DISTRITO"],
    )
    return df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)


# @pytest.fixture
# def db_enaho_2024():
#     """
#     Lee un dataset de ejemplo de la Enaho 01 2024 para pruebas.
#     Fuente: https://proyectos.inei.gob.pe/iinei/srienaho/descarga/CSV/966-Modulo01.zip
#     """

#     downloader = inei.Downloader(
#         modulos="1",
#         anios=2024,
#         output_dir=DBS_DIR,
#         overwrite=False,
#         file_type="csv",
#         data_only=True,
#     )
#     DB_PATH = downloader.download_all()[0]

#     df = pd.read_csv(
#         DB_PATH,
#         sep=",",
#         usecols=[
#             "AÑO",
#             "MES",
#             "UBIGEO",
#             "P22",
#         ],
#         encoding="latin-1",
#     )
#     return df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

# @pytest.fixture
# def sample_dataframe():
#     """Crea un DataFrame de ejemplo para pruebas"""
#     departamento = [random.randint(1, 25) for _ in range(500)]

#     return pd.DataFrame(
#         {
#             "ubigeo": ,
#         }
#     )
