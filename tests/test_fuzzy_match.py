import ubigeos_peru as ubg
from rapidfuzz import fuzz, process, utils

def test_fuzzy_match():
    distritos = ubg.cargar_diccionario("equivalencias")["distritos"]
    options = list(distritos.keys())
    print(process.extract("CUSCO", options, scorer=fuzz.WRatio, limit=1)[0])
    
test_fuzzy_match()