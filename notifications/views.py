from rest_framework import generics, permissions
from django.shortcuts import render
from .models import Notification
from .serializers import Notification
from core.mixins import IsolateToUserMixin

class NotificationListAPIView(IsolateToUserMixin, generics.ListAPIView):
    """
    GET /api/notifications/  --> List ONLY my notifications (newest first)
    No POST here — notifications are created by signals, not by users.
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()
    serializer_class = Notification

class NotificationUpdateAPIView(IsolateToUserMixin, generics.RetrieveUpdateAPIView):
    """
    GET   /api/notifications/<pk>/  --> One of my notifications
    PATCH /api/notifications/<pk>/  --> Mark as read: {"is_read": true}
    """
    queryset = Notification.objects.all()
    serializer_class = Notification
    permission_classes = [permissions.IsAuthenticated]
