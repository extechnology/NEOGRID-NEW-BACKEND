import os
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from Application.UserServices.user_mails import get_logo_attachment

def send_warranty_registration_email(warranty, subfranchise):
    # 1. Email to the User
    user_subject = "Warranty Registered Successfully"
    
    user_text_body = f"""Hi {warranty.fullname},

Your warranty for {warranty.product_name} ({warranty.model_number}) has been registered successfully.
Serial Number: {warranty.serial_number}
Purchased Date: {warranty.purchased_date}
Franchise: {warranty.franchise}

Thank you for choosing NEOGRID!

NEOGRID
MM 11/505-C, Mullampara,
Manjeri, Malappuram,
Kerala – 676121
+91 98461 31500
info@neogrid.in
www.neogrid.in"""

    user_html_body = f"""
    <div style="font-family: Arial, sans-serif; color: #333;">
        <p>Hi {warranty.fullname},</p>
        <p>Your warranty for <strong>{warranty.product_name}</strong> ({warranty.model_number}) has been registered successfully.</p>
        <ul>
            <li><strong>Serial Number:</strong> {warranty.serial_number}</li>
            <li><strong>Purchased Date:</strong> {warranty.purchased_date}</li>
            <li><strong>Franchise:</strong> {warranty.franchise}</li>
        </ul>
        <p>Thank you for choosing NEOGRID!</p>
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
    
    user_email = EmailMultiAlternatives(
        subject=user_subject,
        body=user_text_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[warranty.email]
    )
    user_email.attach_alternative(user_html_body, "text/html")
    
    logo1 = get_logo_attachment()
    if logo1:
        user_email.attach(logo1)
        
    user_email.send(fail_silently=True)

    # 2. Email to the Franchise
    franchise_subject = f"New Client Warranty Registration - {warranty.fullname}"
    
    franchise_text_body = f"""Hi {subfranchise.name},

A new client has registered a warranty under your franchise.

Client Details:
Name: {warranty.fullname}
Email: {warranty.email}
Phone: {warranty.phone}
Address: {warranty.address}, {warranty.district}, {warranty.state} - {warranty.pincode}

Product Details:
Product: {warranty.product_name}
Model Number: {warranty.model_number}
Serial Number: {warranty.serial_number}
Purchased Date: {warranty.purchased_date}

NEOGRID
MM 11/505-C, Mullampara,
Manjeri, Malappuram,
Kerala – 676121
+91 98461 31500
info@neogrid.in
www.neogrid.in"""

    franchise_html_body = f"""
    <div style="font-family: Arial, sans-serif; color: #333;">
        <p>Hi {subfranchise.name},</p>
        <p>A new client has registered a warranty under your franchise.</p>
        
        <h3>Client Details:</h3>
        <ul>
            <li><strong>Name:</strong> {warranty.fullname}</li>
            <li><strong>Email:</strong> {warranty.email}</li>
            <li><strong>Phone:</strong> {warranty.phone}</li>
            <li><strong>Address:</strong> {warranty.address}, {warranty.district}, {warranty.state} - {warranty.pincode}</li>
        </ul>

        <h3>Product Details:</h3>
        <ul>
            <li><strong>Product:</strong> {warranty.product_name}</li>
            <li><strong>Model Number:</strong> {warranty.model_number}</li>
            <li><strong>Serial Number:</strong> {warranty.serial_number}</li>
            <li><strong>Purchased Date:</strong> {warranty.purchased_date}</li>
        </ul>
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
    
    franchise_email = EmailMultiAlternatives(
        subject=franchise_subject,
        body=franchise_text_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[subfranchise.email]
    )
    franchise_email.attach_alternative(franchise_html_body, "text/html")
    
    logo2 = get_logo_attachment()
    if logo2:
        franchise_email.attach(logo2)
        
    franchise_email.send(fail_silently=True)
