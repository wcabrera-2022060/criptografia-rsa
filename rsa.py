"""Encriptación RSA: une validaciones, conversión a bloques y exponenciación modular."""
from typing import NamedTuple

from algoritmos import exponenciacion_modular
from validaciones import ErrorValidacion, validar_parametros
from texto_bloques import texto_a_bloques


class ResultadoCifrado(NamedTuple):
    C: str                       # bloques cifrados de 6 dígitos separados por un espacio
    L: int                       # longitud original del mensaje
    llave_publica: tuple         # (e, n)
    n: int
    phi: int
    hubo_relleno: bool
    texto_relleno: str           # mensaje con el espacio de relleno (si lo hubo)
    codigos: list                # códigos ASCII, uno por carácter del texto con relleno
    bloques_m: list              # bloques numéricos antes de cifrar
    bloques_c: list              # bloques numéricos cifrados


def encriptar(mensaje, p_txt, q_txt, e_txt):
    """Cifra `mensaje` con RSA. Lanza ErrorValidacion si los datos son inválidos."""
    # 1. Primero parámetros; luego el mensaje (texto_a_bloques lo valida al inicio).
    params = validar_parametros(p_txt, q_txt, e_txt)
    texto = texto_a_bloques(mensaje)

    # 2. Cifrado bloque por bloque.
    bloques_c = []
    for m in texto.bloques:
        if not 0 <= m < params.n:
            raise ErrorValidacion(
                f"El bloque {m:06d} no es menor que n = {params.n}; no se puede cifrar."
            )
        bloques_c.append(exponenciacion_modular(m, params.e, params.n))

    C = " ".join(f"{c:06d}" for c in bloques_c)

    return ResultadoCifrado(
        C=C,
        L=texto.L,
        llave_publica=(params.e, params.n),
        n=params.n,
        phi=params.phi,
        hubo_relleno=texto.relleno,
        texto_relleno=texto.texto_relleno,
        codigos=texto.codigos,
        bloques_m=texto.bloques,
        bloques_c=bloques_c,
    )