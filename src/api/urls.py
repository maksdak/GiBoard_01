# src/api/urls.py

from django.urls import path
from accounts.views import UserRegistrationView, UserProfileView
from categories.views import CategoryListView
from listings.views import ListingListCreateView, ListingDetailView # <--- Import the combined view
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
        name='token_obtain_pair' # This is the "login" endpoint
    ),
    path(
        'auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh' # This is for refreshing the access token
    ),
    path(
        'users/me/',
        UserProfileView.as_view(),
        name='user_profile' # The "me" endpoint
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
        ListingListCreateView.as_view(), # <-- Point to the combined view
        name='listing-list-create'
    ),
    path(
        'listings/<slug:slug>/', # This captures the slug from the URL
        ListingDetailView.as_view(),
        name='listing-detail'
    ),
]