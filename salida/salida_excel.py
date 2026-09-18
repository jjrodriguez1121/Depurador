# ============================================================
# MODULO: SALIDA EXCEL
# ============================================================
#
# Este módulo genera el archivo Excel final.
#
# Hojas:
#
#   1. Base
#   2. Montaje
#   3. Rechazos
#
# ============================================================


# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd

from pathlib import Path

from config import (
    NOMBRE_HOJA_BASE,
    NOMBRE_HOJA_MONTAJE,
    NOMBRE_HOJA_RECHAZOS
)


# ============================================================
# COLUMNAS DE FECHA
# ============================================================

COLUMNAS_FECHA = [
    "Policy_Effective_Date",
    "Policy_Cancellation_Date"
]


# ============================================================
# CREAR COPIAS
# ============================================================

def crear_copias_exportacion(
    base,
    montaje,
    rechazos
):

    base_export = base.copy()

    montaje_export = montaje.copy()

    rechazos_export = rechazos.copy()


    return (
        base_export,
        montaje_export,
        rechazos_export
    )


# ============================================================
# CONVERTIR FECHAS
# ============================================================

def convertir_fechas_exportacion(
    base_export,
    montaje_export,
    rechazos_export
):

    for columna in COLUMNAS_FECHA:

        # ----------------------------------------------------
        # Base
        # ----------------------------------------------------

        if columna in base_export.columns:

            base_export[columna] = pd.to_datetime(
                base_export[columna],
                errors="coerce",
                dayfirst=False
            )


        # ----------------------------------------------------
        # Montaje
        # ----------------------------------------------------

        if columna in montaje_export.columns:

            montaje_export[columna] = pd.to_datetime(
                montaje_export[columna],
                errors="coerce",
                dayfirst=False
            )


        # ----------------------------------------------------
        # Rechazos
        # ----------------------------------------------------

        if columna in rechazos_export.columns:

            rechazos_export[columna] = pd.to_datetime(
                rechazos_export[columna],
                errors="coerce",
                dayfirst=False
            )


    return (
        base_export,
        montaje_export,
        rechazos_export
    )


# ============================================================
# GENERAR EXCEL
# ============================================================

def generar_excel(
    base_export,
    montaje_export,
    rechazos_export,
    ruta_excel
):

    ruta_excel = Path(
        ruta_excel
    )


    # --------------------------------------------------------
    # Crear carpeta de destino.
    # --------------------------------------------------------

    ruta_excel.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    print("\n========================================")
    print("GENERANDO ARCHIVO EXCEL")
    print("========================================")


    print(
        "\nRuta de salida:"
    )


    print(
        ruta_excel
    )


    # ========================================================
    # CREAR EXCEL
    # ========================================================

    with pd.ExcelWriter(
        ruta_excel,
        engine="openpyxl"
    ) as writer:

        # ----------------------------------------------------
        # Base
        # ----------------------------------------------------

        base_export.to_excel(
            writer,
            sheet_name=NOMBRE_HOJA_BASE,
            index=False
        )


        # ----------------------------------------------------
        # Montaje
        # ----------------------------------------------------

        montaje_export.to_excel(
            writer,
            sheet_name=NOMBRE_HOJA_MONTAJE,
            index=False
        )


        # ----------------------------------------------------
        # Rechazos
        # ----------------------------------------------------

        rechazos_export.to_excel(
            writer,
            sheet_name=NOMBRE_HOJA_RECHAZOS,
            index=False
        )


        # ====================================================
        # FORMATO DE FECHAS
        # ====================================================

        for nombre_hoja in [
            NOMBRE_HOJA_BASE,
            NOMBRE_HOJA_MONTAJE,
            NOMBRE_HOJA_RECHAZOS
        ]:

            hoja = writer.book[
                nombre_hoja
            ]


            for columna in hoja.iter_cols():

                encabezado = columna[0].value


                if encabezado in COLUMNAS_FECHA:

                    for celda in columna[1:]:

                        if celda.value is not None:

                            celda.number_format = "mm/dd/yyyy"


    return ruta_excel


