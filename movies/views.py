from rest_framework import generics, filters, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from categories.models import Category
from .models import Movie
from .serializers import MovieSerializer, MovieListSerializer
from .filters import MovieFilter
from .pagination import MoviePagination
from .throttles import MovieUserThrottle
from .services import fetch_movie_from_omdb, OmdbError

"""
The core piece — cache_page(60): wraps a view function so that the first call runs it 
normally and stores the response in Redis; every call after that, for 60 seconds, 
returns the stored copy without touching your view code (no DB query, no filters) at all.
"""
@method_decorator(cache_page(60), name='get')  # cache GET responses for 60s
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

    # Catalog rule (built-in DjangoModelPermissions):
    #   GET    -> any authenticated user
    #   POST   -> needs 'add_movie' permission    (superuser/admin has ALL perms automatically)
    #   PUT/PATCH -> 'change_movie', DELETE -> 'delete_movie'
    # Normal signups hold no permissions -> read-only for them, no custom code.
    permission_classes = [permissions.DjangoModelPermissions]

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

    # Same rate limit as the list/create view
    throttle_classes = [MovieUserThrottle]
    # Same catalog rule: read for all authenticated, write only with model permissions
    permission_classes = [permissions.DjangoModelPermissions]


class MovieImportAPIView(APIView):
    """
    POST /api/movies/import/   {"title": "Interstellar"}   (admin only)

    Concept #28: our backend acting as an API CLIENT — it calls OMDB,
    translates the answer, and saves a full movie from just a title.
    A real APIView (concept #22 floor 1): not CRUD-on-a-queryset, so
    generics don't fit — we write post() by hand.
    """
    permission_classes = [permissions.IsAdminUser]  # is_staff only, built-in

    def post(self, request):
        title = request.data.get('title')
        if not title:
            return Response({'title': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Ask OMDB (all external-API mess lives in services.py)
        try:
            movie_data = fetch_movie_from_omdb(title)
        except OmdbError as e:
            # 502 Bad Gateway = "an upstream server let US down" — the honest
            # status when the failure is OMDB's side, not the client's.
            return Response({'detail': str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        # 2. Genre names -> Category rows. get_or_create reuses existing
        # categories ("Sci-Fi" exists? use it) and creates the new ones —
        # our Category.save() auto-generates slugs as usual.
        category_ids = []
        for genre_name in movie_data.pop('genres'):
            category, _created = Category.objects.get_or_create(name=genre_name)
            category_ids.append(category.id)
        movie_data['category'] = category_ids

        # 3. Reuse MovieSerializer so ALL our validations run — including
        # the duplicate title+year check. Import twice -> clean 400.
        serializer = MovieSerializer(data=movie_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ============================================================================
# CONCEPT #22 REFERENCE — the SAME movie API on the other two "floors".
  # Commented out on purpose: our real implementation is the generics version
# above. Kept here so the three styles can be compared side by side.
# ============================================================================

# ---------------- Floor 1: APIView — manual mode ----------------
# You write one method per HTTP verb, and every step inside it by hand.
# Compare with MovieListAndCreateAPIView above: same result, but we LOSE all
# the free extras (filtering, search, ordering, pagination, throttling) —
# each would need manual wiring here.
#
# URLs: wired exactly like our generics — same style, same path() lines:
#     path('', MovieListAPIView.as_view(), name='movie-list'),
#     path('<int:pk>/', MovieDetailAPIView.as_view(), name='movie-detail'),

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.shortcuts import get_object_or_404
#
#
# class MovieListAPIView(APIView):
#
#     def get(self, request):
#         movies = Movie.objects.with_categories()                  # you fetch
#         serializer = MovieListSerializer(movies, many=True)       # you serialize
#         return Response(serializer.data)                          # you respond
#
#     def post(self, request):
#         serializer = MovieSerializer(data=request.data)           # you bind input
#         serializer.is_valid(raise_exception=True)                 # you validate (400 on fail)
#         serializer.save()                                         # you save
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class MovieDetailAPIView(APIView):
#
#     def get(self, request, pk):
#         movie = get_object_or_404(Movie, pk=pk)                   # you fetch-or-404
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
#
#     def patch(self, request, pk):
#         movie = get_object_or_404(Movie, pk=pk)
#         # partial=True = PATCH semantics: only sent fields are updated
#         serializer = MovieSerializer(movie, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         movie = get_object_or_404(Movie, pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# ---------------- Floor 3: ViewSet — bundle mode ----------------
# ONE class replaces BOTH generic classes above (list + detail + all writes),
# and urls.py is replaced by a router (see commented block in movies/urls.py):
#     router = DefaultRouter()
#     router.register('', MovieViewSet, basename='movie')
#     urlpatterns = router.urls
# The router GENERATES what we hand-write today:
#     ''          -> list + create            (GET, POST)
#     '<int:pk>/' -> detail + update + delete (GET, PUT, PATCH, DELETE)
# Note: looks identical to a generic view — because it IS the same machinery,
# one floor up. Our hooks (get_serializer_class, filter_backends, pagination,
# throttles, permissions) would all still work on it unchanged.

# from rest_framework import viewsets
#
#
# class MovieViewSet(viewsets.ModelViewSet):
#     queryset = Movie.objects.with_categories()
#     serializer_class = MovieSerializer