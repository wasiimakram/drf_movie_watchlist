from rest_framework import serializers
from .models import Category

# Serializer converts your Python model → JSON for the API response
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'created_at']
        read_on_fields = ['slug','created_at']