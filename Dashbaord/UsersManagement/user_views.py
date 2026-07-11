from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .user_serializers import *
from Application.AuthenticationServices.auth_models import User
from Application.UserServices.user_models import (
    UserOrderModel
)
from Dashbaord.paginations import DashboardCustomPagination
from django.db.models import Count, Sum

class UsersList(APIView):
    pagination_class = [DashboardCustomPagination]

    def get(self, request):
        users = User.objects.annotate(
            orders_count=Count('orders'),
            total_spend=Sum('orders__total_value')
        ).order_by('-date_joined') # Good practice to order them
        
        paginator = DashboardCustomPagination()
        paginator.message = "Users retrieved successfully"
        paginated_users = paginator.paginate_queryset(users, request)
        
        data = [
            {
                "id": user.id,
                "name": user.username,
                "email": user.email,
                "orders": user.orders_count,
                "total_spend": float(user.total_spend or 0.0)
            } for user in paginated_users
        ]
        
        return paginator.get_paginated_response(data)