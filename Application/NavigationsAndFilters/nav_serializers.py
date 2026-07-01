from Application.ProductServices.product_models import (
    ProductDepartment,
    ProductFamily,
    Product,
    ProductImages
)
from rest_framework import serializers

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['image']
    
    def to_representation(self, instance):
        request = self.context.get('request')
        image_url = instance.image.url if instance.image else None
        if image_url and request:
            image_url = request.build_absolute_uri(image_url)
        return {
            "image": image_url
        }

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImagesSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id','name','model_type','model_number','price','discount_percentage','discount_price','description','additional_info','technical_spec','new_arrival','is_available','images']
    
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "name": instance.name,
            "model_type": instance.model_type,
            "model_number": instance.model_number,
            "price": instance.price,
            "discount_percentage": instance.discount_percentage,
            "discount_price": instance.discount_price,
            "description": instance.description,
            "additional_info": instance.additional_info,
            "technical_spec": instance.technical_spec,
            "new_arrival": instance.new_arrival,
            "is_available": instance.is_available,
            "images": ProductImagesSerializer(instance.images.all(), many=True, context=self.context).data,
        }

class ProductFamilySerializer(serializers.ModelSerializer):
    # products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = ProductFamily
        fields = ['name','image']
    
    def to_representation(self, instance):
        request = self.context.get('request')
        image_url = instance.image.url if instance.image else None
        if image_url and request:
            image_url = request.build_absolute_uri(image_url)
        return {
            "name": instance.name,
            "image": image_url
        }


class ProductDepartmentSerializer(serializers.ModelSerializer):
    family = ProductFamilySerializer(many=True, source='families', read_only=True)
    class Meta:
        model = ProductDepartment
        fields = ['name', 'family']

    def to_representation(self, instance):
        return {
            "name": instance.name,
            "family": ProductFamilySerializer(instance.families.all(), many=True, context=self.context).data
        }

class ProductFamilySerializerforFilter(serializers.ModelSerializer):
    class Meta:
        model = ProductFamily
        fields = ['name']


class ProductDepartmentSerializerforFilter(serializers.ModelSerializer):
    class Meta:
        model = ProductDepartment
        fields = ['name']