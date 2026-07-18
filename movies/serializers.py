from rest_framework import serializers
from django.db.models import Avg
from .models import Movie
from categories.serializers import CategorySerializer
from datetime import date


class MovieSerializer(serializers.ModelSerializer):

    # Nested serializer for rich response (Read-only)
    category_detail = CategorySerializer(source='category', many=True, read_only=True)

    # Computed field — not in the database, calculated fresh on every response.
    # No need for read_only_fields: a SerializerMethodField is read-only by nature
    # (read_only_fields only applies to fields auto-built from the model).
    # And no migration risk: makemigrations reads ONLY models.py, never serializers —
    # model = database schema, serializer = shape of the JSON response.
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'year', 'category', 'category_detail', 'average_rating',
            'director', 'plot', 'poster_url', 'poster', 'imdb_rating', 'runtime_minutes',
            'language', 'country', 'created_at'
        ]
        read_only_fields = ['created_at']

    # ------ Method Field ------------
    # DRF finds this by name: get_ + average_rating
    def get_average_rating(self, obj):
        # obj = the Movie currently being turned into JSON.
        #
        # obj.reviews = the REVERSE side of the FK (related_name='reviews' on Review.movie):
        # "all Review rows pointing at this movie" == Review.objects.filter(movie=obj).
        #
        # Avg = Django aggregate function (Count, Sum, Avg, Min, Max) — becomes real SQL:
        #   SELECT AVG(rating) FROM reviews_review WHERE movie_id = <obj.id>;

        avg = obj.reviews.aggregate(value=Avg('rating'))['value']
        return round(avg, 1) if avg is not None else None  # None = no reviews yet

    # ------ Validations Methods --------
    def validate_year(self, value):
        # DRF calls this automatically because of the name: validate_ + year
        current_year = date.today().year
        if value < 1888:
            raise serializers.ValidationError('Year cannot be before 1888 (the first film ever made).')
        if value > current_year:
            raise serializers.ValidationError(f'Year cannot be in the future (max {current_year}).')
        return value  # value is valid — always return it

    def validate_imdb_rating(self, value):
        # This field allows null, so value can be None — only check real values
        if value is not None and (value < 0 or value > 10):
            raise serializers.ValidationError('IMDb rating must be between 0 and 10.')
        return value

    def validate_runtime_minutes(self, value):
        # Also nullable — same None guard
        if value is not None and value <= 0:
            raise serializers.ValidationError('Runtime must be a positive number of minutes.')
        return value

    def validate_category(self, value):
        # For a ManyToMany field, value arrives as a LIST of categories
        if not value:
            raise serializers.ValidationError('Pick at least one category.')
        return value


class MovieListSerializer(serializers.ModelSerializer):
    """
    LIGHT serializer — used ONLY for the list endpoint (GET /api/movies/).
    A list screen shows movie cards, so we send just card-sized data:
    no plot, no poster_url, no language/country.
    The full MovieSerializer above stays in charge of detail + create/update.
    """

    category_detail = CategorySerializer(source='category', many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'director', 'poster', 'imdb_rating', 'average_rating', 'category_detail']

    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(value=Avg('rating'))['value']
        return round(avg, 1) if avg is not None else None