import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from depuracion.limpieza import (
    limpiar_montaje, limpiar_legal_name, limpiar_company_rep1,
    limpiar_insurer, limpiar_emails,
)
from salida.salida_excel import preparar_exportacion, exportar_excel
from salida.exportador_csv import exportar_csv, exportar_csv_desde_montaje


class ExportacionMemoriaTests(unittest.TestCase):
    def tabla(self):
        return pd.DataFrame({
            "DOT": ["00123", "456"], "Legal_Name": ["Empresa; A", "NA"],
            "Company_Rep1": ["Juan", "Ana"], "Business_State": ["FL", "TX"],
            "Years_In_Business": [2.0, None], "Insurer": ["A", "NULL"],
            "Policy_Effective_Date": ["03/25/2026", "sin fecha"],
            "Policy_Cancellation_Date": [None, "04/25/2026"],
            "Email": ["a@example.com", None], "Power_Units": [1, 3],
            "Phone": ["93055551234", "93055555678"],
        }, index=[2, 7])

    def test_csv_identico_al_generado_desde_excel_sin_releer_archivo(self):
        for vacio in (False, True):
            with self.subTest(vacio=vacio), tempfile.TemporaryDirectory() as carpeta:
                carpeta = Path(carpeta)
                montaje = self.tabla()
                if vacio:
                    montaje = montaje.iloc[:0]
                original = montaje.copy(deep=True)
                with contextlib.redirect_stdout(io.StringIO()):
                    datos = preparar_exportacion(original, montaje, montaje.iloc[:0])
                    exportar_excel(*datos, carpeta / "base.xlsx", datos_preparados=True)
                    exportar_csv(carpeta / "base.xlsx", carpeta / "antes.csv")
                    with patch("pandas.read_excel", side_effect=AssertionError("No releer Excel")):
                        exportar_csv_desde_montaje(datos[1], carpeta / "despues.csv")
                self.assertEqual((carpeta / "antes.csv").read_bytes(), (carpeta / "despues.csv").read_bytes())
                pd.testing.assert_frame_equal(montaje, original)

    def test_limpieza_una_copia_mantiene_resultado_y_no_modifica_entrada(self):
        entrada = self.tabla()
        entrada.loc[2, "Legal_Name"] = "José & Hijos - LLC"
        entrada.loc[2, "Email"] = " a@example.com; b@example.com "
        original = entrada.copy(deep=True)
        anterior = limpiar_emails(limpiar_insurer(limpiar_company_rep1(limpiar_legal_name(entrada))))
        with contextlib.redirect_stdout(io.StringIO()):
            actual = limpiar_montaje(entrada)
        pd.testing.assert_frame_equal(actual, anterior)
        pd.testing.assert_frame_equal(entrada, original)


if __name__ == "__main__":
    unittest.main()
