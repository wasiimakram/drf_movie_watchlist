from django.conf import settings
from django.db import models
from movies.models import Movie


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()  # 1 to 5 stars
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')  # one review per user per movie
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} - {self.movie} ({self.rating}/5)'
