# ============================================================
# REPRESENTANTES - TRUKING
# ============================================================
#
# Este módulo controla:
#
# 1. Validación de representante vacío.
# 2. Validación de representante contra FILTROS ESPAÑOL.
# 3. Limpieza de los registros que pasan la validación latina.
#
# ============================================================


# ============================================================
# 1. IMPORTACIONES
# ============================================================

import re

import unicodedata

import pandas as pd

from config import (
    RUTA_FILTROS,
    EXTENSIONES_PERMITIDAS,
    NOMBRE_ARCHIVO_FILTROS
)

from depuracion.limpieza import limpiar_montaje


# ============================================================
# 2. BUSCAR FILTROS ESPAÑOL
# ============================================================

def buscar_archivo_filtros():

    archivos_filtros = [
        archivo
        for archivo in RUTA_FILTROS.iterdir()
        if (
            archivo.is_file()
            and archivo.stem.lower() == NOMBRE_ARCHIVO_FILTROS.lower()
            and archivo.suffix.lower() in EXTENSIONES_PERMITIDAS
        )
    ]


    # ========================================================
    # VALIDAR QUE EXISTA UN ARCHIVO
    # ========================================================

    if len(archivos_filtros) == 0:

        raise FileNotFoundError(
            "No se encontró el archivo "
            "'FILTROS ESPAÑOL' en la ruta configurada:\n"
            f"{RUTA_FILTROS}"
        )


    # ========================================================
    # VALIDAR QUE SOLAMENTE EXISTA UNO
    # ========================================================

    if len(archivos_filtros) > 1:

        nombres = "\n".join(
            archivo.name
            for archivo in archivos_filtros
        )

        raise ValueError(
            "Se encontraron varios archivos "
            "'FILTROS ESPAÑOL' en la ruta:\n"
            f"{RUTA_FILTROS}\n\n"
            "Archivos encontrados:\n"
            f"{nombres}\n\n"
            "Debe existir solamente uno."
        )


    return archivos_filtros[0]


# ============================================================
# 3. QUITAR TILDES
# ============================================================

def quitar_tildes(texto):

    texto = unicodedata.normalize(
        "NFD",
        texto
    )


    texto = "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )


    return texto


# ============================================================
# 4. NORMALIZAR NOMBRE PARA VALIDACIÓN
# ============================================================

def normalizar_nombre(texto):

    if pd.isna(texto):

        return ""


    texto = str(texto)


    # --------------------------------------------------------
    # Quitar tildes.
    # --------------------------------------------------------

    texto = quitar_tildes(
        texto
    )


    # --------------------------------------------------------
    # Convertir a minúsculas.
    # --------------------------------------------------------

    texto = texto.lower()


    # --------------------------------------------------------
    # Reemplazar caracteres especiales por espacios.
    # --------------------------------------------------------

    texto = re.sub(
        r"[^a-zA-Z0-9\s]",
        " ",
        texto
    )


    # --------------------------------------------------------
    # Eliminar espacios duplicados.
    # --------------------------------------------------------

    texto = " ".join(
        texto.split()
    )


    return texto


# ============================================================
# 5. CARGAR FILTROS ESPAÑOL
# ============================================================
#
# IMPORTANTE:
#
# Los valores del archivo FILTROS ESPAÑOL también se
# normalizan utilizando normalizar_nombre().
#
# De esta manera:
#
#     José
#
# y:
#
#     jose
#
# se consideran equivalentes.
#
# ============================================================

