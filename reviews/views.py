from rest_framework import generics, permissions
from core.mixins import IsolateToUserMixin
from .models import Review
from .serializers import ReviewSerializer


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
