import pandas as pd
import random
from ubigeos_peru import Ubigeo as ubg
import time

def medir_tiempo(func):
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
def main(data: pd.DataFrame):
    data["departamento"] = data["ubigeo"].apply(ubg.get_departamento)


if __name__ == "__main__":  
    data = construct_random_data(size=1_000_000)
    main(data)