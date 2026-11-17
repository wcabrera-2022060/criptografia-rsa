from rsa import encriptar
from validaciones import ErrorValidacion

P, Q, E = "367", "373", "17"


def cifrar(m):
    return encriptar(m, P, Q, E)


def debe_fallar(*args):
    try:
        encriptar(*args)
    except ErrorValidacion:
        return
    raise AssertionError(f"No lanzó ErrorValidacion con {args!r}")


def test_ejemplo_referencia():
    r = cifrar("RSA")
    assert r.n == 136891
    assert r.phi == 136152
    assert r.llave_publica == (17, 136891)
    assert r.L == 3
    assert r.hubo_relleno is True
    assert r.texto_relleno == "RSA "
    assert r.codigos == [82, 83, 65, 32]
    assert r.bloques_m == [82083, 65032]
    assert r.bloques_c == [26054, 123875]
    assert r.C == "026054 123875"


def test_longitud_par():
    r = cifrar("Hola")
    assert r.L == 4
    assert r.hubo_relleno is False
    assert r.texto_relleno == "Hola"
    assert r.bloques_m == [72111, 108097]
    assert r.C == "109641 028621"


def test_longitud_impar():
    r = cifrar("Hola!")
    assert r.L == 5
    assert r.hubo_relleno is True
    assert r.texto_relleno == "Hola! "
    assert r.C == "109641 028621 127769"


def test_espacio_al_inicio():
    r = cifrar("  A")
    assert r.L == 3
    assert r.texto_relleno == "  A "
    assert r.bloques_m == [32032, 65032]
    assert r.C == "038557 123875"


def test_espacio_al_final():
    r = cifrar("Hi  ")
    assert r.L == 4
    assert r.hubo_relleno is False
    assert r.C == "051670 038557"


def test_espacios_consecutivos():
    r = cifrar("a  b")
    assert r.L == 4
    assert r.bloques_m == [97032, 32098]
    assert r.C == "021860 001245"


def test_solo_espacios():
    r = cifrar("  ")
    assert r.L == 2
    assert r.C == "038557"


def test_ceros_iniciales():
    r = cifrar("IU")
    assert r.bloques_c == [56]
    assert r.C == "000056"
    r = cifrar("a  b")
    assert r.C.split()[1] == "001245"
    assert all(len(b) == 6 for b in r.C.split())


def test_otros_caracteres():
    assert cifrar("AB").C == "117927"
    assert cifrar("ab").C == "044076"
    assert cifrar("12").C == "126442"
    assert cifrar("~~").C == "051700"
    assert cifrar("Hola mundo").C == "109641 028621 087662 063943 072468"


def test_parametros_invalidos():
    debe_fallar("RSA", "4", "373", "17")        # p no primo
    debe_fallar("RSA", "367", "367", "17")      # p = q
    debe_fallar("RSA", "3", "5", "7")           # n demasiado pequeño
    debe_fallar("RSA", "1009", "1013", "17")    # n demasiado grande
    debe_fallar("RSA", "367", "373", "1")       # e <= 1
    debe_fallar("RSA", "367", "373", "2")       # MCD(e, phi) != 1
    debe_fallar("RSA", "abc", "373", "17")      # no es entero
    debe_fallar("RSA", "367", "", "17")         # vacío


def test_parametros_se_validan_antes_que_mensaje():
    debe_fallar("ñ", "4", "373", "17")


def test_caracteres_no_admitidos():
    debe_fallar("camión", P, Q, E)
    debe_fallar("hola\n", P, Q, E)
    debe_fallar("a\tb", P, Q, E)
    debe_fallar("\u00e1", P, Q, E)
    debe_fallar("emoji \U0001F600", P, Q, E)


def test_mensaje_vacio():
    debe_fallar("", P, Q, E)


if __name__ == "__main__":
    pruebas = [f for nombre, f in sorted(globals().items()) if nombre.startswith("test_")]
    for f in pruebas:
        f()
        print(f"OK  {f.__name__}")
    print(f"\n{len(pruebas)} pruebas pasaron.")