from rsa import encriptar, desencriptar
from validaciones import ErrorValidacion

P, Q, E = "367", "373", "17"


def _espera_error(*args):
    try:
        desencriptar(*args)
    except ErrorValidacion:
        return
    raise AssertionError(f"Se esperaba ErrorValidacion con {args!r}")


def _ida_y_vuelta(msg):
    r = encriptar(msg, P, Q, E)
    d = desencriptar(r.C, str(r.L), P, Q, E)
    assert d.mensaje == msg, (msg, d.mensaje)
    return d


def test_desencriptar_rsa():
    d = desencriptar("026054 123875", "3", P, Q, E)
    assert d.d == 8009
    assert d.n == 136891 and d.phi == 136152
    assert d.L == 3 and d.k == 2 and d.hubo_relleno is True
    assert d.bloques_c == [26054, 123875]
    assert d.bloques_m == [82083, 65032]
    assert d.texto_completo == "RSA "
    assert d.mensaje == "RSA"


def test_encriptar_referencia_y_detalle():
    r = encriptar("RSA", P, Q, E)
    assert r.C == "026054 123875"
    assert (r.L, r.k, r.hubo_relleno) == (3, 2, True)
    assert r.llave_publica == (17, 136891)
    assert (r.n, r.phi) == (136891, 136152)
    assert r.mensaje == "RSA" and r.texto_completo == "RSA "
    assert r.codigos == [82, 83, 65, 32]
    assert r.bloques_m == [82083, 65032]
    assert r.bloques_c == [26054, 123875]


def test_encriptar_rechaza_datos_invalidos():
    for mensaje, p, q, e in [
        ("", P, Q, E), ("año", P, Q, E), ("a\nb", P, Q, E),
        ("RSA", "369", Q, E), ("RSA", P, Q, "2"),
    ]:
        try:
            encriptar(mensaje, p, q, e)
        except ErrorValidacion:
            continue
        raise AssertionError("Se esperaba ErrorValidacion")


def test_todos_los_caracteres_y_otros_parametros():
    mensaje = "".join(chr(c) for c in range(32, 127))
    for p, q, e in [(P, Q, E), ("991", "1009", "13"),
                    ("2", "499979", "3"), (P, Q, "136169")]:
        for original in (mensaje, mensaje + " "):
            r = encriptar(original, p, q, e)
            assert desencriptar(r.C, str(r.L), p, q, e).mensaje == original


def test_error_codigos_recuperados_y_relleno():
    _espera_error("000000", "2", P, Q, E)
    r = encriptar("AB", P, Q, E)
    _espera_error(r.C, "1", P, Q, E)


def test_desencriptar_valores_fijos():
    assert desencriptar("109641 028621", "4", P, Q, E).mensaje == "Hola"
    assert desencriptar("021860 013282", "3", P, Q, E).mensaje == "a b"


def test_exponente_mayor_que_phi_y_de_mas_de_100_digitos():
    e = "136152" + "0" * 99 + "17"
    r = encriptar("  RSA  ", P, Q, e)
    assert desencriptar(r.C, str(r.L), P, Q, e).mensaje == "  RSA  "


def test_desencriptar_ceros_iniciales():
    d = desencriptar("000056", "2", P, Q, E)
    assert d.mensaje == "IU" and d.hubo_relleno is False and d.k == 1


def test_ida_y_vuelta_par_e_impar():
    assert _ida_y_vuelta("Hola").hubo_relleno is False
    assert _ida_y_vuelta("RSA").hubo_relleno is True
    _ida_y_vuelta("A")
    _ida_y_vuelta("Hello, World! 123 ~")


def test_ida_y_vuelta_espacios():
    _ida_y_vuelta(" hola")       # inicio, impar
    _ida_y_vuelta("hola ")       # final, impar
    _ida_y_vuelta("  hola  ")    # inicio y final, par
    _ida_y_vuelta("a  b")        # consecutivos, par
    _ida_y_vuelta("a   b")       # consecutivos, impar
    _ida_y_vuelta(" ")           # solo un espacio (relleno + original)
    _ida_y_vuelta("   ")         # solo espacios, impar


def test_error_bloque_longitud():
    _espera_error("02605 123875", "3", P, Q, E)      # 5 dígitos
    _espera_error("0260540 123875", "3", P, Q, E)    # 7 dígitos


def test_error_caracteres_en_c():
    _espera_error("02605a 123875", "3", P, Q, E)
    _espera_error("026054\t123875", "3", P, Q, E)
    _espera_error("026054\n123875", "3", P, Q, E)
    _espera_error("０26054 123875", "3", P, Q, E)    # dígito no ASCII


def test_error_espacios_en_c():
    _espera_error("026054  123875", "3", P, Q, E)    # doble
    _espera_error(" 026054 123875", "3", P, Q, E)    # inicio
    _espera_error("026054 123875 ", "3", P, Q, E)    # final
    _espera_error(" ", "3", P, Q, E)


def test_error_c_vacio():
    _espera_error("", "1", P, Q, E)


def test_error_c_fuera_de_rango():
    _espera_error("136891 123875", "3", P, Q, E)     # c == n
    _espera_error("026054 999999", "3", P, Q, E)


def test_error_l():
    _espera_error("026054 123875", "2", P, Q, E)     # ni 4 ni 3
    _espera_error("026054 123875", "5", P, Q, E)
    _espera_error("026054 123875", "0", P, Q, E)
    _espera_error("026054 123875", "abc", P, Q, E)
    _espera_error("026054 123875", "3.5", P, Q, E)
    _espera_error("026054 123875", "", P, Q, E)


def test_error_parametros_en_desencriptar():
    _espera_error("026054 123875", "3", "368", Q, E)   # p no primo
    _espera_error("026054 123875", "3", P, P, E)       # p == q
    _espera_error("026054 123875", "3", P, Q, "2")     # mcd(e, phi) != 1
    _espera_error("026054 123875", "3", P, Q, "abc")


def test_e_distinto_nunca_da_el_original():
    try:
        d = desencriptar("026054 123875", "3", P, Q, "5")
    except ErrorValidacion:
        return
    assert d.mensaje != "RSA"


def test_c_no_texto_es_typeerror():
    try:
        desencriptar(123, "1", P, Q, E)
    except TypeError:
        return
    raise AssertionError("Se esperaba TypeError")
