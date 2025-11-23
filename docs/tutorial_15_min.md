# Tutorial en 15 minutos

## Convertir departamentos

Convertir ubigeos con `ubigeos_peru` solo toma un par de líneas, y no se necesita conocimientos extensos de Python.

Antes de comenzar, asegúrate de haber instalado la librería con el siguiente comando:

```shell
pip install ubigeos-peru
```

Vamos a comenzar creando un DataFrame de prueba.

Abre tu editor de Python preferido, crea un archivo ``main.py`` file y copia el siguiente código:

<!--**Integración con Pandas: insertar una columna (Serie) de departamentos** -->
```py
import pandas as pd
import ubigeos_peru as ubg

df = pd.DataFrame({
    "UBIGEO": [10516, 40118, 150140, 151010, 170101, 200701, 220101],
    "P1144": [1, 0, 1, 1, 0, 1, 0]
})
print(df)
```
**Resultado:**

| UBIGEO | P1144 |
|--------|-------|
| 10516  | 1     |
| 40118  | 0     |
| 150140 | 1     |
| 151010 | 0     |
| 170101 | 0     |
| 200701 | 1     |
| 220101 | 0     |

Para convertir ubigeos a departamentos, simplemente pasamos la columna (Serie) de ubigeos a `get_departamento`.

Lo guardamos en una columna nueva para nuestro DataFrame.

```py
df["DPTO"] = ubg.get_departamento(df["UBIGEO"])
df
```
**Resultado:**

| UBIGEO | P1144 | DPTO          |
|--------|-------|---------------|
| 10516  | 1     | Amazonas      |
| 40118  | 0     | Arequipa      |
| 150140 | 1     | Lima          |
| 151010 | 0     | Lima          |
| 170101 | 0     | Madre de Dios |
| 200701 | 1     | Piura         |
| 220101 | 0     | San Martín    |

Podemos personalizar el output con dos parámetros adicionales.

### Cambiar de institución

Por defecto, `get_departamento` usa la base de datos del INEI, pero podemos cambiar a la Reniec con el argumento `institucion`:

```py
df["DPTO"] = ubg.get_departamento(df["UBIGEO"], institucion="reniec")
print(df)
```

| UBIGEO | P1144 | DPTO          |
|--------|-------|---------------|
| 10516  | 1     | Amazonas      |
| 40118  | 0     | Arequipa      |
| 150140 | 1     | Loreto        |
| 151010 | 0     | Loreto        |
| 170101 | 0     | Moquegua      |
| 200701 | 1     | Puno          |
| 220101 | 0     | Tacna         |

Actualmente, esta librería solo ofrece soporte actualizado al 2025 para los ubigeos del INEI y la Reniec. 

La librería también ofrece soporte para la Sunat, pero la base de datos está actualizada al 2019, y no está lista para producción.

### Normalizar nombres
El argumento `normalize` convierte los resultados en mayúsculas y quita los acentos.

```py
df["DPTO"] = ubg.get_departamento(df["UBIGEO"], normalize=True)
print(df)
```

| UBIGEO | P1144 | DPTO          |
|--------|-------|---------------|
| 10516  | 1     | AMAZONAS      |
| 40118  | 0     | AREQUIPA      |
| 150140 | 1     | LIMA          |
| 151010 | 0     | LIMA          |
| 170101 | 0     | MADRE DE DIOS |
| 200701 | 1     | PIURA         |
| 220101 | 0     | SAN MARTIN    |

### Diferenciar Lima Metropolitana de Lima Región

Por defecto, `get_departamento` no diferencia Lima de Lima Metropolitana o Lima Región, pero podemos cambiar su comportamiento determinado con el argumento `divide_lima`:

```py
df["DPTO"] = ubg.get_departamento(df["UBIGEO"], divide_lima=True)
df
```

| UBIGEO | P1144 | DPTO               |
|--------|-------|--------------------|
| 10516  | 1     | Amazonas           |
| 40118  | 0     | Arequipa           |
| 150140 | 1     | Lima Metropolitana |
| 151010 | 0     | Lima Región        |
| 170101 | 0     | Madre de Dios      |
| 200701 | 1     | Piura              |
| 220101 | 0     | San Martín         |


## Convertir provincias y distritos

Convertir provincias y distritos es el mismo procedimiento que convertir departamentos (y los mismos argumentos). Lo único que cambia es el nombre de la función.

```python
df["PROVINCIA"] = ubg.get_provincia(df["UBIGEO"])
df["DISTRITO"] = ubg.get_distrito(df["UBIGEO"])
```


| UBIGEO | P1144 | DPTO          | PROVINCIA  | DISTRITO            |
|--------|-------|---------------|------------|---------------------|
| 10516  | 1     | Amazonas      | Luya       | San Cristóbal       |
| 40118  | 0     | Arequipa      | Arequipa   | San Juan de Siguas  |
| 150140 | 1     | Lima          | Lima       | Santiago de Surco   |
| 151010 | 0     | Lima          | Yauyos     | Cochas              |
| 170101 | 0     | Madre de Dios | Tambopata  | Tambopata           |
| 200701 | 1     | Piura         | Talara     | Pariñas             |
| 220101 | 0     | San Martín    | Moyobamba  | Moyobamba           |
