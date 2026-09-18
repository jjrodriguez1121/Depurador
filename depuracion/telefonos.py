# ============================================================
# TELÉFONOS - DEPURADOR DE BASES TRUKING
# ============================================================
#
# Este módulo contiene toda la lógica relacionada con el
# procesamiento y validación de teléfonos.
#
# PROCESO:
#
# 1. Normalizar Phone.
# 2. Normalizar Cell_Num.
# 3. Validar Phone.
# 4. Validar Cell_Num.
# 5. Utilizar Cell_Num como respaldo.
# 6. Rechazar registros sin teléfono válido.
# 7. Agregar el prefijo 9 al Phone válido.
#
# IMPORTANTE:
#
# Este módulo recibe los DataFrames:
#
#     montaje
#     rechazos
#
# y devuelve nuevamente:
#
#     montaje
#     rechazos
#
# No carga archivos ni genera el Excel.
# ============================================================


# ============================================================
# 1. IMPORTAR LIBRERÍAS
# ============================================================

import pandas as pd


# ============================================================
# 2. NORMALIZAR TELÉFONO
# ============================================================

def normalizar_telefono(valor):
    """
    Normaliza un número de teléfono.

    Reglas:

    1. Si el valor está vacío, devuelve cadena vacía.
    2. Convierte el valor a texto.
    3. Elimina espacios al principio y al final.
    4. Elimina ".0" cuando proviene de Excel.
    5. Conserva únicamente los dígitos.

    Ejemplos:

        3001234567
        ↓
        "3001234567"

        "300 123 4567"
        ↓
        "3001234567"

        3001234567.0
        ↓
        "3001234567"

        "(300) 123-4567"
        ↓
        "3001234567"

        NaN
        ↓
        ""
    """

    # --------------------------------------------------------
    # Si el valor está vacío, devolvemos una cadena vacía.
    # --------------------------------------------------------

    if pd.isna(valor):

        return ""


    # --------------------------------------------------------
    # Convertir a texto y quitar espacios exteriores.
    # --------------------------------------------------------

    valor = str(valor).strip()


    # --------------------------------------------------------
    # Eliminar ".0" al final.
    # --------------------------------------------------------

    if valor.endswith(".0"):

        valor = valor[:-2]


    # --------------------------------------------------------
    # Conservar únicamente los dígitos.
    #
    # Ejemplo:
    #
    # "(300) 123-4567"
    #
    # se convierte en:
    #
    # "3001234567"
    # --------------------------------------------------------

    valor = "".join(
        caracter
        for caracter in valor
        if caracter.isdigit()
    )


    return valor


# ============================================================
# 3. VALIDAR TELÉFONO
# ============================================================

def telefono_valido(telefono):
   
    return (
        pd.notna(telefono)
        and len(str(telefono)) == 10
        and str(telefono).isdigit()
    )


# ============================================================
# 4. NORMALIZAR COLUMNAS TELEFÓNICAS
# ============================================================

def normalizar_telefonos(montaje):
    """
    Normaliza las columnas Phone y Cell_Num.

    No realiza todavía ningún rechazo.

    Únicamente prepara los valores para la validación.
    """

    # --------------------------------------------------------
    # Normalizar Phone.
    # --------------------------------------------------------

    montaje["Phone"] = montaje["Phone"].apply(
        normalizar_telefono
    )


    # --------------------------------------------------------
    # Normalizar Cell_Num.
    # --------------------------------------------------------

    montaje["Cell_Num"] = montaje["Cell_Num"].apply(
        normalizar_telefono
    )


    return montaje


# ============================================================
# 5. UTILIZAR CELL_NUM COMO RESPALDO
# ============================================================

def utilizar_cell_como_respaldo(montaje):
    """
    Utiliza Cell_Num como respaldo cuando Phone no es válido.

    Regla:

        Si Phone no es válido
        Y
        Cell_Num es válido

        entonces:

        Phone = Cell_Num

    Cell_Num NO se modifica.

    Ejemplo:

        Phone:
            12345

        Cell_Num:
            3001234567

        Resultado:

        Phone:
            3001234567

        Cell_Num:
            3001234567
    """

    # --------------------------------------------------------
    # Crear condición para Phone inválido.
    # --------------------------------------------------------

    phone_invalido = ~montaje["Phone"].apply(
        telefono_valido
    )


    # --------------------------------------------------------
    # Crear condición para Cell_Num válido.
    # --------------------------------------------------------

    cell_valido = montaje["Cell_Num"].apply(
        telefono_valido
    )


    # --------------------------------------------------------
    # Ambas condiciones deben cumplirse.
    # --------------------------------------------------------

    usar_cell = (
        phone_invalido
        & cell_valido
    )


    # --------------------------------------------------------
    # Copiar Cell_Num sobre Phone.
    # --------------------------------------------------------

    montaje.loc[
        usar_cell,
        "Phone"
    ] = montaje.loc[
        usar_cell,
        "Cell_Num"
    ]


    return montaje


