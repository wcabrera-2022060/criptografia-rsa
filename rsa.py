"""Operaciones RSA y datos del proceso para mostrar en la interfaz gráfica."""

from typing import NamedTuple

from algoritmos import exponenciacion_modular, inverso_modular
from validaciones import ErrorValidacion, validar_parametros, texto_a_entero, DIGITOS
from texto_bloques import texto_a_bloques, bloques_a_texto, BLOQUE_MAX


class ResultadoCifrado(NamedTuple):
    C: str
    L: int
    llave_publica: tuple[int, int]
    n: int
    phi: int
    mcd_e_phi: int
    k: int
    hubo_relleno: bool
    mensaje: str
    texto_completo: str          # incluye el espacio de relleno si L es impar
    codigos: list                # ASCII del texto completo, incluido el relleno
    bloques_m: list
    bloques_c: list


def encriptar(mensaje, p_txt, q_txt, e_txt):
    """Cifra el mensaje sin alterar sus espacios; devuelve C, L y el detalle.

    Los parámetros RSA se reciben como texto desde los campos de la interfaz.
    Los datos inválidos del usuario producen ErrorValidacion.
    """
    params = validar_parametros(p_txt, q_txt, e_txt)
    texto = texto_a_bloques(mensaje)
    bloques_c = [
        exponenciacion_modular(m, params.e, params.n)
        for m in texto.bloques
    ]
    return ResultadoCifrado(
        C=" ".join(f"{c:06d}" for c in bloques_c),
        L=texto.L,
        llave_publica=(params.e, params.n),
        n=params.n,
        phi=params.phi,
        mcd_e_phi=1,
        k=len(bloques_c),
        hubo_relleno=texto.relleno,
        mensaje=mensaje,
        texto_completo=texto.texto_relleno,
        codigos=texto.codigos,
        bloques_m=texto.bloques,
        bloques_c=bloques_c,
    )


class ResultadoDescifrado(NamedTuple):
    d: int                       # exponente privado
    n: int
    phi: int
    mcd_e_phi: int
    L: int
    k: int                       # cantidad de bloques cifrados
    hubo_relleno: bool           # True si L es impar
    bloques_c: list              # bloques cifrados (enteros)
    bloques_m: list              # bloques numéricos recuperados
    codigos: list                # códigos ASCII recuperados (con relleno)
    texto_completo: str          # texto recuperado, con el relleno si lo hubo
    mensaje: str                 # mensaje original


def _validar_cifrado(c_txt, n):
    """Devuelve la lista de bloques c (enteros) o lanza ErrorValidacion."""
    if not isinstance(c_txt, str):
        raise TypeError("c_txt debe ser una cadena de texto.")
    if c_txt == "":
        raise ErrorValidacion("El cifrado C está vacío; debe tener al menos un bloque.")

    bloques = []
    for i, trozo in enumerate(c_txt.split(" "), start=1):
        if trozo == "":
            raise ErrorValidacion(
                "Los bloques de C deben separarse por exactamente un espacio, "
                "sin espacios al inicio, al final ni consecutivos."
            )
        for car in trozo:
            if car not in DIGITOS:
                raise ErrorValidacion(
                    f"El bloque {i} contiene un carácter no permitido ({car!r}); "
                    "solo se aceptan dígitos del 0 al 9 separados por un espacio."
                )
        if len(trozo) != 6:
            raise ErrorValidacion(
                f"El bloque {i} tiene {len(trozo)} dígitos; debe tener exactamente 6."
            )
        c = int(trozo)
        if c >= n:
            raise ErrorValidacion(
                f"El bloque {i} ({trozo}) no es menor que n = {n}."
            )
        bloques.append(c)
    return bloques


def desencriptar(c_txt, l_txt, p_txt, q_txt, e_txt):
    """Descifra C con RSA. Lanza ErrorValidacion si los datos son inválidos."""
    # 1. Parámetros, luego C, luego L.
    params = validar_parametros(p_txt, q_txt, e_txt)
    bloques_c = _validar_cifrado(c_txt, params.n)
    k = len(bloques_c)

    L = texto_a_entero(l_txt, "L")
    if L not in (2 * k, 2 * k - 1):
        raise ErrorValidacion(
            f"L = {L} no es coherente con {k} bloque(s): debe ser {2 * k} o {2 * k - 1}."
        )

    # 2. Exponente privado y descifrado bloque por bloque.
    d = inverso_modular(params.e, params.phi)
    bloques_m = []
    for c in bloques_c:
        m = exponenciacion_modular(c, d, params.n)
        if not 0 <= m <= BLOQUE_MAX:
            raise ErrorValidacion(
                f"El bloque {c:06d} se descifró como {m}, que no cabe en 6 dígitos. "
                "Revise que p, q y e sean los usados al encriptar."
            )
        bloques_m.append(m)

    # 3. Texto. bloques_a_texto valida códigos, relleno y L; si falla, casi seguro
    #    los parámetros no son los de la encriptación.
    try:
        res = bloques_a_texto(bloques_m, L)
    except ErrorValidacion as ex:
        raise ErrorValidacion(
            f"No se pudo recuperar un mensaje válido: {ex} "
            "Revise que p, q y e sean los usados al encriptar."
        ) from ex

    return ResultadoDescifrado(
        d=d,
        n=params.n,
        phi=params.phi,
        mcd_e_phi=1,
        L=L,
        k=k,
        hubo_relleno=res.relleno,
        bloques_c=bloques_c,
        bloques_m=bloques_m,
        codigos=res.codigos,
        texto_completo=res.texto_completo,
        mensaje=res.mensaje,
    )
