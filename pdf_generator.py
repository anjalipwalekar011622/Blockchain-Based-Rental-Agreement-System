from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER
from datetime import datetime
import os

def generate_agreement(data):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"agreement_{data['tenant_name'].replace(' ', '_')}_{timestamp}.pdf"
    filepath = os.path.join("static", "agreements", filename)

    # ✅ Reduced margins to save space
    doc = SimpleDocTemplate(filepath, pagesize=A4,
                            rightMargin=0.7*inch, leftMargin=0.7*inch,
                            topMargin=0.6*inch, bottomMargin=0.6*inch)

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('Title', parent=styles['Title'],
                                  fontSize=16, spaceAfter=4, alignment=TA_CENTER)

    heading_style = ParagraphStyle('Heading', parent=styles['Normal'],
                                    fontSize=12, spaceAfter=3, spaceBefore=6,
                                    fontName='Helvetica-Bold')

    # ✅ Reduced leading and spaceAfter
    body_style = ParagraphStyle('Body', parent=styles['Normal'],
                                 fontSize=10, spaceAfter=3, leading=13)

    content = []

    # Title
    content.append(Paragraph("RENTAL AGREEMENT", title_style))
    content.append(Paragraph("Blockchain-Verified Document",
                              ParagraphStyle('sub', parent=styles['Normal'],
                                            fontSize=9, alignment=TA_CENTER,
                                            textColor='grey')))
    content.append(Spacer(1, 15))  # ✅ Reduced from 20

    # Date
    content.append(Paragraph(f"Date: {data['start_date']}", body_style))
    content.append(Spacer(1, 5))  # ✅ Reduced from 10

    # Parties
    content.append(Paragraph("1. PARTIES INVOLVED", heading_style))
    content.append(Paragraph(
        f"This Rental Agreement is entered into between <b>{data['landlord_name']}</b> "
        f"(hereinafter referred to as 'Landlord') and <b>{data['tenant_name']}</b> "
        f"(hereinafter referred to as 'Tenant').", body_style))

    # Property
    content.append(Paragraph("2. PROPERTY", heading_style))
    content.append(Paragraph(
        f"The Landlord agrees to rent the property located at: "
        f"<b>{data['property_address']}</b>", body_style))

    # Duration
    content.append(Paragraph("3. LEASE DURATION", heading_style))
    content.append(Paragraph(
        f"The lease shall commence on <b>{data['start_date']}</b> and "
        f"shall continue for a period of <b>{data['duration_months']} months</b>.",
        body_style))

    # Rent
    content.append(Paragraph("4. RENT AMOUNT", heading_style))
    content.append(Paragraph(
        f"The Tenant agrees to pay a monthly rent of "
        f"<b>₹{data['rent_amount']}</b>, due on the 1st of every month.", body_style))

    # Deposit
    content.append(Paragraph("5. SECURITY DEPOSIT", heading_style))
    content.append(Paragraph(
        f"A security deposit of <b>₹{data['deposit_amount']}</b> shall be paid "
        f"by the Tenant prior to occupancy. This deposit shall be refunded at the "
        f"end of the lease period, subject to property condition.", body_style))

    # Terms
    content.append(Paragraph("6. TERMS AND CONDITIONS", heading_style))
    terms = [
        "The Tenant shall not sublet the property without written consent of the Landlord.",
        "The Tenant shall maintain the property in good condition.",
        "The Landlord shall ensure all essential services are functional at the time of occupancy.",
        "Either party may terminate this agreement with 30 days written notice.",
        "Any disputes shall be resolved through mutual discussion or legal arbitration.",
    ]
    for i, term in enumerate(terms, 1):
        content.append(Paragraph(f"{i}. {term}", body_style))

    # Blockchain notice
    content.append(Spacer(1, 10))  # ✅ Reduced from 20
    content.append(Paragraph(
        "⚠️ This document is blockchain-verified. Any modification after registration "
        "will be detected during verification.",
        ParagraphStyle('notice', parent=styles['Normal'], fontSize=8,
                       textColor='red', alignment=TA_CENTER)))

    # Signatures
    from reportlab.platypus import Table, TableStyle
    from reportlab.lib import colors

    content.append(Spacer(1, 16))
    content.append(Paragraph("SIGNATURES", heading_style))
    content.append(Spacer(1, 20))

    # Table with 2 columns — perfectly aligned
    sig_data = [
        [f"Landlord: {data['landlord_name']}", f"Tenant: {data['tenant_name']}"],
        ["", ""],
        ["_______________________", "_______________________"],
        ["(Landlord Signature)", "(Tenant Signature)"],
    ]

    sig_table = Table(sig_data, colWidths=[3.5*inch, 3.5*inch])
    sig_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))

    content.append(sig_table)

    doc.build(content)
    return filepath, filename