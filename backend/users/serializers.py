from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
import re

from .emails import send_verification_email

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Handles user registration with strong password validation
    and sends verification email.
    """
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'role']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "An account with this email already exists."
            )
        return value

    def validate_password(self, value):
        """
        Strong password rules
        """
        errors = []

        if len(value) < 8:
            errors.append("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            errors.append("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            errors.append("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', value):
            errors.append("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', value):
            errors.append("Password must contain at least one special symbol.")

        try:
            validate_password(value)
        except ValidationError as e:
            errors.extend(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')

        # ✅ User created but NOT verified
        user = User.objects.create_user(**validated_data)
        user.is_verified = False
        user.save()

        # ✅ Send verification email
        send_verification_email(user)

        return user


# 🔒 ADDED: Custom JWT serializer to block unverified users
class VerifiedTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Prevents login if email is not verified.
    """

    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_verified:
            raise AuthenticationFailed(
                "Please verify your email before logging in."
            )

        return data
