from pathlib import Path
from datetime import datetime

import pandas as pd

from depuracion.carga_datos import validar_archivo_entrada

from config import (
    RUTA_DESCARGAS,
    EXTENSIONES_PERMITIDAS,
    NOMBRE_ARCHIVO_DATA
)


# ============================================================
# NORMALIZACIÓN DE DOT
# ============================================================

def normalizar_dot(valor):
    """
    Normaliza un valor DOT para poder compararlo correctamente.

    Reglas:
    - Convierte a texto.
    - Elimina espacios al inicio y al final.
    - Elimina el ".0" que puede aparecer cuando Excel convierte
      un DOT numérico a decimal.
    - Devuelve "" cuando el valor está vacío.
    """

    if pd.isna(valor):
        return ""

    valor = str(valor).strip()

    # Caso típico de Excel:
    # 1234567.0 -> 1234567
    if valor.endswith(".0"):
        valor = valor[:-2]

    return valor


# ============================================================
# BUSCAR ARCHIVO DATA
# ============================================================

def validar_dot(montaje, rechazos):
    """Rechaza DOT ausentes o no numéricos, sin consultar su existencia real.

    Solo se permiten dígitos ASCII tras normalizar espacios exteriores y .0.
    Los rechazados conservan su valor recibido para poder revisar el problema.
    """
    originales = montaje["DOT"].astype("string").str.strip()
    normalizados = montaje["DOT"].map(normalizar_dot).astype("string")
    vacios = originales.isna() | originales.eq("").fillna(False)
    validos = normalizados.str.fullmatch(r"[0-9]+", na=False) & ~vacios

    descartados = montaje.loc[~validos].copy()
    if not descartados.empty:
        descartados.insert(1, "Motivo Rechazo", "DOT invalido")
        rechazos = pd.concat([rechazos, descartados], ignore_index=True)

    montaje = montaje.loc[validos].copy()
    montaje["DOT"] = normalizados.loc[validos]
    print(f"\nRegistros rechazados sin DOT: {vacios.sum():,}")
    print(f"Registros rechazados por formato DOT: {(~validos & ~vacios).sum():,}")
    return montaje, rechazos


def buscar_archivo_data():
    """
    Busca los archivos llamados 'data' en la carpeta Descargas.

    Si existe más de uno, selecciona automáticamente el archivo
    modificado más recientemente.

    Ejemplo:

        data.csv
        data.xlsx

    Si data.xlsx fue modificado más recientemente, se utilizará
    data.xlsx.
    """

    archivos = [
        archivo
        for archivo in RUTA_DESCARGAS.iterdir()
        if archivo.is_file()
        and archivo.stem.lower() == NOMBRE_ARCHIVO_DATA.lower()
        and archivo.suffix.lower() in EXTENSIONES_PERMITIDAS
    ]

    # --------------------------------------------------------
    # No se encontró ningún archivo
    # --------------------------------------------------------

    if not archivos:
        raise FileNotFoundError(
            f"No se encontró ningún archivo llamado "
            f"'{NOMBRE_ARCHIVO_DATA}' en la carpeta Descargas.\n\n"
            f"Ruta revisada:\n{RUTA_DESCARGAS}"
        )

    # --------------------------------------------------------
    # Si existe uno solo, utilizarlo
    # --------------------------------------------------------

    if len(archivos) == 1:

        archivo_data = archivos[0]

        print("\nArchivo data encontrado:")
        print(f"  {archivo_data.name}")

        return archivo_data

    # --------------------------------------------------------
    # Si existen varios, seleccionar el más reciente
    # --------------------------------------------------------

    archivo_data = max(
        archivos,
        key=lambda archivo: archivo.stat().st_mtime
    )

    print("\nArchivos data encontrados:")

    for archivo in sorted(
        archivos,
        key=lambda archivo: archivo.stat().st_mtime,
        reverse=True
    ):

        fecha_modificacion = datetime.fromtimestamp(
            archivo.stat().st_mtime
        )

        if archivo == archivo_data:
            marca = " <-- SELECCIONADO"
        else:
            marca = ""

        print(
            f"  - {archivo.name} | "
            f"Modificado: {fecha_modificacion.strftime('%d/%m/%Y %H:%M:%S')}"
            f"{marca}"
        )

    print(
        f"\nArchivo data seleccionado automáticamente: "
        f"{archivo_data.name}"
    )

    return archivo_data


