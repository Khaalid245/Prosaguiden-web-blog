from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    RegisterSerializer,
    VerifiedTokenObtainPairSerializer
)
from .emails import send_verification_email

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    Handles user registration.
    - Creates user
    - Sends verification email
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        send_verification_email(user)


class VerifyEmailView(APIView):
    """
    Handles email verification.
    - Validates token
    - Prevents fake URLs
    - Prevents double verification
    """

    def get(self, request, uid, token):
        user = get_object_or_404(User, id=uid)

        # ✅ Prevent double verification
        if user.is_verified:
            return Response(
                {"message": "Email already verified."},
                status=200
            )

        # 🔒 Validate token
        if not default_token_generator.check_token(user, token):
            return Response(
                {"error": "Invalid or expired verification link."},
                status=400
            )

        # ✅ Verify user
        user.is_verified = True
        user.save()

        # ✅ Optional frontend redirect
        # return redirect("http://localhost:3000/email-verified")

        return Response(
            {"message": "Email verified successfully!"},
            status=200
        )


# 🔒 ADDED: Custom login view that blocks unverified users
class LoginView(TokenObtainPairView):
    serializer_class = VerifiedTokenObtainPairSerializer
