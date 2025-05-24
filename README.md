# Ubigeos Perú

Librería de Python ligera especializada para consultas a partir del código de ubigeo para obtener el nombre del departamento, provincia o distrito, y viceversa, además de información suplementaria.

## Características Principales

- **Soporte Multi-institucional**: Soporte para consultar códigos de ubigeo de INEI, RENIEC y SUNAT.
- **Normalización Inteligente**: Manejo automático de acentos, mayúsculas y formatos variables
- **Optimizado para Big Data**: 500 000 consultas en 0.62 segundos aprox.
- **Carga Diferida**: Optimización de memoria mediante lazy loading de recursos y patrón singleton
- **Metadatos Geográficos**: Acceso a información adicional como capital, altitud, superficie y coordenadas

## Instalación

Ejecutar en una terminal

```bash
pip install ubigeos_peru
```

## Uso Básico

### Inicialización

Se recomienda importar de la siguiente manera:

```python
from ubigeos_peru import Ubigeo as ubg
```
Cabe mencionar que la clase siempre tendrá una única instancia para evitar cargar recursos dos veces,
por lo que también se puede utilizar de la siguiente manera.

```python
from ubigeos_peru import Ubigeo
ubg = Ubigeo()
```

## Obtener Información de Ubigeo
```python
# Departamento
departamento = ubg.get_departamento("1")                 # "Amazonas" (código corto)
departamento = ubg.get_departamento("010101")            # "Amazonas" (código completo)
departamento = ubg.get_departamento(10101)               # "Amazonas" (integer)
departamento = ubg.get_departamento(10101, normalize=True) # "AMAZONAS"

# Provincia
provincia = ubg.get_provincia("010101")                  # "Chachapoyas"
provincia = ubg.get_provincia("101", normalize=True)     # "CHACHAPOYAS"

# Distrito
distrito = ubg.get_distrito("50110")                     # "San Juan Bautista"
distrito = ubg.get_distrito(150110)                      # "Comas"
```
## Obtener Ubigeo a partir de ubicación
```python
codigo_dept = ubg.get_ubigeo("Madre de dios", "departamentos") # "17"
codigo_prov = ubg.get_ubigeo("Huaral", "provincia")            # "1506"
codigo_dist = ubg.get_ubigeo("Lince", "distritos")             # "150116"
codigo_dist = ubg.get_ubigeo("Miraflores", "distritos")        # "151021"
```

## Validación y Normalización
```python
ubg.validate_departamento("HUANUCO")                    # "Huánuco"
ubg.validate_departamento("HUÁNUCO", normalize=True)    # "HUANUCO"
ubg.validate_departamento("HUÁNUCO", normalize=True).lower()  # "huanuco"

# Validar cualquier ubicación geográfica
ubicacion = ubg.validate_ubicacion("SAN MARTIN")        # "San Martín"
ubicacion = ubg.validate_ubicacion("Madre de dios")     # "Madre de Dios"
```

## Macrorregiones

```python
# Obtener macrorregión - múltiples formatos
macro = ubg.get_macrorregion("Amazonas")                # "Oriente"
macro = ubg.get_macrorregion("AMAZONAS")                # "Oriente" (mayúsculas)
macro = ubg.get_macrorregion("01")                      # "Oriente" (código string)
macro = ubg.get_macrorregion(1)                         # "Oriente" (entero)

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

# Superficies de lugares
sup1 = ubg.get_metadato("Lince", level="distritos", key="superficie")               # "3.03"
sup2 = ubg.get_metadato("San Isidro", level="distritos", key="superficie")          # "11.1"

```

---

## Integración con Pandas

La librería está optimizada para trabajar con DataFrames de pandas:

```python
import pandas as pd

# Crear DataFrame de ejemplo
df = pd.DataFrame({
    "UBIGEO": [10101, 50101, 110101, 150101, 210101],
    "POBLACION": [45694, 67823, 34576, 8574974, 45983]
})

# Agregar información geográfica
df["DEPARTAMENTO"] = df["UBIGEO"].apply(ubg.get_departamento)
```
Esto generará el siguiente DataFrame:

```
    UBIGEO  POBLACION DEPARTAMENTO
0    10101      45694    Amazonas
1    50101      67823    Ayacucho
2   110101      34576    Ica     
3   150101    8574974    Lima    
4   210101      45983    Puno    
```
También se pueden pasar argumentos con una función lambda
```python
# Agregar información geográfica
df["PROVINCIA"] = df["UBIGEO"].apply(lambda x: ubg.get_distrito(x, normalize= True))
```
Esto generará el siguiente DataFrame:

```
    UBIGEO  POBLACION DEPARTAMENTO  PROVINCIA   
0    10101      45694    Amazonas    CHACHAPOYAS
1    50101      67823    Ayacucho    HUAMANGA
2   110101      34576    Ica         ICA   
3   150101    8574974    Lima        LIMA
4   210101      45983    Puno        PUNO
```
---

## Contribución

Para contribuir al desarrollo de esta librería, por favor contáctame: michael-salvador@hotmail.com

## Licencia

Esta librería utiliza datos oficiales de instituciones públicas peruanas y está destinada para uso académico y de investigación.


## Fuentes
 - Nombres oficiales: https://github.com/ernestorivero/Ubigeo-Peru
 - Códigos de ubigeo por instituciones: https://github.com/CONCYTEC/ubigeo-peru/blob/master/equivalencia-ubigeos-oti-concytec.csv
 - Otros datos (capital, altitud, latitud, longitud): https://github.com/jmcastagnetto/ubigeo-peru-aumentado/blob/main/ubigeo_departamento.csv