"""Arranque gráfico de la aplicación sin abrir una consola de Windows.

El archivo ``.pyw`` se ejecuta con ``pythonw.exe`` desde ``iniciar.vbs``.
Como ese ejecutable no muestra ``stdout`` ni ``stderr`` en una consola visible,
este módulo redirige ambos flujos a ``logs/aplicacion.log`` para conservar la
información necesaria cuando ocurre un error durante el arranque.
"""

import contextlib
import ctypes
from datetime import datetime
from pathlib import Path
import traceback


def main():
    # __file__ es la ruta de este archivo. Resolverla y tomar su carpeta hace
    # que el registro se guarde junto al proyecto, independientemente de la
    # carpeta de trabajo con la que Windows haya iniciado el proceso.
    registro = Path(__file__).resolve().parent / "logs" / "aplicacion.log"
    try:
        # El directorio de logs puede no existir en una copia nueva del
        # proyecto, por eso se crea junto con sus carpetas padre.
        registro.parent.mkdir(parents=True, exist_ok=True)

        # Mantener acotado el registro entre ejecuciones.
        if registro.exists() and registro.stat().st_size > 5 * 1024 * 1024:
            # replace conserva el archivo anterior con un nombre conocido y
            # permite comenzar un registro nuevo en el siguiente open().
            registro.replace(registro.with_suffix(".anterior.log"))

        # buffering=1 solicita escritura con vaciado frecuente del texto. Si
        # la aplicación se cierra inesperadamente, los últimos mensajes tienen
        # más posibilidades de quedar disponibles para el diagnóstico.
        with registro.open("a", encoding="utf-8", buffering=1) as salida:
            # Durante el bloque, print() y los mensajes de error se escriben
            # en el registro en lugar de intentar mostrarse en una consola.
            with contextlib.redirect_stdout(salida), contextlib.redirect_stderr(salida):
                # Marca cada sesión para separar los arranques y facilitar la
                # lectura del historial cuando se revisa el archivo manualmente.
                print(f"\n--- Inicio {datetime.now():%Y-%m-%d %H:%M:%S} ---")
                try:
                    # Se reutiliza el mismo main() del modo con consola. Así
                    # ambos lanzadores mantienen exactamente el mismo arranque
                    # y solo difieren en la forma de mostrar los errores.
                    from iniciar import main as abrir_aplicacion
                    resultado = abrir_aplicacion()
                except Exception:
                    # traceback.print_exc() escribe la excepción completa,
                    # incluyendo su tipo, mensaje y la cadena de llamadas.
                    traceback.print_exc()
                    resultado = 1

        # Un resultado distinto de cero indica un arranque fallido. Como no
        # hay consola visible, se muestra un aviso gráfico que dirige al
        # usuario hacia el archivo con los detalles técnicos.
        if resultado:
            ctypes.windll.user32.MessageBoxW(
                None,
                f"No se pudo iniciar la aplicación.\n\nRevisa el registro:\n{registro}\n\n"
                "Si faltan dependencias, ejecuta instalar.cmd.",
                "Depurador Trucking", 16,
            )
        return resultado
    except Exception as error:
        # Este bloque cubre fallos todavía más tempranos, por ejemplo falta de
        # permisos para crear logs o errores al abrir el archivo de registro.
        # En ese caso no se puede confiar en el propio log, por lo que el error
        # se comunica directamente mediante una ventana de Windows.
        ctypes.windll.user32.MessageBoxW(
            None, f"No se pudo iniciar la aplicación o guardar su registro:\n{error}",
            "Depurador Trucking", 16,
        )
        return 1


if __name__ == "__main__":
    # Permite ejecutar este archivo directamente y propaga el código de salida
    # al proceso que lo lanzó, aunque normalmente se inicia desde iniciar.vbs.
    raise SystemExit(main())
