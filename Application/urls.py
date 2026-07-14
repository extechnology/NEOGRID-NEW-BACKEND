from django.urls import path, include

urlpatterns = [
    path('auth/', include('Application.AuthenticationServices.auth_urls')),
    path('products/', include('Application.ProductServices.product_urls')),
    path('navigations/', include('Application.NavigationsAndFilters.nav_urls')),
    path('user/', include('Application.UserServices.user_urls')),
    path('ui/', include('Application.UIServices.ui_urls')),
    path('project/', include('Application.ProjectGalleryServices.project_urls')),
    path('dealer/', include('Application.DealerServices.dealer_urls')),
    path('personal/', include('Application.PersonalDatas.personal_urls')),
    
]