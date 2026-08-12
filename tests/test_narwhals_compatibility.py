# """
# Tests de compatibilidad con narwhals para verificar que la librería
# funciona correctamente con pandas.Series y polars.Series.

# Estos tests verifican que:
# 1. Al pasar una Series de pandas, devuelve una Series de pandas
# 2. Al pasar una Series de polars, devuelve una Series de polars
# 3. Los valores retornados son correctos en ambos casos
# """

# import pandas as pd
# import polars as pl

# import ubigeos_peru as ubg

# # ============================================================================
# # Tests con pandas.Series
# # ============================================================================


# class TestPandasSeries:
#     """Tests que verifican compatibilidad con pandas.Series"""

#     def test_get_departamento_pandas_series_returns_pandas_series(self):
#         """Verificar que get_departamento devuelve pandas.Series cuando recibe pandas.Series"""
#         ubigeos = pd.Series(["010101", "150131", "080101"])
#         result = ubg.get_departamento(ubigeos)

#         assert isinstance(result, pd.Series), (
#             f"Esperado pandas.Series, recibido {type(result)}"
#         )
#         assert len(result) == 3

#     def test_get_departamento_pandas_series_values_correct(self):
#         """Verificar que los valores de get_departamento son correctos para pandas.Series"""
#         ubigeos = pd.Series(["01", "15", "08"])
#         result = ubg.get_departamento(ubigeos)
#         expected = pd.Series(["Amazonas", "Lima", "Junín"])

#         pd.testing.assert_series_equal(result, expected, check_names=False)

#     def test_get_provincia_pandas_series_returns_pandas_series(self):
#         """Verificar que get_provincia devuelve pandas.Series cuando recibe pandas.Series"""
#         ubigeos = pd.Series(["101", "1506", "0801"])
#         result = ubg.get_provincia(ubigeos)

#         assert isinstance(result, pd.Series), (
#             f"Esperado pandas.Series, recibido {type(result)}"
#         )
#         assert len(result) == 3

#     def test_get_provincia_pandas_series_values_correct(self):
#         """Verificar que los valores de get_provincia son correctos para pandas.Series"""
#         ubigeos = pd.Series(["0101", "1502", "0801"])
#         result = ubg.get_provincia(ubigeos)
#         expected = pd.Series(["Chachapoyas", "Barranca", "Huancayo"])

#         pd.testing.assert_series_equal(result, expected, check_names=False)

#     def test_get_distrito_pandas_series_returns_pandas_series(self):
#         """Verificar que get_distrito devuelve pandas.Series cuando recibe pandas.Series"""
#         ubigeos = pd.Series(["050110", "150131", "080110"])
#         result = ubg.get_distrito(ubigeos)

#         assert isinstance(result, pd.Series), (
#             f"Esperado pandas.Series, recibido {type(result)}"
#         )
#         assert len(result) == 3

#     def test_get_distrito_pandas_series_values_correct(self):
#         """Verificar que los valores de get_distrito son correctos para pandas.Series"""
#         ubigeos = pd.Series(["050110", "150131", "080110"])
#         result = ubg.get_distrito(ubigeos)
#         expected = pd.Series(["San Juan Bautista", "Ancón", "Huancayo"])

#         pd.testing.assert_series_equal(result, expected, check_names=False)


# # ============================================================================
# # Tests con polars.Series
# # ============================================================================


# class TestPolarsSeries:
#     """Tests que verifican compatibilidad con polars.Series"""

#     def test_get_departamento_polars_series_returns_polars_series(self):
#         """Verificar que get_departamento devuelve polars.Series cuando recibe polars.Series"""
#         ubigeos = pl.Series(["010101", "150131", "080101"])
#         result = ubg.get_departamento(ubigeos)

#         assert isinstance(result, pl.Series), (
#             f"Esperado polars.Series, recibido {type(result)}"
#         )
#         assert len(result) == 3

#     def test_get_departamento_polars_series_values_correct(self):
#         """Verificar que los valores de get_departamento son correctos para polars.Series"""
#         ubigeos = pl.Series(["01", "15", "08"])
#         result = ubg.get_departamento(ubigeos)
#         expected = pl.Series(["Amazonas", "Lima", "Junín"])

#         assert result.to_list() == expected.to_list()

