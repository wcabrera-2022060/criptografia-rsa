"""Ejecuta las pruebas existentes con la biblioteca estándar: python run_tests.py."""

import runpy
import unittest
from pathlib import Path


def main():
    suite = unittest.TestSuite()
    for archivo in sorted((Path(__file__).parent / "tests").glob("test_*.py")):
        # test_texto_bloques ejecuta sus comprobaciones al cargar el archivo.
        contenido = runpy.run_path(str(archivo))
        for nombre, funcion in sorted(contenido.items()):
            if nombre.startswith("test_") and callable(funcion):
                suite.addTest(unittest.FunctionTestCase(
                    funcion, description=f"{archivo.stem}.{nombre}"
                ))
    resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if resultado.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
