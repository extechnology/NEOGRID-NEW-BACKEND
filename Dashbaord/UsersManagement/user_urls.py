from django.urls import path
from .user_views import *

urlpatterns = [
    path("list/", UsersList.as_view(), name="users"),
    path('enquiry/', UserContacts.as_view(), name='enquiry'),
    path('contact-infos/', UserPhoneNumbersAPIview.as_view(), name='contact-infos')
]