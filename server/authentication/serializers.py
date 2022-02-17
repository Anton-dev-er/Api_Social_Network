from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class RegSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email:
            raise serializers.ValidationError('Email is required')

        if not password:
            raise serializers.ValidationError('Password is required')

        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError('Not found')

        if not user.is_active:
            raise serializers.ValidationError('Is not active')

        data["token"] = user.token
        return data
