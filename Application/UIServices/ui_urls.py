from django.urls import path
from .ui_views import *

urlpatterns = [
    path('home/slider/', HomeSliderListView.as_view(), name='home_slider_list'),
    path('product/department/', ProductDepartmentListView.as_view(), name='product_department_list'),
]