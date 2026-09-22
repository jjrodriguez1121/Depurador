import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from depuracion.carga_datos import (
    cargar_archivo, preparar_base, crear_montaje, agregar_fecha_montaje,
    crear_rechazos, agregar_motivo_rechazo,
)
from depuracion.cruces import validar_dot, procesar_cruces


class DotTests(unittest.TestCase):
    def preparar(self, valores):
        base = preparar_base(pd.DataFrame({"DOT": valores}), lambda columnas: True)
        montaje = agregar_fecha_montaje(crear_montaje(base), "21/09/2026")
        rechazos = agregar_motivo_rechazo(crear_rechazos(montaje))
        return montaje, rechazos

    def test_validos_se_normalizan_y_no_se_modifica_original(self):
        montaje, rechazos = self.preparar(["1234567", " 2345678 ", "3456789.0", 4567890.0, "00123"])
        original = montaje.copy()
        aceptados, descartados = validar_dot(montaje, rechazos)
        self.assertEqual(aceptados.DOT.tolist(), ["1234567", "2345678", "3456789", "4567890", "00123"])
        self.assertTrue(descartados.empty)
        pd.testing.assert_frame_equal(montaje, original)

    def test_vacios_e_invalidos_tienen_motivos_y_valores_originales(self):
        valores = [None, pd.NA, float("nan"), "", "  ", "ABC123", "123-456", "+123", "12.5", ".0", "１２３", "1e3"]
        montaje, rechazos = self.preparar(valores)
        aceptados, descartados = validar_dot(montaje, rechazos)
        self.assertTrue(aceptados.empty)
        self.assertEqual(descartados["Motivo Rechazo"].tolist(), ["DOT invalido"] * 12)
        self.assertEqual(descartados.DOT.iloc[5:].tolist(), valores[5:])
        self.assertEqual(len(descartados), len(montaje))

    def test_montaje_vacio(self):
        montaje, rechazos = self.preparar([])
        aceptados, descartados = validar_dot(montaje, rechazos)
        self.assertTrue(aceptados.empty)
        self.assertTrue(descartados.empty)
        self.assertIn("DOT", aceptados.columns)

    def test_columna_dot_creada_vacia_se_rechaza(self):
        base = preparar_base(pd.DataFrame({"Legal_Name": ["ABC", "DEF"]}), lambda columnas: True)
        montaje = agregar_fecha_montaje(base.copy(), "21/09/2026")
        aceptados, descartados = validar_dot(montaje, agregar_motivo_rechazo(crear_rechazos(montaje)))
        self.assertTrue(aceptados.empty)
        self.assertEqual(descartados["Motivo Rechazo"].tolist(), ["DOT invalido", "DOT invalido"])

    def test_validacion_precede_duplicados_y_cruce(self):
        montaje, rechazos = self.preparar(["ABC", "ABC", "123.0", "123", "456", "789", None])
        data = pd.DataFrame({"general_info.dot": [456], "stage": ["Contactado"]})
        with (
            patch("depuracion.cruces.buscar_archivo_data", return_value=Path("data.csv")),
            patch("depuracion.cruces.cargar_data", return_value=data),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            aceptados, descartados = procesar_cruces(montaje, rechazos)
        self.assertEqual(aceptados.DOT.tolist(), ["123", "789"])
        self.assertEqual(descartados["Motivo Rechazo"].tolist(), [
            "DOT invalido", "DOT invalido", "DOT invalido",
            "Repetido en misma base", "Contactado",
        ])
        self.assertEqual(len(aceptados) + len(descartados), len(montaje))

    def test_lectura_no_convierte_signos_o_notacion_cientifica_en_dot_valido(self):
        with tempfile.TemporaryDirectory() as carpeta:
            for extension in ("csv", "xlsx"):
                with self.subTest(extension=extension):
                    archivo = Path(carpeta) / f"base.{extension}"
                    valores = ["+123", "1e3", "00123"]
                    if extension == "csv":
                        archivo.write_text("DOT\n" + "\n".join(valores), encoding="utf-8")
                    else:
                        pd.DataFrame({"DOT": valores}).to_excel(archivo, index=False)
                    base = cargar_archivo(archivo)
                    self.assertEqual(base.DOT.tolist(), valores)
                    montaje, rechazos = self.preparar(base.DOT.tolist())
                    aceptados, descartados = validar_dot(montaje, rechazos)
                    self.assertEqual(aceptados.DOT.tolist(), ["00123"])
                    self.assertEqual(len(descartados), 2)


if __name__ == "__main__":
    unittest.main()
