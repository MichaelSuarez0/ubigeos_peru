import statistics
import random
import time
import ubigeos_peru as ubg
import ubigeos_rust as ur
from functools import wraps
import pandas as pd

def medir_tiempo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()  # mide con precisión alta para benchmarks
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
    data["ubigeo"] = data["ubigeo"].apply(ubg.Ubigeo._validate_codigo)
    return data

# def construct_random_data(size: int = 500_000):
#     random.seed(10)
#     random_numbers_list = [str(random.randint(1,25)) + "01" for _ in range(size)]
#     id = [1] * size
#     data = pd.DataFrame({
#         "id": id,
#         "ubigeo": random_numbers_list
#     })
#     return data

@medir_tiempo_repetido
def with_apply(data: pd.DataFrame):
    data["departamento"] = data["ubigeo"].apply(ubg.get_departamento)

@medir_tiempo_repetido
def with_map(data: pd.DataFrame):
    dptos = ubg.ResourceManager.cargar_diccionario("provincias")
    data["provincia"] = data["ubigeo"].map(dptos)
    return data

@medir_tiempo_repetido
def with_series(data: pd.DataFrame):
    data["departamento"] = ubg.get_departamento(data["ubigeo"])
    return data

DEPARTAMENTOS = {
        1: "Amazonas",
        2: "Áncash",
        3: "Apurímac",
        4: "Arequipa",
        5: "Ayacucho",
        6: "Cajamarca",
        7: "Callao",
        8: "Cusco",
        9: "Huancavelica",
        10: "Huánuco",
        11: "Ica",
        12: "Junín",
        13: "La Libertad",
        14: "Lambayeque",
        15: "Lima",
        16: "Loreto",
        17: "Madre de Dios",
        18: "Moquegua",
        19: "Pasco",
        20: "Piura",
        21: "Puno",
        22: "San Martín",
        23: "Tacna",
        24: "Tumbes",
        25: "Ucayali",
        -1: "Desconocido"
    }

@medir_tiempo_repetido
def with_rust(data: pd.DataFrame):
    # Obtenemos los códigos desde Rust
    data["ubigeo"] = ur.get_departamento_codes(data["ubigeo"].tolist())
    data["departamento"] = data["ubigeo"].map(DEPARTAMENTOS)

if __name__ == "__main__":  
    data = construct_random_data(size=1_000_000)
    #with_apply(data)
    #with_series(data)
    with_rust(data)
    with_map(data)


# timeit.timeit("Ubigeo._validate_codigo('150101')", globals=globals(), number=100000)
# timeit.timeit("mapping['15']", globals=globals(), number=100000)
# timeit.timeit("mapping['1501']", globals=globals(), number=100000)

# import timeit

# print("departamento:",
#     timeit.timeit("Ubigeo.get_departamento('150101')",
#                   globals=globals(), number=100000)
# )

# print("provincia:",
#     timeit.timeit("Ubigeo.get_provincia('150101')",
#                   globals=globals(), number=100000)
# )
