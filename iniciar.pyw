"""Arranque sin consola, con salida y errores en logs/aplicacion.log."""

import contextlib
import ctypes
from datetime import datetime
from pathlib import Path
import traceback


def main():
    registro = Path(__file__).resolve().parent / "logs" / "aplicacion.log"
    try:
        registro.parent.mkdir(parents=True, exist_ok=True)
        # Mantener acotado el registro entre ejecuciones.
        if registro.exists() and registro.stat().st_size > 5 * 1024 * 1024:
            registro.replace(registro.with_suffix(".anterior.log"))
        with registro.open("a", encoding="utf-8", buffering=1) as salida:
            with contextlib.redirect_stdout(salida), contextlib.redirect_stderr(salida):
                print(f"\n--- Inicio {datetime.now():%Y-%m-%d %H:%M:%S} ---")
                try:
                    from iniciar import main as abrir_aplicacion
                    resultado = abrir_aplicacion()
                except Exception:
                    traceback.print_exc()
                    resultado = 1
        if resultado:
            ctypes.windll.user32.MessageBoxW(
                None,
                f"No se pudo iniciar la aplicación.\n\nRevisa el registro:\n{registro}\n\n"
                "Si faltan dependencias, ejecuta instalar.cmd.",
                "Depurador Trucking", 16,
            )
        return resultado
    except Exception as error:
        ctypes.windll.user32.MessageBoxW(
            None, f"No se pudo iniciar la aplicación o guardar su registro:\n{error}",
            "Depurador Trucking", 16,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
