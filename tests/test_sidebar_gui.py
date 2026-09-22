"""Comprueba la imagen lateral con diferentes escalas y tamaños de ventana."""

import os
import unittest


@unittest.skipUnless(os.environ.get("DEPURADOR_TEST_GUI") == "1", "Requiere escritorio")
class SidebarGuiTests(unittest.TestCase):
    def test_imagen_sin_doble_escalado_y_panel_compacto(self):
        import customtkinter as ctk
        from interfaz.ventana import Aplicacion

        # Permite simular el modo ancho incluso en el escritorio de pruebas
        # de baja resolución; el escalado de widgets se prueba por separado.
        ctk.set_window_scaling(0.65)
        app = Aplicacion()
        app.update()
        def estabilizar():
            listo = ctk.BooleanVar(value=False)
            app.after(350, lambda: listo.set(True))
            app.wait_variable(listo)
            app.update_idletasks()
        try:
            app.minsize(400, 300)
            for escala in (1.0, 1.25, 1.5):
                with self.subTest(escala=escala):
                    ctk.set_widget_scaling(escala)
                    app.geometry("1100x600")
                    estabilizar()
                    app.actualizar_sidebar(type("Tamano", (), {
                        "width": app.sidebar.winfo_width(),
                        "height": app.sidebar.winfo_height(),
                    })())
                    ancho, alto = app.imagen_sidebar_ctk.cget("size")
                    factor = app.label_sidebar._get_widget_scaling()
                    self.assertAlmostEqual(ancho * factor, app.sidebar.winfo_width(), delta=1)
                    self.assertAlmostEqual(alto * factor, app.sidebar.winfo_height(), delta=1)
                    self.assertTrue(app.sidebar.winfo_ismapped(), f"width={app.winfo_width()}, scale={app._get_window_scaling()}, geometry={app.geometry()}, manager={app.sidebar.winfo_manager()}")
            app.geometry("800x500")
            estabilizar()
            self.assertFalse(app.sidebar.winfo_ismapped())
            self.assertTrue(app.contenedor_principal.winfo_ismapped())
            app.geometry("1100x600")
            estabilizar()
            self.assertTrue(app.sidebar.winfo_ismapped())
        finally:
            ctk.set_widget_scaling(1.0)
            ctk.set_window_scaling(1.0)
            app.destroy()


if __name__ == "__main__":
    unittest.main()
