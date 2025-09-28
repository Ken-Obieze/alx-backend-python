from rest_framework.pagination import PageNumberPagination


class MessagePagination(PageNumberPagination):
    page_size = 20  # default items per page
    page_size_query_param = "page_size"  # optional, client can override
    max_page_size = 100
