# ============================================================
# INTERFAZ - VENTANA PRINCIPAL
# ============================================================
#
# Este módulo contiene la ventana principal de la aplicación.
#
# Responsabilidades:
#
#     - Crear y configurar la ventana principal.
#     - Crear el sidebar.
#     - Crear el contenedor principal.
#     - Crear el encabezado.
#     - Crear el gestor de archivos.
#     - Crear el gestor del proceso.
#     - Crear el gestor del resumen.
#     - Crear el estado inferior.
#     - Coordinar la comunicación entre los gestores.
#     - Actualizar el ancho responsive del sidebar.
#     - Actualizar la imagen del sidebar.
#     - Controlar el cierre de la aplicación.
#
# Este módulo NO contiene la lógica de:
#
#     - selección de archivos;
#     - procesamiento de datos;
#     - validación de teléfonos;
#     - validación de representantes;
#     - cruces;
#     - limpieza;
#     - generación de Excel;
#     - generación de CSV.
#
# Esas responsabilidades pertenecen a otros módulos.
#
# ============================================================


from config import RUTA_ARCHIVOS
from interfaz.fondo_sidebar import componer_fondo

from interfaz.confirmacion import solicitar_confirmacion

import customtkinter as ctk

from PIL import (
    Image,
    ImageOps
)


# ============================================================
# IMPORTACIÓN DE GESTORES
# ============================================================

from interfaz.archivos import (
    GestorArchivos
)

from interfaz.proceso import (
    GestorProceso
)

from interfaz.resumen import (
    GestorResumen
)


# ============================================================
# IMPORTACIÓN DE COLORES
# ============================================================

from estilos.colores import (
    AZUL_OSCURO,
    AZUL,
    GRIS_TEXTO,
    GRIS_CLARO,
    BLANCO
)


# ============================================================
# IMPORTACIÓN DE FUENTES
# ============================================================

from estilos.fuentes import (
    FUENTE_NORMAL_NEGRITA,
    FUENTE_TITULO,
    FUENTE_SUBTITULO,
    FUENTE_PEQUENA_NEGRITA
)


# ============================================================
# IMPORTACIÓN DE DIMENSIONES
# ============================================================

from estilos.dimensiones import (
    ANCHO_INICIAL,
    ALTO_INICIAL,
    ANCHO_MINIMO,
    ALTO_MINIMO,
    ANCHO_SIDEBAR_MIN,
    ANCHO_SIDEBAR_MAX,
    ANCHO_SIDEBAR_INICIAL
)


# ============================================================
# IMPORTACIÓN DE BOTONES
# ============================================================

from plantillas.botones import (
    crear_boton_salir
)


# ============================================================
# CONFIGURACIÓN DE CUSTOMTKINTER
# ============================================================

ctk.set_appearance_mode(
    "light"
)

ctk.set_default_color_theme(
    "blue"
)


# ============================================================
# CLASE PRINCIPAL
# ============================================================

