# src/moderation/admin.py

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _ 
from .models import Report

# =================================================================
#  REPORT ADMIN
# =================================================================

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Report model.
    """
    list_display = (
        'reported_object_link',
        'reporter',
        'status',
        'created_at',
    )
    list_filter = ('status', 'content_type', 'created_at')
    search_fields = (
        'reporter__email',
        'reporter__username',
        'reason',
        'object_id',
    )
    readonly_fields = (
        'reporter',
        'reason',
        'reported_object_link',
        'created_at',
        'updated_at',
    )
    # We organize the fields into sections for clarity
    fieldsets = (
        (_("Report Details"), {
            'fields': ('reporter', 'reason', 'reported_object_link')
        }),
        (_("Moderation"), {
            'fields': ('status', 'moderator_notes')
        }),
        (_("Timestamps"), {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def reported_object_link(self, obj):
        """

        Creates a clickable link to the reported item's admin change page.
        """
        if obj.content_object:
            admin_url = reverse(
                f'admin:{obj.content_type.app_label}_{obj.content_type.model}_change',
                args=(obj.object_id,)
            )
            return format_html('<a href="{}">{}</a>', admin_url, obj.content_object)
        return _("Object no longer exists")
    reported_object_link.short_description = _("Reported Item")

    def has_add_permission(self, request):
        # Reports should be created by users, not admins.
        return False

