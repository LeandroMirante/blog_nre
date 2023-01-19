from rest_framework import serializers
from app.users.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from app.users.base64 import Base64ImageField


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    profile_picture = Base64ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = User
        fields = ["profile_picture", "email", "name", "phone", "birth_date", "password"]

    def validade(self, attrs):
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=3, write_only=True)
    tokens = serializers.CharField(max_length=68, min_length=3, read_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "tokens"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials")
        if not user.is_active:
            raise AuthenticationFailed("Account is not active")

        return {"email": user.email, "name": user.name, "tokens": user.tokens()}


class UserSerializer(serializers.ModelSerializer):
    profile_picture = Base64ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "profile_picture",
            "email",
            "name",
            "phone",
            "birth_date",
            "password",
        ]
