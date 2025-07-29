import unicodedata


def eliminar_acentos(texto: str) -> str:
    texto_normalizado = unicodedata.normalize("NFKD", texto)
    texto_sin_acentos = "".join(
        c for c in texto_normalizado if not unicodedata.combining(c)
    )
    return texto_sin_acentos
