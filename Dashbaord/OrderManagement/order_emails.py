from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.conf import settings
import threading

class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list, sender):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.sender = sender
        threading.Thread.__init__(self)

    def run(self):
        try:
            send_mail(
                self.subject,
                strip_tags(self.html_content),
                self.sender,
                self.recipient_list,
                html_message=self.html_content,
                fail_silently=True,
            )
        except Exception as e:
            print(f"Failed to send email: {e}")

def send_order_update_email(order):
    subject = f"Order Status Update - {order.order_id}"
    sender = getattr(settings, 'DEFAULT_FROM_EMAIL', getattr(settings, 'EMAIL_HOST_USER', 'noreply@example.com'))
    recipient_list = [order.user.email]
    
    logo_url = "https://neogrid.in/neo%20grid%20logo-01.png"
    
    print("Recipient List:", recipient_list)
    html_content = f"""
    <div style="font-family: 'Inter', Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #333; background-color: #f4f7f6; padding: 20px; border-radius: 8px;">
        <div style="background-color: #0c1e33; padding: 30px; text-align: center; border-radius: 8px 8px 0 0;">
            <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 600;">Order Update</h1>
            <p style="color: #00d4ff; margin: 10px 0 0 0; font-size: 16px; font-weight: 500;">Order #{order.order_id}</p>
        </div>
        <div style="background-color: #ffffff; padding: 30px; border-radius: 0 0 8px 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <p style="font-size: 16px; color: #555;">Dear Customer,</p>
            <p style="font-size: 16px; color: #555; line-height: 1.5;">Your order <strong>#{order.order_id}</strong> has been updated. Here is your current status:</p>
            
            <div style="background: linear-gradient(135deg, #00d4ff 0%, #007bff 100%); padding: 15px; border-radius: 6px; text-align: center; margin: 25px 0;">
                <span style="color: #fff; font-size: 20px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;">{order.status}</span>
            </div>
    """
    
    if order.tracking_id:
        html_content += f'<p style="font-size: 15px; margin-bottom: 5px;"><strong style="color:#0c1e33;">Tracking ID:</strong> <span style="color:#007bff;">{order.tracking_id}</span></p>'
    if order.tracking_url:
        html_content += f'<p style="font-size: 15px;"><strong style="color:#0c1e33;">Track your order:</strong> <a href="{order.tracking_url}" style="color: #007bff; text-decoration: none; font-weight: bold;">Click Here &rarr;</a></p>'
        
    # Add Product Details Table
    html_content += """
            <h3 style="color: #0c1e33; margin-top: 35px; border-bottom: 2px solid #f0f0f0; padding-bottom: 10px;">Order Details</h3>
            <table style="width: 100%; border-collapse: separate; border-spacing: 0; margin-bottom: 20px;">
                <thead>
                    <tr style="background-color: #f8f9fa;">
                        <th style="padding: 12px; text-align: left; border-bottom: 2px solid #dee2e6; color: #495057; border-top-left-radius: 6px;">Product</th>
                        <th style="padding: 12px; text-align: center; border-bottom: 2px solid #dee2e6; color: #495057;">Qty</th>
                        <th style="padding: 12px; text-align: right; border-bottom: 2px solid #dee2e6; color: #495057; border-top-right-radius: 6px;">Price</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    for item in order.items.all():
        product_name = item.product.name if item.product else 'Unknown Product'
        price = item.price_at_addition or 0
        html_content += f"""
                    <tr>
                        <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #555;">{product_name}</td>
                        <td style="padding: 12px; text-align: center; border-bottom: 1px solid #e9ecef; color: #555; font-weight: bold;">{item.quantity}</td>
                        <td style="padding: 12px; text-align: right; border-bottom: 1px solid #e9ecef; color: #007bff; font-weight: bold;">${price}</td>
                    </tr>
        """
        
    html_content += f"""
                </tbody>
            </table>
            
            <div style="text-align: right; margin-top: 10px;">
                <p style="font-size: 16px; color: #777; margin: 0; text-transform: uppercase; letter-spacing: 1px;">Total Amount</p>
                <p style="font-size: 26px; color: #0c1e33; font-weight: bold; margin: 5px 0 0 0;">${order.total_value or 0}</p>
            </div>
            
            <hr style="border: 0; border-top: 1px solid #eee; margin: 30px 0;">
            <p style="font-size: 15px; color: #777; text-align: center; margin-bottom: 30px;">Thank you for shopping with us!</p>
            
            <div style="text-align: center;">
                <img src="{logo_url}" alt="Neogrid Logo" style="max-width: 160px; height: auto;">
            </div>
        </div>
    </div>
    """

    EmailThread(subject, html_content, recipient_list, sender).start()
