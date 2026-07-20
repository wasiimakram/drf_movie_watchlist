from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, permissions
from .models import Category
from .serializers import CategorySerializer


@method_decorator(cache_page(60), name='get')  # cache GET responses for 60s
class CategoryListAndCreateAPIView(generics.ListCreateAPIView):
    """
    GET  /api/categories/   -> List all categories
    POST /api/categories/   -> Create a new category
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # Catalog rule: GET for any authenticated user; POST/PUT/PATCH/DELETE only
    # with model permissions (add/change/delete_category) — admin has them all.
    permission_classes = [permissions.DjangoModelPermissions]

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
    # Catalog rule: GET for any authenticated user; POST/PUT/PATCH/DELETE only
    # with model permissions (add/change/delete_category) — admin has them all.
    permission_classes = [permissions.DjangoModelPermissions]
