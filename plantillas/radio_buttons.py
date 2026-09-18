# ============================================================
# PLANTILLAS - RADIO BUTTONS
# ============================================================
#
# Componentes relacionados con opciones de selección única.
#
# ============================================================

import customtkinter as ctk

from estilos.colores import (
    AZUL,
    AZUL_HOVER,
    AZUL_OSCURO
)

from estilos.fuentes import FUENTE_PEQUENA


# ============================================================
# CREAR RADIO BUTTON
# ============================================================

def crear_radio_button(
    parent,
    text,
    variable,
    value,
    command
):
    """
    Crea un RadioButton con el estilo estándar de la
    aplicación.
    """

    radio = ctk.CTkRadioButton(
        parent,
        text=text,
        variable=variable,
        value=value,
        command=command,
        font=FUENTE_PEQUENA,
        text_color=AZUL_OSCURO,
        fg_color=AZUL,
        hover_color=AZUL_HOVER
    )


    return radio