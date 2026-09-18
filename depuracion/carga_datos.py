# ============================================================
# CARGA DE DATOS - DEPURADOR DE BASES TRUKING
# ============================================================
#
# Este módulo se encarga de preparar la base para iniciar
# el proceso de depuración.
#
# Responsabilidades:
#
# 1. Recibir la ruta del archivo seleccionado.
# 2. Validar que el archivo exista.
# 3. Validar la extensión del archivo.
# 4. Cargar el archivo.
# 5. Validar/preparar las columnas necesarias.
# 6. Crear Montaje.
# 7. Agregar Fecha Montaje.
# 8. Crear Rechazos.
# 9. Agregar Motivo Rechazo.
#
# IMPORTANTE:
#
# La selección del archivo NO se realiza desde este módulo.
#
# El archivo es seleccionado desde:
#
#     interfaz/archivos.py
#
# y posteriormente la ruta es enviada a:
#
#     cargar_y_preparar_datos()
#
# ============================================================


# ============================================================
# 1. IMPORTAR LIBRERÍAS
# ============================================================

import pandas as pd

from datetime import date

from pathlib import Path


# ============================================================
# 2. IMPORTAR CONFIGURACIÓN
# ============================================================

from config import (
    EXTENSIONES_PERMITIDAS
)


# ============================================================
# 3. DEFINIR COLUMNAS NECESARIAS
# ============================================================
#
# Estas son las columnas que el proceso de depuración
# necesita trabajar.
#
# Si alguna no existe en la base recibida, se creará vacía.
#
# El orden también es importante porque posteriormente
# trabajaremos con estas mismas columnas.
#
# ============================================================

COLUMNAS_NECESARIAS = [
    "DOT",
    "Legal_Name",
    "Phone",
    "Cell_Num",
    "Business_State",
    "Email",
    "Company_Rep1",
    "Years_In_Business",
    "Power_Units",
    "Insurer",
    "Policy_Effective_Date",
    "Policy_Cancellation_Date"
]


# ============================================================
# 4. VALIDAR ARCHIVO DE ENTRADA
# ============================================================

def validar_archivo_entrada(archivo):
    # --------------------------------------------------------
    # Convertir la ruta recibida en objeto Path
    # --------------------------------------------------------

    archivo = Path(archivo)


    # ========================================================
    # VALIDAR QUE EL ARCHIVO EXISTA
    # ========================================================

    if not archivo.exists():

        raise FileNotFoundError(
            "El archivo seleccionado no existe.\n\n"
            f"Archivo:\n{archivo}"
        )


    # ========================================================
    # VALIDAR QUE REALMENTE SEA UN ARCHIVO
    # ========================================================

    if not archivo.is_file():

        raise ValueError(
            "La ruta seleccionada no corresponde a un archivo.\n\n"
            f"Ruta:\n{archivo}"
        )


    # ========================================================
    # VALIDAR EXTENSIÓN
    # ========================================================

    if archivo.suffix.lower() not in EXTENSIONES_PERMITIDAS:

        raise ValueError(
            "El archivo seleccionado tiene una extensión "
            "que no está permitida.\n\n"
            f"Extensión encontrada: {archivo.suffix}\n\n"
            "Extensiones permitidas:\n"
            f"{', '.join(EXTENSIONES_PERMITIDAS)}"
        )


    # ========================================================
    # RETORNAR ARCHIVO VALIDADO
    # ========================================================

    return archivo


# ============================================================
# 5. CARGAR EL ARCHIVO
# ============================================================

def cargar_archivo(archivo):
   
    # --------------------------------------------------------
    # Si el archivo es CSV
    # --------------------------------------------------------

    if archivo.suffix.lower() == ".csv":

        base = pd.read_csv(
            archivo
        )


    # --------------------------------------------------------
    # Si el archivo es Excel
    # --------------------------------------------------------

    else:

        base = pd.read_excel(
            archivo
        )


    return base


