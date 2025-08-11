# src/settings/admin.py

from django.contrib import admin
from solo.admin import SingletonModelAdmin
from django.utils.translation import gettext_lazy as _ 
from .models import SiteSettings

# =================================================================
#  SITE SETTINGS ADMIN (SINGLETON)
# =================================================================

@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonModelAdmin):
    """
    Admin configuration for the singleton SiteSettings model.
    """
    # We can group fields into fieldsets for a cleaner layout
    fieldsets = (
        (_("General Settings"), {
            'fields': ('site_name', 'contact_email')
        }),
        (_("Social Media"), {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url')
        }),
        (_("Maintenance"), {
            'fields': ('maintenance_mode',)
        }),
    )