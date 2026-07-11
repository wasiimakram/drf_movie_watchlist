from rest_framework import generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Movie
from .serializers import MovieSerializer, MovieListSerializer
from .filters import MovieFilter
from .pagination import MoviePagination
from .throttles import MovieUserThrottle

class MovieListAndCreateAPIView(generics.ListCreateAPIView):

    """
    GET /api/movies --> List all movies (filterable, searchable, orderable, paginated)
    POST /api/movies --> Create a new movie

    Example (structured filters, from MovieFilter):
      /api/movies/?year_min=2000&year_max=2015&rating_min=7.5&rating_max=9
      &runtime_min=90&runtime_max=150&category=2&director=nolan
      &language=English&country=USA

    Example (free-text search, OR's across search_fields):
      /api/movies/?search=nolan

    Example (sorting, '-' prefix = descending, comma-separated = multi-field):
      /api/movies/?ordering=-imdb_rating,year

    Example (pagination, see MoviePagination):
      /api/movies/?page=2&page_size=25
    """

    # Before: Movie.objects.all() -> 1 query for movies + 1 query PER movie
    # to fetch its categories (for category_detail in the serializer). N+1.
    #
    # After: prefetch_related runs ONE extra query for ALL categories needed,
    # then joins them in Python. Total stays at 2 queries no matter how many
    # movies are returned.
    #
    # select_related =  We use it when we have 1 to 1 relationship. It will run only 1 query
    #                   Not needed here since

    # prefetch_related = When we have M2M relationship.

    # with_categories() = MovieQuerySet method (see movies/models.py) that
    # wraps prefetch_related('category') so it's defined once, not repeated
    # in every view.
    queryset = Movie.objects.with_categories()

    # Response shaping (concept #23): this view serves TWO kinds of request with diff serializers,
    # so instead of one fixed serializer_class it picks per request:
    #   GET  (list)   -> MovieListSerializer  (light, card-sized fields)
    #   POST (create) -> MovieSerializer      (all fields + all validations)
    # get_serializer_class() is to serializer_class what get_queryset() is to
    # queryset — the dynamic method version of the static attribute.
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MovieSerializer 
        return MovieListSerializer

    # Stacked backends, applied in order: filter -> search -> order. GET/list-only.
    # This search only based on specific columns and return result
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Structured filters (?year_min=, ?category=, ?director=) — see movies/filters.py
    filterset_class = MovieFilter

    # SearchFilter: ?search=<term> matches if ANY of these fields contain
    # the term. Its will filter out from  all mentioned columns.
    search_fields = ['title', 'director', 'plot']

    # Whitelisted sortable fields — ?ordering=-imdb_rating,year
    ordering_fields = ['year', 'imdb_rating', 'runtime_minutes', 'created_at']

    # Default sort when no ?ordering= is passed. "-" means decending
    ordering = ['-created_at']

    # Pagination — see movies/pagination.py. ?page=2&page_size=25
    pagination_class = MoviePagination

    # Rate limit — 50 requests/min per user (see movies/throttles.py)
    throttle_classes = [MovieUserThrottle]

    # Every request must include a valid JWT access token
    permission_classes = [permissions.IsAuthenticated]

class MovieDetailAndUpdateAndDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):

    """
    GET: Retrieve specific movie
    PUT/PATCH: Update movie
    PATCH: In patch, we can only pass specific value that needs to be updated
    PUT: In PUT we need to send the whole object to update even 1 value.
    DELETE: Delete movie
    """

    queryset = Movie.objects.with_categories()
    serializer_class = MovieSerializer

    # Same rate limit + auth requirement as the list/create view
    throttle_classes = [MovieUserThrottle]
    permission_classes = [permissions.IsAuthenticated]