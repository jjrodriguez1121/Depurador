# ============================================================
# PLANTILLAS - BOTONES
# ============================================================
#
# Componentes reutilizables relacionados con botones.
#
# ============================================================

import customtkinter as ctk

from estilos.colores import (
    AZUL,
    AZUL_HOVER,
    AZUL_OSCURO,
    BLANCO,
    VERDE,
    VERDE_HOVER,
    AZUL_SIDEBAR_HOVER,
    AZUL_SIDEBAR_BORDE
)

from estilos.fuentes import (
    FUENTE_BOTON,
    FUENTE_BOTON_PEQUENA
)

from estilos.dimensiones import (
    ALTO_BOTON_PRINCIPAL,
    ALTO_BOTON_BUSCAR,
    ALTO_BOTON_SALIR
)


# ============================================================
# BOTÓN PRINCIPAL
# ============================================================

def crear_boton_principal(
    parent,
    text,
    command
):
    """
    Crea el botón principal utilizado para iniciar
    la depuración.
    """

    boton = ctk.CTkButton(
        parent,
        text=text,
        width=225,
        height=ALTO_BOTON_PRINCIPAL,
        corner_radius=8,
        fg_color=VERDE,
        hover_color=VERDE_HOVER,
        font=FUENTE_BOTON,
        command=command
    )


    return boton


# ============================================================
# BOTÓN BUSCAR
# ============================================================

def crear_boton_buscar(
    parent,
    command
):
    """
    Crea el botón utilizado para seleccionar archivos.
    """

    boton = ctk.CTkButton(
        parent,
        text="📁  Buscar",
        width=105,
        height=ALTO_BOTON_BUSCAR,
        corner_radius=7,
        fg_color=AZUL_OSCURO,
        hover_color=AZUL_HOVER,
        font=FUENTE_BOTON_PEQUENA,
        command=command
    )


    return boton


# ============================================================
# BOTÓN SALIR
# ============================================================

def crear_boton_salir(
    parent,
    command
):
    """
    Crea el botón Salir del sidebar.
    """

    boton = ctk.CTkButton(
        parent,
        text="↪  Salir",
        height=ALTO_BOTON_SALIR,
        corner_radius=7,
        fg_color=AZUL_OSCURO,
        hover_color=AZUL_SIDEBAR_HOVER,
        border_width=1,
        border_color=AZUL_SIDEBAR_BORDE,
        text_color=BLANCO,
        font=FUENTE_BOTON,
        command=command
    )


    return boton