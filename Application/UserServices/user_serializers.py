from rest_framework import serializers

from .user_models import (
    UserCartModel,
    UserCartItemModel,
    UserAddress,
    UserOrderModel,
    UserOrderItemModel
)

from Application.ProductServices.product_models import (
    Product,
    ProductImages
)


import re
from bs4 import BeautifulSoup

def clean_html_remove_styles(html):
    soup = BeautifulSoup(html, "lxml")

    # Remove style attributes from all tags
    for tag in soup.find_all(True):
        tag.attrs.pop("style", None)

    # OPTIONAL: remove html/body tags
    if soup.body:
        return soup.body.decode_contents()

    return str(soup)

class ProductImagesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'

class ProductModelSerializer(serializers.ModelSerializer):
    images = ProductImagesModelSerializer(many=True, read_only=True)
    class Meta:
        model = Product 
        fields = '__all__'

    def to_representation(self, instance):  
        data = super().to_representation(instance)
        data['description'] = clean_html_remove_styles(data['description'])
        data["description"] = data["description"].replace("\r\n", "")
        data["description"] = data["description"].replace("\r", "")
        data["description"] = data["description"].replace("\n", "")
        data['additional_info'] = clean_html_remove_styles(data['additional_info'])
        data["additional_info"] = data["additional_info"].replace("\r\n", "")
        data["additional_info"] = data["additional_info"].replace("\r", "")
        data["additional_info"] = data["additional_info"].replace("\n", "")
        data['technical_spec'] = clean_html_remove_styles(data['technical_spec'])
        data["technical_spec"] = data["technical_spec"].replace("\r\n", "")
        data["technical_spec"] = data["technical_spec"].replace("\r", "")
        data["technical_spec"] = data["technical_spec"].replace("\n", "")
        return data

class UserCartItemModelSerializer(serializers.ModelSerializer):
    product = ProductModelSerializer(read_only=True)
    class Meta:
        model = UserCartItemModel
        fields = '__all__'

class UserCartModelSerializer(serializers.ModelSerializer):
    items = UserCartItemModelSerializer(many=True, read_only=True)
    total_value = serializers.SerializerMethodField()

    class Meta:
        model = UserCartModel
        fields = ['id', 'user', 'items', 'total_value', 'created_at', 'updated_at']

    def get_total_value(self, obj):
        total_amount = 0
        cart = obj
        total_shipping = 0
        for item in UserCartItemModel.objects.filter(cart=cart):
            if item.product.discount_price > 0:
                total_amount += item.product.discount_price * item.quantity
            else:
                total_amount += item.product.price * item.quantity
            total_shipping += item.product.shipping_charge
        total_amount += total_shipping    
        return total_amount



class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = '__all__'
        read_only_fields = ['user', 'unique_id']

class UserOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOrderItemModel
        fields = '__all__'


class UserOrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOrderModel
        fields = '__all__'

class VerifyPaymentSerializer(serializers.Serializer):
    razorpay_order_id = serializers.CharField(max_length=100)
    razorpay_payment_id = serializers.CharField(max_length=100)
    razorpay_signature = serializers.CharField(max_length=200)



class UserAddressSerializerForListOrder(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = "__all__"


class OrderProductSerializerForListOrder(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "model_type",
            "model_number",
            "price",
            "discount_percentage",
            "discount_price",
            "shipping_charge",
            "image",
        ]

    def get_image(self, obj):
        image = obj.images.first()
        request = self.context.get("request")

        if image and image.image:
            return request.build_absolute_uri(image.image.url)
        return None


class OrderItemSerializerForListOrder(serializers.ModelSerializer):
    product = OrderProductSerializerForListOrder(read_only=True)

    class Meta:
        model = UserOrderItemModel
        fields = [
            "id",
            "quantity",
            "price_at_addition",
            "product",
        ]


class UserOrderDetailSerializerForListOrder(serializers.ModelSerializer):
    address = UserAddressSerializerForListOrder(read_only=True)
    items = OrderItemSerializerForListOrder(many=True, read_only=True)

    class Meta:
        model = UserOrderModel
        fields = [
            "id",
            "order_id",
            "status",
            "total_value",
            "created_at",
            "address",
            "items",
        ]