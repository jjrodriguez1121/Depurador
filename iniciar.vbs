Option Explicit

' Declara todas las variables antes de usarlas. Esto ayuda a detectar errores
' tipográficos en los nombres de variables durante la ejecución del script.
Dim archivos, shell, carpeta, python, entrada

' FileSystemObject permite consultar archivos y construir rutas sin depender
' de la carpeta desde la que el usuario haya abierto el acceso directo.
Set archivos = CreateObject("Scripting.FileSystemObject")

' WScript.Shell permite cambiar la carpeta de trabajo y lanzar el proceso
' de Python que contiene la aplicación.
Set shell = CreateObject("WScript.Shell")

' WScript.ScriptFullName contiene la ruta completa de este archivo .vbs.
' GetParentFolderName obtiene la carpeta del proyecto, incluso si la ruta
' contiene espacios o si el usuario inició el script desde otra ubicación.
carpeta = archivos.GetParentFolderName(WScript.ScriptFullName)

' pythonw.exe es la versión de Python que no abre una ventana de consola.
' El instalador crea este ejecutable dentro del entorno virtual del proyecto.
python = archivos.BuildPath(carpeta, ".venv\Scripts\pythonw.exe")

' iniciar.pyw contiene el punto de entrada gráfico de la aplicación.
' BuildPath combina la carpeta del proyecto con el nombre del archivo de forma
' segura para Windows.
entrada = archivos.BuildPath(carpeta, "iniciar.pyw")

' Si el entorno virtual todavía no existe, la aplicación no puede ejecutarse.
' Se muestra una instrucción clara y se termina con código 1 para indicar
' que el arranque no fue exitoso.
If Not archivos.FileExists(python) Then
    MsgBox "Primero ejecuta instalar.cmd en la carpeta del proyecto.", 48, "Depurador Trucking"
    WScript.Quit 1
End If

' La aplicación usa rutas relativas para encontrar sus módulos y recursos.
' Por eso la carpeta de trabajo debe ser siempre la carpeta del proyecto,
' no necesariamente la carpeta activa desde la que se abrió el .vbs.
shell.CurrentDirectory = carpeta

' Chr(34) devuelve una comilla doble. Se agregan comillas a las rutas para
' que el comando siga funcionando aunque el proyecto esté dentro de una ruta
' como "C:\Users\Nombre\Mis proyectos\Depurador".
' El segundo parámetro, 0, oculta la ventana de consola.
' El tercer parámetro, False, permite que el script termine sin esperar a que
' finalice la aplicación gráfica.
shell.Run Chr(34) & python & Chr(34) & " " & Chr(34) & entrada & Chr(34), 0, False