# ============================================================
# VERIFICAR ARCHIVO
# ============================================================

def verificar_archivo_creado(
    ruta_excel
):

    ruta_excel = Path(
        ruta_excel
    )


    print("\n========================================")
    print("ARCHIVO EXCEL GENERADO")
    print("========================================")


    print(
        "\nArchivo:"
    )


    print(
        ruta_excel
    )


    existe = ruta_excel.exists()


    print(
        "\n¿El archivo existe?:",
        existe
    )


    if existe:

        tamaño = ruta_excel.stat().st_size


        print(
            "Tamaño:",
            tamaño,
            "bytes"
        )


    return existe


# ============================================================
# VERIFICAR EXCEL
# ============================================================

def verificar_excel(
    ruta_excel
):

    ruta_excel = Path(
        ruta_excel
    )


    try:

        prueba = pd.ExcelFile(
            ruta_excel,
            engine="openpyxl"
        )


        print("\n========================================")
        print("VERIFICACIÓN DEL ARCHIVO")
        print("========================================")


        print(
            "\nArchivo Excel válido."
        )


        print(
            "\nHojas encontradas:"
        )


        for hoja in prueba.sheet_names:

            print(
                "-",
                hoja
            )


        # ----------------------------------------------------
        # Verificar hojas esperadas.
        # ----------------------------------------------------

        hojas_esperadas = [
            NOMBRE_HOJA_BASE,
            NOMBRE_HOJA_MONTAJE,
            NOMBRE_HOJA_RECHAZOS
        ]


        if prueba.sheet_names != hojas_esperadas:

            prueba.close()


            raise ValueError(
                "\nLas hojas del Excel no coinciden con "
                "la estructura esperada.\n\n"
                f"Esperadas: {hojas_esperadas}\n"
                f"Encontradas: {prueba.sheet_names}"
            )


        prueba.close()


        return True


    except Exception as error:

        print("\n========================================")
        print("ERROR AL VERIFICAR EL EXCEL")
        print("========================================")


        print(
            type(error).__name__
        )


        print(
            error
        )


        return False


# ============================================================
# EXPORTAR EXCEL
# ============================================================

def exportar_excel(
    base,
    montaje,
    rechazos,
    ruta_excel
):

    ruta_excel = Path(
        ruta_excel
    )


    # --------------------------------------------------------
    # Crear copias.
    # --------------------------------------------------------

    (
        base_export,
        montaje_export,
        rechazos_export
    ) = crear_copias_exportacion(
        base,
        montaje,
        rechazos
    )


    # --------------------------------------------------------
    # Convertir fechas.
    # --------------------------------------------------------

    (
        base_export,
        montaje_export,
        rechazos_export
    ) = convertir_fechas_exportacion(
        base_export,
        montaje_export,
        rechazos_export
    )


    # --------------------------------------------------------
    # Generar Excel.
    # --------------------------------------------------------

    generar_excel(
        base_export,
        montaje_export,
        rechazos_export,
        ruta_excel
    )


    # --------------------------------------------------------
    # Verificar existencia.
    # --------------------------------------------------------

    archivo_existe = verificar_archivo_creado(
        ruta_excel
    )


    if not archivo_existe:

        raise FileNotFoundError(
            "\nEl archivo Excel no fue creado correctamente."
        )


    # --------------------------------------------------------
    # Verificar estructura.
    # --------------------------------------------------------

    archivo_valido = verificar_excel(
        ruta_excel
    )


    if not archivo_valido:

        raise ValueError(
            "\nEl archivo Excel fue creado, "
            "pero no pudo ser validado correctamente."
        )


    return ruta_excel


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("\n========================================")
    print("PRUEBA DEL MODULO SALIDA EXCEL")
    print("========================================")


    print(
        "\nEste módulo necesita recibir:"
    )


    print("- base")
    print("- montaje")
    print("- rechazos")
    print("- ruta_excel")


    print(
        "\nLa generación real del Excel se realizará"
    )


    print(
        "cuando sea llamado desde depurador.py."
    )