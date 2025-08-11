# src/accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model

# Get the custom user model
User = get_user_model()

# =================================================================
#  USER SERIALIZER (FOR DISPLAYING USER DATA)
# =================================================================

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying user information safely.
    """
    class Meta:
        model = User
        fields = (
            'public_id',
            'username',
            'email',
            'avatar',
            'date_joined'
        )
        read_only_fields = ('public_id', 'date_joined')


# =================================================================
#  USER REGISTRATION SERIALIZER (FOR CREATING NEW USERS)
# =================================================================

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for handling new user registration.
    """
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        """
        Check that the two password fields match.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        """
        Create and return a new user with a hashed password.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user