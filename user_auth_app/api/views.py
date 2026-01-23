"""REST API views for authentication and token management.

Provides registration, login and logout endpoints used by the front-end
clients. Uses token-based authentication provided by
`rest_framework.authtoken`.
"""

from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer
from rest_framework.permissions import IsAuthenticated


class RegistrationView(generics.CreateAPIView):
    """Endpoint for user registration creating a new User."""
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    """Authenticate user credentials and return an auth token."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Validate credentials and return token, fullname and email."""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                "token": token.key,
                "fullname": user.first_name,
                "email": user.email,
                "user_id": user.id
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """Invalidate the requesting user's authentication token."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Delete the user's token or return a not-found error."""
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response(
                {"message": "Successfully logged out"},
                status=status.HTTP_200_OK
            )
        except Token.DoesNotExist:
            return Response(
                {"error": "Token not found"},
                status=status.HTTP_400_BAD_REQUEST
            )
