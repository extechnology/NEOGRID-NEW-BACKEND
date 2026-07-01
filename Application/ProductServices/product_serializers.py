from rest_framework import serializers
from .product_models import *

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

class ProductDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDepartment
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if instance.image:
            image_url = instance.image.url
            if request:
                image_url = request.build_absolute_uri(image_url)
            data['image'] = image_url
        return data

class ProductFamilySerializer(serializers.ModelSerializer):
    department = ProductDepartmentSerializer()
    class Meta:
        model = ProductFamily
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "name": instance.name,
            "department": ProductDepartmentSerializer(instance.department, context=self.context).data if instance.department else None,
        }

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if instance.image:
            image_url = instance.image.url
            if request:
                image_url = request.build_absolute_uri(image_url)
            data['image'] = image_url
        return data

class ProductSerializer(serializers.ModelSerializer):
    family = ProductFamilySerializer()
    images = ProductImagesSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "name": instance.name,
            "family": ProductFamilySerializer(instance.family, context=self.context).data if instance.family else None,
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
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
        }

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
        data['warrenty_info'] = clean_html_remove_styles(data['warrenty_info'])
        data["warrenty_info"] = data["warrenty_info"].replace("\r\n", "")
        data["warrenty_info"] = data["warrenty_info"].replace("\r", "")
        data["warrenty_info"] = data["warrenty_info"].replace("\n", "")
        return data