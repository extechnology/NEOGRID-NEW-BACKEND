from django.urls import path
from .analytics_views import (
    PerformanceStats, RevenueTrend, OrderStatusWheel, DailyOrder,
    TopProducts, RecentOrders
)

urlpatterns = [

    path('performance-stats/',PerformanceStats.as_view(),name='performance-stats'),
    path('revenue-trend/',RevenueTrend.as_view(),name='revenue-trend'),
    path('order-status-wheel/',OrderStatusWheel.as_view(),name='order-status-wheel'),
    path('daily-orders/',DailyOrder.as_view(),name='daily-orders'),
    path('top-products/',TopProducts.as_view(),name='top-products'),
    path('recent-orders/',RecentOrders.as_view(),name='recent-orders'),


]