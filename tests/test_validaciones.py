"""Pruebas de validacion.py.

Ejecutar desde la raiz del proyecto:
    python -m tests.test_validacion
"""

from validaciones import ErrorValidacion, ParametrosRSA, validar_parametros


def debe_fallar(p, q, e, fragmento):
    """Comprueba que lanza ErrorValidacion y que el mensaje contiene `fragmento`."""
    try:
        validar_parametros(p, q, e)
    except ErrorValidacion as error:
        assert fragmento in str(error), (
            f"({p!r}, {q!r}, {e!r}): se esperaba {fragmento!r} en {str(error)!r}"
        )
        return
    raise AssertionError(f"({p!r}, {q!r}, {e!r}) debio fallar con {fragmento!r}")


def test_valido_ejemplo_referencia():
    r = validar_parametros("367", "373", "17")
    assert isinstance(r, ParametrosRSA)
    assert (r.p, r.q, r.e, r.n, r.phi) == (367, 373, 17, 136891, 136152)
    # los tipos devueltos son enteros, no texto
    assert all(type(x) is int for x in r)


def test_validos_extremos():
    # p y q intercambiados dan el mismo n y phi
    a = validar_parametros("373", "367", "17")
    assert (a.n, a.phi) == (136891, 136152)
    # n cerca del limite superior: 991 * 1009
    r = validar_parametros("991", "1009", "13")
    assert (r.n, r.phi) == (999919, 997920)
    # p = 2 con el mayor primo menor que 500000
    r = validar_parametros("2", "499979", "3")
    assert (r.n, r.phi) == (999958, 499978)
    # ceros a la izquierda se aceptan como el mismo numero
    assert validar_parametros("0367", "373", "017").e == 17


def test_texto_vacio():
    for malo in ["", "   ", "\t", "\n"]:
        debe_fallar(malo, "373", "17", "p está vacío")
        debe_fallar("367", malo, "17", "q está vacío")
        debe_fallar("367", "373", malo, "e está vacío")


def test_texto_con_signo():
    debe_fallar("-7", "373", "17", "sin signo")
    debe_fallar("367", "+373", "17", "sin signo")
    debe_fallar("367", "373", "-17", "sin signo")


def test_texto_con_decimales():
    debe_fallar("3.5", "373", "17", "decimales")
    debe_fallar("367", "37,3", "17", "decimales")
    debe_fallar("367", "373", "17.0", "decimales")


def test_texto_con_espacios():
    debe_fallar(" 367", "373", "17", "espacios")
    debe_fallar("367", "373 ", "17", "espacios")
    debe_fallar("367", "373", "1 7", "espacios")


def test_texto_con_caracteres_invalidos():
    for malo in ["abc", "1_000", "12a", "0x11", "1e3",
                 "٣٦٧",      # digitos arabigo-indicos
                 "１７",      # digitos de ancho completo
                 "²"]:       # superindice
        debe_fallar(malo, "373", "17", "carácter no válido")
        debe_fallar("367", "373", malo, "carácter no válido")


def test_texto_demasiado_grande_o_largo():
    debe_fallar("1000003", "373", "17", "p = 1000003 es demasiado grande")
    debe_fallar("367", "500000", "17", "q = 500000 es demasiado grande")
    # un numero gigante no debe colgar el programa
    debe_fallar("9" * 50, "373", "17", "demasiado grande")
    debe_fallar("367", "9" * 101, "17", "demasiado largo")
    debe_fallar("367", "373", "9" * 101, "demasiado largo")


def test_no_primos():
    debe_fallar("369", "373", "17", "p = 369 no es primo.")
    debe_fallar("367", "371", "17", "q = 371 no es primo.")
    debe_fallar("0", "373", "17", "p = 0 no es primo.")
    debe_fallar("1", "373", "17", "p = 1 no es primo.")
    debe_fallar("367", "1", "17", "q = 1 no es primo.")


def test_primos_iguales():
    debe_fallar("367", "367", "17", "distintos")
    debe_fallar("2", "2", "3", "distintos")


def test_n_fuera_de_rango():
    # 331 * 379 = 125449 <= 126126
    debe_fallar("331", "379", "17", "n = p·q = 125449 es demasiado pequeño")
    debe_fallar("2", "3", "5", "demasiado pequeño")
    # 1009 * 1013 = 1022117 >= 1000000
    debe_fallar("1009", "1013", "17", "n = p·q = 1022117 es demasiado grande")


def test_e_invalido():
    debe_fallar("367", "373", "0", "mayor que 1")
    debe_fallar("367", "373", "1", "mayor que 1")
    # phi es par, asi que e = 2 nunca es coprimo
    debe_fallar("367", "373", "2", "primo relativo")
    # 136152 = 366 * 372 = 2^3 * 3^2 * 31 * 61
    debe_fallar("367", "373", "61", "primo relativo")
    debe_fallar("367", "373", "93", "primo relativo")   # 3 * 31
    debe_fallar("367", "373", "136152", "primo relativo")
    debe_fallar("367", "373", "272304", "primo relativo")


def test_orden_de_comprobaciones():
    # el formato se revisa antes que las condiciones matematicas
    debe_fallar("369", "373", "abc", "e contiene un carácter no válido")
    # la cota y la primalidad van antes que e
    debe_fallar("369", "373", "1", "p = 369 no es primo.")
    # p y q no primos antes que n fuera de rango
    debe_fallar("4", "6", "5", "p = 4 no es primo.")
    # n fuera de rango antes que e
    debe_fallar("331", "379", "1", "demasiado pequeño")


def test_tipo_no_texto():
    for malo in [(367, "373", "17"), ("367", 373.0, "17"), ("367", "373", None)]:
        try:
            validar_parametros(*malo)
        except TypeError:
            continue
        raise AssertionError(f"{malo} debio lanzar TypeError")


if __name__ == "__main__":
    pruebas = [f for nombre, f in sorted(globals().items())
               if nombre.startswith("test_")]
    for prueba in pruebas:
        prueba()
        print(f"OK  {prueba.__name__}")
    print("Todas las pruebas pasaron.")