# ============================================================
# CARGAR DATA
# ============================================================

def cargar_data(archivo_data):
    """
    Carga el archivo data seleccionado.

    CSV:
        Se intenta detectar automáticamente el separador.

    Excel:
        Se utiliza read_excel().
    """

    extension = archivo_data.suffix.lower()

    print(f"\nCargando archivo: {archivo_data.name}")

    if extension == ".csv":

        data = pd.read_csv(
            archivo_data,
            sep=None,
            engine="python"
        )

    else:

        data = pd.read_excel(
            archivo_data
        )

    print(f"Registros cargados: {len(data):,}")
    print(f"Columnas encontradas: {len(data.columns)}")

    return data


# ============================================================
# VALIDAR COLUMNAS DE DATA
# ============================================================

def validar_columnas_data(data):
    """
    Verifica que el archivo data tenga las columnas necesarias
    para realizar el cruce.

    Columnas requeridas:
        - general_info.dot
        - stage
    """

    columnas_requeridas = [
        "general_info.dot",
        "stage"
    ]

    columnas_faltantes = [
        columna
        for columna in columnas_requeridas
        if columna not in data.columns
    ]

    if columnas_faltantes:

        raise ValueError(
            "El archivo data no contiene las columnas necesarias.\n\n"
            f"Columnas faltantes:\n{columnas_faltantes}\n\n"
            f"Columnas encontradas:\n{list(data.columns)}"
        )

    print("\nColumnas necesarias de data encontradas correctamente.")


# ============================================================
# PREPARAR DATA PARA EL CRUCE
# ============================================================

def preparar_data_cruce(data):
    """
    Prepara la información de data para realizar el cruce.

    Se crea una columna auxiliar:
        DOT_cruce

    Esta columna contiene el DOT normalizado.

    Si un mismo DOT aparece varias veces en data, se conserva
    únicamente el primer stage encontrado, respetando el orden
    original del archivo.

    Retorna:
        diccionario {DOT: stage}
    """

    data_cruce = data.copy()

    # --------------------------------------------------------
    # Normalizar DOT
    # --------------------------------------------------------

    data_cruce["DOT_cruce"] = (
        data_cruce["general_info.dot"]
        .apply(normalizar_dot)
    )

    # --------------------------------------------------------
    # Eliminar DOT vacíos
    # --------------------------------------------------------

    data_cruce = data_cruce[
        data_cruce["DOT_cruce"] != ""
    ].copy()

    # --------------------------------------------------------
    # Mantener el primer registro de cada DOT
    # --------------------------------------------------------

    data_cruce = data_cruce.drop_duplicates(
        subset="DOT_cruce",
        keep="first"
    )

    # --------------------------------------------------------
    # Crear diccionario DOT -> stage
    # --------------------------------------------------------

    diccionario_dot_stage = dict(
        zip(
            data_cruce["DOT_cruce"],
            data_cruce["stage"]
        )
    )

    print(
        f"\nDOT únicos disponibles para cruce: "
        f"{len(diccionario_dot_stage):,}"
    )

    return diccionario_dot_stage


# ============================================================
# RECHAZAR DUPLICADOS DENTRO DE LA MISMA BASE
# ============================================================

