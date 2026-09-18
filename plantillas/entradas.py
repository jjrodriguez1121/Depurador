# ============================================================
# PLANTILLAS - ENTRADAS
# ============================================================
#
# Componentes reutilizables relacionados con CTkEntry.
#
# ============================================================

import customtkinter as ctk

from estilos.colores import (
    AZUL_OSCURO,
    BORDE,
    FONDO_ENTRADA
)

from estilos.fuentes import FUENTE_NORMAL

from estilos.dimensiones import ALTO_ENTRADA


# ============================================================
# CREAR ENTRADA DE RUTA
# ============================================================

def crear_entrada_ruta(
    parent
):
    """
    Crea una entrada para mostrar la ruta de un archivo.
    """

    entrada = ctk.CTkEntry(
        parent,
        height=ALTO_ENTRADA,
        corner_radius=7,
        border_color=BORDE,
        fg_color=FONDO_ENTRADA,
        text_color=AZUL_OSCURO,
        font=FUENTE_NORMAL
    )


    return entrada