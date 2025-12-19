from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import re  # For regex checks

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
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
        Enforce classic complexity:
        - At least 8 characters
        - At least 1 uppercase letter
        - At least 1 lowercase letter
        - At least 1 number
        - At least 1 special symbol
        """
        errors = []

        # Length check
        if len(value) < 8:
            errors.append("Password must be at least 8 characters long.")

        # Uppercase letter
        if not re.search(r'[A-Z]', value):
            errors.append("Password must contain at least one uppercase letter.")

        # Lowercase letter
        if not re.search(r'[a-z]', value):
            errors.append("Password must contain at least one lowercase letter.")

        # Number
        if not re.search(r'[0-9]', value):
            errors.append("Password must contain at least one number.")

        # Special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            errors.append("Password must contain at least one special symbol (@#$ etc.).")

        # Django built-in password validators (optional, keeps previous checks)
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
        user = User.objects.create_user(**validated_data)
        return user
