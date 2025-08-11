# src/advertising/admin.py

from django.contrib import admin
from .models import Banner

# =================================================================
#  BANNER ADMIN
# =================================================================

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Banner model.
    """
    list_display = ('name', 'url', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'url')
    readonly_fields = ('created_at', 'updated_at')