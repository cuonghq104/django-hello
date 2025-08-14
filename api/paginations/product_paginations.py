import math

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomProductPagination(PageNumberPagination):
    page_size = 6
    max_page_size = 6
    page_size_query_param = 'page_size'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        total_pages = math.ceil(self.page.paginator.count / self.get_page_size(self.request))

        return Response({
            'count': self.page.paginator.count,
            'total_pages': total_pages,
            'current_page': self.page.number,
            'results': data
        })
