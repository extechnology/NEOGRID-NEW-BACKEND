from rest_framework import serializers
from Application.UserServices.user_models import (
    UserOrderItemModel, UserOrderModel,
    UserAddress
)

from Application.ProductServices.product_models import (
    ProductDepartment, ProductFamily,
    Product, ProductImages
)

class UserAddressSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = "__all__"


class ProductSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerilaizer(read_only=True)
    class Meta:
        model = UserOrderItemModel
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address = UserAddressSerializers(read_only=True)
    user = serializers.SerializerMethodField()
    shipping_charge = serializers.SerializerMethodField()
    class Meta:
        model = UserOrderModel
        fields = "__all__"
    
    def get_user(self, obj):
        user = obj.user
        return {
            "email": user.email,
            "username": user.username
        }
    
    def get_shipping_charge(self, obj):
        total_shipping_charge = 0
        for item in obj.items.all():
            if item.product and item.product.shipping_charge:
                total_shipping_charge += item.quantity * item.product.shipping_charge
        return total_shipping_charge