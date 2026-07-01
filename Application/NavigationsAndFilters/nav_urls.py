from django.urls import path
from .nav_views import (
    ProductNavigationAPIView,
    ProductFilterCategoryAPIView
)

urlpatterns = [
    path('product-navigation/', ProductNavigationAPIView.as_view(), name='product-navigation'),
    path('product-filter-category/', ProductFilterCategoryAPIView.as_view(), name='product-filter-category'),
]