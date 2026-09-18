# ============================================================
# CONFIGURACIÓN 
# ============================================================
#
# Este módulo contiene las rutas y configuraciones generales
# utilizadas por el proyecto.
#
# La idea es evitar tener rutas y nombres escritos directamente
# dentro de los diferentes módulos del sistema.
#
# Si en el futuro cambia una ruta o configuración general,
# solamente será necesario modificar este archivo.
#
# ============================================================


# ============================================================
# 1. IMPORTAR LIBRERÍA
# ============================================================

from pathlib import Path


# ============================================================
# 2. RUTA PRINCIPAL DEL PROYECTO
# ============================================================
#
# Carpeta principal donde se encuentra el proyecto.
#
# ============================================================

RUTA_PROYECTO = Path(
    r"C:\Users\jeferson.rodriguez\OneDrive - USA Truck Brokers SAS"
    r"\Escritorio\Campañas\DepuradorTruking"
)


# ============================================================
# 3. RUTA DE LOS ARCHIVOS AUXILIARES DEL PROYECTO
# ============================================================
#
# Esta carpeta contiene recursos auxiliares utilizados por
# la aplicación.
#
# IMPORTANTE:
#
# El archivo "data" NO se busca aquí.
#
# El archivo "FILTROS ESPAÑOL" TAMPOCO se busca aquí.
#
# ============================================================

RUTA_ARCHIVOS = RUTA_PROYECTO / "Archivos"


# ============================================================
# 4. RUTA DE DESCARGAS
# ============================================================
#
# El archivo externo "data" se busca automáticamente dentro
# de la carpeta Downloads del usuario actual de Windows.
#
# Path.home() permite evitar escribir directamente el nombre
# del usuario de Windows.
#
# Ejemplo:
#
#     C:\Users\Usuario\Downloads
#
# ============================================================

RUTA_DESCARGAS = Path.home() / "Downloads"


# ============================================================
# 5. RUTA DE FILTROS ESPAÑOL
# ============================================================
#
# Carpeta donde actualmente se encuentra el archivo:
#
#     FILTROS ESPAÑOL
#
# Ubicación actual:
#
#     OneDrive - USA Truck Brokers SAS
#         └── Escritorio
#             └── Campañas
#
# ============================================================

RUTA_FILTROS = Path(
    r"C:\Users\jeferson.rodriguez\OneDrive - USA Truck Brokers SAS"
    r"\Escritorio\Campañas"
)


# ============================================================
# 9. NOMBRE DE LA HOJA DE MONTAJE
# ============================================================
#
# Esta hoja contiene los registros que superaron todas las
# validaciones y posteriormente será utilizada por el
# exportador CSV.
#
# ============================================================

NOMBRE_HOJA_MONTAJE = "Montaje"


# ============================================================
# 10. NOMBRE DE LA HOJA BASE
# ============================================================

NOMBRE_HOJA_BASE = "Base"


# ============================================================
# 11. NOMBRE DE LA HOJA DE RECHAZOS
# ============================================================

NOMBRE_HOJA_RECHAZOS = "Rechazos"


# ============================================================
# 12. NOMBRE DEL ARCHIVO EXTERNO "data"
# ============================================================
#
# No se incluye la extensión porque el archivo puede ser:
#
#     data.xlsx
#     data.xls
#     data.csv
#
# Este archivo será buscado dentro de:
#
#     RUTA_DESCARGAS
#
# ============================================================

NOMBRE_ARCHIVO_DATA = "data"


# ============================================================
# 13. NOMBRE DEL ARCHIVO "FILTROS ESPAÑOL"
# ============================================================
#
# No se incluye la extensión porque el archivo puede ser:
#
#     FILTROS ESPAÑOL.xlsx
#     FILTROS ESPAÑOL.xls
#     FILTROS ESPAÑOL.csv
#
# Este archivo será buscado dentro de:
#
#     RUTA_FILTROS
#
# ============================================================

NOMBRE_ARCHIVO_FILTROS = "FILTROS ESPAÑOL"


# ============================================================
# 14. EXTENSIONES PERMITIDAS
# ============================================================
#
# Extensiones que actualmente acepta el proceso.
#
# ============================================================

EXTENSIONES_PERMITIDAS = [
    ".xlsx",
    ".xls",
    ".csv"
]