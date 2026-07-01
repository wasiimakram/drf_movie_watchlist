from rest_framework import generics
from .models import Movie
from .serializers import MovieSerializer

class MovieListAndCreateAPIView(generics.ListCreateAPIView):

    """
    GET /api/movies --> List all movies
    POST /api/movies --> Create a new movie
    """

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieDetailAndUpdateAndDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):

    """
    GET: Retrieve specific movie
    PUT/PATCH: Update movie
    PATCH: In patch, we can only pass specific value that needs to be updated
    PUT: In PUT we need to send the whole object to update even 1 value.
    DELETE: Delete movie
    """

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer