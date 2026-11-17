"""Conversión entre texto y bloques numéricos para el proyecto RSA.

Cada carácter ASCII imprimible (32 a 126) se escribe con tres dígitos y cada
bloque junta dos caracteres: "AB" -> 065066 -> 65066.

Errores del usuario -> ErrorValidacion. Errores de programación -> TypeError.
"""

from typing import NamedTuple

from validaciones import ErrorValidacion

CODIGO_MIN = 32
CODIGO_MAX = 126
CODIGO_ESPACIO = 32
BLOQUE_MAX = 999999  # el mayor valor que cabe en seis dígitos


class ResultadoTexto(NamedTuple):
    mensaje: str          # mensaje original
    L: int                # longitud original (con todos sus espacios)
    relleno: bool         # True si se agregó un espacio al final
    texto_relleno: str    # mensaje con relleno (longitud par)
    codigos: list         # códigos ASCII del texto con relleno
    bloques: list         # valores m = código1 * 1000 + código2
    bloques_str: list     # los mismos bloques con seis dígitos


class ResultadoBloques(NamedTuple):
    bloques: list         # valores m recibidos
    bloques_str: list     # m con seis dígitos
    codigos: list         # códigos ASCII recuperados (dos por bloque)
    texto_completo: str   # texto recuperado antes de quitar el relleno
    relleno: bool         # True si se retiró un espacio de relleno
    mensaje: str          # mensaje final


def validar_mensaje(m):
    """Acepta solo caracteres con código 32 a 126. No modifica el mensaje.

    El mensaje vacío se rechaza: no produciría bloques y no habría nada que
    desencriptar (L debe ser 2k o 2k - 1 con k > 0).
    """
    if not isinstance(m, str):
        raise TypeError("El mensaje debe ser una cadena de texto.")
    if len(m) == 0:
        raise ErrorValidacion("El mensaje está vacío. Escribe al menos un carácter.")
    for i in range(len(m)):
        c = m[i]
        if ord(c) < CODIGO_MIN or ord(c) > CODIGO_MAX:
            raise ErrorValidacion(
                f"El carácter {c!r} (posición {i + 1}) no está permitido. "
                f"Solo se admiten caracteres ASCII imprimibles "
                f"(códigos {CODIGO_MIN} a {CODIGO_MAX}); no se aceptan "
                f"tildes, ñ, tabulaciones ni saltos de línea."
            )


def texto_a_bloques(m):
    """Convierte el mensaje en bloques numéricos (agrega un espacio si L es impar)."""
    validar_mensaje(m)
    L = len(m)
    relleno = L % 2 == 1
    texto_relleno = m + " " if relleno else m

    codigos = []
    for c in texto_relleno:
        codigos.append(ord(c))

    bloques = []
    for i in range(0, len(codigos), 2):
        bloques.append(codigos[i] * 1000 + codigos[i + 1])

    bloques_str = [f"{b:06d}" for b in bloques]
    return ResultadoTexto(m, L, relleno, texto_relleno, codigos, bloques, bloques_str)


def bloques_a_texto(bloques, L):
    """Convierte bloques numéricos en el mensaje original.

    Comprueba que L sea 2k o 2k - 1, que cada bloque tenga seis dígitos, que
    cada código esté entre 32 y 126 y, si L es impar, que el carácter de
    relleno sea un espacio. Solo se quita ese último carácter.
    """
    if not isinstance(bloques, list):
        raise TypeError("bloques debe ser una lista de enteros.")
    for b in bloques:
        if not isinstance(b, int) or isinstance(b, bool):
            raise TypeError("Cada bloque debe ser un entero.")
    if not isinstance(L, int) or isinstance(L, bool):
        raise TypeError("L debe ser un entero.")

    k = len(bloques)
    if k == 0:
        raise ErrorValidacion("No hay bloques que desencriptar.")
    if L != 2 * k and L != 2 * k - 1:
        raise ErrorValidacion(
            f"La longitud L = {L} no es coherente con {k} bloque(s): "
            f"debe ser {2 * k} o {2 * k - 1}."
        )

    bloques_str = []
    codigos = []
    texto_completo = ""
    for i in range(k):
        b = bloques[i]
        if b < 0 or b > BLOQUE_MAX:
            raise ErrorValidacion(
                f"El bloque {i + 1} ({b}) no cabe en seis dígitos."
            )
        s = f"{b:06d}"
        c1 = int(s[:3])
        c2 = int(s[3:])
        for c in (c1, c2):
            if c < CODIGO_MIN or c > CODIGO_MAX:
                raise ErrorValidacion(
                    f"El bloque {i + 1} ({s}) produce el código {c:03d}, "
                    f"fuera del rango {CODIGO_MIN} a {CODIGO_MAX}. "
                    f"Revisa p, q, e o el cifrado."
                )
        bloques_str.append(s)
        codigos.append(c1)
        codigos.append(c2)
        texto_completo += chr(c1) + chr(c2)

    relleno = L % 2 == 1
    if relleno:
        if ord(texto_completo[-1]) != CODIGO_ESPACIO:
            raise ErrorValidacion(
                "L es impar, pero el último carácter recuperado no es un "
                "espacio de relleno. Revisa p, q, e, el cifrado o L."
            )
        mensaje = texto_completo[:-1]  # quita solo el relleno
    else:
        mensaje = texto_completo

    return ResultadoBloques(list(bloques), bloques_str, codigos,
                            texto_completo, relleno, mensaje)