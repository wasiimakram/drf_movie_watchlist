from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .serializers import RegisterSerializer


class RegisterAPIView(generics.CreateAPIView):
    """
    POST /api/auth/register/  --> Create a new user account
    The ONE endpoint where anonymous visitors are welcome (AllowAny) —
    you cannot ask someone to be logged in before they have an account.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
