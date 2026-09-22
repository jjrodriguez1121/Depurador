import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd

from depuracion.carga_datos import (
    COLUMNAS_NECESARIAS,
    DepuracionCancelada,
    preparar_base,
)
from depurador import ejecutar_depuracion


class ColumnasEntradaTests(unittest.TestCase):
    def test_base_completa_no_pide_confirmacion(self):
        base = pd.DataFrame({columna: ["dato"] for columna in COLUMNAS_NECESARIAS})
        confirmar = Mock()
        resultado = preparar_base(base.copy(), confirmar)
        confirmar.assert_not_called()
        pd.testing.assert_frame_equal(resultado, base)

    def test_continuar_crea_solo_faltantes_vacias(self):
        base = pd.DataFrame({"DOT": [123, 456], "Phone": ["3055551234", ""]})
        faltantes = [c for c in COLUMNAS_NECESARIAS if c not in base.columns]
        confirmar = Mock(return_value=True)
        resultado = preparar_base(base.copy(), confirmar)
        confirmar.assert_called_once_with(faltantes)
        self.assertEqual(list(resultado.columns), COLUMNAS_NECESARIAS)
        self.assertTrue(resultado[faltantes].isna().all().all())
        pd.testing.assert_frame_equal(resultado[base.columns], base)

    def test_cancelar_no_modifica_la_base(self):
        base = pd.DataFrame({"DOT": [123]})
        original = base.copy()
        with self.assertRaises(DepuracionCancelada):
            preparar_base(base, lambda columnas: False)
        pd.testing.assert_frame_equal(base, original)

    def test_sin_callback_no_se_autoriza_una_base_incompleta(self):
        with self.assertRaisesRegex(ValueError, "Se requiere confirmación"):
            preparar_base(pd.DataFrame({"DOT": [123]}))

    def test_todas_las_columnas_faltantes_se_informan(self):
        confirmar = Mock(return_value=True)
        resultado = preparar_base(pd.DataFrame({"Otra": ["dato"]}), confirmar)
        confirmar.assert_called_once_with(COLUMNAS_NECESARIAS)
        self.assertEqual(len(resultado), 1)
        self.assertTrue(resultado.isna().all().all())

    def test_cancelar_pipeline_no_procesa_ni_sobrescribe_salidas(self):
        with tempfile.TemporaryDirectory() as carpeta:
            carpeta = Path(carpeta)
            origen = carpeta / "entrada.csv"
            excel = carpeta / "resultado.xlsx"
            csv = carpeta / "resultado.csv"
            origen.write_text("DOT\n123\n", encoding="utf-8")
            excel.write_bytes(b"excel anterior")
            csv.write_bytes(b"csv anterior")
            confirmar = Mock(return_value=False)

            with (
                patch("depurador.procesar_telefonos") as telefonos,
                patch("depurador.exportar_excel") as exportar_excel,
                patch("depurador.exportar_csv_desde_montaje") as exportar_csv,
                contextlib.redirect_stdout(io.StringIO()),
                self.assertRaises(DepuracionCancelada),
            ):
                ejecutar_depuracion(
                    origen, excel, csv,
                    confirmar_columnas_faltantes=confirmar,
                )

            confirmar.assert_called_once()
            telefonos.assert_not_called()
            exportar_excel.assert_not_called()
            exportar_csv.assert_not_called()
            self.assertEqual(excel.read_bytes(), b"excel anterior")
            self.assertEqual(csv.read_bytes(), b"csv anterior")
            self.assertEqual(origen.read_text(encoding="utf-8"), "DOT\n123\n")


if __name__ == "__main__":
    unittest.main()