def rechazar_dot_repetidos(montaje, rechazos):
    """
    Busca DOT repetidos dentro de la base actual.

    Regla:
        - El primer registro de un DOT se conserva.
        - Los siguientes registros se rechazan.

    Motivo:
        'Repetido en misma base'

    Los DOT vacíos no se consideran duplicados.
    """

    # --------------------------------------------------------
    # Normalizar DOT temporalmente
    # --------------------------------------------------------

    dot_normalizado = montaje["DOT"].apply(
        normalizar_dot
    )

    # --------------------------------------------------------
    # Identificar duplicados
    #
    # keep='first':
    # el primero queda False
    # los siguientes quedan True
    # --------------------------------------------------------

    duplicados = (
        dot_normalizado != ""
    ) & dot_normalizado.duplicated(
        keep="first"
    )

    cantidad_rechazos = duplicados.sum()

    if cantidad_rechazos == 0:

        print(
            "\nNo se encontraron DOT repetidos "
            "dentro de la misma base."
        )

        return montaje, rechazos

    # --------------------------------------------------------
    # Obtener registros rechazados
    # --------------------------------------------------------

    registros_rechazados = montaje.loc[
        duplicados
    ].copy()

    registros_rechazados.insert(
        1,
        "Motivo Rechazo",
        "Repetido en misma base"
    )

    # --------------------------------------------------------
    # Agregar a rechazos
    # --------------------------------------------------------

    rechazos = pd.concat(
        [
            rechazos,
            registros_rechazados
        ],
        ignore_index=True
    )

    # --------------------------------------------------------
    # Eliminar del montaje
    # --------------------------------------------------------

    montaje = montaje.loc[
        ~duplicados
    ].copy()

    print(
        f"\nDOT repetidos rechazados: "
        f"{cantidad_rechazos:,}"
    )

    print(
        f"Registros restantes en montaje: "
        f"{len(montaje):,}"
    )

    return montaje, rechazos


# ============================================================
# CRUZAR DOT CONTRA DATA
# ============================================================

def cruzar_dot_data(
    montaje,
    rechazos,
    diccionario_dot_stage
):
    """
    Cruza los DOT de Montaje contra el archivo data.

    Si el DOT existe en data:
        - El registro se rechaza.
        - El valor de stage se utiliza como Motivo Rechazo.

    Si el DOT no existe:
        - El registro permanece en Montaje.
    """

    # --------------------------------------------------------
    # Crear columna auxiliar para el cruce
    # --------------------------------------------------------

    montaje = montaje.copy()

    montaje["DOT_cruce"] = (
        montaje["DOT"]
        .apply(normalizar_dot)
    )

    # --------------------------------------------------------
    # Determinar qué DOT aparecen en data
    # --------------------------------------------------------

    coincidencias = montaje["DOT_cruce"].isin(
        diccionario_dot_stage.keys()
    )

    cantidad_rechazos = coincidencias.sum()

    if cantidad_rechazos == 0:

        print(
            "\nNo se encontraron coincidencias "
            "entre Montaje y data."
        )

        montaje.drop(
            columns=["DOT_cruce"],
            inplace=True
        )

        return montaje, rechazos

    # --------------------------------------------------------
    # Copiar registros coincidentes
    # --------------------------------------------------------

    registros_rechazados = montaje.loc[
        coincidencias
    ].copy()

    # --------------------------------------------------------
    # Obtener stage correspondiente
    # --------------------------------------------------------

    registros_rechazados.insert(
        1,
        "Motivo Rechazo",
        registros_rechazados["DOT_cruce"].map(
            diccionario_dot_stage
        )
    )

    # --------------------------------------------------------
    # Eliminar columna auxiliar de los rechazos
    # --------------------------------------------------------

    registros_rechazados.drop(
        columns=["DOT_cruce"],
        inplace=True
    )

    # --------------------------------------------------------
    # Agregar a rechazos
    # --------------------------------------------------------

    rechazos = pd.concat(
        [
            rechazos,
            registros_rechazados
        ],
        ignore_index=True
    )

    # --------------------------------------------------------
    # Mantener únicamente los que NO coincidieron
    # --------------------------------------------------------

    montaje = montaje.loc[
        ~coincidencias
    ].copy()

    # --------------------------------------------------------
    # Eliminar columna auxiliar
    # --------------------------------------------------------

    montaje.drop(
        columns=["DOT_cruce"],
        inplace=True
    )

    print(
        f"\nCoincidencias con data rechazadas: "
        f"{cantidad_rechazos:,}"
    )

    print(
        f"Registros restantes en montaje: "
        f"{len(montaje):,}"
    )

    return montaje, rechazos


# ============================================================
# ELIMINAR COLUMNAS AUXILIARES
# ============================================================

def eliminar_columnas_auxiliares(montaje):
    """
    Elimina cualquier columna auxiliar utilizada durante
    el proceso de cruce.
    """

    columnas_auxiliares = [
        "DOT_cruce"
    ]

    columnas_a_eliminar = [
        columna
        for columna in columnas_auxiliares
        if columna in montaje.columns
    ]

    if columnas_a_eliminar:

        montaje = montaje.drop(
            columns=columnas_a_eliminar
        )

    return montaje


