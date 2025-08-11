# src/listings/views.py

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Listing
from .serializers import ListingSerializer, ListingCreateSerializer
from .permissions import IsOwnerOrReadOnly 

# =================================================================
#  API VIEWS
# =================================================================

class ListingListCreateView(generics.ListCreateAPIView):
    """
    API endpoint that allows listings to be viewed or created.
    - GET requests return a list of all active listings.
    - POST requests create a new listing.
    """
    # The queryset is for the 'list' (GET) part of the view.
    queryset = Listing.objects.filter(is_active=True).select_related(
        'owner', 'category', 'city'
    ).prefetch_related('images')

    def get_serializer_class(self):
        """
        Dynamically choose the serializer class.
        - Use ListingSerializer for 'GET' requests (reading).
        - Use ListingCreateSerializer for 'POST' requests (writing).
        """
        if self.request.method == 'POST':
            return ListingCreateSerializer
        return ListingSerializer

    def get_permissions(self):
        """
        Dynamically set permissions.
        - Anyone can 'GET' (view the list).
        - Only authenticated users can 'POST' (create).
        """
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        """
        Automatically set the owner of the listing to the current user on creation.
        """
        serializer.save(owner=self.request.user)


class ListingDetailView(generics.RetrieveAPIView):
    """
    API endpoint to retrieve a single listing by its slug.
    """
    queryset = Listing.objects.filter(is_active=True).select_related(
        'owner', 'category', 'city'
    ).prefetch_related('images')
    
    serializer_class = ListingSerializer
    permission_classes = [AllowAny]
    
    lookup_field = 'slug'