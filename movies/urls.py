from django.urls import path, include
from .views import (
    MovieListAndCreateAPIView,
    MovieDetailAndUpdateAndDeleteAPIView,
    MovieImportAPIView,
)
from reviews.views import MovieReviewsListAPIView

urlpatterns = [
    # POST, GET List
    path('', MovieListAndCreateAPIView.as_view(), name='movie-list'),

    # POST {"title": "..."} -> fetch from OMDB + create (admin only).
    # Keep it at top, so it don't mix with <id> request.
    path('import-from-omdb/', MovieImportAPIView.as_view(), name='movie-import'),

    # GET, PUT, PATCH, DELETE
    path('<int:pk>/', MovieDetailAndUpdateAndDeleteAPIView.as_view(), name='movie-detail'),

    # Nested route: all reviews of ONE movie (view lives in the reviews app).
    # <int:movie_id> here is what the view reads as self.kwargs['movie_id'].
    path('<int:movie_id>/reviews/', MovieReviewsListAPIView.as_view(), name='movie-reviews'),
]

# ---------------- Concept #22 reference: ViewSet + router (commented) ----------------
# The router version replaces this WHOLE file's urlpatterns with 2 lines —
# and generates the same two URLs we wrote by hand above:
#     ''          -> list + create           (GET, POST)
#     '<int:pk>/' -> detail + update + delete (GET, PUT, PATCH, DELETE)
#
# from rest_framework.routers import DefaultRouter
# from .views import MovieViewSet
#
# router = DefaultRouter()
# router.register('', MovieViewSet, basename='movie')
# urlpatterns = router.urls
#
# Trade-off: fewer lines, but the URLs are no longer visible in this file —
# you must know the router's conventions to know what endpoints exist.