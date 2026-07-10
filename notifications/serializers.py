from rest_framework import serializers
from .models import Notification

class Meta:
    model = Notification
    fields = ['id', 'message', 'is_read', 'created_at']
    # Only is_read is editable — the user can mark as read, nothing else.
    # Notifications are CREATED by signals, never by the API.
    read_only_fields = ['message', 'created_at']