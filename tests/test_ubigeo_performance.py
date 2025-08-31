import statistics
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

def medir_tiempo_repetido(_func=None, *, n_iter=10, warmup=1, copiar_df=True):
    def _decorator(func):
        def _wrapper(*args, **kwargs):
            # Warmup (no medido)
            for _ in range(warmup):
                if copiar_df and args and isinstance(args[0], pd.DataFrame):
                    tmp_args = (args[0].copy(),) + args[1:]
                    func(*tmp_args, **kwargs)
                else:
                    func(*args, **kwargs)

            tiempos = []
            result = None
            for _ in range(n_iter):
                if copiar_df and args and isinstance(args[0], pd.DataFrame):
                    tmp_args = (args[0].copy(),) + args[1:]
                else:
                    tmp_args = args
                start = time.perf_counter()
                result = func(*tmp_args, **kwargs)
                tiempos.append(time.perf_counter() - start)

            promedio = statistics.mean(tiempos)
            desv = statistics.pstdev(tiempos) if len(tiempos) > 1 else 0.0
            print(f"{func.__name__}: {promedio:.6f} s ± {desv:.6f} s "
                  f"(promedio de {n_iter} corridas, warmup={warmup})")
            return result
        return _wrapper

    # Permite @medir_tiempo_repetido y @medir_tiempo_repetido(...)
    return _decorator if _func is None else _decorator(_func)

def construct_random_data(size: int = 500_000):
    random_numbers_list = [random.randint(1,25) for _ in range(size)]
    id = [1] * size
    data = pd.DataFrame({
        "id": id,
        "ubigeo": random_numbers_list
    })
    return data

@medir_tiempo_repetido
def with_apply(data: pd.DataFrame):
    data["departamento"] = data["ubigeo"].apply(ubg.get_departamento)

@medir_tiempo_repetido
def with_map(data: pd.DataFrame):
    dptos = ubg.ResourceManager.cargar_diccionario("departamentos")
    data["departamento"] = data["ubigeo"].map(dptos)
    return data

@medir_tiempo_repetido
def with_series(data: pd.DataFrame):
    data["departamento"] = ubg.get_departamento(data["ubigeo"], normalize=True)
    return data

if __name__ == "__main__":  
    data = construct_random_data(size=1_000_000)
    with_apply(data)
    #df = with_map(data)
    with_series(data)