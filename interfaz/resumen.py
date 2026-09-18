# ============================================================
# INTERFAZ - RESUMEN DE RESULTADOS
# ============================================================
#
# Este módulo contiene todo lo relacionado con la sección
# "Resumen de resultados" de la interfaz.
#
# Responsabilidades:
#
#     - Crear la sección de resumen.
#     - Crear las tarjetas estadísticas.
#     - Actualizar el total de registros.
#     - Actualizar los registros en montaje.
#     - Actualizar los registros en rechazos.
#     - Actualizar el estado de los archivos generados.
#     - Mostrar el último mensaje del proceso.
#     - Reiniciar el resumen.
#
# ============================================================


import customtkinter as ctk


# ============================================================
# IMPORTACIÓN DE COLORES
# ============================================================

from estilos.colores import (
    AZUL,
    AZUL_CLARO,
    AZUL_OSCURO,
    VERDE,
    VERDE_CLARO,
    ROJO,
    ROJO_CLARO,
    MORADO,
    MORADO_CLARO,
    FONDO_ULTIMO_MENSAJE
)


# ============================================================
# IMPORTACIÓN DE FUENTES
# ============================================================

from estilos.fuentes import (
    FUENTE_SECCION,
    FUENTE_PEQUENA_NEGRITA,
    FUENTE_NORMAL
)


# ============================================================
# IMPORTACIÓN DE PLANTILLAS
# ============================================================

from plantillas.tarjetas import (
    crear_tarjeta_estadistica
)


# ============================================================
# CLASE GESTORA DEL RESUMEN
# ============================================================

