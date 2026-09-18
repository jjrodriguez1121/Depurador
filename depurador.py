# ============================================================
# DEPURADOR PRINCIPAL - TRUKING
# ============================================================
#
# Este archivo es el punto de entrada principal del proyecto.
#
# El proceso puede ejecutarse:
#
#     - Desde consola.
#     - Desde la interfaz gráfica.
#
# La interfaz puede enviar un callback para recibir información
# sobre el progreso del proceso.
#
# ============================================================
#
# ETAPAS VISUALES PARA LA INTERFAZ
#
# 1. Cargar datos
# 2. Procesar teléfonos
# 3. Validar representantes
# 4. Cruces DOT
# 5. Limpieza
# 6. Generar archivos
# 7. Completado
#
# ============================================================


# ============================================================
# 1. IMPORTACIÓN DE MÓDULOS
# ============================================================

from depuracion.carga_datos import (
    cargar_y_preparar_datos
)

from depuracion.telefonos import (
    procesar_telefonos
)

from depuracion.representantes import (
    procesar_representantes,
    procesar_nombres_latinos
)

from depuracion.cruces import (
    procesar_cruces
)

from salida.salida_excel import (
    exportar_excel
)

from salida.exportador_csv import (
    exportar_csv
)


# ============================================================
# 2. FUNCIÓN PARA REPORTAR EL PROGRESO
# ============================================================

def reportar_progreso(
    callback,
    etapa,
    mensaje,
    montaje=None,
    rechazos=None,
    total=None
):
    """
    Envía información del proceso a la interfaz gráfica.

    Parámetros
    ----------
    callback:
        Función proporcionada por interfaz.py.

    etapa:
        Número de etapa visual actual.

        1 = Cargar datos
        2 = Procesar teléfonos
        3 = Validar representantes
        4 = Cruces DOT
        5 = Limpieza
        6 = Generar archivos
        7 = Completado

    mensaje:
        Mensaje que se mostrará en la interfaz.

    montaje:
        DataFrame actual de registros aceptados.

    rechazos:
        DataFrame acumulado de registros rechazados.

    total:
        Cantidad total de registros de la base original.
    """

    # --------------------------------------------------------
    # Si no existe callback, solamente continuamos.
    #
    # Esto permite que depurador.py siga funcionando aunque
    # sea ejecutado sin interfaz gráfica.
    # --------------------------------------------------------

    if callback is None:
        return


    # --------------------------------------------------------
    # Cantidad actual en montaje
    # --------------------------------------------------------

    cantidad_montaje = (
        len(montaje)
        if montaje is not None
        else 0
    )


    # --------------------------------------------------------
    # Cantidad actual en rechazos
    # --------------------------------------------------------

    cantidad_rechazos = (
        len(rechazos)
        if rechazos is not None
        else 0
    )


    # --------------------------------------------------------
    # Crear información estadística
    # --------------------------------------------------------

    estadisticas = {
        "total": total if total is not None else 0,
        "montaje": cantidad_montaje,
        "rechazos": cantidad_rechazos
    }


    # --------------------------------------------------------
    # Ejecutar callback
    # --------------------------------------------------------

    callback(
        etapa,
        mensaje,
        estadisticas
    )


# ============================================================
# 3. FUNCIÓN PRINCIPAL
# ============================================================

