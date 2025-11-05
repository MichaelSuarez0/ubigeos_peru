"""
Configuración global para pytest
"""

from pathlib import Path

import pandas as pd
import pytest
import inei_tools as inei

DBS_DIR = Path(__file__).parent.resolve() / "test_dbs"


@pytest.fixture
def db_enaho_2024():
    """
    Lee un dataset de ejemplo de la Enaho 01 2024 para pruebas.
    Fuente: https://proyectos.inei.gob.pe/iinei/srienaho/descarga/CSV/966-Modulo01.zip
    """
    
    downloader = inei.Downloader(
        modulos="1",
        anios=2024,
        output_dir=DBS_DIR,
        overwrite=False,
        file_type="csv",
        data_only=True,
    )
    DB_PATH = downloader.download_all()[0]
    

    df = pd.read_csv(
        DB_PATH,
        sep=",",
        usecols=[
            "AÑO",
            "MES",
            "UBIGEO",
            "P22",
        ],
        encoding="latin-1",
    )
    return df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)


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
# def sample_dataframe():
#     """Crea un DataFrame de ejemplo para pruebas"""
#     departamento = [random.randint(1, 25) for _ in range(500)]

#     return pd.DataFrame(
#         {
#             "ubigeo": ,
#         }
#     )