class GestorResumen:
    """
    Gestiona la sección de resumen de resultados.

    Esta clase centraliza los elementos visuales que muestran
    las estadísticas del proceso de depuración.

    Las estadísticas mostradas son:

        - Total de registros.
        - Registros en montaje.
        - Registros en rechazos.
        - Archivos generados.

    También administra el mensaje informativo mostrado
    debajo de las tarjetas.
    """


    # ========================================================
    # CONSTRUCTOR
    # ========================================================

    def __init__(
        self,
        parent,
        row=3
    ):
        """
        Inicializa el gestor del resumen.

        Parámetros
        ----------
        parent:
            Contenedor principal donde se construirá la
            sección de resumen.

        row:
            Fila de la cuadrícula donde se colocará la
            sección de resumen.
        """

        self.parent = parent

        self.row = row


        # ----------------------------------------------------
        # FRAME PRINCIPAL
        # ----------------------------------------------------

        self.frame_seccion = None


        # ----------------------------------------------------
        # REFERENCIAS A LAS TARJETAS
        # ----------------------------------------------------
        #
        # Cada variable almacenará el CTkLabel que contiene
        # el valor de la estadística correspondiente.
        #

        self.valor_total = None

        self.valor_montaje = None

        self.valor_rechazos = None

        self.valor_archivos = None


        # ----------------------------------------------------
        # REFERENCIAS AL ÚLTIMO MENSAJE
        # ----------------------------------------------------

        self.label_ultimo_mensaje = None

        self.label_ultimo_mensaje_texto = None


        # ----------------------------------------------------
        # CREAR AUTOMÁTICAMENTE LA SECCIÓN
        # ----------------------------------------------------
        #
        # Al igual que GestorArchivos y GestorProceso,
        # el gestor se encarga de construir su propia sección
        # al momento de ser creado.
        #

        self.crear_seccion_resumen(
            row=self.row
        )


    # ========================================================
    # CREAR SECCIÓN DE RESUMEN
    # ========================================================

    def crear_seccion_resumen(self, row=3):
        """
        Crea la tarjeta completa del resumen de resultados.

        La sección contiene:

            1. Total de registros.
            2. Registros en montaje.
            3. Registros en rechazos.
            4. Archivos generados.
            5. Último mensaje.

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
            fg_color="#FFFFFF",
            corner_radius=12
        )

        self.frame_seccion.grid(
            row=row,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(8, 15)
        )


        # ----------------------------------------------------
        # TÍTULO
        # ----------------------------------------------------

        label_titulo = ctk.CTkLabel(
            self.frame_seccion,
            text="▣  Resumen de resultados",
            font=FUENTE_SECCION,
            text_color=AZUL_OSCURO
        )

        label_titulo.pack(
            anchor="w",
            padx=20,
            pady=(15, 12)
        )


        # ----------------------------------------------------
        # CONTENEDOR DE TARJETAS
        # ----------------------------------------------------

        frame_tarjetas = ctk.CTkFrame(
            self.frame_seccion,
            fg_color="transparent"
        )

        frame_tarjetas.pack(
            fill="x",
            padx=16
        )


        # ====================================================
        # TARJETA - TOTAL DE REGISTROS
        # ====================================================

        self.valor_total = crear_tarjeta_estadistica(
            frame_tarjetas,
            "Total registros",
            "0",
            AZUL_CLARO,
            AZUL
        )


        # ====================================================
        # TARJETA - REGISTROS EN MONTAJE
        # ====================================================

        self.valor_montaje = crear_tarjeta_estadistica(
            frame_tarjetas,
            "Registros en montaje",
            "0",
            VERDE_CLARO,
            VERDE
        )


        # ====================================================
        # TARJETA - REGISTROS EN RECHAZOS
        # ====================================================

        self.valor_rechazos = crear_tarjeta_estadistica(
            frame_tarjetas,
            "Registros en rechazos",
            "0",
            ROJO_CLARO,
            ROJO
        )


        # ====================================================
        # TARJETA - ARCHIVOS GENERADOS
        # ====================================================

        self.valor_archivos = crear_tarjeta_estadistica(
            frame_tarjetas,
            "Archivos generados",
            "Excel ○   CSV ○",
            MORADO_CLARO,
            MORADO
        )


        # ====================================================
        # ÚLTIMO MENSAJE
        # ====================================================

        self.crear_ultimo_mensaje()


        return self.frame_seccion


    # ========================================================
    # CREAR ÚLTIMO MENSAJE
    # ========================================================

    def crear_ultimo_mensaje(self):
        """
        Crea el bloque visual donde se muestra el último
        mensaje enviado por el proceso.
        """

        # ----------------------------------------------------
        # CONTENEDOR DEL MENSAJE
        # ----------------------------------------------------

        frame_mensaje = ctk.CTkFrame(
            self.frame_seccion,
            fg_color=FONDO_ULTIMO_MENSAJE,
            corner_radius=8
        )

        frame_mensaje.pack(
            fill="x",
            padx=20,
            pady=(12, 15)
        )


        # ----------------------------------------------------
        # TÍTULO DEL MENSAJE
        # ----------------------------------------------------

        self.label_ultimo_mensaje = ctk.CTkLabel(
            frame_mensaje,
            text="ⓘ  Último mensaje",
            font=FUENTE_PEQUENA_NEGRITA,
            text_color=AZUL
        )

        self.label_ultimo_mensaje.pack(
            anchor="w",
            padx=14,
            pady=(8, 1)
        )


        # ----------------------------------------------------
        # TEXTO DEL MENSAJE
        # ----------------------------------------------------

        self.label_ultimo_mensaje_texto = ctk.CTkLabel(
            frame_mensaje,
            text="Esperando inicio del proceso...",
            font=FUENTE_NORMAL,
            text_color=AZUL_OSCURO,
            anchor="w",
            justify="left"
        )

        self.label_ultimo_mensaje_texto.pack(
            fill="x",
            padx=14,
            pady=(0, 8)
        )


    # ========================================================
    # ACTUALIZAR ESTADÍSTICAS
    # ========================================================

    def actualizar_estadisticas(
        self,
        total=None,
        montaje=None,
        rechazos=None
    ):
        """
        Actualiza las estadísticas mostradas en las tarjetas.

        Parámetros
        ----------
        total:
            Cantidad total de registros.

        montaje:
            Cantidad de registros actualmente en Montaje.

        rechazos:
            Cantidad de registros actualmente en Rechazos.

        Los parámetros son opcionales para permitir actualizar
        únicamente una estadística cuando sea necesario.
        """

        # ----------------------------------------------------
        # TOTAL
        # ----------------------------------------------------

        if total is not None:

            self.valor_total.configure(
                text=str(total)
            )


        # ----------------------------------------------------
        # MONTAJE
        # ----------------------------------------------------

        if montaje is not None:

            self.valor_montaje.configure(
                text=str(montaje)
            )


        # ----------------------------------------------------
        # RECHAZOS
        # ----------------------------------------------------

        if rechazos is not None:

            self.valor_rechazos.configure(
                text=str(rechazos)
            )


    # ========================================================
    # ACTUALIZAR DESDE ESTADÍSTICAS DEL PROCESO
    # ========================================================

    def actualizar_desde_estadisticas(
        self,
        estadisticas
    ):
        """
        Actualiza las tarjetas utilizando el diccionario de
        estadísticas enviado por el proceso de depuración.

        Se espera un diccionario con las claves:

            total
            montaje
            rechazos

        Ejemplo:

            {
                "total": 1000,
                "montaje": 850,
                "rechazos": 150
            }
        """

        if not estadisticas:
            return


        self.actualizar_estadisticas(
            total=estadisticas.get(
                "total"
            ),
            montaje=estadisticas.get(
                "montaje"
            ),
            rechazos=estadisticas.get(
                "rechazos"
            )
        )


    # ========================================================
    # ACTUALIZAR ARCHIVOS GENERADOS
    # ========================================================

    def actualizar_archivos(
        self,
        excel=False,
        csv=False
    ):
        """
        Actualiza la tarjeta "Archivos generados".

        Parámetros
        ----------
        excel:
            True si el archivo Excel ya fue generado.

        csv:
            True si el archivo CSV ya fue generado.

        Ejemplo:

            excel=False
            csv=False

                Excel ○   CSV ○

            excel=True
            csv=False

                Excel ✓   CSV ○

            excel=True
            csv=True

                Excel ✓   CSV ✓
        """

        estado_excel = (
            "✓"
            if excel
            else "○"
        )

        estado_csv = (
            "✓"
            if csv
            else "○"
        )


        self.valor_archivos.configure(
            text=(
                f"Excel {estado_excel}   "
                f"CSV {estado_csv}"
            )
        )


    # ========================================================
    # ACTUALIZAR MENSAJE
    # ========================================================

    def actualizar_mensaje(
        self,
        mensaje
    ):
        """
        Actualiza el texto mostrado como último mensaje.

        Parámetros
        ----------
        mensaje:
            Mensaje que se desea mostrar.
        """

        if self.label_ultimo_mensaje_texto is None:
            return


        self.label_ultimo_mensaje_texto.configure(
            text=str(mensaje)
        )


    # ========================================================
    # ACTUALIZAR TÍTULO DEL MENSAJE
    # ========================================================

    def actualizar_titulo_mensaje(
        self,
        texto="ⓘ  Último mensaje"
    ):
        """
        Permite modificar el título del bloque de mensajes.

        Por defecto conserva el título utilizado actualmente
        por la aplicación.
        """

        if self.label_ultimo_mensaje is None:
            return


        self.label_ultimo_mensaje.configure(
            text=texto
        )


    # ========================================================
    # REINICIAR RESUMEN
    # ========================================================

    def reiniciar_resumen(self):
        """
        Devuelve el resumen a su estado inicial.

        Estado inicial:

            Total registros: 0

            Registros en montaje: 0

            Registros en rechazos: 0

            Archivos generados:
                Excel ○   CSV ○

            Último mensaje:
                Esperando inicio del proceso...
        """

        # ----------------------------------------------------
        # REINICIAR TOTAL
        # ----------------------------------------------------

        if self.valor_total is not None:

            self.valor_total.configure(
                text="0"
            )


        # ----------------------------------------------------
        # REINICIAR MONTAJE
        # ----------------------------------------------------

        if self.valor_montaje is not None:

            self.valor_montaje.configure(
                text="0"
            )


        # ----------------------------------------------------
        # REINICIAR RECHAZOS
        # ----------------------------------------------------

        if self.valor_rechazos is not None:

            self.valor_rechazos.configure(
                text="0"
            )


        # ----------------------------------------------------
        # REINICIAR ARCHIVOS
        # ----------------------------------------------------

        if self.valor_archivos is not None:

            self.valor_archivos.configure(
                text="Excel ○   CSV ○"
            )


        # ----------------------------------------------------
        # REINICIAR MENSAJE
        # ----------------------------------------------------

        self.actualizar_titulo_mensaje()

        self.actualizar_mensaje(
            "Esperando inicio del proceso..."
        )


    # ========================================================
    # MARCAR ARCHIVOS COMO GENERADOS
    # ========================================================

    def proceso_completado(
        self,
        total=None,
        montaje=None,
        rechazos=None
    ):
        """
        Actualiza el resumen cuando el proceso termina
        correctamente.

        Los dos archivos de salida se marcan como generados.
        """

        # ----------------------------------------------------
        # ACTUALIZAR ESTADÍSTICAS
        # ----------------------------------------------------

        self.actualizar_estadisticas(
            total=total,
            montaje=montaje,
            rechazos=rechazos
        )


        # ----------------------------------------------------
        # MARCAR ARCHIVOS
        # ----------------------------------------------------

        self.actualizar_archivos(
            excel=True,
            csv=True
        )


        # ----------------------------------------------------
        # MENSAJE FINAL
        # ----------------------------------------------------

        self.actualizar_titulo_mensaje(
            "✓  Proceso completado"
        )

        self.actualizar_mensaje(
            "La depuración terminó correctamente."
        )


    # ========================================================
    # MOSTRAR ERROR
    # ========================================================

    def proceso_error(
        self,
        mensaje
    ):
        """
        Actualiza el resumen cuando ocurre un error durante
        el proceso.
        """

        self.actualizar_titulo_mensaje(
            "⚠  Error durante el proceso"
        )

        self.actualizar_mensaje(
            str(mensaje)
        )