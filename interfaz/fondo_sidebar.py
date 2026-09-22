"""Composición del panel lateral sin franjas de color ni recorte del original."""

from PIL import Image, ImageColor, ImageFilter


def extender_borde(borde, ancho, lado):
    """Suaviza la extensión hacia fuera sin crear una costura junto a la foto."""
    extension = borde.resize((ancho, borde.height))
    suave = extension.filter(ImageFilter.GaussianBlur(24))
    mascara = Image.new("L", (ancho, 1))
    mascara.putdata([
        round(255 * ((ancho - 1 - i if lado == "izquierdo" else i) / max(1, ancho - 1)) ** 0.5)
        for i in range(ancho)
    ])
    return Image.composite(suave, extension, mascara.resize(extension.size))


def componer_fondo(imagen, ancho, alto, x, y, color_pie):
    """Extiende los píxeles del borde y funde el pie hacia el color del panel."""
    fondo = Image.new("RGB", (ancho, alto), color_pie)
    derecha = x + imagen.width
    inferior = y + imagen.height
    if x:
        borde = imagen.crop((0, 0, 1, imagen.height))
        fondo.paste(extender_borde(borde, x, "izquierdo"), (0, y))
    if derecha < ancho:
        borde = imagen.crop((imagen.width - 1, 0, imagen.width, imagen.height))
        fondo.paste(extender_borde(borde, ancho - derecha, "derecho"), (derecha, y))
    fondo.paste(imagen, (x, y))
    if y:
        borde = fondo.crop((0, y, ancho, y + 1))
        fondo.paste(borde.resize((ancho, y)), (0, 0))
    if inferior < alto:
        borde = fondo.crop((0, inferior - 1, ancho, inferior))
        destino = Image.new("RGB", (ancho, 1), ImageColor.getrgb(color_pie))
        espacio = alto - inferior
        for fila in range(espacio):
            mezcla = fila / max(1, espacio - 1)
            fondo.paste(Image.blend(borde, destino, mezcla), (0, inferior + fila))
    return fondo