#     def test_get_provincia_polars_series_returns_polars_series(self):
#         """Verificar que get_provincia devuelve polars.Series cuando recibe polars.Series"""
#         ubigeos = pl.Series(["101", "1506", "0801"])
#         result = ubg.get_provincia(ubigeos)

#         assert isinstance(result, pl.Series), (
#             f"Esperado polars.Series, recibido {type(result)}"
#         )
#         assert len(result) == 3

#     def test_get_provincia_polars_series_values_correct(self):
#         """Verificar que los valores de get_provincia son correctos para polars.Series"""
#         ubigeos = pl.Series(["0101", "1502", "0801"])
#         result = ubg.get_provincia(ubigeos)
#         expected = pl.Series(["Chachapoyas", "Barranca", "Huancayo"])

#         assert result.to_list() == expected.to_list()

#     def test_get_distrito_polars_series_returns_polars_series(self):
#         """Verificar que get_distrito devuelve polars.Series cuando recibe polars.Series"""
#         ubigeos = pl.Series(["050110", "150131", "080110"])
#         result = ubg.get_distrito(ubigeos)

#         assert isinstance(result, pl.Series), (
#             f"Esperado polars.Series, recibido {type(result)}"
#         )
#         assert len(result) == 3

#     def test_get_distrito_polars_series_values_correct(self):
#         """Verificar que los valores de get_distrito son correctos para polars.Series"""
#         ubigeos = pl.Series(["050110", "150131", "080110"])
#         result = ubg.get_distrito(ubigeos)
#         expected = pl.Series(["San Juan Bautista", "Ancón", "Huancayo"])

#         assert result.to_list() == expected.to_list()


# # ============================================================================
# # Tests con get_ubigeo (requiere conversión inversa)
# # ============================================================================


# class TestGetUbigeoWithPandas:
#     """Tests para get_ubigeo con pandas.Series"""

#     def test_get_ubigeo_from_provincias_pandas_series_returns_pandas_series(self):
#         """Verificar que get_ubigeo devuelve pandas.Series cuando recibe pandas.Series"""
#         provincias = pd.Series(["Chachapoyas", "Barranca", "Huancayo"])
#         result = ubg.UbigeoConverter.get_ubigeo(provincias, "provincias")

#         assert isinstance(result, pd.Series), (
#             f"Esperado pandas.Series, recibido {type(result)}"
#         )
#         assert len(result) == 3

#     def test_get_ubigeo_from_provincias_pandas_series_values_correct(self):
#         """Verificar que los valores de get_ubigeo son correctos para provincias"""
#         provincias = pd.Series(["Chachapoyas", "Barranca", "Huancayo"])
#         result = ubg.UbigeoConverter.get_ubigeo(provincias, "provincias")
#         expected = pd.Series(["0101", "1502", "0801"])

#         pd.testing.assert_series_equal(result, expected, check_names=False)

#     def test_get_ubigeo_from_distritos_pandas_series_returns_pandas_series(self):
#         """Verificar que get_ubigeo devuelve pandas.Series cuando recibe pandas.Series"""
#         distritos = pd.Series(["San Juan Bautista", "Ancón", "Huancayo"])
#         result = ubg.UbigeoConverter.get_ubigeo(distritos, "distritos")

#         assert isinstance(result, pd.Series), (
#             f"Esperado pandas.Series, recibido {type(result)}"
#         )
#         assert len(result) == 3

#     def test_get_ubigeo_from_distritos_pandas_series_values_correct(self):
#         """Verificar que los valores de get_ubigeo son correctos para distritos"""
#         distritos = pd.Series(["San Juan Bautista", "Ancón", "Huancayo"])
#         result = ubg.UbigeoConverter.get_ubigeo(distritos, "distritos")
#         expected = pd.Series(["050110", "150131", "080110"])

#         pd.testing.assert_series_equal(result, expected, check_names=False)


# class TestGetUbigeoWithPolars:
#     """Tests para get_ubigeo con polars.Series"""

#     def test_get_ubigeo_from_provincias_polars_series_returns_polars_series(self):
#         """Verificar que get_ubigeo devuelve polars.Series cuando recibe polars.Series"""
#         provincias = pl.Series(["Chachapoyas", "Barranca", "Huancayo"])
#         result = ubg.UbigeoConverter.get_ubigeo(provincias, "provincias")

