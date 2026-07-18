from rest_framework import serializers
from .models import Review
from movies.serializers import MovieSerializer


class ReviewSerializer(serializers.ModelSerializer):

    # Nested serializer for rich response (read-only), same pattern as movie_detail in watchlist
    movie_detail = MovieSerializer(source='movie', read_only=True)

    # declare the Star field, Computed field
    stars = serializers.SerializerMethodField()

    # Stars is a computed field, that does not exist in db but we will
    # calculate at time of response sending
    class Meta:
        model = Review
        fields = ['id', 'movie', 'movie_detail', 'rating', 'stars', 'text', 'created_at']
        read_only_fields = ['created_at']

    def get_stars(self, obj):
        # Build a 5-star string from the rating, e.g. rating=4 -> '★★★★☆'
        # step-1: multiple filled star with rating value
        # step-2: multiple empty stars with minus value from rating
        # step-3: combine them.
        
        return '★' * obj.rating + '☆' * (5 - obj.rating)

    def validate_rating(self, value):
        # DRF calls this automatically: validate_ + rating
        if value < 1 or value > 5:
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value


class ReviewPublicSerializer(ReviewSerializer):
    """
    Public listing for /api/movies/<movie_id>/reviews/ — WHO said WHAT.
    No movie fields: the URL already says which movie we're looking at.
    Inherits stars + get_stars from ReviewSerializer for free.
    """

    # source= walks the FK: review.user.username (same idea as source='movie',
    # just one step deeper). read_only — usernames are display data here.
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta(ReviewSerializer.Meta):
        fields = ['id', 'username', 'rating', 'stars', 'text', 'created_at']
