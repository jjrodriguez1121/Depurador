"""Configuración centralizada y portable del proyecto.

Este módulo reúne las rutas y nombres que utilizan varios componentes de la
aplicación. La interfaz normalmente trabaja con los archivos seleccionados por
el usuario; las rutas de ``RUTA_DESCARGAS`` y ``RUTA_FILTROS`` solo funcionan
como respaldo cuando una llamada desde código no proporciona esos archivos.

Las rutas se calculan a partir de la ubicación real de este archivo, no de la
carpeta desde la que se inició Python. Por eso el proyecto puede copiarse a
otra carpeta o a otro equipo sin editar rutas absolutas.
"""

import os
from pathlib import Path

# Path(__file__) apunta a config.py. resolve() convierte esa ubicación en una
# ruta absoluta y parent obtiene la carpeta raíz del proyecto Depurador.
RUTA_PROYECTO = Path(__file__).resolve().parent

# Los archivos auxiliares distribuidos con el proyecto se encuentran dentro
# de esta subcarpeta, por ejemplo el catálogo de filtros predeterminado.
RUTA_ARCHIVOS = RUTA_PROYECTO / "Archivos"


def ruta_configurada(variable, predeterminada):
    """Devuelve una ruta definida por entorno o una ruta predeterminada.

    ``variable`` es el nombre de una variable de entorno y ``predeterminada``
    es la ruta que se utiliza cuando la variable no existe o está vacía.
    Las rutas relativas se interpretan desde la carpeta del proyecto; las
    rutas absolutas se conservan en su ubicación original.
    """

    # get() evita un KeyError cuando la variable no está definida. strip()
    # permite tratar como vacía una variable que solo contiene espacios.
    valor = os.environ.get(variable, "").strip()
    if not valor:
        return predeterminada

    # expanduser() permite expresiones como ~ y Path() normaliza el texto
    # recibido para poder operar con él de forma independiente de Windows.
    ruta = Path(valor).expanduser()

    # Una ruta relativa no debe depender de la carpeta de trabajo actual,
    # porque el programa puede iniciarse desde un acceso directo. Se ancla a
    # la carpeta del proyecto para conservar un comportamiento portable.
    if not ruta.is_absolute():
        ruta = RUTA_PROYECTO / ruta

    # resolve() devuelve una ruta absoluta normalizada y elimina componentes
    # redundantes como . o .. cuando el sistema puede resolverlos.
    return ruta.resolve()


# Carpeta donde se buscan archivos data cuando una llamada no proporciona una
# ruta explícita. Por defecto es la carpeta Downloads del usuario actual.
RUTA_DESCARGAS = ruta_configurada(
    "DEPURADOR_RUTA_DATA", Path.home() / "Downloads"
)

# Carpeta de respaldo donde se busca el catálogo FILTROS ESPAÑOL. Puede
# sustituirse mediante DEPURADOR_RUTA_FILTROS.
RUTA_FILTROS = ruta_configurada("DEPURADOR_RUTA_FILTROS", RUTA_ARCHIVOS)

# Nombres de las hojas que genera el archivo Excel de salida.
NOMBRE_HOJA_MONTAJE = "Montaje Español"
NOMBRE_HOJA_BASE = "Base"
NOMBRE_HOJA_RECHAZOS = "Rechazos"

# Nombres lógicos de los archivos auxiliares que el código intenta localizar
# cuando no recibe una selección explícita desde la interfaz.
NOMBRE_ARCHIVO_DATA = "data"
NOMBRE_ARCHIVO_FILTROS = "FILTROS ESPAÑOL"

# Extensiones admitidas para las bases y los archivos auxiliares.
EXTENSIONES_PERMITIDAS = [".xlsx", ".xls", ".csv"]
