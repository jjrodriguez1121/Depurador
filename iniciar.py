"""Punto de entrada de la aplicación: python iniciar.py."""

import sys


def main():
    if sys.version_info < (3, 12):
        print("Usa Python 3.12 o posterior. La versión probada es Python 3.12.")
        return 1
    try:
        from interfaz.ventana import Aplicacion
    except ImportError as error:
        print(f"No se pudo cargar una dependencia: {error}")
        print("Ejecuta instalar.cmd o instala requirements.txt en tu entorno Python.")
        print("Si falta tkinter, instala Python con el componente Tcl/Tk.")
        return 1
    app = Aplicacion()
    app.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
