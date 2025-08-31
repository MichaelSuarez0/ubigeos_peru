import pandas as pd
import random
import time
import ubigeos_peru as ubg
from functools import wraps

def medir_tiempo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()  # mide con precisión alta
        resultado = func(*args, **kwargs)
        fin = time.perf_counter()
        print(f"La función '{func.__name__}' tardó {fin - inicio:.6f} segundos")
        return resultado
    return wrapper

def construct_random_data(size: int = 500_000):
    random_numbers_list = [random.randint(1,25) for _ in range(size)]
    id = [1] * size
    data = pd.DataFrame({
        "id": id,
        "ubigeo": random_numbers_list
    })
    return data

@medir_tiempo
def with_apply(data: pd.DataFrame):
    data["departamento"] = data["ubigeo"].apply(ubg.get_departamento)

@medir_tiempo
def with_map(data: pd.DataFrame):
    dptos = ubg.ResourceManager.cargar_diccionario("departamentos")
    data["departamento"] = data["ubigeo"].map(dptos)



if __name__ == "__main__":  
    data = construct_random_data(size=1_000_000)
    with_apply(data)
    with_map(data)