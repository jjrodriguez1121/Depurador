import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from depuracion.carga_datos import cargar_archivo, preparar_base
from depurador import ejecutar_depuracion


class LecturaCsvTests(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)
        self.archivo = Path(self.temporal.name) / "base.csv"

    def leer(self, texto, encoding="utf-8"):
        self.archivo.write_text(texto, encoding=encoding, newline="")
        return cargar_archivo(self.archivo)

    def test_coma_y_punto_coma(self):
        for separador in (",", ";"):
            with self.subTest(separador=separador):
                base = self.leer(f"DOT{separador}Phone\n123{separador}3055551234\n")
                self.assertEqual(list(base.columns), ["DOT", "Phone"])
                self.assertEqual(base.iloc[0]["DOT"], "123")

    def test_comillas_separadores_salto_de_linea_y_comillas_dobles(self):
        for separador in (",", ";"):
            with self.subTest(separador=separador):
                base = self.leer(
                    f'DOT{separador}Legal_Name\n123{separador}"ABC, Inc; ""Norte""\nLLC"\n'
                )
                self.assertEqual(base.iloc[0]["Legal_Name"], 'ABC, Inc; "Norte"\nLLC')
                self.assertEqual(len(base), 1)

    def test_utf8_bom_y_acentos(self):
        base = self.leer("DOT;Legal_Name\n123;Transportes José\n", "utf-8-sig")
        self.assertEqual(list(base.columns), ["DOT", "Legal_Name"])
        self.assertEqual(base.iloc[0]["Legal_Name"], "Transportes José")

    def test_saltos_windows_dentro_de_comillas_se_conservan(self):
        base = self.leer('DOT;Legal_Name\r\n123;"ABC\r\nLLC"\r\n')
        self.assertEqual(base.iloc[0]["Legal_Name"], "ABC\r\nLLC")

    def test_campos_vacios_explicitos_y_lineas_vacias(self):
        base = self.leer("\nDOT;Phone\n123;\n\n456;3055551234\n")
        self.assertEqual(len(base), 2)
        self.assertTrue(base["Phone"].isna().iloc[0])

    def test_una_columna_y_columnas_faltantes_conservan_el_aviso(self):
        for texto in ("DOT\n123\n", "DOT;Phone\n123;3055551234\n"):
            with self.subTest(texto=texto):
                confirmar = Mock(return_value=True)
                base = preparar_base(self.leer(texto), confirmar)
                confirmar.assert_called_once()
                self.assertNotIn("DOT", confirmar.call_args.args[0])
                self.assertTrue(base["Email"].isna().all())

    def test_filas_con_campos_de_mas_o_de_menos(self):
        for separador in (",", ";"):
            for fila in ("123", f"123{separador}3055551234{separador}extra"):
                with self.subTest(separador=separador, fila=fila):
                    with self.assertRaisesRegex(ValueError, "línea 2"):
                        self.leer(f"DOT{separador}Phone\n{fila}\n")

    def test_comillas_sin_cerrar(self):
        with self.assertRaisesRegex(ValueError, "comillas"):
            self.leer('DOT;Legal_Name\n123;"Nombre incompleto\n')

    def test_separador_ambiguo(self):
        with self.assertRaisesRegex(ValueError, "seguridad el separador"):
            self.leer("DOT,Phone;Email\n123,3055551234;a@b.com\n")

    def test_archivo_vacio(self):
        with self.assertRaisesRegex(ValueError, "vacío"):
            self.leer("\n\n")

    def test_separador_no_admitido_no_se_confunde_con_columnas_ausentes(self):
        for separador in ("\t", "|"):
            with self.subTest(separador=separador):
                with self.assertRaisesRegex(ValueError, "separador distinto"):
                    self.leer(f"DOT{separador}Phone\n123{separador}3055551234\n")

    def test_caracter_nulo_no_se_trunca_silenciosamente(self):
        with self.assertRaisesRegex(ValueError, "caracteres nulos"):
            self.leer("DOT;Legal_Name\n123;ABC\x00DEF\n")

    def test_codificacion_incorrecta_tiene_mensaje_claro(self):
        with self.assertRaisesRegex(ValueError, "CSV UTF-8"):
            self.leer("DOT;Legal_Name\n123;José\n", "cp1252")

    def test_csv_invalido_se_detiene_antes_de_confirmar_o_exportar(self):
        self.archivo.write_text("DOT;Phone\n123;3055551234;extra\n", encoding="utf-8")
        excel = self.archivo.with_suffix(".xlsx")
        csv = self.archivo.parent / "salida.csv"
        confirmar = Mock(return_value=True)
        with (
            patch("depurador.procesar_telefonos") as telefonos,
            patch("depurador.exportar_excel") as exportar,
            contextlib.redirect_stdout(io.StringIO()),
            self.assertRaises(ValueError),
        ):
            ejecutar_depuracion(self.archivo, excel, csv, confirmar_columnas_faltantes=confirmar)
        confirmar.assert_not_called()
        telefonos.assert_not_called()
        exportar.assert_not_called()
        self.assertFalse(excel.exists())
        self.assertFalse(csv.exists())


if __name__ == "__main__":
    unittest.main()
