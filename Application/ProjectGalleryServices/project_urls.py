from django.urls import path

from .project_views import *

urlpatterns = [
    path("projects/", ProjectsAPIview.as_view()),
    path("gallery/", GalleryAPIView.as_view()),
]