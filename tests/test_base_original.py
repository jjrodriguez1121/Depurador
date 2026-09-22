import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import pandas as pd
from openpyxl import load_workbook

from depurador import ejecutar_depuracion
from depuracion.carga_datos import cargar_y_preparar_datos


class BaseOriginalTests(unittest.TestCase):
    def test_preparacion_no_agrega_ni_quita_columnas_de_base(self):
        with tempfile.TemporaryDirectory() as carpeta:
            origen = Path(carpeta) / "entrada.csv"
            origen.write_text(
                'DOT;Observaciones;Codigo;Policy_Effective_Date\n'
                '00123;NA;0007;fecha pendiente\n', encoding="utf-8"
            )
            with contextlib.redirect_stdout(io.StringIO()):
                base, montaje, _, _, _ = cargar_y_preparar_datos(origen, lambda faltantes: True)
            self.assertEqual(list(base.columns), ["DOT", "Observaciones", "Codigo", "Policy_Effective_Date"])
            self.assertEqual(base.iloc[0].tolist(), ["00123", "NA", "0007", "fecha pendiente"])
            self.assertIn("Phone", montaje.columns)
            self.assertNotIn("Phone", base.columns)
            montaje.loc[0, "DOT"] = "999"
            self.assertEqual(base.loc[0, "DOT"], "00123")

    def test_excel_y_csv_conservan_base_y_exportan_montaje_espanol(self):
        for extension in ("csv", "xlsx"):
            with self.subTest(extension=extension), tempfile.TemporaryDirectory() as carpeta:
                carpeta = Path(carpeta)
                origen = carpeta / f"entrada.{extension}"
                original = pd.DataFrame({
                    "DOT": ["00123", "00456"],
                    "Legal_Name": ["José & Hijos", "Ana Transportes"],
                    "Phone": ["(305) 555-1234", "(305) 555-5678"],
                    "Company_Rep1": ["Juan", "Ana"],
                    "Policy_Effective_Date": ["fecha pendiente", "03/25/2026"],
                    "Observaciones": ["NA", "=texto literal"],
                    "Codigo extra": ["0007", "0008"],
                })
                if extension == "csv":
                    original.to_csv(origen, sep=";", index=False, encoding="utf-8-sig")
                else:
                    original.to_excel(origen, index=False)
                    # La celda de observación del origen es un texto, no fórmula.
                    libro = load_workbook(origen)
                    libro.active["F3"].data_type = "s"
                    libro.save(origen)
                    libro.close()
                contenido_original = origen.read_bytes()
                data = carpeta / "data.csv"
                data.write_text("general_info.dot,stage\n999,Contactado\n", encoding="utf-8")
                filtros = carpeta / "filtros.csv"
                filtros.write_text("Juan\nAna\n", encoding="utf-8")
                destino = carpeta / "resultado.xlsx"
                csv = carpeta / "resultado.csv"
                with contextlib.redirect_stdout(io.StringIO()):
                    base, montaje, rechazos = ejecutar_depuracion(
                        origen, destino, csv,
                        confirmar_columnas_faltantes=lambda faltantes: True,
                        archivo_data=data, archivo_filtros=filtros,
                    )
                pd.testing.assert_frame_equal(base, original, check_dtype=False)
                self.assertEqual(origen.read_bytes(), contenido_original)
                with pd.ExcelFile(destino) as libro:
                    self.assertEqual(libro.sheet_names, ["Base", "Montaje Español", "Rechazos"])
                    base_salida = pd.read_excel(libro, sheet_name="Base", dtype=str, keep_default_na=False)
                pd.testing.assert_frame_equal(base_salida, original)
                self.assertEqual(montaje.Phone.tolist(), ["93055551234", "93055555678"])
                self.assertEqual(len(base), len(montaje) + len(rechazos))
                salida_csv = pd.read_csv(csv, sep=";", dtype=str, keep_default_na=False)
                self.assertEqual(len(salida_csv), 2)
                self.assertEqual(salida_csv.ID.tolist(), ["00123", "00456"])
                self.assertNotIn("Codigo extra", montaje.columns)


if __name__ == "__main__":
    unittest.main()
