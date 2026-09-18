# ============================================================
# INTERFAZ - GESTIÓN DE ARCHIVOS
# ============================================================
#
# Este módulo contiene todo lo relacionado con la sección
# "Seleccionar archivos" de la interfaz.
#
# Responsabilidades:
#
#     - Crear la sección de archivos.
#     - Crear las filas de selección.
#     - Seleccionar archivo de entrada.
#     - Seleccionar archivo Excel de salida.
#     - Seleccionar archivo CSV de salida.
#     - Mostrar las rutas seleccionadas.
#     - Mantener las referencias a las rutas seleccionadas.
#
# ============================================================


from pathlib import Path

from tkinter import filedialog

import customtkinter as ctk


# ============================================================
# IMPORTACIÓN DE ESTILOS
# ============================================================

from estilos.colores import (
    BLANCO,
    AZUL_OSCURO,
    BORDE
)

from estilos.fuentes import (
    FUENTE_SECCION,
    FUENTE_SUBTITULO,
    FUENTE_NORMAL_NEGRITA
)


# ============================================================
# IMPORTACIÓN DE COMPONENTES VISUALES
# ============================================================

from plantillas.botones import (
    crear_boton_buscar
)

from plantillas.entradas import (
    crear_entrada_ruta
)


# ============================================================
# CLASE GESTORA DE ARCHIVOS
# ============================================================

