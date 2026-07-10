from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .user_serializers import *
from Application.AuthenticationServices.auth_models import User
from Application.UserServices.user_models import (
    UserOrderModel
)
from django.db.models import Count, Sum

class UsersList(APIView):
    def get(self, request):
        users = User.objects.annotate(
            orders_count=Count('orders'),
            total_spend=Sum('orders__total_value')
        ).order_by('-date_joined') # Good practice to order them
        
        data = [
            {
                "id": user.id,
                "name": user.username,
                "email": user.email,
                "orders": user.orders_count,
                "total_spend": float(user.total_spend or 0.0)
            } for user in users
        ]
        
        return Response(data, status=status.HTTP_200_OK)