from rest_framework import serializers
from .personal_models import PhoneNumbers

class PhoneNumbersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumbers
        fields = '__all__'