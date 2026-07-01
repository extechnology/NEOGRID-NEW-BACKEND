from django.template import context
from rest_framework.decorators import permission_classes
from .product_models import *
from .product_serializers import *

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination

from .product_filters import ProductFilter

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "status": status.HTTP_200_OK,
            "message": "Products retrieved successfully",
            "data": data,
            "banner": getattr(self, 'banner', None),
            "meta": {
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "next": self.get_next_link(),
                "previous": self.get_previous_link()
            }
        })

class ProductAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            
            # Fetch the banner before pagination happens
            department_name = request.query_params.get('department', '')
            dept_serilaizer = None

            if department_name:
                dept = ProductDepartment.objects.filter(name=department_name).first()
                if dept:
                    dept_serilaizer = ProductDepartmentSerializer(dept, context={'request': request}).data
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                self.paginator.banner = dept_serilaizer # Pass to custom pagination class
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
                
            serializer = self.get_serializer(queryset, many=True)

            return Response({
                "status": status.HTTP_200_OK,
                "message": "Products retrieved successfully",
                "data": serializer.data,
                'banner': dept_serilaizer
            })
        except Exception as e:
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SingleProductAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
            serializer = ProductSerializer(product, context={'request': request})
            return Response({
                "status": status.HTTP_200_OK,
                "message": "Product retrieved successfully",
                "data": serializer.data
            })
        except Product.DoesNotExist:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Product not found",
                "data": []
            })
        except Exception as e:
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
                "data": []
            })


class ProductSliderAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        product = Product.objects.filter(is_available = True)[:7]
        serializer = ProductSerializer(product, many=True, context = {"request":request})
        return Response({
            "message": "Product slider retrieved successfully",
            "data": serializer.data
        },status=status.HTTP_200_OK)