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
      .stApp { background: #F4F7FB; color: #243B53; }
      [data-testid="stHeader"], #MainMenu, footer { background: transparent; visibility: hidden; }
      .block-container { max-width: 1180px; padding-top: 1.8rem; padding-bottom: 2rem; }
      .rsa-banner {
        background: #102A43; border-radius: 10px; color: white;
        padding: 1.25rem 1.8rem; margin-bottom: 1.2rem;
      }
      .rsa-banner h1 { margin: 0; font-size: 2.1rem; letter-spacing: .02em; }
      .rsa-banner p { color: #C9D9E8; margin: .2rem 0 0; }
      .app-pill {
        display: inline-block; float: right; margin-top: -3.4rem; color: #EAF3FA;
        background: #1A4569; padding: .4rem .75rem; border-radius: 5px;
        font-size: .8rem; font-weight: 700;
      }
      .page-title { color: #102A43; font-size: 1.45rem; font-weight: 700; margin: .4rem 0 0; }
      .page-subtitle { color: #627D98; font-size: .93rem; margin: .1rem 0 1.1rem; }
      .section-title { color: #102A43; font-size: 1.1rem; font-weight: 700; margin: 0; }
      .section-help { color: #627D98; font-size: .85rem; margin: .1rem 0 1rem; }
      .detail-title { color: #102A43; font-size: 1.1rem; font-weight: 700; margin: 0; }
      .detail-help { color: #627D98; font-size: .85rem; margin: .15rem 0 .75rem; }
      [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF; border-color: #D9E2EC !important; border-radius: 7px;
        box-shadow: 0 1px 2px rgba(16,42,67,.04);
      }
      [data-baseweb="tab-list"] { gap: 3px; border-bottom: 0; }
      [data-baseweb="tab"] {
        background: #DCE6F0; border-radius: 6px 6px 0 0; color: #627D98;
        font-weight: 700; padding: .6rem 1.3rem;
      }
      [aria-selected="true"][data-baseweb="tab"] { background: #FFFFFF; color: #102A43; }
      [data-baseweb="tab-highlight"] { background-color: #FFFFFF !important; }
      .stButton > button {
        background: #1D6FA5; color: white; border: 0; border-radius: 5px;
        font-weight: 700; padding: .55rem 1rem;
      }
      .stButton > button:hover { background: #155A87; color: white; border: 0; }
      .stTextInput input, .stTextArea textarea {
        background: #FBFDFF; border-color: #D9E2EC; color: #243B53;
        font-family: "Cascadia Mono", Consolas, monospace;
      }
      .stTextInput label, .stTextArea label { color: #243B53 !important; font-weight: 700; }
      [data-testid="stCodeBlock"] { border: 1px solid #D9E2EC; border-radius: 4px; }
      .rsa-footer { color: #627D98; font-size: .78rem; text-align: center; margin-top: 1.5rem; }
    </style>
    <div class="rsa-banner">
      <h1>RSA</h1>
      <p>Cifrado de texto · Matemática Discreta 1 &nbsp;·&nbsp; ASCII 32–126 · bloques de 2 caracteres</p>
    </div>
    <div class="app-pill">ASCII 32–126 · bloques de 2 caracteres</div>
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
    with st.container(border=True):
        st.markdown('<p class="detail-title">Detalle del proceso</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="detail-help">Valores calculados y relación entre cada pareja de caracteres, m y c.</p>',
            unsafe_allow_html=True,
        )
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
    st.markdown('<p class="page-title">Encriptar mensaje</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Convierte el texto en bloques RSA de seis dígitos.</p>',
        unsafe_allow_html=True,
    )
    izquierda, derecha = st.columns(2, gap="large")
    with izquierda:
        with st.container(border=True):
            st.markdown('<p class="section-title">1. Datos de entrada</p>', unsafe_allow_html=True)
            st.markdown('<p class="section-help">El mensaje conserva mayúsculas, signos y espacios.</p>', unsafe_allow_html=True)
            mensaje = st.text_area(
                "Mensaje M", height=150,
                placeholder="Escribe el mensaje que deseas encriptar…",
                help="No se admiten tildes, ñ, tabulaciones ni saltos de línea.",
            )
            _parametros("enc")
            ejecutar_cifrado = st.button("Encriptar mensaje", type="primary", use_container_width=True)

    with derecha:
        with st.container(border=True):
            st.markdown('<p class="section-title">2. Resultado</p>', unsafe_allow_html=True)
            st.markdown('<p class="section-help">Guarda C y L; ambos se necesitan para desencriptar.</p>', unsafe_allow_html=True)
            if "resultado_cifrado" in st.session_state:
                resultado = st.session_state.resultado_cifrado
                st.markdown("**Cifrado C**")
                st.code(resultado.C, language=None)
                st.success(
                    f"Listo · L = {resultado.L} · llave pública = {resultado.llave_publica} · "
                    f"relleno: {'sí' if resultado.hubo_relleno else 'no'}"
                )
                if st.button("→ Enviar C y L a Desencriptar", use_container_width=True):
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
    st.markdown('<p class="page-title">Desencriptar mensaje</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Recupera el texto original con C, L y los parámetros RSA.</p>',
        unsafe_allow_html=True,
    )
    izquierda, derecha = st.columns(2, gap="large")
    with izquierda:
        with st.container(border=True):
            st.markdown('<p class="section-title">1. Datos de entrada</p>', unsafe_allow_html=True)
            st.markdown('<p class="section-help">C usa bloques de seis dígitos separados por un solo espacio.</p>', unsafe_allow_html=True)
            st.text_area("Cifrado C", key="des_c", height=130)
            st.text_input("Longitud original L", key="des_l")
            _parametros("des")
            ejecutar_descifrado = st.button("Desencriptar mensaje", type="primary", use_container_width=True)

    with derecha:
        with st.container(border=True):
            st.markdown('<p class="section-title">2. Mensaje recuperado</p>', unsafe_allow_html=True)
            st.markdown('<p class="section-help">El resultado conserva todos los espacios originales.</p>', unsafe_allow_html=True)
            if "resultado_descifrado" in st.session_state:
                resultado = st.session_state.resultado_descifrado
                st.markdown("**Mensaje M**")
                st.code(resultado.mensaje, language=None)
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

st.markdown(
    '<p class="rsa-footer">Proyecto RSA · MM2015 Matemática Discreta 1 · Validación ASCII 32–126</p>',
    unsafe_allow_html=True,
)
