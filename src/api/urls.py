# src/api/urls.py

from django.urls import path
from accounts.views import UserRegistrationView, UserProfileView
from categories.views import CategoryListView
from listings.views import (
    ListingListCreateView,
    ListingDetailView,
    MyListingsView, # <--- Import the new view
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'api'

urlpatterns = [
    # --- Authentication & User Profile ---
    path(
        'auth/register/',
        UserRegistrationView.as_view(),
        name='register'
    ),
    path(
        'auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair' # Login endpoint
    ),
    path(
        'auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh' # Refresh the access token
    ),
    path(
        'users/me/',
        UserProfileView.as_view(),
        name='user_profile' # The "me" endpoint
    ),
    # --- ADDING NEW ENDPOINT HERE ---
    path(
        'users/me/listings/',
        MyListingsView.as_view(),
        name='my-listings' # Endpoint for the current user's listings
    ),


    # --- Content & Taxonomy ---
    path(
        'categories/',
        CategoryListView.as_view(),
        name='category-list'
    ),

    # --- Listings ---
    path(
        'listings/',
        ListingListCreateView.as_view(), # Handles GET (list) and POST (create)
        name='listing-list-create'
    ),
    path(
        'listings/<slug:slug>/', # Captures the slug from the URL
        ListingDetailView.as_view(), # Handles GET (retrieve), PUT/PATCH (update), DELETE
        name='listing-detail'
    ),
]