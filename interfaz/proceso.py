# ============================================================
# INTERFAZ - PROCESO DE DEPURACIÓN
# ============================================================
#
# Este módulo contiene todo lo relacionado con la ejecución
# visual y funcional del proceso de depuración.
#
# Responsabilidades:
#
#     - Crear la sección "Proceso de depuración".
#     - Mostrar las siete etapas.
#     - Mostrar el criterio de coincidencias.
#     - Permitir seleccionar 1 o 2 coincidencias.
#     - Mostrar el progreso.
#     - Mostrar el porcentaje.
#     - Iniciar la depuración.
#     - Ejecutar la depuración en segundo plano.
#     - Recibir el progreso enviado por depurador.py.
#     - Actualizar visualmente las etapas.
#     - Reiniciar el progreso.
#     - Mostrar finalización.
#     - Manejar errores.
#
# Este módulo NO se encarga de:
#
#     - Seleccionar archivos.
#     - Mostrar las estadísticas del resumen.
#     - Procesar directamente los datos.
#
# Para seleccionar archivos utiliza un callback que será
# proporcionado posteriormente por GestorArchivos.
#
# Para actualizar el resumen utiliza otro callback que será
# proporcionado posteriormente por GestorResumen.
#
# ============================================================


import threading

from tkinter import IntVar

import customtkinter as ctk


# ============================================================
# IMPORTACIÓN DEL PROCESO PRINCIPAL
# ============================================================

from depurador import (
    ejecutar_depuracion
)

from depuracion.carga_datos import DepuracionCancelada
from interfaz.confirmacion import (
    confirmar_columnas_faltantes, solicitar_confirmacion,
    mostrar_advertencia, mostrar_error, mostrar_exito,
)


# ============================================================
# IMPORTACIÓN DE COLORES
# ============================================================

from estilos.colores import (
    AZUL,
    AZUL_CLARO,
    AZUL_OSCURO,
    VERDE,
    VERDE_HOVER,
    VERDE_CLARO,
    BLANCO,
    GRIS,
    GRIS_TEXTO,
    ROJO,
    ROJO_CLARO
)


# ============================================================
# IMPORTACIÓN DE FUENTES
# ============================================================

from estilos.fuentes import (
    FUENTE_SECCION,
    FUENTE_SUBTITULO,
    FUENTE_NORMAL_NEGRITA,
    FUENTE_ICONO_ETAPA
)


# ============================================================
# IMPORTACIÓN DE DIMENSIONES
# ============================================================

from estilos.dimensiones import (
    ALTO_ESTADO_PROCESO,
    ALTO_BOTON_PRINCIPAL
)


# ============================================================
# IMPORTACIÓN DE PLANTILLAS
# ============================================================

from plantillas.botones import (
    crear_boton_principal
)

from plantillas.radio_buttons import (
    crear_radio_button
)

from plantillas.etapas import (
    crear_etapas,
    actualizar_etapas,
    completar_etapas,
    reiniciar_etapas
)


# ============================================================
# CLASE GESTORA DEL PROCESO
# ============================================================

