@echo off

REM Evita mostrar cada comando en la consola y hace que las variables creadas
REM dentro de bloques entre parentesis se actualicen correctamente.
setlocal enabledelayedexpansion

REM Cambia a la carpeta donde esta este archivo .cmd. Asi el instalador
REM funciona aunque se abra desde un acceso directo o desde otra carpeta.
cd /d "%~dp0"
if errorlevel 1 goto error

REM Si ya existe el entorno virtual, se reutiliza para no reinstalar Python.
if exist ".venv\Scripts\python.exe" goto dependencias

REM PYTHON_CMD guardara el comando disponible para crear el entorno virtual.
REM Se prueba primero el lanzador py y despues los nombres habituales de
REM Python, porque algunas instalaciones no incluyen el lanzador py.
set "PYTHON_CMD="
where py >nul 2>nul
if not errorlevel 1 set "PYTHON_CMD=py -3"
if not defined PYTHON_CMD where python >nul 2>nul
if not defined PYTHON_CMD if not errorlevel 1 set "PYTHON_CMD=python"
if not defined PYTHON_CMD where python3 >nul 2>nul
if not defined PYTHON_CMD if not errorlevel 1 set "PYTHON_CMD=python3"

if not defined PYTHON_CMD (
    REM Ningun comando de Python esta disponible en PATH.
    echo No se encontro Python 3.12 o superior en PATH.
    echo Instala Python 3.12+ de 64 bits y asegura que "py" o "python" esten disponibles.
    echo Si falta Tcl/Tk, instala el componente en la misma instalacion de Python.
    goto error
)

REM Crea un entorno aislado para que las dependencias de esta aplicacion no
REM interfieran con otros programas instalados en el equipo.
echo Creando entorno virtual con: %PYTHON_CMD% -m venv .venv
%PYTHON_CMD% -m venv .venv
if errorlevel 1 (
    echo No se pudo crear el entorno virtual.
    echo Instala Python 3.12+ de 64 bits con el componente Tcl/Tk incluido.
    goto error
)

:dependencias
REM Desde este punto siempre se utiliza el Python del entorno virtual. Esto
REM garantiza que pip instale y compruebe paquetes en el lugar correcto.
set "VENV_PY=.venv\Scripts\python.exe"
if not exist "%VENV_PY%" (
    echo No se encontro el ejecutable del entorno virtual en "%VENV_PY%".
    goto error
)

REM Comprueba que la version del interprete cumple el minimo del proyecto.
"%VENV_PY%" -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)"
if errorlevel 1 (
    echo El entorno virtual no usa Python 3.12 o superior.
    echo Reinstala con Python 3.12+ y vuelve a ejecutar instalar.cmd.
    goto error
)

REM Actualiza pip antes de instalar para mejorar la compatibilidad con ruedas
REM binarias recientes y con las versiones actuales del indice de paquetes.
"%VENV_PY%" -m pip install --upgrade pip
if errorlevel 1 goto error

REM Instala exactamente las dependencias declaradas por el proyecto.
"%VENV_PY%" -m pip install -r requirements.txt
if errorlevel 1 goto error

REM Busca dependencias incompatibles o versiones rotas dentro del entorno.
"%VENV_PY%" -m pip check
if errorlevel 1 goto error

REM Importa la biblioteca grafica y los modulos principales para detectar
REM durante la instalacion problemas de tkinter, paquetes o rutas del codigo.
"%VENV_PY%" -c "import tkinter, pandas, openpyxl, customtkinter, PIL, xlrd; import interfaz.ventana"
if errorlevel 1 goto error

REM Si se llega aqui, el entorno y las importaciones esenciales son validos.
echo Instalacion completada. Abre iniciar.cmd para usar el programa.
pause
exit /b 0
:error
REM Todos los errores terminan aqui con codigo 1 para que Windows sepa que la
REM instalacion fallo. El mensaje apunta al README para diagnosticos comunes.
echo No se pudo completar la instalacion. Revisa el mensaje anterior y README.md.
pause
exit /b 1
