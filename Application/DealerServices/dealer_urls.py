from django.urls import path
from .dealer_views import *

urlpatterns = [
    path('country/', CountryListCreate.as_view(), name='country-list-create'),
    path('country/<int:pk>/', CountryDetail.as_view(), name='country-detail'),

    path('state/', StateListCreate.as_view(), name='state-list-create'),
    path('state/<int:pk>/', StateDetail.as_view(), name='state-detail'),

    path('district/', DistrictListCreate.as_view(), name='district-list-create'),
    path('district/<int:pk>/', DistrictDetail.as_view(), name='district-detail'),

    path('franchasies/', FranchasiessList.as_view(), name='franchasies-list'),

    path('warranty-register/', WarrantyRegisterAPIvie.as_view(), name='warrenty-register'),
]