"""Pruebas con ventanas reales: activar con DEPURADOR_TEST_GUI=1."""

import os
import unittest


@unittest.skipUnless(
    os.environ.get("DEPURADOR_TEST_GUI") == "1",
    "Las pruebas de ventanas requieren DEPURADOR_TEST_GUI=1",
)
class ConfirmacionGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import customtkinter as ctk
        cls.ctk = ctk
        cls.root = ctk.CTk()
        cls.root.title("Prueba automática del aviso de columnas")
        cls.root.geometry("600x200+40+40")
        cls.root.update()

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def comprobar_respuesta(self, accion, esperado, dialogo=None, contenido=None, confirmacion=True):
        from depuracion.carga_datos import COLUMNAS_NECESARIAS
        from interfaz.confirmacion import confirmar_columnas_faltantes

        errores = []
        accion_ejecutada = []

        def descendientes(widget):
            for hijo in widget.winfo_children():
                yield hijo
                yield from descendientes(hijo)

        def responder():
            ventanas = [
                widget for widget in self.root.winfo_children()
                if isinstance(widget, self.ctk.CTkToplevel)
            ]
            if not ventanas:
                self.root.after(50, responder)
                return
            ventana = ventanas[0]
            try:
                widgets = list(descendientes(ventana))
                lista = next(w for w in widgets if isinstance(w, self.ctk.CTkTextbox))
                texto = lista.get("1.0", "end")
                if contenido is None:
                    for columna in COLUMNAS_NECESARIAS:
                        self.assertIn(columna, texto)
                else:
                    self.assertEqual(texto.rstrip("\n"), contenido)
                self.assertEqual(lista.cget("state"), "disabled")
                botones = [w for w in widgets if isinstance(w, self.ctk.CTkButton)]
                self.assertEqual(len(botones), 2 if confirmacion else 1)
                for boton in botones:
                    self.assertTrue(boton.winfo_ismapped())
                    self.assertLessEqual(
                        boton.winfo_rooty() + boton.winfo_height(),
                        ventana.winfo_rooty() + ventana.winfo_height(),
                    )
                if accion == "cerrar":
                    ventana.tk.call(ventana.protocol("WM_DELETE_WINDOW"))
                elif accion == "escape":
                    ventana.focus_force()
                    ventana.event_generate("<Escape>")
                else:
                    boton = next(
                        w for w in widgets
                        if isinstance(w, self.ctk.CTkButton)
                        and w.cget("text") == accion
                    )
                    self.assertTrue(boton.winfo_ismapped())
                    boton.invoke()
                accion_ejecutada.append(accion)
            except Exception as error:
                errores.append(error)
                ventana.destroy()

        def agotar_tiempo():
            errores.append(AssertionError("El aviso no respondió en 10 segundos"))
            for widget in self.root.winfo_children():
                if isinstance(widget, self.ctk.CTkToplevel):
                    widget.destroy()

        limite = self.root.after(10000, agotar_tiempo)
        self.root.after(500, responder)
        resultado = (
            dialogo(self.root) if dialogo is not None
            else confirmar_columnas_faltantes(self.root, COLUMNAS_NECESARIAS)
        )
        self.root.after_cancel(limite)
        if errores:
            raise errores[0]
        self.assertEqual(accion_ejecutada, [accion])
        self.assertIs(resultado, esperado)
        self.assertIsNone(self.root.grab_current())

    def test_continuar(self):
        self.comprobar_respuesta("Continuar", True)

    def test_cancelar(self):
        self.comprobar_respuesta("Cancelar", False)

    def test_cerrar_equivale_a_cancelar(self):
        self.comprobar_respuesta("cerrar", False)

    def test_avisos_comparten_boton_aceptar_y_conservan_texto_largo(self):
        from interfaz.confirmacion import (
            mostrar_advertencia, mostrar_error, mostrar_exito, mostrar_mensaje,
        )
        contenido = "Detalle de la operación\n" + "Ruta con espacios y acentos: depuración/" * 40
        for funcion in (mostrar_advertencia, mostrar_error, mostrar_exito, mostrar_mensaje):
            with self.subTest(tipo=funcion.__name__):
                self.comprobar_respuesta(
                    "Aceptar", True,
                    dialogo=lambda parent: funcion(parent, "Resultado", contenido),
                    contenido=contenido, confirmacion=False,
                )

    def test_confirmacion_de_salida(self):
        from interfaz.confirmacion import solicitar_confirmacion
        for accion, esperado in (("Salir", True), ("Cancelar", False), ("cerrar", False), ("escape", False)):
            with self.subTest(accion=accion):
                self.comprobar_respuesta(
                    accion, esperado,
                    dialogo=lambda parent: solicitar_confirmacion(
                        parent, "Salir", "¿Deseas cerrar la aplicación?", texto_confirmar="Salir"
                    ),
                    contenido="¿Deseas cerrar la aplicación?",
                )

    def test_selectores_auxiliares_conservan_rutas_y_cancelar_no_las_borra(self):
        from pathlib import Path
        from unittest.mock import patch
        from interfaz.archivos import GestorArchivos
        frame = self.ctk.CTkFrame(self.root)
        frame.pack(fill="both", expand=True)
        try:
            gestor = GestorArchivos(frame)
            for tipo, ruta in (("data", "C:/pruebas/CRM elegido.xlsx"), ("filtros", "C:/pruebas/Nombres.csv")):
                with patch("interfaz.archivos.filedialog.askopenfilename", return_value=ruta):
                    gestor.seleccionar_archivo(tipo)
                entrada = getattr(gestor, f"entrada_{tipo}")
                self.assertEqual(entrada.get(), str(Path(ruta)))
                self.assertEqual(entrada.cget("state"), "readonly")
                with patch("interfaz.archivos.filedialog.askopenfilename", return_value=""):
                    gestor.seleccionar_archivo(tipo)
                self.assertEqual(getattr(gestor, f"archivo_{tipo}"), Path(ruta))
            self.assertEqual(gestor.obtener_rutas()[3:], (Path("C:/pruebas/CRM elegido.xlsx"), Path("C:/pruebas/Nombres.csv")))
            self.assertFalse(gestor.rutas_completas())
        finally:
            frame.destroy()


if __name__ == "__main__":
    unittest.main()
