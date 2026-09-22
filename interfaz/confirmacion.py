"""Mensajes y confirmaciones compartidos. Usar desde el hilo de la interfaz."""

import textwrap
import customtkinter as ctk

from estilos.colores import (
    AZUL, AZUL_HOVER, AZUL_OSCURO, AZUL_CLARO,
    BLANCO, BORDE, GRIS, GRIS_CLARO, GRIS_TEXTO,
    ROJO, ROJO_CLARO, VERDE, VERDE_CLARO,
)
from estilos.fuentes import FUENTE_BOTON, FUENTE_SECCION, FUENTE_SUBTITULO


def mostrar_mensaje(
    parent, titulo, mensaje, *, tipo="informacion", confirmar=False,
    texto_confirmar="Aceptar", subtitulo="", titulo_detalle="",
    titulo_ayuda="", ayuda="", nota="",
):
    """Muestra un diálogo modal; X/Escape nunca confirman una acción.

    El contenido largo es seleccionable y desplazable para poder leer y
    copiar rutas o errores completos. Todos los avisos comparten este diseño.
    """
    estilos = {
        "informacion": ("i", AZUL_CLARO, AZUL),
        "confirmacion": ("?", AZUL_CLARO, AZUL),
        "advertencia": ("!", "#FFF1D6", "#9A5B00"),
        "error": ("!", ROJO_CLARO, ROJO),
        "exito": ("✓", VERDE_CLARO, VERDE),
    }
    simbolo, fondo_icono, color_icono = estilos[tipo]
    ventana = ctk.CTkToplevel(parent)
    ventana.title(titulo)
    lineas = sum(max(1, len(textwrap.wrap(linea, 58))) for linea in str(mensaje).splitlines())
    alto_lista = 32 + 24 * min(max(lineas, 1), 8)
    ancho = 580
    alto = 244 + alto_lista + (100 if ayuda else 0) + (46 if nota else 0)
    ventana.geometry(f"{ancho}x{alto}")
    ventana.resizable(False, False)
    ventana.configure(fg_color=GRIS_CLARO)
    ventana.transient(parent.winfo_toplevel())
    continuar = False

    def responder(aceptar):
        nonlocal continuar
        continuar = aceptar
        ventana.destroy()

    try:
        encabezado = ctk.CTkFrame(ventana, fg_color="transparent")
        encabezado.pack(fill="x", padx=28, pady=(24, 18))
        ctk.CTkLabel(
            encabezado, text=simbolo, width=44, height=44,
            corner_radius=12, fg_color=fondo_icono, text_color=color_icono,
            font=("Segoe UI", 24, "bold")
        ).pack(side="left", padx=(0, 14))
        titulos = ctk.CTkFrame(encabezado, fg_color="transparent")
        titulos.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(
            titulos, text=titulo, wraplength=400, justify="left",
            font=FUENTE_SECCION, text_color=AZUL_OSCURO, anchor="w"
        ).pack(fill="x")
        if subtitulo:
            ctk.CTkLabel(
                titulos, text=subtitulo, font=FUENTE_SUBTITULO,
                text_color=GRIS_TEXTO, anchor="w", wraplength=400, justify="left"
            ).pack(fill="x")

        tarjeta = ctk.CTkFrame(
            ventana, fg_color=BLANCO, corner_radius=12,
            border_width=1, border_color=BORDE
        )
        tarjeta.pack(fill="x", padx=28)
        if titulo_detalle:
            ctk.CTkLabel(
                tarjeta, text=titulo_detalle, anchor="w",
                font=("Segoe UI", 11, "bold"), text_color=GRIS_TEXTO
            ).pack(fill="x", padx=18, pady=(12, 0))
        lista = ctk.CTkTextbox(
            tarjeta, height=alto_lista, fg_color=BLANCO,
            text_color=AZUL_OSCURO, font=("Segoe UI", 14),
            border_width=0, corner_radius=0, wrap="word",
            scrollbar_button_color=BORDE, scrollbar_button_hover_color=GRIS_TEXTO
        )
        lista.pack(fill="x", padx=14, pady=(10, 10))
        lista.insert("1.0", mensaje)
        lista.configure(state="disabled")

        if ayuda:
            informacion = ctk.CTkFrame(
                ventana, fg_color=AZUL_CLARO, corner_radius=10
            )
            informacion.pack(fill="x", padx=28, pady=(16, 0))
            ctk.CTkLabel(
                informacion, text=titulo_ayuda,
                font=("Segoe UI", 13, "bold"), text_color=AZUL_OSCURO,
                anchor="w"
            ).pack(fill="x", padx=16, pady=(10, 0))
            ctk.CTkLabel(
                informacion, text=ayuda, wraplength=480,
                font=FUENTE_SUBTITULO, text_color=AZUL_OSCURO,
                anchor="w", justify="left"
            ).pack(fill="x", padx=16, pady=(2, 12))

        pie = ctk.CTkFrame(ventana, fg_color="transparent")
        pie.pack(side="bottom", fill="x", padx=28, pady=(16, 22))
        if nota:
            ctk.CTkLabel(
                pie, text=nota, wraplength=510, justify="left",
                font=("Segoe UI", 12), text_color=GRIS_TEXTO, anchor="w"
            ).pack(fill="x", pady=(0, 10))
        botones = ctk.CTkFrame(pie, fg_color="transparent")
        botones.pack(fill="x")
        aceptar = ctk.CTkButton(
            botones, text=texto_confirmar, command=lambda: responder(True),
            width=150, height=40, corner_radius=8, font=FUENTE_BOTON,
            fg_color=AZUL, hover_color=AZUL_HOVER, text_color=BLANCO
        )
        aceptar.pack(side="right")
        foco = aceptar
        if confirmar:
            cancelar = ctk.CTkButton(
                botones, text="Cancelar", command=lambda: responder(False),
                width=120, height=40, corner_radius=8, font=FUENTE_BOTON,
                fg_color=BLANCO, hover_color=GRIS, text_color=AZUL_OSCURO,
                border_width=1, border_color=BORDE
            )
            cancelar.pack(side="right", padx=(0, 12))
            foco = cancelar

        ventana.protocol("WM_DELETE_WINDOW", lambda: responder(False))
        ventana.bind("<Escape>", lambda evento: responder(False))
        ventana.wait_visibility()
        ventana.grab_set()
        foco.focus_set()
        ventana.wait_window()
    finally:
        if ventana.winfo_exists():
            ventana.destroy()

    return continuar


