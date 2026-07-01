from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .ui_models import *
from .ui_serializers import *

from rest_framework.permissions import AllowAny


class HomeSliderListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            sliders = HomeSlider.objects.all()
            serializer = HomeSliderSerializer(sliders, many=True, context = {"request":request})
            return Response({
                "message": "Home sliders retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": str(e),
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductDepartmentListView(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        try:
            departments = ProductDepartment.objects.all()
            serializer = ProductDepartmentUISerializer(departments, many=True, context = {"request":request})
            return Response({
                "message": "Product departments retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": str(e),
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)