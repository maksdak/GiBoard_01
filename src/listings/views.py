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
    - GET: returns a list of all active listings.
    - POST: creates a new listing.
    """
    queryset = Listing.objects.filter(is_active=True).select_related(
        'owner', 'category', 'city'
    ).prefetch_related('images')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ListingCreateSerializer
        return ListingSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a single listing by its slug.
    - GET: retrieve a listing.
    - PUT/PATCH: update a listing.
    - DELETE: delete a listing.
    """
    queryset = Listing.objects.all().select_related(
        'owner', 'category', 'city'
    ).prefetch_related('images')
    
    serializer_class = ListingSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'slug'


class MyListingsView(generics.ListAPIView):
    """
    API endpoint to list all listings owned by the currently authenticated user.
    """
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated] # Only logged-in users can see their listings

    def get_queryset(self):
        """
        This view should return a list of all the listings
        for the currently authenticated user.
        """
        user = self.request.user
        return Listing.objects.filter(owner=user).select_related(
            'owner', 'category', 'city'
        ).prefetch_related('images').order_by('-created_at')