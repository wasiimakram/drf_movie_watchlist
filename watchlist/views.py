from rest_framework import generics, permissions
from core.mixins import IsolateToUserMixin
from .models import Watchlist
from .serializers import WatchlistSerializer

# We are adding Custom Mixin in our class
class ListAndCreateAPIView(IsolateToUserMixin, generics.ListCreateAPIView):
    """
    GET  /api/watchlist/  --> List ONLY my watchlist items
    POST /api/watchlist/  --> Add a movie to MY watchlist
    """
    # .all() is just the starting point — the mixin narrows it to the current user
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]


class DetailAndUpdateAndDeleteAPIView(IsolateToUserMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/watchlist/<pk>/  --> One of MY items
    PATCH  /api/watchlist/<pk>/  --> e.g. {"status": "watched"}
    DELETE /api/watchlist/<pk>/  --> Remove from my list
    """
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]
