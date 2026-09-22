import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from depurador import ejecutar_depuracion
from depuracion.representantes import cargar_filtros


class ArchivosAuxiliaresTests(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)
        self.carpeta = Path(self.temporal.name)
        self.base = self.carpeta / "base.xlsx"
        pd.DataFrame({
            "DOT": [123, 456, 789],
            "Legal_Name": ["Empresa A", "Empresa B", "Empresa C"],
            "Phone": ["3055551234"] * 3,
            "Company_Rep1": ["Juan", "Ana", "Maria"],
        }).to_excel(self.base, index=False)
        self.data = self.carpeta / "CRM elegido.xlsx"
        self.filtros = self.carpeta / "Nombres elegidos.xlsx"
        self.excel = self.carpeta / "resultado.xlsx"
        self.csv = self.carpeta / "resultado.csv"

    def ejecutar(self):
        with (
            patch("depuracion.cruces.buscar_archivo_data", side_effect=AssertionError("No buscar automáticamente")),
            patch("depuracion.representantes.buscar_archivo_filtros", side_effect=AssertionError("No buscar automáticamente")),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            return ejecutar_depuracion(
                self.base, self.excel, self.csv,
                confirmar_columnas_faltantes=lambda columnas: True,
                archivo_data=self.data, archivo_filtros=self.filtros,
            )

    def test_archivos_elegidos_determinan_el_resultado_y_las_salidas(self):
        for dot, nombre, esperado in ((123, "Ana", "456"), (456, "Maria", "789")):
            with self.subTest(dot=dot, nombre=nombre):
                pd.DataFrame({"general_info.dot": [dot], "stage": ["Contactado"]}).to_excel(self.data, index=False)
                pd.DataFrame([nombre]).to_excel(self.filtros, index=False, header=False)
                base, montaje, rechazos = self.ejecutar()
                self.assertEqual(montaje.DOT.tolist(), [esperado])
                self.assertEqual(len(montaje) + len(rechazos), len(base))
                salida = pd.read_csv(self.csv, sep=";", dtype=str)
                self.assertEqual(salida.ID.tolist(), [esperado])
                self.assertTrue(self.excel.exists())

    def test_data_sin_columnas_requeridas_no_exporta(self):
        pd.DataFrame({"DOT": [123]}).to_excel(self.data, index=False)
        with self.assertRaisesRegex(ValueError, "columnas necesarias"):
            self.ejecutar()
        self.assertFalse(self.excel.exists())
        self.assertFalse(self.csv.exists())

    def test_ruta_elegida_inexistente_no_busca_otro_archivo(self):
        with self.assertRaises(FileNotFoundError):
            self.ejecutar()

    def test_catalogo_vacio_no_rechaza_toda_la_base_silenciosamente(self):
        pd.DataFrame(["   "]).to_excel(self.filtros, index=False, header=False)
        with self.assertRaisesRegex(ValueError, "no contiene nombres"):
            cargar_filtros(self.filtros)

    def test_catalogo_csv_con_nombre_libre(self):
        archivo = self.carpeta / "Mi catalogo.csv"
        archivo.write_text("José\nAna\n", encoding="utf-8")
        with patch("depuracion.representantes.buscar_archivo_filtros", side_effect=AssertionError):
            self.assertEqual(cargar_filtros(archivo), {"jose", "ana"})


if __name__ == "__main__":
    unittest.main()
