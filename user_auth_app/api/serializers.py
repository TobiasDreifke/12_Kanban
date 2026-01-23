"""Serializers for authentication API endpoints.

Handle registration and login payloads, validation and token creation.
These serializers convert between Django `User` instances and the JSON
represented shape expected by clients.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer handling user registration and token creation."""
    fullname = serializers.CharField(
        source='first_name')
    repeated_password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()
    user_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'fullname', 'email',
                  'password', 'repeated_password', 'token']
        extra_kwargs = {'password': {'write_only': True}}

    def get_token(self, obj):
        """Return or create an authentication token for the user."""
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key

    def validate(self, data):
        """Validate passwords match and that the email is unique."""
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError("Passwords must match.")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists.")
        return data

    def create(self, validated_data):
        """Create a new user from validated registration data."""
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name']
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for validating login credentials."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Authenticate credentials and attach the user to validated data."""
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError(
                    "Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError(
                "Must include 'email' and 'password'.")

        data['user'] = user
        return data
