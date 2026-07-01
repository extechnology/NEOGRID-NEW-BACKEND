from rest_framework import serializers

from .user_models import (
    UserCartModel,
    UserCartItemModel,
    UserAddress,
    UserOrderModel
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

    class Meta:
        model = UserCartModel
        fields = ['id', 'user', 'items', 'total_value', 'created_at', 'updated_at']

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = '__all__'
        read_only_fields = ['user', 'unique_id']

class UserOrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOrderModel
        fields = '__all__'
