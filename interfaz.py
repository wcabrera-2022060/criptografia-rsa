"""Interfaz gráfica del proyecto RSA.

Ejecutar desde la raíz del proyecto con: py interfaz.py
"""

import tkinter as tk
from tkinter import messagebox, ttk

from rsa import desencriptar, encriptar
from validaciones import ErrorValidacion


AZUL_OSCURO = "#102A43"
AZUL = "#1D6FA5"
AZUL_CLARO = "#E8F2FA"
FONDO = "#F4F7FB"
TARJETA = "#FFFFFF"
TEXTO = "#243B53"
SECUNDARIO = "#627D98"
VERDE = "#16806A"
ROJO = "#C2414C"
BORDE = "#D9E2EC"
FUENTE = "Segoe UI"
MONO = ("Cascadia Mono", 10)


class AplicacionRSA(tk.Tk):
    """Ventana para cifrar y descifrar texto con RSA."""

    def __init__(self):
        super().__init__()
        self.title("RSA · Matemática Discreta 1")
        self.geometry("1120x780")
        self.minsize(960, 700)
        self.configure(bg=FONDO)
        self._configurar_estilos()
        self._crear_encabezado()

        self.libro = ttk.Notebook(self, style="Principal.TNotebook")
        self.libro.pack(fill="both", expand=True, padx=26, pady=(18, 24))
        self.pestana_cifrar = ttk.Frame(self.libro, style="Pagina.TFrame", padding=18)
        self.pestana_descifrar = ttk.Frame(self.libro, style="Pagina.TFrame", padding=18)
        self.libro.add(self.pestana_cifrar, text="  Encriptar  ")
        self.libro.add(self.pestana_descifrar, text="  Desencriptar  ")

        self._crear_pestana_cifrar()
        self._crear_pestana_descifrar()

    def _configurar_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("Pagina.TFrame", background=FONDO)
        estilo.configure("Principal.TNotebook", background=FONDO, borderwidth=0)
        estilo.configure(
            "Principal.TNotebook.Tab", background="#DCE6F0", foreground=SECUNDARIO,
            padding=(18, 9), font=(FUENTE, 10, "bold"), borderwidth=0,
        )
        estilo.map(
            "Principal.TNotebook.Tab",
            background=[("selected", TARJETA), ("active", "#EAF1F7")],
            foreground=[("selected", AZUL_OSCURO)],
        )
        estilo.configure("Titulo.TLabel", background=FONDO, foreground=AZUL_OSCURO,
                        font=(FUENTE, 18, "bold"))
        estilo.configure("Subtitulo.TLabel", background=FONDO, foreground=SECUNDARIO,
                        font=(FUENTE, 10))
        estilo.configure("Etiqueta.TLabel", background=TARJETA, foreground=TEXTO,
                        font=(FUENTE, 10, "bold"))
        estilo.configure("Ayuda.TLabel", background=TARJETA, foreground=SECUNDARIO,
                        font=(FUENTE, 9))
        estilo.configure("Resultado.TLabel", background=TARJETA, foreground=AZUL_OSCURO,
                        font=(FUENTE, 10, "bold"))
        estilo.configure("Estado.TLabel", background=TARJETA, foreground=VERDE,
                        font=(FUENTE, 10, "bold"))
        estilo.configure("TButton", font=(FUENTE, 10, "bold"), padding=(14, 8))
        estilo.configure("Primario.TButton", background=AZUL, foreground="white",
                        borderwidth=0, font=(FUENTE, 10, "bold"), padding=(16, 9))
        estilo.map("Primario.TButton", background=[("active", "#155A87")])
        estilo.configure("Transferir.TButton", background=AZUL_CLARO, foreground=AZUL,
                        borderwidth=0, font=(FUENTE, 9, "bold"), padding=(11, 7))
        estilo.map("Transferir.TButton", background=[("active", "#D7EAF8")])

    def _crear_encabezado(self):
        encabezado = tk.Frame(self, bg=AZUL_OSCURO, height=108)
        encabezado.pack(fill="x")
        encabezado.pack_propagate(False)
        titulo = tk.Frame(encabezado, bg=AZUL_OSCURO)
        titulo.pack(side="left", padx=30, pady=22)
        tk.Label(titulo, text="RSA", bg=AZUL_OSCURO, fg="white",
                 font=(FUENTE, 25, "bold")).pack(anchor="w")
        tk.Label(titulo, text="Cifrado de texto · Matemática Discreta 1",
                 bg=AZUL_OSCURO, fg="#C9D9E8", font=(FUENTE, 10)).pack(anchor="w")
        tk.Label(encabezado, text="ASCII 32–126   ·   bloques de 2 caracteres",
                 bg="#1A4569", fg="#EAF3FA", font=(FUENTE, 9, "bold"),
                 padx=14, pady=7).pack(side="right", padx=30)

    @staticmethod
    def _texto(parent, alto, solo_lectura=False):
        texto = tk.Text(
            parent, height=alto, wrap="word", font=MONO, bg="#FBFDFF", fg=TEXTO,
            insertbackground=AZUL_OSCURO, relief="solid", borderwidth=1,
            highlightthickness=1, highlightbackground=BORDE,
            padx=10, pady=8,
        )
        if solo_lectura:
            texto.configure(state="disabled", bg="#F8FAFC")
        return texto

    @staticmethod
    def _escribir(texto, valor):
        estado = str(texto.cget("state"))
        texto.configure(state="normal")
        texto.delete("1.0", "end")
        texto.insert("1.0", valor)
        texto.configure(state=estado)

    @classmethod
    def _limpiar(cls, texto):
        cls._escribir(texto, "")

    @staticmethod
    def _tarjeta(parent, titulo, subtitulo):
        tarjeta = tk.Frame(parent, bg=TARJETA, highlightthickness=1,
                           highlightbackground=BORDE, padx=18, pady=16)
        tk.Label(tarjeta, text=titulo, bg=TARJETA, fg=AZUL_OSCURO,
                 font=(FUENTE, 12, "bold")).pack(anchor="w")
        tk.Label(tarjeta, text=subtitulo, bg=TARJETA, fg=SECUNDARIO,
                 font=(FUENTE, 9), wraplength=430, justify="left").pack(
            anchor="w", pady=(2, 14)
        )
        return tarjeta

    @staticmethod
    def _campo(parent, etiqueta, variable):
        fila = tk.Frame(parent, bg=TARJETA)
        fila.pack(fill="x", pady=4)
        tk.Label(fila, text=etiqueta, bg=TARJETA, fg=TEXTO,
                 font=(FUENTE, 10, "bold"), width=5, anchor="w").pack(side="left")
        entrada = ttk.Entry(fila, textvariable=variable, width=24,
                            font=(FUENTE, 10))
        entrada.pack(side="left", fill="x", expand=True, padx=(5, 0))
        return entrada

    def _parametros(self, parent):
        bloque = tk.Frame(parent, bg=TARJETA)
        tk.Label(bloque, text="Parámetros RSA", bg=TARJETA, fg=AZUL_OSCURO,
                 font=(FUENTE, 10, "bold")).pack(anchor="w", pady=(10, 3))
        tk.Label(bloque, text="p y q deben ser primos distintos.", bg=TARJETA,
                 fg=SECUNDARIO, font=(FUENTE, 9)).pack(anchor="w", pady=(0, 5))
        variables = {
            "p": tk.StringVar(value="367"),
            "q": tk.StringVar(value="373"),
            "e": tk.StringVar(value="17"),
        }
        self._campo(bloque, "p", variables["p"])
        self._campo(bloque, "q", variables["q"])
        self._campo(bloque, "e", variables["e"])
        return bloque, variables

    def _crear_pestana_cifrar(self):
        pagina = self.pestana_cifrar
        pagina.columnconfigure(0, weight=1)
        pagina.rowconfigure(2, weight=1)
        self._titulo_pagina(
            pagina, "Encriptar mensaje", "Convierte el texto en bloques RSA de seis dígitos."
        )
        columnas = tk.Frame(pagina, bg=FONDO)
        columnas.grid(row=1, column=0, sticky="nsew", pady=(18, 14))
        columnas.columnconfigure(0, weight=1)
        columnas.columnconfigure(1, weight=1)

        entrada = self._tarjeta(columnas, "1. Datos de entrada",
                                "El mensaje conserva mayúsculas, signos y espacios.")
        entrada.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        tk.Label(entrada, text="Mensaje M", bg=TARJETA, fg=TEXTO,
                 font=(FUENTE, 10, "bold")).pack(anchor="w")
        self.mensaje_cifrar = self._texto(entrada, 6)
        self.mensaje_cifrar.pack(fill="x", pady=(5, 4))
        tk.Label(entrada, text="No se admiten tildes, ñ, tabulaciones ni saltos de línea.",
                 bg=TARJETA, fg=SECUNDARIO, font=(FUENTE, 9)).pack(anchor="w")
        parametros, self.vars_cifrar = self._parametros(entrada)
        parametros.pack(fill="x")
        ttk.Button(entrada, text="Encriptar mensaje", style="Primario.TButton",
                   command=self._encriptar).pack(anchor="w", pady=(16, 0))

        salida = self._tarjeta(columnas, "2. Resultado",
                               "Guarda C y L; ambos se necesitan para desencriptar.")
        salida.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        tk.Label(salida, text="Cifrado C", bg=TARJETA, fg=TEXTO,
                 font=(FUENTE, 10, "bold")).pack(anchor="w")
        self.cifrado_salida = self._texto(salida, 6, solo_lectura=True)
        self.cifrado_salida.pack(fill="x", pady=(5, 10))
        self.resumen_cifrar = tk.StringVar(value="Completa los datos y presiona Encriptar.")
        ttk.Label(salida, textvariable=self.resumen_cifrar,
                  style="Estado.TLabel", wraplength=420).pack(anchor="w")
        ttk.Button(salida, text="→ Enviar C y L a Desencriptar",
                   style="Transferir.TButton",
                   command=self._pasar_a_descifrar).pack(anchor="w", pady=(18, 0))

        self.detalle_cifrar = self._crear_detalle(pagina, 2)

    def _crear_pestana_descifrar(self):
        pagina = self.pestana_descifrar
        pagina.columnconfigure(0, weight=1)
        pagina.rowconfigure(2, weight=1)
        self._titulo_pagina(
            pagina, "Desencriptar mensaje", "Recupera el texto original con C, L y los parámetros RSA."
        )
        columnas = tk.Frame(pagina, bg=FONDO)
        columnas.grid(row=1, column=0, sticky="nsew", pady=(18, 14))
        columnas.columnconfigure(0, weight=1)
        columnas.columnconfigure(1, weight=1)

        entrada = self._tarjeta(columnas, "1. Datos de entrada",
                                "C usa bloques de seis dígitos separados por un solo espacio.")
        entrada.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        tk.Label(entrada, text="Cifrado C", bg=TARJETA, fg=TEXTO,
                 font=(FUENTE, 10, "bold")).pack(anchor="w")
        self.cifrado_entrada = self._texto(entrada, 5)
        self.cifrado_entrada.pack(fill="x", pady=(5, 10))
        fila_l = tk.Frame(entrada, bg=TARJETA)
        fila_l.pack(anchor="w")
        tk.Label(fila_l, text="Longitud original L", bg=TARJETA, fg=TEXTO,
                 font=(FUENTE, 10, "bold")).pack(side="left")
        self.longitud_descifrar = tk.StringVar()
        ttk.Entry(fila_l, textvariable=self.longitud_descifrar, width=10,
                  font=(FUENTE, 10)).pack(side="left", padx=(10, 0))
        parametros, self.vars_descifrar = self._parametros(entrada)
        parametros.pack(fill="x")
        ttk.Button(entrada, text="Desencriptar mensaje", style="Primario.TButton",
                   command=self._desencriptar).pack(anchor="w", pady=(16, 0))

        salida = self._tarjeta(columnas, "2. Mensaje recuperado",
                               "El resultado conserva todos los espacios originales.")
        salida.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        tk.Label(salida, text="Mensaje M", bg=TARJETA, fg=TEXTO,
                 font=(FUENTE, 10, "bold")).pack(anchor="w")
        self.mensaje_salida = self._texto(salida, 5, solo_lectura=True)
        self.mensaje_salida.pack(fill="x", pady=(5, 10))
        self.resumen_descifrar = tk.StringVar(value="Completa los datos y presiona Desencriptar.")
        ttk.Label(salida, textvariable=self.resumen_descifrar,
                  style="Estado.TLabel", wraplength=420).pack(anchor="w")

        self.detalle_descifrar = self._crear_detalle(pagina, 2)

    @staticmethod
    def _titulo_pagina(parent, titulo, subtitulo):
        cabecera = tk.Frame(parent, bg=FONDO)
        cabecera.grid(row=0, column=0, sticky="w")
        ttk.Label(cabecera, text=titulo, style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(cabecera, text=subtitulo, style="Subtitulo.TLabel").pack(
            anchor="w", pady=(2, 0)
        )

    def _crear_detalle(self, parent, fila):
        tarjeta = self._tarjeta(
            parent, "Detalle del proceso",
            "Valores calculados y relación entre cada pareja de caracteres, m y c."
        )
        tarjeta.grid(row=fila, column=0, sticky="nsew")
        parent.rowconfigure(fila, weight=1)
        contenedor = tk.Frame(tarjeta, bg=TARJETA)
        contenedor.pack(fill="both", expand=True)
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(0, weight=1)
        detalle = self._texto(contenedor, 11, solo_lectura=True)
        detalle.configure(wrap="none")
        vertical = ttk.Scrollbar(contenedor, orient="vertical", command=detalle.yview)
        horizontal = ttk.Scrollbar(contenedor, orient="horizontal", command=detalle.xview)
        detalle.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        detalle.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        return detalle

    @staticmethod
    def _detalle(resultado, e, d=None):
        relleno = "Sí; se añadió o retiró un espacio final." if resultado.hubo_relleno else "No."
        lineas = [
            f"LLAVE PÚBLICA: (e, n) = ({e}, {resultado.n})",
            f"n = {resultado.n}     φ = {resultado.phi}     L = {resultado.L}     "
            f"bloques = {resultado.k}",
            f"Relleno: {relleno}",
        ]
        if d is not None:
            lineas.append(f"EXPONENTE PRIVADO: d = {d}")
        lineas.extend([
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

    def _encriptar(self):
        self._limpiar(self.cifrado_salida)
        self._limpiar(self.detalle_cifrar)
        try:
            resultado = encriptar(
                self.mensaje_cifrar.get("1.0", "end-1c"),
                self.vars_cifrar["p"].get(), self.vars_cifrar["q"].get(),
                self.vars_cifrar["e"].get(),
            )
        except (ErrorValidacion, TypeError) as error:
            self.resumen_cifrar.set(f"Error: {error}")
            messagebox.showerror("Datos inválidos", str(error), parent=self)
            return
        self._escribir(self.cifrado_salida, resultado.C)
        self._escribir(self.detalle_cifrar, self._detalle(resultado, resultado.llave_publica[0]))
        self.resumen_cifrar.set(
            f"Listo · L = {resultado.L} · llave pública = {resultado.llave_publica} · "
            f"relleno: {'sí' if resultado.hubo_relleno else 'no'}"
        )
        self.ultimo_cifrado = resultado

    def _pasar_a_descifrar(self):
        if not hasattr(self, "ultimo_cifrado"):
            messagebox.showinfo("Sin resultado", "Primero realiza una encriptación válida.", parent=self)
            return
        resultado = self.ultimo_cifrado
        self._escribir(self.cifrado_entrada, resultado.C)
        self.longitud_descifrar.set(str(resultado.L))
        for nombre in self.vars_descifrar:
            self.vars_descifrar[nombre].set(self.vars_cifrar[nombre].get())
        self.libro.select(self.pestana_descifrar)

    def _desencriptar(self):
        self._limpiar(self.mensaje_salida)
        self._limpiar(self.detalle_descifrar)
        try:
            resultado = desencriptar(
                self.cifrado_entrada.get("1.0", "end-1c"), self.longitud_descifrar.get(),
                self.vars_descifrar["p"].get(), self.vars_descifrar["q"].get(),
                self.vars_descifrar["e"].get(),
            )
        except (ErrorValidacion, TypeError) as error:
            self.resumen_descifrar.set(f"Error: {error}")
            messagebox.showerror("Datos inválidos", str(error), parent=self)
            return
        self._escribir(self.mensaje_salida, resultado.mensaje)
        self._escribir(
            self.detalle_descifrar,
            self._detalle(resultado, self.vars_descifrar["e"].get(), resultado.d),
        )
        self.resumen_descifrar.set(
            f"Listo · d = {resultado.d} · L = {resultado.L} · "
            f"relleno retirado: {'sí' if resultado.hubo_relleno else 'no'}"
        )


if __name__ == "__main__":
    AplicacionRSA().mainloop()
