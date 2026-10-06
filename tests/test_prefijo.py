import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd

from depurador import ejecutar_depuracion
from interfaz.proceso import GestorProceso


class PrefijoTests(unittest.TestCase):
    def test_prefijos_en_excel_csv_respaldo_y_base_original(self):
        for prefijo in (None, "57", "009"):
            with self.subTest(prefijo=prefijo), tempfile.TemporaryDirectory() as temporal:
                carpeta = Path(temporal)
                origen, data, filtros, excel, csv = [
                    carpeta / nombre for nombre in
                    ("base.csv", "data.csv", "filtros.csv", "salida.xlsx", "salida.csv")
                ]
                pd.DataFrame({
                    "DOT": ["123", "456", "789"],
                    "Phone": ["3055551234", "", "mal"],
                    "Cell_Num": ["3055559999", "3055555678", ""],
                    "Company_Rep1": ["Juan"] * 3,
                }).to_csv(origen, index=False)
                data.write_text("general_info.dot,stage\n999,Contactado\n", encoding="utf-8")
                filtros.write_text("Juan\n", encoding="utf-8")
                opciones = {} if prefijo is None else {"prefijo": prefijo}
                with contextlib.redirect_stdout(io.StringIO()):
                    base, montaje, rechazos = ejecutar_depuracion(
                        origen, excel, csv, archivo_data=data, archivo_filtros=filtros,
                        confirmar_columnas_faltantes=lambda _: True, **opciones,
                    )
                esperado = [(prefijo or "9") + numero for numero in ("3055551234", "3055555678")]
                self.assertEqual(montaje.Phone.tolist(), esperado)
                self.assertEqual(base.Phone.tolist(), ["3055551234", "", "mal"])
                self.assertEqual(montaje.Cell_Num.tolist(), ["3055559999", "3055555678"])
                self.assertEqual(rechazos["Motivo Rechazo"].tolist(), ["Sin teléfono"])
                salida = pd.read_excel(excel, sheet_name="Montaje Español", dtype=str)
                self.assertEqual(salida.Phone.tolist(), esperado)
                salida = pd.read_csv(csv, sep=";", dtype=str)
                self.assertEqual(salida.TEL1.tolist(), esperado)

    def test_prefijo_invalido_impide_leer_o_exportar(self):
        for prefijo in ("", " ", " 9", "+57", "9.0", "a", "９", None, 9):
            with self.subTest(prefijo=prefijo), patch("depurador.cargar_y_preparar_datos") as cargar:
                with self.assertRaisesRegex(ValueError, "prefijo telefónico"):
                    ejecutar_depuracion("base", "excel", "csv", prefijo=prefijo)
                cargar.assert_not_called()

    def gestor(self, prefijo):
        gestor = GestorProceso.__new__(GestorProceso)
        gestor.parent = MagicMock()
        gestor.proceso_en_ejecucion = False
        gestor.obtener_rutas = lambda: ("base", "excel", "csv", "data", "filtros")
        gestor.entrada_prefijo = MagicMock()
        gestor.entrada_prefijo.get.return_value = prefijo
        gestor.actualizar_criterio_coincidencias = MagicMock()
        gestor.reiniciar_progreso = MagicMock()
        gestor.actualizar_estado_exterior = MagicMock()
        gestor.boton_iniciar = MagicMock()
        gestor.label_progreso = MagicMock()
        return gestor

    def test_interfaz_avisa_y_no_inicia_con_prefijo_invalido(self):
        gestor = self.gestor("+57")
        with patch("interfaz.proceso.mostrar_advertencia") as aviso, patch("interfaz.proceso.threading.Thread") as hilo:
            gestor.iniciar_depuracion()
        self.assertEqual(aviso.call_args.args[1], "Prefijo inválido")
        hilo.assert_not_called()

    def test_interfaz_fija_prefijo_y_lo_envia_al_motor(self):
        gestor = self.gestor("009")
        gestor.minimo_coincidencias = 1
        with patch("interfaz.proceso.solicitar_confirmacion", return_value=True) as confirmar, patch("interfaz.proceso.threading.Thread"):
            gestor.iniciar_depuracion()
        self.assertIn("009", confirmar.call_args.args[2])
        gestor.entrada_prefijo.configure.assert_called_with(state="disabled")
        gestor.entrada_prefijo.get.return_value = "57"
        with patch("interfaz.proceso.ejecutar_depuracion", return_value=([], [], [])) as ejecutar:
            gestor.ejecutar_proceso()
        self.assertEqual(ejecutar.call_args.kwargs["prefijo"], "009")
        gestor.proceso_cancelado()
        gestor.entrada_prefijo.configure.assert_called_with(state="normal")
