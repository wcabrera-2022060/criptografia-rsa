"""Interfaz web desplegable del proyecto RSA.

Ejecutar localmente con: streamlit run app.py
La lógica matemática vive en los módulos del proyecto y no se duplica aquí.
"""

import streamlit as st

from rsa import desencriptar, encriptar
from validaciones import ErrorValidacion


st.set_page_config(
    page_title="RSA · Matemática Discreta 1",
    page_icon="🔐",
    layout="wide",
)

st.markdown(
    """
    <style>
      .stApp { background: #F4F7FB; }
      [data-testid="stHeader"] { background: transparent; }
      .rsa-banner {
        background: #102A43; border-radius: 12px; color: white;
        padding: 1.2rem 1.7rem; margin-bottom: 1.25rem;
      }
      .rsa-banner h1 { margin: 0; font-size: 2rem; }
      .rsa-banner p { color: #C9D9E8; margin: .2rem 0 0; }
      .block-container { padding-top: 1.8rem; }
    </style>
    <div class="rsa-banner">
      <h1>RSA</h1>
      <p>Cifrado de texto · Matemática Discreta 1 &nbsp;·&nbsp; ASCII 32–126 · bloques de 2 caracteres</p>
    </div>
    """,
    unsafe_allow_html=True,
)


def _inicializar_estado():
    """Crea las claves de sesión sin borrar resultados entre interacciones."""
    valores = {
        "enc_p": "367", "enc_q": "373", "enc_e": "17",
        "des_p": "367", "des_q": "373", "des_e": "17",
        "des_c": "", "des_l": "",
    }
    for clave, valor in valores.items():
        if clave not in st.session_state:
            st.session_state[clave] = valor


def _detalle(resultado, e, d=None):
    """Forma el panel de detalle solicitado en el enunciado."""
    if resultado.hubo_relleno:
        relleno = (
            "Sí; se retiró exactamente un espacio final de relleno."
            if d is not None
            else "Sí; se agregó exactamente un espacio final de relleno."
        )
    else:
        relleno = "No se requirió relleno."

    lineas = [
        f"LLAVE PÚBLICA: (e, n) = ({e}, {resultado.n})",
        f"n = {resultado.n}     φ = {resultado.phi}     MCD(e, φ) = {resultado.mcd_e_phi}",
        f"Longitud original L = {resultado.L}     Cantidad de bloques = {resultado.k}",
        f"Relleno: {relleno}",
    ]
    if d is not None:
        lineas.append(f"EXPONENTE PRIVADO: d = {d}")
    lineas.extend([
        f"Mensaje original/recuperado: {resultado.mensaje!r}",
        f"Texto con relleno: {resultado.texto_completo!r}",
        "ASCII: " + " ".join(f"{codigo:03d}" for codigo in resultado.codigos),
        "",
        " Nº  | caracteres | ASCII       | m (original) | c (cifrado)",
        "-----+------------+-------------+--------------+--------------",
    ])
    for indice, (m, c) in enumerate(zip(resultado.bloques_m, resultado.bloques_c), 1):
        base = (indice - 1) * 2
        caracteres = repr(resultado.texto_completo[base:base + 2])
        ascii_par = f"{resultado.codigos[base]:03d} {resultado.codigos[base + 1]:03d}"
        lineas.append(
            f"{indice:>4} | {caracteres:<10} | {ascii_par} | {m:06d}       | {c:06d}"
        )
    return "\n".join(lineas)


def _parametros(prefijo):
    """Campos p, q y e de una operación."""
    st.caption("p y q deben ser primos distintos.")
    a, b, c = st.columns(3)
    with a:
        st.text_input("p", key=f"{prefijo}_p")
    with b:
        st.text_input("q", key=f"{prefijo}_q")
    with c:
        st.text_input("e", key=f"{prefijo}_e")


def _mostrar_detalle(resultado, e, d=None):
    st.subheader("Detalle del proceso")
    st.caption("Valores calculados, ASCII y bloques numéricos de la operación.")
    st.code(_detalle(resultado, e, d), language=None)


