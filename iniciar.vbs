Option Explicit
Dim archivos, shell, carpeta, python, entrada
Set archivos = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")
carpeta = archivos.GetParentFolderName(WScript.ScriptFullName)
python = archivos.BuildPath(carpeta, ".venv\Scripts\pythonw.exe")
entrada = archivos.BuildPath(carpeta, "iniciar.pyw")
If Not archivos.FileExists(python) Then
    MsgBox "Primero ejecuta instalar.cmd en la carpeta del proyecto.", 48, "Depurador Trucking"
    WScript.Quit 1
End If
shell.CurrentDirectory = carpeta
shell.Run Chr(34) & python & Chr(34) & " " & Chr(34) & entrada & Chr(34), 0, False
