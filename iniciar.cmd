@echo off
setlocal
cd /d "%~dp0"
if errorlevel 1 goto error
if not exist ".venv\Scripts\python.exe" (
    echo Primero ejecuta instalar.cmd.
    goto error
)
".venv\Scripts\python.exe" iniciar.py
if errorlevel 1 goto error
exit /b 0
:error
echo El programa no pudo iniciarse o se cerro con un error. Revisa el mensaje anterior.
pause
exit /b 1