def ejecutar_depuracion(
    archivo_origen,
    ruta_excel,
    ruta_csv,
    minimo_coincidencias=1,
    callback=None
):
    """
    Ejecuta el proceso completo de depuración.

    Parámetros
    ----------
    archivo_origen:
        Ruta del archivo que el usuario desea depurar.

    ruta_excel:
        Ruta donde se guardará el archivo Excel.

    ruta_csv:
        Ruta donde se guardará el archivo CSV.

    minimo_coincidencias:
        Cantidad mínima de palabras de Company_Rep1 que
        deben coincidir con FILTROS ESPAÑOL.

        1 = al menos una coincidencia.
        2 = al menos dos coincidencias.

        Las coincidencias pueden ser iguales.

    callback:
        Función opcional utilizada por la interfaz gráfica
        para recibir información del progreso.

    Retorna
    -------
    base:
        Base original.

    montaje:
        Base final depurada.

    rechazos:
        Registros rechazados durante el proceso.
    """


    # ========================================================
    # INICIO
    # ========================================================

    print("\n")
    print("=" * 70)
    print("             DEPURADOR DE BASES - TRUKING")
    print("=" * 70)

    print(
        "\nIniciando proceso completo de depuración..."
    )


    # ========================================================
    # MOSTRAR CONFIGURACIÓN RECIBIDA
    # ========================================================

    print("\n")
    print("=" * 70)
    print("CONFIGURACIÓN SELECCIONADA")
    print("=" * 70)

    print(
        "\nArchivo de entrada:"
    )

    print(
        archivo_origen
    )

    print(
        "\nRuta de salida Excel:"
    )

    print(
        ruta_excel
    )

    print(
        "\nRuta de salida CSV:"
    )

    print(
        ruta_csv
    )

    print(
        "\nMínimo de coincidencias para representante:"
    )

    print(
        minimo_coincidencias
    )


    # ========================================================
    # ETAPA 1
    # CARGA Y PREPARACIÓN DE DATOS
    # ========================================================

    print("\n")
    print("=" * 70)
    print("ETAPA 1 - CARGA Y PREPARACIÓN DE DATOS")
    print("=" * 70)


    # --------------------------------------------------------
    # Avisar a la interfaz que comenzó la etapa 1
    # --------------------------------------------------------

    reportar_progreso(
        callback,
        1,
        "Cargando datos de la base..."
    )


    # --------------------------------------------------------
    # Cargar y preparar
    # --------------------------------------------------------

    (
        base,
        montaje,
        rechazos,
        archivo,
        fecha_montaje
    ) = cargar_y_preparar_datos(
        archivo_origen
    )


    # --------------------------------------------------------
    # Cantidad original de registros
    # --------------------------------------------------------

    cantidad_base = len(base)


    print(
        f"\nBase cargada correctamente."
    )

    print(
        f"Registros encontrados: {cantidad_base:,}"
    )


    # --------------------------------------------------------
    # Informar resultado de etapa 1
    # --------------------------------------------------------

    reportar_progreso(
        callback,
        1,
        (
            f"Base cargada correctamente. "
            f"{cantidad_base:,} registros."
        ),
        montaje,
        rechazos,
        cantidad_base
    )


    # ========================================================
    # ETAPA 2
    # VALIDACIÓN DE TELÉFONOS
    # ========================================================

    print("\n")
    print("=" * 70)
    print("ETAPA 2 - VALIDACIÓN DE TELÉFONOS")
    print("=" * 70)


    # --------------------------------------------------------
    # Avisar inicio
    # --------------------------------------------------------

    reportar_progreso(
        callback,
        2,
        "Procesando y validando teléfonos...",
        montaje,
        rechazos,
        cantidad_base
    )


    # --------------------------------------------------------
    # Procesar teléfonos
    # --------------------------------------------------------

    montaje, rechazos = procesar_telefonos(
        montaje,
        rechazos
    )


    print(
        f"\nTeléfonos procesados."
    )

    print(
        f"Registros restantes en montaje: "
        f"{len(montaje):,}"
    )

    print(
        f"Registros rechazados acumulados: "
        f"{len(rechazos):,}"
    )


    # --------------------------------------------------------
    # Informar resultado
    # --------------------------------------------------------

    reportar_progreso(
        callback,
        2,
        (
            f"Teléfonos procesados. "
            f"{len(montaje):,} registros restantes."
        ),
        montaje,
        rechazos,
        cantidad_base
    )


    # ========================================================
    # ETAPA 3
    # VALIDACIÓN DE REPRESENTANTE
    # ========================================================
    #
    # En esta etapa se revisa:
    #
    # - Que Company_Rep1 no esté vacío.
    #
    # Los registros sin representante pasan a Rechazos.
    #
    # La validación de nombre latino se realiza después
    # del cruce contra data.
    #
    # ========================================================

    print("\n")
    print("=" * 70)
    print("ETAPA 3 - VALIDACIÓN DE REPRESENTANTE")
    print("=" * 70)


    # --------------------------------------------------------
    # Avisar inicio
    # --------------------------------------------------------

    reportar_progreso(
        callback,
        3,
        "Validando representantes...",
        montaje,
        rechazos,
        cantidad_base
    )


    # --------------------------------------------------------
    # Procesar representantes
    # --------------------------------------------------------

    montaje, rechazos = procesar_representantes(
        montaje,
        rechazos
    )


    print(
        f"\nRepresentantes validados."
    )

    print(
        f"Registros restantes en montaje: "
        f"{len(montaje):,}"
    )

    print(
        f"Registros rechazados acumulados: "
        f"{len(rechazos):,}"
    )


    # --------------------------------------------------------
    # Informar resultado
    # --------------------------------------------------------

    reportar_progreso(
        callback,
        3,
        (
            f"Representantes validados. "
            f"{len(montaje):,} registros restantes."
        ),
        montaje,
        rechazos,
        cantidad_base
    )


    # ========================================================
    # ETAPA 4
    # VALIDACIÓN Y CRUCE DE DOT
    # ========================================================
    #
    # Se realizan:
    #
    # 1. DOT repetido dentro de la misma base.
    #
    # 2. Cruce contra el archivo externo data.
    #
    # El archivo data será seleccionado automáticamente
    # según la lógica definida en cruces.py.
    #
    # ========================================================

    print("\n")
    print("=" * 70)
    print("ETAPA 4 - VALIDACIÓN Y CRUCE DE DOT")
    print("=" * 70)


    # --------------------------------------------------------
    # Avisar inicio
    # --------------------------------------------------------

    reportar_progreso(
        callback,
        4,
        "Realizando validación y cruces de DOT...",
        montaje,
        rechazos,
        cantidad_base
    )


    # --------------------------------------------------------
    # Procesar cruces
    # --------------------------------------------------------

    montaje, rechazos = procesar_cruces(
        montaje,
        rechazos
    )


    print(
        f"\nCruces DOT completados."
    )

    print(
        f"Registros restantes en montaje: "
        f"{len(montaje):,}"
    )

    print(
        f"Registros rechazados acumulados: "
        f"{len(rechazos):,}"
    )


    # --------------------------------------------------------
    # Informar resultado
    # --------------------------------------------------------

    reportar_progreso(
        callback,
        4,
        (
            f"Cruces DOT completados. "
            f"{len(montaje):,} registros restantes."
        ),
        montaje,
        rechazos,
        cantidad_base
    )


    # ========================================================
    # ETAPA 5
    # VALIDACIÓN DE NOMBRES LATINOS + LIMPIEZA
    # ========================================================
    #
    # Esta es la última etapa de depuración de registros.
    #
    # Primero:
    #
    #     Company_Rep1
    #
    # se valida contra FILTROS ESPAÑOL.
    #
    # La cantidad mínima de coincidencias es definida por
    # el usuario.
    #
    # Los no reconocidos pasan a Rechazos.
    #
    # Después:
    #
    # solamente los registros que quedaron en Montaje
    # reciben la limpieza.
    #
    # ========================================================

    print("\n")
    print("=" * 70)
    print("ETAPA 5 - NOMBRES LATINOS Y LIMPIEZA")
    print("=" * 70)


    # --------------------------------------------------------
    # Avisar inicio
    # --------------------------------------------------------

    reportar_progreso(
        callback,
        5,
        "Validando nombres latinos y limpiando información...",
        montaje,
        rechazos,
        cantidad_base
    )


    # --------------------------------------------------------
    # Validar nombres + limpieza
    # --------------------------------------------------------

    montaje, rechazos = procesar_nombres_latinos(
        montaje,
        rechazos,
        minimo_coincidencias
    )


    print(
        f"\nNombres latinos y limpieza completados."
    )

    print(
        f"Registros finales en montaje: "
        f"{len(montaje):,}"
    )

    print(
        f"Registros rechazados acumulados: "
        f"{len(rechazos):,}"
    )


    # --------------------------------------------------------
    # Informar resultado
    # --------------------------------------------------------

    reportar_progreso(
        callback,
        5,
        (
            f"Limpieza completada. "
            f"{len(montaje):,} registros finales."
        ),
        montaje,
        rechazos,
        cantidad_base
    )


    # ========================================================
    # ETAPA 6
    # CONTROL DE TRAZABILIDAD
    # ========================================================
    #
    # Antes de generar los archivos comprobamos:
    #
    # Base original =
    #
    #     Montaje final + Rechazos
    #
    # ========================================================

    print("\n")
    print("=" * 70)
    print("ETAPA 6 - CONTROL DE TRAZABILIDAD")
    print("=" * 70)


    cantidad_base = len(base)

    cantidad_montaje = len(montaje)

    cantidad_rechazos = len(rechazos)

    cantidad_total = (
        cantidad_montaje
        + cantidad_rechazos
    )


    print(
        "\nRegistros en Base original:"
    )

    print(
        cantidad_base
    )


    print(
        "\nRegistros finales en Montaje:"
    )

    print(
        cantidad_montaje
    )


    print(
        "\nRegistros acumulados en Rechazos:"
    )

    print(
        cantidad_rechazos
    )


    print(
        "\nMontaje + Rechazos:"
    )

    print(
        cantidad_total
    )


    # ========================================================
    # VALIDAR TRAZABILIDAD
    # ========================================================

    if cantidad_base != cantidad_total:

        raise ValueError(
            "\nERROR DE TRAZABILIDAD.\n\n"
            f"Base original: {cantidad_base}\n"
            f"Montaje + Rechazos: {cantidad_total}\n\n"
            "La cantidad de registros no coincide."
        )


    print(
        "\nControl de trazabilidad: OK"
    )


    # ========================================================
    # ETAPA 6
    # GENERACIÓN DE ARCHIVOS
    # ========================================================
    #
    # Visualmente esta etapa aparecerá como:
    #
    #     Generar archivos
    #
    # Aquí generamos:
    #
    #     1. Excel
    #     2. CSV
    #
    # ========================================================

    print("\n")
    print("=" * 70)
    print("ETAPA 7 - GENERACIÓN DE ARCHIVOS")
    print("=" * 70)


    # --------------------------------------------------------
    # Avisar a la interfaz
    # --------------------------------------------------------

    reportar_progreso(
        callback,
        6,
        "Generando archivo Excel...",
        montaje,
        rechazos,
        cantidad_base
    )


    # --------------------------------------------------------
    # GENERAR EXCEL
    # --------------------------------------------------------

    archivo_excel = exportar_excel(
        base,
        montaje,
        rechazos,
        ruta_excel
    )


    print(
        "\nExcel generado correctamente:"
    )

    print(
        archivo_excel
    )


    # --------------------------------------------------------
    # Informar Excel
    # --------------------------------------------------------

    reportar_progreso(
        callback,
        6,
        "Excel generado correctamente. Generando CSV...",
        montaje,
        rechazos,
        cantidad_base
    )


    # --------------------------------------------------------
    # GENERAR CSV
    # --------------------------------------------------------

    archivo_csv = exportar_csv(
        archivo_excel,
        ruta_csv
    )


    print(
        "\nCSV generado correctamente:"
    )

    print(
        archivo_csv
    )


    # --------------------------------------------------------
    # Informar CSV
    # --------------------------------------------------------

    reportar_progreso(
        callback,
        6,
        "Excel y CSV generados correctamente.",
        montaje,
        rechazos,
        cantidad_base
    )


    # ========================================================
    # ETAPA 7
    # COMPLETADO
    # ========================================================

    print("\n")
    print("=" * 70)
    print("             PROCESO COMPLETADO")
    print("=" * 70)


    # --------------------------------------------------------
    # Informar finalización
    # --------------------------------------------------------

    reportar_progreso(
        callback,
        7,
        "Proceso completado correctamente.",
        montaje,
        rechazos,
        cantidad_base
    )


    print(
        "\nArchivos generados:"
    )


    print(
        "\n1. Excel:"
    )

    print(
        archivo_excel
    )


    print(
        "\n2. CSV:"
    )

    print(
        archivo_csv
    )


    print("\n")
    print("=" * 70)
    print("DEPURACIÓN FINALIZADA CORRECTAMENTE")
    print("=" * 70)


    # ========================================================
    # RETORNAR RESULTADOS
    # ========================================================

    return (
        base,
        montaje,
        rechazos
    )


# ============================================================
# 4. EJECUCIÓN DIRECTA
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 70)
    print("DEPURADOR DE BASES - TRUKING")
    print("=" * 70)

    print(
        "\nEste programa debe ser iniciado actualmente "
        "desde interfaz.py."
    )

    print(
        "\nLa interfaz gráfica será la encargada de "
        "proporcionar las rutas."
    )