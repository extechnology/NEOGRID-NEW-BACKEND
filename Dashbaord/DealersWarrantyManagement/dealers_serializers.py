from rest_framework import serializers
from Application.DealerServices.dealer_models import WarrantyRegisterModel


class WarrantyRegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = WarrantyRegisterModel
        fields = '__all__'