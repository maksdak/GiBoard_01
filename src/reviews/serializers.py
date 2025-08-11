# src/reviews/serializers.py

from rest_framework import serializers
from .models import Review
from accounts.serializers import UserSerializer

# =================================================================
#  REVIEW SERIALIZER (FOR DISPLAYING REVIEWS)
# =================================================================

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying a list of reviews.
    Includes nested author information for a rich display.
    """
    author = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            'id',
            'listing',
            'author',
            'rating',
            'comment',
            'created_at',
        )


# =================================================================
#  REVIEW CREATE SERIALIZER (FOR WRITING NEW REVIEWS)
# =================================================================

class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new review.
    The 'author' and 'listing' will be set automatically in the view.
    """
    class Meta:
        model = Review
        fields = ('rating', 'comment')