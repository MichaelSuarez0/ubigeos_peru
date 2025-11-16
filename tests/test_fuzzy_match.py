import ubigeos_peru as ubg


class TestFuzzyMatch:
    def test_fuzzy_match_departamento(self, fuzzy_match_test_cases):
        # Diccionarios de equivalencias esperadas
        test_cases = fuzzy_match_test_cases["departamentos"]
        for original, expected in test_cases.items():
            result = ubg.validate_departamento(original, fuzzy_match=True, on_error="ignore")

            assert result == expected, f"Fallo en departamento: '{original}' → '{result}', esperado: '{expected}'"
            
    def test_fuzzy_match_provincia(self, fuzzy_match_test_cases):
        # Diccionarios de equivalencias esperadas
        test_cases = fuzzy_match_test_cases["provincias"]
        for original, expected in test_cases.items():
            result = ubg.validate_provincia(original, fuzzy_match=True, on_error="ignore")

            assert result == expected, f"Fallo en provincia: '{original}' → '{result}', esperado: '{expected}'"
            
    def test_fuzzy_match_distrito(self, fuzzy_match_test_cases):
        # Diccionarios de equivalencias esperadas
        test_cases = fuzzy_match_test_cases["distritos"]
        for original, expected in test_cases.items():
            result = ubg.validate_distrito(original, fuzzy_match=True, on_error="ignore")

            assert result == expected, f"Fallo en distrito: '{original}' → '{result}', esperado: '{expected}'"

# if __name__ == "__main__":
#     test_scorers()
#     # test_fuzzy_match_batch()
