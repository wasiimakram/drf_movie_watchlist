from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):

    # write_only = Its means password will part of POST/PUT and will not shown in GET
    # min_length: min pass length
    password = serializers.CharField(write_only=True, min_length=8)

    # User.email is optional in Django's model — we make it required for signup
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def validate_email(self, value):
        # Django allows duplicate emails by default — we don't
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('An account with this email already exists.')
        return value

    def create(self, validated_data):
        # create_user() HASHES the password before saving.
        # (User.objects.create() would store it as readable text — never that!)
        return User.objects.create_user(**validated_data)