#         assert isinstance(result, pl.Series), (
#             f"Esperado polars.Series, recibido {type(result)}"
#         )
#         assert len(result) == 3

#     def test_get_ubigeo_from_provincias_polars_series_values_correct(self):
#         """Verificar que los valores de get_ubigeo son correctos para provincias"""
#         provincias = pl.Series(["Chachapoyas", "Barranca", "Huancayo"])
#         result = ubg.UbigeoConverter.get_ubigeo(provincias, "provincias")
#         expected = pl.Series(["0101", "1502", "0801"])

#         assert result.to_list() == expected.to_list()

#     def test_get_ubigeo_from_distritos_polars_series_returns_polars_series(self):
#         """Verificar que get_ubigeo devuelve polars.Series cuando recibe polars.Series"""
#         distritos = pl.Series(["San Juan Bautista", "Ancón", "Huancayo"])
#         result = ubg.UbigeoConverter.get_ubigeo(distritos, "distritos")

#         assert isinstance(result, pl.Series), (
#             f"Esperado polars.Series, recibido {type(result)}"
#         )
#         assert len(result) == 3

#     def test_get_ubigeo_from_distritos_polars_series_values_correct(self):
#         """Verificar que los valores de get_ubigeo son correctos para distritos"""
#         distritos = pl.Series(["San Juan Bautista", "Ancón", "Huancayo"])
#         result = ubg.UbigeoConverter.get_ubigeo(distritos, "distritos")
#         expected = pl.Series(["050110", "150131", "080110"])

#         assert result.to_list() == expected.to_list()


# # ============================================================================
# # Tests de compatibilidad cruzada (DataFrame operations)
# # ============================================================================


# class TestPandasDataFrameIntegration:
#     """Tests que verifican que las Series funcionan correctamente dentro de DataFrames de pandas"""

#     def test_add_departamento_column_to_pandas_dataframe(self):
#         """Verificar que se puede agregar una columna de departamentos a un DataFrame de pandas"""
#         df = pd.DataFrame({"ubigeo": ["010101", "150131", "080101"]})
#         df["departamento"] = ubg.get_departamento(df["ubigeo"])

#         assert isinstance(df["departamento"], pd.Series)
#         assert df["departamento"].tolist() == ["Amazonas", "Lima", "Junín"]

#     def test_add_multiple_geocoding_columns_pandas_dataframe(self):
#         """Verificar que se pueden agregar múltiples columnas de geocodificación a un DataFrame de pandas"""
#         df = pd.DataFrame({"ubigeo": ["150131", "080110", "050110"]})
#         df["departamento"] = ubg.get_departamento(df["ubigeo"])
#         df["provincia"] = ubg.get_provincia(df["ubigeo"])
#         df["distrito"] = ubg.get_distrito(df["ubigeo"])

#         assert len(df) == 3
#         assert list(df.columns) == ["ubigeo", "departamento", "provincia", "distrito"]
#         assert df["distrito"].tolist() == ["Ancón", "Huancayo", "San Juan Bautista"]


# class TestPolarsDataFrameIntegration:
#     """Tests que verifican que las Series funcionan correctamente dentro de DataFrames de polars"""

#     def test_add_departamento_column_to_polars_dataframe(self):
#         """Verificar que se puede agregar una columna de departamentos a un DataFrame de polars"""
#         df = pl.DataFrame({"ubigeo": ["010101", "150131", "080101"]})
#         df = df.with_columns(departamento=ubg.get_departamento(df["ubigeo"]))

#         assert "departamento" in df.columns
#         assert df["departamento"].to_list() == ["Amazonas", "Lima", "Junín"]

#     def test_add_multiple_geocoding_columns_polars_dataframe(self):
#         """Verificar que se pueden agregar múltiples columnas de geocodificación a un DataFrame de polars"""
#         df = pl.DataFrame({"ubigeo": ["150131", "080110", "050110"]})
#         df = df.with_columns(
#             departamento=ubg.get_departamento(df["ubigeo"]),
#             provincia=ubg.get_provincia(df["ubigeo"]),
#             distrito=ubg.get_distrito(df["ubigeo"]),
#         )

#         assert len(df) == 3
#         assert set(df.columns) == {"ubigeo", "departamento", "provincia", "distrito"}
#         assert df["distrito"].to_list() == ["Ancón", "Huancayo", "San Juan Bautista"]
