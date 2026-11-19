"""Pruebas de texto_bloques.py. Correr desde la raíz: python -m tests.test_texto_bloques"""

from texto_bloques import validar_mensaje, texto_a_bloques, bloques_a_texto
from validaciones import ErrorValidacion

fallos = 0


def comprobar(nombre, condicion):
    global fallos
    if not condicion:
        fallos += 1
        print(f"FALLA: {nombre}")


def lanza(excepcion, f, *args):
    try:
        f(*args)
    except excepcion:
        return True
    except Exception:
        return False
    return False


def ida_y_vuelta(m):
    r = texto_a_bloques(m)
    return bloques_a_texto(r.bloques, r.L).mensaje


# --- Ejemplo de referencia ---
r = texto_a_bloques("RSA")
comprobar("RSA: L", r.L == 3)
comprobar("RSA: relleno", r.relleno is True)
comprobar("RSA: texto con relleno", r.texto_relleno == "RSA ")
comprobar("RSA: códigos", r.codigos == [82, 83, 65, 32])
comprobar("RSA: bloques", r.bloques == [82083, 65032])
comprobar("RSA: bloques con 6 dígitos", r.bloques_str == ["082083", "065032"])
d = bloques_a_texto([82083, 65032], 3)
comprobar("RSA: recuperado", d.mensaje == "RSA")
comprobar("RSA: texto completo", d.texto_completo == "RSA ")
comprobar("RSA: relleno retirado", d.relleno is True)

# --- Longitud par e impar ---
r = texto_a_bloques("AB")
comprobar("par: sin relleno", r.relleno is False and r.bloques == [65066])
comprobar("par: ida y vuelta", ida_y_vuelta("AB") == "AB")
comprobar("impar: ida y vuelta", ida_y_vuelta("Hola") == "Hola")
comprobar("un carácter", ida_y_vuelta("Z") == "Z")

# --- Espacios ---
r = texto_a_bloques("  A")
comprobar("inicio: bloques", r.bloques == [32032, 65032] and r.relleno)
comprobar("inicio: ida y vuelta", ida_y_vuelta("  A") == "  A")
comprobar("final par: se conserva", ida_y_vuelta("A ") == "A ")
comprobar("final par: sin relleno", texto_a_bloques("A ").relleno is False)
comprobar("final impar: se conserva", ida_y_vuelta("A  ") == "A  ")
comprobar("final con relleno", texto_a_bloques("A  ").texto_relleno == "A   ")
comprobar("consecutivos", ida_y_vuelta("a   b") == "a   b")
comprobar("inicio y final", ida_y_vuelta("  hola mundo  ") == "  hola mundo  ")

# --- Ceros iniciales ---
r = texto_a_bloques("  ")
comprobar("032032: valor", r.bloques == [32032])
comprobar("032032: seis dígitos", r.bloques_str == ["032032"])
comprobar("032032: ida y vuelta", ida_y_vuelta("  ") == "  ")
comprobar("solo espacios impar", ida_y_vuelta("   ") == "   ")
comprobar("bloque 032065", texto_a_bloques(" A").bloques_str == ["032065"])

# --- Todos los caracteres admitidos ---
todos = ""
for c in range(32, 127):
    todos += chr(c)
comprobar("todos (95, impar)", ida_y_vuelta(todos) == todos)
comprobar("todos + espacio (96, par)", ida_y_vuelta(todos + " ") == todos + " ")
comprobar("mayúsculas, números y signos", ida_y_vuelta("Hola, Mundo! 123 #$%&") == "Hola, Mundo! 123 #$%&")

# --- Mensajes inválidos ---
for nombre, m in [("tilde", "canción"), ("ñ", "año"), ("tab", "a\tb"),
                  ("salto de línea", "a\nb"), ("retorno", "a\rb"),
                  ("char 31", chr(31)), ("char 127", chr(127))]:
    comprobar(f"inválido {nombre} (validar)", lanza(ErrorValidacion, validar_mensaje, m))
    comprobar(f"inválido {nombre} (texto_a_bloques)", lanza(ErrorValidacion, texto_a_bloques, m))
comprobar("vacío", lanza(ErrorValidacion, validar_mensaje, ""))
comprobar("no es str", lanza(TypeError, validar_mensaje, 123))
try:
    validar_mensaje("canción")
except ErrorValidacion as e:
    comprobar("el mensaje de error indica la posición", "posición 6" in str(e))

# --- bloques_a_texto: errores ---
comprobar("código < 32", lanza(ErrorValidacion, bloques_a_texto, [31032], 2))
comprobar("código > 126", lanza(ErrorValidacion, bloques_a_texto, [127032], 2))
comprobar("bloque 000000", lanza(ErrorValidacion, bloques_a_texto, [0], 2))
comprobar("bloque 065127", lanza(ErrorValidacion, bloques_a_texto, [65127], 2))
comprobar("bloque > 999999", lanza(ErrorValidacion, bloques_a_texto, [1000000], 2))
comprobar("bloque negativo", lanza(ErrorValidacion, bloques_a_texto, [-1], 2))
comprobar("lista vacía", lanza(ErrorValidacion, bloques_a_texto, [], 0))
comprobar("L muy grande", lanza(ErrorValidacion, bloques_a_texto, [65066], 3))
comprobar("L muy pequeña", lanza(ErrorValidacion, bloques_a_texto, [65066, 65066], 2))
comprobar("L = 0", lanza(ErrorValidacion, bloques_a_texto, [65066], 0))
comprobar("L impar sin espacio al final", lanza(ErrorValidacion, bloques_a_texto, [65066], 1))
comprobar("L par no exige espacio", bloques_a_texto([65066], 2).mensaje == "AB")
comprobar("L par no quita espacio", bloques_a_texto([65032], 2).mensaje == "A ")
comprobar("L impar quita solo uno", bloques_a_texto([65032, 32032], 3).mensaje == "A  ")

# --- Errores de programación ---
comprobar("bloques no es lista", lanza(TypeError, bloques_a_texto, "065066", 2))
comprobar("bloque no entero", lanza(TypeError, bloques_a_texto, ["065066"], 2))
comprobar("L no entero", lanza(TypeError, bloques_a_texto, [65066], "2"))

if fallos == 0:
    print("Todas las pruebas de texto_bloques pasaron.")
else:
    raise AssertionError(f"{fallos} prueba(s) fallaron.")
