"""Configuración portable del proyecto.

La interfaz utiliza los archivos elegidos por el usuario. Las rutas auxiliares
solo sirven como respaldo para llamadas desde código que no proporcionen rutas.
"""

import os
from pathlib import Path

RUTA_PROYECTO = Path(__file__).resolve().parent
RUTA_ARCHIVOS = RUTA_PROYECTO / "Archivos"


def ruta_configurada(variable, predeterminada):
    valor = os.environ.get(variable, "").strip()
    if not valor:
        return predeterminada
    ruta = Path(valor).expanduser()
    if not ruta.is_absolute():
        ruta = RUTA_PROYECTO / ruta
    return ruta.resolve()


RUTA_DESCARGAS = ruta_configurada(
    "DEPURADOR_RUTA_DATA", Path.home() / "Downloads"
)
RUTA_FILTROS = ruta_configurada("DEPURADOR_RUTA_FILTROS", RUTA_ARCHIVOS)

NOMBRE_HOJA_MONTAJE = "Montaje Español"
NOMBRE_HOJA_BASE = "Base"
NOMBRE_HOJA_RECHAZOS = "Rechazos"
NOMBRE_ARCHIVO_DATA = "data"
NOMBRE_ARCHIVO_FILTROS = "FILTROS ESPAÑOL"
EXTENSIONES_PERMITIDAS = [".xlsx", ".xls", ".csv"]