class GestorProceso:
    """
    Gestiona la sección visual y funcional del proceso de
    depuración.

    Esta clase se encarga de:

        - Mostrar las etapas.
        - Mostrar el progreso.
        - Seleccionar el criterio de coincidencias.
        - Iniciar la depuración.
        - Ejecutar la depuración en segundo plano.
        - Recibir actualizaciones.
        - Mostrar errores.
        - Mostrar la finalización.

    La clase utiliza callbacks para comunicarse con otros
    componentes de la interfaz.

    Esto permite que el módulo permanezca independiente de
    GestorArchivos y GestorResumen.
    """


    # ========================================================
    # CONSTRUCTOR
    # ========================================================

    def __init__(
        self,
        parent,
        obtener_rutas,
        callback_resumen=None,
        callback_estado=None
    ):
        """
        Inicializa el gestor del proceso.

        Parámetros
        ----------
        parent:
            Contenedor donde se construirá la sección.

        obtener_rutas:
            Función que debe retornar:

                (
                    archivo_origen,
                    ruta_excel,
                    ruta_csv,
                    archivo_data,
                    archivo_filtros
                )

        callback_resumen:
            Función opcional que recibirá:

                base
                montaje
                rechazos

            cuando el proceso termine correctamente.

        callback_estado:
            Función opcional utilizada para actualizar el
            estado inferior de la aplicación.
        """

        self.parent = parent

        self.obtener_rutas = obtener_rutas

        self.callback_resumen = callback_resumen

        self.callback_estado = callback_estado


        # ====================================================
        # ESTADO DEL PROCESO
        # ====================================================

        self.proceso_en_ejecucion = False

        self.etapa_actual = 0


        # ====================================================
        # ESTADÍSTICAS
        # ====================================================

        self.total_registros = 0

        self.registros_montaje = 0

        self.registros_rechazos = 0


        # ====================================================
        # CRITERIO DE COINCIDENCIAS
        # ====================================================
        #
        # El valor predeterminado es 1 para conservar el
        # comportamiento actual de la aplicación.
        #

        self.minimo_coincidencias_var = IntVar(
            value=1
        )

        self.minimo_coincidencias = 1


        # ====================================================
        # REFERENCIAS VISUALES
        # ====================================================

        self.card_proceso = None

        self.frame_etapas = None

        self.frame_criterio = None

        self.frame_estado_proceso = None

        self.label_progreso = None

        self.label_porcentaje = None

        self.barra_progreso = None

        self.boton_iniciar = None

        self.etapas = []


        # ====================================================
        # CREAR SECCIÓN
        # ====================================================

        self.crear_seccion_proceso()


    # ========================================================
    # CREAR SECCIÓN DEL PROCESO
    # ========================================================

    def crear_seccion_proceso(self, row=2):
        """
        Crea visualmente la sección completa del proceso.

        La sección contiene:

            - Título.
            - Descripción.
            - Selector de coincidencias.
            - Siete etapas.
            - Mensaje de progreso.
            - Porcentaje.
            - Barra de progreso.
            - Botón de inicio.
        """

        # ----------------------------------------------------
        # TARJETA PRINCIPAL
        # ----------------------------------------------------

        self.card_proceso = ctk.CTkFrame(
            self.parent,
            fg_color=BLANCO,
            corner_radius=12
        )

        self.card_proceso.grid(
            row=row,
            column=0,
            sticky="ew",
            padx=25,
            pady=8
        )


        # ----------------------------------------------------
        # TÍTULO
        # ----------------------------------------------------

        titulo = ctk.CTkLabel(
            self.card_proceso,
            text="⚙  Proceso de depuración",
            font=FUENTE_SECCION,
            text_color=AZUL_OSCURO
        )

        titulo.pack(
            anchor="w",
            padx=22,
            pady=(15, 1)
        )


        # ----------------------------------------------------
        # DESCRIPCIÓN
        # ----------------------------------------------------

        descripcion = ctk.CTkLabel(
            self.card_proceso,
            text=(
                "El proceso se ejecuta por etapas. "
                "Puedes visualizar el progreso en tiempo real."
            ),
            font=FUENTE_SUBTITULO,
            text_color=GRIS_TEXTO
        )

        descripcion.pack(
            anchor="w",
            padx=22
        )


        # ====================================================
        # CRITERIO DE COINCIDENCIAS
        # ====================================================

        self.crear_criterio_coincidencias()


        # ====================================================
        # CONTENEDOR DE ETAPAS
        # ====================================================

        self.frame_etapas = ctk.CTkFrame(
            self.card_proceso,
            fg_color="transparent"
        )

        self.frame_etapas.pack(
            fill="x",
            padx=20,
            pady=(8, 4)
        )


        # ----------------------------------------------------
        # CREAR LAS SIETE ETAPAS
        # ----------------------------------------------------

        self.etapas = crear_etapas(
            self.frame_etapas
        )


        # ====================================================
        # ESTADO / MENSAJE DE PROGRESO
        # ====================================================

        self.frame_estado_proceso = ctk.CTkFrame(
            self.card_proceso,
            fg_color=AZUL_CLARO,
            corner_radius=8,
            height=ALTO_ESTADO_PROCESO
        )

        self.frame_estado_proceso.pack(
            fill="x",
            padx=22,
            pady=(8, 10)
        )

        self.frame_estado_proceso.pack_propagate(
            False
        )


        # ----------------------------------------------------
        # MENSAJE
        # ----------------------------------------------------

        self.label_progreso = ctk.CTkLabel(
            self.frame_estado_proceso,
            text="  Listo para iniciar.",
            font=FUENTE_NORMAL_NEGRITA,
            text_color=AZUL,
            anchor="w"
        )

        self.label_progreso.pack(
            side="left",
            fill="both",
            expand=True,
            padx=8
        )


        # ----------------------------------------------------
        # PORCENTAJE
        # ----------------------------------------------------

        self.label_porcentaje = ctk.CTkLabel(
            self.frame_estado_proceso,
            text="0%",
            width=50,
            font=FUENTE_NORMAL_NEGRITA,
            text_color=AZUL
        )

        self.label_porcentaje.pack(
            side="right"
        )


        # ====================================================
        # BARRA DE PROGRESO
        # ====================================================

        self.barra_progreso = ctk.CTkProgressBar(
            self.card_proceso,
            height=7,
            corner_radius=4,
            fg_color=GRIS,
            progress_color=VERDE
        )

        self.barra_progreso.pack(
            fill="x",
            padx=22,
            pady=(0, 8)
        )

        self.barra_progreso.set(
            0
        )


        # ====================================================
        # BOTÓN INICIAR
        # ====================================================

        self.boton_iniciar = crear_boton_principal(
            self.card_proceso,
            "▶  Iniciar depuración",
            self.iniciar_depuracion
        )

        self.boton_iniciar.pack(
            pady=(3, 15)
        )


    # ========================================================
    # CREAR CRITERIO DE COINCIDENCIAS
    # ========================================================

    def crear_criterio_coincidencias(self):
        """
        Crea el selector que permite elegir cuántas palabras
        del representante deben coincidir con la base de
        nombres latinos.

        Opciones:

            - Al menos 1 coincidencia.
            - Al menos 2 coincidencias.

        El valor predeterminado es 1.
        """

        # ----------------------------------------------------
        # CONTENEDOR
        # ----------------------------------------------------

        self.frame_criterio = ctk.CTkFrame(
            self.card_proceso,
            fg_color="transparent"
        )

        self.frame_criterio.pack(
            fill="x",
            padx=22,
            pady=(8, 4)
        )


        # ----------------------------------------------------
        # TEXTO
        # ----------------------------------------------------

        label_criterio = ctk.CTkLabel(
            self.frame_criterio,
            text="Criterio de validación:",
            font=FUENTE_NORMAL_NEGRITA,
            text_color=AZUL_OSCURO
        )

        label_criterio.pack(
            side="left",
            padx=(0, 15)
        )


        # ----------------------------------------------------
        # RADIO - 1 COINCIDENCIA
        # ----------------------------------------------------

        radio_una = crear_radio_button(
            self.frame_criterio,
            "Al menos 1 coincidencia",
            self.minimo_coincidencias_var,
            1,
            self.actualizar_criterio_coincidencias
        )

        radio_una.pack(
            side="left",
            padx=(0, 20)
        )


        # ----------------------------------------------------
        # RADIO - 2 COINCIDENCIAS
        # ----------------------------------------------------

        radio_dos = crear_radio_button(
            self.frame_criterio,
            "Al menos 2 coincidencias",
            self.minimo_coincidencias_var,
            2,
            self.actualizar_criterio_coincidencias
        )

        radio_dos.pack(
            side="left"
        )


    # ========================================================
    # ACTUALIZAR CRITERIO DE COINCIDENCIAS
    # ========================================================

    def actualizar_criterio_coincidencias(self):
        """
        Actualiza el número mínimo de coincidencias elegido
        por el usuario.

        Valores permitidos:

            1
            2
        """

        valor = self.minimo_coincidencias_var.get()


        # ----------------------------------------------------
        # VALIDAR VALOR
        # ----------------------------------------------------

        if valor not in (1, 2):

            valor = 1

            self.minimo_coincidencias_var.set(
                1
            )


        # ----------------------------------------------------
        # GUARDAR VALOR
        # ----------------------------------------------------

        self.minimo_coincidencias = valor


    # ========================================================
    # OBTENER CRITERIO
    # ========================================================

    def obtener_minimo_coincidencias(self):
        """
        Retorna el número mínimo de coincidencias seleccionado.

        Retorna
        -------
        int
            1 o 2.
        """

        return self.minimo_coincidencias


    # ========================================================
    # INICIAR DEPURACIÓN
    # ========================================================

    def iniciar_depuracion(self):
        """
        Valida las rutas y solicita confirmación antes de
        iniciar el proceso.

        La depuración se ejecuta en un hilo separado para
        evitar que la interfaz gráfica se congele.
        """

        # ----------------------------------------------------
        # EVITAR DOBLE EJECUCIÓN
        # ----------------------------------------------------

        if self.proceso_en_ejecucion:

            return


        # ====================================================
        # OBTENER RUTAS
        # ====================================================

        (
            archivo_origen,
            ruta_excel,
            ruta_csv,
            archivo_data,
            archivo_filtros
        ) = self.obtener_rutas()


        # ====================================================
        # VALIDAR BASE
        # ====================================================

        if not archivo_origen:

            mostrar_advertencia(
                self.parent,
                "Archivo faltante",
                "Selecciona la base de entrada."
            )

            return


        # ====================================================
        # VALIDAR EXCEL
        # ====================================================

        if not ruta_excel:

            mostrar_advertencia(
                self.parent,
                "Ruta faltante",
                "Selecciona dónde guardar el archivo Excel."
            )

            return


        # ====================================================
        # VALIDAR CSV
        # ====================================================

        if not ruta_csv:

            mostrar_advertencia(
                self.parent,
                "Ruta faltante",
                "Selecciona dónde guardar el archivo CSV."
            )

            return


        # ====================================================
        # CONFIRMACIÓN
        # ====================================================

        if not archivo_data or not archivo_filtros:
            faltantes = []
            if not archivo_data:
                faltantes.append("data (cruce de DOT)")
            if not archivo_filtros:
                faltantes.append("FILTROS ESPAÑOL (catálogo de nombres)")
            mostrar_advertencia(
                self.parent, "Archivos auxiliares faltantes",
                "Selecciona los siguientes archivos antes de iniciar:\n\n"
                + "\n".join(f"• {nombre}" for nombre in faltantes),
            )
            return

        confirmar = solicitar_confirmacion(
            self.parent,
            "Iniciar depuración",
            (
                "¿Deseas iniciar el proceso de depuración?\n\n"
                "La aplicación puede tardar varios minutos "
                "dependiendo del tamaño de la base."
            )
        )


        if not confirmar:

            return


        # ====================================================
        # ACTUALIZAR CRITERIO
        # ====================================================

        self.rutas_ejecucion = (
            archivo_origen, ruta_excel, ruta_csv, archivo_data, archivo_filtros
        )
        self.actualizar_criterio_coincidencias()


        # ====================================================
        # REINICIAR INTERFAZ
        # ====================================================

        self.reiniciar_progreso()


        # ====================================================
        # MARCAR COMO ACTIVO
        # ====================================================

        self.proceso_en_ejecucion = True


        # ====================================================
        # DESHABILITAR BOTÓN
        # ====================================================

        self.boton_iniciar.configure(
            state="disabled",
            text="Procesando..."
        )


        # ====================================================
        # ACTUALIZAR ESTADO EXTERIOR
        # ====================================================

        self.actualizar_estado_exterior(
            "●  Proceso en ejecución. Por favor, espera...",
            AZUL_CLARO,
            AZUL
        )


        # ====================================================
        # CREAR HILO
        # ====================================================

        hilo = threading.Thread(
            target=self.ejecutar_proceso,
            daemon=True
        )

        hilo.start()


    # ========================================================
    # EJECUTAR PROCESO
    # ========================================================

    def ejecutar_proceso(self):
        """
        Ejecuta el proceso real de depuración.

        Este método se ejecuta dentro de un hilo separado.

        La función ejecutar_depuracion() es la responsable
        del procesamiento de los datos.
        """

        try:

            # ------------------------------------------------
            # OBTENER RUTAS
            # ------------------------------------------------

            (
                archivo_origen,
                ruta_excel,
                ruta_csv,
                archivo_data,
                archivo_filtros
            ) = self.rutas_ejecucion


            # ------------------------------------------------
            # EJECUTAR DEPURACIÓN
            # ------------------------------------------------
            #
            # Se envía el nuevo criterio de coincidencias.
            #
            # El valor predeterminado es 1.
            #

            resultado = ejecutar_depuracion(
                archivo_origen,
                ruta_excel,
                ruta_csv,
                minimo_coincidencias=self.minimo_coincidencias,
                callback=self.recibir_progreso,
                confirmar_columnas_faltantes=self.confirmar_columnas_faltantes,
                archivo_data=archivo_data,
                archivo_filtros=archivo_filtros
            )


            # ------------------------------------------------
            # RESULTADO
            # ------------------------------------------------

            base, montaje, rechazos = resultado


            # ------------------------------------------------
            # ACTUALIZAR INTERFAZ
            # ------------------------------------------------
            #
            # La interfaz gráfica debe actualizarse en el
            # hilo principal.
            #
            # Por eso utilizamos after(0, ...).
            #

            self.parent.after(
                0,
                lambda: self.proceso_completado(
                    base,
                    montaje,
                    rechazos
                )
            )


        except DepuracionCancelada:
            self.parent.after(0, self.proceso_cancelado)

        except Exception as error:

    # ------------------------------------------------
    # MOSTRAR ERROR EN HILO PRINCIPAL
    # ------------------------------------------------
    #
    # Se utiliza error=error para conservar el error
    # actual dentro del lambda.
    #
    # Esto es necesario porque after() ejecuta el lambda
    # posteriormente, cuando el bloque except ya terminó.
    #

            self.parent.after(
                0,
                lambda error=error: self.proceso_error(
                    error
                )
            )


    # ========================================================
    # RECIBIR PROGRESO
    # ========================================================

    def confirmar_columnas_faltantes(self, columnas):
        """Espera la decisión sin bloquear el hilo principal de la ventana."""
        respuesta_lista = threading.Event()
        resultado = {"continuar": False, "error": None}

        def preguntar():
            try:
                resultado["continuar"] = confirmar_columnas_faltantes(
                    self.parent, columnas
                )
            except Exception as error:
                resultado["error"] = error
            finally:
                respuesta_lista.set()

        self.parent.after(0, preguntar)
        respuesta_lista.wait()
        if resultado["error"] is not None:
            raise resultado["error"]
        return resultado["continuar"]

    def proceso_cancelado(self):
        """Restablece los controles sin presentar la cancelación como error."""
        self.reiniciar_progreso()
        self.proceso_en_ejecucion = False
        self.boton_iniciar.configure(
            state="normal", text="▶  Iniciar depuración"
        )
        mensaje = "Depuración cancelada. No se generaron archivos."
        self.label_progreso.configure(text=f"  {mensaje}")
        self.actualizar_estado_exterior(mensaje, AZUL_CLARO, AZUL)

    def recibir_progreso(
        self,
        etapa,
        mensaje,
        estadisticas
    ):
        """
        Recibe las actualizaciones enviadas por
        ejecutar_depuracion().

        Parámetros
        ----------
        etapa:
            Número de etapa actual.

        mensaje:
            Mensaje descriptivo de la etapa.

        estadisticas:
            Diccionario con:

                total
                montaje
                rechazos
        """

        # ----------------------------------------------------
        # ACTUALIZAR DESDE HILO PRINCIPAL
        # ----------------------------------------------------

        self.parent.after(
            0,
            lambda: self.actualizar_interfaz(
                etapa,
                mensaje,
                estadisticas
            )
        )


    # ========================================================
    # ACTUALIZAR INTERFAZ
    # ========================================================

    def actualizar_interfaz(
        self,
        etapa,
        mensaje,
        estadisticas
    ):
        """
        Actualiza todos los elementos visuales relacionados
        con el progreso.
        """

        # ====================================================
        # ETAPA ACTUAL
        # ====================================================

        self.etapa_actual = etapa


        # ====================================================
        # ESTADÍSTICAS
        # ====================================================

        if estadisticas is None:

            estadisticas = {}


        total = estadisticas.get(
            "total",
            0
        )

        montaje = estadisticas.get(
            "montaje",
            0
        )

        rechazos = estadisticas.get(
            "rechazos",
            0
        )


        # ----------------------------------------------------
        # GUARDAR ESTADÍSTICAS
        # ----------------------------------------------------

        self.total_registros = total

        self.registros_montaje = montaje

        self.registros_rechazos = rechazos


        # ====================================================
        # PROGRESO
        # ====================================================

        if etapa >= 7:

            progreso = 1

        else:

            progreso = etapa / 7


        self.barra_progreso.set(
            progreso
        )


        self.label_porcentaje.configure(
            text=f"{progreso * 100:.0f}%"
        )


        # ====================================================
        # ACTUALIZAR ETAPAS
        # ====================================================

        actualizar_etapas(
            self.etapas,
            etapa
        )


        # ====================================================
        # MENSAJE
        # ====================================================

        self.label_progreso.configure(
            text=f"  {mensaje}"
        )


        # ====================================================
        # ESTADO EXTERIOR
        # ====================================================

        self.actualizar_estado_exterior(
            f"●  {mensaje}",
            AZUL_CLARO,
            AZUL
        )


        # ====================================================
        # RESUMEN
        # ====================================================
        #
        # El resumen se actualiza mediante callback.
        #

        self.actualizar_resumen(
            total,
            montaje,
            rechazos
        )


    # ========================================================
    # ACTUALIZAR RESUMEN
    # ========================================================

    def actualizar_resumen(
        self,
        total,
        montaje,
        rechazos
    ):
        """
        Envía las estadísticas al gestor del resumen mediante
        el callback correspondiente.
        """

        if self.callback_resumen is None:

            return


        self.callback_resumen(
            total,
            montaje,
            rechazos
        )


    # ========================================================
    # ACTUALIZAR ESTADO EXTERIOR
    # ========================================================

    def actualizar_estado_exterior(
        self,
        texto,
        fondo,
        color
    ):
        """
        Envía información al estado inferior de la interfaz
        mediante un callback.

        Esto evita que GestorProceso tenga que conocer
        directamente el label de estado de ventana.py.
        """

        if self.callback_estado is None:

            return


        self.callback_estado(
            texto,
            fondo,
            color
        )


    # ========================================================
    # REINICIAR PROGRESO
    # ========================================================

    def reiniciar_progreso(self):
        """
        Devuelve todos los elementos visuales del proceso
        a su estado inicial.
        """

        # ====================================================
        # ETAPA
        # ====================================================

        self.etapa_actual = 0


        # ====================================================
        # ETAPAS
        # ====================================================

        reiniciar_etapas(
            self.etapas
        )


        # ====================================================
        # BARRA
        # ====================================================

        self.barra_progreso.set(
            0
        )


        # ====================================================
        # PORCENTAJE
        # ====================================================

        self.label_porcentaje.configure(
            text="0%"
        )


        # ====================================================
        # MENSAJE
        # ====================================================

        self.label_progreso.configure(
            text="  Iniciando proceso.",
            fg_color=AZUL_CLARO,
            text_color=AZUL
        )


        # ====================================================
        # ESTADÍSTICAS
        # ====================================================

        self.total_registros = 0

        self.registros_montaje = 0

        self.registros_rechazos = 0


        # ====================================================
        # RESUMEN
        # ====================================================

        self.actualizar_resumen(
            0,
            0,
            0
        )


        # ====================================================
        # ESTADO EXTERIOR
        # ====================================================

        self.actualizar_estado_exterior(
            "●  Iniciando proceso.",
            AZUL_CLARO,
            AZUL
        )


    # ========================================================
    # PROCESO COMPLETADO
    # ========================================================

    def proceso_completado(
        self,
        base,
        montaje,
        rechazos
    ):
        """
        Actualiza la interfaz cuando el proceso termina
        correctamente.
        """

        # ====================================================
        # MARCAR COMO FINALIZADO
        # ====================================================

        self.proceso_en_ejecucion = False


        # ====================================================
        # TODAS LAS ETAPAS VERDES
        # ====================================================

        completar_etapas(
            self.etapas
        )


        # ====================================================
        # BARRA 100%
        # ====================================================

        self.barra_progreso.set(
            1
        )

        self.label_porcentaje.configure(
            text="100%"
        )


        # ====================================================
        # ESTADÍSTICAS FINALES
        # ====================================================

        cantidad_base = len(
            base
        )

        cantidad_montaje = len(
            montaje
        )

        cantidad_rechazos = len(
            rechazos
        )


        # ----------------------------------------------------
        # GUARDAR ESTADÍSTICAS
        # ----------------------------------------------------

        self.total_registros = cantidad_base

        self.registros_montaje = cantidad_montaje

        self.registros_rechazos = cantidad_rechazos


        # ====================================================
        # ACTUALIZAR RESUMEN
        # ====================================================

        self.actualizar_resumen(
            cantidad_base,
            cantidad_montaje,
            cantidad_rechazos
        )


        # ====================================================
        # MENSAJE DE PROGRESO
        # ====================================================

        self.label_progreso.configure(
            text="  ✓ Proceso completado correctamente.",
            fg_color=VERDE_CLARO,
            text_color=VERDE
        )


        # ====================================================
        # ESTADO EXTERIOR
        # ====================================================

        self.actualizar_estado_exterior(
            "●  Depuración completada correctamente.",
            VERDE_CLARO,
            VERDE
        )


        # ====================================================
        # BOTÓN
        # ====================================================

        self.boton_iniciar.configure(
            state="normal",
            text="▶  Iniciar depuración"
        )


        # ====================================================
        # CALLBACK DE ARCHIVOS GENERADOS
        # ====================================================
        #
        # El resumen puede utilizar esta señal para marcar
        # Excel y CSV como generados.
        #
        # Para mantener el módulo desacoplado, se utiliza
        # el mismo callback del resumen enviando un cuarto
        # parámetro únicamente cuando el callback lo soporte.
        #

        self.notificar_archivos_generados()


        # ====================================================
        # MENSAJE FINAL
        # ====================================================

        (
            archivo_origen,
            ruta_excel,
            ruta_csv,
            archivo_data,
            archivo_filtros
        ) = self.rutas_ejecucion


        mostrar_exito(
            self.parent,
            "Proceso completado",
            (
                "La depuración terminó correctamente.\n\n"
                f"Registros originales: {cantidad_base:,}\n"
                f"Registros en montaje: {cantidad_montaje:,}\n"
                f"Registros rechazados: {cantidad_rechazos:,}\n\n"
                f"Excel:\n{ruta_excel}\n\n"
                f"CSV:\n{ruta_csv}\n\n"
                f"Data utilizado:\n{archivo_data}\n\n"
                f"Filtros utilizados:\n{archivo_filtros}"
            )
        )


    # ========================================================
    # NOTIFICAR ARCHIVOS GENERADOS
    # ========================================================

    def notificar_archivos_generados(self):
        """
        Notifica al callback del resumen que los archivos
        Excel y CSV fueron generados correctamente.

        El método intenta mantener compatibilidad con un
        callback sencillo de tres parámetros.
        """

        if self.callback_resumen is None:

            return


        try:

            self.callback_resumen(
                self.total_registros,
                self.registros_montaje,
                self.registros_rechazos,
                True,
                True
            )

        except TypeError:

            # ------------------------------------------------
            # COMPATIBILIDAD CON CALLBACK DE 3 PARÁMETROS
            # ------------------------------------------------

            self.callback_resumen(
                self.total_registros,
                self.registros_montaje,
                self.registros_rechazos
            )


    # ========================================================
    # PROCESO ERROR
    # ========================================================

    def proceso_error(
        self,
        error
    ):
        """
        Actualiza la interfaz cuando ocurre un error durante
        el proceso.
        """

        # ====================================================
        # MARCAR COMO FINALIZADO
        # ====================================================

        self.proceso_en_ejecucion = False


        # ====================================================
        # BOTÓN
        # ====================================================

        self.boton_iniciar.configure(
            state="normal",
            text="▶  Iniciar depuración"
        )


        # ====================================================
        # ESTADO EXTERIOR
        # ====================================================

        self.actualizar_estado_exterior(
            "●  Se produjo un error durante el proceso.",
            ROJO_CLARO,
            ROJO
        )


        # ====================================================
        # PROGRESO
        # ====================================================

        self.label_progreso.configure(
            text=f"  Error: {error}",
            fg_color=ROJO_CLARO,
            text_color=ROJO
        )


        # ====================================================
        # MENSAJE
        # ====================================================

        # El mensaje queda visible en la sección de proceso.


        # ====================================================
        # MOSTRAR ERROR
        # ====================================================

        mostrar_error(
            self.parent,
            "Error durante la depuración",
            str(error)
        )


    # ========================================================
    # OBTENER ESTADO DEL PROCESO
    # ========================================================

    def esta_en_ejecucion(self):
        """
        Indica si actualmente existe un proceso de depuración
        ejecutándose.

        Retorna
        -------
        bool
            True si está ejecutándose.
            False si no.
        """

        return self.proceso_en_ejecucion


    # ========================================================
    # OBTENER ESTADÍSTICAS
    # ========================================================

    def obtener_estadisticas(self):
        """
        Retorna las estadísticas actuales del proceso.

        Retorna
        -------
        tuple
            (
                total,
                montaje,
                rechazos
            )
        """

        return (
            self.total_registros,
            self.registros_montaje,
            self.registros_rechazos
        )
