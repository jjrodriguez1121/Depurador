"""Punto de entrada de la aplicación cuando se ejecuta desde una consola.

Este archivo mantiene el arranque separado de la implementación gráfica. Su
responsabilidad es comprobar los requisitos mínimos, importar la ventana
principal y entregar el control al bucle de eventos de Tkinter.
"""

import sys


def main():
    # El proyecto utiliza características y versiones de dependencias que
    # requieren Python 3.12 o posterior. Se comprueba antes de importar la
    # interfaz para mostrar un mensaje útil en lugar de un error más confuso.
    if sys.version_info < (3, 12):
        print("Usa Python 3.12 o posterior. La versión probada es Python 3.12.")
        return 1

    try:
        # La importación se realiza dentro de un try para capturar tanto una
        # dependencia ausente como un problema de instalación de tkinter u
        # otro módulo requerido por la interfaz.
        from interfaz.ventana import Aplicacion
    except ImportError as error:
        print(f"No se pudo cargar una dependencia: {error}")
        print("Ejecuta instalar.cmd o instala requirements.txt en tu entorno Python.")
        print("Si falta tkinter, instala Python con el componente Tcl/Tk.")
        return 1

    # Aplicacion es la ventana principal. mainloop mantiene abierta la
    # interfaz y procesa eventos de teclado, ratón y repintado de ventanas.
    app = Aplicacion()
    app.mainloop()

    # Cero comunica a Windows que la aplicación terminó correctamente.
    return 0


if __name__ == "__main__":
    # Este bloque solo se ejecuta cuando el archivo se lanza directamente.
    # sys.exit convierte el resultado de main en el código de salida del
    # proceso, que pueden utilizar los scripts de instalación o diagnóstico.
    sys.exit(main())
