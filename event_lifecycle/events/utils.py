from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


def generate_certificate_pdf(participant):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    pdf.setTitle('Certificate of Participation')

    pdf.setFont('Helvetica-Bold', 30)
    pdf.drawCentredString(width / 2, height - 5 * cm, 'Certificate of Participation')

    pdf.setFont('Helvetica', 16)
    pdf.drawCentredString(width / 2, height - 8 * cm, 'This certifies that')

    pdf.setFont('Helvetica-Bold', 22)
    pdf.drawCentredString(width / 2, height - 10 * cm, participant.name)

    pdf.setFont('Helvetica', 14)
    pdf.drawCentredString(width / 2, height - 12 * cm, 'has successfully completed the Event Lifecycle Workshop.')

    pdf.setFont('Helvetica-Oblique', 11)
    pdf.drawCentredString(width / 2, height - 14.5 * cm, f'Certificate Ref: {participant.certificate_hash}')

    pdf.rect(2 * cm, 2 * cm, width - 4 * cm, height - 4 * cm)

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer
