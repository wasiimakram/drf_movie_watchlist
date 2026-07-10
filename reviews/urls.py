from django.urls import path
from .views import (
    ListAndCreateAPIView,
    DetailAndUpdateAndDeleteAPIView,
)

urlpatterns = [
    # POST, GET List
    path('', ListAndCreateAPIView.as_view(), name='review-list'),

    # GET, PUT, PATCH, DELETE
    path('<int:pk>/', DetailAndUpdateAndDeleteAPIView.as_view(), name='review-detail'),
]
