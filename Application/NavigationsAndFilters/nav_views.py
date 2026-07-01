from Application import permissions
from Application import permissions
from Application.ProductServices.product_models import (
    ProductDepartment,
    ProductFamily
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .nav_serializers import (
    ProductDepartmentSerializer,
    ProductFamilySerializer,
    ProductFamilySerializerforFilter,
    ProductDepartmentSerializerforFilter
)

class ProductNavigationAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            departments = ProductDepartment.objects.filter(is_active=True)
            serializer = ProductDepartmentSerializer(departments, many=True, context={'request': request})
            return Response({
                "status": status.HTTP_200_OK,
                "message": "Departments retrieved successfully",
                "data": serializer.data
            })
        except Exception as e:
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
                "data": []
            })

class ProductFilterCategoryAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        departments = ProductDepartment.objects.values_list('name', flat=True)
        families = ProductFamily.objects.values_list('name', flat=True)
        
        return Response({
            "status": status.HTTP_200_OK,
            "message": "Filters retrieved successfully",
            "data": {
                "departments": list(departments),
                "families": list(families),
            }
        })