def _mostrar_validaciones():
    with st.expander("Validaciones de datos", expanded=False):
        st.markdown(
            """
**Parámetros p, q y e:** enteros; p y q primos distintos; `126126 < n < 1000000`; `e > 1` y `MCD(e, φ) = 1`.

**Mensaje M:** únicamente ASCII imprimible, códigos 32 a 126. No se sustituyen ni eliminan caracteres.

**Cifrado C:** cada bloque tiene exactamente seis dígitos; se separan por un solo espacio y cumplen `0 ≤ c < n`.

**Longitud L:** si hay `k` bloques, debe ser `2k` o `2k − 1`. La opción impar requiere y retira exactamente un espacio de relleno.
            """
        )


_inicializar_estado()
_mostrar_validaciones()

tab_cifrar, tab_descifrar = st.tabs(["🔒 Encriptar", "🔓 Desencriptar"])

with tab_cifrar:
    izquierda, derecha = st.columns(2, gap="large")
    with izquierda:
        st.subheader("1. Datos de entrada")
        st.caption("El mensaje conserva mayúsculas, signos y espacios.")
        mensaje = st.text_area(
            "Mensaje M", height=150,
            placeholder="Escribe el mensaje que deseas encriptar…",
            help="No se admiten tildes, ñ, tabulaciones ni saltos de línea.",
        )
        _parametros("enc")
        ejecutar_cifrado = st.button("Encriptar mensaje", type="primary", use_container_width=True)

    with derecha:
        st.subheader("2. Resultado")
        st.caption("Guarda C y L; ambos se necesitan para desencriptar.")
        if "resultado_cifrado" in st.session_state:
            resultado = st.session_state.resultado_cifrado
            st.text_area("Cifrado C", value=resultado.C, height=150, disabled=True)
            st.success(
                f"Listo · L = {resultado.L} · llave pública = {resultado.llave_publica} · "
                f"relleno: {'sí' if resultado.hubo_relleno else 'no'}"
            )
            if st.button("Enviar C y L a Desencriptar", use_container_width=True):
                st.session_state.des_c = resultado.C
                st.session_state.des_l = str(resultado.L)
                st.session_state.des_p = st.session_state.enc_p
                st.session_state.des_q = st.session_state.enc_q
                st.session_state.des_e = st.session_state.enc_e
                st.toast("C, L y parámetros copiados a Desencriptar.")
        else:
            st.info("Completa los datos y presiona Encriptar.")

    if ejecutar_cifrado:
        try:
            st.session_state.resultado_cifrado = encriptar(
                mensaje, st.session_state.enc_p, st.session_state.enc_q, st.session_state.enc_e
            )
            st.rerun()
        except (ErrorValidacion, TypeError) as error:
            st.error(f"Datos inválidos: {error}")

    if "resultado_cifrado" in st.session_state:
        _mostrar_detalle(st.session_state.resultado_cifrado, st.session_state.enc_e)

with tab_descifrar:
    izquierda, derecha = st.columns(2, gap="large")
    with izquierda:
        st.subheader("1. Datos de entrada")
        st.caption("C usa bloques de seis dígitos separados por un solo espacio.")
        st.text_area("Cifrado C", key="des_c", height=130)
        st.text_input("Longitud original L", key="des_l")
        _parametros("des")
        ejecutar_descifrado = st.button("Desencriptar mensaje", type="primary", use_container_width=True)

    with derecha:
        st.subheader("2. Mensaje recuperado")
        st.caption("El resultado conserva todos los espacios originales.")
        if "resultado_descifrado" in st.session_state:
            resultado = st.session_state.resultado_descifrado
            st.text_area("Mensaje M", value=resultado.mensaje, height=150, disabled=True)
            st.success(
                f"Listo · d = {resultado.d} · L = {resultado.L} · "
                f"relleno retirado: {'sí' if resultado.hubo_relleno else 'no'}"
            )
        else:
            st.info("Completa los datos y presiona Desencriptar.")

    if ejecutar_descifrado:
        try:
            st.session_state.resultado_descifrado = desencriptar(
                st.session_state.des_c, st.session_state.des_l,
                st.session_state.des_p, st.session_state.des_q, st.session_state.des_e,
            )
            st.rerun()
        except (ErrorValidacion, TypeError) as error:
            st.error(f"Datos inválidos: {error}")

    if "resultado_descifrado" in st.session_state:
        resultado = st.session_state.resultado_descifrado
        _mostrar_detalle(resultado, st.session_state.des_e, resultado.d)
