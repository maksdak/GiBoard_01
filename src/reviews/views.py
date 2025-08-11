# src/reviews/views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Review
from listings.models import Listing
from .serializers import ReviewSerializer, ReviewCreateSerializer

# =================================================================
#  API VIEWS
# =================================================================

class ReviewListCreateView(generics.ListCreateAPIView):
    """
    API endpoint that allows reviews for a listing to be viewed or created.
    - GET: returns a list of all reviews for a specific listing.
    - POST: creates a new review for a specific listing.
    """
    def get_queryset(self):
        """
        This view should return a list of all the reviews
        for the listing as determined by the listing_slug portion of the URL.
        """
        listing_slug = self.kwargs['listing_slug']
        return Review.objects.filter(listing__slug=listing_slug).select_related('author')

    def get_serializer_class(self):
        """
        Use ReviewCreateSerializer for writing, and ReviewSerializer for reading.
        """
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewSerializer

    def get_permissions(self):
        """
        - Anyone can view reviews (GET).
        - Only authenticated users can create reviews (POST).
        """
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        """
        Custom logic for creating a new review.
        """
        listing_slug = self.kwargs['listing_slug']
        try:
            listing = Listing.objects.get(slug=listing_slug)
        except Listing.DoesNotExist:
            raise ValidationError("Listing does not exist.")

        user = self.request.user

        # --- Business Logic Checks ---
        if listing.owner == user:
            raise ValidationError("You cannot review your own listing.")

        if Review.objects.filter(listing=listing, author=user).exists():
            raise ValidationError("You have already reviewed this listing.")

        # If all checks pass, save the review
        serializer.save(author=user, listing=listing)