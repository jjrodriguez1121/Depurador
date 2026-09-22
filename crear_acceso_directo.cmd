@echo off
setlocal
cd /d "%~dp0"
if errorlevel 1 goto error

set "APP_PATH=%~dp0DepuradorTruking.exe"
set "WORKING_DIR=%~dp0"
if exist "%~dp0dist\DepuradorTruking\DepuradorTruking.exe" (
    set "APP_PATH=%~dp0dist\DepuradorTruking\DepuradorTruking.exe"
    set "WORKING_DIR=%~dp0dist\DepuradorTruking"
)
set "SHORTCUT_PATH=%USERPROFILE%\Desktop\DepuradorTruking.lnk"

if not exist "%APP_PATH%" (
    echo No se encontro el ejecutable:
    echo %APP_PATH%
    echo Ejecuta construir.cmd antes de crear el acceso directo.
    goto error
)

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$shell = New-Object -ComObject WScript.Shell; $shortcut = $shell.CreateShortcut($env:SHORTCUT_PATH); $shortcut.TargetPath = $env:APP_PATH; $shortcut.WorkingDirectory = $env:WORKING_DIR; $shortcut.IconLocation = $env:APP_PATH + ',0'; $shortcut.Save()"
if errorlevel 1 goto error

echo Acceso directo creado en:
echo %SHORTCUT_PATH%
exit /b 0

:error
echo No se pudo crear el acceso directo.
pause
exit /b 1