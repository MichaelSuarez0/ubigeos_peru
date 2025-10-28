library(readxl)
library(dplyr)
library(readr)

df <- read_excel(r"(C:\Users\micha\OneDrive\Python\ubigeos_peru\databases\geodir-ubigeo-reniec.xlsx)")
df2 <- read_csv(r"(C:\Users\micha\OneDrive\Python\ubigeos_peru\databases\ubigeo_reniec_2025.csv)")

df_geodir <- df |>
  group_by(Departamento) |> 
  count()

df_reniec <- df2 |>
  group_by(Departamento) |> 
  count()

df_diff <- df_geodir %>%
  full_join(df_reniec, by = "Departamento", suffix = c("_geodir", "_reniec")) %>%
  mutate(
    n_geodir = coalesce(n_geodir, 0),   # reemplaza NA por 0
    n_reniec = coalesce(n_reniec, 0),
    diferencia = n_geodir - n_reniec
  )