class Aplicacion(ctk.CTk):
    """
    Ventana principal de la aplicación.

    Esta clase funciona como coordinadora de los diferentes
    componentes de la interfaz.

    Componentes principales:

        GestorArchivos
        GestorProceso
        GestorResumen
    """


    # ========================================================
    # CONSTRUCTOR
    # ========================================================

    def __init__(self):

        super().__init__()


        # ====================================================
        # CONFIGURACIÓN DE VENTANA
        # ====================================================

        self.title(
            "Depurador de Bases - TRUCKING"
        )

        # Windows informa píxeles físicos; CTk.geometry usa unidades lógicas.
        escala = self._get_window_scaling()
        ancho_disponible = max(1, int((self.winfo_screenwidth() - 40) / escala))
        alto_disponible = max(1, int((self.winfo_screenheight() - 100) / escala))
        self.geometry(
            f"{min(ANCHO_INICIAL, ancho_disponible)}x{min(ALTO_INICIAL, alto_disponible)}"
        )
        self.minsize(
            min(ANCHO_MINIMO, ancho_disponible),
            min(ALTO_MINIMO, alto_disponible)
        )

        self.configure(
            fg_color=GRIS_CLARO
        )


        # ====================================================
        # CONFIGURACIÓN GRID PRINCIPAL
        # ====================================================

        self.grid_rowconfigure(
            0,
            weight=1
        )

        self.grid_columnconfigure(
            0,
            weight=0
        )

        self.grid_columnconfigure(
            1,
            weight=1
        )


        # ====================================================
        # VARIABLES DEL PROCESO
        # ====================================================

        self.proceso_en_ejecucion = False


        # ====================================================
        # REFERENCIAS DE IMAGEN
        # ====================================================

        self.imagen_sidebar_original = None

        self.imagen_sidebar_ctk = None


        # ====================================================
        # CREAR INTERFAZ
        # ====================================================

        self.crear_interfaz()


        # ====================================================
        # EVENTO RESPONSIVE
        # ====================================================

        self.bind(
            "<Configure>",
            self.actualizar_ancho_sidebar
        )


    # ========================================================
    # CREAR INTERFAZ
    # ========================================================

    def crear_interfaz(self):
        """
        Construye todos los componentes principales de la
        ventana.
        """

        # ----------------------------------------------------
        # SIDEBAR
        # ----------------------------------------------------

        self.crear_sidebar()


        # ----------------------------------------------------
        # CONTENEDOR PRINCIPAL
        # ----------------------------------------------------

        self.crear_contenedor_principal()


        # ----------------------------------------------------
        # ENCABEZADO
        # ----------------------------------------------------

        self.crear_encabezado()


        # ----------------------------------------------------
        # GESTOR DE ARCHIVOS
        # ----------------------------------------------------

        self.crear_gestor_archivos()


        # ----------------------------------------------------
        # GESTOR DEL PROCESO
        # ----------------------------------------------------

        self.crear_gestor_proceso()


        # ----------------------------------------------------
        # GESTOR DEL RESUMEN
        # ----------------------------------------------------

        self.crear_gestor_resumen()


        # ----------------------------------------------------
        # ESTADO INFERIOR
        # ----------------------------------------------------

        self.crear_estado_inferior()


    # ========================================================
    # SIDEBAR
    # ========================================================

    def crear_sidebar(self):
        """
        Crea el panel lateral izquierdo.
        """

        self.sidebar = ctk.CTkFrame(
            self,
            width=ANCHO_SIDEBAR_INICIAL,
            corner_radius=0,
            fg_color=AZUL_OSCURO
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(
            False
        )


        # ====================================================
        # CARGAR IMAGEN
        # ====================================================

        ruta_imagen = (
            RUTA_ARCHIVOS / "sidebar_trustcore.png"
        )


        # ----------------------------------------------------
        # VERIFICAR EXISTENCIA
        # ----------------------------------------------------

        if not ruta_imagen.exists():

            self.crear_sidebar_sin_imagen()

            return


        # ----------------------------------------------------
        # ABRIR IMAGEN
        # ----------------------------------------------------

        try:

            self.imagen_sidebar_original = (
                Image.open(
                    ruta_imagen
                ).convert(
                    "RGB"
                )
            )

        except Exception:

            self.crear_sidebar_sin_imagen()

            return


        # ====================================================
        # LABEL DE IMAGEN
        # ====================================================

        self.label_sidebar = ctk.CTkLabel(
            self.sidebar,
            text=""
        )

        self.label_sidebar.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )


        # ====================================================
        # EVENTO PARA REDIMENSIONAR IMAGEN
        # ====================================================

        self.sidebar.bind(
            "<Configure>",
            self.actualizar_sidebar
        )


        # ====================================================
        # BOTÓN SALIR
        # ====================================================

        self.boton_salir = crear_boton_salir(
            self.sidebar,
            self.salir
        )

        self.boton_salir.place(
            relx=0.5,
            rely=0.94,
            relwidth=0.78,
            anchor="center"
        )


    # ========================================================
    # SIDEBAR SIN IMAGEN
    # ========================================================

    def crear_sidebar_sin_imagen(self):
        """
        Crea el contenido mínimo del sidebar cuando la imagen
        no está disponible.
        """

        self.label_sidebar = ctk.CTkLabel(
            self.sidebar,
            text="TRUCKING",
            font=(
                "Segoe UI",
                20,
                "bold"
            ),
            text_color=BLANCO
        )

        self.label_sidebar.place(
            relx=0.5,
            rely=0.15,
            anchor="center"
        )


        # ----------------------------------------------------
        # BOTÓN SALIR
        # ----------------------------------------------------

        self.boton_salir = crear_boton_salir(
            self.sidebar,
            self.salir
        )

        self.boton_salir.place(
            relx=0.5,
            rely=0.94,
            relwidth=0.78,
            anchor="center"
        )


    # ========================================================
    # ANCHO RESPONSIVE DEL SIDEBAR
    # ========================================================

    def actualizar_ancho_sidebar(
        self,
        event=None
    ):
        """
        Calcula dinámicamente el ancho del sidebar.

        Se utiliza aproximadamente el 20% del ancho de la
        ventana, respetando los límites establecidos.
        """

        if event is not None and event.widget is not self:
            return
        ancho_ventana = self.winfo_width() / self._get_window_scaling()

        # En ventanas estrechas se prioriza el formulario sobre la decoración.
        if ancho_ventana < ANCHO_MINIMO:
            self.sidebar.grid_remove()
            return
        if not self.sidebar.winfo_ismapped():
            self.sidebar.grid()


        # ----------------------------------------------------
        # EVITAR TAMAÑOS INVÁLIDOS
        # ----------------------------------------------------

        if ancho_ventana <= 1:

            return


        # ====================================================
        # CALCULAR ANCHO
        # ====================================================

        nuevo_ancho = int(
            ancho_ventana * 0.20
        )


        # ====================================================
        # APLICAR LÍMITES
        # ====================================================

        nuevo_ancho = max(
            ANCHO_SIDEBAR_MIN,
            nuevo_ancho
        )

        nuevo_ancho = min(
            ANCHO_SIDEBAR_MAX,
            nuevo_ancho
        )


        # ====================================================
        # EVITAR ACTUALIZACIONES INNECESARIAS
        # ====================================================

        if self.sidebar.cget("width") == nuevo_ancho:

            return


        # ====================================================
        # ACTUALIZAR ANCHO
        # ====================================================

        self.sidebar.configure(
            width=nuevo_ancho
        )


    # ========================================================
    # ACTUALIZAR IMAGEN DEL SIDEBAR
    # ========================================================

    def actualizar_sidebar(
        self,
        event
    ):
        """
        Redimensiona la imagen del sidebar manteniendo sus
        proporciones originales.

        Se utiliza ImageOps.contain() para evitar recortes.
        """

        if self.imagen_sidebar_original is None:

            return


        ancho = event.width

        alto = event.height
        escala = self.label_sidebar._get_widget_scaling()


        # ----------------------------------------------------
        # EVITAR TAMAÑOS INVÁLIDOS
        # ----------------------------------------------------

        if ancho <= 10 or alto <= 10:

            return


        # ====================================================
        # REDIMENSIONAR SIN RECORTAR
        # ====================================================

        imagen = ImageOps.contain(
            self.imagen_sidebar_original,
            (
                ancho,
                max(1, alto - round(80 * escala))
            ),
            method=Image.Resampling.LANCZOS
        )


        # ====================================================
        # CREAR FONDO
        # ====================================================



        # ====================================================
        # CENTRAR IMAGEN
        # ====================================================

        posicion_x = (
            ancho - imagen.width
        ) // 2

        posicion_y = max(0, (alto - round(80 * escala) - imagen.height) // 2)


        fondo = componer_fondo(
            imagen, ancho, alto, posicion_x, posicion_y, AZUL_OSCURO
        )


        # ====================================================
        # CREAR IMAGEN CTK
        # ====================================================

        self.imagen_sidebar_ctk = ctk.CTkImage(
            light_image=fondo,
            dark_image=fondo,
            size=(
                ancho / escala,
                alto / escala
            )
        )


        # ====================================================
        # MOSTRAR IMAGEN
        # ====================================================

        self.label_sidebar.configure(
            image=self.imagen_sidebar_ctk
        )


    # ========================================================
    # CONTENEDOR PRINCIPAL
    # ========================================================

    def crear_contenedor_principal(self):
        """
        Crea el contenedor principal desplazable.
        """

        self.contenedor_principal = ctk.CTkScrollableFrame(
            self,
            corner_radius=0,
            fg_color=GRIS_CLARO
        )

        self.contenedor_principal.grid(
            row=0,
            column=1,
            sticky="nsew"
        )


        # ----------------------------------------------------
        # UNA COLUMNA RESPONSIVE
        # ----------------------------------------------------

        self.contenedor_principal.grid_columnconfigure(
            0,
            weight=1
        )


    # ========================================================
    # ENCABEZADO
    # ========================================================

    def crear_encabezado(self):
        """
        Crea el encabezado principal de la aplicación.
        """

        self.frame_encabezado = ctk.CTkFrame(
            self.contenedor_principal,
            fg_color=BLANCO,
            corner_radius=0,
            height=105
        )

        self.frame_encabezado.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        self.frame_encabezado.grid_propagate(
            False
        )


        # ====================================================
        # CONTENIDO
        # ====================================================

        contenido = ctk.CTkFrame(
            self.frame_encabezado,
            fg_color="transparent"
        )

        contenido.pack(
            fill="both",
            expand=True,
            padx=35
        )


        # ====================================================
        # TÍTULO
        # ====================================================

        self.label_titulo = ctk.CTkLabel(
            contenido,
            text="DEPURADOR DE BASES - TRUCKING",
            font=FUENTE_TITULO,
            text_color=AZUL_OSCURO,
            anchor="w"
        )

        self.label_titulo.pack(
            anchor="w",
            pady=(23, 0)
        )


        # ====================================================
        # SUBTÍTULO
        # ====================================================

        self.label_subtitulo = ctk.CTkLabel(
            contenido,
            text="Limpia. Valida. Cruza. Exporta.",
            font=FUENTE_SUBTITULO,
            text_color=GRIS_TEXTO,
            anchor="w"
        )

        self.label_subtitulo.pack(
            anchor="w"
        )


        # ====================================================
        # VERSIÓN
        # ====================================================

        self.label_version = ctk.CTkLabel(
            contenido,
            text="v1.0",
            width=45,
            height=24,
            corner_radius=12,
            fg_color=GRIS_CLARO,
            text_color=GRIS_TEXTO,
            font=(
                "Segoe UI",
                9,
                "bold"
            )
        )

        self.label_version.place(
            relx=0.97,
            y=20,
            anchor="ne"
        )


    # ========================================================
    # CREAR GESTOR DE ARCHIVOS
    # ========================================================

    def crear_gestor_archivos(self):
        """
        Crea el componente encargado de seleccionar los
        archivos de entrada y salida.
        """

        self.gestor_archivos = GestorArchivos(
            self.contenedor_principal,
            row=1
        )


    # ========================================================
    # CREAR GESTOR DEL PROCESO
    # ========================================================

    def crear_gestor_proceso(self):
        """
        Crea el componente encargado de ejecutar y mostrar
        el progreso de la depuración.
        """

        self.gestor_proceso = GestorProceso(
            self.contenedor_principal,
            obtener_rutas=self.obtener_rutas,
            callback_resumen=self.actualizar_resumen,
            callback_estado=self.actualizar_estado
        )


    # ========================================================
    # CREAR GESTOR DEL RESUMEN
    # ========================================================

    def crear_gestor_resumen(self):
        """
        Crea el componente encargado de mostrar las estadísticas
        finales y parciales.
        """

        self.gestor_resumen = GestorResumen(
            self.contenedor_principal,
            row=3
        )


    # ========================================================
    # OBTENER RUTAS
    # ========================================================

    def obtener_rutas(self):
        """
        Obtiene las rutas seleccionadas en el gestor de
        archivos.

        Retorna
        -------
        tuple

            (
                archivo_origen,
                ruta_excel,
                ruta_csv,
                archivo_data,
                archivo_filtros
            )
        """

        return self.gestor_archivos.obtener_rutas()


    # ========================================================
    # ACTUALIZAR RESUMEN
    # ========================================================

    def actualizar_resumen(
        self,
        total,
        montaje,
        rechazos,
        excel_generado=False,
        csv_generado=False
    ):
        """
        Envía las estadísticas al gestor del resumen.
        """

        if not hasattr(
            self,
            "gestor_resumen"
        ):

            return


        # ----------------------------------------------------
        # ACTUALIZAR ESTADÍSTICAS
        # ----------------------------------------------------

        self.gestor_resumen.actualizar_estadisticas(
            total,
            montaje,
            rechazos
        )


        # ----------------------------------------------------
        # ACTUALIZAR ARCHIVOS
        # ----------------------------------------------------

        if excel_generado or csv_generado:

            self.gestor_resumen.actualizar_archivos(
                excel_generado,
                csv_generado
            )


    # ========================================================
    # CREAR ESTADO INFERIOR
    # ========================================================

    def crear_estado_inferior(self):
        """
        Crea el indicador de estado ubicado en la parte
        inferior de la ventana.
        """

        self.label_estado = ctk.CTkLabel(
            self.contenedor_principal,
            text="●  Listo para procesar",
            height=40,
            corner_radius=8,
            fg_color="#E8F8EF",
            text_color="#18A957",
            font=FUENTE_NORMAL_NEGRITA,
            anchor="w"
        )

        self.label_estado.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=25,
            pady=(5, 18)
        )


    # ========================================================
    # ACTUALIZAR ESTADO
    # ========================================================

    def actualizar_estado(
        self,
        texto,
        fondo,
        color
    ):
        """
        Actualiza el indicador de estado inferior.
        """

        if not hasattr(
            self,
            "label_estado"
        ):

            return


        self.label_estado.configure(
            text=texto,
            fg_color=fondo,
            text_color=color
        )


    # ========================================================
    # SALIR
    # ========================================================

    def salir(self):
        """
        Cierra la aplicación solicitando confirmación al
        usuario.

        Si existe un proceso activo, se informa que cerrarlo
        podría interrumpir la depuración.
        """

        # ====================================================
        # VERIFICAR PROCESO ACTIVO
        # ====================================================

        proceso_activo = False


        if hasattr(
            self,
            "gestor_proceso"
        ):

            proceso_activo = (
                self.gestor_proceso.esta_en_ejecucion()
            )


        # ====================================================
        # PROCESO ACTIVO
        # ====================================================

        if proceso_activo:

            confirmar = solicitar_confirmacion(
                self,
                "Proceso en ejecución",
                (
                    "La depuración todavía está en ejecución.\n\n"
                    "Si cierras la aplicación, el proceso podría "
                    "interrumpirse.\n\n"
                    "¿Deseas cerrar la aplicación?"
                ),
                texto_confirmar="Salir"
            )


            if not confirmar:

                return


        # ====================================================
        # SIN PROCESO
        # ====================================================

        else:

            confirmar = solicitar_confirmacion(
                self,
                "Salir",
                "¿Deseas cerrar el Depurador de Bases?",
                texto_confirmar="Salir"
            )


            if not confirmar:

                return


        # ====================================================
        # CERRAR
        # ====================================================

        self.destroy()


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    app = Aplicacion()

    app.mainloop()
