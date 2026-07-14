from re import search
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from .user_serializers import *
from Application.AuthenticationServices.auth_models import User
from Application.UserServices.user_models import (
    UserOrderModel,
    ContactModel
)

from Application.PersonalDatas.personal_serializers import PhoneNumbersSerializer, PhoneNumbers as UserPhoneNumbers
from Dashbaord.paginations import DashboardCustomPagination
from django.db.models import Count, Sum

from ..utils import get_date_range_from_request
import csv
from django.http import HttpResponse


class UsersList(APIView):
    pagination_class = [DashboardCustomPagination]

    def get(self, request):
        users = User.objects.annotate(
            orders_count=Count('orders'),
            total_spend=Sum('orders__total_value')
        ).order_by('-date_joined') # Good practice to order them
        
        if request.GET.get('export') == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="users_list.csv"'
            writer = csv.writer(response)
            writer.writerow(['ID', 'Name', 'Email', 'Phone', 'Orders', 'Total Spend'])
            for user in users:
                writer.writerow([user.id, user.username, user.email, user.phone if user.phone else "", user.orders_count, float(user.total_spend or 0.0)])
            return response

        paginator = DashboardCustomPagination()
        paginated_users = paginator.paginate_queryset(users, request)
        
        data = [
            {
                "id": user.id,
                "name": user.username,
                "email": user.email,
                "phone": user.phone if user.phone else "",
                "orders": user.orders_count,
                "total_spend": float(user.total_spend or 0.0)
            } for user in paginated_users
        ]
        
        query_params = request.GET.copy()
        query_params['export'] = 'csv'
        export_csv_url = f"{request.build_absolute_uri(request.path)}?{query_params.urlencode()}"

        return Response({
            "status": 200,
            "message": "Users retrieved successfully",
            "data": data,
            "meta": {
                "count": paginator.page.paginator.count,
                "total_pages": paginator.page.paginator.num_pages,
                "current_page": paginator.page.number,
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link()
            },
            "export_csv_url": export_csv_url
        })


class UserContacts(APIView):
    def get(self, request):
        start_date, end_date = get_date_range_from_request(request)
        search_query = request.GET.get('search', '')
        contacts = ContactModel.objects.all().order_by('-created_at')
        
        if start_date and end_date:
            contacts = contacts.filter(created_at__range=(start_date, end_date))
        
        if search_query:
            contacts = contacts.filter(Q(name__icontains=search_query) | Q(phone__icontains=search_query) | Q(email__icontains=search_query) | Q(service__icontains=search_query) | Q(message__icontains=search_query))
            
        if request.GET.get('export') == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="user_contacts.csv"'
            
            writer = csv.writer(response)
            writer.writerow(['Name', 'Phone', 'Email', 'Service', 'Message', 'Is Read', 'Created At'])
            
            for contact in contacts:
                writer.writerow([
                    contact.name,
                    contact.phone,
                    contact.email,
                    contact.service,
                    contact.message,
                    'Yes' if contact.is_read else 'No',
                    contact.created_at.strftime('%Y-%m-%d %H:%M:%S')
                ])
            return response

        paginator = DashboardCustomPagination()
        paginated_contacts = paginator.paginate_queryset(contacts, request)

        data = ContactSerializer(paginated_contacts, many=True).data
        
        query_params = request.GET.copy()
        query_params['export'] = 'csv'
        export_csv_url = f"{request.build_absolute_uri(request.path)}?{query_params.urlencode()}"

        return Response({
            "status": 200,
            "message": "Contacts retrieved successfully",
            "data": data,
            "meta": {
                "count": paginator.page.paginator.count,
                "total_pages": paginator.page.paginator.num_pages,
                "current_page": paginator.page.number,
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link()
            },
            "export_csv_url": export_csv_url
        })

class UserPhoneNumbersAPIview(APIView):
    def get(self, request):
        start_date, end_date = get_date_range_from_request(request)
        search_query = request.GET.get('search', '')
        phone_numbers = UserPhoneNumbers.objects.all().order_by('-created_at')
        
        if start_date and end_date:
            phone_numbers = phone_numbers.filter(created_at__range=(start_date, end_date))
        
        if search_query:
            phone_numbers = phone_numbers.filter(Q(name__icontains=search_query) | Q(phone_number__icontains=search_query))
            
        if request.GET.get('export') == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="user_phone_numbers.csv"'
            
            writer = csv.writer(response)
            writer.writerow(['Name', 'Phone Number', 'Created At'])
            
            for phone in phone_numbers:
                writer.writerow([
                    phone.name,
                    phone.phone_number,
                    phone.created_at.strftime('%Y-%m-%d %H:%M:%S')
                ])
            return response

        paginator = DashboardCustomPagination()
        paginated_phones = paginator.paginate_queryset(phone_numbers, request)

        data = PhoneNumbersSerializer(paginated_phones, many=True).data
        
        query_params = request.GET.copy()
        query_params['export'] = 'csv'
        export_csv_url = f"{request.build_absolute_uri(request.path)}?{query_params.urlencode()}"

        return Response({
            "status": 200,
            "message": "Phone numbers retrieved successfully",
            "data": data,
            "meta": {
                "count": paginator.page.paginator.count,
                "total_pages": paginator.page.paginator.num_pages,
                "current_page": paginator.page.number,
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link()
            },
            "export_csv_url": export_csv_url
        })
