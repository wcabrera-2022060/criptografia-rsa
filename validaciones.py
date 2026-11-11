"""Validación de los parámetros RSA (p, q, e) recibidos como texto desde la interfaz.

Toda la lógica de decisión está aquí, para poder probarla por separado.
Los errores se reportan con ErrorValidacion, con mensaje listo para mostrarse en pantalla.
"""

from typing import NamedTuple

from algoritmos import es_primo, mcd

N_MIN = 126126        # n debe ser estrictamente mayor
N_MAX = 1000000       # n debe ser estrictamente menor
P_MAX = (N_MAX - 1) // 2   # 499999: el otro primo es >= 2, así que p*q < N_MAX obliga p <= 499999
LARGO_MAX = 100       # tope de caracteres por campo
DIGITOS = "0123456789"


class ErrorValidacion(Exception):
    """Dato inválido. El mensaje es comprensible para el usuario."""


class ParametrosRSA(NamedTuple):
    p: int
    q: int
    e: int
    n: int
    phi: int


def texto_a_entero(texto, nombre):
    """Convierte texto a entero no negativo aceptando únicamente los dígitos 0-9."""
    if not isinstance(texto, str):
        raise TypeError("texto_a_entero espera un str")

    if texto.strip() == "":
        raise ErrorValidacion(f"{nombre} está vacío. Escribe un número entero.")

    if len(texto) > LARGO_MAX:
        raise ErrorValidacion(
            f"{nombre} es demasiado largo (máximo {LARGO_MAX} dígitos)."
        )

    for c in texto:
        if c in DIGITOS:
            continue
        if c in "+-":
            raise ErrorValidacion(
                f"{nombre} debe ser un entero positivo, sin signo ('{c}' no es válido)."
            )
        if c in ".,":
            raise ErrorValidacion(
                f"{nombre} debe ser un entero, sin decimales ni separadores ('{c}' no es válido)."
            )
        if c.isspace():
            raise ErrorValidacion(
                f"{nombre} contiene espacios. Escribe solo dígitos, sin espacios."
            )
        raise ErrorValidacion(
            f"{nombre} contiene un carácter no válido ({c!r}). Usa solo dígitos del 0 al 9."
        )

    return int(texto)


def validar_parametros(p_txt, q_txt, e_txt):
    """Valida p, q y e (texto) y devuelve ParametrosRSA(p, q, e, n, phi).

    Orden de las comprobaciones:
      1. Formato de p, q y e (enteros, solo dígitos 0-9).
      2. Límite de tamaño de p y q.
      3. p y q primos.
      4. p y q distintos.
      5. 126126 < n < 1000000.
      6. e > 1.
      7. MCD(e, phi) = 1.
    """
    p = texto_a_entero(p_txt, "p")
    q = texto_a_entero(q_txt, "q")
    e = texto_a_entero(e_txt, "e")

    for nombre, valor in (("p", p), ("q", q)):
        if valor > P_MAX:
            raise ErrorValidacion(
                f"{nombre} = {valor} es demasiado grande: como n = p·q debe ser menor que "
                f"{N_MAX} y el otro primo es al menos 2, {nombre} no puede superar {P_MAX}."
            )

    for nombre, valor in (("p", p), ("q", q)):
        if not es_primo(valor):
            raise ErrorValidacion(f"{nombre} = {valor} no es primo.")

    if p == q:
        raise ErrorValidacion(f"p y q deben ser primos distintos (ambos son {p}).")

    n = p * q
    phi = (p - 1) * (q - 1)

    if n <= N_MIN:
        raise ErrorValidacion(
            f"n = p·q = {n} es demasiado pequeño: debe ser mayor que {N_MIN} "
            "para poder representar cualquier pareja de caracteres."
        )
    if n >= N_MAX:
        raise ErrorValidacion(
            f"n = p·q = {n} es demasiado grande: debe ser menor que {N_MAX} "
            "para que cada bloque cifrado quepa en seis dígitos."
        )

    if e <= 1:
        raise ErrorValidacion(f"e = {e} no es válido: debe ser mayor que 1.")

    g = mcd(e, phi)
    if g != 1:
        raise ErrorValidacion(
            f"e = {e} no es primo relativo con φ = {phi}: MCD(e, φ) = {g}. Elige otro e."
        )

    return ParametrosRSA(p, q, e, n, phi)