def cargar_filtros():

    archivo_filtros = buscar_archivo_filtros()


    print("\nArchivo FILTROS ESPAÑOL:")

    print(archivo_filtros)


    # ========================================================
    # LEER ARCHIVO
    # ========================================================

    if archivo_filtros.suffix.lower() == ".csv":

        filtros = pd.read_csv(
            archivo_filtros,
            header=None,
            dtype=str
        )

    else:

        filtros = pd.read_excel(
            archivo_filtros,
            header=None,
            dtype=str
        )


    # ========================================================
    # VALIDAR QUE EXISTA AL MENOS UNA COLUMNA
    # ========================================================

    if filtros.shape[1] == 0:

        raise ValueError(
            "El archivo FILTROS ESPAÑOL no contiene columnas."
        )


    # ========================================================
    # TOMAR PRIMERA COLUMNA
    # ========================================================

    filtros = filtros.iloc[:, 0].copy()


    # ========================================================
    # ELIMINAR VALORES VACÍOS
    # ========================================================

    filtros = filtros.dropna()


    # ========================================================
    # NORMALIZAR CADA NOMBRE
    # ========================================================

    filtros = filtros.apply(
        normalizar_nombre
    )


    # ========================================================
    # ELIMINAR VALORES QUE QUEDARON VACÍOS
    # ========================================================

    filtros = filtros[
        filtros != ""
    ]


    # ========================================================
    # CONVERTIR EN CONJUNTO
    # ========================================================

    filtros_set = set(
        filtros
    )


    print(
        "\nNombres disponibles en FILTROS ESPAÑOL:",
        len(filtros_set)
    )


    return filtros_set


# ============================================================
# 6. VALIDAR REPRESENTANTE
# ============================================================
#
# La función ahora permite definir cuántas coincidencias
# mínimas se necesitan.
#
# Ejemplo con minimo_coincidencias = 1:
#
#     JUAN TRUCKING
#
#     JUAN -> 1 coincidencia
#
#     Resultado: True
#
#
# Ejemplo con minimo_coincidencias = 2:
#
#     JUAN CARLOS TRUCKING
#
#     JUAN   -> 1
#     CARLOS -> 2
#
#     Resultado: True
#
#
# Las coincidencias pueden repetirse.
#
# Ejemplo:
#
#     JUAN JUAN TRUCKING
#
#     JUAN -> 1
#     JUAN -> 2
#
#     Resultado con mínimo 2: True
#
# ============================================================

def representante_valido(
    texto,
    filtros_set,
    minimo_coincidencias=1
):

    # --------------------------------------------------------
    # Validar que el mínimo solicitado sea válido.
    # --------------------------------------------------------

    if minimo_coincidencias < 1:

        raise ValueError(
            "El mínimo de coincidencias debe ser "
            "mayor o igual a 1."
        )


    # --------------------------------------------------------
    # Normalizar el representante.
    # --------------------------------------------------------

    texto_normalizado = normalizar_nombre(
        texto
    )


    # --------------------------------------------------------
    # Si no existe texto, no es válido.
    # --------------------------------------------------------

    if texto_normalizado == "":

        return False


    # --------------------------------------------------------
    # Separar el representante en palabras.
    # --------------------------------------------------------

    palabras = texto_normalizado.split()


    # --------------------------------------------------------
    # Contar coincidencias.
    #
    # IMPORTANTE:
    #
    # Cada aparición cuenta.
    #
    # Por ejemplo:
    #
    #     JUAN JUAN CARLOS
    #
    # genera:
    #
    #     JUAN   -> 1
    #     JUAN   -> 2
    #     CARLOS -> 3
    #
    # No utilizamos un conjunto para las palabras del
    # representante porque queremos conservar las
    # repeticiones.
    # --------------------------------------------------------

    coincidencias = 0


    for palabra in palabras:

        if palabra in filtros_set:

            coincidencias += 1


            # ------------------------------------------------
            # Si ya alcanzamos el mínimo requerido,
            # podemos detener la búsqueda.
            # ------------------------------------------------

            if coincidencias >= minimo_coincidencias:

                return True


    # --------------------------------------------------------
    # No se alcanzó el mínimo requerido.
    # --------------------------------------------------------

    return False


# ============================================================
# 7. VALIDAR REPRESENTANTE VACÍO
# ============================================================

def rechazar_sin_representante(
    montaje,
    rechazos
):

    # --------------------------------------------------------
    # Identificar valores vacíos.
    # --------------------------------------------------------

    representante = (
        montaje["Company_Rep1"]
        .astype("string")
        .str.strip()
    )


    mascara_vacia = (
        representante.isna()
        |
        (representante == "")
    )


    # --------------------------------------------------------
    # Extraer registros rechazados.
    # --------------------------------------------------------

    registros_rechazados = montaje.loc[
        mascara_vacia
    ].copy()


    # --------------------------------------------------------
    # Agregar motivo únicamente si existen rechazados.
    # --------------------------------------------------------

    if len(registros_rechazados) > 0:

        registros_rechazados.insert(
            1,
            "Motivo Rechazo",
            "Sin representante"
        )


        rechazos = pd.concat(
            [
                rechazos,
                registros_rechazados
            ],
            ignore_index=True
        )


    # --------------------------------------------------------
    # Dejar solamente registros con representante.
    # --------------------------------------------------------

    montaje = montaje.loc[
        ~mascara_vacia
    ].copy()


    print(
        "\nRegistros rechazados por falta de representante:",
        mascara_vacia.sum()
    )


    return montaje, rechazos


