# src/listings/permissions.py

from rest_framework import permissions

# =================================================================
#  CUSTOM PERMISSIONS
# =================================================================

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Read-only access is allowed for any request.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the listing.
        # 'obj' is the Listing instance here.
        return obj.owner == request.user