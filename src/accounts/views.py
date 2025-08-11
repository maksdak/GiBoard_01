# src/accounts/views.py

from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated # <--- Import IsAuthenticated
from .serializers import UserRegistrationSerializer, UserSerializer # <--- Import UserSerializer

User = get_user_model()

# =================================================================
#  API VIEWS
# =================================================================

class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for creating (registering) a new user.
    Accessible by anyone (no authentication required).
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating the authenticated user's profile.
    Requires authentication.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,) # <-- Only logged-in users can access this

    def get_object(self):
        """
        This method overrides the default behavior to always return
        the currently authenticated user.
        """
        return self.request.user