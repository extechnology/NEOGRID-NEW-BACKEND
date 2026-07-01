from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .project_models import *
from .project_serializers import (
    ProjectImagesSerializer,
    ProjectSerializer,
    GallerySerializer
)


class ProjectsAPIview(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            queryset = Project.objects.all()
            serializer = ProjectSerializer(queryset, many=True, context={'request': request})
            return Response({
                "message": "Projects retrieved successfully",
                "data": serializer.data,
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": str(e),
                "data": [],
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GalleryAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            queryset = Gallery.objects.all()
            serializer = GallerySerializer(queryset, many=True, context={'request': request})
            return Response({
                "message": "Gallery retrieved successfully",
                "data": serializer.data,
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": str(e),
                "data": [],
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)