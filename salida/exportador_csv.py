# ============================================================
# EXPORTADOR CSV - TRUKING
# ============================================================
#
# Este módulo toma la hoja "Montaje" del Excel generado
# y construye el CSV requerido por la plataforma.
#
# No realiza depuración.
#
# ============================================================


# ============================================================
# 1. IMPORTACIONES
# ============================================================

import pandas as pd

from pathlib import Path

from datetime import date, datetime


# ============================================================
# 2. NOMBRE DE LA HOJA
# ============================================================

NOMBRE_HOJA = "Montaje"


# ============================================================
# 3. ESTRUCTURA EXACTA DEL CSV
# ============================================================

COLUMNAS_CSV = [
    "NOMBRE",
    "APELLIDO",
    "TIPOID",
    "ID",
    "EDAD",
    "SEXO",
    "PAIS",
    "DEPARTAMENTO",
    "CIUDAD",
    "ZONA",
    "DIRECCION",
    "OPT1",
    "OPT2",
    "OPT3",
    "OPT4",
    "OPT5",
    "OPT6",
    "OPT7",
    "OPT8",
    "OPT9",
    "OPT10",
    "OPT11",
    "OPT12",
    "TEL1",
    "TEL2",
    "TEL3",
    "TEL4",
    "TEL5",
    "TEL6",
    "TEL7",
    "TEL8",
    "TEL9",
    "TEL10",
    "OTROSTEL",
    "EMAIL",
    "RECALL-INFO",
    "AGENTE",
    "RESULTADOREG",
    "FECHAFINREG",
    "LLAMADAS",
    "IDCALL",
    "COD01",
    "DESC1",
    "COD02",
    "DESC2",
    "COMENTARIOSACUMULADOS",
    "DATE_RECALL",
    "COUNT_RECALL",
    "TEL_RECALL",
    "LAST_DIAL_TEL",
    "HISTORY_TEL"
]


# ============================================================
# 4. CONVERTIR VALORES A TEXTO
# ============================================================

def convertir_texto(valor):

    if pd.isna(valor):

        return ""


    # --------------------------------------------------------
    # Si es una fecha de Python.
    # --------------------------------------------------------

    if isinstance(
        valor,
        (datetime, date)
    ):

        return valor.strftime(
            "%m/%d/%Y"
        )


    # --------------------------------------------------------
    # Convertir a texto.
    # --------------------------------------------------------

    valor = str(valor).strip()


    # --------------------------------------------------------
    # Eliminar .0 al final.
    # --------------------------------------------------------

    if valor.endswith(".0"):

        valor = valor[:-2]


    return valor


# ============================================================
# 5. CONVERTIR FECHA PARA CSV
# ============================================================

def convertir_fecha_csv(valor):

    """
    Convierte una fecha proveniente de Excel a texto.

    Formato final:

        mm/dd/yyyy

    Ejemplo:

        03/25/2026
    """

    if pd.isna(valor):

        return ""


    # --------------------------------------------------------
    # Si pandas ya entregó un Timestamp.
    # --------------------------------------------------------

    if isinstance(
        valor,
        pd.Timestamp
    ):

        return valor.strftime(
            "%m/%d/%Y"
        )


    # --------------------------------------------------------
    # Si es datetime/date.
    # --------------------------------------------------------

    if isinstance(
        valor,
        (datetime, date)
    ):

        return valor.strftime(
            "%m/%d/%Y"
        )


    # --------------------------------------------------------
    # Convertir texto.
    # --------------------------------------------------------

    texto = str(valor).strip()


    # --------------------------------------------------------
    # Intentar convertir a fecha.
    # --------------------------------------------------------

    fecha = pd.to_datetime(
        texto,
        errors="coerce",
        dayfirst=False
    )


    if pd.notna(fecha):

        return fecha.strftime(
            "%m/%d/%Y"
        )


    # --------------------------------------------------------
    # Si no pudo convertirse, conservar el valor original.
    # --------------------------------------------------------

    return texto


# ============================================================
# 6. EXPORTAR CSV
# ============================================================

