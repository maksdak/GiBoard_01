# src/listings/serializers.py

from rest_framework import serializers
from .models import Listing, ListingImage
from accounts.serializers import UserSerializer # To show owner details

# =================================================================
#  LISTING IMAGE SERIALIZER
# =================================================================

class ListingImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the ListingImage model.
    """
    class Meta:
        model = ListingImage
        fields = ('id', 'image')


# =================================================================
#  LISTING SERIALIZER (FOR LIST AND DETAIL VIEWS)
# =================================================================

class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying a list of listings or a single listing's details.
    It provides rich, readable information about related models.
    """
    # Use the UserSerializer to show nested owner details instead of just an ID
    owner = UserSerializer(read_only=True)

    # Use a simple string representation for related fields
    category = serializers.StringRelatedField()
    city = serializers.StringRelatedField()

    # Use the ListingImageSerializer for the nested images
    images = ListingImageSerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = (
            'id',
            'title',
            'slug',
            'description',
            'price',
            'is_active',
            'owner',
            'category',
            'city',
            'images', # This will be a list of image objects
            'created_at',
            'updated_at',
        )


# =================================================================
#  LISTING CREATE SERIALIZER (FOR WRITING NEW LISTINGS)
# =================================================================

class ListingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new listing.
    This serializer handles write operations.
    """
    class Meta:
        model = Listing
        # These are the fields a user submits when creating a listing.
        # The 'owner' will be set automatically in the view.
        # The 'slug' is generated automatically in the model's save() method.
        fields = (
            'title',
            'description',
            'price',
            'category',
            'city',
        )