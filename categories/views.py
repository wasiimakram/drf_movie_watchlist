from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Category
from .serializers import CategorySerializer


class CategoryListAndCreateAPIView(generics.ListCreateAPIView):
    """
    GET  /api/categories/   -> List all categories
    POST /api/categories/   -> Create a new category
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class CategoryDetailAndUpdateAndDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve specific category
    PUT/PATCH: Update category
    Patch: In patch, we can only pass specific value that needs to be updated
    PUT: In PUT we need to send the whole object to update even 1 value.
    DELETE: Delete category
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
