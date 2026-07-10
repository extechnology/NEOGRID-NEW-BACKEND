from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Sum, Count

from Application.UserServices.user_models import (
    UserOrderItemModel, UserOrderModel,
    UserAddress
)
from Application.ProductServices.product_models import (
    ProductDepartment, ProductFamily,
    Product, ProductImages
)
from .order_serializers import (
    OrderItemSerializer, OrderSerializer, ProductSerilaizer
)
from Application.permissions import IsSuperUserAuthenticated
from ..utils import get_date_range_from_request
from ..paginations import DashboardCustomPagination
from .order_emails import send_order_update_email

class OrdersStats(APIView):
    permission_classes = [IsSuperUserAuthenticated]
    def get(self, request):
        start_date, end_date = get_date_range_from_request(request)

        # Base query for all orders
        base_query = UserOrderModel.objects.all()

        # Apply date filters
        if start_date and end_date:
            base_query = base_query.filter(created_at__range=(start_date, end_date))
        elif end_date:
            base_query = base_query.filter(created_at__lte=end_date)
        elif start_date:
            base_query = base_query.filter(created_at__gte=start_date)

        stats = base_query.aggregate(
            total_orders=Count('id'),
            total_orders_value=Sum('total_value'),
            revenue=Sum('total_value', filter=Q(status='CONFIRMED')),
            completed=Count('id', filter=Q(status='DELIVERED')),
            pending=Count('id', filter=Q(status='PENDING')),
        )

        return Response({
            'total_orders': stats['total_orders'] or 0,
            'total_orders_value': float(stats['total_orders_value'] or 0),
            'revenue': float(stats['revenue'] or 0),
            'orders': stats['total_orders'] or 0,
            'completed': stats['completed'] or 0,
            'pending': stats['pending'] or 0
        }, status=status.HTTP_200_OK)



class Orders(APIView):
    permission_classes = [IsSuperUserAuthenticated]
    pagination_class = [DashboardCustomPagination]
    def get(self, request):
        start_date, end_date = get_date_range_from_request(request)

        # Base query for all orders
        base_query = UserOrderModel.objects.all()

        # Apply date filters
        if start_date and end_date:
            base_query = base_query.filter(created_at__range=(start_date, end_date))
        elif end_date:
            base_query = base_query.filter(created_at__lte=end_date)
        elif start_date:
            base_query = base_query.filter(created_at__gte=start_date)
        # Search functionality
        search_query = request.GET.get('search', '').strip()
        if search_query:
            base_query = base_query.filter(
                Q(order_id__icontains=search_query) |
                Q(user__email__icontains=search_query)
            )
            
        # Status filter
        status_query = request.GET.get('status', '').strip().upper()
        if status_query:
            base_query = base_query.filter(status=status_query)

        # Order by newest
        base_query = base_query.order_by('-created_at')

        # CSV Export Functionality
        if request.GET.get('export') == 'csv':
            import csv
            from django.http import HttpResponse
            
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="orders.csv"'
            
            writer = csv.writer(response)
            writer.writerow(['Order ID', 'Customer Email', 'Total Value', 'Status', 'Date Created'])
            
            # Use an iterator or just evaluate if it's not too massive. For massive lists, iterator() is better.
            for order in base_query.select_related('user').iterator():
                writer.writerow([
                    order.order_id,
                    order.user.email if order.user else 'N/A',
                    order.total_value,
                    order.status,
                    order.created_at.strftime("%Y-%m-%d %H:%M:%S") if order.created_at else 'N/A'
                ])
                
            return response

        # Pagination
        paginator = DashboardCustomPagination()
        paginator.message = "Orders retrieved successfully"
        paginated_queryset = paginator.paginate_queryset(base_query, request)

        # Serialize
        serializer = OrderSerializer(paginated_queryset, many=True, context={'request': request})
        response = paginator.get_paginated_response(serializer.data)
        
        # Build the CSV export URL preserving active search and date filters
        query_params = request.GET.copy()
        query_params['export'] = 'csv'
        
        # Add the CSV download link directly to the JSON response
        response.data['export_csv_url'] = f"{request.build_absolute_uri(request.path)}?{query_params.urlencode()}"
        
        return response

class OrderUpdate(APIView):
    permission_classes = [IsSuperUserAuthenticated]

    def put(self, request, order_id):
        try:
            order = UserOrderModel.objects.get(order_id=order_id)
        except UserOrderModel.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        status_update = request.data.get('status')
        if status_update:
            order.status = status_update
            
        tracking_id = request.data.get('tracking_id')
        if tracking_id is not None:
            order.tracking_id = tracking_id
            
        tracking_url = request.data.get('tracking_url')
        if tracking_url is not None:
            order.tracking_url = tracking_url

        order.save()

        # Send the order update email asynchronously
        send_order_update_email(order)

        serializer = OrderSerializer(order)
        return Response({
            "message": "Order updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