def exportar_csv(
    archivo_excel,
    ruta_csv
):

    """
    Lee Montaje y genera el CSV final.
    """

    archivo_excel = Path(
        archivo_excel
    )


    ruta_csv = Path(
        ruta_csv
    )


    # ========================================================
    # INICIO
    # ========================================================

    print("=" * 60)

    print("INICIO DEL EXPORTADOR CSV")

    print("=" * 60)


    # ========================================================
    # VALIDAR EXCEL
    # ========================================================

    if not archivo_excel.exists():

        raise FileNotFoundError(
            f"\nNo se encontró el archivo de depuración:\n"
            f"{archivo_excel}"
        )


    print(
        "\nArchivo de depuración encontrado:"
    )


    print(
        archivo_excel
    )


    # ========================================================
    # LEER MONTAJE
    # ========================================================

    print(
        f"\nLeyendo hoja: {NOMBRE_HOJA}"
    )


    montaje = pd.read_excel(
        archivo_excel,
        sheet_name=NOMBRE_HOJA,
        dtype=object
    )


    print(
        f"Registros encontrados en Montaje: "
        f"{len(montaje)}"
    )


    # ========================================================
    # COLUMNAS NECESARIAS
    # ========================================================

    columnas_necesarias = [
        "Legal_Name",
        "DOT",
        "Company_Rep1",
        "Business_State",
        "Years_In_Business",
        "Insurer",
        "Policy_Effective_Date",
        "Policy_Cancellation_Date",
        "Email",
        "Power_Units",
        "Phone"
    ]


    # ========================================================
    # VALIDAR COLUMNAS
    # ========================================================

    columnas_faltantes = [
        columna
        for columna in columnas_necesarias
        if columna not in montaje.columns
    ]


    if columnas_faltantes:

        raise ValueError(
            "\nFaltan las siguientes columnas en "
            "la hoja Montaje:\n\n"
            + "\n".join(
                columnas_faltantes
            )
        )


    print(
        "\nTodas las columnas necesarias fueron encontradas."
    )


    # ========================================================
    # CREAR DATAFRAME FINAL
    # ========================================================

    csv_final = pd.DataFrame(
        "",
        index=montaje.index,
        columns=COLUMNAS_CSV
    )


    # ========================================================
    # NOMBRE
    # ========================================================

    csv_final["NOMBRE"] = montaje[
        "Legal_Name"
    ].apply(
        convertir_texto
    )


    # ========================================================
    # APELLIDO
    # ========================================================

    csv_final["APELLIDO"] = ""


    # ========================================================
    # TIPOID
    # ========================================================

    csv_final["TIPOID"] = "DOT"


    # ========================================================
    # ID
    # ========================================================

    csv_final["ID"] = montaje[
        "DOT"
    ].apply(
        convertir_texto
    )


    # ========================================================
    # OPT1
    # ========================================================

    csv_final["OPT1"] = montaje[
        "Company_Rep1"
    ].apply(
        convertir_texto
    )


    # ========================================================
    # OPT2
    # ========================================================

    csv_final["OPT2"] = montaje[
        "Business_State"
    ].apply(
        convertir_texto
    )


    # ========================================================
    # OPT3
    # ========================================================

    csv_final["OPT3"] = montaje[
        "Years_In_Business"
    ].apply(
        convertir_texto
    )


    # ========================================================
    # OPT4
    # ========================================================

    csv_final["OPT4"] = montaje[
        "Insurer"
    ].apply(
        convertir_texto
    )


    # ========================================================
    # OPT5
    # ========================================================
    #
    # Policy_Effective_Date
    #
    # Se transforma explícitamente a:
    #
    #     mm/dd/yyyy
    #
    # ========================================================

    csv_final["OPT5"] = montaje[
        "Policy_Effective_Date"
    ].apply(
        convertir_fecha_csv
    )


    # ========================================================
    # OPT6
    # ========================================================
    #
    # Policy_Cancellation_Date
    #
    # Se transforma explícitamente a:
    #
    #     mm/dd/yyyy
    #
    # ========================================================

    csv_final["OPT6"] = montaje[
        "Policy_Cancellation_Date"
    ].apply(
        convertir_fecha_csv
    )


    # ========================================================
    # OPT7
    # ========================================================

    csv_final["OPT7"] = montaje[
        "Email"
    ].apply(
        convertir_texto
    )


    # ========================================================
    # OPT8
    # ========================================================

    csv_final["OPT8"] = montaje[
        "Power_Units"
    ].apply(
        convertir_texto
    )


    # ========================================================
    # OPT9
    # ========================================================

    fecha_actual = date.today().strftime(
        "%d/%m/%Y"
    )


    csv_final["OPT9"] = fecha_actual


    # ========================================================
    # TEL1
    # ========================================================

    csv_final["TEL1"] = montaje[
        "Phone"
    ].apply(
        convertir_texto
    )


    # ========================================================
    # VALIDACIONES
    # ========================================================

    print(
        "\nValidando cantidad de columnas..."
    )


    if len(csv_final.columns) != len(
        COLUMNAS_CSV
    ):

        raise ValueError(
            "La cantidad de columnas del CSV no coincide "
            "con la estructura definida."
        )


    print(
        "Validando orden de columnas..."
    )


    if list(csv_final.columns) != COLUMNAS_CSV:

        raise ValueError(
            "El orden de las columnas del CSV no coincide "
            "con la estructura definida."
        )


    print(
        "Validando cantidad de registros..."
    )


    if len(csv_final) != len(montaje):

        raise ValueError(
            "La cantidad de registros del CSV no coincide "
            "con la cantidad de registros de Montaje."
        )


    print(
        "Todas las validaciones fueron exitosas."
    )


    # ========================================================
    # CREAR CARPETA DE SALIDA
    # ========================================================

    ruta_csv.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    # ========================================================
    # EXPORTAR
    # ========================================================

    print(
        "\nGenerando archivo CSV delimitado por ';'..."
    )


    csv_final.to_csv(
        ruta_csv,
        index=False,
        encoding="utf-8-sig",
        sep=";"
    )


    # ========================================================
    # VALIDAR ARCHIVO
    # ========================================================

    if not ruta_csv.exists():

        raise FileNotFoundError(
            "\nEl archivo CSV no fue generado correctamente."
        )


    # ========================================================
    # INFORMACIÓN FINAL
    # ========================================================

    print("\n" + "=" * 60)

    print("EXPORTACIÓN COMPLETADA")

    print("=" * 60)


    print(
        "\nArchivo generado:"
    )


    print(
        ruta_csv
    )


    print(
        "\nCantidad de registros:"
    )


    print(
        len(csv_final)
    )


    print(
        "\nCantidad de columnas:"
    )


    print(
        len(csv_final.columns)
    )


    print(
        "\nFecha utilizada en OPT9:"
    )


    print(
        fecha_actual
    )


    print(
        "\nDelimitador utilizado:"
    )


    print(
        "Punto y coma (;)"
    )


    print(
        "\n" + "=" * 60
    )


    return ruta_csv


# ============================================================
# 7. PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("\n========================================")
    print("PRUEBA DEL MODULO EXPORTADOR CSV")
    print("========================================")


    print(
        "\nEste módulo necesita recibir:"
    )


    print(
        "- archivo_excel"
    )


    print(
        "- ruta_csv"
    )


    print(
        "\nLa generación real del CSV se realizará"
    )


    print(
        "cuando sea llamado desde depurador.py."
    )