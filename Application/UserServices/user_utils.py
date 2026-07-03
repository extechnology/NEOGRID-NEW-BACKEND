import string
import random

def create_order_id():
    chars = string.ascii_uppercase + string.digits
    random_str = ''.join(random.choices(chars, k=10))
    return f"ord-{random_str}"

def create_user_address_id():
    chars = string.ascii_uppercase + string.digits
    random_str = ''.join(random.choices(chars, k=10))
    return f"uad-{random_str}"


import tempfile
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from xhtml2pdf import pisa
from io import BytesIO

def generate_invoice_pdf(order):
    html_string = render_to_string('Application/invoice_template.html', {
        'order': order,
        'items': order.items.all()
    })
    
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), result)
    
    if not pdf.err:
        order.invoice.save(f"invoice_{order.order_id}.pdf", ContentFile(result.getvalue()), save=True)
