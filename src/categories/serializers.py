# src/categories/serializers.py

from rest_framework import serializers
from .models import Category

# =================================================================
#  CATEGORY SERIALIZER (RECURSIVE)
# =================================================================

class CategorySerializer(serializers.ModelSerializer):
    """
    A recursive serializer for the Category model to handle nested children.
    """
    # We define 'children' here. It will use this same serializer to represent
    # any child categories, creating the nested tree structure.
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'parent', # The ID of the parent category
            'children'
        ]
        # We can also add 'read_only_fields' if we want to prevent modification
        # through this serializer, but for now, this is fine.

    def get_children(self, obj):
        """
        This method gets all the direct children of the category instance 'obj'
        and serializes them using this same CategorySerializer.
        """
        # We only want to serialize children if they exist
        if obj.get_children():
            return CategorySerializer(obj.get_children(), many=True).data
        return None # Return None or an empty list if there are no children