from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
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


class ActivateAccountAPIView(APIView):
    """
    GET /api/auth/activate/<uidb64>/<token>/  --> flip is_active to True.
    AllowAny: the user clicking the email link is not logged in yet.
    uidb64 + token are the two parts the signal put into the link.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        # Step 1: unpack the user id ('Nw' -> b'7' -> '7') and find the user.
        try:
            user = User.objects.get(pk=urlsafe_base64_decode(uidb64).decode())
        except (User.DoesNotExist, ValueError):
            return Response({'detail': 'Invalid activation link.'}, status=status.HTTP_400_BAD_REQUEST)

        # Step 2: verify the secret. check_token redoes the same math the
        # signal did — matches only if the link is genuine AND still fresh.
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'detail': 'Account activated. You can log in now.'})

        return Response({'detail': 'Invalid or expired activation link.'}, status=status.HTTP_400_BAD_REQUEST)
