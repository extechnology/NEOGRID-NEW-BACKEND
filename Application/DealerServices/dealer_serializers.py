from rest_framework import serializers
from .dealer_models import Country, State, District, Dealers, WarrentyRegisterModel

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

class DealersSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source='district.name', read_only=True)
    
    class Meta:
        model = Dealers
        fields = '__all__'

class WarrentyRegisterSerializer(serializers.ModelSerializer):
    dealer_name = serializers.CharField(source='dealer.dealer_name', read_only=True)
    
    class Meta:
        model = WarrentyRegisterModel
        fields = '__all__'
