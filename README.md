# Proyecto RSA — MM2015 Matemática Discreta 1

**Autores:**

- Weslly Cabrera — Carnet 25771
- Ricardo Escobar — Carnet 25891

## Requisitos e instalación

El proyecto requiere Python 3.10 o superior y usa únicamente la biblioteca estándar de Python. No necesita instalar dependencias externas ni incluye un archivo `requirements.txt`.

## Ejecución

Desde la carpeta del proyecto, iniciar la aplicación con:

```console
py interfaz.py
```

En sistemas donde el intérprete se llama `python` o `python3`, usar ese comando en lugar de `py`.

Para ejecutar las pruebas automáticas:

```console
py run_tests.py
```

## Uso de la aplicación

La pestaña **Encriptar** recibe el mensaje, p, q y e. Al completar una operación válida muestra el cifrado C, la longitud original L y la llave pública `(e, n)`. El botón **Enviar C y L a Desencriptar** copia los datos necesarios a la otra pestaña.

La pestaña **Desencriptar** recibe C, L, p, q y e. C debe contener bloques de exactamente seis dígitos separados por un solo espacio. Con los mismos valores RSA utilizados para cifrar, la aplicación muestra el exponente privado d y el mensaje recuperado.

El área **Detalle del proceso** muestra n, φ, L, la presencia de relleno, los códigos ASCII y los bloques numéricos m y c. En desencriptación incluye d.

Se admiten únicamente caracteres ASCII imprimibles, del código 32 al 126. Si el mensaje original tiene longitud impar, se agrega un solo espacio al final para formar parejas. Ese espacio se verifica y se elimina al desencriptar; los demás espacios, incluso los iniciales y finales, se conservan.

## Implementación

- `algoritmos.py`: comprobación de primalidad, MCD, algoritmo de Bézout, inverso modular y exponenciación modular propia.
- `validaciones.py`: validación de p, q, e, n, φ y formato de enteros.
- `texto_bloques.py`: conversión ASCII, creación de bloques y relleno.
- `rsa.py`: encriptación, desencriptación y validación de C y L.
- `interfaz.py`: interfaz gráfica construida con Tkinter.

## Pruebas sugeridas

| Operación | Entradas | Salida esperada |
|---|---|---|
| Encriptar | M = `RSA`, p = 367, q = 373, e = 17 | C = `026054 123875`, L = 3, n = 136891, φ = 136152; se indica relleno. |
| Desencriptar | C = `026054 123875`, L = 3, p = 367, q = 373, e = 17 | d = 8009 y M = `RSA`. |
| Encriptar y desencriptar | M = `  Hola 123!  `, p = 367, q = 373, e = 17 | Se recupera exactamente el mensaje, incluidos sus espacios extremos. |
| Validación | M = `año`, p = 367, q = 373, e = 17 | Se informa que `ñ` no pertenece al ASCII imprimible admitido. |
| Validación | M = `RSA`, p = 367, q = 373, e = 2 | Se informa que e no es primo relativo con φ. |

Las pruebas automáticas cubren además longitudes pares e impares, signos, números, espacios consecutivos, ceros iniciales en C, parámetros inválidos, bloques mal formados y longitudes inconsistentes.
