from rest_framework import serializers

from .ui_models import *
from Application.ProductServices.product_models import ProductDepartment

class HomeSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeSlider
        fields = '__all__'


class ProductDepartmentUISerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDepartment
        fields = '__all__'