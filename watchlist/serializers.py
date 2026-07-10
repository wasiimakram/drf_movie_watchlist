from rest_framework import serializers
from .models import Watchlist
from movies.serializers import MovieSerializer


class WatchlistSerializer(serializers.ModelSerializer):

    # Nested serializer for rich response (read-only), same pattern as category_detail in movies
    movie_detail = MovieSerializer(source='movie', read_only=True)

    class Meta:
        model = Watchlist
        fields = ['id', 'movie', 'movie_detail', 'status', 'watched_at', 'notes', 'added_at']
        read_only_fields = ['added_at', 'watched_at']
