from django.urls import path
from .dealer_views import *

urlpatterns = [
    path('country/', CountryListCreate.as_view(), name='country-list-create'),
    path('country/<int:pk>/', CountryDetail.as_view(), name='country-detail'),

    path('state/', StateListCreate.as_view(), name='state-list-create'),
    path('state/<int:pk>/', StateDetail.as_view(), name='state-detail'),

    path('district/', DistrictListCreate.as_view(), name='district-list-create'),
    path('district/<int:pk>/', DistrictDetail.as_view(), name='district-detail'),

    path('dealers/', DealersListCreate.as_view(), name='dealers-list-create'),
    path('dealers/<int:pk>/', DealersDetail.as_view(), name='dealers-detail'),

    path('warrenty/', WarrentyRegisterListCreate.as_view(), name='warrenty-list-create'),
    path('warrenty/<int:pk>/', WarrentyRegisterDetail.as_view(), name='warrenty-detail'),
]