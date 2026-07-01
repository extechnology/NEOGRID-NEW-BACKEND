from django.urls import path
from .product_views import (
    ProductAPIView,
    SingleProductAPIView,
    ProductSliderAPIView
)

urlpatterns = [
    path("", ProductAPIView.as_view(), name="product"),
    path("<int:id>/", SingleProductAPIView.as_view(), name="single-product"),
    path("product-slider/",ProductSliderAPIView.as_view(),name="product-slider"),
]