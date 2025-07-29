import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO

# Fuente decorativa opcional
try:
    pdfmetrics.registerFont(TTFont('Fancy', 'LiberationSerif-BoldItalic.ttf'))
    fuente_super = 'Fancy'
except:
    fuente_super = 'Helvetica-Bold'

def generar_qr(id_texto):
    qr = qrcode.QRCode(box_size=10, border=1)
    qr.add_data(id_texto)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return ImageReader(buf)

def main():
    desde = int(input("Desde ID: "))
    hasta = int(input("Hasta ID: "))

    nombre_pdf = f"qr_{desde}_a_{hasta}.pdf"
    c = canvas.Canvas(nombre_pdf, pagesize=A4)

    ancho_pagina, alto_pagina = A4
    qr_size = 4.5 * cm  # recuadro cuadrado
    margen = 1 * cm

    x = margen
    y = alto_pagina - margen - qr_size

    for id_num in range(desde, hasta + 1):
        id_texto = str(id_num)
        qr_img = generar_qr(id_texto)

        # Marco cuadrado
        c.rect(x, y, qr_size, qr_size)

        # Texto superior "Mi Súper"
        c.setFont(fuente_super, 10)
        c.drawCentredString(x + qr_size / 2, y + qr_size - 10, "Mi Súper")

        # ID en esquina inferior izquierda
        c.setFont("Helvetica", 7)
        c.drawString(x + 4, y + 6, id_texto)

        # Línea horizontal para escribir
        c.setLineWidth(0.3)
        c.line(x + 28, y + 6, x + qr_size - 4, y + 6)

        # Dibuja QR en el centro del recuadro
        qr_margin = 0.4 * cm
        c.drawImage(
            qr_img,
            x + qr_margin,
            y + qr_margin + 6,
            width=qr_size - 2 * qr_margin,
            height=qr_size - 2 * qr_margin - 12  # Deja espacio arriba y abajo
        )

        # Siguiente posición
        x += qr_size
        if x + qr_size > ancho_pagina - margen:
            x = margen
            y -= qr_size
            if y < margen:
                c.showPage()
                x = margen
                y = alto_pagina - margen - qr_size

    c.save()
    print(f"✅ PDF generado: {nombre_pdf}")

if __name__ == "__main__":
    main()
