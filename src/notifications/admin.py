# src/notifications/admin.py

from django.contrib import admin
from django.utils.translation import gettext_lazy as _ 
from .models import Notification

# =================================================================
#  NOTIFICATION ADMIN
# =================================================================

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Notification model.
    """
    list_display = (
        'recipient',
        'message_summary',
        'is_read',
        'created_at',
    )
    list_filter = ('is_read', 'created_at')
    search_fields = ('recipient__username', 'recipient__email', 'message')
    readonly_fields = (
        'recipient',
        'message',
        'related_object',
        'created_at'
    )
    
    # We can allow admins to mark notifications as read/unread
    # 'is_read' is not in readonly_fields

    def message_summary(self, obj):
        # To avoid cluttering the list view with long messages
        return obj.message[:75] + '...' if len(obj.message) > 75 else obj.message
    message_summary.short_description = _("Message")