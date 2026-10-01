@echo off

REM Evita mostrar cada comando mientras se ejecuta este lanzador.
setlocal

REM %~dp0 representa la carpeta donde esta este archivo .cmd.
REM El modificador /d tambien permite cambiar de unidad, por ejemplo de C: a D:.
REM Asi las rutas relativas del programa siempre parten de la carpeta correcta.
cd /d "%~dp0"
if errorlevel 1 goto error

REM Antes de iniciar, verifica que el entorno virtual creado por instalar.cmd
REM tenga su interprete de Python. No se ejecuta Python global porque las
REM dependencias de la aplicacion deben estar aisladas dentro de .venv.
if not exist ".venv\Scripts\python.exe" (
    REM Este mensaje aparece cuando el usuario intenta iniciar la aplicacion
    REM en una copia nueva del proyecto o antes de completar la instalacion.
    echo Primero ejecuta instalar.cmd.
    goto error
)

REM iniciar.vbs se encarga de localizar pythonw.exe y ejecutar iniciar.pyw
REM sin dejar una ventana de consola visible. Se usa start para que el .cmd
REM termine inmediatamente y no bloquee la consola del usuario.
REM El primer argumento vacio ("") es el titulo de la ventana requerido por
REM start cuando el comando siguiente se proporciona entre comillas.
start "" wscript.exe "%~dp0iniciar.vbs"
if errorlevel 1 goto error

REM Codigo 0: Windows interpreta que el lanzador pudo iniciar el proceso.
exit /b 0

:error
REM Cualquier fallo anterior llega aqui. pause mantiene visible el mensaje
REM cuando el archivo se abre con doble clic y exit /b 1 indica error.
echo El programa no pudo iniciarse o se cerro con un error. Revisa el mensaje anterior.
pause
exit /b 1
