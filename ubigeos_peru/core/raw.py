import os
import json
import pandas as pd
from icecream import ic

script_dir = os.path.dirname(__file__)
databases = os.path.join(script_dir, "..", "databases")

all_path = os.path.join(databases, "equivalencia-ubigeos-oti-concytec.csv")
# departamentos_path = os.path.join(databases, "ubigeo_peru_2016_departamentos.csv")
# provincias_path = os.path.join(databases, "ubigeo_peru_2016_provincias.csv")
# distritos_path = os.path.join(databases, "ubigeo_peru_2016_distritos.csv")

salud_dep = os.path.join(databases, "salud_departamento.json")
salud_prov = os.path.join(databases, "salud_provincia.json")

with open(salud_prov, "r", encoding="utf-8") as file:
    salud_provincia = json.load(file)

provincias = pd.read_csv(provincias_path, converters={'id': lambda x: str(x)})
departamentos = pd.read_csv(departamentos_path, converters={'id': lambda x: str(x)})

#ic(provincias)
ic(departamentos)
#ic(salud_departamento)

db = []
for list_of_dicts in salud_provincia.values():
    for details in list_of_dicts:
        id_dep = details["IdDepartamento"]
        id_prov = details["IdDepartamento"] + details["IdProvincia"]
        total = details["Total"]
        for row in list(departamentos.itertuples(index=False, name=None)):
            if str(row[0]) == str(id_dep):
                temp_dict ={
                    "Departamento": row[1]
                    }
                break
        for row in list(provincias.itertuples(index=False, name=None)):
            if str(row[0]) == str(id_prov):
                temp_dict.update({
                    "id_prov": id_prov,
                    "Provincia": row[1],
                    "Centros de salud con telemedicina": total
                    })
                break
        db.append(temp_dict)

data = pd.DataFrame(db)
data = data.sort_values(by="Centros de salud con telemedicina", ascending=True)
data.to_excel(os.path.join(script_dir, "..", "products", "otros", "centros_telemedicina_provincia.xlsx"), index=False)



