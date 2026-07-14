from django.urls import path
from .user_views import *

urlpatterns = [
    path('cart/', UserCartListView.as_view(), name='user-cart'),
    path('cart/add/', AddCartItemView.as_view(), name='add-cart-item'),
    path('cart/update/<int:pk>/', UpdateCartItemView.as_view(), name='update-cart-item'),
    path('cart/delete/<int:pk>/', DeleteCartItems.as_view(), name='delete-cart-item'),
    path('cart/delete/', DeleteCartView.as_view(), name='delete-cart'),
    path('address/',GetUserAddressView.as_view(), name='get-user-address'),
    path('address/add/',AddUserAddressView.as_view(), name='add-user-address'),
    path('address/update/<int:pk>/',UpdateUserAddressView.as_view(), name='update-user-address'),
    path('address/delete/<int:pk>/',DeleteUserAddressView.as_view(), name='delete-user-address'),
    path('order/create-order/', CreateOrderView.as_view(), name='create-order'),
    path('order/verify-payment/', VerifyOrderView.as_view(), name='verify-payment'),
    path('order/', UserOrderDetailAPIView.as_view(), name='user-orders'),
    path('contact/', ContactAPIView.as_view(), name='contact'),

]