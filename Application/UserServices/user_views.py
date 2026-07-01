from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status

from rest_framework import generics

from Application.permissions import IsUserAuthenticated

from Application.AuthenticationServices.auth_models import (
    User
)

from Application.AuthenticationServices.auth_utils import get_user_from_request


from .user_models import (
    UserAddress,
    UserCartModel,
    UserCartItemModel,
    UserOrderModel
)

from .user_serializers import (
    UserAddressSerializer,
    UserCartModelSerializer,
    UserCartItemModelSerializer,
    UserOrderModelSerializer
)

from Application.ProductServices.product_models import (
    Product
)


class UserCartListView(generics.ListAPIView):
    serializer_class = UserCartModelSerializer
    queryset = UserCartModel.objects.all()
    permission_classes = [IsUserAuthenticated]

    def get(self, request):
        try:
            cart, _ = UserCartModel.objects.get_or_create(user=request.user)

            total_products = UserCartItemModel.objects.filter(cart=cart).count()
            
            total_amount = 0
            for item in UserCartItemModel.objects.filter(cart=cart):
                if item.product.discount_price > 0:
                    total_amount += item.product.discount_price * item.quantity
                else:
                    total_amount += item.product.price * item.quantity

            orginal_amount = 0
            for item in UserCartItemModel.objects.filter(cart=cart):
                orginal_amount += item.product.price * item.quantity
            
            total_discount = orginal_amount - total_amount

            shipping_charge = 0

            if total_amount >= 1000:
                shipping_charge = 0
            else:
                shipping_charge = 100

            return Response({
                "message": "Cart items retrieved successfully",
                "data": UserCartModelSerializer([cart], many=True).data,
                "total_products": total_products,
                "total_amount": total_amount,
                "total_discount": total_discount,
                "shipping_charge": shipping_charge,
                "orginal_amount": orginal_amount
            },status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": str(e),
                "data": []
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AddCartItemView(generics.CreateAPIView):
    serializer_class = UserCartItemModelSerializer
    queryset = UserCartItemModel.objects.all()
    permission_classes = [IsUserAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            product_id = request.data.get('product_id')
            quantity = int(request.data.get('quantity', 1))

            if not product_id:
                return Response({
                    "message": "Product ID is required",
                    "data": []
                },status=status.HTTP_400_BAD_REQUEST)
            
            product = Product.objects.get(id=product_id)
            cart, _ = UserCartModel.objects.get_or_create(user=request.user)
            cart_item = UserCartItemModel.objects.filter(cart=cart, product=product)

            if cart_item.exists():
                cart_item.update(quantity=quantity+cart_item.first().quantity)
                return Response({
                    "message": "Cart item updated successfully",
                    "data": []
                }, status=status.HTTP_202_ACCEPTED)
            else:
                UserCartItemModel.objects.create(cart=cart, product=product, quantity=quantity)
                return Response({
                    "message": "Cart item added successfully",
                    "data": []
                },status=status.HTTP_201_CREATED)

        except Product.DoesNotExist:
            return Response({
                "message": "Product not found",
                "data": []
            },status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "message": str(e),
                "data": []
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
                            
class UpdateCartItemView(generics.UpdateAPIView):
    serializer_class = UserCartItemModelSerializer
    queryset = UserCartItemModel.objects.all()
    permission_classes = [IsUserAuthenticated]

    def patch(self, request, pk):
        try:
            cart_item_id = pk
            quantity = request.data.get('quantity')

            if not cart_item_id:
                return Response({
                    "message": "Cart item ID is required",
                    "data": []
                },status=status.HTTP_400_BAD_REQUEST)
            
            if not quantity:
                return Response({
                    "message": "Quantity is required",
                    "data": []
                },status=status.HTTP_400_BAD_REQUEST
                )
            cart_item = UserCartItemModel.objects.get(id=cart_item_id, cart__user=request.user)
            cart_item.quantity = quantity
            cart_item.save()
            return Response({
                "message": "Cart item updated successfully",
                "data": []
            },
            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": str(e),
                "data": []
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class DeleteCartItems(generics.DestroyAPIView):
    serializer_class = UserCartItemModelSerializer
    queryset = UserCartItemModel.objects.all()
    permission_classes = [IsUserAuthenticated]

    def delete(self, request, pk):
        try:
            cart_item_id = pk
            cart_item = UserCartItemModel.objects.get(id=cart_item_id, cart__user=request.user)
            cart_item.delete()
            return Response({
                "message": "Cart item deleted successfully",
                "data": []
            },
            status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({
                "message": str(e),
                "data": []
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DeleteCartView(generics.DestroyAPIView):
    serializer_class = UserCartModelSerializer
    queryset = UserCartModel.objects.all()
    permission_classes = [IsUserAuthenticated]

    def delete(self, request):
        try:
            cart = UserCartModel.objects.get(user=request.user)
            cart_items = UserCartItemModel.objects.filter(cart=cart)
            cart_items.delete()
            return Response({
                "message": "Cart deleted successfully",
                "data": []
            },
            status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({
                "message": str(e),
                "data": []
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
class GetUserAddressView(generics.ListAPIView):
    serializer_class = UserAddressSerializer
    queryset = UserAddress.objects.all()
    permission_classes = [IsUserAuthenticated]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                "status": status.HTTP_200_OK,
                "message": "Addresses retrieved successfully",
                "data": serializer.data
            })
        except Exception as e:
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddUserAddressView(generics.CreateAPIView):
    serializer_class = UserAddressSerializer
    queryset = UserAddress.objects.all()
    permission_classes = [IsUserAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({
                    "status": status.HTTP_201_CREATED,
                    "message": "Address added successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Validation Error",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateUserAddressView(generics.UpdateAPIView):
    serializer_class = UserAddressSerializer
    queryset = UserAddress.objects.all()
    permission_classes = [IsUserAuthenticated]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": status.HTTP_200_OK,
                    "message": "Address updated successfully",
                    "data": serializer.data
                })
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Validation Error",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteUserAddressView(generics.DestroyAPIView):
    serializer_class = UserAddressSerializer
    queryset = UserAddress.objects.all()
    permission_classes = [IsUserAuthenticated]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({
                "status": status.HTTP_200_OK,
                "message": "Address deleted successfully",
                "data": []
            })
        except Exception as e:
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
