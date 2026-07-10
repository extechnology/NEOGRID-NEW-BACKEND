from django.urls import path
from .order_views import (
    OrdersStats, Orders, OrderUpdate
    )

urlpatterns = [ 
    path('stats/', OrdersStats.as_view(), name='orders-stats'),
    path('list/', Orders.as_view(), name='orders-list'),
    path('update/<str:order_id>/', OrderUpdate.as_view(), name='order-update'),
]