# ============================================================
# 6. PREPARAR LA BASE
# ============================================================

def preparar_base(base):


    # ========================================================
    # 6.1. CREAR COLUMNAS FALTANTES
    # ========================================================

    for columna in COLUMNAS_NECESARIAS:

        if columna not in base.columns:

            base[columna] = pd.NA


    # ========================================================
    # 6.2. CONSERVAR ÚNICAMENTE LAS COLUMNAS NECESARIAS
    # ========================================================

    base = base[
        COLUMNAS_NECESARIAS
    ]


    return base


# ============================================================
# 7. CREAR MONTAJE
# ============================================================

def crear_montaje(base):
    montaje = base.copy()


    return montaje


# ============================================================
# 8. OBTENER FECHA DE MONTAJE
# ============================================================

def obtener_fecha_montaje():
    

    fecha_montaje = date.today().strftime(
        "%d/%m/%Y"
    )


    return fecha_montaje


# ============================================================
# 9. AGREGAR FECHA DE MONTAJE
# ============================================================

def agregar_fecha_montaje(montaje,fecha_montaje):
   
    montaje.insert(
        0,
        "Fecha Montaje",
        fecha_montaje
    )


    return montaje


# ============================================================
# 10. CREAR RECHAZOS
# ============================================================

def crear_rechazos(montaje):
    rechazos = pd.DataFrame(
        columns=montaje.columns
    )


    return rechazos


# ============================================================
# 11. AGREGAR MOTIVO DE RECHAZO
# ============================================================

def agregar_motivo_rechazo(rechazos):
    

    rechazos.insert(
        1,
        "Motivo Rechazo",
        pd.NA
    )


    return rechazos


# ============================================================
# 12. FUNCIÓN PRINCIPAL DEL MÓDULO
# ============================================================

def cargar_y_preparar_datos(archivo_origen):
    
    # ========================================================
    # 12.1. VALIDAR ARCHIVO
    # ========================================================

    archivo = validar_archivo_entrada(archivo_origen)


    # ========================================================
    # 12.2. CARGAR ARCHIVO
    # ========================================================

    base = cargar_archivo(archivo)


    # ========================================================
    # 12.3. MOSTRAR INFORMACIÓN
    # ========================================================

    print(
        f"\nArchivo cargado: {archivo.name}"
    )

    print(
        f"Ruta del archivo: {archivo}"
    )


    # ========================================================
    # 12.4. PREPARAR BASE
    # ========================================================

    base = preparar_base(base)


    # ========================================================
    # 12.5. CREAR MONTAJE
    # ========================================================

    montaje = crear_montaje(base)


    # ========================================================
    # 12.6. OBTENER FECHA DE MONTAJE
    # ========================================================

    fecha_montaje = obtener_fecha_montaje()


    # ========================================================
    # 12.7. AGREGAR FECHA DE MONTAJE
    # ========================================================

    montaje = agregar_fecha_montaje(
        montaje,
        fecha_montaje
    )


    # ========================================================
    # 12.8. CREAR RECHAZOS
    # ========================================================

    rechazos = crear_rechazos(
        montaje
    )


    # ========================================================
    # 12.9. AGREGAR MOTIVO DE RECHAZO
    # ========================================================

    rechazos = agregar_motivo_rechazo(
        rechazos
    )


    # ========================================================
    # 12.10. MOSTRAR INFORMACIÓN
    # ========================================================

    print(
        f"\nRegistros cargados: {len(base)}"
    )

    print(
        f"Registros iniciales en Montaje: {len(montaje)}"
    )

    print(
        f"Registros iniciales en Rechazos: {len(rechazos)}"
    )


    # ========================================================
    # 12.11. RETORNAR RESULTADOS
    # ========================================================

    return (
        base,
        montaje,
        rechazos,
        archivo,
        fecha_montaje
    )


