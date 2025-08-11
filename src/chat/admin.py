# src/chat/admin.py

from django.contrib import admin
from .models import Conversation, Message

# =================================================================
#  MESSAGE INLINE ADMIN
# =================================================================

class MessageInline(admin.TabularInline):
    """
    Allows viewing and editing messages directly within the conversation view.
    This is mostly for read-only purposes.
    """
    model = Message
    extra = 0  # Don't show any empty extra forms for new messages
    readonly_fields = ('sender', 'content', 'timestamp', 'is_read')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        # Prevent adding messages from the admin
        return False

# =================================================================
#  CONVERSATION ADMIN
# =================================================================

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Conversation model.
    """
    list_display = ('id', 'participant_list', 'updated_at')
    search_fields = ('participants__username', 'participants__email')
    filter_horizontal = ('participants',) # A better widget for ManyToMany fields
    inlines = [MessageInline] # This is where we embed the message view

    def participant_list(self, obj):
        return ", ".join([p.username for p in obj.participants.all()])
    participant_list.short_description = 'Participants'