from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status
from django.db.models import Prefetch

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
    UserOrderModel,
    UserOrderItemModel,
)

from .user_serializers import (
    UserAddressSerializer,
    UserCartModelSerializer,
    UserCartItemModelSerializer,
    UserOrderModelSerializer,
    VerifyPaymentSerializer,

    UserAddressSerializerForListOrder,
    OrderItemSerializerForListOrder,
    OrderProductSerializerForListOrder,
    UserOrderDetailSerializerForListOrder,
)

from django.conf import settings
import razorpay

from Application.ProductServices.product_models import (
    Product,
    ProductImages
)
from .user_utils import generate_invoice_pdf
from .user_mails import send_order_created_email, send_payment_failed_email


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
            for item in UserCartItemModel.objects.filter(cart=cart):
                if item.product and item.product.shipping_charge:
                    shipping_charge += item.product.shipping_charge * item.quantity

            total_amount += shipping_charge

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

class CreateOrderView(APIView):
    permission_classes = [IsUserAuthenticated]

    def post(self, request):
        try:
            address_id = request.data.get('address_id')

            cart = UserCartModel.objects.get(user=request.user)
            items = UserCartItemModel.objects.filter(cart=cart)

            total_value = request.data.get('total_value')

            print("************************************")
            print("cart",cart)
            print(total_value)
            print(request.data)
            print(address_id)
            print('razorpay Key:',settings.RAZORPAY_KEY_ID)
            print("************************************")

            if not items:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Cart is empty.",
                    "data": []
                }, status=status.HTTP_400_BAD_REQUEST)

            if not address_id or not total_value:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "address_id and total_value are required.",
                    "data": []
                }, status=status.HTTP_400_BAD_REQUEST)

            address = UserAddress.objects.filter(unique_id=address_id, user=request.user).first()
            if not address:
                return Response({
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Address not found.",
                    "data": []
                }, status=status.HTTP_404_NOT_FOUND)

            # Initialize Razorpay Client
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            # Create Order in Razorpay
            # amount is in paise, so multiply by 100
            payment_amount = int(float(total_value) * 100)
            data = {
                "amount": payment_amount,
                "currency": "INR",
                "payment_capture": "1"
            }
            razorpay_order = client.order.create(data=data)

            # Create Local Order
            order = UserOrderModel.objects.create(
                user=request.user,
                address=address,
                total_value=total_value,
                razorpay_order_id=razorpay_order['id'],
                status='PENDING'
            )
            
            for i in items:
                UserOrderItemModel.objects.create(
                    order=order,
                    product=i.product,
                    quantity=i.quantity
                )

            return Response({
                "status": status.HTTP_201_CREATED,
                "message": "Order created successfully",
                "data": {
                    "order_id": order.order_id,
                    "razorpay_order_id": razorpay_order['id'],
                    "amount": payment_amount,
                    "currency": "INR",
                    "key_id":settings.RAZORPAY_KEY_ID
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyOrderView(APIView):
    permission_classes = [IsUserAuthenticated]

    def post(self, request):
        try:
            serializer = VerifyPaymentSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Validation Error",
                    "data": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            razorpay_order_id = serializer.validated_data['razorpay_order_id']
            razorpay_payment_id = serializer.validated_data['razorpay_payment_id']
            razorpay_signature = serializer.validated_data['razorpay_signature']

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }

            order = UserOrderModel.objects.filter(razorpay_order_id=razorpay_order_id, user=request.user).first()
            if not order:
                return Response({
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Order not found",
                    "data": []
                }, status=status.HTTP_404_NOT_FOUND)

            try:
                client.utility.verify_payment_signature(params_dict)
            except razorpay.errors.SignatureVerificationError:
                send_payment_failed_email(order)
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Payment verification failed",
                    "data": []
                }, status=status.HTTP_400_BAD_REQUEST)

            order.razorpay_payment_id = razorpay_payment_id
            order.razorpay_signature = razorpay_signature
            order.status = 'CONFIRMED'
            order.save()

            cart = UserCartModel.objects.get(user=request.user)
            items = UserCartItemModel.objects.filter(cart=cart)
            items.delete()
            
            # Generate and save invoice
            generate_invoice_pdf(order)
            
            # Send confirmation email
            send_order_created_email(order)

            return Response({
                "status": status.HTTP_200_OK,
                "message": "Payment verified and order updated successfully",
                "data": UserOrderModelSerializer(order).data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserOrderDetailAPIView(generics.ListAPIView):
    serializer_class = UserOrderDetailSerializerForListOrder
    permission_classes = [IsUserAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return (
            UserOrderModel.objects.filter(user=self.request.user).order_by("-id")
            .select_related("address")
            .prefetch_related(
                Prefetch(
                    "items__product__images",
                    queryset=ProductImages.objects.order_by("id"),
                )
            )
        )