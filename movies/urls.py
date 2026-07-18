from django.urls import path, include
from .views import (
    MovieListAndCreateAPIView,
    MovieDetailAndUpdateAndDeleteAPIView,
)

urlpatterns = [
    # POST, GET List
    path('', MovieListAndCreateAPIView.as_view(), name='movie-list'),

    # GET, PUT, PATCH, DELETE
    path('<int:pk>/', MovieDetailAndUpdateAndDeleteAPIView.as_view(), name='movie-detail'),
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