# src/categories/views.py

from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Category
from .serializers import CategorySerializer

# =================================================================
#  API VIEWS
# =================================================================

class CategoryListView(generics.ListAPIView):
    """
    API endpoint to list all top-level categories.
    Child categories are nested recursively within their parents.
    """
    # We only want to fetch categories that are at the root of the tree.
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny] # Anyone can view the categories