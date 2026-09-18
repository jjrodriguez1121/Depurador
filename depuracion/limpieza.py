# ============================================================
# LIMPIEZA DE DATOS - TRUKING
# ============================================================
#
# Este módulo limpia únicamente los registros que ya pasaron
# todas las depuraciones.
#
# Campos:
#
# - Legal_Name
# - Company_Rep1
# - Insurer
# - Email
#
# ============================================================


# ============================================================
# 1. IMPORTACIONES
# ============================================================

import re

import unicodedata

import pandas as pd


# ============================================================
# 2. QUITAR TILDES
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
# 3. LIMPIAR CAMPOS DE TEXTO
# ============================================================

def limpiar_campo_texto(texto):

    # --------------------------------------------------------
    # Si está vacío, devolvemos cadena vacía.
    # --------------------------------------------------------

    if pd.isna(texto):

        return ""


    # --------------------------------------------------------
    # Convertimos a texto.
    # --------------------------------------------------------

    texto = str(texto)


    # --------------------------------------------------------
    # Quitamos tildes.
    # --------------------------------------------------------

    texto = quitar_tildes(
        texto
    )


    # --------------------------------------------------------
    # IMPORTANTE:
    #
    # "&" se convierte en "Y".
    #
    # Ejemplo:
    #
    # A & A GLOBAL FREIGHT LLC
    #
    # queda:
    #
    # A Y A GLOBAL FREIGHT LLC
    #
    # --------------------------------------------------------

    texto = texto.replace(
        "&",
        "Y"
    )


    # --------------------------------------------------------
    # Los guiones se convierten en espacio.
    # --------------------------------------------------------

    texto = texto.replace(
        "-",
        " "
    )


    # --------------------------------------------------------
    # Los demás caracteres especiales se convierten en
    # espacios.
    #
    # Esto se ejecuta DESPUÉS de convertir & en Y.
    #
    # Por eso el carácter & ya no se pierde.
    # --------------------------------------------------------

    texto = re.sub(
        r"[^a-zA-Z0-9\s]",
        " ",
        texto
    )


    # --------------------------------------------------------
    # Eliminamos espacios duplicados.
    # --------------------------------------------------------

    texto = " ".join(
        texto.split()
    )


    return texto


# ============================================================
# 4. LIMPIAR EMAIL
# ============================================================

def limpiar_email(valor):

    # --------------------------------------------------------
    # Si está vacío.
    # --------------------------------------------------------

    if pd.isna(valor):

        return ""


    # --------------------------------------------------------
    # Convertimos a texto.
    # --------------------------------------------------------

    correo = str(valor).strip()


    # --------------------------------------------------------
    # IMPORTANTE:
    #
    # Si existen varios correos separados por ";",
    # conservamos SOLAMENTE EL PRIMERO.
    #
    # Ejemplo:
    #
    # juan@gmail.com;maria@gmail.com
    #
    # queda:
    #
    # juan@gmail.com
    #
    # --------------------------------------------------------

    correo = correo.split(
        ";",
        1
    )[0]


    # --------------------------------------------------------
    # Quitamos espacios.
    # --------------------------------------------------------

    correo = correo.strip()


    # --------------------------------------------------------
    # Cambiamos coma por punto.
    # --------------------------------------------------------

    correo = correo.replace(
        ",",
        "."
    )


    # --------------------------------------------------------
    # Eliminamos espacios internos.
    # --------------------------------------------------------

    correo = re.sub(
        r"\s+",
        "",
        correo
    )


    return correo


# ============================================================
# 5. LIMPIAR LEGAL_NAME
# ============================================================

def limpiar_legal_name(montaje):

    montaje = montaje.copy()


    montaje["Legal_Name"] = montaje[
        "Legal_Name"
    ].apply(
        limpiar_campo_texto
    )


    return montaje


# ============================================================
# 6. LIMPIAR COMPANY_REP1
# ============================================================

def limpiar_company_rep1(montaje):

    montaje = montaje.copy()


    montaje["Company_Rep1"] = montaje[
        "Company_Rep1"
    ].apply(
        limpiar_campo_texto
    )


    return montaje


# ============================================================
# 7. LIMPIAR INSURER
# ============================================================

def limpiar_insurer(montaje):

    montaje = montaje.copy()


    montaje["Insurer"] = montaje[
        "Insurer"
    ].apply(
        limpiar_campo_texto
    )


    return montaje


# ============================================================
# 8. LIMPIAR EMAILS
# ============================================================

def limpiar_emails(montaje):

    montaje = montaje.copy()


    montaje["Email"] = montaje[
        "Email"
    ].apply(
        limpiar_email
    )


    return montaje


# ============================================================
# 9. FUNCIÓN PRINCIPAL DE LIMPIEZA
# ============================================================

def limpiar_montaje(montaje):

    print("\n")
    print("=" * 60)
    print("LIMPIEZA DE REGISTROS FINALES")
    print("=" * 60)


    # --------------------------------------------------------
    # Legal_Name
    # --------------------------------------------------------

    montaje = limpiar_legal_name(
        montaje
    )


    # --------------------------------------------------------
    # Company_Rep1
    # --------------------------------------------------------

    montaje = limpiar_company_rep1(
        montaje
    )


    # --------------------------------------------------------
    # Insurer
    # --------------------------------------------------------

    montaje = limpiar_insurer(
        montaje
    )


    # --------------------------------------------------------
    # Email
    # --------------------------------------------------------

    montaje = limpiar_emails(
        montaje
    )


    print("\nCampos limpiados:")

    print("- Legal_Name")
    print("- Company_Rep1")
    print("- Insurer")
    print("- Email")


    print(
        "\nRegistros actualmente en Montaje:",
        len(montaje)
    )


    return montaje


# ============================================================
# 10. PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 60)
    print("PRUEBA DEL MÓDULO LIMPIEZA")
    print("=" * 60)


    ejemplos = [
        "A & A GLOBAL FREIGHT LLC",
        "ACME & SONS - TRUCKING, INC.",
        "José Pérez & Asociados"
    ]


    print("\nPrueba de limpieza de textos:")


    for ejemplo in ejemplos:

        resultado = limpiar_campo_texto(
            ejemplo
        )

        print(
            f"\nOriginal: {ejemplo}"
        )

        print(
            f"Limpio:   {resultado}"
        )


    correos = [
        "correo1@gmail.com;correo2@gmail.com",
        "correo1@gmail.com",
        "correo,com@gmail.com"
    ]


    print("\nPrueba de limpieza de correos:")


    for correo in correos:

        resultado = limpiar_email(
            correo
        )

        print(
            f"\nOriginal: {correo}"
        )

        print(
            f"Limpio:   {resultado}"
        )