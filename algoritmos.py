"""
Primo
Determinar si un entero es primo mediante división de prueba.
Entradas: `n` entero
Salida: `True` si n es primo, `False` en caso contrario
"""
def es_primo(n: int) -> bool:
    """True si n es primo (division de prueba hasta la raiz de n)."""

    if n < 2:
        return False

    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

"""
Algoritmo euclidiano
Implementar el algoritmo euclidiano para calcular el MCD de dos enteros positivos.

Entradas: a y b enteros positivos

Salida: el MCD de a y b
"""
def mcd(a: int, b: int) -> int:
    """MCD de dos enteros positivos mediante el algoritmo de Euclides."""
    for valor in (a, b):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("a y b deben ser enteros")
        if valor <= 0:
            raise ValueError("a y b deben ser positivos")

    dividendo = a
    divisor = b
    while divisor != 0:
        dividendo, divisor = divisor, dividendo % divisor
    return dividendo

"""
Algoritmo euclidiano extendido: versión matricial
Implementar el algoritmo euclidiano extendido (versión matricial) para resolver la ecuación de Bezout para dos enteros positivos:

                ax+by=mcd(a,b). 

Entradas: a y b enteros positivos

Salida: una tupla (x, y) con los coeficientes de Bezout
"""
def bezout_matricial(a: int, b: int) -> tuple[int, int]:
    """Devuelve (x, y) con a*x + b*y = MCD(a, b)."""

    # Validar entradas
    for valor in (a, b):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("a y b deben ser enteros")
        if valor <= 0:
            raise ValueError("a y b deben ser positivos")

    dividendo = a
    divisor = b

    # M empieza como la matriz identidad: [[arriba_izq, arriba_der], [abajo_izq, abajo_der]]
    arriba_izq, arriba_der = 1, 0
    abajo_izq, abajo_der = 0, 1

    while divisor != 0:
        cociente = dividendo // divisor
        residuo = dividendo % divisor

        # M = M * Q, donde Q = [[cociente, 1], [1, 0]]
        arriba_izq, arriba_der = arriba_izq * cociente + arriba_der, arriba_izq
        abajo_izq, abajo_der = abajo_izq * cociente + abajo_der, abajo_izq

        dividendo = divisor
        divisor = residuo

    # La inversa de M es (1/det) * [[abajo_der, -arriba_der], [-abajo_izq, arriba_izq]]
    # det(M) = (-1)^k, k = número de pasos; por eso 1/det = det
    determinante = arriba_izq * abajo_der - arriba_der * abajo_izq

    x = abajo_der * determinante
    y = -arriba_der * determinante

    return (x, y)

"""
Inverso modular
Calcular el inverso de e módulo φ usando el algoritmo euclidiano extendido.
Entradas: `e` y `phi` enteros, con `phi >= 2` y MCD(e, phi) = 1
Salida: el entero `d` con e·d ≡ 1 (mod phi) y 1 <= d < phi

phi es φ(n) = (p - 1)(q - 1), la cantidad de enteros en [1, n]
primos relativos con n = p·q. En RSA, d es el exponente privado.
"""
def inverso_modular(e: int, phi: int) -> int:
    """Devuelve d con e*d = 1 (mod phi) y 1 <= d < phi."""

    if phi < 2:
        raise ValueError("phi debe ser mayor que 1")
    if mcd(e, phi) != 1:
        raise ValueError("e no tiene inverso modulo phi (MCD distinto de 1)")

    x, _ = bezout_matricial(e, phi)
    return x % phi


"""
Exponenciación modular
Implementar el algoritmo de exponenciación modular estudiado en clase.

Entradas: la base b, el exponente e y el módulo n; b y e enteros no negativos, n >= 2

Salida: b^e mod n
"""
def exponenciacion_modular(b: int, e: int, n: int) -> int:
    """Calcula b^e mod n para b, e >= 0 y n >= 2."""

    # Validar entradas
    for valor in (b, e, n):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("b, e y n deben ser enteros")
    if b < 0 or e < 0:
        raise ValueError("b y e no pueden ser negativos")
    if n < 2:
        raise ValueError("n debe ser al menos 2")

    b = b % n

    # Anotar los exponentes hasta llegar a 0
    exponentes = []
    exponente_actual = e

    while exponente_actual > 0:
        exponentes.append(exponente_actual)
        exponente_actual = exponente_actual // 2

    # Sustituir en reversa empezando desde b^0 = 1
    resultado = 1

    for exponente in reversed(exponentes):
        resultado = (resultado * resultado) % n

        if exponente % 2 == 1:
            resultado = (resultado * b) % n

    return resultado