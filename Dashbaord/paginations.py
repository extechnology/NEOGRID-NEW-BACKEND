from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

class DashboardCustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "status": status.HTTP_200_OK,
            "message": getattr(self, 'message', "Data retrieved successfully"),
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
