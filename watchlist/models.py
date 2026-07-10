from django.conf import settings
from django.db import models
from movies.models import Movie

STATUS_CHOICES = [
    ('want_to_watch', 'Want to watch'),
    ('watching', 'Watching'),
    ('watched', 'Watched'),
]

class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watchlist_items')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watchlist_entries')
    added_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='want_to_watch')  # 3 states: want_to_watch / watching / watched
    watched_at = models.DateTimeField(null=True, blank=True)  # set when status becomes 'watched'
    notes = models.TextField(max_length=255, blank=True)

    class Meta:
        unique_together = ('user', 'movie')  # one user can add a movie only once
        ordering = ['-added_at']

    def __str__(self):
        return f'{self.user} - {self.movie} ({self.status})'