# ============================================================
# 8. VALIDAR NOMBRES LATINOS
# ============================================================

def validar_nombres_latinos(
    montaje,
    rechazos,
    minimo_coincidencias=1
):

    # --------------------------------------------------------
    # Cargar nombres válidos.
    # --------------------------------------------------------

    filtros_set = cargar_filtros()


    # --------------------------------------------------------
    # Validar Company_Rep1.
    # --------------------------------------------------------

    mascara_valida = montaje[
        "Company_Rep1"
    ].apply(
        lambda valor: representante_valido(
            valor,
            filtros_set,
            minimo_coincidencias
        )
    )


    # --------------------------------------------------------
    # Extraer no reconocidos.
    # --------------------------------------------------------

    registros_rechazados = montaje.loc[
        ~mascara_valida
    ].copy()


    # --------------------------------------------------------
    # Agregar motivo.
    # --------------------------------------------------------

    if len(registros_rechazados) > 0:

        registros_rechazados.insert(
            1,
            "Motivo Rechazo",
            "Bilingue"
        )


        # ----------------------------------------------------
        # Agregar al final de Rechazos.
        # ----------------------------------------------------

        rechazos = pd.concat(
            [
                rechazos,
                registros_rechazados
            ],
            ignore_index=True
        )


    # --------------------------------------------------------
    # Mantener solamente nombres reconocidos.
    # --------------------------------------------------------

    montaje = montaje.loc[
        mascara_valida
    ].copy()


    print(
        "\nRegistros revisados para nombre latino:",
        len(mascara_valida)
    )


    print(
        "Registros rechazados por nombre no reconocido:",
        (~mascara_valida).sum()
    )


    print(
        "Registros restantes en Montaje:",
        len(montaje)
    )


    print(
        "Registros acumulados en Rechazos:",
        len(rechazos)
    )


    return montaje, rechazos


# ============================================================
# 9. PROCESAR REPRESENTANTES
# ============================================================

def procesar_representantes(
    montaje,
    rechazos
):

    montaje, rechazos = rechazar_sin_representante(
        montaje,
        rechazos
    )


    return montaje, rechazos


# ============================================================
# 10. VALIDACIÓN LATINA + LIMPIEZA
# ============================================================

def procesar_nombres_latinos(
    montaje,
    rechazos,
    minimo_coincidencias=1
):

    # ========================================================
    # VALIDAR NOMBRES
    # ========================================================

    montaje, rechazos = validar_nombres_latinos(
        montaje,
        rechazos,
        minimo_coincidencias
    )


    # ========================================================
    # LIMPIAR SOLAMENTE LOS REGISTROS APROBADOS
    # ========================================================

    montaje = limpiar_montaje(
        montaje
    )


    return montaje, rechazos


# ============================================================
# 11. PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("\n")

    print("=" * 60)

    print("PRUEBA DEL MÓDULO REPRESENTANTES")

    print("=" * 60)


    filtros_set = cargar_filtros()


    ejemplos = [
        "Juan",
        "Maria",
        "Ana",
        "Anabel",
        "ABC JUAN TRUCKING",
        "José",
        "JOSE",
        "Juan Juan",
        "Carlos Juan",
        "Carlos Juan Trucking"
    ]


    print("\nEjemplos:")


    for ejemplo in ejemplos:

        resultado_1 = representante_valido(
            ejemplo,
            filtros_set,
            minimo_coincidencias=1
        )


        resultado_2 = representante_valido(
            ejemplo,
            filtros_set,
            minimo_coincidencias=2
        )


        print(
            f"{ejemplo} -> "
            f"1 coincidencia: {resultado_1} | "
            f"2 coincidencias: {resultado_2}"
        )