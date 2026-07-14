from rest_framework import serializers
from Application.AuthenticationServices.auth_models import User
from Application.UserServices.user_models import ContactModel

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model=ContactModel
        fields='__all__'

