import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from io import BytesIO

def generar_qr(id_texto):
    qr = qrcode.QRCode(box_size=10, border=2)
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
    margen = 1.5 * cm
    espacio_horizontal = 4 * cm
    espacio_vertical = 4.5 * cm
    qr_size = 3 * cm
    texto_altura = 0.5 * cm

    x_inicio = margen
    y_inicio = alto_pagina - margen - qr_size

    x = x_inicio
    y = y_inicio

    for id_num in range(desde, hasta + 1):
        id_texto = str(id_num)
        qr_img = generar_qr(id_texto)

        # Dibuja borde
        c.rect(x, y, qr_size, qr_size)

        # Dibuja QR
        c.drawImage(qr_img, x, y, width=qr_size, height=qr_size)

        # Dibuja ID debajo del QR
        c.setFont("Helvetica", 7)
        c.drawCentredString(x + qr_size / 2, y - texto_altura, id_texto)

        # Actualiza posición
        x += espacio_horizontal
        if x + qr_size > ancho_pagina - margen:
            x = x_inicio
            y -= espacio_vertical

            if y < margen:
                c.showPage()
                x = x_inicio
                y = y_inicio

    c.save()
    print(f"PDF generado: {nombre_pdf}")

if __name__ == "__main__":
    main()
