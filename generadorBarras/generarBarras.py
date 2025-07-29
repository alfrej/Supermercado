import os
from barcode import EAN13
from barcode.writer import ImageWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from io import BytesIO
from PIL import Image

def generar_imagen_ean13_recortada(texto, ancho_px=360, alto_max_px=150):
    """Genera imagen PIL del código EAN13 recortando si es muy alto"""
    if not texto.isdigit() or len(texto) != 12:
        raise ValueError("EAN-13 requiere exactamente 12 dígitos numéricos.")

    barcode = EAN13(texto, writer=ImageWriter())
    buffer = BytesIO()
    barcode.write(buffer, options={
        'module_height': 30.0,
        'quiet_zone': 0.5
    })
    buffer.seek(0)
    imagen = Image.open(buffer).convert("RGB")

    # Escalado al ancho deseado
    proporcion = imagen.height / imagen.width
    nuevo_ancho = ancho_px
    nuevo_alto = int(nuevo_ancho * proporcion)
    imagen = imagen.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)

    # Recorte si excede alto máximo
    if nuevo_alto > alto_max_px:
        y_inicio = nuevo_alto - alto_max_px  # recortar por arriba
        imagen = imagen.crop((0, y_inicio, nuevo_ancho, nuevo_alto))

    # Convertir a ImageReader
    buffer_recorte = BytesIO()
    imagen.save(buffer_recorte, format="PNG")
    buffer_recorte.seek(0)
    return ImageReader(buffer_recorte)

def generar_pdf_ean13(desde, hasta, nombre_pdf="codigos_ean13.pdf"):
    c = canvas.Canvas(nombre_pdf, pagesize=A4)
    ancho_pagina, alto_pagina = A4

    etiqueta_ancho = 4 * cm
    etiqueta_alto = 3 * cm
    margen = 1 * cm

    barcode_ancho_cm = etiqueta_ancho * 0.9          # 90% del ancho
    barcode_alto_cm = etiqueta_alto * 0.75           # máx 75% del alto

    barcode_px_ancho = 360  # para buen render
    barcode_px_alto_max = int(barcode_px_ancho * (barcode_alto_cm / barcode_ancho_cm))

    x = margen
    y = alto_pagina - margen - etiqueta_alto

    for id_num in range(desde, hasta + 1):
        id_str = str(id_num).zfill(12)
        try:
            imagen_reader = generar_imagen_ean13_recortada(id_str, barcode_px_ancho, barcode_px_alto_max)
        except ValueError as e:
            print(f"❌ Error con ID {id_str}: {e}")
            continue

        # Dibuja el marco
        c.rect(x, y, etiqueta_ancho, etiqueta_alto)

        # Título superior
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(x + etiqueta_ancho / 2, y + etiqueta_alto - 8, "Mi Súper")

        # Coordenadas para el código de barras
        barcode_x = x + (etiqueta_ancho - barcode_ancho_cm) / 2
        barcode_y = y + (etiqueta_alto - barcode_alto_cm) / 2 - 2  # bajado un poco (2 pts)

        c.drawImage(
            imagen_reader,
            barcode_x,
            barcode_y,
            width=barcode_ancho_cm,
            height=barcode_alto_cm,
            preserveAspectRatio=False
        )

        # Línea inferior
        c.setLineWidth(0.3)
        c.line(x + 4, y + 4, x + etiqueta_ancho - 4, y + 4)

        # Siguiente posición
        x += etiqueta_ancho
        if x + etiqueta_ancho > ancho_pagina - margen:
            x = margen
            y -= etiqueta_alto
            if y < margen:
                c.showPage()
                x = margen
                y = alto_pagina - margen - etiqueta_alto

    c.save()
    print(f"✅ PDF generado: {nombre_pdf}")

if __name__ == "__main__":
    desde = int(input("Desde ID (número entero): "))
    hasta = int(input("Hasta ID (número entero): "))
    generar_pdf_ean13(desde, hasta)
