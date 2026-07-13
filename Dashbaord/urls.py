from django.urls import path, include
from .views import AdminLoginView, CheckLogin, Logout


urlpatterns = [
    path('analytics/', include('Dashbaord.AnalyticsServices.analytics_urls')),
    path('order/', include('Dashbaord.OrderManagement.order_urls')),
    path('product/', include('Dashbaord.ProductManagement.product_urls')),
    path('user/', include('Dashbaord.UsersManagement.user_urls')),
    path('dealers-warranty/', include('Dashbaord.DealersWarrantyManagement.dealers_urls')),

    path('admin-login/', AdminLoginView.as_view(), name='admin_login'),
    path('check-login/', CheckLogin.as_view(), name='check_login'),
    path('logout/', Logout.as_view(), name='logout'),
]