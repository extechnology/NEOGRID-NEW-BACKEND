from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .dealers_serializers import *
from Application.DealerServices.dealer_models import WarrantyRegisterModel
from ..utils import get_date_range_from_request

from ..paginations import DashboardCustomPagination
import csv
from django.http import HttpResponse

from Application.permissions import IsSuperUserAuthenticated

class RegisterdWarranty(APIView):
    permission_classes = [IsSuperUserAuthenticated]
    def get(self, request):
        start_date, end_date = get_date_range_from_request(request)
        data = WarrantyRegisterModel.objects.all().order_by('-created_at')
        
        if start_date and end_date:
            data = data.filter(created_at__range=[start_date, end_date])
            
        # CSV Export
        if request.GET.get('export') == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="registered_warranty.csv"'
            
            writer = csv.writer(response)
            writer.writerow(['Full Name', 'Email', 'Phone', 'Address', 'State', 'District', 'Pincode', 'Franchise', 'Product Name', 'Model Number', 'Serial Number', 'Purchased Date', 'Created At'])
            
            for item in data:
                writer.writerow([
                    item.fullname, item.email, item.phone, item.address, 
                    item.state, item.district, item.pincode, item.franchise, 
                    item.product_name, item.model_number, item.serial_number, 
                    item.purchased_date, item.created_at.strftime('%Y-%m-%d %H:%M:%S')
                ])
            return response

        # Pagination
        paginator = DashboardCustomPagination()
        paginated_data = paginator.paginate_queryset(data, request)
        
        serializer = WarrantyRegisterSerializers(paginated_data, many=True)

        # Build export_csv_url with existing query parameters
        query_params = request.GET.copy()
        query_params['export'] = 'csv'
        export_csv_url = f"{request.build_absolute_uri(request.path)}?{query_params.urlencode()}"

        return Response({
            "status": 200,
            "message": "Warranty data fetched successfully.",
            "data": serializer.data,
            "meta": {
                "count": paginator.page.paginator.count,
                "total_pages": paginator.page.paginator.num_pages,
                "current_page": paginator.page.number,
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link()
            },
            "export_csv_url": export_csv_url
        })