# ============================================================
# PROCESO COMPLETO DE CRUCES
# ============================================================

def procesar_cruces(montaje, rechazos, archivo_data=None):
    """
    Ejecuta todo el proceso relacionado con DOT:

    1. Validar formato de DOT y rechazar repetidos dentro de la misma base.
    2. Buscar automáticamente el archivo data más reciente.
    3. Cargar data.
    4. Validar columnas.
    5. Preparar el diccionario DOT -> stage.
    6. Cruzar Montaje contra data.
    7. Agregar coincidencias a Rechazos.
    8. Eliminar columnas auxiliares.

    Retorna:
        montaje
        rechazos
    """

    print("\n")
    print("=" * 60)
    print("INICIO DEL PROCESO DE CRUCES")
    print("=" * 60)

    # ========================================================
    # PASO 1
    # DOT REPETIDOS EN LA MISMA BASE
    # ========================================================

    print("\n")
    print("-" * 60)
    print("PASO 1: VALIDAR FORMATO Y DUPLICADOS DE DOT")
    print("-" * 60)

    montaje, rechazos = validar_dot(montaje, rechazos)

    montaje, rechazos = rechazar_dot_repetidos(
        montaje,
        rechazos
    )

    # ========================================================
    # PASO 2
    # BUSCAR DATA
    # ========================================================

    print("\n")
    print("-" * 60)
    print("PASO 2: BUSCAR ARCHIVO DATA")
    print("-" * 60)

    archivo_data = (
        buscar_archivo_data() if archivo_data is None
        else validar_archivo_entrada(archivo_data)
    )

    # ========================================================
    # PASO 3
    # CARGAR DATA
    # ========================================================

    print("\n")
    print("-" * 60)
    print("PASO 3: CARGAR DATA")
    print("-" * 60)

    data = cargar_data(
        archivo_data
    )

    # ========================================================
    # PASO 4
    # VALIDAR COLUMNAS
    # ========================================================

    print("\n")
    print("-" * 60)
    print("PASO 4: VALIDAR COLUMNAS DE DATA")
    print("-" * 60)

    validar_columnas_data(
        data
    )

    # ========================================================
    # PASO 5
    # PREPARAR DATA PARA EL CRUCE
    # ========================================================

    print("\n")
    print("-" * 60)
    print("PASO 5: PREPARAR DATA PARA EL CRUCE")
    print("-" * 60)

    diccionario_dot_stage = preparar_data_cruce(
        data
    )

    # ========================================================
    # PASO 6
    # CRUZAR DOT
    # ========================================================

    print("\n")
    print("-" * 60)
    print("PASO 6: CRUZAR DOT CONTRA DATA")
    print("-" * 60)

    montaje, rechazos = cruzar_dot_data(
        montaje,
        rechazos,
        diccionario_dot_stage
    )

    # ========================================================
    # PASO 7
    # LIMPIAR COLUMNAS AUXILIARES
    # ========================================================

    montaje = eliminar_columnas_auxiliares(
        montaje
    )

    # ========================================================
    # RESUMEN
    # ========================================================

    print("\n")
    print("=" * 60)
    print("FIN DEL PROCESO DE CRUCES")
    print("=" * 60)

    print(
        f"Registros finales en Montaje: "
        f"{len(montaje):,}"
    )

    print(
        f"Registros acumulados en Rechazos: "
        f"{len(rechazos):,}"
    )

    print("=" * 60)

    return montaje, rechazos


# ============================================================
# PRUEBA DIRECTA DEL MÓDULO
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 60)
    print("PRUEBA DEL MODULO CRUCES")
    print("=" * 60)

    archivo_data = buscar_archivo_data()

    print("\nArchivo seleccionado:")
    print(archivo_data)

    data = cargar_data(
        archivo_data
    )

    validar_columnas_data(
        data
    )

    diccionario = preparar_data_cruce(
        data
    )

    print(
        f"\nDiccionario generado correctamente."
    )

    print(
        f"DOT disponibles: "
        f"{len(diccionario):,}"
    )
