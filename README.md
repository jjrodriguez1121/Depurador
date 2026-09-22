# Depurador de bases TRUKING

Aplicación de escritorio para depurar una base, cruzar DOT contra un archivo de
referencia y generar un Excel de revisión y un CSV para campañas.

## Instalación en Windows

1. Instala **Python 3.12 de 64 bits**, incluyendo el lanzador `py`, `pip` y
   el componente **Tcl/Tk**. Python 3.12 es la versión con la que se verifica el proyecto.
2. Copia o descarga la carpeta completa del proyecto en una ubicación con permiso
   de escritura. Conserva sus subcarpetas, incluida `Archivos`.
3. Abre **`instalar.cmd`** con doble clic. Creará `.venv` e instalará las
   dependencias de `requirements.txt`. Necesita conexión a Internet durante la instalación.
4. Cuando indique que terminó, abre **`iniciar.vbs`** para iniciar sin consola.

Puedes crear un acceso directo a `iniciar.vbs` en el escritorio. Este lanzador
utiliza `pythonw.exe` del entorno `.venv`. Los mensajes y errores se guardan en
`logs/aplicacion.log`; al superar 5 MiB se conserva una copia anterior en el
siguiente arranque. `iniciar.cmd` también delega en este lanzador, aunque Windows
puede mostrar brevemente la consola al abrir un archivo `.cmd`.

No hace falta instalar Microsoft Excel. No se requieren rutas de un usuario
específico ni activar manualmente el entorno virtual. Los lanzadores trabajan
desde su propia carpeta, incluso si la ruta contiene espacios.

Si trasladas el proyecto a otro equipo o ubicación, copia el código **sin `.venv`**
y ejecuta allí `instalar.cmd`: los entornos virtuales no son portables.

### Instalación manual en PowerShell

Abre PowerShell dentro de la carpeta del proyecto:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe iniciar.py
```

Para actualizar dependencias declaradas, vuelve a ejecutar `instalar.cmd`.
Se reutiliza el entorno existente; no se borran las bases ni los resultados.

## Uso

1. Selecciona la **base de entrada** (`.xlsx`, `.xls` o `.csv`).
2. Selecciona **data**, que debe contener `general_info.dot` y `stage`.
3. Selecciona **FILTROS ESPAÑOL**: los nombres van en la primera columna,
   sin encabezado. Debe contener al menos un nombre utilizable.
4. Elige los destinos del Excel y el CSV. Usa archivos distintos de las entradas.
5. Elige una o dos coincidencias para representantes e inicia la depuración.
6. Si faltan columnas, revisa el aviso y elige continuar creándolas vacías o cancelar.

Los archivos auxiliares seleccionados pueden tener cualquier nombre y estar en
cualquier carpeta. En la interfaz no se eligen automáticamente.

La base CSV admite coma o punto y coma, con codificación UTF-8. Los campos que
contengan separadores o saltos de línea deben estar entre comillas. Las filas
mal formadas detienen la lectura y muestran el problema.

Columnas usadas para depurar:

```text
DOT, Legal_Name, Phone, Cell_Num, Business_State, Email, Company_Rep1,
Years_In_Business, Power_Units, Insurer, Policy_Effective_Date,
Policy_Cancellation_Date
```

El Excel contiene **Base**, **Montaje Español** y **Rechazos**. Base conserva
las columnas y datos de la tabla de entrada; no es una copia del formato,
fórmulas ni otras hojas del libro original. El CSV se genera desde Montaje
Español, separado por punto y coma y con codificación UTF-8 con BOM.
Ambos archivos se generan desde los datos preparados en memoria, sin releer
el Excel para construir el CSV.

## Configuración

`config.py` obtiene la carpeta del proyecto desde su propia ubicación y encuentra
los recursos en `Archivos`. No hay que editar rutas para instalarlo en otro equipo.

Solo para llamadas desde código que **omitan** los archivos auxiliares, se mantiene
una búsqueda de respaldo:

| Archivo | Carpeta predeterminada | Variable opcional |
|---|---|---|
| `data.xlsx`, `.xls` o `.csv` | `Downloads` del usuario actual | `DEPURADOR_RUTA_DATA` |
| `FILTROS ESPAÑOL.xlsx`, `.xls` o `.csv` | `Archivos` del proyecto | `DEPURADOR_RUTA_FILTROS` |

Las variables indican **carpetas**, no archivos. Las rutas relativas se resuelven
desde el proyecto. Ejemplo para una sesión de PowerShell:

```powershell
$env:DEPURADOR_RUTA_DATA = 'D:\Bases\CRM'
$env:DEPURADOR_RUTA_FILTROS = 'D:\Bases\Catalogos'
```

Estas variables no reemplazan lo elegido en la interfaz.

## Dependencias

`requirements.txt` fija las dependencias directas:

- `pandas`: procesamiento de tablas.
- `openpyxl`: lectura y escritura de `.xlsx`.
- `xlrd`: lectura de archivos antiguos `.xls`.
- `customtkinter`: interfaz gráfica.
- `Pillow`: imágenes de la interfaz.

`tkinter`, `unittest`, `csv` y `pathlib` vienen con Python; no se instalan con pip.
Las dependencias transitivas las resuelve pip.

## Pruebas

Desde la carpeta del proyecto:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Las pruebas gráficas se omiten por defecto. Para incluirlas (abren y cierran ventanas):

```powershell
$env:DEPURADOR_TEST_GUI = '1'
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
Remove-Item Env:DEPURADOR_TEST_GUI
```

## Medir rendimiento

```powershell
.\.venv\Scripts\python.exe benchmarks/exportacion.py --filas 1000 20000
```

La medición compara únicamente generar el CSV: leyendo el Excel frente a usar
la tabla preparada en memoria. Excluye escribir el Excel y las etapas de
depuración. Usa datos sintéticos y comprueba que los CSV sean idénticos byte a
byte. El pico de memoria mide asignaciones Python con `tracemalloc`, no la RAM
total; se mide en una ejecución separada para no distorsionar el tiempo.

Resultados de referencia del 22/09/2026, Python 3.12:

| Registros | CSV desde Excel | CSV desde memoria | Pico Python antes / después |
|---|---|---|---|
| 1.000 | 0,200 s | 0,027 s | 1,57 / 1,28 MiB |
| 20.000 | 2,869 s | 0,811 s | 24,74 / 13,02 MiB |

Son mediciones puntuales en este equipo, no garantías para otras bases.
La limpieza principal también pasa de cuatro copias de tabla a una; Base se
mantiene separada de la depuración y no se vuelve a copiar para exportarla.

## Problemas frecuentes

- **No se reconoce `py`:** instala el lanzador de Python o usa la ruta completa
  al ejecutable Python 3.12 en lugar de `py -3.12` en la instalación manual.
- **Falta un módulo:** ejecuta `instalar.cmd` y luego inicia con `iniciar.cmd`,
  para usar el mismo entorno donde instalaste las dependencias.
- **Falta tkinter/Tcl/Tk:** modifica la instalación de Python e incluye ese componente.
- **No puede descargar paquetes:** revisa Internet, proxy o restricciones de la red.
- **No puede guardar el Excel:** cierra ese archivo en Excel y comprueba los permisos
  de la carpeta de destino.
- **El CSV no es UTF-8:** vuelve a guardarlo como CSV UTF-8.
- **La selección de auxiliares falla:** comprueba las columnas de data y el catálogo;
  el programa no sustituye un archivo elegido por otro encontrado automáticamente.
