from django.db import models

from Application.ProductServices.product_models import (
    Product
)

from Application.AuthenticationServices.auth_models import (
    User
)
from .user_utils import create_order_id, create_user_address_id




class UserCartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    total_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # Price of the product when added to cart
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.email}"
    
    class Meta:
        verbose_name = 'User Cart'
        verbose_name_plural = 'User Carts'
    
class UserCartItemModel(models.Model):
    cart = models.ForeignKey(UserCartModel, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    price_at_addition = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # Price of the product when added to cart

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.price_at_addition:
            self.price_at_addition = self.product.price * self.quantity
        super().save(*args, **kwargs)
    

    def subtotal(self):
        return self.product.price * self.quantity


        
class UserAddress(models.Model):
    unique_id = models.CharField(max_length=100, default=create_user_address_id, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_addresses')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    address_type = models.CharField(max_length=10,null=True,blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    is_default = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + " - " + str(self.name)

    def save(self, *args, **kwargs):
        if self.phone_number:
            self.phone_number = self.phone_number.strip()
            if self.phone_number.startswith('+91'):
                self.phone_number = self.phone_number[3:].strip()
        super().save(*args, **kwargs)

STATUS_CHOICES = (
    ('PENDING', 'Pending'),
    ('CONFIRMED', 'Confirmed'),
    ('SHIPPED', 'Shipped'),
    ('OUT_FOR_DELIVERY', 'Out For Delivery'),
    ('DELIVERED', 'Delivered'),
    ('CANCELLED', 'Cancelled'),
)

class UserOrderModel(models.Model):
    order_id = models.CharField(max_length=100, default=create_order_id, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='orders')

    total_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # Price of the product when added to cart

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=200, null=True, blank=True)

    invoice = models.FileField(upload_to='invoices/', null=True, blank=True)

    tracking_id = models.CharField(max_length = 200, null=True, blank=True)
    tracking_url = models.CharField(max_length = 500, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order for {self.user.email}"
    
    class Meta:
        verbose_name = 'User Order'
        verbose_name_plural = 'User Orders'


class UserOrderItemModel(models.Model):
    order = models.ForeignKey(UserOrderModel, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price_at_addition = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # Price of the product when added to cart

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.price_at_addition:
            self.price_at_addition = self.product.price
        super().save(*args, **kwargs)

    def subtotal(self):
        return self.price_at_addition * self.quantity
    