# src/content/admin.py

from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import StaticPage

# =================================================================
#  STATIC PAGE ADMIN
# =================================================================

@admin.register(StaticPage)
class StaticPageAdmin(TabbedTranslationAdmin):
    """
    Admin configuration for the StaticPage model,
    using TabbedTranslationAdmin for easy language management.
    """
    list_display = ('title', 'slug', 'is_published', 'updated_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'slug', 'content')
    prepopulated_fields = {'slug': ('title',)} # Automatically creates slug from title