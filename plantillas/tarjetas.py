# ============================================================
# PLANTILLAS - TARJETAS
# ============================================================
#
# Componentes visuales relacionados con tarjetas estadísticas.
#
# ============================================================

import customtkinter as ctk

from estilos.colores import AZUL_OSCURO

from estilos.fuentes import (
    FUENTE_PEQUENA_NEGRITA
)


# ============================================================
# CREAR TARJETA ESTADÍSTICA
# ============================================================

def crear_tarjeta_estadistica(
    parent,
    titulo,
    valor,
    fondo,
    color
):
    """
    Crea una tarjeta estadística reutilizable.

    Parámetros
    ----------
    parent:
        Contenedor donde se colocará la tarjeta.

    titulo:
        Texto descriptivo de la estadística.

    valor:
        Valor que se mostrará inicialmente.

    fondo:
        Color de fondo de la tarjeta.

    color:
        Color utilizado para el título.

    Retorna
    -------
    CTkLabel
        Label que contiene el valor de la tarjeta.

    """

    # --------------------------------------------------------
    # TARJETA
    # --------------------------------------------------------

    tarjeta = ctk.CTkFrame(
        parent,
        fg_color=fondo,
        corner_radius=9
    )


    tarjeta.pack(
        side="left",
        fill="both",
        expand=True,
        padx=4
    )


    # --------------------------------------------------------
    # TÍTULO
    # --------------------------------------------------------

    label_titulo = ctk.CTkLabel(
        tarjeta,
        text=titulo,
        font=FUENTE_PEQUENA_NEGRITA,
        text_color=color
    )


    label_titulo.pack(
        pady=(11, 2)
    )


    # --------------------------------------------------------
    # VALOR
    # --------------------------------------------------------

    label_valor = ctk.CTkLabel(
        tarjeta,
        text=valor,
        font=(
            "Segoe UI",
            19,
            "bold"
        ),
        text_color=AZUL_OSCURO
    )


    label_valor.pack(
        pady=(0, 11)
    )


    # --------------------------------------------------------
    # RETORNAR LABEL DEL VALOR
    # ----------------------------------------------------
    #
    # La interfaz necesita conservar esta referencia para
    # poder actualizar posteriormente el número mostrado.
    #
    # Ejemplo:
    #
    #     self.total_card.configure(text="1500")
    #
    # --------------------------------------------------------

    return label_valor