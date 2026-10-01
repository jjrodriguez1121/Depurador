@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
if errorlevel 1 goto error

if exist ".venv\Scripts\python.exe" goto dependencias

set "PYTHON_CMD="
where py >nul 2>nul
if not errorlevel 1 set "PYTHON_CMD=py -3"
if not defined PYTHON_CMD where python >nul 2>nul
if not defined PYTHON_CMD if not errorlevel 1 set "PYTHON_CMD=python"
if not defined PYTHON_CMD where python3 >nul 2>nul
if not defined PYTHON_CMD if not errorlevel 1 set "PYTHON_CMD=python3"

if not defined PYTHON_CMD (
    echo No se encontro Python 3.12 o superior en PATH.
    echo Instala Python 3.12+ de 64 bits y asegura que "py" o "python" esten disponibles.
    echo Si falta Tcl/Tk, instala el componente en la misma instalacion de Python.
    goto error
)

echo Creando entorno virtual con: %PYTHON_CMD% -m venv .venv
%PYTHON_CMD% -m venv .venv
if errorlevel 1 (
    echo No se pudo crear el entorno virtual.
    echo Instala Python 3.12+ de 64 bits con el componente Tcl/Tk incluido.
    goto error
)

:dependencias
set "VENV_PY=.venv\Scripts\python.exe"
if not exist "%VENV_PY%" (
    echo No se encontro el ejecutable del entorno virtual en "%VENV_PY%".
    goto error
)

"%VENV_PY%" -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)"
if errorlevel 1 (
    echo El entorno virtual no usa Python 3.12 o superior.
    echo Reinstala con Python 3.12+ y vuelve a ejecutar instalar.cmd.
    goto error
)

"%VENV_PY%" -m pip install --upgrade pip
if errorlevel 1 goto error
"%VENV_PY%" -m pip install -r requirements.txt
if errorlevel 1 goto error
"%VENV_PY%" -m pip check
if errorlevel 1 goto error
"%VENV_PY%" -c "import tkinter, pandas, openpyxl, customtkinter, PIL, xlrd; import interfaz.ventana"
if errorlevel 1 goto error
echo Instalacion completada. Abre iniciar.cmd para usar el programa.
pause
exit /b 0
:error
echo No se pudo completar la instalacion. Revisa el mensaje anterior y README.md.
pause
exit /b 1
