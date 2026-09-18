# ============================================================
# PLANTILLAS - ETAPAS DEL PROCESO
# ============================================================
#
# Componentes visuales utilizados para representar las
# diferentes etapas de la depuración.
#
# ============================================================

import customtkinter as ctk

from estilos.colores import (
    AZUL,
    BLANCO,
    GRIS,
    GRIS_TEXTO,
    VERDE
)

from estilos.fuentes import (
    FUENTE_ICONO_ETAPA,
    FUENTE_PEQUENA_NEGRITA
)

from estilos.dimensiones import (
    TAMANO_CIRCULO_ETAPA
)


# ============================================================
# CONFIGURACIÓN DE ETAPAS
# ============================================================

NOMBRES_ETAPAS = [
    "Cargar\ndatos",
    "Procesar\nteléfonos",
    "Validar\nrepresentantes",
    "Cruces\n(DOT)",
    "Limpieza",
    "Generar\narchivos",
    "Completado"
]


SIMBOLOS_ETAPAS = [
    "▤",
    "☎",
    "●",
    "↗",
    "✦",
    "▣",
    "✓"
]


# ============================================================
# CREAR UNA ETAPA
# ============================================================

def crear_etapa(
    parent,
    nombre,
    simbolo
):
    """
    Crea visualmente una etapa del proceso.

    Retorna un diccionario con las referencias a los
    elementos gráficos para poder actualizarlos posteriormente.
    """

    # --------------------------------------------------------
    # CONTENEDOR
    # --------------------------------------------------------

    frame = ctk.CTkFrame(
        parent,
        fg_color="transparent"
    )


    frame.pack(
        side="left",
        fill="x",
        expand=True
    )


    # --------------------------------------------------------
    # CÍRCULO
    # --------------------------------------------------------

    circulo = ctk.CTkLabel(
        frame,
        text=simbolo,
        width=TAMANO_CIRCULO_ETAPA,
        height=TAMANO_CIRCULO_ETAPA,
        corner_radius=23,
        fg_color=GRIS,
        text_color=GRIS_TEXTO,
        font=FUENTE_ICONO_ETAPA
    )


    circulo.pack()


    # --------------------------------------------------------
    # NOMBRE
    # --------------------------------------------------------

    label_nombre = ctk.CTkLabel(
        frame,
        text=nombre,
        font=FUENTE_PEQUENA_NEGRITA,
        text_color=GRIS_TEXTO,
        justify="center"
    )


    label_nombre.pack(
        pady=(4, 0)
    )


    # --------------------------------------------------------
    # RETORNAR REFERENCIAS
    # --------------------------------------------------------

    return {
        "frame": frame,
        "circulo": circulo,
        "nombre": label_nombre
    }


# ============================================================
# CREAR TODAS LAS ETAPAS
# ============================================================

def crear_etapas(
    parent
):
    """
    Crea las siete etapas del proceso.

    Retorna
    -------
    list
        Lista con las referencias de cada etapa.
    """

    etapas = []


    for nombre, simbolo in zip(
        NOMBRES_ETAPAS,
        SIMBOLOS_ETAPAS
    ):

        etapa = crear_etapa(
            parent,
            nombre,
            simbolo
        )


        etapas.append(
            etapa
        )


    return etapas


# ============================================================
# ACTUALIZAR ESTADO DE UNA ETAPA
# ============================================================

def actualizar_etapa(
    etapa,
    estado
):
    """
    Actualiza visualmente una etapa.

    Parámetros
    ----------
    etapa:
        Diccionario retornado por crear_etapa().

    estado:
        Puede ser:

            "pendiente"
            "actual"
            "completada"
    """

    if estado == "completada":

        etapa["circulo"].configure(
            fg_color=VERDE,
            text_color=BLANCO
        )


        etapa["nombre"].configure(
            text_color=VERDE
        )


    elif estado == "actual":

        etapa["circulo"].configure(
            fg_color=AZUL,
            text_color=BLANCO
        )


        etapa["nombre"].configure(
            text_color=AZUL
        )


    else:

        etapa["circulo"].configure(
            fg_color=GRIS,
            text_color=GRIS_TEXTO
        )


        etapa["nombre"].configure(
            text_color=GRIS_TEXTO
        )


# ============================================================
# ACTUALIZAR TODAS LAS ETAPAS
# ============================================================

def actualizar_etapas(
    etapas,
    etapa_actual
):
    """
    Actualiza todas las etapas según la etapa actual.

    Ejemplo:

        etapa_actual = 3

    Resultado:

        1 → completada
        2 → completada
        3 → actual
        4 → pendiente
        5 → pendiente
        6 → pendiente
        7 → pendiente
    """

    for indice, etapa in enumerate(
        etapas
    ):

        numero = indice + 1


        if numero < etapa_actual:

            actualizar_etapa(
                etapa,
                "completada"
            )


        elif numero == etapa_actual:

            actualizar_etapa(
                etapa,
                "actual"
            )


        else:

            actualizar_etapa(
                etapa,
                "pendiente"
            )


# ============================================================
# MARCAR TODAS COMO COMPLETADAS
# ============================================================

def completar_etapas(
    etapas
):
    """
    Marca todas las etapas como completadas.
    """

    for etapa in etapas:

        actualizar_etapa(
            etapa,
            "completada"
        )


# ============================================================
# REINICIAR TODAS LAS ETAPAS
# ============================================================

def reiniciar_etapas(
    etapas
):
    """
    Devuelve todas las etapas al estado pendiente.
    """

    for etapa in etapas:

        actualizar_etapa(
            etapa,
            "pendiente"
        )