# ============================================================
# 6. RECHAZAR REGISTROS SIN TELÉFONO
# ============================================================

def rechazar_sin_telefono(
    montaje,
    rechazos
):
    """
    Rechaza los registros que no tienen ningún teléfono válido.

    Condición:

        Phone inválido
        Y
        Cell_Num inválido

    Motivo:

        "Sin teléfono"

    Los registros rechazados se agregan al DataFrame
    rechazos y posteriormente se eliminan de montaje.
    """

    # --------------------------------------------------------
    # Validar Phone.
    # --------------------------------------------------------

    phone_valido = montaje["Phone"].apply(
        telefono_valido
    )


    # --------------------------------------------------------
    # Validar Cell_Num.
    # --------------------------------------------------------

    cell_valido = montaje["Cell_Num"].apply(
        telefono_valido
    )


    # --------------------------------------------------------
    # Un registro no tiene teléfono cuando ninguno
    # de los dos campos es válido.
    # --------------------------------------------------------

    sin_telefono = (
        ~phone_valido
        & ~cell_valido
    )


    # --------------------------------------------------------
    # Obtener registros rechazados.
    # --------------------------------------------------------

    registros_rechazados = montaje.loc[
        sin_telefono
    ].copy()


    # --------------------------------------------------------
    # Agregar motivo.
    #
    # La estructura de rechazos ya contiene:
    #
    # Fecha Montaje
    # Motivo Rechazo
    # ...
    #
    # Por lo tanto, únicamente debemos asignar el motivo
    # en la columna correspondiente.
    # --------------------------------------------------------

    registros_rechazados.insert(
        1,
        "Motivo Rechazo",
        "Sin teléfono"
    )


    # --------------------------------------------------------
    # Acumular los registros en rechazos.
    # --------------------------------------------------------

    rechazos = pd.concat(
        [
            rechazos,
            registros_rechazados
        ],
        ignore_index=True
    )


    # --------------------------------------------------------
    # Eliminar los registros rechazados de montaje.
    # --------------------------------------------------------

    montaje = montaje.loc[
        ~sin_telefono
    ].copy()


    return montaje, rechazos


# ============================================================
# 7. AGREGAR PREFIJO 9
# ============================================================

def agregar_prefijo_9(montaje):
    """
    Agrega el prefijo 9 a los teléfonos válidos de Phone.

    IMPORTANTE:

    La validación se realiza antes con 10 dígitos.

    Después de esta función:

        3001234567
        ↓
        93001234567

    Solamente se modifica:

        Phone

    Cell_Num permanece sin modificar.
    """

    # --------------------------------------------------------
    # Crear máscara para identificar teléfonos válidos.
    # --------------------------------------------------------

    phone_valido = montaje["Phone"].apply(
        telefono_valido
    )


    # --------------------------------------------------------
    # Agregar prefijo 9 únicamente a los teléfonos válidos.
    # --------------------------------------------------------

    montaje.loc[
        phone_valido,
        "Phone"
    ] = (
        "9"
        + montaje.loc[
            phone_valido,
            "Phone"
        ].astype(str)
    )


    return montaje


# ============================================================
# 8. PROCESAR TELÉFONOS
# ============================================================

def procesar_telefonos(
    montaje,
    rechazos
):
    """
    Ejecuta todo el proceso de teléfonos en el orden correcto.

    ORDEN:

        1. Normalizar teléfonos.
        2. Utilizar Cell_Num como respaldo.
        3. Rechazar sin teléfono.
        4. Agregar prefijo 9.

    Retorna:

        montaje
        rechazos
    """

    # ========================================================
    # PASO 1
    # NORMALIZAR TELÉFONOS
    # ========================================================

    montaje = normalizar_telefonos(
        montaje
    )


    # ========================================================
    # PASO 2
    # UTILIZAR CELL_NUM COMO RESPALDO
    # ========================================================

    montaje = utilizar_cell_como_respaldo(
        montaje
    )


    # ========================================================
    # PASO 3
    # RECHAZAR SIN TELÉFONO
    # ========================================================

    montaje, rechazos = rechazar_sin_telefono(
        montaje,
        rechazos
    )


    # ========================================================
    # PASO 4
    # AGREGAR PREFIJO 9
    # ========================================================

    montaje = agregar_prefijo_9(
        montaje
    )


    # ========================================================
    # RETORNAR RESULTADOS
    # ========================================================

    return montaje, rechazos