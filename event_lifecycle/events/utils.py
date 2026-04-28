import base64
from io import BytesIO

import qrcode
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


def generate_qr_data(url):
    qr = qrcode.QRCode(box_size=4, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    image = qr.make_image(fill_color='black', back_color='white')

    buffer = BytesIO()
    image.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')


def generate_certificate_pdf(participant):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    pdf.setTitle('Certificate of Participation')

    gradient_bands = [
        (colors.HexColor('#f4f7ff'), height - 6.8 * cm),
        (colors.HexColor('#e7edff'), height - 7.4 * cm),
        (colors.HexColor('#d8f2ff'), height - 8.0 * cm),
    ]
    for color, y in gradient_bands:
        pdf.setFillColor(color)
        pdf.roundRect(2.1 * cm, y, width - 4.2 * cm, 0.8 * cm, 0.2 * cm, stroke=0, fill=1)

    pdf.setStrokeColor(colors.HexColor('#536dfe'))
    pdf.setLineWidth(3)
    pdf.roundRect(1.8 * cm, 1.8 * cm, width - 3.6 * cm, height - 3.6 * cm, 0.35 * cm, stroke=1, fill=0)

    pdf.setStrokeColor(colors.HexColor('#21b6ff'))
    pdf.setLineWidth(1)
    pdf.roundRect(2.1 * cm, 2.1 * cm, width - 4.2 * cm, height - 4.2 * cm, 0.25 * cm, stroke=1, fill=0)

    pdf.setFillColor(colors.HexColor('#2d3ddf'))
    pdf.setFont('Helvetica-Bold', 30)
    pdf.drawCentredString(width / 2, height - 5 * cm, 'Certificate of Participation')

    pdf.setFillColor(colors.HexColor('#23395d'))
    pdf.setFont('Helvetica', 16)
    pdf.drawCentredString(width / 2, height - 8 * cm, 'This certifies that')

    pdf.setFillColor(colors.HexColor('#19233b'))
    pdf.setFont('Helvetica-Bold', 22)
    pdf.drawCentredString(width / 2, height - 10 * cm, participant.name)

    event_title = participant.event.title if participant.event else 'the selected event'

    pdf.setFillColor(colors.HexColor('#23395d'))
    pdf.setFont('Helvetica', 14)
    pdf.drawCentredString(width / 2, height - 12 * cm, f'Event: {event_title}')

    marks_text = f'Marks: {participant.marks}/100' if participant.marks is not None else 'Marks: Pending'
    pdf.setFillColor(colors.HexColor('#0a8f4f') if participant.marks is not None else colors.HexColor('#d9822b'))
    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawCentredString(width / 2, height - 13.2 * cm, marks_text)
    pdf.setFont('Helvetica', 14)
    pdf.drawCentredString(width / 2, height - 12 * cm, f'has successfully completed {event_title}.')

    marks_text = f'Marks: {participant.marks}/100' if participant.marks is not None else 'Marks: Pending'
    pdf.setFont('Helvetica-Bold', 14)
    pdf.drawCentredString(width / 2, height - 13.2 * cm, marks_text)

    pdf.setFont('Helvetica-Oblique', 11)
    pdf.drawCentredString(width / 2, height - 14.6 * cm, f'Certificate Ref: {participant.certificate_hash}')

    pdf.setFillColor(colors.HexColor('#4a5d85'))
    pdf.setFont('Helvetica-Oblique', 11)
    pdf.drawCentredString(width / 2, height - 14.6 * cm, f'Certificate Ref: {participant.certificate_hash}')

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer
