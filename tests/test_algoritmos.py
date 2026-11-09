"""Pruebas de algoritmos.py.

Ejecutar desde la raiz del proyecto:
    python -m tests.test_algoritmos
"""

from algoritmos import (
    es_primo,
    mcd,
    bezout_matricial,
    inverso_modular,
    exponenciacion_modular,
)


def debe_fallar(funcion, *args):
    """Comprueba que la funcion lanza TypeError o ValueError."""
    try:
        funcion(*args)
    except (TypeError, ValueError):
        return
    raise AssertionError(f"{funcion.__name__}{args} debio fallar")


def test_es_primo():
    assert es_primo(2) and es_primo(3) and es_primo(97)
    assert es_primo(367) and es_primo(373)
    assert not es_primo(-5) and not es_primo(0) and not es_primo(1)
    assert not es_primo(4) and not es_primo(9) and not es_primo(25)
    assert not es_primo(136891)      # 367 * 373
    assert es_primo(999983)          # mayor primo menor que 10^6


def test_mcd():
    assert mcd(12, 18) == 6
    assert mcd(18, 12) == 6
    assert mcd(17, 136152) == 1
    assert mcd(7, 7) == 7
    assert mcd(1, 99) == 1
    assert mcd(100, 25) == 25
    for malo in [(0, 5), (-3, 6), (2.0, 4), (True, 4), ("3", 4)]:
        debe_fallar(mcd, *malo)


def test_bezout_matricial():
    for a, b in [(3, 7), (7, 3), (12, 18), (17, 136152), (1, 1), (100, 25)]:
        x, y = bezout_matricial(a, b)
        assert a * x + b * y == mcd(a, b)
    for malo in [(0, 5), (-3, 6), (2.0, 4), (True, 4)]:
        debe_fallar(bezout_matricial, *malo)


def test_inverso_modular():
    assert inverso_modular(3, 7) == 5
    assert inverso_modular(17, 136152) == 8009
    for e, phi in [(5, 12), (7, 40), (65537, 136152)]:
        d = inverso_modular(e, phi)
        assert 1 <= d < phi and (e * d) % phi == 1
    for malo in [(4, 8), (6, 9), (3, 1), (0, 7)]:
        debe_fallar(inverso_modular, *malo)


def test_exponenciacion_modular():
    assert exponenciacion_modular(2, 10, 1000) == 24
    assert exponenciacion_modular(3, 4, 5) == 1        # 81 mod 5
    assert exponenciacion_modular(5, 0, 7) == 1
    assert exponenciacion_modular(0, 5, 7) == 0
    assert exponenciacion_modular(10, 3, 7) == 6       # b >= n
    for malo in [(2, -1, 5), (-2, 3, 5), (2, 3, 1), (2, 3, 0),
                 (2.0, 3, 5), (True, 3, 5)]:
        debe_fallar(exponenciacion_modular, *malo)


def test_ejemplo_referencia():
    p, q, e = 367, 373, 17
    n, phi = p * q, (p - 1) * (q - 1)
    assert (n, phi) == (136891, 136152)
    assert mcd(e, phi) == 1
    d = inverso_modular(e, phi)
    assert d == 8009
    # "RSA " -> 082083 065032 -> 026054 123875
    assert exponenciacion_modular(82083, e, n) == 26054
    assert exponenciacion_modular(65032, e, n) == 123875
    assert exponenciacion_modular(26054, d, n) == 82083
    assert exponenciacion_modular(123875, d, n) == 65032


if __name__ == "__main__":
    pruebas = [f for nombre, f in sorted(globals().items())
               if nombre.startswith("test_")]
    for prueba in pruebas:
        prueba()
        print(f"OK  {prueba.__name__}")
    print("Todas las pruebas pasaron.")