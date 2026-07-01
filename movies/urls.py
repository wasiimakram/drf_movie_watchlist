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