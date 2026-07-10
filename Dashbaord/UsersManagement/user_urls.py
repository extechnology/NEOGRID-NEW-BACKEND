from django.urls import path
from .user_views import *

urlpatterns = [
    path("list/", UsersList.as_view(), name="users"),
]