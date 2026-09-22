@echo off
setlocal
cd /d "%~dp0"
if errorlevel 1 goto error
if exist ".venv\Scripts\python.exe" goto dependencias
py -3.12 -m venv .venv
if errorlevel 1 (
    echo Instala Python 3.12 con el lanzador py y el componente Tcl/Tk.
    goto error
)
:dependencias
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto error
".venv\Scripts\python.exe" -m pip check
if errorlevel 1 goto error
".venv\Scripts\python.exe" -c "import tkinter, pandas, openpyxl, customtkinter, PIL, xlrd; import interfaz.ventana"
if errorlevel 1 goto error
echo Instalacion completada. Abre iniciar.cmd para usar el programa.
pause
exit /b 0
:error
echo No se pudo completar la instalacion. Revisa el mensaje anterior y README.md.
pause
exit /b 1
