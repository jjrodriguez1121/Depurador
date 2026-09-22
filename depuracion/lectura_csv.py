"""Lectura estricta de la base CSV con coma o punto y coma."""

import csv
from io import StringIO
from pathlib import Path

import pandas as pd


def _encabezado(texto, separador):
    lector = csv.reader(StringIO(texto, newline=""), delimiter=separador, strict=True)
    for fila in lector:
        if fila and not (len(fila) == 1 and not fila[0].strip()):
            return fila
    return []


def _validar_filas(texto, separador, columnas):
    lector = csv.reader(StringIO(texto, newline=""), delimiter=separador, strict=True)
    try:
        for fila in lector:
            if not fila or (len(fila) == 1 and not fila[0].strip()):
                continue
            if len(fila) != columnas:
                raise ValueError(
                    f"CSV mal formado en la línea {lector.line_num}: "
                    f"se esperaban {columnas} campos y se encontraron {len(fila)}. "
                    "Revisa los separadores y las comillas de esa fila."
                )
    except csv.Error as error:
        raise ValueError(
            f"CSV mal formado cerca de la línea {lector.line_num}: "
            "revisa las comillas y los campos del archivo."
        ) from error


def leer_csv_base(archivo, conservar_original=False):
    """Detecta el separador en el encabezado y valida todas las filas.

    Nunca descarta filas defectuosas. Si ambos separadores producen varias
    columnas, pide corregir la ambigüedad en lugar de adivinar el formato.
    DOT se conserva como texto para validar su formato sin conversiones
    automáticas; las demás columnas mantienen la inferencia de pandas.
    Con conservar_original=True se guardan todos los campos como texto y
    no se interpretan valores como 'NA' ni se eliminan ceros iniciales.
    """
    archivo = Path(archivo)
    try:
        with archivo.open(encoding="utf-8-sig", newline="") as fuente:
            texto = fuente.read()
    except UnicodeDecodeError as error:
        raise ValueError(
            f"No se pudo leer '{archivo.name}' como UTF-8. "
            "Guarda el archivo como CSV UTF-8 y vuelve a intentarlo."
        ) from error

    if "\x00" in texto:
        raise ValueError(
            "El CSV contiene caracteres nulos y no puede leerse con seguridad. "
            "Guarda una copia como CSV UTF-8 y vuelve a intentarlo."
        )

    encabezados = {}
    for separador in (",", ";"):
        try:
            encabezados[separador] = _encabezado(texto, separador)
        except csv.Error:
            continue

    if not encabezados:
        raise ValueError("No se pudo leer el encabezado del CSV. Revisa sus comillas.")
    if not any(encabezados.values()):
        raise ValueError("El archivo CSV está vacío o no contiene un encabezado.")

    candidatos = [s for s, columnas in encabezados.items() if len(columnas) > 1]
    if len(candidatos) > 1:
        raise ValueError(
            "No se pudo determinar con seguridad el separador del CSV: "
            "el encabezado contiene comas y puntos y coma. "
            "Usa un único separador y encierra entre comillas los textos que lo contengan."
        )

    if candidatos:
        separador = candidatos[0]
        _validar_filas(texto, separador, len(encabezados[separador]))
    else:
        for otro in ("\t", "|"):
            try:
                no_admitido = len(_encabezado(texto, otro)) > 1
            except csv.Error:
                no_admitido = False
            if no_admitido:
                raise ValueError(
                    "El CSV parece utilizar un separador distinto de coma o punto y coma. "
                    "Guarda el archivo con uno de esos dos separadores."
                )
        # Un CSV de una sola columna es válido y debe llegar al aviso de
        # columnas faltantes. Ninguna fila puede introducir campos adicionales.
        for opcion in encabezados:
            _validar_filas(texto, opcion, 1)
        separador = next(iter(encabezados))

    try:
        return pd.read_csv(
            StringIO(texto), sep=separador, on_bad_lines="error",
            dtype=str if conservar_original else {"DOT": str},
            keep_default_na=not conservar_original,
        )
    except (pd.errors.ParserError, pd.errors.EmptyDataError) as error:
        raise ValueError(
            f"No se pudo interpretar el CSV '{archivo.name}'. "
            "Revisa el encabezado, los separadores y las comillas."
        ) from error
