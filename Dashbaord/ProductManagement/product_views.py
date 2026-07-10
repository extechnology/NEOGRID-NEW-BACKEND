from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .product_serializers import (
    ProductDepartmentSerializers,
    ProductFamilySerializers,
    ProductImagesSerializers,
    ProductSerializers
)
from Application.ProductServices.product_models import (
    ProductDepartment, ProductFamily,
    Product, ProductImages
)
from django.db import transaction


class Products(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializers(products, many=True, context={'request': request})
        return Response({
            'message': "Products retrieved successfully",
            'data': serializer.data
        },status=status.HTTP_200_OK)

from rest_framework import generics

# Product Department Views
class ProductDepartmentCreate(generics.CreateAPIView):
    queryset = ProductDepartment.objects.all()
    serializer_class = ProductDepartmentSerializers

class ProductDepartmentUpdate(generics.UpdateAPIView):
    queryset = ProductDepartment.objects.all()
    serializer_class = ProductDepartmentSerializers

# Product Family Views
class ProductFamilyCreate(generics.CreateAPIView):
    queryset = ProductFamily.objects.all()
    serializer_class = ProductFamilySerializers

class ProductFamilyUpdate(generics.UpdateAPIView):
    queryset = ProductFamily.objects.all()
    serializer_class = ProductFamilySerializers

# Product Views
class ProductCreate(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

class ProductUpdate(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

# Product Images Views
class ProductImagesCreate(generics.CreateAPIView):
    queryset = ProductImages.objects.all()
    serializer_class = ProductImagesSerializers

class ProductImagesUpdate(generics.UpdateAPIView):
    queryset = ProductImages.objects.all()
    serializer_class = ProductImagesSerializers

class DepartmentFamilyCreate(APIView):
    """
    Creates a ProductDepartment and a ProductFamily inside it in a single request.
    Expects multipart/form-data.
    """
    def post(self, request):
        data = request.data
        
        if not data.get('department_name') or not data.get('family_name'):
            return Response({"error": "department_name and family_name are required."}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            with transaction.atomic():
                department = ProductDepartment.objects.create(
                    name=data.get('department_name'),
                    description=data.get('department_description', ''),
                    image=request.FILES.get('department_image')
                )
                
                family = ProductFamily.objects.create(
                    department=department,
                    name=data.get('family_name'),
                    image=request.FILES.get('family_image')
                )
                
            return Response({
                "message": "Department and Family created successfully",
                "department_id": department.id,
                "family_id": family.id
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProductWithImagesCreate(APIView):
    """
    Creates a Product and multiple ProductImages in a single request.
    Expects multipart/form-data.
    """
    def post(self, request):
        data = request.data
        
        if not data.get('family_id') or not data.get('name'):
            return Response({"error": "family_id and name are required."}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            with transaction.atomic():
                product = Product.objects.create(
                    family_id=data.get('family_id'),
                    name=data.get('name'),
                    model_type=data.get('model_type', ''),
                    model_number=data.get('model_number', ''),
                    price=data.get('price') or 0,
                    discount_percentage=data.get('discount_percentage') or 0,
                    discount_price=data.get('discount_price') or 0,
                    description=data.get('description', ''),
                    additional_info=data.get('additional_info', ''),
                    technical_spec=data.get('technical_spec', ''),
                    warrenty_info=data.get('warrenty_info', ''),
                    new_arrival=str(data.get('new_arrival', 'false')).lower() == 'true',
                    shipping_charge=data.get('shipping_charge') or 0,
                    is_available=str(data.get('is_available', 'true')).lower() == 'true',
                )
                
                images = request.FILES.getlist('product_images')
                for img in images:
                    ProductImages.objects.create(
                        product=product,
                        image=img
                    )
                    
            return Response({
                "message": "Product and images created successfully",
                "product_id": product.id
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)