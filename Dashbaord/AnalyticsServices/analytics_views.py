from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q, Sum, Count
from django.db.models.functions import ExtractMonth, TruncDate, Coalesce
from django.utils import timezone
from datetime import timedelta, datetime
import calendar

from ..utils import get_date_range_from_request
from Application.AuthenticationServices.auth_models import User
from Application.UserServices.user_models import (
    UserOrderItemModel,
    UserOrderModel
)
from Application.ProductServices.product_models import (
    Product,
    ProductDepartment,
    ProductFamily,
    ProductImages
)
from Application.permissions import IsSuperUserAuthenticated

class PerformanceStats(APIView):
    permission_classes = [IsSuperUserAuthenticated]
    def get(self, request):
        search_query = request.GET.get('search', '').strip()
        start_date, end_date = get_date_range_from_request(request)

        # Base query for orders
        base_query = UserOrderModel.objects.filter(status='CONFIRMED')

        # Apply date filters
        if start_date and end_date:
            base_query = base_query.filter(created_at__range=(start_date, end_date))
        elif end_date:
            base_query = base_query.filter(created_at__lte=end_date)
        elif start_date:
            base_query = base_query.filter(created_at__gte=start_date)

        # Apply search filter
        if search_query:
            base_query = base_query.filter(
                Q(order_id__icontains=search_query) |
                Q(user__email__icontains=search_query)
            )

        # 1. Total Revenue, Orders, and Customers (optimized into a single query)
        stats = base_query.aggregate(
            total_revenue=Sum('total_value'),
            total_orders=Count('id'),
            total_customers=Count('user', distinct=True)
        )
        
        revenue = stats['total_revenue'] or 0
        orders = stats['total_orders'] or 0
        customers = stats['total_customers'] or 0

        # 4. Average Order Value
        avarage_orders = round(float(revenue) / orders, 2) if orders > 0 else 0

        return Response({
            'revenue': float(revenue),
            'orders': orders,
            'customers': customers,
            'avarage_orders': float(avarage_orders)
        }, status=status.HTTP_200_OK)


class RevenueTrend(APIView):
    permission_classes = [IsSuperUserAuthenticated]

    def get(self, request):
        try:
            year = int(request.GET.get('year', timezone.now().year))
        except ValueError:
            year = timezone.now().year
            
        # Initialize data for all 12 months
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        trend_data = {month: 0 for month in months}
        
        # Query monthly revenue for the given year
        monthly_revenues = UserOrderModel.objects.filter(
            status='CONFIRMED',
            created_at__year=year
        ).annotate(
            month=ExtractMonth('created_at')
        ).values('month').annotate(
            total=Sum('total_value')
        ).order_by('month')
        
        # Populate the trend_data dictionary
        for entry in monthly_revenues:
            month_idx = entry['month'] - 1 # ExtractMonth returns 1-12
            if 0 <= month_idx < 12:
                month_name = months[month_idx]
                trend_data[month_name] = float(entry['total'] or 0)
                
        # Format trend data as a list of dictionaries for the frontend chart
        formatted_trend = [
            {"month": month, "revenue": revenue} 
            for month, revenue in trend_data.items()
        ]
        
        # Calculate YoY Growth (reuse already calculated monthly sums for current year)
        current_year_revenue = sum(trend_data.values())
        
        previous_year_revenue = UserOrderModel.objects.filter(
            status='CONFIRMED', created_at__year=year - 1
        ).aggregate(total=Sum('total_value'))['total'] or 0
        
        yoy_growth = 0
        if previous_year_revenue > 0:
            yoy_growth = ((float(current_year_revenue) - float(previous_year_revenue)) / float(previous_year_revenue)) * 100
        elif current_year_revenue > 0:
            yoy_growth = 100
            
        return Response({
            "year": year,
            "total_revenue": float(current_year_revenue),
            "yoy_growth": round(yoy_growth, 1),
            "trend_data": formatted_trend
        }, status=status.HTTP_200_OK)


class OrderStatusWheel(APIView):
    def get(self, request):
        start_date, end_date = get_date_range_from_request(request)

        # Base query for orders
        base_query = UserOrderModel.objects.all()

        if start_date and end_date:
            base_query = base_query.filter(created_at__range=(start_date, end_date))
        elif end_date:
            base_query = base_query.filter(created_at__lte=end_date)
        elif start_date:
            base_query = base_query.filter(created_at__gte=start_date)  

        # Aggregate status counts in a single query
        status_counts = base_query.values('status').annotate(count=Count('id'))
        
        counts = {
            'CONFIRMED': 0,
            'PENDING': 0,
            'SHIPPED': 0,
            'DELIVERED': 0,
            'CANCELLED': 0,
        }
        
        for item in status_counts:
            if item['status'] in counts:
                counts[item['status']] = item['count']

        data = [
            {'status': s, 'count': c} for s, c in counts.items()
        ]

        # Sort by count in descending order
        sorted_data = sorted(data, key=lambda x: x['count'], reverse=True)

        return Response(sorted_data, status=status.HTTP_200_OK)


class DailyOrder(APIView):
    permission_classes = [IsSuperUserAuthenticated]

    def get(self, request):
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=13)
        
        # Generate list of last 14 dates
        date_list = [start_date + timedelta(days=i) for i in range(14)]
        trend_data = {d: 0 for d in date_list}
        
        # Query orders in the last 14 days
        daily_orders = UserOrderModel.objects.filter(
            created_at__date__range=(start_date, end_date)
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        for entry in daily_orders:
            d = entry['date']
            # TruncDate might return datetime or date depending on database backend
            if isinstance(d, datetime):
                d = d.date()
            if d in trend_data:
                trend_data[d] = entry['count']
                
        formatted_trend = [
            {"date": f"{d.strftime('%b')} {d.day}", "orders": count}
            for d, count in trend_data.items()
        ]
        
        return Response({
            "trend_data": formatted_trend
        }, status=status.HTTP_200_OK)


class TopProducts(APIView):
    permission_classes = [IsSuperUserAuthenticated]

    def get(self, request):
        start_date, end_date = get_date_range_from_request(request)

        # Build filter for the Sum aggregation
        order_filter = Q(order_items__order__status='CONFIRMED')
        if start_date and end_date:
            order_filter &= Q(order_items__order__created_at__range=(start_date, end_date))
        elif end_date:
            order_filter &= Q(order_items__order__created_at__lte=end_date)
        elif start_date:
            order_filter &= Q(order_items__order__created_at__gte=start_date)  

        # Annotate total sold matching the filter, replacing None with 0
        top_products = (
            Product.objects
            .annotate(
                total_sold=Coalesce(Sum('order_items__quantity', filter=order_filter), 0)
            )
            .order_by('-total_sold', 'id')[:5]
            .values('id', 'name', 'description', 'price', 'total_sold')
        )

        return Response(list(top_products), status=status.HTTP_200_OK)

class RecentOrders(APIView):
    permission_classes = [IsSuperUserAuthenticated]

    def get(self, request):
        start_date, end_date = get_date_range_from_request(request)

        base_query = UserOrderModel.objects.all()

        if start_date and end_date:
            base_query = base_query.filter(created_at__range=(start_date, end_date))
        elif end_date:
            base_query = base_query.filter(created_at__lte=end_date)
        elif start_date:
            base_query = base_query.filter(created_at__gte=start_date)  

        recent_orders = base_query.order_by('-created_at')[:10].values(
            'order_id', 'user__email', 'total_value', 'status', 'created_at'
        )

        return Response(list(recent_orders), status=status.HTTP_200_OK)        
