from rest_framework import serializers
from .models import Movie
from categories.serializers import CategorySerializer

class MovieSerializer(serializers.ModelSerializer):

    # Nested serializer for rich response (Read-only)
    category_detail = CategorySerializer(source='category', many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'year', 'category', 'category_detail', 'director', 'plot',
            'poster_url', 'imdb_rating', 'runtime_minutes',
            'language', 'country', 'created_at'
        ]
        read_only_fields = ['created_at']