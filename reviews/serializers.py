from rest_framework import serializers
from .models import Review
from movies.serializers import MovieSerializer


class ReviewSerializer(serializers.ModelSerializer):

    # Nested serializer for rich response (read-only), same pattern as movie_detail in watchlist
    movie_detail = MovieSerializer(source='movie', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'movie', 'movie_detail', 'rating', 'text', 'created_at']
        read_only_fields = ['created_at']
