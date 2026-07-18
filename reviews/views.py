from rest_framework import generics, permissions
from core.mixins import IsolateToUserMixin
from .models import Review
from .serializers import ReviewSerializer, ReviewPublicSerializer


class ListAndCreateAPIView(IsolateToUserMixin, generics.ListCreateAPIView):
    """
    GET  /api/reviews/  --> List ONLY my reviews
    POST /api/reviews/  --> Create a review (user comes from JWT)
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]


class DetailAndUpdateAndDeleteAPIView(IsolateToUserMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/reviews/<pk>/  --> One of MY reviews
    PATCH  /api/reviews/<pk>/  --> e.g. {"rating": 4}
    DELETE /api/reviews/<pk>/  --> Delete my review
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]


class MovieReviewsListAPIView(generics.ListAPIView):
    """
    GET /api/movies/<movie_id>/reviews/  --> ALL users' reviews for ONE movie.
    Read-only, and deliberately WITHOUT IsolateToUserMixin: this is the public
    "movie page" view — everyone's opinions, visible to any logged-in user.
    (Isolation is a choice, not a default — here the point is sharing.)
    """
    serializer_class = ReviewPublicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        KWARGS: is used to capture the named arguments inside any function or from url.
        kwargs itself a dictionary that hold the record.
        Like in current scenrio kwargs is: {'movie_id': 2}, its type of object that holds everything inside it.
        For JS: its seems like object destruction, or rest operator
         """
        # self.kwargs = named parameters from the URL — like useParams() in
        # React Router. 'movie_id' matches the name in the path() pattern.
        return Review.objects.filter(movie_id=self.kwargs['movie_id'])