def solicitar_confirmacion(parent, titulo, mensaje, texto_confirmar="Continuar"):
    return mostrar_mensaje(
        parent, titulo, mensaje, tipo="confirmacion", confirmar=True,
        texto_confirmar=texto_confirmar,
    )


def mostrar_advertencia(parent, titulo, mensaje):
    return mostrar_mensaje(parent, titulo, mensaje, tipo="advertencia")


def mostrar_error(parent, titulo, mensaje):
    return mostrar_mensaje(parent, titulo, mensaje, tipo="error")


def mostrar_exito(parent, titulo, mensaje):
    return mostrar_mensaje(parent, titulo, mensaje, tipo="exito")


def confirmar_columnas_faltantes(parent, columnas):
    cantidad = len(columnas)
    return mostrar_mensaje(
        parent, "Revisa las columnas de tu base",
        "\n".join(f"• {columna}" for columna in columnas),
        tipo="advertencia", confirmar=True, texto_confirmar="Continuar",
        subtitulo=(
            "Falta 1 columna necesaria para la depuración." if cantidad == 1
            else f"Faltan {cantidad} columnas necesarias para la depuración."
        ),
        titulo_detalle="COLUMNAS FALTANTES",
        titulo_ayuda="Puedes continuar con la base incompleta",
        ayuda=(
            "Las columnas faltantes se crearán vacías y se aplicarán\n"
            "las reglas actuales de depuración."
        ),
        nota="Si cancelas, no se generarán archivos de salida.",
    )
