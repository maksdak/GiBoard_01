# src/security/admin.py

from django.contrib import admin
from .models import UserActivityLog

# =================================================================
#  USER ACTIVITY LOG ADMIN
# =================================================================

@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserActivityLog.
    This model must be strictly read-only for data integrity.
    """
    list_display = ('timestamp', 'user', 'action', 'ip_address')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'user__email', 'ip_address', 'details')

    # Make all fields read-only
    readonly_fields = [f.name for f in UserActivityLog._meta.get_fields()]

    def has_add_permission(self, request):
        # Prevent manual creation of log entries
        return False

    def has_change_permission(self, request, obj=None):
        # Prevent editing of log entries
        return False

    def has_delete_permission(self, request, obj=None):
        # Optional: Prevent deletion of log entries for a strict audit trail.
        # Set to True if you want admins to be able to clear old logs.
        return False