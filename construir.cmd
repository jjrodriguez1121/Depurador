@echo off
setlocal
cd /d "%~dp0"
if errorlevel 1 goto error

if not exist ".venv\Scripts\python.exe" (
    echo Primero ejecuta instalar.cmd para crear el entorno de construccion.
    goto error
)

".venv\Scripts\python.exe" -m pip install pyinstaller
if errorlevel 1 goto error

".venv\Scripts\python.exe" -m PyInstaller --noconfirm --clean --onedir --windowed --name "DepuradorTruking" --add-data "Archivos;Archivos" --collect-all customtkinter iniciar.py
if errorlevel 1 goto error
copy /y "crear_acceso_directo.cmd" "dist\DepuradorTruking\crear_acceso_directo.cmd" > nul
if errorlevel 1 goto error

echo.
echo Paquete creado en:
echo %CD%\dist\DepuradorTruking
echo.
echo Para crear un acceso directo en este equipo, ejecuta crear_acceso_directo.cmd.
pause
exit /b 0

:error
echo No se pudo construir el paquete. Revisa el mensaje anterior.
pause
exit /b 1