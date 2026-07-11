from rest_framework import serializers
from .models import Watchlist
from movies.serializers import MovieSerializer
from reviews.serializers import ReviewSerializer
from reviews.models import Review


class ReviewInlineSerializer(ReviewSerializer):
    """
    Narrowed version of ReviewSerializer for nested input: just rating + text.
    The movie comes from the watchlist item, the user from the JWT — so the
    nested object must not ask for them. Inherits validate_rating for free.
    """
    class Meta(ReviewSerializer.Meta):
        fields = ['rating', 'text']


class WatchlistSerializer(serializers.ModelSerializer):

    # Nested serializer for rich response (read-only), same pattern as category_detail in movies
    movie_detail = MovieSerializer(source='movie', read_only=True)

    """
    Write-Nested-Serializer: The concept is same like we get nested object in details,
    If we want to Create the Nested object then this concept came.
    We can create a light weight serializer for it and can perform create.
    """
    # Writable nested field (concept #25) — NO read_only this time.
    # write_only = accepted in the request body, never shown in responses.
    # required=False = adding to watchlist without a review still works.
    review = ReviewInlineSerializer(required=False, write_only=True)

    class Meta:
        model = Watchlist
        fields = ['id', 'movie', 'movie_detail', 'status', 'watched_at', 'notes', 'review', 'added_at']
        read_only_fields = ['added_at', 'watched_at']

    """
    Scenerio: User marked the movie as watched, App display a Pop-up, you can write a review.
    User write a review and FE send the review object nested with PATCH request data.
    So, 1- get that review object from rerquest, 2- update watchlist data, 3- add review
    """
    def update(self, instance, validated_data):
        # PATCH = the "I watched it!" moment — this is where the UI pops up
        # the review box. Three steps: pop nested -> update parent -> create child.

        # 1. Pop the nested part OUT — take reviews from request object
        #    Like JS: const { review, ...rest } = validatedData
        review_data = validated_data.pop('review', None)

        # 2. Let DRF do the normal update of the watchlist row itself
        #    (super() = "next in line", same idea as in our mixin).
        instance = super().update(instance, validated_data)

        # 3. Create the child, reusing user + movie from the parent, so the
        #    review can never belong to a different person or movie.
        if review_data:
            # A review only makes sense on a watched movie.
            if instance.status != 'watched':
                raise serializers.ValidationError(
                    {'review': 'You can only review a movie marked as watched.'}
                )
            # one-review-per-movie rule ourselves (else: 500 IntegrityError).
            if Review.objects.filter(user=instance.user, movie=instance.movie).exists():
                raise serializers.ValidationError({'review': 'You already reviewed this movie.'})
            Review.objects.create(
                user=instance.user,
                movie=instance.movie,
                **review_data,
            )
        return instance
