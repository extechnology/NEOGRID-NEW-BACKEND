import os
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from django.conf import settings

def get_logo_attachment():
    logo_path = os.path.join(settings.BASE_DIR, 'media', 'logos', 'NEOGRID FEVIC LOGO 400X300.png')
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', '<neogrid_logo>')
            return img
    return None

def send_order_created_email(order):
    subject = f"Order Confirmed - {order.order_id}"
    
    text_body = f"""Hi {order.user.fullname or order.user.email},

Your order has been successfully placed. Your order ID is {order.order_id}.

Please find your invoice attached.
(including tax)

Thank you for shopping with NEOGRID!

NEOGRID
MM 11/505-C, Mullampara,
Manjeri, Malappuram,
Kerala – 676121
+91 98461 31500
info@neogrid.in
www.neogrid.in"""

    html_body = f"""
    <div style="font-family: Arial, sans-serif; color: #333;">
        <p>Hi {order.user.fullname or order.user.email},</p>
        <p>Your order has been successfully placed. Your order ID is <strong>{order.order_id}</strong>.</p>
        <p>Please find your invoice attached.</p>
        <p style="font-size: 12px; color: #666;">(including tax)</p>
        <p>Thank you for shopping with NEOGRID!</p>
        <br>
        <img src="cid:neogrid_logo" alt="NEOGRID Logo" style="width: 200px; max-width: 100%;">
        <div style="margin-top: 20px;">
            <strong>NEOGRID</strong><br>
            MM 11/505-C, Mullampara,<br>
            Manjeri, Malappuram,<br>
            Kerala – 676121<br>
            +91 98461 31500<br>
            <a href="mailto:info@neogrid.in">info@neogrid.in</a><br>
            <a href="https://www.neogrid.in">www.neogrid.in</a>
        </div>
    </div>
    """
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[order.user.email]
    )
    email.attach_alternative(html_body, "text/html")
    
    logo = get_logo_attachment()
    if logo:
        email.attach(logo)
    
    if order.invoice:
        email.attach_file(order.invoice.path)
        
    email.send(fail_silently=True)

def send_payment_failed_email(order):
    subject = f"Payment Failed - {order.order_id}"
    
    text_body = f"""Hi {order.user.fullname or order.user.email},

We noticed a failed payment attempt for your order {order.order_id}. If you faced any issues, please try again or contact support.

Thank you,

NEOGRID
MM 11/505-C, Mullampara,
Manjeri, Malappuram,
Kerala – 676121
+91 98461 31500
info@neogrid.in
www.neogrid.in"""

    html_body = f"""
    <div style="font-family: Arial, sans-serif; color: #333;">
        <p>Hi {order.user.fullname or order.user.email},</p>
        <p>We noticed a failed payment attempt for your order <strong>{order.order_id}</strong>. If you faced any issues, please try again or contact support.</p>
        <p>Thank you,</p>
        <br>
        <img src="cid:neogrid_logo" alt="NEOGRID Logo" style="width: 200px; max-width: 100%;">
        <div style="margin-top: 20px;">
            <strong>NEOGRID</strong><br>
            MM 11/505-C, Mullampara,<br>
            Manjeri, Malappuram,<br>
            Kerala – 676121<br>
            +91 98461 31500<br>
            <a href="mailto:info@neogrid.in">info@neogrid.in</a><br>
            <a href="https://www.neogrid.in">www.neogrid.in</a>
        </div>
    </div>
    """
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[order.user.email]
    )
    email.attach_alternative(html_body, "text/html")
    
    logo = get_logo_attachment()
    if logo:
        email.attach(logo)
        
    email.send(fail_silently=True)