class GestorArchivos:
    """
    Gestiona la sección de selección de archivos de la
    aplicación.

    Esta clase centraliza:

        - La interfaz visual de archivos.
        - La selección del archivo de entrada.
        - La selección del archivo Excel de salida.
        - La selección del archivo CSV de salida.
        - Las rutas seleccionadas.

    La clase no ejecuta ningún proceso de depuración.
    Su única responsabilidad es manejar los archivos y
    sus rutas dentro de la interfaz.
    """


    # ========================================================
    # CONSTRUCTOR
    # ========================================================

    def __init__(
        self,
        parent,
        row=1
    ):
        """
        Inicializa el gestor de archivos.

        Parámetros
        ----------
        parent:
            Contenedor principal donde se construirá la
            sección de archivos.

        row:
            Fila de la cuadrícula donde se colocará la
            sección de archivos.
        """

        self.parent = parent

        self.row = row


        # ----------------------------------------------------
        # RUTAS DE LOS ARCHIVOS
        # ----------------------------------------------------

        self.archivo_origen = None

        self.ruta_excel = None

        self.ruta_csv = None


        # ----------------------------------------------------
        # REFERENCIAS A LOS CAMPOS DE RUTA
        # ----------------------------------------------------
        #
        # Se guardan las referencias a los CTkEntry para
        # poder actualizar su contenido posteriormente.
        #

        self.entrada_base = None

        self.entrada_excel = None

        self.entrada_csv = None


        # ----------------------------------------------------
        # FRAME PRINCIPAL DE LA SECCIÓN
        # ----------------------------------------------------

        self.frame_seccion = None


        # ----------------------------------------------------
        # CREAR LA SECCIÓN
        # ----------------------------------------------------
        #
        # Al crear el gestor también construimos
        # automáticamente su sección visual.
        #

        self.crear_seccion_archivos(
            row=self.row
        )


    # ========================================================
    # CREAR SECCIÓN DE ARCHIVOS
    # ========================================================

    def crear_seccion_archivos(
        self,
        row=1
    ):
        """
        Crea la tarjeta completa de selección de archivos.

        La sección contiene:

            1. Archivo de entrada.
            2. Archivo Excel de salida.
            3. Archivo CSV de salida.

        Parámetros
        ----------
        row:
            Fila de la cuadrícula donde se colocará la
            sección.

        Retorna
        -------
        CTkFrame
            Frame principal de la sección.
        """

        # ----------------------------------------------------
        # TARJETA PRINCIPAL
        # ----------------------------------------------------

        self.frame_seccion = ctk.CTkFrame(
            self.parent,
            fg_color=BLANCO,
            corner_radius=12
        )

        self.frame_seccion.grid(
            row=row,
            column=0,
            sticky="ew",
            padx=25,
            pady=(15, 8)
        )


        # ----------------------------------------------------
        # CONFIGURACIÓN DE COLUMNAS
        # ----------------------------------------------------
        #
        # La columna 1 contiene los campos de ruta y debe
        # ocupar todo el espacio disponible.
        #

        self.frame_seccion.grid_columnconfigure(
            1,
            weight=1
        )


        # ----------------------------------------------------
        # TÍTULO
        # ----------------------------------------------------

        label_titulo = ctk.CTkLabel(
            self.frame_seccion,
            text="▣  Seleccionar archivos",
            font=FUENTE_SECCION,
            text_color=AZUL_OSCURO
        )

        label_titulo.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="w",
            padx=20,
            pady=(15, 2)
        )


        # ----------------------------------------------------
        # DESCRIPCIÓN
        # ----------------------------------------------------

        label_descripcion = ctk.CTkLabel(
            self.frame_seccion,
            text=(
                "Selecciona la base de entrada y las rutas "
                "de salida para Excel y CSV."
            ),
            font=FUENTE_SUBTITULO,
            text_color="#64748B"
        )

        label_descripcion.grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="w",
            padx=20,
            pady=(0, 12)
        )


        # ----------------------------------------------------
        # FILA 1 - BASE DE ENTRADA
        # ----------------------------------------------------

        self.entrada_base = self.crear_fila_archivo(
            parent=self.frame_seccion,
            fila=2,
            texto="Archivo de entrada (Base):",
            tipo="base"
        )


        # ----------------------------------------------------
        # FILA 2 - EXCEL DE SALIDA
        # ----------------------------------------------------

        self.entrada_excel = self.crear_fila_archivo(
            parent=self.frame_seccion,
            fila=3,
            texto="Archivo Excel de salida:",
            tipo="excel"
        )


        # ----------------------------------------------------
        # FILA 3 - CSV DE SALIDA
        # ----------------------------------------------------

        self.entrada_csv = self.crear_fila_archivo(
            parent=self.frame_seccion,
            fila=4,
            texto="Archivo CSV de salida:",
            tipo="csv"
        )


        return self.frame_seccion


    # ========================================================
    # CREAR FILA DE ARCHIVO
    # ========================================================

    def crear_fila_archivo(
        self,
        parent,
        fila,
        texto,
        tipo
    ):
        """
        Crea una fila completa para seleccionar un archivo.

        Cada fila contiene:

            - Etiqueta descriptiva.
            - Campo donde aparece la ruta.
            - Botón Buscar.

        Parámetros
        ----------
        parent:
            Contenedor de la fila.

        fila:
            Número de fila dentro del grid.

        texto:
            Texto de la etiqueta.

        tipo:
            Tipo de archivo:

                "base"
                "excel"
                "csv"

        Retorna
        -------
        CTkEntry
            Campo donde se mostrará la ruta.
        """

        # ----------------------------------------------------
        # ETIQUETA
        # ----------------------------------------------------

        label = ctk.CTkLabel(
            parent,
            text=texto,
            width=205,
            anchor="w",
            font=FUENTE_NORMAL_NEGRITA,
            text_color=AZUL_OSCURO
        )

        label.grid(
            row=fila,
            column=0,
            sticky="w",
            padx=(20, 10),
            pady=5
        )


        # ----------------------------------------------------
        # CAMPO DE RUTA
        # ----------------------------------------------------

        entrada = crear_entrada_ruta(
            parent
        )

        entrada.grid(
            row=fila,
            column=1,
            sticky="ew",
            padx=5,
            pady=5
        )


        # ----------------------------------------------------
        # BOTÓN BUSCAR
        # ----------------------------------------------------

        boton = crear_boton_buscar(
            parent,
            command=lambda: self.seleccionar_archivo(
                tipo
            )
        )

        boton.grid(
            row=fila,
            column=2,
            padx=(10, 20),
            pady=5
        )


        return entrada


    # ========================================================
    # SELECCIONAR ARCHIVO
    # ========================================================

    def seleccionar_archivo(
        self,
        tipo
    ):
        """
        Abre el diálogo correspondiente para seleccionar
        un archivo.

        Parámetros
        ----------
        tipo:
            Puede ser:

                "base"
                "excel"
                "csv"
        """

        # ====================================================
        # ARCHIVO DE ENTRADA
        # ====================================================

        if tipo == "base":

            archivo = filedialog.askopenfilename(
                title="Seleccionar base de entrada",
                filetypes=[
                    (
                        "Archivos Excel y CSV",
                        "*.xlsx *.xls *.csv"
                    )
                ]
            )


            # ------------------------------------------------
            # Si el usuario canceló
            # ------------------------------------------------

            if not archivo:
                return


            # ------------------------------------------------
            # Guardar ruta
            # ------------------------------------------------

            self.archivo_origen = Path(
                archivo
            )


            # ------------------------------------------------
            # Mostrar ruta
            # ------------------------------------------------

            self.colocar_ruta(
                self.entrada_base,
                self.archivo_origen
            )


        # ====================================================
        # ARCHIVO EXCEL DE SALIDA
        # ====================================================

        elif tipo == "excel":

            archivo = filedialog.asksaveasfilename(
                title="Guardar archivo Excel",
                defaultextension=".xlsx",
                filetypes=[
                    (
                        "Archivo Excel",
                        "*.xlsx"
                    )
                ]
            )


            # ------------------------------------------------
            # Si el usuario canceló
            # ------------------------------------------------

            if not archivo:
                return


            # ------------------------------------------------
            # Guardar ruta
            # ------------------------------------------------

            self.ruta_excel = Path(
                archivo
            )


            # ------------------------------------------------
            # Mostrar ruta
            # ------------------------------------------------

            self.colocar_ruta(
                self.entrada_excel,
                self.ruta_excel
            )


        # ====================================================
        # ARCHIVO CSV DE SALIDA
        # ====================================================

        elif tipo == "csv":

            archivo = filedialog.asksaveasfilename(
                title="Guardar archivo CSV",
                defaultextension=".csv",
                filetypes=[
                    (
                        "Archivo CSV",
                        "*.csv"
                    )
                ]
            )


            # ------------------------------------------------
            # Si el usuario canceló
            # ------------------------------------------------

            if not archivo:
                return


            # ------------------------------------------------
            # Guardar ruta
            # ------------------------------------------------

            self.ruta_csv = Path(
                archivo
            )


            # ------------------------------------------------
            # Mostrar ruta
            # ------------------------------------------------

            self.colocar_ruta(
                self.entrada_csv,
                self.ruta_csv
            )


    # ========================================================
    # COLOCAR RUTA EN EL CAMPO
    # ========================================================

    def colocar_ruta(
        self,
        entrada,
        ruta
    ):
        """
        Coloca una ruta dentro de un CTkEntry.

        Antes de insertar la nueva ruta se elimina cualquier
        contenido anterior.

        Parámetros
        ----------
        entrada:
            CTkEntry donde se mostrará la ruta.

        ruta:
            Ruta del archivo seleccionada.
        """

        entrada.delete(
            0,
            "end"
        )

        entrada.insert(
            0,
            str(ruta)
        )


    # ========================================================
    # OBTENER RUTAS
    # ========================================================

    def obtener_rutas(self):
        """
        Retorna las tres rutas seleccionadas.

        Retorna
        -------
        tuple
            (
                archivo_origen,
                ruta_excel,
                ruta_csv
            )
        """

        return (
            self.archivo_origen,
            self.ruta_excel,
            self.ruta_csv
        )


    # ========================================================
    # VALIDAR RUTAS
    # ========================================================

    def rutas_completas(self):
        """
        Verifica si el usuario ha seleccionado los tres
        archivos necesarios.

        Retorna
        -------
        bool
            True si las tres rutas existen.
            False si falta alguna.
        """

        return (
            self.archivo_origen is not None
            and self.ruta_excel is not None
            and self.ruta_csv is not None
        )