from django.urls import path
from .dealers_views import RegisterdWarranty

urlpatterns = [
    path('registered-warranty/', RegisterdWarranty.as_view(), name='registered-warranty'),
]