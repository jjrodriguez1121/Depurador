r"""Compara exportación CSV desde Excel frente a memoria, con datos sintéticos.

Ejecutar: .venv\Scripts\python.exe benchmarks/exportacion.py --filas 1000 20000
El tiempo excluye escribir el Excel (paso común) y preparar los datos.
La memoria usa tracemalloc: asignaciones Python, no RAM total del proceso.
"""

import argparse
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import time
import tracemalloc
import gc

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
from config import NOMBRE_HOJA_MONTAJE
from salida.exportador_csv import exportar_csv, exportar_csv_desde_montaje


def medir(funcion):
    gc.collect()
    with contextlib.redirect_stdout(io.StringIO()):
        inicio = time.perf_counter()
        funcion()
        segundos = time.perf_counter() - inicio
        gc.collect()
        tracemalloc.start()
        try:
            funcion()
            _, pico = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
    return {"segundos": round(segundos, 3), "pico_python_mib": round(pico / 1024**2, 2)}


def comparar(filas):
    montaje = pd.DataFrame({
        "DOT": [str(1000000 + i) for i in range(filas)],
        "Legal_Name": ["Empresa de transporte"] * filas,
        "Company_Rep1": ["Juan Perez"] * filas,
        "Business_State": ["FL"] * filas,
        "Years_In_Business": [4] * filas,
        "Insurer": ["Aseguradora"] * filas,
        "Policy_Effective_Date": [pd.Timestamp("2026-03-25")] * filas,
        "Policy_Cancellation_Date": [pd.NaT] * filas,
        "Email": ["correo@example.com"] * filas,
        "Power_Units": [3] * filas,
        "Phone": ["93055551234"] * filas,
    })
    with tempfile.TemporaryDirectory() as carpeta:
        carpeta = Path(carpeta)
        excel, anterior, actual = (carpeta / nombre for nombre in ("montaje.xlsx", "anterior.csv", "actual.csv"))
        montaje.to_excel(excel, sheet_name=NOMBRE_HOJA_MONTAJE, index=False, engine="openpyxl")
        antes = medir(lambda: exportar_csv(excel, anterior))
        despues = medir(lambda: exportar_csv_desde_montaje(montaje, actual))
        if anterior.read_bytes() != actual.read_bytes():
            raise AssertionError("Los CSV no coinciden")
        return {"filas": filas, "desde_excel": antes, "desde_memoria": despues, "csv_identicos": True}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--filas", nargs="+", type=int, default=[1000, 20000])
    argumentos = parser.parse_args()
    for cantidad in argumentos.filas:
        if cantidad < 1:
            parser.error("La cantidad de filas debe ser positiva")
        print(json.dumps(comparar(cantidad), ensure_ascii=False), flush=True)
