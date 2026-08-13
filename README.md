# Ubigeos Perú

[![PyPI version](https://img.shields.io/pypi/v/ubigeos-peru?color=blue)](https://pypi.org/project/ubigeos-peru/)
[![Downloads](https://img.shields.io/pypi/dm/ubigeos-peru)](https://pypi.org/project/ubigeos-peru/)
[![GitHub stars](https://img.shields.io/github/stars/MichaelSuarez0/ubigeos_peru?style=social)](https://github.com/MichaelSuarez0/ubigeos_peru/stargazers)

Librería de Python que convierte códigos de ubigeo en su correspondiente departamento, provincia o distrito, y viceversa. Incluye métodos clave para limpiar y validar nombres oficiales, consultar macrorregiones, coordenadas geográficas, etc. 

Se integra fácilmente con `pandas` y `polars` para procesar bases de datos peruanas como la **ENAHO**.

## Ejemplo rápido

Un caso típico: tienes un módulo de la ENAHO con la columna `UBIGEO` y quieres 
saber a qué departamento y provincia pertenece cada observación:

```py
import pandas as pd
import ubigeos_peru as ubg

# Módulo 100 de la ENAHO
df = pd.read_csv("enaho01-2024-100.csv")

df["DEPARTAMENTO"] = ubg.get_departamento(df["UBIGEO"])
df["PROVINCIA"] = ubg.get_provincia(df["UBIGEO"])

print(df[["UBIGEO", "DEPARTAMENTO", "PROVINCIA"]].head())
```

```
   UBIGEO DEPARTAMENTO    PROVINCIA
0   10101     Amazonas  Chachapoyas
1  150101         Lima         Lima
2  080101        Cusco        Cusco
3  100101      Huánuco      Huánuco
```

La librería también permite normalizar automáticamente los nombres oficiales:

```python
ubg.validate_departamento("HUANUCO")          # "Huánuco"
ubg.validate_departamento(df["DEPARTAMENTO"]) # Normaliza todos
```

Sin `ubigeos_peru`, tendrías que descargar un diccionario de ubigeos aparte y 
hacer el merge manualmente, lidiando con inconsistencias de versiones, instituciones, tildes o mayúsculas. 

## Bases de datos

Las fuentes o bases de datos de ubigeos:
- **[ubigeos_inei_2025](https://github.com/MichaelSuarez0/ubigeos_peru/blob/main/databases/ubigeo_inei_2025.csv)**: 
  - Fuente: limpieza del Directorio Nacional de Gobiernos Regionales, Municipalidades Provinciales, Distritales y de Centros Poblados 2025 (Cuadros en Excel).
  - [Script y detalles aquí](https://github.com/MichaelSuarez0/ubigeos_peru/blob/main/construction/crear_ubigeo_inei.py)
  
- **[ubigeos_reniec_2025](https://github.com/MichaelSuarez0/ubigeos_peru/blob/main/databases/ubigeo_reniec_2025.csv)**: 
  - Fuente: solicitud de acceso a la información pública. SOLICITUD DE REGISTRO Nº 1931-2025.
  - [Script y detalles aquí](https://github.com/MichaelSuarez0/ubigeos_peru/blob/main/construction/crear_ubigeo_reniec.py)

## Características Principales

- **Soporte Multi-institucional**: Soporte para consultar códigos de ubigeo de INEI y Reniec.
- **Normalización Inteligente**: Manejo automático de acentos y mayúsculas para validar ubicaciones.
- **Optimizado para Big Data**: 1 000 000 consultas en menos de 1 segundo.
- **Carga Diferida**: Optimización de memoria mediante lazy loading de recursos y patrón singleton.


## Instalación

Ejecutar en una terminal

```bash
pip install ubigeos_peru
```

Con uv

```bash
uv add ubigeos_peru
```

## Uso Básico

### Inicialización

Se recomienda importar de la siguiente manera:

```python
import ubigeos_peru as ubg
```
La clase siempre tendrá una única instancia para evitar cargar recursos dos veces.
### Consultar información de Ubigeo

```python
departamento = ubg.get_departamento("010101") # "Amazonas"
provincia = ubg.get_provincia("1201")         # "Huancayo"
distrito = ubg.get_distrito("150110")         # "Comas"
```

#### Validación y Normalización

```python
ubg.validate_departamento("HUANUCO")              # "Huánuco"
ubg.validate_ubicacion("Mi peru")                 # "Mi Perú"
```

#### A partir de ubicación

```python
codigo_dept = ubg.get_ubigeo("Madre de dios", "departamentos") # "17"
codigo_dist = ubg.get_ubigeo("Lince", "distritos")              # "150116"
```


#### Metadatos Geográficos

(No preparada para producción)

```python
capital = ubg.get_metadato(
  "La Libertad",
  level="departamentos", 
  key="capital"
)  # -> "Trujillo"

altitud = ubg.get_metadato(
  "Cusco",
  level="departamentos",
  key="altitud"
) # -> "3439"
```
---

## Integración con Pandas

La librería está optimizada para trabajar con DataFrames de pandas, como por ejemplo encuestas de la Enaho:

```python
import pandas as pd

# Crear DataFrame de ejemplo (datos no oficiales)
df = pd.DataFrame({
    "UBIGEO": [10101, 50101, 110101, 150101, 210101, 220101],
    "POBLACION": [45694, 67823, 34576, 857497, 45983, 87564]
})

# Agregar información geográfica
df["DEPARTAMENTO"] = ubg.get_departamento(df["UBIGEO"])
```
Esto generará el siguiente DataFrame:

```
    UBIGEO  POBLACION DEPARTAMENTO
0    10101      45694    Amazonas
1    50101      67823    Ayacucho
2   110101      34576    Ica
3   150101     857497    Lima
4   210101      45983    Puno
5   220101      87564    San Martín
```
También se pueden pasar argumentos

```python
# Agregar información geográfica
df["PROVINCIA"] = ubg.get_provincia(df["UBIGEO"], normalize=True)
```

```
    UBIGEO  POBLACION DEPARTAMENTO  PROVINCIA
0    10101      45694    Amazonas    CHACHAPOYAS
1    50101      67823    Ayacucho    HUAMANGA
2   110101      34576    Ica         ICA
3   150101     857497    Lima        LIMA
4   210101      45983    Puno        PUNO
5   220101      87564    San Martín  MOYOBAMBA
```
---

## Contribución

Por favor, contáctame si encuentras alguno de los siguientes:

- **Base de datos de la SUNAT actualizada**: Es la única que me falta.
- **Errores en el uso de la librería**: Funciones que dan error cuando no deberían.
- **Códigos incorrectos**: Códigos INEI o RENIEC incorrectos.
- **Nombres incorrectos**: Ubicaciones que no siguen el nombre oficial.
- **Ubicaciones faltantes**: Provincias o distritos que no están en la base de datos.

📧 a20180264@pucp.edu.pe
[Mi Linkedin](https://www.linkedin.com/in/michael-su%C3%A1rez-1734a2211/)

## Cómo contribuir

#### 1. Preparar el entorno
Debes clonar o hacer fork del repositorio para tener acceso a las carpetas /construction y /resources_readable

```bash
# Clona o haz fork del repositorio
git clone https://github.com/username/ubigeos_peru.git
cd ubigeos_peru

# Si usas uv
uv sync
```

#### 2. Identificar el recurso a actualizar

Los recursos disponibles son:
- `departamentos`-> ubigeo : departamento
- `provincias`-> ubigeo : provincia
- `distritos`-> ubigeo : distrito
- `equivalencias`-> UBICACION : Ubicación
- `inverted`-> nivel : { Ubicación : ubigeo }
- `macrorregiones`-> departamento : { macrorregion }
- `otros`-> Ubicación : capital, superficie, altitud, etc


## Licencia

Esta librería utiliza datos oficiales de instituciones públicas peruanas y está destinada para uso académico y de investigación.
