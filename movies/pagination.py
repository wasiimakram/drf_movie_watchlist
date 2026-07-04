from rest_framework.pagination import PageNumberPagination


class MoviePagination(PageNumberPagination):
    # Default number of movies per page when the client sends no ?page_size=
    page_size = 10

    # Lets the client override page size — ?page_size=25
    page_size_query_param = 'page_size'

    # Hard cap so a client can't request ?page_size=999999 and defeat pagination
    max_page_size = 100
