from django.db import models
from django.conf import settings

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # date + time, so "2 hours ago" works

    class Meta:
        ordering = ["-created_at"] # newest first

    def __str__(self):
        #f like a JS template literal `${user} - ${message}`
        return f'{self.user} - {self.message}'