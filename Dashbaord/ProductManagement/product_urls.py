from django.urls import path
from .product_views import *

urlpatterns = [
    path('department-family/create/', DepartmentFamilyCreate.as_view(), name='department-family-create'),
    path('product-images/create/', ProductWithImagesCreate.as_view(), name='product-images-create'),
    path('list/', Products.as_view(), name='product-list'),
    
    path('create/', ProductCreate.as_view(), name='product-create'),
    path('update/<int:pk>/', ProductUpdate.as_view(), name='product-update'),
    
    path('department/create/', ProductDepartmentCreate.as_view(), name='department-create'),
    path('department/update/<int:pk>/', ProductDepartmentUpdate.as_view(), name='department-update'),
    
    path('family/create/', ProductFamilyCreate.as_view(), name='family-create'),
    path('family/update/<int:pk>/', ProductFamilyUpdate.as_view(), name='family-update'),
    
    path('images/create/', ProductImagesCreate.as_view(), name='images-create'),
    path('images/update/<int:pk>/', ProductImagesUpdate.as_view(), name='images-update'),
]