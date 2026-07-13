from rest_framework import serializers
from .dealer_models import *

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)
    
    class Meta:
        model = State
        fields = '__all__'

class DistrictSerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', read_only=True)
    
    class Meta:
        model = District
        fields = '__all__'


class WarrantyRegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = WarrantyRegisterModel
        fields = '__all__'