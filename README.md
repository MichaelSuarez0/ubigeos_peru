# Ubigeos Perú

Librería de Python que convierte códigos de ubigeo en su correspondiente departamento, provincia o distrito, y viceversa. Incluye métodos clave para limpiar y validar nombres oficiales, consultar macrorregiones, coordenadas geográficas, etc. Se integra fácilmente con pandas y polars para procesar bases de datos peruanas como la ENAHO.

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
- **Optimizado para Big Data**: 1 000 000 consultas en 0.25-0.65 segundos
- **Carga Diferida**: Optimización de memoria mediante lazy loading de recursos y patrón singleton.
- **Metadatos Geográficos**: Acceso a información adicional como capital, altitud, superficie y coordenadas

## Instalación

Ejecutar en una terminal

```bash
pip install ubigeos-peru
```

Con uv

```bash
uv add ubigeos-peru
```

## Uso Básico

### Inicialización

Se recomienda importar de la siguiente manera:

```python
import ubigeos_peru as ubg
```
La clase siempre tendrá una única instancia para evitar cargar recursos dos veces.

## Consultar información de Ubigeo
```python
# Departamento
departamento = ubg.get_departamento("1")                 # "Amazonas" (código corto)
departamento = ubg.get_departamento("010101")            # "Amazonas" (código completo)
departamento = ubg.get_departamento(10101)               # "Amazonas" (integer)
departamento = ubg.get_departamento(10101, normalize=True) # "AMAZONAS"

# Provincia
provincia = ubg.get_provincia("1201")                    # "Huancayo"
provincia = ubg.get_provincia(10101, normalize = True)   # "CHACHAPOYAS"

# Distrito
distrito = ubg.get_distrito("50110")                     # "San Juan Bautista"
distrito = ubg.get_distrito(150110)                      # "Comas"
```
## Obtener Ubigeo a partir de ubicación
```python
codigo_dept = ubg.get_ubigeo("Madre de dios", "departamentos") # "17"
codigo_prov = ubg.get_ubigeo("Huaral", "provincia")            # "1506"
codigo_dist = ubg.get_ubigeo("Lince", "distritos")             # "150116"
codigo_dist = ubg.get_ubigeo("Mi peru", "distritos", "reniec") # "240107"
```

## Validación y Normalización ("agregar" o quitar tildes)
```python
ubg.validate_departamento("HUANUCO")                     # "Huánuco"
ubg.validate_departamento("HUÁNUCO", normalize=True)     # "HUANUCO"
ubicacion = ubg.validate_ubicacion("SAN MARTIN")         # "San Martín"

# Validar y agregar tildes o mayúsculas a cualquier ubicación geográfica
ubicacion = ubg.validate_ubicacion("Mi peru")            # "Mi Perú"
ubicacion = ubg.validate_ubicacion("Madre de dios")      # "Madre de Dios"
```

## Macrorregiones

```python
# Obtener macrorregión - múltiples formatos
macro = ubg.get_macrorregion("Amazonas")                 # "Oriente"
macro = ubg.get_macrorregion("AMAZONAS")                 # "Oriente" (mayúsculas)
macro = ubg.get_macrorregion("01")                       # "Oriente" (código string)
macro = ubg.get_macrorregion(1)                          # "Oriente" (entero)

# Con institución específica
macro_ceplan = ubg.get_macrorregion(25, institucion="ceplan")          # "Nororiente"
macro_ceplan = ubg.get_macrorregion("Ucayali", institucion="ceplan")   # "Nororiente"

# Mapeo completo de macrorregiones
mapa_macro = ubg.get_macrorregion_map()
```

## Metadatos Geográficos

```python
# Capitales
capital_dept = ubg.get_metadato("La libertad", level="departamentos", key="capital") # "Trujillo"
capital_prov = ubg.get_metadato("Huarochiri", level="provincias", key="capital")     # "Matucana"

# Altitudes
altitud_dept = ubg.get_metadato("Cusco", level="departamento", key="altitud")       # "3439"
altitud_prov = ubg.get_metadato("Huarochiri", level="provincia", key="altitud")     # "2395"

# Superficies
sup1 = ubg.get_metadato("Lince", level="distritos", key="superficie")               # "3.03"
sup2 = ubg.get_metadato("San Isidro", level="distritos", key="superficie")          # "11.1"

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
También se pueden pasar argumentos con una función lambda
```python
# Agregar información geográfica
df["PROVINCIA"] = ubg.get_provincia(df["UBIGEO"], normalize=True)
```
Esto generará el siguiente DataFrame:

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

📧 a20180264@pucp.edu.com  
[Mi Linkedin](https://www.linkedin.com/in/michael-su%C3%A1rez-1734a2211/)

## Cómo contribuir

#### 1. Preparar el entorno
Debes clonar o hacer fork del repositorio para tener acceso a las carpetas /construction y /resources_readable

```bash
# Clona o haz fork del repositorio
git clone https://github.com/username/repo-name.git
cd repo-name

# Si usas uv
uv sync
uv pip install -e .

# Si usas pip
pip install -e .
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
