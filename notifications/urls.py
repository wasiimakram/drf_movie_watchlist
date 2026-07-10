from django.urls import path
from .views import NotificationListAPIView, NotificationUpdateAPIView

urlpatterns = [
    # GET list
    path('', NotificationListAPIView.as_view(), name='notification-list'),

    # GET one, PATCH mark-as-read
    path('<int:pk>/', NotificationUpdateAPIView.as_view(), name='notification-detail'),
]