from django.db import models
from categories.models import Category

class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    # If we M2M relationship, then we will use this approach. It will not add
    # category_id in movies table, but will create a pivot table for it.
    category = models.ManyToManyField(Category, related_name='movies')
    director = models.CharField(max_length=200)
    plot = models.TextField(blank=True)
    poster_url = models.URLField(blank=True)
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    runtime_minutes = models.IntegerField(null=True, blank=True)
    language = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title