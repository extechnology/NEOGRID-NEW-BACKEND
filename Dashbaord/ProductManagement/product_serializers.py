from pyexpat import model
from rest_framework import serializers

from Application.ProductServices.product_models import (
    ProductDepartment, ProductFamily,
    Product, ProductImages
)

class ProductDepartmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductDepartment
        fields = "__all__"


class ProductFamilySerializers(serializers.ModelSerializer):
    department = ProductDepartmentSerializers(read_only=True)
    class Meta:
        model = ProductFamily
        fields = "__all__"

class ProductImagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = "__all__"

class ProductSerializers(serializers.ModelSerializer):
    family = ProductFamilySerializers(read_only=True)
    images = ProductImagesSerializers(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
